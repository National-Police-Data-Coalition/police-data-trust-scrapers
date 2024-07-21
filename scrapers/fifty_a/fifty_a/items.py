from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem


@dataclass
class CommandItem(BaseItem):
    name: str
    url: str


@dataclass
class OfficerItem(BaseItem):
    taxnum: int
    url: str
    gender: str
    complaints: List[dict]
    age: str
