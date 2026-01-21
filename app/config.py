import os

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not NEWSAPI_KEY:
    raise RuntimeError(
        "NEWSAPI_KEY not set. Export it before using NEWS_SOURCE=newsapi"
    )
