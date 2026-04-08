import argparse
import csv
import json
import logging
from datetime import datetime

from models.agencies import UpdateUnit
from scrapers.nycopen.items import SOURCE_REL, SOURCE_UID
from scrapers.nycopen.utils import validate_date

# Set up logging
log_path = "_nyc_od_units.log"
log_path = datetime.now().strftime("%Y-%m-%d:%H:%M:%S") + log_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_path,
)

STATIC_PROPS = {
    "hq_state": "NY",
}


def process_csv(csv_filename, unit_output_file, dict_output_file="units_dict.py"):
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(dict_output_file, mode="w", encoding="utf-8") as dictionary_file:
            dictionary_file.write("UNIT_DICT = {\n")
            with open(unit_output_file, mode="w", encoding="utf-8") as jsonl_file:
                for row in csv_reader:
                    name = row.get("Command Name Long", "NA")
                    if name.strip() == "NA":
                        logging.warning("Missing name in row, skipping.")
                        continue
                    short_name = row.get("Command Name Abbreviation", None).strip()
                    if short_name:
                        dictionary_file.write(f'    "{short_name}": "{name}",\n')
                
                    status = row.get("Record Status", None)
                    try:
                        unit_data = {
                            **STATIC_PROPS,
                            "name": name,
                            "status": status,
                        }
                        unit = UpdateUnit(**unit_data)
                    except ValueError as e:
                        logging.error(
                            f"Validation error for unit {name}: {e}"
                        )
                        continue


                    unit_item = {
                        "url": "https://data.cityofnewyork.us/Public-Safety/Civilian-Complaint-Review-Board-Police-Officers/2fir-qns4/about_data",
                        "model": "unit",
                        "data": unit.model_dump(),
                        "agency": "New York City Police Department",
                        "a_hq_state": "NY",
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_uid": SOURCE_UID,
                    }
                    logging.info(f"Processed unit {name}")
                    jsonl_file.write(json.dumps(unit_item) + "\n")
            dictionary_file.write("}\n")


if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process CSV files to JSONL for units."
    )
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument(
        "unit_jsonl", help="Path to the output JSONL file for units"
    )

    args = parser.parse_args()

    process_csv(csv_filename=args.csv_file, unit_output_file=args.unit_jsonl)
    print(f"Units saved to {args.unit_jsonl}")