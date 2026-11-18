#!/usr/bin/env python3
"""Build the Spanish (/es/) version of the site from the English pages.

Run from the repository root, on a machine that can reach your Apps Script URL:

    pip install beautifulsoup4
    export ES_TRANSLATE_URL="https://script.google.com/macros/s/XXXX/exec"
    export ES_TRANSLATE_KEY="the-secret-from-your-apps-script"
    python3 scripts/translate_es.py --wave 1 --engine web

Waves are cumulative (``--wave 2`` also rebuilds wave 1) and every translated
string is cached in ``scripts/translations_es.json``, so re-running only sends
text that is new or changed.

    wave 1  home, AI & Developer Tools, Build & Ship (topics, subtopics, guides)
    wave 2  site pages, tools hub, tool categories
    wave 3  every tool page
    wave 4  tool blog

For each translated page the script
  * translates visible text, alt/title/placeholder/aria-label, meta tags and JSON-LD,
  * sets lang="es", a self-referencing /es/ canonical and an hreflang cluster
    (the English page gets the same cluster),
  * points internal links at the /es/ page when that page is translated,
  * leaves components/es/ alone: the Spanish navbar and footer are written by hand so the menu
    labels, search box and language links stay exact (keep them in step with components/).

Translation engines (``--engine``):
  web         free Google Translate web endpoint through the ``deep-translator`` package.
              No account, key or card. Unofficial, so it can rate-limit; just re-run later.
              Install with: pip install deep-translator beautifulsoup4
  appsscript  your own Google Apps Script web app (needs ES_TRANSLATE_URL and ES_TRANSLATE_KEY,
              and the deployment must allow "Anyone").
  fake        marks text with "[es]" instead of translating. Offline pipeline test.
  fake-web    same, but through the tag-protecting path that ``web`` uses.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
from bs4.element import Script
from bs4.dammit import EntitySubstitution
from bs4.formatter import HTMLFormatter

import js_strings

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://logrith.in'
CACHE_FILE = ROOT / 'scripts' / 'translations_es.json'
SKIP_DIRS = {'assets', 'components', 'es', 'scripts', 'node_modules', '.git'}

WAVES = {
    1: ['index.html', 'ai-technology/**/*.html', 'startups-business/**/*.html'],
    2: ['pages/*.html', 'tool/index.html', 'tool/categories/*.html'],
    3: ['tool/tools/**/*.html'],
    4: ['tool/blog/**/*.html'],
}

SKIP_TAGS = {'script', 'style', 'code', 'pre', 'svg', 'textarea', 'noscript', 'template', 'iframe', 'kbd', 'samp', 'canvas'}
BLOCK_TAGS = {'address', 'article', 'aside', 'blockquote', 'details', 'div', 'dl', 'dd', 'dt', 'fieldset', 'figure', 'footer', 'form',
              'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'li', 'main', 'nav', 'ol', 'p', 'section', 'summary', 'table', 'tbody',
              'thead', 'tr', 'td', 'th', 'ul', 'aside'}
TEXT_ATTRS = ('alt', 'title', 'placeholder', 'aria-label')
META_TEXT = [('name', 'description'), ('property', 'og:title'), ('property', 'og:description'), ('name', 'twitter:title'), ('name', 'twitter:description')]
JSONLD_TEXT_KEYS = {'name', 'description', 'text', 'headline', 'alternateName'}
PROTECTED = re.compile(r'<(code|kbd|svg|samp)\b.*?</\1>|\b(?:Logrith|Plert Ankush|AdSense)\b', re.S)
TAG = re.compile(r'<[^>]+>')

SCRIPT_PROTECTED = re.compile(PROTECTED.pattern + r'|\$\{\d+\}', re.S)   # inside scripts, ${n} marks inserted code
TOKEN = re.compile(r'§\s*(\d+)\s*§')
LETTERS = re.compile(r'[A-Za-z]{2,}')

MAX_BATCH_ITEMS = 40
MAX_BATCH_CHARS = 20000


class SourceOrderFormatter(HTMLFormatter):
    """Write attributes in their original order and void tags without a trailing slash, like the English pages."""

    def __init__(self, **options):
        # Escape & < > in text. Without this the formatter writes a sentence about "<script>" as a real tag.
        super().__init__(entity_substitution=EntitySubstitution.substitute_xml, **options)

    def attributes(self, tag):
        return tag.attrs.items()


def serialize(soup):
    return soup.decode(formatter=SourceOrderFormatter(void_element_close_prefix=''))


# --------------------------------------------------------------------------
# Translation back ends and cache
# --------------------------------------------------------------------------

# Exact source strings whose machine translation is known to be wrong or awkward. They always win over the
# translator, and are written into the cache before every run. Add the "&amp;" spelling next to a "&" one.
GLOSSARY = {
    'Home': 'Inicio',
    'Breadcrumb': 'Ruta de navegación',
    'Utilities': 'Utilidades',
    'Smallpdf': 'Smallpdf',
    'EMI Calculator': 'Calculadora de cuotas EMI',
    'Server upload': 'Subida a un servidor',
    'Passphrase Generator': 'Generador de frases de contraseña',
    'More in Build & Ship': 'Más en Construir y enviar',
    'More in AI & Developer Tools': 'Más en Herramientas de IA y para desarrolladores',
    **{f'{n} min read': f'{n} min de lectura' for n in range(1, 21)},
}


class Cache:
    """Translated strings keyed by a hash of the source. Saved atomically after every batch."""

    def __init__(self, path):
        self.path = path
        self.data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

    @staticmethod
    def key(text):
        return hashlib.sha1(text.encode('utf-8')).hexdigest()

    def get(self, text):
        return self.data.get(self.key(text))

    def put(self, text, translation):
        self.data[self.key(text)] = translation

    def discard(self, text):
        self.data.pop(self.key(text), None)

    def save(self):
        temporary = self.path.with_suffix('.tmp')
        temporary.write_text(json.dumps(self.data, ensure_ascii=False, indent=0, sort_keys=True), encoding='utf-8')
        os.replace(temporary, self.path)    # a crash can never leave a half-written cache


class TranslatorStop(Exception):
    """Translating cannot continue right now (quota used up, bad key, deployment problem)."""


def page_message(body):
    """The readable text of an HTML error page, without scripts, styles and tags."""
    body = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', body)
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', body))).strip()[:300]


class AppsScriptTranslator:
    """Sends batches of strings to a Google Apps Script web app that wraps LanguageApp.translate.

    The script answers {"translations": [...]} and, if LanguageApp fails part-way, adds an "error" text
    next to the strings it did finish, so nothing already paid for in quota is lost.
    """
    QUOTA_HINTS = ('too many times', 'quota', 'rate limit', 'exceeded')

    def __init__(self, url, key):
        self.url, self.key = url, key
        self.stop_reason = None

    def translate(self, texts):
        for attempt in range(5):
            try:
                return self._request(texts)
            except TranslatorStop:
                raise
            except Exception as error:
                if attempt == 4:
                    raise TranslatorStop(f'gave up after 5 attempts: {error}') from error
                wait = 5 * 2 ** attempt
                print(f'  attempt {attempt + 1} failed: {error}\n  waiting {wait}s')
                time.sleep(wait)

    def _request(self, texts):
        payload = json.dumps({'key': self.key, 'texts': texts}).encode('utf-8')
        request = urllib.request.Request(self.url, payload, {'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                status, final_url, kind, body = response.status, response.geturl(), response.headers.get('Content-Type', ''), response.read()
        except urllib.error.HTTPError as error:
            status, final_url, kind, body = error.code, error.url, error.headers.get('Content-Type', ''), error.read()
        body = body.decode('utf-8', 'replace')

        try:
            result = json.loads(body)
        except json.JSONDecodeError:
            message = page_message(body)
            detail = f'HTTP {status}, {kind or "no content type"}, from {urlparse(final_url).netloc}: "{message}"'
            if any(hint in message.lower() for hint in self.QUOTA_HINTS):
                raise TranslatorStop(f'Apps Script reports a quota problem. {detail}')
            raise RuntimeError(f'reply was not JSON. {detail}')

        translations = result.get('translations', [])
        if result.get('error'):
            self.stop_reason = result['error']
        elif len(translations) != len(texts):
            raise RuntimeError(f'asked for {len(texts)} translations, got {len(translations)}')
        return translations


class FakeTranslator:
    """Marks text instead of translating it, so the pipeline can be tested offline."""

    def translate(self, texts):
        return [f'[es] {text}' for text in texts]


class WebTranslator:
    """Free Google Translate web endpoint (deep-translator).

    It only understands plain text, so HTML tags are swapped for tokens before sending and put back
    afterwards. Strings keep the same cache keys as the Apps Script engine, so both can share one cache.
    A string whose tags come back damaged returns None and stays untranslated (it is retried next run).
    """
    MAX_CHARS = 4800

    def __init__(self):
        try:
            from deep_translator import GoogleTranslator
        except ImportError:
            sys.exit('Install the engine first: pip install deep-translator')
        self.client = GoogleTranslator(source='en', target='es')

    def translate(self, texts):
        results = []
        for text in texts:
            results.append(self._translate_one(text))
            time.sleep(0.25)
        return results

    def _call(self, text):
        for attempt in range(5):
            try:
                return self.client.translate(text) or text
            except Exception as error:   # rate limit or network hiccup
                if attempt == 4:
                    raise TranslatorStop(f'web translator failed repeatedly: {error}') from error
                wait = 10 * 2 ** attempt
                print(f'  attempt {attempt + 1} failed: {error}\n  waiting {wait}s')
                time.sleep(wait)

    def _translate_one(self, text):
        if len(text) > self.MAX_CHARS:
            return None
        base = len(TOKEN.findall(text))          # tokens 0..base-1 already protect code and brand names
        tags = []

        def hide(match):
            tags.append(match.group(0))
            return f'§{base + len(tags) - 1}§'

        masked = TAG.sub(hide, text)
        reply = self._call(masked)
        if sorted(int(n) for n in TOKEN.findall(reply)) != list(range(base + len(tags))):
            return None                          # a token was lost or duplicated
        result = TOKEN.sub(lambda m: tags[int(m.group(1)) - base] if int(m.group(1)) >= base else m.group(0), reply)
        return result if tags_nest_properly(result) else None


class FakeWebTranslator(WebTranslator):
    """WebTranslator's tag handling with a fake translation call (offline test)."""

    def __init__(self):
        pass

    def _call(self, text):
        return f'[es] {text}'

    def translate(self, texts):
        return [self._translate_one(text) for text in texts]


