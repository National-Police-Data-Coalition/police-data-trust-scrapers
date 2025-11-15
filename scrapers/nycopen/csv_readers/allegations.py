import argparse
import csv
import json
import logging
from datetime import datetime

from models.complaints import CreateAllegation, CreateCivilian
from models.officers import CreateStateId
from scrapers.nycopen.items import SOURCE_UID
from scrapers.nycopen.utils import clean_age_range, map_ethnicity, map_gender

# Set up logging
log_path = "_nyc_od_allegations.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
)


def process_csv(csv_filename, allegations_output_file):
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(allegations_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                record_id = row.get("Allegation Record Identity", None)
                if record_id is None:
                    logging.error("Missing record ID in row, skipping.")
                    continue
                complaint_id = row.get("Complaint Id", None)
                if complaint_id is None:
                    logging.error(
                        f"Missing complaint ID for allegation {record_id}, skipping."
                    )
                    continue

                sid_data = {
                    "state": "NY",
                    "id_name": "Tax ID",
                    "value": row.get("Tax ID", None),
                }

                try:
                    state_id = CreateStateId(**sid_data)
                except ValueError as e:
                    logging.error(
                        f"Validation error for state ID in complaint {record_id}: {e}"
                    )
                    continue

                civ_data = {
                    "age_range": clean_age_range(
                        row.get("Victim/Alleged Victim Age Range At Incident", None)
                    ),
                    "ethnicity": map_ethnicity(
                        row.get("Victim / Alleged Victim Race (Legacy)", None)
                    ),
                    "gender": map_gender(row.get("Victim/Alleged Victim Gender", None)),
                }

                try:
                    civ = CreateCivilian(**civ_data)
                except ValueError as e:
                    logging.error(
                        f"Validation error for civilian in complaint {record_id}: {e}"
                    )
                    civ = None

                allegation_data = {
                    "accused_uid": "state_id",
                    "complainant": civ,
                    "allegation": row.get("Allegation", None),
                    "type": row.get("FADO Type", None),
                    "recommended_finding": row.get(
                        "CCRB Investigations Division Recommendation", None
                    ),
                    "recommended_outcome": row.get("CCRB Allegation Disposition", None),
                    "finding": row.get(
                        "CCRB Investigations Division Recommendation", None
                    ),
                    "outcome": row.get("NYPD Allegation Disposition", None),
                }

                try:
                    allegation = CreateAllegation(**allegation_data)
                except ValueError as e:
                    logging.error(f"Validation error for allegation {record_id}: {e}")
                    return None

                allegation_item = {
                    "url": "https://data.cityofnewyork.us/Public-Safety/Civilian-Complaint-Review-Board-Allegations-Agains/6xgr-kwjq/about_data",
                    "model": "allegation",
                    "data": allegation.model_dump(),
                    "complaint_id": complaint_id,
                    "officer_state_id": state_id.model_dump(),
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_uid": SOURCE_UID,
                }
                logging.info(f"Processed allegation {record_id}")
                jsonl_file.write(json.dumps(allegation_item) + "\n")


if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process CSV files to JSONL for officers and agencies."
    )
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument(
        "allegations_jsonl", help="Path to the output JSONL file for allegations"
    )

    args = parser.parse_args()

    process_csv(
        csv_filename=args.csv_file, allegations_output_file=args.allegations_jsonl
    )
    print(f"Allegations saved to {args.allegations_jsonl}")
