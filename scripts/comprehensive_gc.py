#!/usr/bin/env python3
"""
Comprehensive Garbage Collection for Knowledge Base
Detects and (optionally) auto-fixes common garbage in index-cache.json.

Modes:

dry-run: only report
auto: perform safe removals (ghosts) and prune edges
"""
import json
import os
import argparse
from collections import defaultdict
from datetime import datetime

CACHE_PATH = 'index-cache.json'
OUTPUT_REPORT = 'synthesis/graph-audit-{}.md'
LOG_PATH = 'log.md'

def load_cache(cache_path=CACHE_PATH):
    with open(cache_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def detect_issues(cache):
    issues = {
        'orphan_files': [], # files entry exists, file path missing
        'missing_nodes': [], # edge.from/to not in files
        'self_loops': [],
        'duplicate_edges': [],
        'isolated_nodes': [],
        'dangling_edges': []
    }
    files = set(cache.get('files', {}).keys())
    edges = cache.get('edges', [])

    indeg = defaultdict(int)
    outdeg = defaultdict(int)
    for e in edges:
        fr = e.get('from')
        to = e.get('to')
        if fr:
            outdeg[fr] += 1
        if to:
            indeg[to] += 1
        if fr and to and fr == to:
            issues['self_loops'].append(fr)
    # dangling edges (to not in files)
    for e in edges:
        if e.get('to') not in files:
            issues['dangling_edges'].append((e.get('from'), e.get('to')))
    # orphan/ghost files
    for f in files:
        if not os.path.exists(f):
            if indeg.get(f, 0) == 0 and outdeg.get(f, 0) == 0:
                issues['isolated_nodes'].append(f)
            else:
                issues['orphan_files'].append(f)
    # missing nodes (edges refer to non-existing files)
    for e in edges:
        if e.get('from') not in files or e.get('to') not in files:
            if e.get('from') not in files:
                issues['missing_nodes'].append(e.get('from'))
            if e.get('to') not in files:
                issues['missing_nodes'].append(e.get('to'))
    # duplicates
    seen = set()
    for e in edges:
        key = (e.get('from'), e.get('to'))
        if key in seen:
            issues['duplicate_edges'].append(key)
        seen.add(key)
    return issues

def generate_report(issues):
    lines = []
    lines.append('# Comprehensive Garbage Collection Report')
    lines.append('')
    for k, v in issues.items():
        lines.append(f'## {k} ({len(v)})')
        if v:
            for item in v:
                lines.append(f'- {item}')
        else:
            lines.append('- (none)')
        lines.append('')
    return "\n".join(lines)

def apply_auto_fix(cache, issues):
    """Very conservative auto-fix: remove ghost files and related edges only."""
    ghosts = set(issues.get('orphan_files', []))
    if not ghosts:
        return cache, []

    # Filter files
    new_files = {k: v for k, v in cache.get('files', {}).items() if k not in ghosts}
    # Filter edges touching ghosts
    new_edges = []
    for e in cache.get('edges', []):
        if (e.get('from') in ghosts) or (e.get('to') in ghosts):
            continue
        new_edges.append(e)
    cache['files'] = new_files
    cache['edges'] = new_edges
    cache['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000000')
    return cache, list(ghosts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', default=CACHE_PATH)
    parser.add_argument('--out', default=OUTPUT_REPORT.format(datetime.now().strftime('%Y%m%d')))
    parser.add_argument('--log', default=LOG_PATH)
    parser.add_argument('--auto', action='store_true', help='Enable auto-fix (safe removals)')
    args = parser.parse_args()

    data = load_cache(args.cache)
    issues = detect_issues(data)
    report = generate_report(issues)
    # Write report
    os.makedirs('synthesis', exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(report)
    # Optional auto-fix
    fixed_nodes = []
    if args.auto:
        data, fixed_nodes = apply_auto_fix(data, issues)
        with open(args.cache, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    # Write log
    with open(args.log, 'a', encoding='utf-8') as lf:
        lf.write("\n")
        lf.write(f"## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Comprehensive GC\n")
        lf.write(report)
        if fixed_nodes:
            lf.write("\nAuto-fixed ghosts:\n")
            for n in fixed_nodes:
                lf.write(f"- {n}\n")

if __name__ == '__main__':
    main()
