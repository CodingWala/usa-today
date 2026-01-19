import logging
import pandas as pd
from pathlib import Path

from app.scraper import fetch_trending_headlines

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

OUTPUT_DIR = Path("/data")
OUTPUT_FILE = OUTPUT_DIR / "yahoo_trending_news.csv"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    headlines = fetch_trending_headlines()

    df = pd.DataFrame([vars(h) for h in headlines])
    df.to_csv(OUTPUT_FILE, index=False)

    logging.info("Saved headlines to %s", OUTPUT_FILE)

if __name__ == "__main__":
    main()
