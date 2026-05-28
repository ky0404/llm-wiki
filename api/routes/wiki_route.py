"""Wiki 知识库路由"""
from __future__ import annotations

import json
import re
import subprocess
import markdown
import urllib.parse
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException

router = APIRouter(tags=["Wiki 知识库"])

WIKI_ROOT = Path("/home/dukkha/wiki")
WIKI_DATA_DIR = WIKI_ROOT / "wiki"
CACHE_FILE = WIKI_DATA_DIR / "index-cache.json"


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
                    file_results[rel_path] = {
                        "file": rel_path,
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


@router.post("/refresh")
async def refresh_cache():
    """手动刷新知识库索引缓存"""
    import time
    try:
        script_path = WIKI_ROOT / "scripts" / "generate_graph_and_cache.py"
        if not script_path.exists():
            raise HTTPException(status_code=500, detail="刷新脚本不存在")
        
        result = subprocess.run(
            ["python3", str(script_path)],
            cwd=str(WIKI_ROOT),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            logger.error(f"刷新缓存失败: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"刷新失败: {result.stderr}")
        
        return {"status": "ok", "message": "知识库索引已刷新", "output": result.stdout[:500]}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="刷新超时")
    except Exception as e:
        logger.error(f"刷新缓存异常: {e}")
        raise HTTPException(status_code=500, detail=f"刷新异常: {str(e)}")


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
    
    # 转换 wikilinks 为可点击链接
    def wikilink_to_html(match):
        link = match.group(1)
        # 格式: [[wiki/path|标题]] 或 [[wiki/path]]
        if "|" in link:
            path, title = link.split("|", 1)
        else:
            path = link
            title = path.split("/")[-1]
        
        # 转换为 URL 路径 (去掉 .md 后缀)
        url_path = path.replace(".md", "")
        # 转换为前端路由格式
        if url_path.startswith("wiki/"):
            url = "/" + url_path
        else:
            url = "/wiki/" + url_path
        
        return f'<a href="{url}" class="wiki-link">{title}</a>'
    
    # 匹配 [[wiki/path|标题]] 或 [[wiki/path]]
    html = re.sub(r'\[\[wiki/([^]]+)\]\]', wikilink_to_html, html)
    
    return {"content": html, "frontmatter": frontmatter, "raw": body}


@router.get("/content")
async def get_content(path: str = Query("", description="页面路径")):
    """获取页面内容"""
    if not path:
        raise HTTPException(status_code=400, detail="缺少页面路径")
    
    path = urllib.parse.unquote(path)
    if path.endswith(".md"):
        path = path[:-3]
    
    # 优先在 wiki/ 目录查找
    possible_dirs = [
        WIKI_DATA_DIR,
        WIKI_DATA_DIR / "sources",
        WIKI_DATA_DIR / "concepts", 
        WIKI_DATA_DIR / "entities",
        WIKI_DATA_DIR / "governance",
        WIKI_DATA_DIR / "my-learning-path",
        WIKI_ROOT / "raw",
    ]
    
    # 尝试多种路径形式
    search_paths = [
        path,
        f"sources/{path}",
        f"concepts/{path}",
        f"entities/{path}",
        f"my-learning-path/{path}",
    ]
    
    for sp in search_paths:
        for search_dir in possible_dirs:
            file_path = search_dir / f"{sp}.md"
            if file_path.exists():
                return await _read_md_file(file_path)
            # 也尝试不带 .md 后缀的直接文件
            if search_dir.exists():
                direct = search_dir / sp
                if direct.exists() and direct.is_file():
                    return await _read_md_file(direct)
    
    raise HTTPException(
        status_code=404, 
        detail={
            "message": "页面未找到",
            "path": path,
            "searched": [str(d) for d in possible_dirs]
        }
    )