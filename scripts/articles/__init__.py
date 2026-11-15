"""Article data, one module per topic. `load_articles()` returns every article in publish order."""
import re

from . import ai_technology, startups_business

PUBLISHED = '2026-11-12'
MODIFIED = '2026-11-12'


def reading_minutes(article):
    html = article['intro'] + ''.join(body for _, _, body in article['sections'])
    words = len(re.sub(r'<[^>]+>', ' ', html).split())
    return max(1, round(words / 200))


def load_articles():
    articles = ai_technology.ARTICLES + startups_business.ARTICLES
    for article in articles:
        article['minutes'] = reading_minutes(article)
        article['published'] = PUBLISHED
        article['modified'] = MODIFIED
    return articles
