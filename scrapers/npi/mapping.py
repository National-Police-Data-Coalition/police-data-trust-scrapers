texas = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "year_of_birth",
    "state_id": {
        "value": "person_nbr"
    },
    "employment":{
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type", # Options: Peace Officer, Reserve Officer, Jailer,
        "employment_change": "$special", # Obtained through ever_surrendered and ever_revoked fields
        "extra": [
            "ever_surrendered",
            "ever_revoked"
        ]
    },
    "extra": [
        "county"
    ]
}

california = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_initial", # Sometimes Middle name is available, sometime only middle initial
    "suffix": "suffix",
    "state_id": {
        "value": "person_nbr"
    },
    "employment":{
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type" # Options: CORRECTIONS, POLICE
    }
}

illinois = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "year_of_birth",
    "ethnicity": "race",
    "gender": "sex",
    "state_id": {
        "value": "person_nbr"
    },
    "employment":{
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "rank": "rank",  
        "type": "type", # Options: Law Enforcement, Correctional, Auxiliary
        "employment_change": "separation_reason",
        "status": "status", # Options: part-time, full-time, auxilary
    }
}

washington = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "birth_year",
    "gender": "sex",
    "state_id": {
        "value": "person_nbr"
    },
    "employment":{
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type", 
        # Options: PEACE OFFICER, CERTIFIED PEACE OFFICER, RESERVE OFFICER, NON-CERTIFIED POSITION,
        # CORRECTIONS OFFICER, PRIVATE SECURITY PERSONNEL, CERTIFIED TRIBAL POLICE OFFICER,
        # NON-CERTIFIED RESERVE OFFICER – RECRUIT, PS FIREARMS INSTRUCTOR, CERTIFICATION PENDING - RECRUIT
        "status": "status",  # Indicates if the officer is ACTIVE or SEPARATED
        "employment_change": "employment_status",  
        # Can be Certified, Resignation, Retired, Hire, Terminated, Promotion, or Demotion
        "extra": {
            "event_based": True,
        }
    }
}

arizona = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "state_id": {
        "value": "person_nbr"
    },
    "employment":{
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "status": "current_certificate_status",  # Options: Active, Inactive, Lapsed, Revoked, Relinquished
    }
}

tennessee = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "state_id": {
        "value": "person_nbr"
    },
    "employment":{
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type",  # Examples: Law Enforcement, Corrections, Auxiliary
        "status": "status",  # Options: Active, Separated, Retired, Resigned, Deceased
        "employment_change": "employment_change",  # Indicates the most recent change in employment
        # Examples: Promotion, Hire, Resigned, Portal Update, On Leave, Correction
    }
}

SCHEMA_MAP = {}

SCHEMA_MAP['default'] = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "year_of_birth",
    "state_id": {
        "value": "value",  # Default state ID field
        "type": "type",  # Optional field for state ID type
        "state": "state"
    },
    "employment":{
        "agency_uid": "agency_uid",
        "unit_uid": "unit_uid",
        "earliest_employment": "start_date",
        "latest_employment": "end_date",
        "badge_number": "badge_number",
        "highest_rank": "rank",
        "commander": "commander",
        "type": "type",  # Options: Peace Officer, Reserve Officer, Jailer, etc.
        "employment_change": "employment_change",  # Placeholder for special cases
        "status": "status",  # Options: Active, Inactive, Retired, etc.
    },
    "extra": []
}

SCHEMA_MAP["TX"] = texas
SCHEMA_MAP["CA"] = california
SCHEMA_MAP["IL"] = illinois
SCHEMA_MAP["WA"] = washington
SCHEMA_MAP["AZ"] = arizona
SCHEMA_MAP["TN"] = tennessee