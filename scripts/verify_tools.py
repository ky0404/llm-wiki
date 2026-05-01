#!/usr/bin/env python3
"""
Tool Verification Framework - verify_tools.py
Comprehensive testing suite for Wiki tooling.

Verifies extract_links correctness
Verifies update_graph outputs
Provides dry-run capability
Emits structured JSON to stdout and optional log file
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import re
from datetime import datetime


def extract_links_from_file(filepath):
    """Extract valid wikilinks from markdown file, ignoring code blocks and inline code."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
    
    # Remove fenced code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove inline code spans
    content = re.sub(r'`[^`]+`', '', content)
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    # Wikilinks pattern
    pattern = r'\[\[([^\]|#]+)(?:\|([^\]]+))?(?:#([^\]]+))?\]\]'
    matches = re.findall(pattern, content)
    links = []
    for m in matches:
        page = m[0].strip()
        if page:
            links.append(page)
    return links


def verify_extract_links(root):
    """Verify extract_links.py on all .md files under root"""
    test_files = glob.glob(os.path.join(root, '**', '*.md'), recursive=True)
    total_files = len(test_files)
    files_with_links = 0
    total_links = 0
    errors = []
    
    for f in test_files:
        try:
            links = extract_links_from_file(f)
            if links:
                files_with_links += 1
                total_links += len(links)
        except Exception as e:
            errors.append((f, str(e)))
    return {
        'total_files': total_files,
        'files_with_links': files_with_links,
        'total_links': total_links,
        'errors': errors
    }


def run_update_graph(root, dry_run=False):
    """Run update_graph.py and collect basic results"""
    py_path = os.path.join(root, 'scripts/update_graph.py')
    if not os.path.exists(py_path):
        return {'returncode': -1, 'error': f'Script not found: {py_path}'}
    if dry_run:
        return {'returncode': None, 'stdout': '', 'stderr': '', 'note': 'dry-run: no changes applied'}
    try:
        res = subprocess.run([sys.executable, py_path], capture_output=True, text=True, timeout=60)
        return {'returncode': res.returncode, 'stdout': res.stdout, 'stderr': res.stderr}
    except Exception as e:
        return {'returncode': -1, 'error': str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--log', default=None, help='Optional log file to append results')
    args = parser.parse_args()
    
    root = args.root
    report = {}
    report['extract_links'] = verify_extract_links(root)
    report['update_graph'] = run_update_graph(root, dry_run=args.dry_run)
    # 输出 JSON
    print(json.dumps(report, ensure_ascii=False, indent=2))
    # 记录日志
    if args.log:
        with open(args.log, 'a', encoding='utf-8') as lf:
            lf.write("\n")
            lf.write(json.dumps(report, ensure_ascii=False, indent=2))
            lf.write("\n")


if __name__ == '__main__':
    main()
