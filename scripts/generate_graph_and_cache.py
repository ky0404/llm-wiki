#!/usr/bin/env python3
import os, re, json, yaml, sys
from pathlib import Path
from datetime import datetime

ROOT = Path("/home/dukkha/wiki")
WIKI = ROOT / "wiki"
OUTPUT = ROOT / "output"
CACHE_FILE = ROOT / "wiki" / "index-cache.json"

def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(data):
    data['last_updated'] = datetime.now().isoformat()
    CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def parse_frontmatter(text):
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                return fm, parts[2]
            except Exception:
                pass
    return {}, text

# 受保护的目录/文件（提取边时不扫描）
PROTECTED_PATHS = [
    'AGENTS.md',
    'skills/',
    'synthesis/knowledge-base-evolution-',
]

# 排除的目录（Obsidian vault 中无关的目录）
EXCLUDED_DIRS = [
    'docs/',
    'frontend/',
    'node_modules/',
    '.obsidian/',
    '.git/',
    'archives/',
    'path/',
    'prep/',
    'templates/',
    'theory/',
    '03-practice-logs/',
    '04-project-archives/',
    'sources/',
    'Clippings/',
]

def gather_pages():
    pages = []
    scan_dirs = [WIKI]
    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue
        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and not _is_protected_dir(d)]
            for f in files:
                if f.endswith('.md') and not _is_protected_file(f):
                    pages.append(Path(root) / f)
    return pages

def _is_protected_dir(name):
    """检查目录是否受保护"""
    for p in PROTECTED_PATHS:
        if p.endswith('/') and name == p.rstrip('/'):
            return True
    return False

def _is_protected_file(name):
    """检查文件是否受保护"""
    for p in PROTECTED_PATHS:
        if not p.endswith('/') and name == p:
            return True
        if p.endswith('/') and name.startswith(p.rstrip('/')):
            return True
        if '-' in p and name.startswith(p.split('-')[0]):
            return True
    return False

def _rel_path(p):
    if str(p).startswith(str(WIKI)):
        return str(p.relative_to(WIKI))
    elif str(p).startswith(str(ROOT)):
        return str(p.relative_to(ROOT))
    return p.name

def extract_edges(pages):
    edges = []
    seen = set()
    pat = re.compile(r'\[\[([^\[\]]+?)\]\]')
    for p in pages:
        text = p.read_text(encoding='utf-8')
        src = _rel_path(p)
        for m in pat.findall(text):
            target = m.split('|')[0].strip()
            if not target.endswith('.md'):
                target += '.md'
            key = (src, target)
            if key not in seen:
                seen.add(key)
                edges.append((src, target))
    return edges

def generate_graph(edges):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    nodes = sorted(set(e[0] for e in edges) | set(e[1] for e in edges))
    node_id = {n: f"N{i}" for i, n in enumerate(nodes)}
    mmd = ["graph TD"]
    for a, b in edges:
        mmd.append(f'    {node_id[a]}["{a}"] --> {node_id[b]}["{b}"]')
    mmd_text = "\n".join(mmd)
    (OUTPUT / "graph.mmd").write_text(mmd_text, encoding='utf-8')
    graph_md = f"# Knowledge Graph\n\n生成：{datetime.now().isoformat()}\n\n```mermaid\n{mmd_text}\n```\n"
    (OUTPUT / "graph.md").write_text(graph_md, encoding='utf-8')
    return nodes, edges

def build_cache(pages):
    cache = load_cache()
    files_meta = {}
    for p in pages:
        try:
            raw = p.read_text(encoding='utf-8')
        except Exception:
            continue
        fm, body = parse_frontmatter(raw)
        rel = _rel_path(p)
        title = fm.get('title', p.stem)
        typ = fm.get('type', 'unknown')
        tags = fm.get('tags', [])
        # 生成 L2 摘要：取 body 中第一个非空行，或截取前 200 字符
        summary = ''
        for line in body.strip().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                summary = line[:200]
                break
        if not summary:
            summary = body.strip()[:200]
        files_meta[rel] = {
            'title': title,
            'type': typ,
            'tags': tags,
            'summary': summary
        }
    cache['files'] = files_meta
    cache['total_files'] = len(files_meta)
    return cache

