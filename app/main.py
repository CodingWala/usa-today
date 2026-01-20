import logging
import pandas as pd
from pathlib import Path

from app.scraper import crawl_trump_news

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

OUTPUT_DIR = Path("/data")
OUTPUT_FILE = OUTPUT_DIR / "trump_related_yahoo_news.csv"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    articles = crawl_trump_news()

    df = pd.DataFrame([vars(a) for a in articles])
    df.to_csv(OUTPUT_FILE, index=False)

    logging.info("Saved %d Trump-related articles", len(df))

if __name__ == "__main__":
    main()
