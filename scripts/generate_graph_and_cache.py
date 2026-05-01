#!/usr/bin/env python3
import os, re, json, yaml, sys
from pathlib import Path
from datetime import datetime

ROOT = Path("/mnt/d/projects/wiki")
WIKI = ROOT / "wiki"
OUTPUT = ROOT / "output"
CACHE_FILE = WIKI / "index-cache.json"

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

def gather_pages():
    pages = []
    if not WIKI.exists():
        return pages
    for root, dirs, files in os.walk(WIKI):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.md'):
                pages.append(Path(root) / f)
    return pages

def extract_edges(pages):
    edges = []
    seen = set()
    pat = re.compile(r'\[\[([^\[\]]+?)\]\]')
    for p in pages:
        text = p.read_text(encoding='utf-8')
        src = str(p.relative_to(WIKI))
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
        rel = str(p.relative_to(WIKI))
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
    nodes, edges_list = generate_graph(edges)
    cache = build_cache(pages)
    # 将边信息写入缓存（L1 导航用）
    cache['edges'] = [{'from': a, 'to': b} for a, b in edges]
    save_cache(cache)
    print(f"Graph: {len(nodes)} 节点, {len(edges)} 边")
    print("index-cache.json 已包含所有页面的 L1/L2 信息。")

if __name__ == '__main__':
    main()
