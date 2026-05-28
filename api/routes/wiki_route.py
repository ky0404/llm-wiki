"""Wiki 知识库路由 - 异步I/O、安全增强、去耦合依赖"""
from __future__ import annotations

import json
import re
import os
import asyncio
import aiofiles
from pathlib import Path
from functools import lru_cache
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

from config import config


router = APIRouter(tags=["Wiki 知识库"])
logger = config.get_logger(__name__)


content_cache: dict = {}
wikilink_pattern = re.compile(r'\[\[wiki/([^]]+)\]\]')


class WikiStatsResponse(BaseModel):
    """/stats 响应模型"""
    total_files: int = Field(description="总文件数")
    total_edges: int = Field(description="总边数（链接数）")
    health_score: int = Field(description="健康分数 0-100")
    type_distribution: dict = Field(description="类型分布")
    recent_pages: list = Field(description="最近页面")
    metadata: dict = Field(description="元数据")


class GraphNode(BaseModel):
    """图谱节点"""
    id: str
    title: str
    type: str
    tags: list


class GraphEdge(BaseModel):
    """图谱边"""
    source: str
    target: str


class WikiGraphResponse(BaseModel):
    """/graph 响应模型"""
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class SearchResult(BaseModel):
    """搜索结果项"""
    file: str
    line: str
    snippet: str


class WikiSearchResponse(BaseModel):
    """/search 响应模型"""
    total: int
    results: list[SearchResult]


class PageInfo(BaseModel):
    """页面信息"""
    path: str
    title: str


class WikiPagesResponse(BaseModel):
    """/pages 响应模型"""
    total: int
    pages: list[PageInfo]


class RefreshResponse(BaseModel):
    """/refresh 响应模型"""
    status: str
    message: str
    output: Optional[str] = None


class ContentResponse(BaseModel):
    """/content 响应模型"""
    content: str
    frontmatter: dict
    raw: str


class WikiSearchParams(BaseModel):
    """/search 输入参数模型"""
    q: str = Field(..., description="搜索关键词", min_length=1, max_length=200)


class WikiContentParams(BaseModel):
    """/content 输入参数模型"""
    path: str = Field(..., description="页面路径", min_length=1, max_length=500)


def load_cache():
    """加载索引缓存"""
    if not config.CACHE_FILE.exists():
        raise HTTPException(status_code=500, detail="索引缓存未找到，请先运行 generate_graph_and_cache.py")
    try:
        with open(config.CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"缓存文件损坏: {e}")


def sanitize_path(path: str) -> str:
    """严格路径规范化处理 - 防止路径遍历攻击"""
    if not path:
        return ""

    path = path.strip()
    path = path.replace("\\", "/")

    path = re.sub(r'[^\w\-/._]', '', path)

    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="无效的路径")

    path = path.strip("/")

    return path


def search_files_native(query: str, search_dirs: list) -> dict:
    """原生 Python 实现文件搜索 - 替代 grep/find 依赖"""
    results = {}
    query_lower = query.lower()

    excluded_dirs = set(config.EXCLUDED_DIRS)

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for md_file in search_dir.rglob("*.md"):
            if any(excluded in md_file.parts for excluded in excluded_dirs):
                continue

            try:
                with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, 1):
                        if query_lower in line.lower():
                            rel_path = str(md_file.relative_to(config.WIKI_ROOT))
                            if rel_path not in results:
                                results[rel_path] = {
                                    "file": rel_path,
                                    "line": str(line_no),
                                    "snippet": line.strip()[:300]
                                }
                            break
            except Exception as e:
                logger.debug(f"[Search] 读取文件失败 {md_file}: {e}")

    return results


def list_files_native(search_dirs: list, limit: int = 200) -> list:
    """原生 Python 实现文件列表 - 替代 find 依赖"""
    files = []
    excluded_dirs = set(config.EXCLUDED_DIRS)

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue

        for md_file in search_dir.rglob("*.md"):
            if any(excluded in md_file.parts for excluded in excluded_dirs):
                continue

            try:
                rel_path = str(md_file.relative_to(config.WIKI_ROOT))
                files.append({
                    "path": rel_path,
                    "title": md_file.stem
                })
                if len(files) >= limit:
                    break
            except Exception as e:
                logger.debug(f"[List] 处理文件失败 {md_file}: {e}")

        if len(files) >= limit:
            break

    return files[:limit]


@lru_cache(maxsize=500)
def convert_wikilink_cached(link: str) -> str:
    """Wikilink 转换缓存版本"""
    if "|" in link:
        path, title = link.split("|", 1)
    else:
        path = link
        title = path.split("/")[-1]

    url_path = path.replace(".md", "")
    if url_path.startswith("wiki/"):
        url = "/" + url_path
    else:
        url = "/wiki/" + url_path

    return f'<a href="{url}" class="wiki-link">{title}</a>'


def convert_wikilinks(html: str) -> str:
    """转换 wikilinks 为可点击链接"""
    def replacer(match):
        link = match.group(1)
        return convert_wikilink_cached(link)

    return wikilink_pattern.sub(replacer, html)


