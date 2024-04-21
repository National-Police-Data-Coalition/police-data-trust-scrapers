# Police Data Trust Scrapers

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
