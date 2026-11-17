#!/usr/bin/env python3
"""Generate assets/data/tools.json (English) and assets/data/tools.es.json (Spanish), the indexes behind
the site-wide tool search.

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
OUT_ES = ROOT / 'assets' / 'data' / 'tools.es.json'

CATEGORIES = {
    'image-pdf-tools': 'Image & PDF',
    'calculate-convert': 'Calculate & Convert',
    'developer-tools': 'Developer',
    'text-generators': 'Text & Generators',
    'utilities': 'Utilities',
    'ai-tools': 'AI',
    'global-tools': 'Global',
}

CATEGORIES_ES = {
    'image-pdf-tools': 'Imagen y PDF',
    'calculate-convert': 'Calcular y convertir',
    'developer-tools': 'Desarrollo',
    'text-generators': 'Texto y generadores',
    'utilities': 'Utilidades',
    'ai-tools': 'IA',
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

# The same pages in Spanish.
OVERRIDES_ES = {
    'gst-calculator': ('Calculadora de GST', 'calculate-convert'),
    'hash-generator': ('Generador de hash', 'developer-tools'),
    'image-compressor': ('Compresor de imágenes', 'image-pdf-tools'),
    'image-converter': ('Convertidor de imágenes', 'image-pdf-tools'),
    'resume-analyzer': ('Analizador de currículums', 'ai-tools'),
    'website-speed-analyzer': ('Analizador de velocidad de sitios web', 'ai-tools'),
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


def build_index(tools_dir, categories, overrides, url_prefix=''):
    """Index entries for every tool page under tools_dir. URLs are stored without url_prefix (/es)."""
    tools = []
    for page in sorted(tools_dir.rglob('*.html')):
        text = page.read_text(encoding='utf-8')
        canonical = first(r'<link rel="canonical" href="([^"]+)"', text)
        url = urlparse(canonical).path if canonical else f'{url_prefix}/tool/tools/{page.stem}'
        url = url[len(url_prefix):] if url_prefix and url.startswith(url_prefix) else url
        crumbs = breadcrumb(text)
        if page.stem in overrides:
            name, slug = overrides[page.stem]
        elif len(crumbs) >= 3:
            name = crumbs[-1]['name']
            slug = urlparse(crumbs[-2]['item']).path.rsplit('/', 1)[-1]
        else:
            print(f'skipped {page.relative_to(ROOT)}: no breadcrumb schema and no override')
            continue
        tools.append({
            'name': name,
            'category': categories.get(slug, 'Tools'),
            'url': url,
            'summary': first(r'<meta name="description" content="([^"]*)"', text),
        })
    tools.sort(key=lambda t: t['name'].lower())
    return tools


def main():
    for tools_dir, out, categories, overrides, prefix in (
        (ROOT / 'tool' / 'tools', OUT, CATEGORIES, OVERRIDES, ''),
        (ROOT / 'es' / 'tool' / 'tools', OUT_ES, CATEGORIES_ES, OVERRIDES_ES, '/es'),
    ):
        tools = build_index(tools_dir, categories, overrides, prefix)
        out.write_text(json.dumps(tools, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(f'wrote {len(tools)} tools to {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
