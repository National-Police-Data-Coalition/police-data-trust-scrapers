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
from scrapers.npi.utils import classify_jurisdiction

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def update_jurisdiction(input_filename, output_filename):
    """
    Update the jurisdiction field in the input data based on the name
    of the agency.
    """
    output_data = []

    with open(input_filename, mode="r", encoding="utf-8") as jsonl_file:
        for line in jsonl_file:
            item = json.loads(line)
            if item.get("model") == "agency":
                agency_name = item["data"].get("name", "").lower()
                jurisdiction = classify_jurisdiction(agency_name)
                item["data"]["jurisdiction"] = jurisdiction
                output_data.append(item)
            else:
                output_data.append(item)

    with open(output_filename, mode="w", encoding="utf-8") as jsonl_file:
        for item in output_data:
            jsonl_file.write(json.dumps(item) + "\n")
        logging.info(f"Updated jurisdiction for {len(output_data)} agencies.")
        print(f"Output saved to {output_filename}")
        

if __name__ == "__main__":
    # Set up argument parser
    # Usage: python officers.py path_to_input.csv path_to_output.jsonl
    parser = argparse.ArgumentParser(
        description="Process JSONL files for agencies."
    )
    parser.add_argument("input", help="Path to the input file.")
    parser.add_argument(
        "output", help="Path to the output JSONL file."
    )

    args = parser.parse_args()

    update_jurisdiction(
        input_filename=args.input,
        output_filename=args.output
    )
