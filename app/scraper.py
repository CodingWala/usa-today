import requests
import logging
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

MAX_TEXT_LENGTH = 10_000


def is_yahoo_news_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("news.yahoo.com")


def extract_article_content(url: str) -> str:
    """
    Fetch full article body from a news URL.
    Source-agnostic: works for Yahoo, NewsAPI links, etc.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        article = soup.find("article")
        paragraphs = article.find_all("p") if article else soup.find_all("p")

        text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        text = re.sub(r"\s+", " ", text)

        return text[:MAX_TEXT_LENGTH]

    except Exception as e:
        logger.warning("Failed to scrape %s: %s", url, e)
        return ""