def main():
    pages = gather_pages()
    if not pages:
        print("No pages found.")
        return
    edges = extract_edges(pages)
    
    # 构建节点映射
    valid_nodes = {}
    node_by_name = {}
    node_by_path = {}
    for p in pages:
        rel = _rel_path(p)
        try:
            content = p.read_text(encoding='utf-8')
            if len(content.strip()) < 100:
                continue
        except:
            continue
        valid_nodes[rel] = True
        name = p.stem.replace('-', '').lower()
        node_by_name[name] = rel
        path_key = rel.replace('.md', '')
        node_by_path[path_key] = rel
    
    # 提取有效边 + 创建语义连接
    normalized_edges = []
    seen_edges = set()
    
    # 1. 先处理显式的 wikilinks 边
    for a, b in edges:
        a = a.replace('wiki/', '', 1) if a.startswith('wiki/') else a
        b = b.replace('wiki/', '', 1) if b.startswith('wiki/') else b
        
        if a not in valid_nodes or not b.endswith('.md'):
            continue
        
        matched_target = None
        b_stem = b.replace('.md', '').replace('-', '').lower()
        matched_target = node_by_name.get(b_stem)
        if not matched_target:
            b_path = b.replace('.md', '')
            matched_target = node_by_path.get(b_path)
        if not matched_target:
            for path, full in node_by_path.items():
                if b_path in path or path in b_path:
                    matched_target = full
                    break
        if not matched_target or matched_target not in valid_nodes:
            continue
        
        key = (a, matched_target)
        if key not in seen_edges:
            seen_edges.add(key)
            normalized_edges.append((a, matched_target))
    
    # 2. 创建语义连接 - 基于话题聚类
    # 定义话题关键词到核心页面的映射
    topic_cores = {
        'prompt': ['wiki/sources/提示工程学习笔记.md', 'wiki/sources/如何写好prompt-结构化.md', 'wiki/sources/prompt-进阶-提示链.md'],
        'agent': ['wiki/sources/你不知道的-agent.md', 'wiki/sources/基于-LangGraph-创建智能体应用.md', 'wiki/sources/agent-skills.md'],
        'rag': ['wiki/sources/高级-RAG-技术学习笔记.md', 'wiki/sources/使用-Embedding-技术打造本地知识库助手.md'],
        'context': ['wiki/sources/浅谈上下文工程.md', 'wiki/sources/context-engineering.md', 'wiki/sources/effective-context-engineering-ai-agents.md'],
        'llm': ['wiki/sources/大模型应用开发框架-LangChain-学习笔记.md', 'wiki/sources/开源大模型-llama-实战.md'],
        'k8s': ['wiki/sources/k8s-流量管理-service.md', 'wiki/sources/k8s-流量管理-ingress.md', 'wiki/sources/k8s-gpu调度.md'],
        'mcp': ['wiki/sources/understanding-model-context-protocol-mcp.md', 'wiki/sources/实战-Model-Context-Protocol.md'],
        'codex': ['wiki/sources/openai-codex-harness工程.md', 'wiki/sources/karpathy-claude-code指南.md'],
    }
    
    # 为每个话题创建一个中心节点作为桥梁
    topic_centers = {}
    topic_list = list(topic_cores.keys())
    for i, topic in enumerate(topic_list):
        center = f'topic-center-{i}'
        topic_centers[topic] = center
        # 添加 topic center 到 index 的边
        normalized_edges.append(('index.md', center))
    
    # 为每个 sources 页找到其话题并连接到对应 core
    for src in valid_nodes:
        if not src.startswith('wiki/sources/'):
            continue
        src_lower = src.lower()
        
        for topic, cores in topic_cores.items():
            if topic in src_lower:
                # 连接到该话题的核心页面
                for core in cores:
                    if core in valid_nodes and (src, core) not in seen_edges:
                        seen_edges.add((src, core))
                        normalized_edges.append((src, core))
                break
    
    # 3. 添加 index -> 所有 sources 的入口（保持可发现性）
    for src in valid_nodes:
        if src.startswith('wiki/sources/') and ('index.md', src) not in seen_edges:
            # 只对核心 sources 添加入口边，避免太密
            if any(k in src.lower() for k in ['prompt', 'agent', 'rag', 'context', 'llm', 'langchain']):
                normalized_edges.append(('index.md', src))
    
    # 4. 添加 entities -> 相关 sources
    entity_refs = {
        'wiki/entities/ai-products.md': ['wiki/sources/prompted-products.md', 'wiki/sources/聊聊-deep-search和deep-research.md'],
        'wiki/entities/developer-tools.md': ['wiki/sources/function-calling-openai-api.md', 'wiki/sources/claude-code编码指南.md'],
        'wiki/entities/key-people.md': ['wiki/sources/karpathy-claude-code指南.md'],
    }
    for ent, refs in entity_refs.items():
        if ent in valid_nodes:
            for ref in refs:
                if ref in valid_nodes and (ent, ref) not in seen_edges:
                    seen_edges.add((ent, ref))
                    normalized_edges.append((ent, ref))
    
    # 5. 添加 my-learning-path -> 相关 sources
    for mlp in valid_nodes:
        if mlp.startswith('wiki/my-learning-path/'):
            for src in valid_nodes:
                if src.startswith('wiki/sources/'):
                    # 基于关键词匹配
                    mlp_lower = mlp.lower()
                    src_lower = src.lower()
                    if any(k in mlp_lower and k in src_lower for k in ['prompt', 'agent', 'rag', 'context']):
                        if (mlp, src) not in seen_edges:
                            seen_edges.add((mlp, src))
                            normalized_edges.append((mlp, src))
    
    nodes, edges_list = generate_graph(normalized_edges)
    cache = build_cache(pages)
    cache['edges'] = [{'from': a, 'to': b} for a, b in normalized_edges]
    save_cache(cache)
    print(f"Graph: {len(nodes)} 节点, {len(normalized_edges)} 边")
    print("index-cache.json 已包含所有页面的 L1/L2 信息。")

if __name__ == '__main__':
    main()
