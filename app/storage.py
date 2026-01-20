from pathlib import Path
import duckdb
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "news.duckdb"


def init_db():
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS trump_news (
                url TEXT PRIMARY KEY,
                title TEXT,
                summary TEXT,
                gist TEXT,
                content TEXT,
                scraped_at TIMESTAMP,
                partition_date DATE
            )
            """
        )


def store_articles(articles):
    if not articles:
        logger.info("No articles to store")
        return 0

    inserted = 0

    with duckdb.connect(str(DB_PATH)) as con:
        for a in articles:
            try:
                con.execute(
                    """
                    INSERT INTO trump_news
                    (url, title, summary, gist, content, scraped_at, partition_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (url) DO NOTHING

                    """,
                    (
                        (
                            a["url"],
                            a["title"],
                            a["summary"],
                            a["gist"],
                            a["content"],
                            a["scraped_at"],
                            a["partition_date"],
                        )

                    ),
                )
                inserted += 1
            except Exception as e:
                logger.warning(f"Failed to insert {a.get('url')}: {e}")

    logger.info(f"Stored {inserted} Trump-related articles")
    return inserted
