import argparse
import csv
import json
import logging
from datetime import datetime

import requests

from models.agencies import UpdateAgency, UpdateUnit
from models.enums import State
from models.officers import UpdateEmployment, UpdateOfficer, StateId
from models.dicts import STATE_INFO
from scrapers.npi.items import SOURCE_UID
from scrapers.npi.mapping import SCHEMA_MAP, IL_OFFICER_RANK_MAP, TX_OFFICER_RANK_MAP
from scrapers.npi.utils import (
    convert_str_to_date,
    get_int,
    indentify_unit,
    map_ethnicity,
    map_gender,
    unit_regex,
)

# Google Places API key
google_api_key = ""

# Set up logging
log_path = "_npi_officers.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
)


# Resolve state
def resolve_agency_hq_state(state, county, agency):
    if state == "TX":
        if county and county.lower() == "other state than texas":
            logging.info(f"County indicates out-of-state agency: {agency} in {county}")
            if agency and agency.lower().startswith("state of"):
                ref = agency.lower().split("state of")[-1].strip()
                logging.info(f"Extracted state reference from agency name: '{ref}'")
                if ref in STATE_INFO:
                    res = STATE_INFO[ref]["abbrv"]
                else:
                    res = None
            else:
                res = None
        else:
            res = state
    else:
        res = state
    return res


# Select the proper place based on the sate and county
def select_place(places, *, state, county):
    for place in places:
        if "addressComponents" in place:
            address_components = place["addressComponents"]
            for component in address_components:
                if "administrative_area_level_1" in component["types"]:
                    if component["shortText"].lower() == state.lower():
                        if county:
                            for comp in address_components:
                                if "administrative_area_level_2" in comp["types"]:
                                    if comp["shortText"].lower() == county.lower():
                                        return place
                        else:
                            return place


