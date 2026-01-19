from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class NewsHeadline:
    title: str
    source: str
    url: str
    scraped_at: datetime
