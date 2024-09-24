#!/bin/sh
BUCKET_NAME=npdc-scraper-output
printf "Running 50A data collection\n"
python fifty_a_download.py --officers-csv-filename=officers.csv
scrapy crawl officer -O officers.jsonl
scrapy crawl command -O commands.jsonl
aws s3 cp officers.csv s3://$BUCKET_NAME/officers/$(date +"%Y-%m-%dT%H-%M-%S")/50a.csv
aws s3 cp officers.jsonl s3://$BUCKET_NAME/officers/$(date +"%Y-%m-%dT%H-%M-%S")/50a.jsonl
aws s3 cp commands.jsonl s3://$BUCKET_NAME/commands/$(date +"%Y-%m-%dT%H-%M-%S")/50a.jsonl
