import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

from app.models import NewsHeadline

YAHOO_NEWS_URL = "https://news.yahoo.com/"
TIMEOUT = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

logger = logging.getLogger(__name__)

def fetch_trending_headlines() -> list[NewsHeadline]:
    logger.info("Fetching Yahoo News homepage")

    response = requests.get(
        YAHOO_NEWS_URL,
        headers=HEADERS,
        timeout=TIMEOUT
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    headlines = []
    seen = set()

    for h3 in soup.select("h3 a"):
        title = h3.get_text(strip=True)
        url = h3.get("href")

        if not title or not url or title in seen:
            continue

        if url.startswith("/"):
            url = f"https://news.yahoo.com{url}"

        seen.add(title)

        headlines.append(
            NewsHeadline(
                title=title,
                source="Yahoo News",
                url=url,
                scraped_at=datetime.utcnow()
            )
        )

    logger.info("Fetched %d headlines", len(headlines))
    return headlines
