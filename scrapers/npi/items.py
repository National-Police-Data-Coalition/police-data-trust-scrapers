from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem

# National Police Index UID
SOURCE_UID = "d4254e0c94034e77be95e1b8dc7bb661"

# NYC Civilian Complaint Review Board Details
SOURCE_REL = {
    "record_type": "news",
    "publication_name": "National Police Index",
    "publication_url": "https://invisible.institute/national-police-index",
}


@dataclass
class NpiItem(BaseItem):
    source_uid: str = SOURCE_UID


@dataclass
class UnitItem(NpiItem):
    agency: str = None


@dataclass
class AgencyItem(NpiItem):
    pass


@dataclass
class OfficerItem(NpiItem):
    employment: List[dict] = None
    service_start: str = None
