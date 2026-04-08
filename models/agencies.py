from typing import List, Optional

from pydantic import BaseModel, Field

from .common import PaginatedResponse



class UpdateAgency(BaseModel):
    name: str = Field(..., description="Name of the agency")
    hq_state: str = Field(..., description="State of the agency")
    hq_address: Optional[str] = Field(None, description="Address of the agency")
    hq_city: Optional[str] = Field(None, description="City of the agency")
    hq_zip: Optional[str] = Field(None, description="Zip code of the agency")
    phone: Optional[str] = Field(None, description="Phone number of the agency")
    email: Optional[str] = Field(None, description="Email of the agency")
    website_url: Optional[str] = Field(None, description="Website of the agency")
    description: Optional[str] = Field(None, description="Description of the agency")
    date_established: Optional[str] = Field(
        None, description="The date that this agency was established."
    )
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction of the agency")


class UpdateUnit(BaseModel):
    name: str = Field(..., description="Name of the unit")
    hq_state: str = Field(..., description="State where the unit is headquartered.")
    hq_address: Optional[str] = Field(None, description="Street address where the unit is headquartered.")
    hq_city: Optional[str] = Field(None, description="City where the unit is headquartered.")
    hq_zip: Optional[str] = Field(None, description="Zip code where the unit is headquartered.")
    phone: Optional[str] = Field(None, description="Phone number of the unit")
    email: Optional[str] = Field(None, description="Email of the unit")
    website_url: Optional[str] = Field(None, description="Website of the unit")
    description: Optional[str] = Field(None, description="Description of the unit")
    status: Optional[str] = Field(None, description="Opertional status of the unit")
    date_established: Optional[str] = Field(
        None,
        description="The date that this unit was established by its parent agency.",
    )
    commander_uid: Optional[str] = Field(
        None, description="The UID of the unit's current commander."
    )


class AddOfficer(BaseModel):
    officer_uid: str = Field(..., description="The uid of the officer")
    earliest_date: Optional[str] = Field(
        None, description="The earliest date of employment"
    )
    latest_date: Optional[str] = Field(
        None, description="The latest date of employment"
    )
    badge_number: str = Field(..., description="The badge number of the officer")
    unit_uid: str = Field(
        ..., description="The UID of the unit the officer is assigned to."
    )
    highest_rank: Optional[str] = Field(
        None,
        description="The highest rank the officer has held during their employment.",
    )
    commander: Optional[bool] = Field(
        None,
        description="-| If true, this officer will be added as the commander of the unit for the specified time period.",
    )


class AddOfficerList(BaseModel):
    officers: List[AddOfficer] = ...


class AddOfficerFailed(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The uid of the officer")
    reason: Optional[str] = Field(
        None, description="The reason the employment record could not be added"
    )
