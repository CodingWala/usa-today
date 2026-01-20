import logging
import pandas as pd
from pathlib import Path
from app.storage import init_db
from app.scraper import crawl_trump_news

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

OUTPUT_DIR = Path("/data")
OUTPUT_FILE = OUTPUT_DIR / "trump_related_yahoo_news.csv"


def main():
    init_db()
    records = crawl_trump_news()
    # OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # df = pd.DataFrame([vars(a) for a in records])
    # df.to_csv(OUTPUT_FILE, index=False)
    logging.info("Stored %d Trump-related articles", records)

if __name__ == "__main__":
    main()
