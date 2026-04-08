import argparse
import csv
import json
import logging
from datetime import datetime

from models.complaints import CreatePenalty
from models.officers import CreateStateId
from scrapers.nycopen.items import SOURCE_UID
from scrapers.nycopen.utils import validate_date

# Set up logging
log_path = "_nyc_od_penalty.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
)


def get_penalty_date(row):
    """
    Extract and validate the penalty date from the row.
    :param row: The CSV row as a dictionary.
    """
    is_apu_case = row.get("Officer is_APU", "no").strip().lower() == "yes"
    if is_apu_case:
        return validate_date(row.get("APU Closing Date", None))
    else:
        return validate_date(row.get("Non-APU NYPD Penalty Report Date", None))


def process_csv(csv_filename, penalty_output_file):
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(penalty_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                complaint_id = row.get("Complaint Id", None)
                if complaint_id is None:
                    logging.error("Missing complaint ID for penalty. Skipping.")
                    continue

                sid_data = {
                    "state": "NY",
                    "id_name": "Tax ID",
                    "value": row.get("Tax ID", None),
                }

                try:
                    state_id = CreateStateId(**sid_data)
                except ValueError:
                    logging.error(
                        f"Invalid Officer Tax ID for penalty in complaint {complaint_id}. Skipping."
                    )
                    continue

                penalty_data = {
                    "officer_uid": "state_id",
                    "crb_plea": row.get("APU Plea Agreed Penalty", None),
                    "crb_case_status": row.get("APU Case Status", None),
                    "crb_disposition": row.get("Board Discipline Recommendation", None),
                    "penalty": row.get("NYPD Officer Penalty", None),
                    "date_assessed": get_penalty_date(row),
                }

                try:
                    penalty = CreatePenalty(**penalty_data)
                except ValueError as e:
                    logging.error(
                        f"Validation error for penalty in complaint {complaint_id}: {e}"
                    )
                    return None

                penalty_item = {
                    "url": "https://data.cityofnewyork.us/Public-Safety/Civilian-Complaint-Review-Board-Penalties/keep-pkmh/about_data",
                    "model": "penalty",
                    "data": penalty.model_dump(),
                    "complaint_id": complaint_id,
                    "officer_state_id": state_id.model_dump(),
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_uid": SOURCE_UID,
                }
                logging.info(f"Processed penalty in complaint {complaint_id}")
                jsonl_file.write(json.dumps(penalty_item) + "\n")


if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process CSV files to JSONL for officers and agencies."
    )
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument(
        "penalties_jsonl", help="Path to the output JSONL file for penalties"
    )

    args = parser.parse_args()

    process_csv(csv_filename=args.csv_file, penalty_output_file=args.penalties_jsonl)
    print(f"Penalties saved to {args.penalties_jsonl}")
