import datetime
#!/usr/bin/env python3
"""Build the in-depth article pages from scripts/articles/*.py.

Run from the repository root (after build_hubs.py is not required, but hubs list these articles):

    python3 scripts/build_articles.py

Output: /<topic>/<slug>.html for every article.
"""
from html import escape
from pathlib import Path

from articles import load_articles
from build_hubs import (ROOT, SITE, breadcrumb_html, breadcrumb_schema, icon, ld, page, tool_rows)
from hub_content import TOPICS

TOPIC_BY_SLUG = {t['slug']: t for t in TOPICS}
SUBTOPIC_BY_SLUG = {s['slug']: s for t in TOPICS for s in t['subtopics']}
AUTHOR = {'@type': 'Organization', 'name': "Logrith Team", 'url': f'{SITE}/pages/founder'}


def article_card(article):
    topic = TOPIC_BY_SLUG[article['topic']]
    return f'''    <a href="/{article['topic']}/{article['slug']}" class="article-card">
      <span class="article-card-topic">{escape(topic['title'])}</span>
      <h3>{escape(article['title'])}</h3>
      <p>{escape(article['description'])}</p>
      <span class="article-card-meta">{article['minutes']} min read</span>
    </a>'''


def build_article(article, all_articles):
    topic = TOPIC_BY_SLUG[article['topic']]
    sub = SUBTOPIC_BY_SLUG[article['subtopic']]
    path = f'/{topic["slug"]}/{article["slug"]}'
    trail = [('Home', '/'), (topic['title'], f'/{topic["slug"]}/'), (sub['title'], f'/{topic["slug"]}/{sub["slug"]}'), (article['title'], path)]

    toc = '\n'.join(f'<li><a href="#{anchor}">{escape(heading)}</a></li>' for anchor, heading, _ in article['sections'])
    sections = '\n'.join(f'<section id="{anchor}">\n<h2>{escape(heading)}</h2>\n{body}\n</section>' for anchor, heading, body in article['sections'])
    takeaways = '\n'.join(f'<li>{escape(t)}</li>' for t in article['takeaways'])
    faq = '\n'.join(f'''<details class="faq-item">
  <summary class="faq-q">{escape(q)}</summary>
  <div class="faq-a"><p>{escape(a)}</p></div>
</details>''' for q, a in article['faq'])
    related = [a for a in all_articles if a is not article and a['topic'] == article['topic']][:3]
    related_html = '\n'.join(article_card(a) for a in related)

    body = f'''<header class="page-hero page-hero-article">
  <div class="page-hero-inner">
    {breadcrumb_html(trail)}
    <div class="badge">{icon(sub['icon'])} {escape(sub['title'])}</div>
    <h1>{escape(article['title'])}</h1>
    <p class="byline">By <a href="/pages/founder" rel="author">Logrith Team</a> &middot; Published <time datetime="{article['published']}">{display_date(article['published'])}</time> &middot; Updated <time datetime="{article['modified']}">{display_date(article['modified'])}</time> &middot; {article['minutes']} min read</p>
  </div>
</header>

<article class="page-section">
  <div class="prose hub-prose article-body">
    {article['intro']}

    <aside class="takeaways" aria-label="Key takeaways">
      <h2>Key takeaways</h2>
      <ul class="check-list">
{takeaways}
      </ul>
    </aside>

    <nav class="article-toc" aria-label="In this guide">
      <h2>In this guide</h2>
      <ol>
{toc}
      </ol>
    </nav>

{sections}

    <section id="faq">
      <h2>Frequently asked questions</h2>
      <div class="faq-list">
{faq}
      </div>
    </section>

    <aside class="author-box">
      <strong>Written by <a href="/pages/founder" rel="author">Logrith Team</a></strong>
      <p>Independent founder and publisher of Logrith. Articles are developed with AI assistance, then directed and reviewed by the author. Spotted a mistake? <a href="/pages/contact">Tell us</a> and we will correct it.</p>
    </aside>
  </div>
</article>

<section class="page-section">
  <div class="section-header"><h2>Free tools mentioned in this guide</h2></div>
  <div class="tool-list">
{tool_rows(article['tools'])}
  </div>
</section>

<section class="page-section">
  <div class="section-header"><h2>More in {escape(topic['title'])}</h2></div>
  <div class="article-list">
{related_html}
  </div>
</section>'''

    schemas = [
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': article['title'], 'description': article['description'],
         'url': f'{SITE}{path}', 'mainEntityOfPage': {'@type': 'WebPage', '@id': f'{SITE}{path}'},
         'datePublished': article['published'], 'dateModified': article['modified'], 'author': AUTHOR,
         'publisher': {'@id': f'{SITE}/#organization'}, 'isPartOf': {'@id': f'{SITE}/#website'}, 'inLanguage': 'en'},
        breadcrumb_schema(trail),
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in article['faq']]},
    ]
    html = page(f'{article["title"]} | Logrith', article['description'], path, schemas, body)
    return html.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">', 1)


def display_date(iso):
    """2026-11-20 -> Nov 20, 2026"""
    day = datetime.date.fromisoformat(iso)
    return f'{day:%b} {day.day}, {day.year}'


def main():
    articles = load_articles()
    for article in articles:
        for slug in article['tools']:
            from build_hubs import TOOLS
            assert slug in TOOLS, f'{article["slug"]}: unknown tool {slug}'
        target = ROOT / article['topic'] / f'{article["slug"]}.html'
        target.write_text(build_article(article, articles))
    print(f'wrote {len(articles)} articles')


if __name__ == '__main__':
    main()
