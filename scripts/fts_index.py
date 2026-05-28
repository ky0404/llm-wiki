#!/usr/bin/env python3
"""
Wiki FTS5 Indexer — 替换慢速 glob+read 扫描
用法:
  python3 fts_index.py build          # 全量重建索引
  python3 fts_index.py update         # 增量更新（只处理 mtime 变化的文件）
  python3 fts_index.py search <query> # 全文检索，毫秒级返回
  python3 fts_index.py stats          # 查看索引状态
"""

import sqlite3
import os
import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

# ── 配置区 ────────────────────────────────────────────────
WIKI_ROOT   = Path(__file__).parent.parent / "wiki"
RAW_ROOT    = Path(__file__).parent.parent / "raw"
DB_PATH     = Path(__file__).parent.parent / ".fts_index.db"
CACHE_PATH  = Path(__file__).parent.parent / "index-cache.json"
SCAN_DIRS   = [WIKI_ROOT, RAW_ROOT]           # 扫描目录
SKIP_DIRS   = {".gc_backups", ".git", "node_modules", "__pycache__"}
# ─────────────────────────────────────────────────────────


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_db(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS files (
            path       TEXT PRIMARY KEY,
            mtime      REAL,
            size       INTEGER,
            checksum   TEXT,
            indexed_at TEXT
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS wiki_fts USING fts5(
            path,
            title,
            tags,
            content,
            tokenize = 'unicode61 remove_diacritics 1'
        );

        CREATE TABLE IF NOT EXISTS links (
            src  TEXT,
            dst  TEXT,
            PRIMARY KEY (src, dst)
        );
    """)
    conn.commit()


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """提取 YAML frontmatter，返回 (meta, body)"""
    meta = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_block = text[3:end].strip()
            body = text[end + 4:].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    k = k.strip()
                    v = v.strip()
                    # 简单解析 tags: [a, b] 或 tags: a
                    if v.startswith("[") and v.endswith("]"):
                        meta[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",")]
                    else:
                        meta[k] = v.strip("'\"")
    return meta, body


def extract_wikilinks(text: str) -> list[str]:
    return re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]+)?\]\]', text)


def index_file(conn: sqlite3.Connection, path: Path) -> bool:
    """索引单个文件，返回是否实际写入"""
    try:
        stat = path.stat()
        path_str = str(path)

        row = conn.execute(
            "SELECT mtime, checksum FROM files WHERE path = ?", (path_str,)
        ).fetchone()

        text = path.read_text(encoding="utf-8", errors="replace")
        checksum = hashlib.md5(text.encode()).hexdigest()

        # 未变化则跳过
        if row and abs(row["mtime"] - stat.st_mtime) < 0.5 and row["checksum"] == checksum:
            return False

        meta, body = parse_frontmatter(text)
        title = meta.get("title") or path.stem
        tags  = " ".join(meta.get("tags", [])) if isinstance(meta.get("tags"), list) else str(meta.get("tags", ""))

        # 删除旧 FTS 行
        conn.execute("DELETE FROM wiki_fts WHERE path = ?", (path_str,))
        conn.execute("DELETE FROM links WHERE src = ?",    (path_str,))

        # 插入新 FTS 行
        conn.execute(
            "INSERT INTO wiki_fts(path, title, tags, content) VALUES (?, ?, ?, ?)",
            (path_str, title, tags, body[:50000])  # 限制单文件最大 50k 字符
        )

        # 提取并存储 wikilinks
        for dst in extract_wikilinks(text):
            conn.execute(
                "INSERT OR IGNORE INTO links(src, dst) VALUES (?, ?)",
                (path_str, dst)
            )

        # 更新文件记录
        conn.execute("""
            INSERT INTO files(path, mtime, size, checksum, indexed_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                mtime = excluded.mtime,
                size  = excluded.size,
                checksum = excluded.checksum,
                indexed_at = excluded.indexed_at
        """, (path_str, stat.st_mtime, stat.st_size, checksum, datetime.now().isoformat()))

        return True

    except Exception as e:
        print(f"  ⚠ 跳过 {path}: {e}", file=sys.stderr)
        return False


def build(incremental: bool = False):
    print(f"{'增量' if incremental else '全量'}构建 FTS 索引 → {DB_PATH}")
    conn = get_db()
    init_db(conn)

    if not incremental:
        conn.execute("DELETE FROM wiki_fts")
        conn.execute("DELETE FROM files")
        conn.execute("DELETE FROM links")
        conn.commit()

    updated = skipped = 0
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for md_path in scan_dir.rglob("*.md"):
            if any(skip in md_path.parts for skip in SKIP_DIRS):
                continue
            if index_file(conn, md_path):
                updated += 1
                print(f"  ✓ {md_path.relative_to(md_path.parent.parent)}")
            else:
                skipped += 1

    conn.commit()
    conn.execute("INSERT INTO wiki_fts(wiki_fts) VALUES('optimize')")  # FTS 优化
    conn.commit()
    conn.close()
    print(f"\n完成：更新 {updated} 个，跳过 {skipped} 个（未变化）")


def search(query: str, limit: int = 10, snippet_len: int = 30):
    """
    全文检索，支持：
      - 普通词：   RAG 向量
      - 短语：     "三混合 RAG"
      - 前缀：     LangGraph*
      - 布尔：     RAG AND 检索 NOT 幻觉
    """
    conn = get_db()
    init_db(conn)

    rows = conn.execute(f"""
        SELECT
            path,
            title,
            tags,
            snippet(wiki_fts, 3, '▶', '◀', '…', {snippet_len}) AS snippet,
            bm25(wiki_fts, 0, 2, 4, 1) AS score
        FROM wiki_fts
        WHERE wiki_fts MATCH ?
        ORDER BY score
        LIMIT ?
    """, (query, limit)).fetchall()

    conn.close()

    if not rows:
        print("无匹配结果")
        return []

    results = []
    for r in rows:
        results.append({
            "path":    r["path"],
            "title":   r["title"],
            "tags":    r["tags"],
            "snippet": r["snippet"],
            "score":   round(r["score"], 4),
        })
        print(f"[{r['title']}]  {r['snippet']}")
        print(f"  → {r['path']}\n")

    return results


def stats():
    conn = get_db()
    init_db(conn)
    n_files = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    n_links = conn.execute("SELECT COUNT(*) FROM links").fetchone()[0]
    db_size = DB_PATH.stat().st_size // 1024 if DB_PATH.exists() else 0
    conn.close()
    print(f"已索引文件: {n_files}")
    print(f"wikilinks:  {n_links}")
    print(f"数据库大小: {db_size} KB")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "build":
        build(incremental=False)
    elif cmd == "update":
        build(incremental=True)
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法: fts_index.py search <query>")
        else:
            search(" ".join(sys.argv[2:]))
    elif cmd == "stats":
        stats()
    else:
        print(__doc__)
