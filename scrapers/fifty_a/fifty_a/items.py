from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem

# NYPD UID
AGENCY_UID = "a3530d6adc2a4bc2beb436b62d346881"

# 50-a.org UID
SOURCE_UID = "e583f54ecc1b435daf6c614c5abc05c1"

# NYC Civilian Complaint Review Board Details
SOURCE_REL = {
    "record_type": "government",
    "reporting_agency": "New York City Civilian Complaint Review Board",
    "reporting_agency_url": "https://www.nyc.gov/site/ccrb/index.page",
}


@dataclass
class FiftyAItem(BaseItem):
    source_uid: str = SOURCE_UID


@dataclass
class ComplaintItem(FiftyAItem):
    pass


@dataclass
class CommandItem(FiftyAItem):
    agency: str = AGENCY_UID
    pass


@dataclass
class OfficerItem(FiftyAItem):
    employment: List[dict] = None
    service_start: str = None
