import requests
from datetime import datetime
from app.sources.base import NewsSource
from app.config import NEWSAPI_KEY

class NewsAPISource(NewsSource):

    URL = "https://newsapi.org/v2/everything"

    def fetch(self):
        params = {
            "q": "Donald Trump",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 50,
            "apiKey": NEWSAPI_KEY,
        }

        r = requests.get(self.URL, params=params, timeout=10)
        r.raise_for_status()

        articles = []
        for a in r.json().get("articles", []):
            articles.append({
                "url": a["url"],
                "title": a["title"],
                "content": a.get("content") or a.get("description") or "",
                "published_at": a["publishedAt"],
            })

        return articles
