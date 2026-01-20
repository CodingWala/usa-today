from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TrumpNewsArticle:
    title: str
    url: str
    matched_on: str
    scraped_at: datetime
