import argparse

import requests

OFFICER_CSV_URL = "https://www.50-a.org/data/nypd/officers.csv"


def download_officer_csv(officer_csv_filename: str):
    response = requests.get(OFFICER_CSV_URL)
    with open(officer_csv_filename, "wb") as officers_csv:
        officers_csv.write(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="50A File Downloader")
    parser.add_argument("--officers-csv-filename", default="officers.csv")

    args = parser.parse_args()

    download_officer_csv(args.officers_csv_filename)
