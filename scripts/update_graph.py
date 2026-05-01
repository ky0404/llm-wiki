#!/usr/bin/env python3
"""
Full Graph Updater for LLM Wiki
Traverses all .md files, extracts [[wikilinks]], rewrites index-cache.json edges, and generates output/graph.md.
Designed to replace manual JSON editing and ad-hoc graph generation.
"""

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime


def extract_wikilinks(content):
    """Extract all valid [[wikilinks]] from markdown content, ignoring code blocks."""
    import re
    # Remove fenced code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove inline code spans
    content = re.sub(r'`[^`]+`', '', content)
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Remove blockquotes
    content = re.sub(r'^>.*$', '', content, flags=re.MULTILINE)
    
    pattern = r'\[\[([^\]|#]+)(?:\|([^\]]+))?(?:#([^\]]+))?\]\]'
    matches = re.findall(pattern, content)
    return [m[0].strip() for m in matches if m[0].strip()]


def parse_frontmatter(content):
    """Extract YAML frontmatter as a dictionary."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    return fm


def scan_md_files(base_dir):
    """Recursively find all .md files, excluding hidden, output, raw, scripts, templates."""
    skip_dirs = {'.git', '.obsidian', 'output', 'raw', 'scripts', 'templates', 'node_modules'}
    md_files = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.relpath(os.path.join(root, f), base_dir))
    return md_files


def resolve_link(link_text, all_files):
    """Normalize wikilink text to a relative file path."""
    clean = link_text.split('|')[0].split('#')[0].strip()
    if not clean:
        return None
    
    # Already has extension
    if clean.endswith('.md'):
        if os.path.exists(clean):
            return clean
        return clean  # Return as-is, validation happens later
    
    # Try to match existing files
    for fp in all_files:
        if os.path.basename(fp) == f"{clean}.md" or fp.replace('/', '/').endswith(f"/{clean}.md"):
            return fp
    return f"{clean}.md"


def main():
    parser = argparse.ArgumentParser(description="Update graph cache and generate reports")
    parser.add_argument('--base-dir', default='.', help='Base directory of wiki')
    parser.add_argument('--cache', default='index-cache.json', help='Path to cache file')
    parser.add_argument('--output-dir', default='output', help='Output directory')
    args = parser.parse_args()

    md_files = scan_md_files(args.base_dir)
    edges = []
    files_meta = {}
    
    # Preserve existing summaries
    existing_cache = {}
    if os.path.exists(args.cache):
        with open(args.cache, 'r', encoding='utf-8') as f:
            existing_cache = json.load(f)
        files_meta = existing_cache.get('files', {})

    for rel_path in md_files:
        fp = os.path.join(args.base_dir, rel_path)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fm = parse_frontmatter(content)
        title = fm.get('title', rel_path.replace('.md', '').replace('/', ' '))
        ftype = fm.get('type', 'unknown')
        tags_raw = fm.get('tags', '[]')
        tags = [t.strip().strip("'\"") for t in tags_raw.strip('[]').split(',')] if tags_raw.strip('[]') else []
        
        # Update metadata
        files_meta[rel_path] = {
            'title': title,
            'type': ftype,
            'tags': tags,
            'summary': files_meta.get(rel_path, {}).get('summary', '')
        }
        
        links = extract_wikilinks(content)
        for link in links:
            target = resolve_link(link, md_files)
            if target:
                edges.append({'from': rel_path, 'to': target})

    # Generate graph report
    os.makedirs(args.output_dir, exist_ok=True)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    for e in edges:
        in_degree[e['to']] += 1
        out_degree[e['from']] += 1
        
    report_lines = [
        f"# Knowledge Graph Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Nodes: {len(files_meta)}",
        f"- Edges: {len(edges)}",
        "\n## Top Hub Nodes (by total degree)"
    ]
    
    sorted_nodes = sorted(files_meta.keys(), key=lambda x: in_degree.get(x, 0) + out_degree.get(x, 0), reverse=True)[:15]
    for n in sorted_nodes:
        report_lines.append(f"- `{n}`: in={in_degree.get(n,0)}, out={out_degree.get(n,0)}")
        
    with open(os.path.join(args.output_dir, 'graph.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines) + '\n')

    # Save cache (full rewrite)
    cache_data = {
        'last_updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000000'),
        'edges': edges,
        'metadata': existing_cache.get('metadata', {}),
        'files': files_meta,
        'total_files': len(files_meta)
    }
    
    with open(args.cache, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
    print(f"[✓] Scanned {len(md_files)} files, extracted {len(edges)} edges.")
    print(f"[✓] Cache updated: {args.cache}")
    print(f"[✓] Report generated: {args.output_dir}/graph.md")


if __name__ == '__main__':
    main()
