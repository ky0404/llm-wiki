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
all_links = set()
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
                all_links.add(target)
                link_to_pages.setdefault(target, set()).add(rel_page)

# 3. Broken links: links that do not correspond to an existing page
broken_links = []
for link in all_links:
    # Normalize: we assume the link is relative to wiki and without .md
    if link not in existing_pages:
        broken_links.append(link)

# 4. Orphaned pages: pages that are not linked from any other page (excluding self-links?)
# We consider a page orphaned if no other page links to it.
# We'll ignore links from the page to itself? But we didn't collect self-links because our pattern would have caught [[page|...]]? Actually if a page links to itself, it would be in link_to_pages[page] including itself.
# We'll compute incoming links excluding self-links? Let's just compute incoming links from link_to_pages and then see if the set of incoming links (excluding self) is empty.
orphaned = []
for page in existing_pages:
    incoming = link_to_pages.get(page, set())
    # Remove self-links if present
    if page in incoming:
        incoming = incoming - {page}
    if len(incoming) == 0:
        orphaned.append(page)

# 5. Check frontmatter: we already know all have frontmatter from earlier check, but we can double-check
no_frontmatter = []
for root, dirs, files in os.walk(WIKI_DIR):
    for f in files:
        if f.endswith('.md'):
            page_path = os.path.join(root, f)
            with open(page_path, 'r', encoding='utf-8') as fp:
                first_line = fp.readline().rstrip('\n')
                if first_line != '---':
                    rel_path = os.path.relpath(page_path, WIKI_DIR)
                    no_frontmatter.append(rel_path)

# 6. Check raw files processed: look at log for lines that contain "处理 raw/"
processed_raw = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as fp:
        for line in fp:
            if '处理 raw/' in line:
                # Extract the raw filename: after 'raw/' until the next space or '→'
                # Example: "处理 raw/CLAUDE.md → wiki/sources/CLAUDE.md"
                # We'll take the substring after 'raw/' and until a space or '→'
                import re
                match = re.search(r'raw/([^\\s→]+)', line)
                if match:
                    processed_raw.add(match.group(1))

# Now list all raw .md files
raw_files = []
for f in os.listdir(RAW_DIR):
    if f.endswith('.md'):
        raw_files.append(f)

unprocessed_raw = [f for f in raw_files if f not in processed_raw]

# Output results
print("=== Lint Check Results ===")
print()
if broken_links:
    print(f"Broken wikilinks ({len(broken_links)}):")
    for link in sorted(broken_links):
        print(f"  - [[{link}]]")
else:
    print("No broken wikilinks.")
print()
if orphaned:
    print(f"Orphaned pages ({len(orphaned)}):")
    for page in sorted(orphaned):
        print(f"  - {page}.md")
else:
    print("No orphaned pages.")
print()
if no_frontmatter:
    print(f"Pages missing frontmatter ({len(no_frontmatter)}):")
    for p in sorted(no_frontmatter):
        print(f"  - {p}")
else:
    print("All pages have frontmatter.")
print()
if unprocessed_raw:
    print(f"Unprocessed raw files ({len(unprocessed_raw)}):")
    for f in sorted(unprocessed_raw):
        print(f"  - {f}")
else:
    print("All raw .md files have been processed (according to log).")
print()
# Also report raw pdfs? Not required.
print("=== End of Lint Check ===")