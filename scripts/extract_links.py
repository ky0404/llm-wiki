#!/usr/bin/env python3
"""
Wiki Link Extractor
Reads a specified .md file, strips code blocks (inline and fenced), 
and extracts valid [[wikilinks]] using regex.
"""

import re
import sys


def extract_links_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return []

    # Remove fenced code blocks (```)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    # Remove inline code spans (`) to avoid matching `[[...]]`
    content = re.sub(r'`[^`]+`', '', content)
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Extract wikilinks
    pattern = r'\[\[([^\]|#]+)(?:\|([^\]]+))?(?:#([^\]]+))?\]\]'
    matches = re.findall(pattern, content)
    
    links = []
    for match in matches:
        # match[0] is the page name
        page = match[0].strip()
        if page:
            links.append(page)
            
    return links


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract_links.py <markdown_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    valid_links = extract_links_from_file(file_path)
    
    print(f"Found {len(valid_links)} valid wikilinks in {file_path}:")
    for link in valid_links:
        print(f"  - {link}")
