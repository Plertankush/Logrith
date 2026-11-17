#!/usr/bin/env python3
"""Regenerate sitemap.xml and its child sitemaps (English and Spanish) from each page's canonical URL.

Run from the repository root:

    python3 scripts/build_sitemaps.py

sitemap.xml is a flat index. The sitemap protocol does not allow an index to list another index,
so every language gets one child sitemap per section, named sitemap-<lang>-<section>.xml:

    pages        home, /pages/*, the tool hub and its category pages
    ai-technology, startups-business   the two topic areas (hub + articles)
    blog         tool guides (/tool/blog/*)
    tools        every tool, including the Global ones

A page's canonical tag is the single source of truth, so a page whose canonical is wrong shows up
here (the script exits non-zero if an English canonical does not match the URL its file is served at).
Spanish pages are the /es/ copies whose <html> has lang="es"; every translated page is listed with
its hreflang cluster on both the English and the Spanish entry.
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
LANGUAGES = ('en', 'es')

# section -> (predicate on the URL path without its language prefix, changefreq, priority)
SECTIONS = {
    'pages':            (lambda p: p == '/' or p.startswith('/pages/') or p == '/tool/' or p.startswith('/tool/categories/'), 'weekly', '0.8'),
    'ai-technology':    (lambda p: p.startswith('/ai-technology/'), 'weekly', '0.9'),
    'startups-business': (lambda p: p.startswith('/startups-business/'), 'weekly', '0.9'),
    'blog':             (lambda p: p.startswith('/tool/blog/'), 'monthly', '0.6'),
    'tools':            (lambda p: p.startswith('/tool/tools/'), 'monthly', '0.8'),
}

URLSET_OPEN = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
               'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')


def url_for(file: Path) -> str:
    rel = file.relative_to(ROOT).with_suffix('').as_posix()
    if rel == 'index':
        return '/'
    if rel.endswith('/index'):
        return '/' + rel[: -len('index')]
    return '/' + rel


def served_path(file: Path) -> str:
    """The clean URL a file is served at, honouring the Global Tools rewrites."""
    return url_for(file).replace('/tool/tools/global/', '/tool/tools/')


def find(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else None


def scan_english(problems):
    """{canonical path: file} for every English page."""
    pages = {}
    for file in sorted(ROOT.rglob('*.html')):
        rel = file.relative_to(ROOT)
        if rel.name in SKIP or rel.parts[0] in ('assets', 'components', 'node_modules', '.git', 'es') or rel.parts[0].startswith('_'):
            continue
        canonical = find(r'<link rel="canonical" href="([^"]+)"', file.read_text(encoding='utf-8'))
        if not canonical:
            problems.append(f'no canonical: {rel}')
            continue
        path = urlparse(canonical).path
        if path != served_path(file):
            problems.append(f'canonical mismatch: {rel} -> {path} (expected {served_path(file)})')
        pages[path] = file
    return pages


def scan_spanish(problems):
    """{Spanish canonical path: English canonical path} for every translated /es/ page."""
    pages = {}
    for file in sorted((ROOT / 'es').rglob('*.html')):
        text = file.read_text(encoding='utf-8')
        if not re.search(r'<html[^>]*\blang="es"', text):
            continue   # still an untranslated English copy
        canonical = find(r'<link rel="canonical" href="([^"]+)"', text)
        english = find(r'<link rel="alternate" hreflang="en" href="([^"]+)"', text)
        if not canonical or not english:
            problems.append(f'es page without canonical/hreflang: {file.relative_to(ROOT)}')
            continue
        pages[urlparse(canonical).path] = urlparse(english).path
    return pages


def entry(path, freq, priority, alternates):
    """One <url>. alternates is {} or {'en': english path, 'es': spanish path}."""
    lines = [f'<loc>{SITE}{path}</loc>', f'<lastmod>{TODAY}</lastmod>', f'<changefreq>{freq}</changefreq>', f'<priority>{priority}</priority>']
    if alternates:
        for lang, href in (('en', alternates['en']), ('es', alternates['es']), ('x-default', alternates['en'])):
            lines.append(f'<xhtml:link rel="alternate" hreflang="{lang}" href="{SITE}{href}"/>')
    return '<url>\n' + '\n'.join(lines) + '\n</url>\n'


def main() -> int:
    problems = []
    english = scan_english(problems)
    spanish = scan_spanish(problems)          # es path -> en path
    spanish_of = {en: es for es, en in spanish.items()}

    # language -> {path without prefix: (full path, alternates)}
    catalogue = {
        'en': {p: (p, {'en': p, 'es': spanish_of[p]} if p in spanish_of else {}) for p in english},
        'es': {en: (es, {'en': en, 'es': es}) for es, en in spanish.items()},
    }

    written, assigned = [], {lang: set() for lang in LANGUAGES}
    for lang in LANGUAGES:
        for section, (predicate, freq, priority) in SECTIONS.items():
            keys = sorted(k for k in catalogue[lang] if k not in assigned[lang] and predicate(k))
            assigned[lang].update(keys)
            name = f'sitemap-{lang}-{section}.xml'
            body = ''.join(entry(catalogue[lang][k][0], freq, '1.0' if k == '/' else priority, catalogue[lang][k][1]) for k in keys)
            (ROOT / name).write_text(URLSET_OPEN + body + '</urlset>\n')
            written.append((name, len(keys)))
        leftover = sorted(set(catalogue[lang]) - assigned[lang])
        if leftover:
            problems.append(f'{lang} pages in no sitemap: {leftover}')

    # Remove sitemap files from earlier layouts so nothing stale stays published.
    names = {name for name, _ in written}
    for old in ROOT.glob('sitemap-*.xml'):
        if old.name not in names:
            old.unlink()

    index = ''.join(f'<sitemap>\n<loc>{SITE}/{name}</loc>\n<lastmod>{TODAY}</lastmod>\n</sitemap>\n' for name, _ in written)
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + index + '</sitemapindex>\n')
    (ROOT / 'robots.txt').write_text(
        'User-agent: *\nAllow: /\n\nSitemap: ' + f'{SITE}/sitemap.xml\n' + ''.join(f'Sitemap: {SITE}/{n}\n' for n, _ in written))

    for name, count in written:
        print(f'{name}: {count} URLs')
    for problem in problems:
        print('PROBLEM:', problem)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
