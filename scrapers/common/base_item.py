from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(kw_only=True)
class BaseItem:
    url: str
    model: str
    data: dict
    scraped_at: datetime = datetime.now(UTC)
    source: str = "Fifty-A.org"