def translate_missing(texts, cache, translator, batch_items=MAX_BATCH_ITEMS):
    """Translate every string that is not cached yet, saving the cache after each batch.

    Raises TranslatorStop if translating cannot continue; everything finished before that is already saved.
    """
    pending = list(dict.fromkeys(t for t in texts if cache.get(t) is None))
    print(f'{len(texts)} strings, {len(pending)} new')
    done = failed = 0
    batch, size = [], 0

    def flush():
        nonlocal batch, size, done, failed
        if batch:
            stopped = None
            try:
                results = translator.translate(batch)
            except TranslatorStop as stop:
                results, stopped = [], stop
            for source, result in zip(batch, results):
                if result is None:
                    failed += 1
                else:
                    cache.put(source, result)
                    done += 1
            cache.save()
            print(f'  translated {done} so far, {len(pending) - done - failed} to go')
            reason = stopped or getattr(translator, 'stop_reason', None)
            if reason:
                raise TranslatorStop(str(reason))
        batch, size = [], 0

    for text in pending:
        if batch and (len(batch) >= batch_items or size + len(text) > MAX_BATCH_CHARS):
            flush()
        batch.append(text)
        size += len(text)
    flush()
    if failed:
        print(f'{failed} strings could not be translated safely; they stay in English and are retried next run')


