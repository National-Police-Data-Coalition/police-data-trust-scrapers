import argparse
import csv
import json
import re
from datetime import datetime

import requests

from models.enums import Ethnicity

# from scrapers.npi.items import OfficerItem

# Google Places API key
google_api_key = ""


def convert_str_to_date(date_string):
    """
    Convert a string to a date object. Accepts:
    - YYYY-MM-DD
    - Month Year
    - Month Day, Year

    :param date_string: The string to convert

    :return: The date object
    """
    if date_string is None:
        return None

    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_string, "%B %Y").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_string, "%m/%d/%Y").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_string, "%B %d, %Y").date()
    except ValueError:
        return None


def number_to_ordinal(number):
    """Convert an integer to its ordinal representation (e.g., 1 to '1st', 2 to '2nd')."""
    num = int(number)
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")
    return f"{num}{suffix}"


def fix_precinct_with_number(unit_label):
    # Regex to capture a number (with optional leading zeros) followed by the word "precinct"
    pattern = r"(\d+)\s*precinct"
    match = re.search(pattern, unit_label, re.IGNORECASE)

    if match:
        # Extract remove leading zeros, add ordinals to number
        number = match.group(1).lstrip("0") or "0"
        ordinal_number = number_to_ordinal(number)
        updated_unit_label = re.sub(
            r"\b0*" + match.group(1) + r"\b\s*precinct",
            ordinal_number + " precinct",
            unit_label,
            1,
            flags=re.IGNORECASE,
        )

        return updated_unit_label

    return unit_label  # Return the original string if no match is found


def map_ethnicity(ethnicity):
    if not ethnicity:
        return None

    ethnicity_mapping = {
        "black": Ethnicity.BLACK_AFRICAN_AMERICAN.value,
        "white": Ethnicity.WHITE.value,
        "asian": Ethnicity.ASIAN.value,
        "hispanic": Ethnicity.HISPANIC_LATINO.value,
        "native american": Ethnicity.AMERICAN_INDIAN_ALASKA_NATIVE.value,
        "native hawaiian": Ethnicity.NATIVE_HAWAIIAN_PACIFIC_ISLANDER.value,
    }

    for key, value in ethnicity_mapping.items():
        if key in ethnicity.lower():
            return value

    return None


def unit_regex(unit_signifiers=["Pct.", "No.", "Dist. No.", "District #", "Mud #"]):
    """
    Construct a regex pattern to match unit signifiers.
    """
    # Construct the regex pattern dynamically based on the provided unit signifiers
    signifiers_pattern = "|".join(re.escape(signifier) for signifier in unit_signifiers)
    unit_pattern = re.compile(
        rf"(.*?)({signifiers_pattern})\s*(\d+|\w+)$", re.IGNORECASE
    )
    return unit_pattern


def clean_agency_name(agency_name):
    """
    Remove duplicate occurrences of the word "Office" from the agency name.
    Example: "tarrant co. sheriff's office office" -> "tarrant co. sheriff's office"
    """
    # Use regex to replace multiple occurrences of "office" (case-insensitive) with a single "office"
    cleaned_name = re.sub(r"\boffice\b", "office", agency_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(
        r"\boffice\s+office\b", "office", cleaned_name, flags=re.IGNORECASE
    )
    return cleaned_name.strip()


def indentify_unit(agency_label, unit_pattern):
    """
    Identify the unit from the agency label.
    """
    agency_label = clean_agency_name(agency_label)
    match = unit_pattern.match(agency_label)
    if match:
        parent_agency = match.group(1).strip()
        unit_type = match.group(2).strip()
        unit_name = match.group(3).strip()
        full_unit_name = f"{unit_type} {unit_name}"
        return parent_agency, full_unit_name
    return agency_label, None


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

        agency_items.append(
            {
                "url": "https://invisible.institute/national-police-index",
                "model": "agency",
                "data": {
                    "name": agency_name.title(),
                    "hq_state": address_data.get("state", None),
                    "hq_city": address_data.get("city", None),
                    "jurisdiction": None,
                    "phone": phone_number,
                    "email": None,
                    "website_url": website_uri,
                    "address": {
                        "street": f"{address_data.get('street_number', '')} {address_data.get('route', '')}".strip(),
                        "city": address_data.get("city", None),
                        "state": address_data.get("state", None),
                        "postal_code": address_data.get("postal_code", None),
                        "country": address_data.get("country", None),
                    },
                },
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_uid": "NPI",
            }
        )
    for unit in units:
        agency_items.append(
            {
                "url": "https://invisible.institute/national-police-index",
                "model": "unit",
                "data": {
                    "name": unit["unit"].title(),
                    "agency": unit["agency"].title(),
                },
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_uid": "NPI",
            }
        )

    return agency_items


def process_csv(
    csv_filename, officer_output_file, agency_output_file=None, collect_agencies=False
):
    officers_dict = {}
    agencies = []

    unit_pattern = unit_regex()

    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(officer_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                person_nbr = row.get("person_nbr")
                if not person_nbr:
                    continue

                # Handle agency and unit data
                agency_label = row.get("agency_name")
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
                    officer_data = {
                        "url": "https://invisible.institute/national-police-index",
                        "model": "officer",
                        "data": {
                            "first_name": row.get("first_name").title()
                            if row.get("first_name")
                            else None,
                            "middle_name": row.get("middle_initial", "").strip()
                            or None,
                            "last_name": row.get("last_name").title()
                            if row.get("last_name")
                            else None,
                            "suffix": row.get("suffix").upper()
                            if row.get("suffix")
                            else None,
                            "ethnicity": None,
                            "gender": None,  # Gender is not provided in CSV
                            "date_of_birth": row.get("year_of_birth", None),
                            "state_ids": [
                                {
                                    "state": "CA",
                                    "id_name": "NPI ID",
                                    "value": row.get("person_nbr"),
                                }
                            ],
                        },
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_uid": "",
                        "employment": [
                            {
                                "earliest_date": row.get("start_date"),
                                "latest_date": row.get("end_date"),
                                "highest_rank": row.get("rank").title()
                                if row.get("rank")
                                else None,
                                "unit_uid": unit.title() if unit else "Unknown",
                                "agency_uid": agency.title() if agency else None,
                            }
                        ],
                        "service_start": row.get("start_date"),
                    }
                    officers_dict[person_nbr] = officer_data
                else:
                    # Handle multiple employment records
                    employment = {
                        "earliest_date": row.get("start_date"),
                        "latest_date": row.get("end_date"),
                        "highest_rank": row.get("rank").title()
                        if row.get("rank")
                        else None,
                        "unit_uid": unit.title() if unit else "Unknown",
                        "agency_uid": agency.title() if agency else None,
                    }
                    officers_dict[person_nbr]["employment"].append(employment)

                    if row.get("start_date"):
                        start_date = convert_str_to_date(row.get("start_date"))
                        if start_date:
                            if start_date < convert_str_to_date(
                                officers_dict[person_nbr]["service_start"]
                            ):
                                officers_dict[person_nbr]["service_start"] = row.get(
                                    "start_date"
                                )

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
        agency_output_file=args.agency_jsonl,
        collect_agencies=args.collect_agencies,
    )
    print(f"Officers saved to {args.officer_jsonl}")
    if args.collect_agencies:
        print(f"Agencies saved to {args.agency_jsonl}")
