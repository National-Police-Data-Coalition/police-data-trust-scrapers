from dataclasses import dataclass
from datetime import datetime, UTC


@dataclass(kw_only=True)
class BaseItem:
    scraped_at: datetime = datetime.now(UTC)
