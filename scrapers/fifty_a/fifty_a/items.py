from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem


@dataclass
class CommandItem(BaseItem):
    pass


@dataclass
class OfficerItem(BaseItem):
    employment: List[dict] = None
    service_start: str = None
