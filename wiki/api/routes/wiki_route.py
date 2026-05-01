"""Wiki 知识库路由"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException

router = APIRouter(tags=["Wiki 知识库"])

WIKI_ROOT = Path("/mnt/d/projects/wiki")
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
    for path, meta in cache.get("files", {}).items():
        nodes.append({
            "id": path,
            "title": meta.get("title", Path(path).stem),
            "type": meta.get("type", "unknown"),
            "tags": meta.get("tags", [])
        })
    edges = []
    for edge in cache.get("edges", []):
        edges.append({
            "source": edge.get("from"),
            "target": edge.get("to")
        })
    return {"nodes": nodes, "edges": edges}


@router.get("/search")
async def search_wiki(q: str = Query(..., description="搜索关键词")):
    """全局内容搜索"""
    try:
        result = subprocess.run(
            ["grep", "-rni", q, str(WIKI_ROOT), "--include=*.md"],
            capture_output=True, text=True, timeout=15
        )
        lines = result.stdout.strip().split("\n")[:30]
        results = []
        for line in lines:
            parts = line.split(":", 2)
            if len(parts) >= 3:
                filepath = parts[0].replace(str(WIKI_ROOT) + "/", "")
                results.append({
                    "file": filepath,
                    "line": parts[1],
                    "snippet": parts[2][:300]
                })
        return {"total": len(results), "results": results}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="搜索超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}") from e


@router.get("/pages")
async def list_pages(limit: int = Query(50, ge=1, le=200)):
    """列出知识库页面"""
    try:
        result = subprocess.run(
            ["find", str(WIKI_ROOT), "-name", "*.md", "-not", "-path", "*/.obsidian/*"],
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