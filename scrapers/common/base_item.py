from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(kw_only=True)
class BaseItem:
    scraped_at: datetime = datetime.now(UTC)
