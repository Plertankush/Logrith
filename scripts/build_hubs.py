#!/usr/bin/env python3
"""Build the Logrith home page and the topic / sub-topic hub pages.

Source data lives in scripts/hub_content.py. Run from the repository root:

    python3 scripts/build_hubs.py

Output (all static HTML, overwritten on every run):
    index.html                         home
    <topic>/index.html                 one per top-level topic
    <topic>/<subtopic>.html            one per sub-topic
"""
import json
from html import escape
from pathlib import Path

from hub_content import SITE, TOPICS

ROOT = Path(__file__).resolve().parent.parent
TOOLS = {t['url'].rsplit('/', 1)[-1]: t for t in json.loads((ROOT / 'assets/data/tools.json').read_text())}
FEATURED_TOOLS = ['image-compressor', 'pdf-merge', 'json-formatter', 'password-generator', 'emi-calculator', 'word-counter']


def icon(name, cls='icon icon-inline'):
    return f'<svg class="{cls}" aria-hidden="true"><use href="/assets/svg/icons.svg#{name}"></use></svg>'


def head(title, description, path, schema):
    url = f'{SITE}{path}'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="author" content="Plert Ankush">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{escape(title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Logrith">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title, quote=True)}">
  <meta name="twitter:description" content="{escape(description, quote=True)}">
  <link rel="icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#0A0A0A">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Source+Serif+4:wght@600;700;800&display=swap">
  <link rel="stylesheet" href="/assets/css/style.css">
  <link rel="stylesheet" href="/assets/css/pages.css">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-BPJ4332XJH"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-BPJ4332XJH');
  </script>
{schema}
</head>
'''


def ld(data):
    return '  <script type="application/ld+json">\n  ' + json.dumps(data, ensure_ascii=False, indent=2).replace('\n', '\n  ') + '\n  </script>'


def breadcrumb_schema(trail):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'name': name, 'item': f'{SITE}{path}'}
            for i, (name, path) in enumerate(trail, 1)
        ],
    }


def breadcrumb_html(trail):
    parts = [f'<a href="{path}">{escape(name)}</a>' for name, path in trail[:-1]]
    parts.append(escape(trail[-1][0]))
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + ' › '.join(parts) + '</nav>'


def page(title, description, path, schemas, body):
    return (head(title, description, path, '\n'.join(ld(s) for s in schemas)) + f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<div id="navbar"></div>

<main id="main">
{body}
</main>

<div id="footer"></div>
<script src="/assets/js/main.js"></script>
</body>
</html>
''')


def tool_rows(slugs):
    rows = []
    for slug in slugs:
        tool = TOOLS[slug]
        rows.append(f'''    <a href="{tool['url']}" class="tool-row">
      <span class="tool-row-icon">{icon('tool', 'icon')}</span>
      <div class="tool-row-body"><div class="tool-row-name">{escape(tool['name'])}</div><div class="tool-row-desc">{escape(tool['summary'])}</div></div>
      <span class="tool-row-arrow" aria-hidden="true">{icon('arrow-right')}</span>
    </a>''')
    return '\n'.join(rows)


def sub_links(topic):
    return '\n'.join(
        f'<li><a href="/{topic["slug"]}/{sub["slug"]}">{icon(sub["icon"])}<span>{escape(sub["title"])}</span></a></li>'
        for sub in topic['subtopics'])


# ---------------------------------------------------------------- sub-topic
def build_subtopic(topic, sub):
    path = f'/{topic["slug"]}/{sub["slug"]}'
    trail = [('Home', '/'), (topic['title'], f'/{topic["slug"]}/'), (sub['title'], path)]
    siblings = [s for s in topic['subtopics'] if s is not sub]
    intro = '\n'.join(f'<p>{escape(p)}</p>' for p in sub['intro'])
    topics = '\n'.join(f'<li>{escape(t)}</li>' for t in sub['topics'])
    concepts = '\n'.join(f'<div class="concept"><h3>{escape(term)}</h3><p>{escape(text)}</p></div>' for term, text in sub['concepts'])
    more = '\n'.join(
        f'<a href="/{topic["slug"]}/{s["slug"]}" class="related-link">{icon(s["icon"])}<span>{escape(s["title"])}</span></a>' for s in siblings)
    body = f'''<header class="page-hero">
  <div class="page-hero-inner">
    {breadcrumb_html(trail)}
    <div class="badge">{icon(sub['icon'])} {escape(topic['title'])}</div>
    <h1>{escape(sub['title'])}</h1>
    <p>{escape(sub['summary'])}</p>
    <p class="byline">By <a href="/pages/founder" rel="author">Plert Ankush</a></p>
  </div>
</header>

<section class="page-section">
  <div class="prose hub-prose">
    <h2>Overview</h2>
    {intro}

    <h2>What this section covers</h2>
    <ul class="check-list">
{topics}
    </ul>

    <h2>Core concepts</h2>
    <div class="concept-grid">
{concepts}
    </div>

    <h2>Where to start</h2>
    <p>{escape(sub['start'])}</p>
  </div>
</section>

<section class="page-section">
  <div class="section-header"><h2>Free tools for this topic</h2><p>Browser-based, no sign-up, and your files stay on your device.</p></div>
  <div class="tool-list">
{tool_rows(sub['tools'])}
  </div>
</section>

<section class="page-section">
  <div class="section-header"><h2>More in {escape(topic['title'])}</h2></div>
  <div class="related-links">
{more}
  </div>
</section>'''
    schemas = [
        {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': sub['title'], 'url': f'{SITE}{path}',
         'description': sub['summary'], 'author': {'@type': 'Person', 'name': 'Plert Ankush', 'url': f'{SITE}/pages/founder'},
         'isPartOf': {'@id': f'{SITE}/#website'}},
        breadcrumb_schema(trail),
    ]
    return path, page(f'{sub["title"]} Guides and Tools | Logrith', sub['summary'], path, schemas, body)


# -------------------------------------------------------------------- topic
def build_topic(topic):
    path = f'/{topic["slug"]}/'
    trail = [('Home', '/'), (topic['title'], path)]
    intro = '\n'.join(f'<p>{escape(p)}</p>' for p in topic['intro'])
    cards = '\n'.join(f'''    <a href="/{topic['slug']}/{sub['slug']}" class="topic-card">
      <span class="topic-card-icon">{icon(sub['icon'], 'icon')}</span>
      <h3>{escape(sub['title'])}</h3>
      <p>{escape(sub['summary'])}</p>
      <span class="topic-card-more">Explore {icon('arrow-right')}</span>
    </a>''' for sub in topic['subtopics'])
    tool_slugs = list(dict.fromkeys(slug for sub in topic['subtopics'] for slug in sub['tools'][:2]))
    body = f'''<header class="page-hero">
  <div class="page-hero-inner">
    {breadcrumb_html(trail)}
    <div class="badge">{icon(topic['icon'])} Topic</div>
    <h1>{escape(topic['title'])}</h1>
    <p>{escape(topic['tagline'])}</p>
  </div>
</header>

<section class="page-section">
  <div class="prose hub-prose">
    <h2>About this section</h2>
    {intro}
  </div>
</section>

<section class="page-section">
  <div class="section-header"><h2>Explore {escape(topic['title'])}</h2><p>Three areas, each with core ideas, the questions we cover and related free tools.</p></div>
  <div class="topic-grid">
{cards}
  </div>
</section>

<section class="page-section">
  <div class="section-header"><h2>Useful free tools</h2><p>Hand-picked from the Logrith tools library.</p></div>
  <div class="tool-list">
{tool_rows(tool_slugs)}
  </div>
</section>'''
    schemas = [
        {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': topic['title'], 'url': f'{SITE}{path}',
         'description': topic['meta'], 'isPartOf': {'@id': f'{SITE}/#website'}},
        breadcrumb_schema(trail),
    ]
    return path, page(f'{topic["title"]}: Guides, Explainers and Tools | Logrith', topic['meta'], path, schemas, body)


# --------------------------------------------------------------------- home
HOME_FAQ = [
    ('What is Logrith?', 'Logrith is an independent publication about technology, startups and digital business, with a library of free browser-based tools alongside the writing.'),
    ('Are the tools really free?', 'Yes. Every tool is free, needs no account and runs in your browser. The site is supported by advertising.'),
    ('Do my files get uploaded?', 'The image, PDF and text tools process files inside your browser, so documents stay on your device. Each tool page explains how that tool handles data.'),
    ('Who writes Logrith?', 'Logrith is built and published by Plert Ankush, an independent founder. You can read more on the founder page.'),
]


def build_home():
    description = 'Logrith is an independent publication on technology, startups and digital business, with free browser-based tools for everyday work.'
    cards = '\n'.join(f'''    <article class="topic-card topic-card-lg">
      <span class="topic-card-icon">{icon(t['icon'], 'icon')}</span>
      <h3><a href="/{t['slug']}/">{escape(t['title'])}</a></h3>
      <p>{escape(t['tagline'])}</p>
      <ul class="sub-links">
{sub_links(t)}
      </ul>
    </article>''' for t in TOPICS)
    principles = [
        ('file-text', 'Plain language', 'Every guide explains the idea first and the jargon second, so you can act on it the same day.'),
        ('check-circle', 'Practical first', 'Frameworks, worked examples and calculators you can use, not predictions or hype.'),
        ('lock', 'Private by default', 'The tools run in your browser. We do not ask you to sign up or upload your files.'),
    ]
    principle_html = '\n'.join(f'''    <div class="feature-card">
      <div class="feature-icon">{icon(i, 'icon')}</div>
      <h3>{t}</h3>
      <p>{d}</p>
    </div>''' for i, t, d in principles)
    faq = '\n'.join(f'''  <details class="faq-item">
    <summary class="faq-q">{escape(q)}</summary>
    <div class="faq-a"><p>{escape(a)}</p></div>
  </details>''' for q, a in HOME_FAQ)
    body = f'''<header class="page-hero home-hero">
  <div class="page-hero-inner">
    <div class="badge">{icon('globe')} Technology, startups and digital business</div>
    <h1>Clear thinking on technology, startups and <span>growth</span>.</h1>
    <p>Practical guides for people who build things online, plus a library of free tools that run right in your browser.</p>
    <div class="btn-group">
      <a href="#topics" class="btn btn-primary btn-lg">Explore topics</a>
      <a href="/tool/" class="btn btn-secondary btn-lg">Browse free tools</a>
    </div>
  </div>
</header>

<section class="page-section" id="topics">
  <div class="section-header"><h2>Three topics, nine areas</h2><p>Start with the subject you are working on today.</p></div>
  <div class="topic-grid topic-grid-3">
{cards}
  </div>
</section>

<section class="page-section">
  <div class="section-header"><h2>How Logrith works</h2></div>
  <div class="feature-grid">
{principle_html}
  </div>
</section>

<section class="page-section">
  <div class="section-header">
    <h2>Free tools, always available</h2>
    <p>Compress an image, merge a PDF, format JSON or run a loan calculation without creating an account.</p>
  </div>
  <div class="tool-list">
{tool_rows(FEATURED_TOOLS)}
  </div>
  <p class="section-more"><a href="/tool/" class="btn btn-secondary">View all {len(TOOLS)} tools {icon('arrow-right')}</a></p>
</section>

<section class="page-section">
  <div class="section-header"><h2>Questions</h2></div>
  <div class="faq-list">
{faq}
  </div>
</section>'''
    schemas = [
        {'@context': 'https://schema.org', '@type': 'WebSite', '@id': f'{SITE}/#website', 'name': 'Logrith', 'url': f'{SITE}/',
         'description': description, 'publisher': {'@id': f'{SITE}/#organization'}},
        {'@context': 'https://schema.org', '@type': 'Organization', '@id': f'{SITE}/#organization', 'name': 'Logrith',
         'url': f'{SITE}/', 'logo': f'{SITE}/apple-touch-icon.png',
         'founder': {'@type': 'Person', 'name': 'Plert Ankush', 'url': f'{SITE}/pages/founder'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in HOME_FAQ]},
    ]
    return '/', page('Logrith: Technology, Startups & Digital Business', description, '/', schemas, body)


def main():
    outputs = [build_home()]
    for topic in TOPICS:
        outputs.append(build_topic(topic))
        outputs.extend(build_subtopic(topic, sub) for sub in topic['subtopics'])
    for slug in {s for t in TOPICS for sub in t['subtopics'] for s in sub['tools']}:
        assert slug in TOOLS, f'unknown tool slug: {slug}'
    for path, html in outputs:
        target = ROOT / (path.strip('/') + '/index.html' if path.endswith('/') else path.strip('/') + '.html')
        if path == '/':
            target = ROOT / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html)
    print(f'wrote {len(outputs)} pages')


if __name__ == '__main__':
    main()
