from models.enums import Rank

TX_OFFICER_RANK_MAP = {
    "Peace Officer": Rank.POLICE_OFFICER.value,
    "Jailer": Rank.POLICE_OFFICER.value,
    "Reserve Officer": Rank.POLICE_OFFICER.value,
    "Contract Jailer": Rank.POLICE_OFFICER.value,
    "Chief Of Police": Rank.CHIEF.value,
    "Special Ranger (Txdps)": Rank.DETECTIVE.value,
    "Supervision Officer": Rank.SERGEANT.value,
    "Sheriff": Rank.CHIEF.value,
    "Po (Ret State Employee)": Rank.POLICE_OFFICER.value,
    "Special Game Warden": Rank.DETECTIVE.value,
    "City Marshal": Rank.CHIEF.value,
    "Public Security Officer": Rank.POLICE_OFFICER.value,
    "Fire Marshal": Rank.CHIEF.value,
    "Special Inspector (Tabc)": Rank.MAJOR.value,
    "Constable": Rank.CHIEF.value,
    "Special Ranger (Tsc)": Rank.DETECTIVE.value,
    "Special Agent": Rank.DETECTIVE.value,
    "Special Ranger (Nic)": Rank.DETECTIVE.value,
    "Chief Law Enforcement Officer": Rank.CHIEF.value,
    "Jail Inspector": Rank.MAJOR.value,
    "Redacted - Peace Officer": Rank.POLICE_OFFICER.value,
    "Homeowner Insurance Inspector": Rank.MAJOR.value,
    "Redacted - Jailer": Rank.POLICE_OFFICER.value,
}

IL_OFFICER_RANK_MAP = {
    "Police Officer": Rank.POLICE_OFFICER.value,
    "Correctional Officer": Rank.POLICE_OFFICER.value,
    "Deputy": Rank.POLICE_OFFICER.value,
    "Sergeant": Rank.SERGEANT.value,
    "Auxiliary Officer": Rank.POLICE_OFFICER.value,
    "Chief": Rank.CHIEF.value,
    "Lieutenant": Rank.LIEUTENANT.value,
    "Court Security Officer": Rank.POLICE_OFFICER.value,
    "Investigator": Rank.DETECTIVE.value,
    "Deputy Chief": Rank.COMMANDER.value,
    "Deputy Coroner": Rank.LIEUTENANT.value,
    "Commander": Rank.COMMANDER.value,
    "Detective": Rank.DETECTIVE.value,
    "Auxiliary Deputy": Rank.POLICE_OFFICER.value,
    "Captain": Rank.CAPTAIN.value,
    "Special Agent": Rank.DETECTIVE.value,
    "Corporal": Rank.SERGEANT.value,
    "Trooper First Class": Rank.POLICE_OFFICER.value,
    "Assistant States Attorney": Rank.MAJOR.value,
    "Telecommunicator": Rank.NON_SWORN.value,
    "Sheriff": Rank.CHIEF.value,
    "Reserve Officer": Rank.POLICE_OFFICER.value,
    "Probation Officer": Rank.POLICE_OFFICER.value,
    "Chief Deputy": Rank.COMMANDER.value,
    "Trooper": Rank.POLICE_OFFICER.value,
    "States Attorney": Rank.CHIEF.value,
    "Assistant Chief": Rank.COMMANDER.value,
    "Master Sergeant": Rank.SERGEANT.value,
    "Coroner": Rank.CHIEF.value,
    "Master Trooper": Rank.SERGEANT.value,
    "Director": Rank.COMMANDER.value,
    "Deputy Marshal": Rank.LIEUTENANT.value,
    "Ranger": Rank.POLICE_OFFICER.value,
    "Cadet": Rank.POLICE_OFFICER.value,
    "Security Officer": Rank.NON_SWORN.value,
    "Inspector": Rank.MAJOR.value,
    "Jail Administrator": Rank.COMMANDER.value,
    "Acting Chief": Rank.CHIEF.value,
    "Public Safety Officer": Rank.POLICE_OFFICER.value,
    "Intern": Rank.NON_SWORN.value,
    "Marshal": Rank.CHIEF.value,
    "Administrator": Rank.COMMANDER.value,
    "Bailiff": Rank.NON_SWORN.value,
    "Senior Master Trooper": Rank.SERGEANT.value,
    "Circuit Clerk": Rank.MAJOR.value,
    "Jailer": Rank.POLICE_OFFICER.value,
    "Mayor": Rank.CHIEF.value,
    "Senior Agent": Rank.DETECTIVE.value,
    "Chief Deputy Coroner": Rank.COMMANDER.value,
    "Process Server": Rank.NON_SWORN.value,
    "Major": Rank.MAJOR.value,
    "Supervisor": Rank.SERGEANT.value,
    "Under Sheriff": Rank.COMMANDER.value,
    "Superintendent": Rank.COLONEL.value,
    "Staff": Rank.NON_SWORN.value,
    "Youth Officer": Rank.POLICE_OFFICER.value,
    "Deputy Jail Administrator": Rank.LIEUTENANT.value,
    "P. F. C.": Rank.POLICE_OFFICER.value,
    "Commissioner": Rank.CHIEF.value,
    "Senior Inspector": Rank.MAJOR.value,
    "Watch Commander": Rank.COMMANDER.value,
    "Conservator Of The Peace": Rank.POLICE_OFFICER.value,
    "Chief Investigator": Rank.COMMANDER.value,
    "Arson Investigator": Rank.DETECTIVE.value,
    "Deputy Director": Rank.CAPTAIN.value,
    "Special Agent In Charge": Rank.COMMANDER.value,
    "Assistant Director": Rank.CAPTAIN.value,
    "Division Commander": Rank.COMMANDER.value,
    "Village President": Rank.CHIEF.value,
    "Colonel": Rank.COLONEL.value,
    "Chief Correctional Officer": Rank.CHIEF.value,
    "Lieutenant Colonel": Rank.COLONEL.value,
    "Officer In Charge": Rank.COMMANDER.value,
    "Deputy Superintendent": Rank.CAPTAIN.value,
    "Chief Auxillary": Rank.CHIEF.value,
    "Supervising Special Agent": Rank.COMMANDER.value,
    "Communications Officer": Rank.POLICE_OFFICER.value,
    "Corrections Parole Agent (State)": Rank.DETECTIVE.value,
    "Inspector General": Rank.COLONEL.value,
    "Deputy Commander": Rank.CAPTAIN.value,
    "Assistant Warden": Rank.CAPTAIN.value,
    "Senior Investigator": Rank.DETECTIVE.value,
    "Unspecified": Rank.NON_SWORN.value,
    "Lieutenant Commander": Rank.COMMANDER.value,
    "Warden": Rank.CHIEF.value,
    "Chief Bailiff": Rank.CHIEF.value,
    "Chief Assistant States Attorney": Rank.COMMANDER.value,
    "Assistant Coroner": Rank.CAPTAIN.value,
    "Chief Marshal": Rank.CHIEF.value,
    "Assistant Superintendent": Rank.CAPTAIN.value,
    "Assistant Deputy Chief": Rank.CAPTAIN.value,
    "First Sergeant": Rank.SERGEANT.value,
    "Chief Court Security Officer": Rank.CHIEF.value,
    "Assistant Commander": Rank.CAPTAIN.value,
}


