#!/usr/bin/env python3
import os, re, json
from pathlib import Path
from datetime import datetime
from collections import Counter

WIKI_ROOT = "/home/dukkha/wiki"
WIKI_DIR = Path(WIKI_ROOT) / "wiki"
OUTPUT_DIR = Path(WIKI_ROOT) / "output"
CACHE_FILE = WIKI_DIR / "index-cache.json"
DISCLOSURES_DIR = OUTPUT_DIR / "disclosures"

def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"edges": []}

def save_cache(data):
    data["last_updated"] = datetime.now().isoformat()
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def gather_pages():
    pages = []
    if not WIKI_DIR.exists():
        return pages
    for root, dirs, files in os.walk(WIKI_DIR):
        dirs[:] = [d for d in dirs if d != ".obsidian"]
        for f in files:
            if f.endswith(".md"):
                pages.append(Path(root) / f)
    return pages

def extract_edges(pages):
    edges = []
    seen = set()
    pat = re.compile(r"\[\[([^\[\]]+?)\]\]")
    for p in pages:
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        src = str(p.relative_to(WIKI_DIR))
        for m in pat.findall(text):
            target = m.split("|")[0].strip()
            if not target.endswith(".md"):
                target += ".md"
            key = (src, target)
            if key not in seen:
                seen.add(key)
                edges.append({"from": src, "to": target})
    return edges

def render(edges):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    nodes = sorted(set(e["from"] for e in edges) | set(e["to"] for e in edges))
    node_id = {n: f"N{i}" for i, n in enumerate(nodes)}
    mmd_lines = ["graph TD"]
    for e in edges:
        a = node_id[e["from"]]
        b = node_id[e["to"]]
        la = e["from"].replace("[","(").replace("]",")")
        lb = e["to"].replace("[","(").replace("]",")")
        mmd_lines.append(f'    {a}["{la}"] --> {b}["{lb}"]')
    mmd_text = "\n".join(mmd_lines)
    (OUTPUT_DIR / "graph.mmd").write_text(mmd_text, encoding="utf-8")
    md_text = f"# Knowledge Graph\n\n生成时间：{datetime.now().isoformat()}\n\n节点：{len(nodes)}  边：{len(edges)}\n\n```mermaid\n{mmd_text}\n```\n"
    (OUTPUT_DIR / "graph.md").write_text(md_text, encoding="utf-8")
    return nodes, edges

def generate_disclosures(nodes, edges):
    DISCLOSURES_DIR.mkdir(parents=True, exist_ok=True)
    adj = {n: [] for n in nodes}
    for e in edges:
        adj.setdefault(e["from"], []).append(e["to"])
    for node in nodes:
        nd = DISCLOSURES_DIR / node.replace(".md", "").replace("/", "_")
        nd.mkdir(parents=True, exist_ok=True)
        neighbors = adj.get(node, [])[:6]
        # L1
        (nd / "level1.md").write_text(f"# {node} - Level 1\n\n核心节点：{node}\n邻居：{', '.join(neighbors)}\n\n提示：查看 Level 2/3 获取更多详情。\n", encoding="utf-8")
        # L2
        (nd / "level2.md").write_text(f"# {node} - Level 2\n\n核心节点：{node}\n简要摘要：2-3 条要点。\n邻居精选：{', '.join(neighbors)}\n", encoding="utf-8")
        # L3
        (nd / "level3.md").write_text(f"# {node} - Level 3\n\n完整摘要：包含详细数据与引用。\n引用示例：见原始 wiki 页面。\n", encoding="utf-8")

def main():
    pages = gather_pages()
    edges = extract_edges(pages)
    nodes, edges = render(edges)
    generate_disclosures(nodes, edges)
    cache = load_cache()
    cache["edges"] = edges
    save_cache(cache)
    if edges:
        indeg = Counter(e["to"] for e in edges)
        top = indeg.most_common(5)
        print("枢纽节点：")
        for n, c in top:
            print(f"  {n} (被引{c}次)")
    print("graph.md / graph.mmd 已生成，disclosures 目录已创建。")

if __name__ == "__main__":
    main()
