import logging
import random
import re
from datetime import UTC, datetime
from typing import List

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from models.common import Article, Attachemnt
from models.litigation import CreateLitigation
from models.officers import CreateOfficer, StateId
from scrapers.fifty_a.fifty_a.items import AGENCY_UID, LitigationItem, OfficerItem
from scrapers.fifty_a.fifty_a.utils import convert_str_to_date, get_demographics


class OfficerSpider(CrawlSpider):
    name = "officer"
    allowed_domains = ["www.50-a.org"]
    start_urls = ["https://www.50-a.org/commands"]

    def __init__(self, *args, **kwargs):
        super(OfficerSpider, self).__init__(*args, **kwargs)
        self.test_mode = "test_mode" in kwargs
        self.max_officers = int(kwargs.get("max_officers", 10))
        self.crawl_target = kwargs.get("crawl_target")

        if self.test_mode:
            self.rules = (
                Rule(LinkExtractor(allow="officer"), callback="parse_officer"),
            )
        else:
            self.rules = (
                Rule(LinkExtractor(allow="command"), follow=True),
                Rule(LinkExtractor(allow="officer"), callback="parse_officer"),
            )

    def start_requests(self):
        if self.crawl_target:
            yield Request(url=self.crawl_target, callback=self.parse_officer)
        else:
            for url in self.start_urls:
                yield Request(url, callback=self.parse_start_url)

    def parse_start_url(self, response):
        commands = response.css("a.command::attr(href)").getall()
        if self.test_mode and commands:
            selected_command = random.choice(commands)  # nosec
            yield response.follow(selected_command, self.parse_command)
        elif not self.test_mode:
            for command in commands:
                yield response.follow(command, self.parse_command)

    def parse_command(self, response):
        officer_links = response.css("td.officer a.name::attr(href)").getall()
        logging.info(f"Found {len(officer_links)} officers in {response.url}")

        if self.test_mode:
            random.shuffle(officer_links)  # nosec
            officer_links = officer_links[: self.max_officers]

        for officer_link in officer_links:
            logging.info(f"Yeilding request for {officer_link}")
            yield response.follow(officer_link, self.parse_officer)

    def parse_officer(self, response):
        name = response.css("h1.title.name::text").get()
        name_parts = self.parse_name(name)
        description = response.css("span.desc::text").get()
        demo_data = get_demographics(description)

        tax_id = response.css("span.taxid::text").re_first(r"Tax #(\d+)")
        state_id = (
            StateId(state="NY", id_name="Tax ID", value=tax_id) if tax_id else None
        )

        rank = response.css("span.rank::text").get()

        command_info = response.css("div.command::text").get()
        logging.info(f"Command Info: {command_info}")
        since_date = response.css("div.command::text").re(r"since\s+(.*)")[0]
        service_info = response.css("div.service::text").get()
        service_start = re.search(r"started (\w+ \d{4})", service_info)
        service_start = service_start.group(1) if service_start else None

        # Parse News Articles
        articles = self.parse_articles(response)

        # Parse Attachments
        attachments = self.parse_attachments(response)

        officer_data = {
            "first_name": name_parts.get("first_name"),
            "middle_name": name_parts.get("middle_name"),
            "last_name": name_parts.get("last_name"),
            "suffix": name_parts.get("suffix"),
            "ethnicity": demo_data.get("ethnicity", None),
            "gender": demo_data.get("gender", None),
            "date_of_birth": self.estimate_dob(demo_data.get("age", None)),
            "state_ids": [state_id] if state_id else None,
            "articles": articles,
            "attachments": attachments,
        }

        employment_history = []
        employment_history.append(
            {
                "earliest_date": since_date,
                "badge_number": response.css("span.badge::text").get(),
                "highest_rank": rank,
                "unit_uid": response.css("div.command a.command::attr(href)").get(),
                "agency_uid": AGENCY_UID,
            }
        )

        prev_employment = response.css("div.commandhistory a::attr(href)").getall()
        for emp in prev_employment:
            employment_history.append(
                {"unit_uid": emp, "agency_uid": AGENCY_UID, "latest_date": since_date}
            )

        try:
            officer = CreateOfficer(**officer_data)
        except ValueError as e:
            logging.error(f"Validation error for officer {name}: {e}")
            return None

        yield OfficerItem(
            url=response.url,
            model="officer",
            data=officer.model_dump(),
            employment=employment_history,
            service_start=service_start,
            scraped_at=datetime.now(UTC),
        )

        # Yield Litigation Items
        yield from self.parse_litigation(response)

    def parse_litigation(self, response):
        container = response.css("div.lawsuits-details")
        if not container:
            return []

        lawsuits_html = container.get()

        # Adjusted regex for splitting on double <br>
        parts = re.split(r"<br\s*>\s*<br\s*>", lawsuits_html)

        for block in parts:
            block_links = re.findall(r"<a\s+(.*?)>(.*?)</a>", block, re.DOTALL)

            # Convert <br> to newlines, remove other HTML tags
            text = re.sub(r"<br\s*>", "\n", block)
            text = re.sub(r"<.*?>", "", text)
            text = text.strip()

            if not text or "Named in" in text:
                continue

            lines = [lin.strip() for lin in text.split("\n") if lin.strip()]
            if not lines:
                continue

            case_title = None
            docket_number = None
            court_name = None
            court_level = None
            jurisdiction = None
            state = "NY"
            description = None
            start_date = None
            end_date = None
            settlement_amount = None
            url = None
            documents = []
            defendants = []

            # The current officer is a defendant
            defendants.append(response.url)

            # case_title is on line[0]
            case_title = lines[0]

            # docket_number is on line[1], format: "Case # 502483/2024,"
            if len(lines) > 1 and lines[1].startswith("Case #"):
                docket_match = re.match(r"Case #\s*([^,]+)", lines[1])
                if docket_match:
                    docket_number = docket_match.group(1).strip()

            # Court and Date parsing
            # "Supreme Court - Queens, May 18, 2015, ended August 24, 2018"
            if len(lines) > 2:
                court_line = lines[2]
                parts_court = [p.strip() for p in court_line.split(",") if p.strip()]

                # Extract court_name and jurisdiction
                court_info = parts_court[0]
                if " - " in court_info:
                    jurisdiction = court_info.split(" - ")[-1]
                    court_name = court_info
                    jurisdiction = jurisdiction.strip()
                else:
                    court_name = court_info
                    jurisdiction = None

                if len(parts_court) >= 3:
                    # start_date is formed from parts_court[1] and parts_court[2]
                    # e.g. "May 18" and "2015" -> "May 18, 2015"
                    start_date_month_day = parts_court[1].strip()  # "May 18"
                    start_date_year = parts_court[2].strip()  # "2015"
                    start_date = (
                        f"{start_date_month_day}, {start_date_year}"  # "May 18, 2015"
                    )

                    # Check if we have an end date
                    # If we have more than 3 elements, we probably have the "ended" part.
                    # parts_court[3] = "ended August 24"
                    # parts_court[4] = "2018"
                    if len(parts_court) >= 5:
                        ended_line = parts_court[3].strip()  # "ended August 24"
                        # Remove 'ended' to get the month/day
                        if ended_line.lower().startswith("ended"):
                            end_date_month_day = ended_line.replace(
                                "ended", ""
                            ).strip()  # "August 24"
                            end_date_year = parts_court[4].strip()  # "2018"
                            end_date = f"{end_date_month_day}, {end_date_year}"  # "August 24, 2018"
                        else:
                            end_date = None
                    else:
                        end_date = None

                # Determine court_level from court_name
                if court_name and "Supreme Court" in court_name:
                    # In New York, Supreme Court is actually a trial-level court
                    court_level = "State Trial Court"
                elif court_name and "District Court" in court_name:
                    # Check if it's federal district
                    if (
                        "U.S." in court_name
                        or "Eastern District" in court_info
                        or "Southern District" in court_info
                    ):
                        court_level = "Federal District Court"
                    else:
                        court_level = "State Trial Court"
                # else leave court_level = None if not identifiable

            # Check for settlement info
            for ln in lines:
                settlement_match = re.search(
                    r"\$(\d[\d,\.]*) Settlement", ln, re.IGNORECASE
                )
                if settlement_match:
                    amt_str = settlement_match.group(1).replace(",", "")
                    try:
                        settlement_amount = float(amt_str)
                    except ValueError:
                        pass

            # Extract description (lines after "Description:")
            desc_lines = []
            desc_mode = False
            for ln in lines:
                if "Description:" in ln:
                    desc_mode = True
                    desc_text = ln.split("Description:", 1)[-1].strip()
                    if desc_text:
                        desc_lines.append(desc_text)
                elif desc_mode:
                    desc_lines.append(ln)
            if desc_lines:
                description = " ".join(desc_lines)

            # Identify the main URL from the title line
            for link_attrs, link_text in block_links:
                link_text_stripped = link_text.strip()
                href_match = re.search(r'href="([^"]+)"', link_attrs)
                if href_match:
                    link_href = href_match.group(1)
                    # If this link_text matches the case_title line exactly, set url
                    if link_text_stripped == case_title:
                        url = link_href

            # Extract document links
            # Document links have `class="document"`
            # We'll create Attachment objects for these
            for link_attrs, link_text in block_links:
                if 'class="document"' in link_attrs:
                    href_match = re.search(r'href="([^"]+)"', link_attrs)
                    if href_match:
                        doc_url = href_match.group(1)
                        # Set some defaults
                        doc_title = link_text.strip() if link_text.strip() else None
                        doc_type = "document"
                        # We can guess description if needed, or leave None
                        documents.append(
                            {
                                "type": doc_type,
                                "url": doc_url,
                                "title": doc_title,
                                "description": None,
                            }
                        )

            litigation = CreateLitigation(
                case_title=case_title,
                docket_number=docket_number,
                court_name=court_name,
                court_level=court_level,
                jurisdiction=jurisdiction,
                state=state,
                description=description,
                start_date=convert_str_to_date(start_date),
                end_date=convert_str_to_date(end_date),
                settlement_amount=settlement_amount,
                url=url,
                documents=documents if documents else None,
                defendants=defendants,
            )

            yield LitigationItem(
                url=response.url,
                model="litigation",
                data=litigation.model_dump(),
                scraped_at=datetime.now(UTC),
            )

    def parse_articles(self, response) -> List[Article]:
        articles = []
        news_container = response.css("div.news")
        if not news_container:
            return articles
        article_links = news_container.css(
            "a:not([class])"
        )  # exclude any a with class like 'document'

        for link in article_links:
            url = link.attrib.get("href")
            title = link.css("::text").get()

            # Get the text after the <a> tag.
            trailing_text = link.xpath("./following-sibling::text()[1]").get()

            # trailing_text might look like: ", The Intercept, 9/25/2023"
            # Let's clean and split it by commas
            if trailing_text:
                parts = [
                    part.strip() for part in trailing_text.split(",") if part.strip()
                ]

                # After splitting and cleaning:
                # parts[0] -> publisher
                # parts[1] -> publication_date
                if len(parts) >= 2:
                    publisher = parts[0]
                    publication_date = parts[1]
                else:
                    # If there's not enough parts, fallback to None
                    publisher = None
                    publication_date = None
            else:
                publisher = None
                publication_date = None

            if url and title and publisher and publication_date:
                articles.append(
                    Article(
                        url=url,
                        title=title,
                        publisher=publisher,
                        publication_date=convert_str_to_date(publication_date),
                    )
                )

        return articles

    def parse_attachments(self, response) -> List[Attachemnt]:
        attachments = []
        container = response.css("div.other-documents")
        if not container:
            return attachments

        doc_divs = container.css("div.document")
        for doc_div in doc_divs:
            link = doc_div.css("a")
            if not link:
                continue

            url = link.attrib.get("href")
            title = link.css("::text").get()

            # Get any trailing text in this div after the link to form a description
            trailing_texts = link.xpath("./following-sibling::text()").getall()
            description = (
                " ".join(t.strip() for t in trailing_texts if t.strip()) or None
            )

            # Guess the type from URL (if it ends with .pdf or contains .pdf)
            doc_type = "document"
            if url and ".pdf" in url.lower():
                doc_type = "pdf"

            attachment = Attachemnt(
                type=doc_type, url=url, title=title, description=description
            )
            attachments.append(attachment)

        return attachments

    @staticmethod
    def parse_name(name):
        parts = name.split()
        suffixes = ["Jr", "Sr", "II", "III", "IV"]
        result = {}

        if parts[-1] in suffixes:
            result["suffix"] = parts[-1].pop()

        result["first_name"] = parts[0]
        result["last_name"] = parts[-1]
        if len(parts) > 2:
            result["middle_name"] = " ".join(parts[1:-1])
        return result

    @staticmethod
    def estimate_dob(age):
        if age is None:
            return None

        today = datetime.today()
        birth_year = today.year - age
        dob = today.replace(year=birth_year).date()
        return dob
