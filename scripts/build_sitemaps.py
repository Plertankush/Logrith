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
    ('sitemap-topics.xml', lambda p: p.split('/')[1] in ('ai-technology', 'startups-business', 'marketing-growth'), 'weekly', '0.9'),
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


def main() -> int:
    pages, problems = {}, []
    for file in sorted(ROOT.rglob('*.html')):
        rel = file.relative_to(ROOT)
        if rel.name in SKIP or rel.parts[0] in ('assets', 'components', 'node_modules', '.git') or rel.parts[0].startswith('_'):
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
