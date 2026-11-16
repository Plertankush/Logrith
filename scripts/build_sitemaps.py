#!/usr/bin/env python3
"""Regenerate sitemap.xml and its child sitemaps from the canonical URL of every page.

Run from the repository root:

    python3 scripts/build_sitemaps.py

A page's canonical tag is the single source of truth, so a page whose canonical
is wrong shows up here (the script exits non-zero if a canonical does not match
the URL its file is served at).
"""
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://logrith.in'
TODAY = date.today().isoformat()
SKIP = {'404.html'}

# child sitemap -> (predicate on URL path, changefreq, priority)
GROUPS = [
    ('sitemap-pages.xml',  lambda p: p == '/' or p.startswith('/pages/') or p == '/tool/' or p.startswith('/tool/categories/'), 'weekly', '0.8'),
    ('sitemap-topics.xml', lambda p: p.split('/')[1] in ('ai-technology', 'startups-business'), 'weekly', '0.9'),
    ('sitemap-blog.xml',   lambda p: p.startswith('/tool/blog/'), 'monthly', '0.6'),
    ('sitemap-global.xml', lambda p: p.startswith('/tool/tools/') and p in GLOBAL_PATHS, 'monthly', '0.7'),
    ('sitemap-tools.xml',  lambda p: p.startswith('/tool/tools/'), 'monthly', '0.8'),
]
GLOBAL_PATHS = set()


def url_for(file: Path) -> str:
    rel = file.relative_to(ROOT).with_suffix('').as_posix()
    if rel == 'index':
        return '/'
    if rel.endswith('/index'):
        return '/' + rel[: -len('index')]
    return '/' + rel


def served_path(file: Path) -> str:
    """The clean URL a file is served at, honouring the Global Tools rewrites."""
    path = url_for(file)
    return path.replace('/tool/tools/global/', '/tool/tools/')


def build_spanish_sitemap(problems):
    """sitemap-es.xml lists only translated /es/ pages (lang="es"), each with its hreflang cluster."""
    entries = []
    for file in sorted((ROOT / 'es').rglob('*.html')):
        text = file.read_text(encoding='utf-8')
        if not re.search(r'<html[^>]*\blang="es"', text):
            continue   # still an untranslated English copy
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        english = re.search(r'<link rel="alternate" hreflang="en" href="([^"]+)"', text)
        if not canonical or not english:
            problems.append(f'es page without canonical/hreflang: {file.relative_to(ROOT)}')
            continue
        es_url = canonical.group(1)
        entries.append(
            f'<url>\n<loc>{es_url}</loc>\n<lastmod>{TODAY}</lastmod>\n'
            f'<xhtml:link rel="alternate" hreflang="en" href="{english.group(1)}"/>\n'
            f'<xhtml:link rel="alternate" hreflang="es" href="{es_url}"/>\n'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{english.group(1)}"/>\n</url>\n')
    if entries:
        (ROOT / 'sitemap-es.xml').write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + ''.join(entries) + '</urlset>\n')
    return len(entries)


def main() -> int:
    pages, problems = {}, []
    for file in sorted(ROOT.rglob('*.html')):
        rel = file.relative_to(ROOT)
        if rel.name in SKIP or rel.parts[0] in ('assets', 'components', 'node_modules', '.git', 'es') or rel.parts[0].startswith('_'):
            continue
        match = re.search(r'<link rel="canonical" href="([^"]+)"', file.read_text(encoding='utf-8'))
        if not match:
            problems.append(f'no canonical: {rel}')
            continue
        canonical = urlparse(match.group(1)).path
        if canonical != served_path(file):
            problems.append(f'canonical mismatch: {rel} -> {canonical} (expected {served_path(file)})')
        pages[canonical] = '/tool/tools/global/' in url_for(file)
        if pages[canonical]:
            GLOBAL_PATHS.add(canonical)

    written, assigned = [], set()
    for name, predicate, freq, priority in GROUPS:
        paths = sorted(p for p in pages if p not in assigned and predicate(p))
        assigned.update(paths)
        entries = ''.join(
            f'<url>\n<loc>{SITE}{p}</loc>\n<lastmod>{TODAY}</lastmod>\n<changefreq>{freq}</changefreq>\n<priority>{"1.0" if p == "/" else priority}</priority>\n</url>\n'
            for p in paths)
        (ROOT / name).write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + '</urlset>\n')
        written.append((name, len(paths)))

    leftover = sorted(set(pages) - assigned)
    if leftover:
        problems.append(f'pages in no sitemap: {leftover}')

    spanish = build_spanish_sitemap(problems)
    if spanish:
        written.append(('sitemap-es.xml', spanish))

    index = ''.join(f'<sitemap>\n<loc>{SITE}/{name}</loc>\n<lastmod>{TODAY}</lastmod>\n</sitemap>\n' for name, _ in written)
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + index + '</sitemapindex>\n')

    robots = 'User-agent: *\nAllow: /\n\nSitemap: ' + f'{SITE}/sitemap.xml\n' + ''.join(f'Sitemap: {SITE}/{n}\n' for n, _ in written)
    (ROOT / 'robots.txt').write_text(robots)

    for name, count in written:
        print(f'{name}: {count} URLs')
    for problem in problems:
        print('PROBLEM:', problem)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
