#!/usr/bin/env python3
"""Generate assets/data/tools.json, the index behind the site-wide tool search.

Run from the repository root after adding or renaming a tool page:

    python3 scripts/build_search_index.py

Each tool page supplies its own entry: the name and category come from its
BreadcrumbList JSON-LD, the URL from <link rel="canonical"> and the summary
from <meta name="description">. Pages without that schema are listed in
OVERRIDES below.
"""
import json
import re
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'data' / 'tools.json'

CATEGORIES = {
    'image-pdf-tools': 'Image & PDF',
    'calculate-convert': 'Calculate & Convert',
    'developer-tools': 'Developer',
    'text-generators': 'Text & Generators',
    'utilities': 'Utilities',
    'ai-tools': 'AI',
    'global-tools': 'Global',
}

# Tool pages that have no BreadcrumbList schema: file stem -> (name, category slug)
OVERRIDES = {
    'gst-calculator': ('GST Calculator', 'calculate-convert'),
    'hash-generator': ('Hash Generator', 'developer-tools'),
    'image-compressor': ('Image Compressor', 'image-pdf-tools'),
    'image-converter': ('Image Converter', 'image-pdf-tools'),
    'resume-analyzer': ('Resume Analyzer', 'ai-tools'),
    'website-speed-analyzer': ('Website Speed Analyzer', 'ai-tools'),
}


def first(pattern, text, flags=0):
    m = re.search(pattern, text, flags)
    return unescape(m.group(1)).strip() if m else ''


def breadcrumb(text):
    for block in re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', text, re.S):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        if data.get('@type') == 'BreadcrumbList':
            return data['itemListElement']
    return []


def main():
    tools = []
    for page in sorted((ROOT / 'tool' / 'tools').rglob('*.html')):
        text = page.read_text(encoding='utf-8')
        canonical = first(r'<link rel="canonical" href="([^"]+)"', text)
        url = urlparse(canonical).path if canonical else f'/tool/tools/{page.stem}'
        crumbs = breadcrumb(text)
        if page.stem in OVERRIDES:
            name, slug = OVERRIDES[page.stem]
        elif len(crumbs) >= 3:
            name = crumbs[-1]['name']
            slug = urlparse(crumbs[-2]['item']).path.rsplit('/', 1)[-1]
        else:
            print(f'skipped {page.relative_to(ROOT)}: no breadcrumb schema and no override')
            continue
        tools.append({
            'name': name,
            'category': CATEGORIES.get(slug, 'Tools'),
            'url': url,
            'summary': first(r'<meta name="description" content="([^"]*)"', text),
        })
    tools.sort(key=lambda t: t['name'].lower())
    OUT.write_text(json.dumps(tools, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'wrote {len(tools)} tools to {OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
