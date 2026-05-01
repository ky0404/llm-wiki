#!/usr/bin/env python3
"""
Knowledge Graph Generator for LLM Wiki
Reads index-cache.json and generates graph visualizations in output/ directory.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime


def load_cache(cache_path):
    """Load and validate index-cache.json"""
    if not os.path.exists(cache_path):
        raise FileNotFoundError(f"Cache file not found: {cache_path}")
    
    with open(cache_path, 'r', encoding='utf-8') as f:
        cache = json.load(f)
    
    if 'edges' not in cache or 'files' not in cache:
        raise ValueError("Invalid cache format: missing 'edges' or 'files' keys")
    
    return cache


def compute_metrics(edges, files):
    """Compute graph metrics: in-degree, out-degree, total connections"""
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for edge in edges:
        src = edge.get('from', '')
        tgt = edge.get('to', '')
        if src and tgt:
            out_degree[src] += 1
            in_degree[tgt] += 1
    
    all_nodes = set(files.keys())
    for node in all_nodes:
        if node not in in_degree:
            in_degree[node] = 0
        if node not in out_degree:
            out_degree[node] = 0
    
    return in_degree, out_degree


def generate_mermaid(edges, files, output_path):
    """Generate Mermaid graph diagram"""
    lines = ["graph TD"]
    
    valid_nodes = set(files.keys())
    
    for edge in edges:
        src = edge.get('from', '').replace('.md', '').replace('/', '_')
        tgt = edge.get('to', '').replace('.md', '').replace('/', '_')
        
        if src in valid_nodes and tgt in valid_nodes:
            lines.append(f"    {src} --> {tgt}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def generate_markdown_report(edges, files, in_degree, out_degree, output_path):
    """Generate Markdown graph report"""
    total_nodes = len(files)
    total_edges = len(edges)
    
    # Sort by total connections
    node_connections = []
    for node in files:
        total = in_degree.get(node, 0) + out_degree.get(node, 0)
        node_connections.append((node, in_degree.get(node, 0), out_degree.get(node, 0), total))
    
    node_connections.sort(key=lambda x: x[3], reverse=True)
    
    # Find isolated nodes (excluding system files)
    system_files = {'index.md', 'log.md', 'AGENTS.md'}
    isolated_nodes = []
    for node, in_d, out_d, total in node_connections:
        if node not in system_files and total == 0:
            isolated_nodes.append(node)
    
    lines = [
        "# Knowledge Graph Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        f"- Total Nodes: {total_nodes}",
        f"- Total Edges: {total_edges}",
        f"- Average Connections per Node: {total_edges * 2 / max(total_nodes, 1):.2f}",
        "",
        "## Top 20 Hub Nodes (by total connections)",
        "| Node | In-Degree | Out-Degree | Total |",
        "|------|-----------|------------|-------|",
    ]
    
    for node, in_d, out_d, total in node_connections[:20]:
        display_name = node.replace('.md', '').replace('/', '/')
        lines.append(f"| {display_name} | {in_d} | {out_d} | {total} |")
    
    lines.append("")
    lines.append("## Isolated Nodes (excluding system files)")
    if isolated_nodes:
        for node in isolated_nodes:
            lines.append(f"- {node}")
    else:
        lines.append("- None detected")
    
    lines.append("")
    lines.append("## Orphan Nodes (zero in-degree, excluding system files)")
    orphan_nodes = [(n, i, o, t) for n, i, o, t in node_connections if n not in system_files and i == 0 and t > 0]
    if orphan_nodes:
        for node, in_d, out_d, total in orphan_nodes[:10]:
            lines.append(f"- {node} (out-degree: {out_d})")
    else:
        lines.append("- None detected")
    
    lines.append("")
    lines.append("## Dead-End Nodes (zero out-degree, excluding system files)")
    dead_end_nodes = [(n, i, o, t) for n, i, o, t in node_connections if n not in system_files and o == 0 and t > 0]
    if dead_end_nodes:
        for node, in_d, out_d, total in dead_end_nodes[:10]:
            lines.append(f"- {node} (in-degree: {in_d})")
    else:
        lines.append("- None detected")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def main():
    parser = argparse.ArgumentParser(description="Generate knowledge graph from wiki cache")
    parser.add_argument('--cache', default='index-cache.json', help='Path to index-cache.json')
    parser.add_argument('--output-dir', default='output', help='Output directory for graph files')
    parser.add_argument('--verbose', action='store_true', help='Print detailed metrics')
    args = parser.parse_args()
    
    try:
        cache = load_cache(args.cache)
        edges = cache['edges']
        files = cache['files']
        
        os.makedirs(args.output_dir, exist_ok=True)
        
        in_degree, out_degree = compute_metrics(edges, files)
        
        md_path = os.path.join(args.output_dir, 'graph.md')
        mmd_path = os.path.join(args.output_dir, 'graph.mmd')
        
        generate_mermaid(edges, files, mmd_path)
        generate_markdown_report(edges, files, in_degree, out_degree, md_path)
        
        print(f"Graph generated: {len(files)} nodes, {len(edges)} edges")
        print(f"Output: {md_path}, {mmd_path}")
        
        if args.verbose:
            print("\nTop 10 hubs:")
            node_connections = []
            for node in files:
                total = in_degree.get(node, 0) + out_degree.get(node, 0)
                node_connections.append((node, total))
            node_connections.sort(key=lambda x: x[1], reverse=True)
            for node, total in node_connections[:10]:
                print(f"  {node}: {total} connections")
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