# --------------------------------------------------------------------------
# Units: the pieces of a page that get translated
# --------------------------------------------------------------------------
class Unit:
    """One translatable string and how to write its translation back."""

    def __init__(self, source, apply, html=True, pattern=PROTECTED):
        self.html = html                      # True for inner HTML, False for plain text
        self.apply = apply                    # callback receiving the translated text
        self.sent, self.slots = protect(source if html else escape(source, quote=False), pattern)
        self.source = source


def protect(markup, pattern=PROTECTED):
    """Swap code, svg and brand names for numbered tokens so the translator cannot touch them."""
    slots = []

    def keep(match):
        slots.append(match.group(0))
        return f'§{len(slots) - 1}§'

    return pattern.sub(keep, markup), slots


def restore(unit, translated):
    """Put protected pieces back. Returns None if the translator broke the structure."""
    found = [int(n) for n in TOKEN.findall(translated)]
    if sorted(found) != list(range(len(unit.slots))):
        return None
    text = TOKEN.sub(lambda m: unit.slots[int(m.group(1))], translated)
    if unit.html:
        tags = lambda s: re.findall(r'</?([a-zA-Z][a-zA-Z0-9-]*)', s)
        if tags(text) != tags(unit.source):
            return None
        return text
    return unescape(text)


VOID_TAGS = {'br', 'img', 'hr', 'input', 'meta', 'link', 'wbr'}


