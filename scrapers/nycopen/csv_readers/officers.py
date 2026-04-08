import argparse
import csv
import json
import logging
from datetime import datetime, date

from models.officers import UpdateOfficer, UpdateEmployment
from scrapers.nycopen.items import AGENCY_LABEL, SOURCE_UID
from scrapers.nycopen.utils import map_ethnicity, map_gender
from scrapers.nycopen.dictionaries.units import UNIT_MAP

# Set up logging
log_path = "_nyc_od_officers.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
)

STATIC_PROPS = {
    "hq_state": "NY",
}


SID_PROPS = {
    "state": "NY",
    "id_name": "Tax ID"
}

def parse_date(s) -> date:
    dt = datetime.strptime(s, "%m/%d/%Y %I:%M:%S %p")
    return dt.date()

def process_csv(csv_filename, output_file):
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                tax_id = row.get("Tax ID", None)
                if tax_id is None or tax_id.strip() == "":
                    logging.warning("Missing Tax ID in row, skipping.")
                    continue
               
                sid = {
                    **SID_PROPS,
                    "value": tax_id.strip(),
                }

                try:
                    officer_data = {
                        "first_name": row.get("Officer First Name", "").strip(),
                        "last_name": row.get("Officer Last Name", "").strip(),
                        "ethnicity": map_ethnicity(row.get("Officer Race", "").strip()),
                        "gender": map_gender(row.get("Officer Gender", "").strip()),
                        "state_ids": [sid],
                    }
                    officer = UpdateOfficer(**officer_data)
                except ValueError as e:
                    logging.warning(
                        f"Validation error for officer {officer_data.get('last_name','')}: {e}"
                    )
                    continue

                try:
                    reported_date = row.get("Last Reported Active Date", None)
                    if reported_date:
                        reported_date = parse_date(reported_date)
                    employment_data = {
                        "badge_number": row.get("Shield No", "").strip(),
                        "highest_rank": row.get("Current Rank", "").strip(),
                        "unit_label": UNIT_MAP.get(row.get("Current Command")),
                        "u_hq_state": "NY",
                        "agency_label": AGENCY_LABEL,
                        "a_hq_state": "NY",
                        "type": "Law Enforcement",
                        "status": "Full-Time",
                    }
                    active = row.get("Active Per Last Reported Status")
                    if active == "No":
                        employment_data["latest_date"] = reported_date.isoformat()
                    else:
                        employment_data["earliest_date"] = reported_date.isoformat()
                    employment = UpdateEmployment(**employment_data)
                except ValueError as e:
                    logging.warning(
                        f"Employment validation error for officer {officer_data.get('last_name','')}: {e}"
                    )
                    continue


                officer_item = {
                    "url": "https://data.cityofnewyork.us/Public-Safety/Civilian-Complaint-Review-Board-Police-Officers/2fir-qns4/about_data",
                    "model": "officer",
                    "data": officer.model_dump(),
                    "employment": [employment.model_dump()],
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_uid": SOURCE_UID,
                }
                logging.info(f"Processed officer {officer_data.get('last_name','')}")
                jsonl_file.write(json.dumps(officer_item) + "\n")


if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process CSV files to JSONL for units."
    )
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument(
        "output", help="Path to the output JSONL file for officers"
    )

    args = parser.parse_args()

    process_csv(csv_filename=args.csv_file, output_file=args.output)
    print(f"Officers saved to {args.output}")