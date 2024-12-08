import logging
import re
from datetime import datetime

from models.enums import Ethnicity


def map_ethnicity(ethnicity):
    if not ethnicity:
        return None

    ethnicity_mapping = {
        "black": Ethnicity.BLACK_AFRICAN_AMERICAN,
        "white": Ethnicity.WHITE,
        "asian": Ethnicity.ASIAN,
        "hispanic": Ethnicity.HISPANIC_LATINO,
        "puerto rican": Ethnicity.HISPANIC_LATINO,
        "native american": Ethnicity.AMERICAN_INDIAN_ALASKA_NATIVE,
        "american indian": Ethnicity.AMERICAN_INDIAN_ALASKA_NATIVE,
        "native hawaiian": Ethnicity.NATIVE_HAWAIIAN_PACIFIC_ISLANDER,
    }

    for key, value in ethnicity_mapping.items():
        if key in ethnicity.lower():
            return value

    return None


def get_demographics(demo_text):
    if demo_text is None:
        return None
    demo = {}

    # Process ethnicity and gender
    expected_genders = {"male", "female"}
    text = demo_text.replace("\xa0", " ")
    parts = text.split(",")

    if len(parts) >= 1:
        info = parts[0].strip().split()
        if len(info) >= 1:
            last_word = info[-1].lower()
            first_word = info[0].lower()
            if last_word in expected_genders:
                # Format: Ethnicity Gender
                demo["gender"] = info[-1]
                eth = " ".join(info[:-1]).strip()
                demo["ethnicity"] = map_ethnicity(eth)
            elif first_word in {"age"}:
                # Format: Age {num}
                demo["age"] = info[1]
            else:
                # Format: Ethnicity
                eth = " ".join(info).strip()
                demo["ethnicity"] = map_ethnicity(eth)

    # Process age group and calculate age
    if len(parts) >= 2:
        age_range = parts[1].strip()
        demo["age_range"] = age_range

        # Attempt to parse age range
        age_range_match = re.match(r"(\d+)-(\d+)", age_range)
        if age_range_match:
            age_low = int(age_range_match.group(1))
            age_high = int(age_range_match.group(2))
            # Calculate approximate age as the average
            demo["age"] = (age_low + age_high) // 2
        else:
            # Handle single age or other formats
            age_match = re.match(r"(\d+)", age_range)
            if age_match:
                demo["age"] = int(age_match.group(1))
            else:
                # Age is not available or in an unexpected format
                demo["age"] = None
    return demo


def convert_str_to_date(date_string):
    """
    Convert a string to a date object. Accepts:
    - YYYY-MM-DD
    - Month Year
    - Month Day, Year

    :param date_string: The string to convert

    :return: The date object
    """
    if date_string is None:
        return None

    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_string, "%B %Y").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_string, "%B %d, %Y").date()
    except ValueError:
        logging.error(f"Invalid date format: {date_string}")
        return None
