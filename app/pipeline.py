from app.sources.factory import get_news_source
from app.nlp.gist import extract_best_gist
from app.storage.duckdb import store_articles


def run_pipeline(source_name: str) -> int:
    source = get_news_source(source_name)

    articles = source.fetch()
    if not articles:
        return 0

    for article in articles:
        article["gist"] = extract_best_gist(article["content"])

    store_articles(articles)
    return len(articles)
