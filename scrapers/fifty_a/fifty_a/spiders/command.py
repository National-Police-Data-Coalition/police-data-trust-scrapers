import re
import random
import logging
import scrapy

from scrapers.fifty_a.fifty_a.items import CommandItem
from models.agencies import CreateUnit


class CommandSpider(scrapy.Spider):
    name = "command"
    allowed_domains = ["www.50-a.org"]
    start_urls = ["https://www.50-a.org/commands"]

    def __init__(self, *args, **kwargs):
        super(CommandSpider, self).__init__(*args, **kwargs)
        self.test_mode = "test_mode" in kwargs
        self.max_units = int(kwargs.get("max_units", 10))

    def parse(self, response):
        commands = response.css("a.command::attr(href)").getall()
        logging.info(f"Found {len(commands)} units.")
        if self.test_mode and commands:
            random.shuffle(commands)
            commands = commands[:self.max_units]
        for command in commands:
            yield response.follow(command, self.parse_command)

    def parse_command(self, response):
        description_set = [desc.strip() for desc in response.css("div.intro p::text").getall() if desc.strip()]
        try:
            desc = description_set[-1]
        except IndexError:
            desc = None
            logging.info(f"Failed to extract description for {response.url}")

        address_data = {}
        address = response.css("div.intro a[href*='google.com']::text").get()
        if address is not None:
            address_data = self.parse_address(address)

        command_data = {k: v for k, v in {
            "name": response.css("h1.title.command::text").get().strip(),  # Extract the unit name from the h1 tag
            "website_url": response.css("div.links a[href*='nypd']::attr(href)").get(),  # Extract the website URL, assuming it contains 'nypd'
            "phone": response.css("div.links p::text").re_first(r"\(\d{3}\) \d{3}-\d{4}"),  # Extract the phone number
            "description": desc,
            "address": address_data.get("street"),
            "city": address_data.get("city"),
            "state": address_data.get("state"),
            "zip": address_data.get("zip_code"),
            "commander_uid": response.css("div.intro a[href*='/officer/']::attr(href)").get(),
        }.items() if v is not None}

        try:
            unit = CreateUnit(**command_data)
            yield unit.model_dump()
        except ValueError as e:
            logging.error(f"Validation error for unit {command_data['name']}: {e}")
            return None

    def parse_address(self, address):
        """Parse the address into its components:
        Street, City, State, Zip
        """
        address_pattern = r"^(.*?),\s*(.*?),\s*([A-Z]{2})\s*(\d{5})$"
        match = re.match(address_pattern, address)
        if match:
            street, city, state, zip_code = match.groups()
            return {
                "street": street,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
        else:
            logging.error(f"Failed to parse address: {address}")
            return None
