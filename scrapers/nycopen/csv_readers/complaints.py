import argparse
import csv
import json
import logging
from datetime import datetime

from models.complaints import CreateComplaint, CreateComplaintSource, CreateLocation
from scrapers.nycopen.items import SOURCE_REL, SOURCE_UID
from scrapers.nycopen.utils import validate_and_return_date_str

# Set up logging
log_path = "_nyc_od_complaints.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
)


def process_csv(csv_filename, complaint_output_file):
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(complaint_output_file, mode="w", encoding="utf-8") as jsonl_file:
            for row in csv_reader:
                record_id = row.get("Complaint Id", None)
                if record_id is None:
                    logging.error("Missing record ID in row, skipping.")
                    continue

                rel_data = SOURCE_REL.copy()
                loc_data = {
                    "location_type": row.get("Location Type Of Incident", None),
                    "city": row.get("Borough Of Incident Occurrence", None),
                    "state": "NY",
                    "administrative_area": row.get(
                        "Precinct Of Incident Occurrence", None
                    ),
                    "administrative_area_type": "precinct",
                }

                try:
                    rel = CreateComplaintSource(**rel_data)
                except ValueError as e:
                    logging.error(
                        f"Validation error for source relation in complaint {record_id}: {e}"
                    )
                    rel = None

                try:
                    loc = CreateLocation(**loc_data)
                except ValueError as e:
                    logging.error(
                        f"Validation error for location in complaint {record_id}: {e}"
                    )
                    loc = None

                complaint_data = {
                    "record_id": record_id,
                    "source_details": rel,
                    "location": loc,
                    "incident_date": validate_and_return_date_str(
                        row.get("Incident Date", None)
                    ),
                    "received_date": validate_and_return_date_str(
                        row.get("Received Date", None)
                    ),
                    "closed_date": validate_and_return_date_str(
                        row.get("Close Date", None)
                    ),
                    "reason_for_contact": row.get("Reason for Police Contact", None),
                    "outcome_of_contact": row.get("Outcome Of Police Encounter", None),
                    # "disposition": row.get("CCRB Complaint Disposition", None),
                }

                try:
                    complaint = CreateComplaint(**complaint_data)
                except ValueError as e:
                    logging.error(f"Validation error for complaint {record_id}: {e}")
                    return None

                complaint_item = {
                    "url": "https://data.cityofnewyork.us/Public-Safety/Civilian-Complaint-Review-Board-Complaints-Against/2mby-ccnw/about_data",
                    "model": "complaint",
                    "data": complaint.model_dump(),
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_uid": SOURCE_UID,
                }
                logging.info(f"Processed complaint {record_id}")
                jsonl_file.write(json.dumps(complaint_item) + "\n")


if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process CSV files to JSONL for officers and agencies."
    )
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument(
        "complaints_jsonl", help="Path to the output JSONL file for complaints"
    )

    args = parser.parse_args()

    process_csv(csv_filename=args.csv_file, complaint_output_file=args.complaints_jsonl)
    print(f"Complaints saved to {args.complaints_jsonl}")
