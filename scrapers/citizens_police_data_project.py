"""Citizens Police Data Project"""

import datetime
import json
import shutil

import requests

from scrapers import config

NOW = datetime.datetime.now(datetime.UTC)
CPDP_DATED_DIR = config.DATA_DIR / "citizens_police_data_project" / str(NOW.date())
OFFICERS_DIR = CPDP_DATED_DIR / "officers"

OFFICERS_URL_TEMPLATE = "https://data.cpdp.co/api/officer-allegations/officers/?&startIdx={start_idx}&length={batch_size}"


def setup() -> None:
    if OFFICERS_DIR.exists():
        shutil.rmtree(OFFICERS_DIR)

    OFFICERS_DIR.mkdir(parents=True, exist_ok=True)


def pull_data():
    batch_size = 5000
    start_idx = 0
    loop = True

    while loop:
        url = OFFICERS_URL_TEMPLATE.format(start_idx=start_idx, batch_size=batch_size)

        print(f"Pulling data from {url}")
        res = requests.get(url, verify=False, timeout=60)  # nosec: B501
        res_data = res.json()

        officers = res_data["officers"]
        file_name = f"officers_{start_idx}.json"
        file_path = OFFICERS_DIR / file_name

        with open(file_path, "w") as f:
            json.dump(officers, f)

        if len(officers) < batch_size:
            loop = False

        start_idx += batch_size


if __name__ == "__main__":
    setup()
    pull_data()
