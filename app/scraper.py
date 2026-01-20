import time
import requests
import logging
import re
import nltk
from nltk.tokenize import sent_tokenize
from collections import Counter

import nltk
from nltk.tokenize import sent_tokenize
import os

NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

nltk.data.path.append(NLTK_DATA_DIR)

nltk.download("punkt", download_dir=NLTK_DATA_DIR, quiet=True)
nltk.download("punkt_tab", download_dir=NLTK_DATA_DIR, quiet=True)
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

from app.models import TrumpNewsRecord
from app.gist import extract_best_gist
from datetime import datetime, date
from app.storage import store_articles

SEARCH_URL = "https://news.search.yahoo.com/search"
KEYWORDS = ["trump", "donald trump", "donald j. trump"]

logger = logging.getLogger(__name__)


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
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

logger = logging.getLogger(__name__)

def is_yahoo_news_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.endswith("news.yahoo.com")

def contains_trump_keyword(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in TRUMP_KEYWORDS)

def extract_article_text(soup: BeautifulSoup) -> str:
    article = soup.find("article")
    if not article:
        return ""

    paragraphs = article.find_all("p")
    return " ".join(p.get_text(" ", strip=True) for p in paragraphs)

def crawl_trump_news(pages: int = 20):
    articles_collected = []

    for page in range(1, pages + 1):
        params = {
            "p": "Donald Trump",
            "b": (page - 1) * 10 + 1
        }

        response = requests.get(SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        results = soup.select("div.NewsArticle")

        for r in results:
            title_tag = r.select_one("h4 a")
            summary_tag = r.select_one("p")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            url = title_tag["href"]
            summary = summary_tag.get_text(strip=True) if summary_tag else ""

            if not any(k in title.lower() for k in KEYWORDS):
                continue
            content = extract_article_content(url)
            gist = generate_gist(content)

            articles_collected.append({
                "url": url,
                "title": title,
                "summary": summary,
                "content": content,
                "gist": gist,
                "scraped_at": datetime.utcnow(),
                "partition_date": date.today()
            })

    store_articles(articles_collected)
    return len(articles_collected)

def extract_article_content(url: str) -> str:
    try:
        r = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "lxml")

        article = soup.find("article")
        if not article:
            paragraphs = soup.find_all("p")
        else:
            paragraphs = article.find_all("p")

        text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        text = re.sub(r"\s+", " ", text)

        return text[:10000]  # safety cap

    except Exception:
        return ""

def generate_gist(text: str) -> str:
    sentences = sent_tokenize(text)
    if not sentences:
        return ""

    words = text.lower().split()
    freq = Counter(words)

    scored = []
    for s in sentences[:10]:
        score = sum(freq[w.lower()] for w in s.split() if w.isalpha())
        scored.append((score, s))

    scored.sort(reverse=True)
    return scored[0][1]
