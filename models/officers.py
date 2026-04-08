from typing import List, Optional
from datetime import date

from pydantic import BaseModel, Field

from models.enums import Ethnicity, Gender

from .common import Article, Attachment, PaginatedResponse


class StateId(BaseModel):
    state: str = Field(..., description="The state of the state id")
    id_name: str = Field(
        ...,
        description="The name of the id. For example, Tax ID, Driver's License, etc.",
    )
    value: str = Field(..., min_length=1, description="The value of the id.")


class CreateStateId(BaseModel):
    state: str = Field(..., description="The state of the state id")
    id_name: str = Field(
        ...,
        description="The name of the id. For example, Tax ID, Driver's License, etc.",
    )
    value: str = Field(..., min_length=1, description="The value of the id.")


class BaseEmployment(BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(
        None, description="The UID of the agency the officer is employed by."
    )
    unit_uid: Optional[str] = Field(
        None, description="The UID of the unit the officer is assigned to."
    )
    earliest_date: Optional[str] = Field(
        None, description="The earliest known date of employment"
    )
    latest_date: Optional[str] = Field(
        None, description="The latest known date of employment"
    )
    badge_number: Optional[str] = Field(
        None, description="The badge number of the officer"
    )
    highest_rank: Optional[str] = Field(
        None,
        description="The highest rank the officer has held during this employment.",
    )
    rank_label: Optional[str] = Field(
        None,
        description="The original rank label as provided by the source system.",
    )
    commander: Optional[bool] = Field(
        None,
        description="Indicates that the officer commanded the unit during this employment.",
    )
    type: Optional[str] = Field(
        None,
        description="The type of employment. For example, 'Law Enforcement', 'Corrections', etc.",
    )
    employment_change: Optional[bool] = Field(
        None,
        description="Indicates the most recent change in employment status."
        "For example, hired, retired, certified, demoted, promoted.",
    )
    status: Optional[str] = Field(
        None,
        description="The current status of the officer's certification. "
        "For example, 'Active', 'Separated', 'Retired', etc.",
    )


class UpdateEmployment(BaseModel):
    agency_label: str = Field(
        ..., description="The label of the agency the officer is employed by."
    )
    a_hq_state: str = Field(
        ..., description="The state where the agency is headquartered."
    )
    unit_label: str = Field(
        ..., description="The label of the unit the officer is assigned to."
    )
    u_hq_state: str = Field(
        ..., description="The state where the unit is headquartered."
    )
    earliest_date: Optional[date] = Field(
        None, description="The earliest known date of employment"
    )
    latest_date: Optional[date] = Field(
        None, description="The latest known date of employment"
    )
    badge_number: Optional[str] = Field(
        None, description="The badge number of the officer"
    )
    highest_rank: Optional[str] = Field(
        None,
        description="The highest rank the officer has held during this employment.",
    )
    rank_label: Optional[str] = Field(
        None,
        description="The original rank label as provided by the source system.",
    )
    commander: Optional[bool] = Field(
        None,
        description="Indicates that the officer commanded the unit during this employment.",
    )
    type: Optional[str] = Field(
        None,
        description="The type of employment. For example, 'Law Enforcement', 'Corrections', etc.",
    )
    change: Optional[str] = Field(
        None,
        description="Indicates the most recent change in employment status."
        "For example, hired, retired, certified, demoted, promoted.",
    )
    status: Optional[str] = Field(
        None,
        description="The current status of the officer's certification. "
        "For example, 'Active', 'Separated', 'Retired', etc.",
    )
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")


class AddEmploymentFailed(BaseModel):
    agency_uid: Optional[str] = Field(
        None, description="The uid of the agency that could not be added."
    )
    reason: Optional[str] = Field(
        None, description="The reason the employment record could not be added"
    )


class AddEmploymentList(BaseModel):
    agencies: Optional[List[UpdateEmployment]] = Field(
        None, description="The units to add to the officer's employment history."
    )


class Employment(BaseEmployment, BaseModel):
    officer_uid: Optional[str] = Field(None, description="The UID of the officer.")
    agency_uid: Optional[str] = Field(
        None, description="The UID of the agency the officer is employed by."
    )
    unit_uid: Optional[str] = Field(
        None, description="The UID of the unit the officer is assigned to."
    )
    earliest_date: Optional[str] = Field(
        None, description="The earliest known date of employment"
    )
    latest_date: Optional[str] = Field(
        None, description="The latest known date of employment"
    )
    badge_number: Optional[str] = Field(
        None, description="The badge number of the officer"
    )
    highest_rank: Optional[str] = Field(
        None,
        description="The highest rank the officer has held during this employment.",
    )
    rank_label: Optional[str] = Field(
        None,
        description="The original rank label as provided by the source system.",
    )
    commander: Optional[bool] = Field(
        None,
        description="Indicates that the officer commanded the unit during this employment.",
    )
    type: Optional[str] = Field(
        None,
        description="The type of employment. For example, 'Law Enforcement', 'Corrections', etc.",
    )
    change: Optional[str] = Field(
        None,
        description="Indicates the most recent change in employment status."
        "For example, hired, retired, certified, demoted, promoted.",
    )
    status: Optional[str] = Field(
        None,
        description="The current status of the officer's certification. "
        "For example, 'Active', 'Separated', 'Retired', etc.",
    )


class UpdateEmployment(BaseModel):
    agency_label: str = Field(
        ..., description="The label of the agency the officer is employed by."
    )
    a_hq_state: str = Field(
        ..., description="The state where the agency is headquartered."
    )
    unit_label: str = Field(
        ..., description="The label of the unit the officer is assigned to."
    )
    u_hq_state: str = Field(
        ..., description="The state where the unit is headquartered."
    )
    earliest_date: Optional[str] = Field(
        None, description="The earliest known date of employment"
    )
    latest_date: Optional[str] = Field(
        None, description="The latest known date of employment"
    )
    badge_number: Optional[str] = Field(
        None, description="The badge number of the officer"
    )
    highest_rank: Optional[str] = Field(
        None,
        description="The highest rank the officer has held during this employment.",
    )
    rank_label: Optional[str] = Field(
        None,
        description="The original rank label as provided by the source system.",
    )
    type: Optional[str] = Field(
        None,
        description="The type of employment. For example, 'Law Enforcement', 'Corrections', etc.",
    )
    change: Optional[bool] = Field(
        None,
        description="Indicates the most recent change in employment status."
        "For example, hired, retired, certified, demoted, promoted.",
    )
    status: Optional[str] = Field(
        None,
        description="The current status of the officer's certification. "
        "For example, 'Active', 'Separated', 'Retired', etc.",
    )


class AddEmploymentResponse(BaseModel):
    created: List[Employment] = ...
    failed: List[AddEmploymentFailed] = ...
    total_created: int = ...
    total_failed: int = ...


class EmploymentList(PaginatedResponse, BaseModel):
    results: Optional[List[Employment]] = None


class BaseOfficer(BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(
        None, description="The ethnicity of the officer"
    )
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    date_of_birth: Optional[str] = Field(
        None, description="The date of birth of the officer"
    )
    state_ids: Optional[List[StateId]] = Field(
        None, description="The state ids of the officer"
    )


class CreateOfficer(BaseOfficer, BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(
        None, description="The ethnicity of the officer"
    )
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    year_of_birth: Optional[int] = Field(
        None, description="The year of birth of the officer"
    )
    state_ids: Optional[List[StateId]] = Field(
        None, description="The state ids of the officer"
    )
    articles: Optional[List[Article]] = Field(
        None, description="News articles that reference the officer."
    )
    attachments: Optional[List[Attachment]] = Field(
        None, description="Documents and files related to the officer."
    )


class UpdateOfficer(BaseModel):
    first_name: str = Field(..., description="First name of the officer")
    last_name: str = Field(..., description="Last name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(
        None, description="The ethnicity of the officer"
    )
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    year_of_birth: Optional[int] = Field(
        None, description="The year of birth of the officer"
    )
    state_ids: Optional[List[StateId]] = Field(
        None, description="The state ids of the officer"
    )


class Officer(BaseOfficer, BaseModel):
    first_name: Optional[str] = Field(None, description="First name of the officer")
    middle_name: Optional[str] = Field(None, description="Middle name of the officer")
    last_name: Optional[str] = Field(None, description="Last name of the officer")
    suffix: Optional[str] = Field(None, description="Suffix of the officer's name")
    ethnicity: Optional[Ethnicity] = Field(
        None, description="The ethnicity of the officer"
    )
    gender: Optional[Gender] = Field(None, description="The gender of the officer")
    year_of_birth: Optional[int] = Field(
        None, description="The year of birth of the officer"
    )
    state_ids: Optional[List[StateId]] = Field(
        None, description="The state ids of the officer"
    )
    uid: Optional[str] = Field(None, description="The uid of the officer")
    employment_history: Optional[str] = Field(
        None, description="A link to retrieve the employment history of the officer"
    )
    allegations: Optional[str] = Field(
        None, description="A link to retrieve the allegations against the officer"
    )
    litigation: Optional[str] = Field(
        None, description="A link to retrieve the litigation against the officer"
    )


class OfficerList(PaginatedResponse, BaseModel):
    results: Optional[List[Officer]] = None
