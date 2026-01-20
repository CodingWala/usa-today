import time
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

from app.models import TrumpNewsArticle

BASE_URL = "https://news.yahoo.com"
MAX_URLS = 300
CRAWL_DEPTH = 2
REQUEST_DELAY = 1  # seconds

TRUMP_KEYWORDS = [
    "donald trump",
    "president trump",
    "former president trump",
    "trump administration",
    "trump campaign"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; YahooNewsCrawler/1.0)"
}

logger = logging.getLogger(__name__)

def is_yahoo_news_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("news.yahoo.com")


def contains_trump_keyword(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in TRUMP_KEYWORDS)

def crawl_trump_news() -> list[TrumpNewsArticle]:
    visited: set[str] = set()
    queue = [(BASE_URL, 0)]
    results: list[TrumpNewsArticle] = []

    while queue and len(visited) < MAX_URLS:
        current_url, depth = queue.pop(0)

        if current_url in visited or depth > CRAWL_DEPTH:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except Exception as e:
            logger.warning("Failed to fetch %s: %s", current_url, e)
            continue

        soup = BeautifulSoup(response.text, "lxml")

        page_text = soup.get_text(" ", strip=True)

        if contains_trump_keyword(page_text):
            title = soup.title.get_text(strip=True) if soup.title else "No Title"

            results.append(
                TrumpNewsArticle(
                    title=title,
                    url=current_url,
                    matched_on="keyword",
                    scraped_at=datetime.utcnow()
                )
            )

        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(BASE_URL, href)

            if (
                is_yahoo_news_url(full_url)
                and full_url not in visited
            ):
                queue.append((full_url, depth + 1))

        time.sleep(REQUEST_DELAY)

    logger.info("Trump-related articles found: %d", len(results))
    return results