def tags_nest_properly(markup):
    """True if every opening tag is closed in order (guards against a translator moving tokens around)."""
    stack = []
    for closing, name in re.findall(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)[^>]*>', markup):
        name = name.lower()
        if name in VOID_TAGS:
            continue
        if not closing:
            stack.append(name)
        elif not stack or stack.pop() != name:
            return False
    return not stack


def has_text(markup):
    return bool(LETTERS.search(re.sub(r'&#?\w+;', '', TAG.sub('', PROTECTED.sub('', markup)))))


def inner_html(element):
    """The element's contents as HTML. Text must be escaped: str() on a text node returns "<" and "&" raw,
    which let "&lt;script&gt;" in a sentence turn into a real <script> tag in the translated page."""
    return ''.join(escape(str(child), quote=False) if isinstance(child, NavigableString) and not isinstance(child, Comment)
                   else str(child) for child in element.children)


def collect_units(soup, scope):
    """Find everything visible (and the head metadata) that needs translating."""
    units = []

    def block_unit(element):
        source = inner_html(element)
        lead = source[:len(source) - len(source.lstrip())]
        tail = source[len(source.rstrip()):]

        def apply(text, el=element):
            el.clear()
            for node in list(BeautifulSoup(lead + text.strip() + tail, 'html.parser').contents):
                el.append(node)
        units.append(Unit(source.strip(), apply))

    def text_unit(node):
        raw = str(node)
        lead = raw[:len(raw) - len(raw.lstrip())]
        tail = raw[len(raw.rstrip()):]
        units.append(Unit(raw.strip(), lambda text, n=node: n.replace_with(NavigableString(lead + text + tail)), html=False))

    def has_block_descendant(element):
        return any(getattr(d, 'name', None) in BLOCK_TAGS for d in element.descendants)

    def walk(element):
        if element.name in SKIP_TAGS:
            return
        if not has_block_descendant(element):
            if has_text(inner_html(element)):
                block_unit(element)
            return
        for child in list(element.children):
            if isinstance(child, (Comment, Doctype)):
                continue
            if isinstance(child, NavigableString):
                if has_text(str(child)):
                    text_unit(child)
            elif child.name:
                walk(child)

    walk(scope)

    for element in scope.find_all(True):
        if any(parent.name in SKIP_TAGS for parent in element.parents):
            continue
        for attr in TEXT_ATTRS:
            value = element.get(attr)
            if isinstance(value, str) and has_text(value):
                units.append(Unit(value, lambda text, el=element, a=attr: el.__setitem__(a, text), html=False))
    return units


# Tools whose script output is data that must stay as it is (the NATO alphabet and its digit names are international).
NO_SCRIPT_TRANSLATION = {'nato-phonetic-alphabet-translator'}


def script_units(soup):
    """Translate the messages and labels inside inline <script>s, so tools answer in Spanish too.

    Each script is rewritten once all its strings are applied (a finisher unit, like the JSON-LD one).
    """
    units = []
    canonical = soup.find('link', rel='canonical')
    if canonical and urlparse(canonical['href']).path.rstrip('/').rsplit('/', 1)[-1] in NO_SCRIPT_TRANSLATION:
        return units
    for script in soup.find_all('script'):
        if script.get('src') or script.get('type') in ('application/ld+json', 'importmap') or not script.string:
            continue
        code = script.string
        strings = js_strings.visible_strings(code)
        if not strings:
            continue
        translations = {}
        for piece in strings:
            units.append(Unit(piece, lambda text, k=piece, t=translations: t.__setitem__(k, text), html=False, pattern=SCRIPT_PROTECTED))

        def finish(_text, el=script, source=code, t=translations):
            el.clear()
            el.append(Script(js_strings.rewrite(source, t)))
        finisher = Unit('', finish, html=False)
        finisher.sent = None
        units.append(finisher)
    return units


def head_units(soup):
    units = []
    if soup.title and soup.title.string and has_text(soup.title.string):
        units.append(Unit(soup.title.string, lambda text, t=soup.title: setattr(t, 'string', text), html=False))
    for attr, name in META_TEXT:
        tag = soup.find('meta', attrs={attr: name})
        if tag and tag.get('content') and has_text(tag['content']):
            units.append(Unit(tag['content'], lambda text, t=tag: t.__setitem__('content', text), html=False))
    return units


