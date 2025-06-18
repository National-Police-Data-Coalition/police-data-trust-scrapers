import argparse
import csv
import json
from datetime import datetime
import logging

import requests

from models.officers import CreateOfficer, StateId, AddEmployment
from models.agencies import CreateAgency, CreateUnit

from scrapers.npi.items import OfficerItem, SOURCE_UID
from scrapers.npi.mapping import SCHEMA_MAP
from scrapers.npi.utils import convert_str_to_date, indentify_unit, unit_regex, map_ethnicity, map_gender, get_int

# Google Places API key
google_api_key = ""

# Set up logging
log_path = "_npi_officers.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path
)


# Function to fetch address components from Google Places API
def get_google_places_data(agency_name):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "X-Goog-FieldMask": "places.displayName,places.addressComponents,places.websiteUri,places.types",
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_api_key,
    }
    payload = {
        "textQuery": agency_name,
        "includedType": "government_office",
        "strictTypeFiltering": True,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        if "places" in data and len(data["places"]) > 0:
            return data["places"][0]  # Return the first result
    return None


def process_agencies(agency_list, unit_pattern, enrich_data=False):
    """
    Identify seperate units within the agency list.
    Return a list of agency and unit items.
    """
    units = []
    updated_agencies = []
    agency_items = []

    for agency in agency_list:
        parent_agency, unit = indentify_unit(agency, unit_pattern)
        if unit:
            units.append({"agency": parent_agency, "unit": unit})
        # Add the parent agency to the updated agency list if not already present
        if parent_agency not in updated_agencies:
            updated_agencies.append(parent_agency)

    for agency_name in updated_agencies:
        if enrich_data:
            google_data = get_google_places_data(agency_name)
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
            "name": agency_name.title(),
            "hq_address": f"{address_data.get('street_number', '')} {address_data.get('route', '')}".strip(),
            "hq_city": address_data.get("city", None),
            "hq_state": address_data.get("state", None),
            "hq_zip": address_data.get("postal_code", None),
            "jurisdiction": None,
            "phone": phone_number,
            "email": None,
            "website_url": website_uri
        }

        try:
            agency = CreateAgency(**agency_data)
        except ValueError as e:
            logging.error(f"Validation error for agency {agency_name}: {e}")
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
        }
        try:
            unit_item = CreateUnit(**unit_data)
        except ValueError as e:
            logging.error(f"Validation error for unit {unit}: {e}")
        agency_items.append(
            {
                "url": "https://invisible.institute/national-police-index",
                "model": "unit",
                "data": unit_item.model_dump(),
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_uid": SOURCE_UID,
                "agency": unit["agency"].title(),
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

def extract_employment(row, employ_schema, unit, agency):
    """
    Extract employment details from the row based on the employment schema.
    Returns a dictionary with employment details.
    """
    data = {
        "earliest_employment": get_field(
            row, employ_schema, "earliest_employment"),
        "latest_employment": get_field(
            row, employ_schema, "latest_employment"),
        "highest_rank": get_field(
            row, employ_schema, "highest_rank", str.title),
        "badge_number": get_field(
            row, employ_schema, "badge_number", str.upper),
        "type": get_field(
            row, employ_schema, "type", str.title),
        "employment_change": get_field(
            row, employ_schema, "employment_change", str.title),
        "status": get_field(
            row, employ_schema, "status", str.title),
        "unit_uid": unit.title() if unit else "Unknown",
        "agency_uid": agency.title() if agency else None,
    }
    try:
        employment = AddEmployment(**data)
    except ValueError as e:
        logging.error(f"Validation error for employment data: {e}")
        return None
    return employment.model_dump()

def process_csv(
    csv_filename, officer_output_file, state, agency_output_file=None, collect_agencies=False
):
    officers_dict = {}
    agencies = []
    schema = SCHEMA_MAP.get(state, SCHEMA_MAP["default"])
    employ_schema = schema.get("employment", {})

    unit_pattern = unit_regex()

    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(officer_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                person_nbr = row.get(schema['state_id']['value'], None)
                if person_nbr is None:
                    logging.error("Missing person number in row, skipping.")
                    continue

                # Handle agency and unit data
                agency_label = get_field(
                    row, employ_schema, "agency_uid", str.lower
                )
                if agency_label:
                    agency_label = agency_label.lower().strip()
                    agency, unit = indentify_unit(agency_label, unit_pattern)
                    if collect_agencies:
                        if agency_label not in agencies:
                            agencies.append(agency_label)
                else:
                    agency = None
                    unit = None

                if person_nbr not in officers_dict:
                    state_id = StateId(
                        state=state, id_name="NPI ID", value=person_nbr
                    )
                    officer_data = {
                        "first_name": get_field(row, schema, "first_name", str.title),
                        "middle_name": get_field(row, schema, "middle_name", str.title),
                        "last_name": get_field(row, schema, "last_name", str.title),
                        "suffix": get_field(row, schema, "suffix", str.upper),
                        "ethnicity": get_field(row, schema, "ethnicity", map_ethnicity),
                        "gender": get_field(row, schema, "gender", map_gender),
                        "year_of_birth": get_field(row, schema, "year_of_birth", get_int),
                        "state_ids": [state_id],
                    }
                    employment = extract_employment(
                        row, employ_schema, unit, agency
                    )
                    if employment:
                        employment_history = [
                            employment
                        ]

                    try:
                        officer = CreateOfficer(**officer_data)
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
                        row, employ_schema, unit, agency
                    )
                    if employment:
                        officers_dict[person_nbr]["employment"].append(employment)

                    try:
                        if row.get("start_date") and officers_dict[person_nbr].get("service_start"):
                            start_date = convert_str_to_date(row.get("start_date"))
                            if start_date and officers_dict[person_nbr].get("service_start"):
                                if start_date < convert_str_to_date(
                                    officers_dict[person_nbr]["service_start"]
                                ):
                                    officers_dict[person_nbr]["service_start"] = row.get(
                                        "start_date"
                                    )
                    except TypeError as e:
                        logging.error(f"Type error for officer {person_nbr}: {e}")

    with open(officer_output_file, mode="w", encoding="utf-8") as jsonl_file:
        for officer in officers_dict.values():
            jsonl_file.write(json.dumps(officer) + "\n")

    if collect_agencies and agency_output_file:
        agency_items = process_agencies(agencies, unit_pattern)
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
        default="TX",
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
