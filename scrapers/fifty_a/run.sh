#!/bin/sh
BUCKET_NAME=npdc-scraper-output
printf "running\n"
scrapy crawl officer -O officers.jsonl
scrapy crawl command -O commands.jsonl
aws s3 cp officers.jsonl s3://$BUCKET_NAME/officers/$(date +"%Y-%m-%dT%H-%M-%S")/50a.jsonl
aws s3 cp commands.jsonl s3://$BUCKET_NAME/commands/$(date +"%Y-%m-%dT%H-%M-%S")/50a.jsonl
cd ../
python scrapers/citizens_police_data_project.py
aws s3 cp ../data/citizens_police_data_project/$(date +"%Y-%m-%d")/officers/*.json s3://$BUCKET_NAME/officers/$(date +"%Y-%m-%dT%H-%M-%S")/cpdp/