def jsonld_units(soup, to_es_url):
    """Translate the readable strings in JSON-LD blocks and point their URLs at /es/."""
    units = []
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '')
        except json.JSONDecodeError:
            continue

        def finish(node=data, el=script):
            el.clear()
            el.append(Script(json.dumps(node, ensure_ascii=False)))

        def visit(node, parent_type=None):
            if isinstance(node, list):
                for item in node:
                    visit(item, parent_type)
            elif isinstance(node, dict):
                kind = node.get('@type')
                if kind == 'Organization':
                    return
                for key, value in list(node.items()):
                    if key == '@id':
                        continue
                    if isinstance(value, str):
                        if value.startswith(SITE):
                            node[key] = to_es_url(value)
                        elif key in JSONLD_TEXT_KEYS and has_text(value):
                            units.append(Unit(value, lambda text, n=node, k=key: n.__setitem__(k, text), html=False))
                    else:
                        visit(value, kind)

        visit(data)
        finisher = Unit('', lambda _text, f=finish: f(), html=False)   # writes the JSON back once all strings are applied
        finisher.sent = None
        units.append(finisher)
    return units


# --------------------------------------------------------------------------
# Page building
# --------------------------------------------------------------------------
def url_path(file):
    """URL a source file is served at (global tools are rewritten to /tool/tools/<slug>)."""
    rel = file.relative_to(ROOT).with_suffix('').as_posix().replace('tool/tools/global/', 'tool/tools/')
    if rel == 'index':
        return '/'
    return '/' + (rel[:-len('index')] if rel.endswith('/index') else rel)


def source_pages(wave):
    files = set()
    for number in range(1, wave + 1):
        for pattern in WAVES[number]:
            files.update(f for f in ROOT.glob(pattern) if f.is_file() and f.relative_to(ROOT).parts[0] not in SKIP_DIRS)
    return sorted(files)


def make_link_rewriter(translated_paths):
    def rewrite(href):
        if not href.startswith('/') or href.startswith('//'):
            return href
        parsed = urlparse(href)
        path = parsed.path.removesuffix('.html')
        if path in translated_paths:
            return '/es' + path + (f'?{parsed.query}' if parsed.query else '') + (f'#{parsed.fragment}' if parsed.fragment else '')
        return href
    return rewrite


def rewrite_links(soup, rewrite):
    for tag in soup.find_all('a', href=True):
        tag['href'] = rewrite(tag['href'])
    for tag in soup.find_all('link', rel=True):
        href = tag.get('href', '')
        if href.startswith('/components/'):
            tag['href'] = href.replace('/components/', '/components/es/', 1)


def set_language_tags(soup, en_canonical, es_canonical):
    soup.html['lang'] = 'es'
    for tag in soup.find_all('link', rel='canonical'):
        tag['href'] = es_canonical
    for tag in soup.find_all('meta', property='og:url'):
        tag['content'] = es_canonical
    for tag in soup.find_all('link', hreflang=True):
        tag.decompose()
    canonical = soup.find('link', rel='canonical')
    for lang, href in (('en', en_canonical), ('es', es_canonical), ('x-default', en_canonical)):
        canonical.insert_after(soup.new_tag('link', rel='alternate', hreflang=lang, href=href))
        canonical.insert_after('\n  ')


def add_hreflang_to_english(file, en_canonical, es_canonical):
    """Give the English page the same hreflang cluster (text edit, so the rest of the file is untouched)."""
    text = file.read_text(encoding='utf-8')
    text = re.sub(r'\n?[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', text)
    cluster = ''.join(f'\n  <link rel="alternate" hreflang="{lang}" href="{href}">'
                      for lang, href in (('en', en_canonical), ('es', es_canonical), ('x-default', en_canonical)))
    text, count = re.subn(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + cluster, text, count=1)
    if count:
        file.write_text(text, encoding='utf-8')


def es_url_for(en_url):
    path = urlparse(en_url).path
    return SITE + '/es' + (path if path != '/' else '/')


def build_document(source_text, to_es_url=None, fragment=False):
    soup = BeautifulSoup(source_text, 'html.parser')
    scope = soup if fragment else soup.body
    units = collect_units(soup, scope)
    if not fragment:
        units += head_units(soup) + jsonld_units(soup, to_es_url) + script_units(soup)
    return soup, units


