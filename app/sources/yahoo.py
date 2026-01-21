import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.sources.base import NewsSource

SEARCH_URL = "https://news.search.yahoo.com/search"
KEYWORDS = ["donald trump", "trump"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}


class YahooNewsSource(NewsSource):
    def fetch(self) -> list[dict]:
        return self.fetch_article_links(pages=20)

    def fetch_article_links(self, pages: int = 20) -> list[dict]:
        results = []

        for page in range(1, pages + 1):
            params = {
                "p": "Donald Trump",
                "b": (page - 1) * 10 + 1
            }

            resp = requests.get(
                SEARCH_URL,
                params=params,
                headers=HEADERS,
                timeout=10
            )
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "lxml")
            articles = soup.select("div.NewsArticle")

            for a in articles:
                title_tag = a.select_one("h4 a")
                summary_tag = a.select_one("p")

                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                url = title_tag["href"]

                if not any(k in title.lower() for k in KEYWORDS):
                    continue

                results.append({
                    "url": url,
                    "title": title,
                    "content": summary_tag.get_text(strip=True) if summary_tag else "" or title,
                    "summary": summary_tag.get_text(strip=True) if summary_tag else "",
                    "source": "yahoo",
                    "fetched_at": datetime.utcnow()
                })

        return results
