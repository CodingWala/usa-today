from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TrumpNewsRecord:
    title: str
    url: str
    gist: str
    scraped_at: datetime