async def _read_md_file_async(file_path: Path) -> dict:
    """异步读取 Markdown 文件并转换为 HTML"""
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
    except Exception as e:
        logger.error(f"[Read] 读取文件失败 {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"读取文件失败: {e}")

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

    if MARKDOWN_AVAILABLE:
        html = markdown.markdown(body, extensions=['fenced_code', 'tables', 'sane_lists'])
    else:
        html = f"<pre>{body}</pre>"

    html = convert_wikilinks(html)

    return {"content": html, "frontmatter": frontmatter, "raw": body}


@router.get("/stats", response_model=WikiStatsResponse)
async def get_wiki_stats():
    """
    知识库核心统计数据

    - **total_files**: 知识库总文件数
    - **total_edges**: 知识库总链接数
    - **health_score**: 健康分数 (0-100)，基于 frontmatter 完整性计算
    - **type_distribution**: 各类型文件分布
    - **recent_pages**: 最近修改的 10 个页面
    - **metadata**: 知识库元数据
    """
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


@router.get("/graph", response_model=WikiGraphResponse)
async def get_knowledge_graph():
    """
    知识图谱数据

    - **nodes**: 所有页面节点，包含 id、title、type、tags
    - **edges**: 页面间的链接关系
    """
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


@router.get("/search", response_model=WikiSearchResponse)
async def search_wiki(q: str = Query(..., description="搜索关键词", min_length=1, max_length=200)):
    """
    全局内容搜索

    - **q**: 搜索关键词
    - 返回匹配的文件列表，每个文件显示行号和内容片段
    """
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="搜索关键词不能为空")

    search_dirs = [
        config.WIKI_DATA_DIR,
        config.RAW_DIR,
        config.LEARNING_PATH_DIR,
    ]

    loop = asyncio.get_event_loop()
    file_results = await loop.run_in_executor(
        None,
        search_files_native,
        q,
        search_dirs
    )

    results = list(file_results.values())[:config.MAX_SEARCH_RESULTS]
    return {"total": len(results), "results": results}


@router.get("/pages", response_model=WikiPagesResponse)
async def list_pages(limit: int = Query(50, ge=1, le=200, description="返回结果数量限制")):
    """
    列出知识库所有页面

    - **limit**: 返回结果数量限制，默认 50，最大 200
    - 返回所有 .md 文件的路径和标题
    """
    search_dirs = [
        config.WIKI_DATA_DIR,
        config.RAW_DIR,
        config.LEARNING_PATH_DIR,
    ]

    loop = asyncio.get_event_loop()
    pages = await loop.run_in_executor(
        None,
        list_files_native,
        search_dirs,
        min(limit, config.MAX_PAGES_LIMIT)
    )

    return {"total": len(pages), "pages": pages}


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "cache_exists": config.CACHE_FILE.exists(),
        "wiki_root_exists": config.WIKI_ROOT.exists(),
        "api_version": config.API_VERSION
    }


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_cache():
    """
    手动刷新知识库索引缓存

    - 执行 generate_graph_and_cache.py 脚本
    - 返回执行结果
    """
    import time

    script_path = config.SCRIPTS_DIR / "generate_graph_and_cache.py"
    if not script_path.exists():
        raise HTTPException(status_code=500, detail="刷新脚本不存在")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                ["python3", str(script_path)],
                cwd=str(config.WIKI_ROOT),
                capture_output=True,
                text=True,
                timeout=config.REFRESH_TIMEOUT
            )
        )

        if result.returncode != 0:
            logger.error(f"刷新缓存失败: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"刷新失败: {result.stderr}")

        return {
            "status": "ok",
            "message": "知识库索引已刷新",
            "output": result.stdout[:500] if result.stdout else None
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="刷新超时")
    except Exception as e:
        logger.error(f"刷新缓存异常: {e}")
        raise HTTPException(status_code=500, detail=f"刷新异常: {str(e)}")


import subprocess


@router.get("/content", response_model=ContentResponse)
async def get_content(path: str = Query("", description="页面路径")):
    """
    获取页面内容

    - **path**: 页面路径（如 'sources/my-file' 或 'my-learning-path/theory/xxx'）
    - 返回 HTML 渲染内容、frontmatter 元数据和原始 Markdown
    """
    if not path:
        raise HTTPException(status_code=400, detail="缺少页面路径")

    try:
        path = sanitize_path(path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"路径格式错误: {e}")

    if path.endswith(".md"):
        path = path[:-3]

    possible_dirs = [
        config.WIKI_DATA_DIR,
        config.WIKI_DATA_DIR / "sources",
        config.WIKI_DATA_DIR / "concepts",
        config.WIKI_DATA_DIR / "entities",
        config.WIKI_DATA_DIR / "governance",
        config.LEARNING_PATH_DIR,
        config.RAW_DIR,
    ]

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
            if file_path.exists() and file_path.is_file():
                return await _read_md_file_async(file_path)

            direct = search_dir / sp
            if direct.exists() and direct.is_file() and direct.suffix == ".md":
                return await _read_md_file_async(direct)

    raise HTTPException(
        status_code=404,
        detail="页面未找到"
    )