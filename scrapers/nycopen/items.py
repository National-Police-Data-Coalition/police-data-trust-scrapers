from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem

# National Police Index UID
SOURCE_UID = ""

# NYC Civilian Complaint Review Board Details
SOURCE_REL = {
    "record_type": "government",
    "reporting_agency": "NYC Open Data",
    "reporting_agency_url": "https://opendata.cityofnewyork.us/",
}


@dataclass
class OpenNycItem(BaseItem):
    source_uid: str = SOURCE_UID


@dataclass
class UnitItem(OpenNycItem):
    agency: str = None


@dataclass
class AgencyItem(OpenNycItem):
    pass


@dataclass
class OfficerItem(OpenNycItem):
    employment: List[dict] = None
    service_start: str = None


@dataclass
class ComplaintItem(OpenNycItem):
    pass


@dataclass
class AllegationItem(OpenNycItem):
    pass


@dataclass
class PenaltyItem(OpenNycItem):
    pass