def apply_units(units, cache):
    """Write cached translations into the tree.

    Returns the units that stay in English, as (source text, reason) pairs: no translation yet,
    or a translation whose markup failed validation.
    """
    fallbacks = []
    for unit in units:
        if unit.sent is None:
            unit.apply('')       # JSON-LD finaliser
            continue
        translated = cache.get(unit.sent)
        if translated is None:
            fallbacks.append((unit.source, 'not translated yet'))
            continue
        restored = restore(unit, translated)
        if restored is None:
            fallbacks.append((unit.source, 'markup changed by translator'))
            continue
        unit.apply(restored)
    return fallbacks


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--wave', type=int, choices=sorted(WAVES), required=True)
    parser.add_argument('--engine', choices=['web', 'appsscript', 'fake', 'fake-web'], default='appsscript')
    parser.add_argument('--batch', type=int, default=MAX_BATCH_ITEMS, help='strings per request (smaller is gentler on Apps Script)')
    parser.add_argument('--retry-fallbacks', action='store_true',
                        help='drop cached translations whose markup failed validation so they are translated again')
    args = parser.parse_args()

    if args.engine == 'appsscript':
        url, key = os.environ.get('ES_TRANSLATE_URL'), os.environ.get('ES_TRANSLATE_KEY')
        if not url or not key:
            sys.exit('Set ES_TRANSLATE_URL and ES_TRANSLATE_KEY (see the top of this file).')
        translator = AppsScriptTranslator(url, key)
    else:
        translator = {'web': WebTranslator, 'fake': FakeTranslator, 'fake-web': FakeWebTranslator}[args.engine]()

    is_fake = args.engine.startswith('fake')
    cache = Cache(ROOT / 'scripts' / '.fake_cache.json' if is_fake else CACHE_FILE)
    for source, spanish in GLOSSARY.items():
        cache.put(source, spanish)
    files = source_pages(args.wave)
    translated_paths = {url_path(f) for f in files}
    translated_paths |= {p.rstrip('/') for p in translated_paths if p != '/'}   # /x/ and /x both count
    rewrite = make_link_rewriter(translated_paths)

    # 1. Parse every page, then translate all new strings in one go.
    jobs = []   # (source file, destination file, soup, units, is_fragment)
    for file in files:
        text = file.read_text(encoding='utf-8')
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        if not canonical:
            print(f'skip (no canonical): {file.relative_to(ROOT)}')
            continue
        en_canonical = canonical.group(1)
        to_es = lambda u: es_url_for(u) if urlparse(u).path in translated_paths else u
        soup, units = build_document(text, to_es)
        jobs.append((file, ROOT / 'es' / file.relative_to(ROOT), soup, units, False, en_canonical))

    all_units = [u for *_, units, _f, _c in jobs for u in units if u.sent is not None]
    if args.retry_fallbacks:
        broken = [u for u in all_units if cache.get(u.sent) is not None and restore(u, cache.get(u.sent)) is None]
        for unit in broken:
            cache.discard(unit.sent)
        print(f'{len(broken)} cached translations with broken markup dropped; they will be translated again')
    try:
        translate_missing([u.sent for u in all_units], cache, translator, args.batch)
    except TranslatorStop as stop:
        sys.exit(f'\nStopped: {stop}\nEverything translated so far is saved in {CACHE_FILE.name}. '
                 f'No pages were written this run. Run the same command again later and it continues from here.')

    # 2. Write the Spanish files.
    fallbacks = []
    for source, destination, soup, units, fragment, en_canonical in jobs:
        fallbacks += [(source.relative_to(ROOT).as_posix(), text, why) for text, why in apply_units(units, cache)]
        rewrite_links(soup, rewrite)
        if not fragment:
            es_canonical = es_url_for(en_canonical)
            set_language_tags(soup, en_canonical, es_canonical)
            add_hreflang_to_english(source, en_canonical, es_canonical)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(serialize(soup), encoding='utf-8')
    report = ROOT / 'scripts' / 'es_fallbacks.txt'
    report.write_text(''.join(f'{page}\t{why}\t{" ".join(text.split())[:120]}\n' for page, text, why in fallbacks), encoding='utf-8')
    print(f'wrote {len(jobs)} files; {len(fallbacks)} strings kept in English (list: {report.relative_to(ROOT)})')


if __name__ == '__main__':
    main()
