import logging
import random
import re
from datetime import UTC, datetime

import scrapy

from models.complaints import (
    Civilian,
    CreateAllegation,
    CreateComplaint,
    CreatePenalty,
    Location,
)
from scrapers.fifty_a.fifty_a.items import SOURCE_REL, ComplaintItem
from scrapers.fifty_a.fifty_a.utils import convert_str_to_date, get_demographics


class ComplaintSpider(scrapy.Spider):
    name = "complaint"
    allowed_domains = ["www.50-a.org"]
    start_urls = [
        "https://www.50-a.org/recent/added",
        "https://www.50-a.org/recent/updated",
    ]

    def __init__(self, *args, **kwargs):
        super(ComplaintSpider, self).__init__(*args, **kwargs)
        self.test_mode = "test_mode" in kwargs
        self.max_units = int(kwargs.get("max_units", 10))

    def parse(self, response):
        complaints = response.css('a[href^="/complaint/"]::attr(href)').getall()
        logging.info(f"Found {len(complaints)} complaints.")
        if not complaints:
            logging.error("No complaints found.")
        if self.test_mode and complaints:
            random.shuffle(complaints)  # nosec
            complaints = complaints[: self.max_units]
        for complaint in complaints:
            yield response.follow(complaint, self.parse_complaint)

    def parse_complaint(self, response):
        # Extract the record_id from the title
        title_text = response.css("h1.title::text").get()
        match = re.search(r"Complaint #(\d+)", title_text)
        if match:
            record_id = match.group(1)
        else:
            record_id = None

        # Extract details from the 'div.details' section
        details_section = response.css("div.details")
        attachments = self.parse_attachments(details_section)
        details_lines = details_section.xpath(".//text()").getall()
        details_lines = [line.strip() for line in details_lines if line.strip()]
        details_data = self.parse_details(details_lines)

        # Extract allegations
        allegations = []
        allegations_table = response.css("div.complaints.is-hidden-mobile table.table")
        allegation_rows = allegations_table.css("tr.allegation")
        for row in allegation_rows:
            a = self.parse_allegation(row)
            if a is not None:
                allegations.append(a)

        # Extract penalties
        penalties = []
        p_divs = response.css("div.penalty")
        for d in p_divs:
            p = self.parse_penalty(d)
            if p is not None:
                penalties.append(p)

        # Form the complaint
        complaint_data = {
            k: v
            for k, v in {
                "source_details": SOURCE_REL,
                "record_id": record_id,
                "incident_date": details_data.get("incident_date", None),
                "received_date": details_data.get("received_date", None),
                "closed_date": details_data.get("closed_date", None),
                "reason_for_contact": details_data.get("reason_for_contact", None),
                "outcome_of_contact": details_data.get("outcome_of_contact", None),
                "location": details_data.get("location", None),
                "notes": details_data.get("notes", None),
                "attachments": attachments,
                "allegations": allegations,
                "penalties": penalties,
            }.items()
            if v is not None
        }

        try:
            complaint = CreateComplaint(**complaint_data)
        except ValueError as e:
            logging.error(f"Validation error for complaint {complaint_data}: {e}")
            return None

        yield ComplaintItem(
            url=response.url,
            model="complaint",
            data=complaint.model_dump(),
            scraped_at=datetime.now(UTC),
        )

    def parse_allegation(self, row):
        # Officer information
        # officer_name = row.css('td.officer a.name::text').get()
        officer_url = row.css("td.officer a.name::attr(href)").get()
        # officer_title = row.css('td.officer a.name::attr(title)').get()

        # Complainant information
        complainant_text = row.css("td.complainant").xpath("normalize-space()").get()
        complainant = self.parse_complainant(complainant_text)

        # Allegation and disposition
        allegation_info = row.css("td.allegation::text").get()
        allegation_type, allegation_desc = allegation_info.split(":", 1)

        disposition = row.css("td.disposition::text").get()
        if "Substantiated" in disposition:
            s_split = disposition.split("(")
            disposition = s_split[0].strip()
            outcome = s_split[1].strip(")")
        else:
            outcome = None

        # Build the allegation dictionary
        allegation_data = {
            "perpetrator_uid": officer_url,
            "type": allegation_type.strip() if allegation_type else None,
            "allegation": allegation_desc.strip() if allegation_desc else None,
            "finding": disposition.strip() if disposition else None,
            "outcome": outcome,
            "complainant": complainant,
        }

        try:
            allegation = CreateAllegation(**allegation_data)
        except ValueError as e:
            logging.error(f"Validation error for allegation {allegation_data}: {e}")
            return None
        return allegation

    @staticmethod
    def parse_attachments(details_section):
        """Parse the details section into a dictionary"""
        attachments = []

        # Extract the entire text content, including text from links
        details_text = details_section.xpath("string(.)").get()
        details_text = details_text.replace("\xa0", " ").strip()

        # Extract 'Document' links and titles
        document_sections = details_section.xpath(".//b[contains(text(),'Document:')]")
        for doc_section in document_sections:
            # Collect following siblings until the next <br> or empty text node
            siblings = doc_section.xpath("following-sibling::*")
            for sibling in siblings:
                if sibling.root.tag == "br":
                    break  # Stop if we reach a <br> tag
                if sibling.root.tag == "a":
                    document_link = sibling.xpath("./@href").get()
                    document_title = sibling.xpath("normalize-space(text())").get()
                    if document_link:
                        attachments.append(
                            {
                                "title": document_title,
                                "url": document_link,
                            }
                        )
                else:
                    # Skip other tags if necessary
                    continue
        return attachments

    @staticmethod
    def parse_complainant(complainant_text):
        """Parse the complainant details from the text"""
        complainant_details = get_demographics(complainant_text)
        try:
            complainant = Civilian(**complainant_details)
        except ValueError as e:
            logging.error(
                f"Validation error for complainant {complainant_details}: {e}"
            )
            return None
        return complainant

    @staticmethod
    def parse_details(details_lines):
        """Parse the details section into a dictionary"""
        details = {}
        notes = []
        lines_iter = iter(details_lines)
        for line in lines_iter:
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key == "Incident":
                    details["incident_date"] = convert_str_to_date(value)
                elif key == "Received":
                    details["received_date"] = convert_str_to_date(value)
                elif key == "Closed":
                    details["closed_date"] = convert_str_to_date(value)
                elif key == "Reason for contact":
                    details["reason_for_contact"] = value
                elif key == "Outcome":
                    details["outcome_of_contact"] = value
                elif key == "Location":
                    details["location_type"] = value
                else:
                    # Add any other key-value pairs if necessary
                    details[key.lower().replace(" ", "_")] = value
            else:
                if line == "In NYPD":
                    # Next lines are precinct and borough
                    precinct = next(lines_iter, "").strip()
                    borough = next(lines_iter, "").strip()
                    details["precinct"] = precinct
                    details["borough"] = borough
                else:
                    # Capture any other notes or special lines
                    notes.append(line)
        if notes:
            details["notes"] = "; ".join(notes)

        # Compose the location dictionary
        location_data = {
            "location_type": details.pop("location_type", ""),
            "responsibility_type": "precinct",  # Always 'precinct' for NYPD
            "location_description": "{}, {}".format(
                details.pop("precinct", ""), details.pop("borough", "")
            ).strip(", "),
        }
        try:
            location = Location(**location_data)
            details["location"] = location.model_dump()
        except ValueError as e:
            logging.error(
                "Validation error for location {}: {}".format(location_data, e)
            )
            details["location"] = None
        return details

    @staticmethod
    def parse_address(address):
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
                "zip_code": zip_code,
            }
        else:
            logging.error(f"Failed to parse address: {address}")
            return None

    @staticmethod
    def parse_penalty(div):
        """Possible div classes
        apu_plea
        apu_status penalty_details
        nypd_disposition
        nppd_penalty
            span.nypd_penalty_details
        """
        p_data = {
            "officer_uid": None,
            "crb_plea": None,
            "crb_case_status": None,
            "crb_disposition": None,
            "agency_disposition": None,
            "penalty": None,
            "date_assesed": None,
        }
        p_data["officer_uid"] = div.css("a.name::attr(href)").get()
        p_data["crb_plea"] = (
            div.css("div.apu_plea")
            .xpath("normalize-space(text()[normalize-space()])")
            .get()
        )
        apu_disp = (
            div.css("div.apu_status.penalty_details")
            .xpath("normalize-space(text()[normalize-space()])")
            .get()
        )
        if apu_disp:
            parts = apu_disp.split(":")
            p_data["crb_case_status"] = parts[0]
            if len(parts) > 1:
                d_parts = parts[1].split(",")
                if len(d_parts) > 1:
                    p_data["date_assesed"] = convert_str_to_date(d_parts[-1].strip())
                    p_data["crb_disposition"] = ",".join(d_parts[:-1]).strip()
                else:
                    p_data["crb_disposition"] = parts[1]
        p_data["agency_disposition"] = "".join(
            div.css("div.nypd_disposition::text").getall()
        ).strip()
        p_data["penalty"] = div.css(
            "div.nypd_penalty span.nypd_penalty_details::text"
        ).get()
        try:
            p = CreatePenalty(**p_data)
        except ValueError as e:
            logging.error(f"Validation error for penalty {p_data}: {e}")
            return None
        return p
