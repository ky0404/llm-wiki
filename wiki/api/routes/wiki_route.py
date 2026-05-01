from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Wiki 知识库"])

# 修正路径：实际Wiki目录
WIKI_ROOT = Path("/mnt/d/projects/wiki")


def load_cache():
    """从 index-cache.json 读取数据"""
    cache_file = WIKI_ROOT / "index-cache.json"
    if not cache_file.exists():
        raise HTTPException(status_code=500, detail="索引缓存未找到")
    with open(cache_file, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/stats")
async def get_wiki_stats():
    """获取知识库核心统计数据"""
    cache = load_cache()
    files = cache.get("files", {})
    edges = cache.get("edges", [])
    
    total_files = len(files)
    total_edges = len(edges)
    
    type_counts = {}
    for f_meta in files.values():
        t = f_meta.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    
    sorted_files = sorted(
        files.items(),
        key=lambda x: x[1].get("updated", ""),
        reverse=True
    )[:10]
    recent = [
        {"path": k, "title": v.get("title", k)}
        for k, v in sorted_files
    ]
    
    return {
        "total_files": total_files,
        "total_edges": total_edges,
        "type_distribution": type_counts,
        "recent_pages": recent
    }


@router.get("/graph")
async def get_knowledge_graph():
    """返回图谱数据（节点和边），供前端可视化"""
    cache = load_cache()
    
    nodes = []
    for path, meta in cache.get("files", {}).items():
        nodes.append({
            "id": path,
            "title": meta.get("title", path),
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
    """全文搜索 wiki 页面内容"""
    wiki_dir = WIKI_ROOT
    
    try:
        result = subprocess.run(
            ["grep", "-rn", q, str(wiki_dir), "--include=*.md"],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split("\n")[:20]
        
        results = []
        for line in lines:
            parts = line.split(":", 2)
            if len(parts) >= 3:
                filepath = parts[0].replace(str(wiki_dir) + "/", "")
                results.append({
                    "file": filepath,
                    "snippet": parts[2][:200]
                })
        
        return {"total": len(results), "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}") from e


@router.get("/pages")
async def list_pages(limit: int = Query(20, ge=1, le=100)):
    """列出知识库中的所有页面"""
    wiki_dir = WIKI_ROOT
    
    try:
        result = subprocess.run(
            ["find", str(wiki_dir), "-name", "*.md"],
            capture_output=True, text=True, timeout=10
        )
        files = result.stdout.strip().split("\n")[:limit]
        
        pages = []
        for f in files:
            if f:
                rel_path = Path(f).relative_to(wiki_dir)
                pages.append({
                    "path": str(rel_path),
                    "title": Path(f).stem
                })
        
        return {"total": len(pages), "pages": pages}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取页面列表失败: {str(e)}") from e


@router.post("/sync")
async def sync_wiki():
    """触发知识图谱同步（调用 scripts/update_graph.py）"""
    try:
        result = subprocess.run(
            ["python3", str(WIKI_ROOT / "scripts/update_graph.py")],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(WIKI_ROOT)
        )
        
        if result.returncode == 0:
            return {"status": "success", "message": "知识图谱已更新", "output": result.stdout}
        else:
            raise HTTPException(status_code=500, detail=f"同步失败: {result.stderr}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步异常: {str(e)}") from e


@router.post("/gc")
async def run_garbage_collection():
    """运行垃圾回收（调用 scripts/comprehensive_gc.py）"""
    try:
        result = subprocess.run(
            ["python3", str(WIKI_ROOT / "scripts/comprehensive_gc.py")],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WIKI_ROOT)
        )
        
        if result.returncode == 0:
            return {"status": "success", "message": "垃圾回收完成", "output": result.stdout[:500]}
        else:
            raise HTTPException(status_code=500, detail=f"GC失败: {result.stderr}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GC异常: {str(e)}") from e


@router.get("/verify")
async def verify_tools():
    """工具验证（调用 scripts/verify_tools.py）"""
    try:
        result = subprocess.run(
            ["python3", str(WIKI_ROOT / "scripts/verify_tools.py"), "--root", str(WIKI_ROOT)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(WIKI_ROOT)
        )
        
        if result.returncode == 0:
            return {"status": "success", "message": "验证完成", "output": result.stdout[:1000]}
        else:
            raise HTTPException(status_code=500, detail=f"验证失败: {result.stderr}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"验证异常: {str(e)}") from e


@router.get("/page/{path:path}")
async def get_page(path: str):
    """获取单个页面的内容"""
    file_path = WIKI_ROOT / path
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="页面不存在")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取失败: {str(e)}") from e