# Police Data Trust Scrapers

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Setup](#setup)
- [Run scrapers](#run-scrapers)
  - [50-a](#50-a)
  - [Citizens Police Data Project](#citizens-police-data-project)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Setup
1. Due to the way Scrapy structures projects, we need to add the path to this repo to python path.

    ```bash
    export PYTHONPATH=/path/to/police-data-trust-scrapers/
    ```

2. Create a virtual environment with Python 3.12.2

3. Install requirements

    ```bash
    pip install -r requirements_dev.txt
    ```

## Run scrapers

### 50-a

1. Go to the fifty_a folder

    ```bash
    cd scrapers/fifty_a
    ```

2. Run the office spider

    ```bash
    scrapy crawl officer -O officers.jsonl
    ```

3. Run the command spider

    ```bash
    scrapy crawl command -O commands.jsonl
    ```

### Citizens Police Data Project

This is not a wb scraper. It rather pulls data from their API endpoint.

From the repo root, run the following. It will pull the data and create json files
in the `data/citizens_police_data_project` folder.

```python
python scrapers/citizens_police_data_project.py
```