texas = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "year_of_birth",
    "state_id": {"value": "person_nbr"},
    "employment": {
        "earliest_date": "start_date",
        "latest_date": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type",  # Options: Peace Officer, Reserve Officer, Jailer,
        "employment_change": "$special",  # Obtained through ever_surrendered and ever_revoked fields
        "extra": ["ever_surrendered", "ever_revoked"],
    },
    "extra": ["county"],
}

california = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_initial",  # Sometimes Middle name is available, sometime only middle initial
    "suffix": "suffix",
    "state_id": {"value": "person_nbr"},
    "employment": {
        "earliest_date": "start_date",
        "latest_date": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type",  # Options: CORRECTIONS, POLICE
    },
}

illinois = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "year_of_birth",
    "ethnicity": "race",
    "gender": "sex",
    "state_id": {"value": "person_nbr"},
    "employment": {
        "earliest_date": "start_date",
        "latest_date": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "rank": "rank",
        "type": "type",  # Options: Law Enforcement, Correctional, Auxiliary
        "employment_change": "separation_reason",
        "status": "status",  # Options: part-time, full-time, auxilary
    },
}

washington = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "birth_year",
    "gender": "sex",
    "state_id": {"value": "person_nbr"},
    "employment": {
        "earliest_date": "start_date",
        "latest_date": "end_date",
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
        },
    },
}

arizona = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "state_id": {"value": "person_nbr"},
    "employment": {
        "earliest_date": "start_date",
        "latest_date": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "status": "current_certificate_status",  # Options: Active, Inactive, Lapsed, Revoked, Relinquished
    },
}

tennessee = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "state_id": {"value": "person_nbr"},
    "employment": {
        "earliest_date": "start_date",
        "latest_date": "end_date",
        "highest_rank": "rank",
        "agency_uid": "agency_name",
        "type": "type",  # Examples: Law Enforcement, Corrections, Auxiliary
        "status": "status",  # Options: Active, Separated, Retired, Resigned, Deceased
        "employment_change": "employment_change",  # Indicates the most recent change in employment
        # Examples: Promotion, Hire, Resigned, Portal Update, On Leave, Correction
    },
}

SCHEMA_MAP = {}

SCHEMA_MAP["default"] = {
    "first_name": "first_name",
    "last_name": "last_name",
    "middle_name": "middle_name",
    "suffix": "suffix",
    "year_of_birth": "year_of_birth",
    "state_id": {
        "value": "value",  # Default state ID field
        "type": "type",  # Optional field for state ID type
        "state": "state",
    },
    "employment": {
        "agency_uid": "agency_uid",
        "unit_uid": "unit_uid",
        "earliest_date": "start_date",
        "latest_date": "end_date",
        "badge_number": "badge_number",
        "highest_rank": "rank",
        "commander": "commander",
        "type": "type",  # Options: Peace Officer, Reserve Officer, Jailer, etc.
        "employment_change": "employment_change",  # Placeholder for special cases
        "status": "status",  # Options: Active, Inactive, Retired, etc.
    },
    "extra": [],
}

SCHEMA_MAP["TX"] = texas
SCHEMA_MAP["CA"] = california
SCHEMA_MAP["IL"] = illinois
SCHEMA_MAP["WA"] = washington
SCHEMA_MAP["AZ"] = arizona
SCHEMA_MAP["TN"] = tennessee