# Function to fetch address components from Google Places API
def get_google_places_data(agency_name, *, google_state=None, google_county=None):
    logging.debug(
        f"Get_places called with state={google_state!r}, county={google_county!r}"
    )
    query = agency_name
    if google_state or google_county:
        query += " in "
    if google_county:
        query += f"{google_county} county, "
    if google_state:
        query += f"{google_state}"
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "X-Goog-FieldMask": "places.displayName,places.addressComponents,places.websiteUri,places.types",
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_api_key,
    }
    payload = {
        "textQuery": query,
        "includedType": "government_office",
        "strictTypeFiltering": True,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if "places" in data and len(data["places"]) > 0:
            # Log the full set of results for debugging
            logging.debug(
                f"Google Places API results for '{query}':\n{json.dumps(data['places'])}"
            )
            return data["places"][0]  # Return the first result
    return None


def process_agencies(agency_set, state, enrich_data=True):
    """
    Identify seperate units within the agency list.
    Return a list of agency and unit items.
    """
    units = []
    updated_agencies = []
    agency_items = []

    for agency in agency_set.values():
        parent_agency = agency.get("agency", None)
        unit = agency.get("unit", None)
        county = agency.get("county", None)
        if unit:
            units.append({"agency": parent_agency, "unit": unit})
        # Add the parent agency to the updated agency list if not already present
        if parent_agency not in updated_agencies:
            updated_agencies.append({"agency": parent_agency, "county": county})

    for distict_agency in updated_agencies:
        name = distict_agency.get("agency", None)
        county = distict_agency.get("county", None)
        if enrich_data:
            if name.lower() != "Other-Out-Of-State".lower():
                logging.debug(f"Enriching data. County: {county}, State: {state}")
                if county == "Other State Than Texas":
                    google_data = get_google_places_data(
                        name, google_state=None, google_county=None
                    )
                else:
                    google_data = get_google_places_data(
                        name, google_state=state, google_county=county
                    )
            else:
                logging.debug(f"Skipping enrichment for agency: {name}")
                google_data = None
        else:
            google_data = None
        address_components = (
            google_data.get("addressComponents", []) if google_data else []
        )
        website_uri = google_data.get("websiteUri", None) if google_data else None
        phone_number = (
            google_data.get("nationalPhoneNumber", None) if google_data else None
        )

        # Extract relevant address components
        address_data = {}
        for component in address_components:
            if "street_number" in component["types"]:
                address_data["street_number"] = component["longText"]
            elif "route" in component["types"]:
                address_data["route"] = component["longText"]
            elif "locality" in component["types"]:
                address_data["city"] = component["longText"]
            elif "administrative_area_level_1" in component["types"]:
                address_data["state"] = component["shortText"]
            elif "postal_code" in component["types"]:
                address_data["postal_code"] = component["longText"]
            elif "country" in component["types"]:
                address_data["country"] = component["longText"]

        agency_data = {
            "name": name.title(),
            "hq_address": f"{address_data.get('street_number', '')} {address_data.get('route', '')}".strip(),
            "hq_city": address_data.get("city", None),
            "hq_state": address_data.get("state", None),
            "hq_zip": address_data.get("postal_code", None),
            "jurisdiction": None,
            "phone": phone_number,
            "email": None,
            "website_url": website_uri,
        }

        try:
            agency = UpdateAgency(**agency_data)
        except ValueError as e:
            logging.error(f"Validation error for agency {name}: {e}")
            continue

        agency_items.append(
            {
                "url": "https://invisible.institute/national-police-index",
                "model": "agency",
                "data": agency.model_dump(),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_uid": SOURCE_UID,
            }
        )
    for unit in units:
        unit_data = {
            "name": unit["unit"].title(),
            "hq_state": state
        }
        try:
            unit_item = UpdateUnit(**unit_data)
        except ValueError as e:
            logging.error(f"Validation error for unit {unit}: {e}")
        agency_items.append(
            {
                "url": "https://invisible.institute/national-police-index",
                "model": "unit",
                "data": unit_item.model_dump(),
                "agency": unit["agency"].title(),
                "a_hq_state": state,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_uid": SOURCE_UID,
            }
        )

    return agency_items


def get_field(row, schema, field_name, transform=lambda x: x):
    """
    Get a field from the row based on the schema.
    If the field is not present, return None.
    """
    col = schema.get(field_name, field_name)
    val = row.get(col)
    return transform(val) if val else None


def get_rank_values(row, employ_schema, state):
    """
    Return normalized highest_rank and the source-system rank label.
    """
    rank_label = get_field(row, employ_schema, "highest_rank", str.strip)
    if not rank_label:
        return None, None

    rank_map = None
    if state == "TX":
        rank_map = TX_OFFICER_RANK_MAP
    elif state == "IL":
        rank_map = IL_OFFICER_RANK_MAP

    if rank_map:
        highest_rank = rank_map.get(rank_label)
        if highest_rank:
            return highest_rank, rank_label

    return rank_label.title(), rank_label


def extract_employment(row, employ_schema, unit, agency, hq_state, state):
    """
    Extract employment details from the row based on the employment schema.
    Returns a dictionary with employment details.
    """
    highest_rank, rank_label = get_rank_values(row, employ_schema, state)
    data = {
        "earliest_date": get_field(row, employ_schema, "earliest_date"),
        "latest_date": get_field(row, employ_schema, "latest_date"),
        "highest_rank": highest_rank,
        "rank_label": rank_label,
        "badge_number": get_field(row, employ_schema, "badge_number", str.upper),
        "type": get_field(row, employ_schema, "type", str.title),
        "change": get_field(
            row, employ_schema, "employment_change", str.title
        ),
        "status": get_field(row, employ_schema, "status", str.title),
        "unit_label": unit.title() if unit else "Unknown",
        "u_hq_state": hq_state,
        "agency_label": agency.title() if agency else "Unknown",
        "a_hq_state": hq_state,
    }
    try:
        employment = UpdateEmployment(**data)
    except ValueError as e:
        logging.error(f"Validation error for employment data: {e}")
        return None
    return employment.model_dump()


def process_csv(
    csv_filename,
    officer_output_file,
    state,
    agency_output_file=None,
    collect_agencies=False,
):
    state = state.value if isinstance(state, State) else state
    officers_dict = {}
    agencies_dict = {}
    schema = SCHEMA_MAP.get(state, SCHEMA_MAP["default"])
    employ_schema = schema.get("employment", {})

    unit_pattern = unit_regex()

    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(officer_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                person_nbr = row.get(schema["state_id"]["value"], None)
                if person_nbr is None:
                    logging.error("Missing person number in row, skipping.")
                    continue

                # Handle agency and unit data
                hq_state = state
                agency_label = get_field(row, employ_schema, "agency_uid", str.lower)
                if agency_label:
                    agency_label = agency_label.strip()
                    agency, unit = indentify_unit(agency_label, unit_pattern)
                    # Get the county if it is given
                    county = row.get("county", None)
                    # TODO: Handle hq_state
                    if collect_agencies:
                        if agency_label not in agencies_dict:
                            agencies_dict[agency_label] = {
                                "agency": agency,
                                "unit": unit,
                                "county": county,
                            }
                    elif state == State.TX.value:
                        hq_state = resolve_agency_hq_state(state, county, agency)
                        if hq_state != state:
                            agency = "Unknown"
                            unit = "Unknown"
                else:
                    agency = "Unknown"
                    unit = "Unknown"
                    hq_state = state

                if person_nbr not in officers_dict:
                    employment_history = []
                    state_id = StateId(state=state, id_name="NPI ID", value=person_nbr)
                    officer_data = {
                        "first_name": get_field(row, schema, "first_name", str.title),
                        "middle_name": get_field(row, schema, "middle_name", str.title),
                        "last_name": get_field(row, schema, "last_name", str.title),
                        "suffix": get_field(row, schema, "suffix", str.upper),
                        "ethnicity": get_field(row, schema, "ethnicity", map_ethnicity),
                        "gender": get_field(row, schema, "gender", map_gender),
                        "year_of_birth": get_field(
                            row, schema, "year_of_birth", get_int
                        ),
                        "state_ids": [state_id],
                    }
                    employment = extract_employment(
                        row, employ_schema, unit, agency, hq_state, state
                    )
                    if employment:
                        employment_history.append(employment)
                    try:
                        officer = UpdateOfficer(**officer_data)
                    except ValueError as e:
                        logging.error(f"Validation error for officer {person_nbr}: {e}")
                        return None

                    officer_item = {
                        "url": "https://invisible.institute/national-police-index",
                        "model": "officer",
                        "data": officer.model_dump(),
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_uid": SOURCE_UID,
                        "employment": employment_history,
                        "service_start": row.get("start_date"),
                    }
                    officers_dict[person_nbr] = officer_item
                else:
                    # Handle multiple employment records
                    employment = extract_employment(
                        row, employ_schema, unit, agency, hq_state, state
                    )
                    if employment:
                        officers_dict[person_nbr]["employment"].append(employment)

                    try:
                        if row.get("start_date") and officers_dict[person_nbr].get(
                            "service_start"
                        ):
                            start_date = convert_str_to_date(row.get("start_date"))
                            if start_date and officers_dict[person_nbr].get(
                                "service_start"
                            ):
                                if start_date < convert_str_to_date(
                                    officers_dict[person_nbr]["service_start"]
                                ):
                                    officers_dict[person_nbr]["service_start"] = (
                                        row.get("start_date")
                                    )
                    except TypeError as e:
                        logging.error(f"Type error for officer {person_nbr}: {e}")

    with open(officer_output_file, mode="w", encoding="utf-8") as jsonl_file:
        for officer in officers_dict.values():
            jsonl_file.write(json.dumps(officer) + "\n")

    if collect_agencies and agency_output_file:
        agency_items = process_agencies(agencies_dict, state)
        with open(agency_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for item in agency_items:
                jsonl_file.write(json.dumps(item) + "\n")


if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process CSV files to JSONL for officers and agencies."
    )
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument(
        "officer_jsonl", help="Path to the output JSONL file for officers"
    )
    parser.add_argument(
        "--state",
        type=State,
        choices=list(State),
        default=State.TX,
        help="State code for the officers (default: TX)",
    )
    parser.add_argument(
        "--agency-jsonl",
        help="Path to the output JSONL file for agencies",
        default=None,
    )
    parser.add_argument(
        "--collect-agencies",
        action="store_true",
        help="Enable collection of agency data",
    )

    args = parser.parse_args()

    process_csv(
        csv_filename=args.csv_file,
        officer_output_file=args.officer_jsonl,
        state=args.state,
        agency_output_file=args.agency_jsonl,
        collect_agencies=args.collect_agencies,
    )
    print(f"Officers saved to {args.officer_jsonl}")
    if args.collect_agencies:
        print(f"Agencies saved to {args.agency_jsonl}")
