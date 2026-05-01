#!/usr/bin/env python3
import os
import re
import sys

WIKI_DIR = '/mnt/d/projects/wiki/wiki'
RAW_DIR = '/mnt/d/projects/wiki/raw'
LOG_FILE = '/mnt/d/projects/wiki/wiki/log.md'

# 1. Collect all existing wiki pages (without .md, relative to wiki)
existing_pages = set()
for root, dirs, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith('.md'):
            rel_path = os.path.relpath(os.path.join(root, f), WIKI_DIR)
            # Remove .md
            rel_path = rel_path[:-3]
            existing_pages.add(rel_path)

# 2. Extract all wikilinks from all wiki pages
link_pattern = re.compile(r'\[\[([^|\]]+)(?:\|[^\]]+)?\]\]')
all_links = []
link_to_pages = {}  # For reverse index: which pages link to a target
for root, dirs, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith('.md'):
            page_path = os.path.join(root, f)
            rel_page = os.path.relpath(page_path, WIKI_DIR)[:-3]  # without .md
            with open(page_path, 'r', encoding='utf-8') as fp:
                content = fp.read()
            for match in link_pattern.finditer(content):
                target = match.group(1).strip()
                all_links.append((target, rel_page))  # Store with source page
                link_to_pages.setdefault(target, set()).add(rel_page)

# 3. Identify potential false positives (documentation examples)
# Patterns that are likely documentation examples, not real intended links
false_positive_patterns = [
    r'页面名称',  # Chinese for "page name"
    r'标题',     # Chinese for "title" or "heading"  
    r'块ID',     # Chinese for "block ID"
    r'显示文本', # Chinese for "display text"
    r'链接到',   # Chinese for "link to"
    r'文本$',    # Ends with "text" 
    r'页面$',    # Ends with "page"
    r'^\^.+',    # Starts with ^ (like ^blockID)
    r'#.+#',     # Contains #...# patterns
    r'\|.*\|',   # Contains |...| (alias syntax in examples)
]

def is_likely_false_positive(link):
    """Check if a link is likely a documentation example rather than a real intended link"""
    link_lower = link.lower()
    # Check against patterns
    for pattern in false_positive_patterns:
        if re.search(pattern, link, re.IGNORECASE):
            return True
    # Additional heuristics
    if link in ['页面名称', '标题', '块ID', '显示文本', '链接到']:
        return True
    if link.startswith('页面名称') or link.endswith('页面名称'):
        return True
    if link.startswith('标题') or link.endswith('标题'):
        return True
    # Links that look like they're showing syntax examples
    if '[[[' in link or ']]]' in link:  # Contains triple brackets
        return True
    return False

# 4. Find real broken links (not false positives)
real_broken_links = []
for link, source_page in all_links:
    # Skip if it's likely a false positive
    if is_likely_false_positive(link):
        continue
    # Normalize: we assume the link is relative to wiki and without .md
    if link not in existing_pages:
        real_broken_links.append((link, source_page))

# 5. Group by link for cleaner output
broken_links_dict = {}
for link, source in real_broken_links:
    if link not in broken_links_dict:
        broken_links_dict[link] = []
    broken_links_dict[link].append(source)

print("=== Real Broken Wikilinks Check ===")
print()
if broken_links_dict:
    print(f"Real broken wikilinks ({len(broken_links_dict)}):")
    for link in sorted(broken_links_dict.keys()):
        sources = broken_links_dict[link]
        print(f"  - [[{link}]]")
        print(f"    Referenced in: {', '.join(sorted(sources))}")
else:
    print("No real broken wikilinks found (all apparent broken links appear to be documentation examples).")
print()

# Also check for orphaned pages with better logic
print("=== Orphaned Pages Check (improved) ===")
print()
# A page is not orphaned if:
# 1. It's referenced in index.md (even without wikilinks, e.g. plain text mention)
# 2. It has incoming wikilinks from other pages
# 3. It's a template (we expect templates to be referenced but not necessarily via wikilinks in content)
# 4. It's in the sources list in index.md (we'll check this specially)

# First, let's see what's in index.md
index_page = os.path.join(WIKI_DIR, 'index.md')
index_content = ""
if os.path.exists(index_page):
    with open(index_page, 'r', encoding='utf-8') as f:
        index_content = f.read()

# Extract all mentioned files from index.md (simple approach)
mentioned_in_index = set()
# Look for [[sources/...]] patterns
source_pattern = re.compile(r'\[\[sources/[^\]]+\]\]')
for match in source_pattern.finditer(index_content):
    link_content = match.group(0)[2:-2]  # Remove [[ and ]]
    mentioned_in_index.add(link_content)

# Also look for direct mentions of filenames (less reliable)
for root, dirs, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith('.md'):
            name_without_ext = f[:-3]
            # Check if this filename (without .md) is mentioned in index.md
            if name_without_ext in index_content:
                mentioned_in_index.add(name_without_ext)

# Now check each page
orphaned = []
for page in existing_pages:
    # Skip index.md itself (it's the main directory)
    if page == 'index.md':
        continue
        
    # Skip templates - they're meant to be referenced but not necessarily via wikilinks in content
    if page.startswith('templates/'):
        continue
        
    # Check if it has incoming wikilinks
    incoming = link_to_pages.get(page, set())
    # Remove self-links if present
    if page in incoming:
        incoming = incoming - {page}
        
    # Check if it's mentioned in index.md
    mentioned_in_idx = page in mentioned_in_index
    
    # If no incoming links AND not mentioned in index, then it's truly orphaned
    if len(incoming) == 0 and not mentioned_in_idx:
        orphaned.append(page)

if orphaned:
    print(f"Orphaned pages ({len(orphaned)}):")
    for page in sorted(orphaned):
        print(f"  - {page}.md")
else:
    print("No orphaned pages found.")
print()

# Check unprocessed raw files with better log parsing
print("=== Unprocessed Raw Files Check (improved) ===")
print()
processed_raw = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as fp:
        for line in fp:
            # Look for patterns like "处理 raw/FILENAME.md →" or "处理 raw/FILENAME.md"
            match = re.search(r'处理\s+raw/([^\s→]+?\.md)', line)
            if match:
                processed_raw.add(match.group(1))

# Now list all raw .md files
raw_files = []
for f in os.listdir(RAW_DIR):
    if f.endswith('.md'):
        raw_files.append(f)

unprocessed_raw = [f for f in raw_files if f not in processed_raw]

if unprocessed_raw:
    print(f"Unprocessed raw files ({len(unprocessed_raw)}):")
    for f in sorted(unprocessed_raw):
        print(f"  - {f}")
else:
    print("All raw .md files have been processed (according to improved log parsing).")
print()
print("=== End of Improved Lint Check ===")