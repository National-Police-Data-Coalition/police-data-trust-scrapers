#!/bin/sh
BUCKET_NAME=npdc-scraper-output
printf "running\n"
scrapy crawl officer -O officers.jsonl
scrapy crawl command -O commands.jsonl
aws s3 cp officers.jsonl s3://$BUCKET_NAME/officers/50a/$(date +"%Y-%m-%dT%H-%M-%S").jsonl
aws s3 cp commands.jsonl s3://$BUCKET_NAME/commands/50a/$(date +"%Y-%m-%dT%H-%M-%S").jsonl
