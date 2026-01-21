
def get_news_source(source: str):
    source = source.lower()

    if source == "yahoo":
        from app.sources.yahoo import YahooNewsSource
        return YahooNewsSource()

    elif source == "newsapi":
        from app.sources.newsapi import NewsAPISource
        return NewsAPISource()

    raise ValueError(f"Unknown NEWS_SOURCE: {source}")


