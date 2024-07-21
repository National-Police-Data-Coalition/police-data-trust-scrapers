from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem

@dataclass
class CommandOfficerItem(BaseItem):
    url: str
    most_recent: int

@dataclass
class CommandItem(BaseItem):
    name: str
    url: str
    website_url: str
    commanding_officer_url: str
    address: str
    description: str
    officers: List[CommandOfficerItem]

@dataclass
class OfficerItem(BaseItem):
    taxnum: int
    url: str
    gender: str
    complaints: List[int]
    age: str
