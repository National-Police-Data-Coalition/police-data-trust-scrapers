from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem

AGENCY_UID = "54485f3cbe3e49229e3d091f0d12e882"


@dataclass
class CommandItem(BaseItem):
    agency: str = AGENCY_UID
    pass


@dataclass
class OfficerItem(BaseItem):
    employment: List[dict] = None
    service_start: str = None
