from dataclasses import dataclass
from typing import List

from scrapers.common.base_item import BaseItem

# NYC Open Data UID
SOURCE_UID = ""

# NYPD UID
AGENCY_UID = ""

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
    from models.officers import StateId

    complaint_id: str = None
    officer_state_id: dict = None
    officer_rank: str = None
    officer_command: str = None
    officer_days_on_duty: int = None


@dataclass
class PenaltyItem(OpenNycItem):
    from models.officers import StateId

    complaint_id: str = None
    officer_state_id: dict = None
