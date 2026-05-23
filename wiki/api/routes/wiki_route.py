"""Wiki 知识库路由"""
from __future__ import annotations

import json
import os
import re
import subprocess
import markdown
import urllib.parse
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException

router = APIRouter(tags=["Wiki 知识库"])

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", "/mnt/d/projects/wiki"))
CACHE_FILE = WIKI_ROOT / "index-cache.json"


def load_cache():
    if not CACHE_FILE.exists():
        raise HTTPException(status_code=500, detail="索引缓存未找到")
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/stats")
async def get_wiki_stats():
    """知识库核心统计数据"""
    cache = load_cache()
    files = cache.get("files", {})
    edges = cache.get("edges", [])
    metadata = cache.get("metadata", {})

    type_counts = {}
    for meta in files.values():
        t = meta.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    total_files = len(files)
    total_edges = len(edges)
    frontmatter_ok = sum(1 for m in files.values() if m.get("title"))
    health_score = round((frontmatter_ok / max(total_files, 1)) * 80 + 20)

    recent = []
    for path, meta in list(files.items())[:10]:
        recent.append({
            "path": path,
            "title": meta.get("title", Path(path).stem),
            "type": meta.get("type", "unknown"),
            "tags": meta.get("tags", [])
        })

    return {
        "total_files": total_files,
        "total_edges": total_edges,
        "health_score": health_score,
        "type_distribution": type_counts,
        "recent_pages": recent,
        "metadata": metadata
    }


@router.get("/graph")
async def get_knowledge_graph():
    """图谱数据：节点和边"""
    cache = load_cache()
    nodes = []
    node_ids = set()
    for path, meta in cache.get("files", {}).items():
        nodes.append({
            "id": path,
            "title": meta.get("title", Path(path).stem),
            "type": meta.get("type", "unknown"),
            "tags": meta.get("tags", [])
        })
        node_ids.add(path)
    edges = []
    for edge in cache.get("edges", []):
        src = edge.get("from")
        tgt = edge.get("to")
        if not src or not tgt:
            continue
        matched_src = None
        matched_tgt = None
        for nid in node_ids:
            if nid.endswith("/" + src) or nid == src:
                matched_src = nid
            if nid.endswith("/" + tgt) or nid == tgt:
                matched_tgt = nid
        if matched_src and matched_tgt:
            edges.append({
                "source": matched_src,
                "target": matched_tgt
            })
    return {"nodes": nodes, "edges": edges}


@router.get("/search")
async def search_wiki(q: str = Query(..., description="搜索关键词")):
    """全局内容搜索"""
    try:
        search_paths = [
            str(WIKI_ROOT / "wiki"),
            str(WIKI_ROOT / "raw"),
            str(WIKI_ROOT / "my-learning-path"),
        ]
        result = subprocess.run(
            ["grep", "-rni", "--include=*.md", "--exclude-dir=node_modules", "--exclude-dir=.git", "--exclude-dir=.obsidian", q] + search_paths,
            capture_output=True, text=True, timeout=15
        )
        
        file_results = {}
        for line in result.stdout.strip().split("\n"):
            parts = line.split(":", 2)
            if len(parts) >= 3:
                filepath = parts[0]
                rel_path = filepath.replace(str(WIKI_ROOT) + "/", "")
                if rel_path not in file_results:
                    title = Path(rel_path).stem
                    file_results[rel_path] = {
                        "file": rel_path,
                        "title": title,
                        "line": parts[1],
                        "snippet": parts[2][:300]
                    }
        
        results = list(file_results.values())[:20]
        return {"total": len(results), "results": results}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="搜索超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}") from e


@router.get("/pages")
async def list_pages(limit: int = Query(50, ge=1, le=200)):
    """列出知识库页面"""
    try:
        search_dirs = ["wiki", "raw", "my-learning-path"]
        find_cmds = []
        for d in search_dirs:
            path = WIKI_ROOT / d
            if path.exists():
                find_cmds.extend(["-path", str(path) + "/*"])
        
        result = subprocess.run(
            ["find", str(WIKI_ROOT), "-name", "*.md", "-not", "-path", "*/.obsidian/*", "-not", "-path", "*/node_modules/*"] + find_cmds,
            capture_output=True, text=True, timeout=10
        )
        files = [f for f in result.stdout.strip().split("\n") if f][:limit]
        pages = []
        for f in files:
            rel = str(Path(f).relative_to(WIKI_ROOT))
            pages.append({"path": rel, "title": Path(f).stem})
        return {"total": len(pages), "pages": pages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取页面列表失败: {str(e)}") from e


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "cache_exists": CACHE_FILE.exists()}


async def _read_md_file(file_path):
    """读取 Markdown 文件并转换为 HTML"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    frontmatter[key.strip()] = val.strip()
            body = parts[2].strip()
    
    html = markdown.markdown(body, extensions=['fenced_code', 'tables', 'sane_lists'])
    return {"content": html, "frontmatter": frontmatter, "raw": body}


@router.get("/content")
async def get_content(path: str = Query("", description="页面路径")):
    """获取页面内容"""
    if not path:
        raise HTTPException(status_code=400, detail="缺少页面路径")
    
    path = urllib.parse.unquote(path)
    prev = None
    while prev != path:
        prev = path
        path = urllib.parse.unquote(path)
    if path.endswith(".md"):
        path = path[:-3]
    
    search_paths = [
        path,
        path.replace("wiki/", ""),
    ]
    
    # 尝试多种可能的位置
    possible_dirs = [
        WIKI_ROOT,
        WIKI_ROOT / "sources",
        WIKI_ROOT / "concepts", 
        WIKI_ROOT / "entities",
        WIKI_ROOT / "governance",
        WIKI_ROOT / "my-learning-path",
        WIKI_ROOT / "my-learning-path" / "practice",
        WIKI_ROOT / "raw",
    ]
    
    for sp in search_paths:
        # 尝试相对路径形式 (wiki/sources/xxx)
        if "/" in sp:
            parts = sp.split("/")
            if len(parts) >= 2:
                base = parts[0]
                rest = "/".join(parts[1:])
                for base_dir in possible_dirs:
                    if base == "wiki":
                        file_path = base_dir / f"{rest}.md"
                    else:
                        file_path = WIKI_ROOT / base / f"{rest}.md"
                    if file_path.exists():
                        return await _read_md_file(file_path)
        
        # 尝试直接路径
        for search_dir in possible_dirs:
            file_path = search_dir / f"{sp}.md"
            if file_path.exists():
                return await _read_md_file(file_path)
    
    raise HTTPException(
        status_code=404, 
        detail={
            "message": "页面未找到",
            "path": path,
            "hint": "请检查路径是否正确，或从首页重新浏览"
        }
    )