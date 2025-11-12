import logging
import re
from datetime import datetime

from models.enums import Ethnicity, Gender


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
        return datetime.strptime(date_string, "%m/%d/%Y").date()
    except ValueError:
        pass

    try:
        return datetime.strptime(date_string, "%B %d, %Y").date()
    except ValueError:
        return None


def validate_and_return_date_str(date_string):
    """
    Validate if a string is in a recognized date format.
    If it is, return the date in YYYY-MM-DD format.
    Expected Format:
     - 01/15/2020 11:32:00 PM

    :param date_string: The string to validate

    :return: True if valid date format, False otherwise
    """
    if date_string is None:
        return None
    if date_string == "":
        return None

    # If the date_string contains "__", that indicates missing data.
    if "__" in date_string:
        return None

    format_code = "%m/%d/%Y %I:%M:%S %p"
    format_code_alt = "%Y-%m-%d"
    try:
        date = datetime.strptime(date_string, format_code).date()
        return date.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass
    try:
        date = datetime.strptime(date_string, format_code_alt).date()
        return date.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        logging.warning(f"Invalid date format for {date_string}")
    return False


def get_int(value):
    """
    Convert a value to an integer, returning None if conversion fails.

    :param value: The value to convert
    :return: The integer value or None if conversion fails
    """
    if value is None:
        return None

    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    if isinstance(value, str) and value.replace(".", "", 1).isdigit():
        # Handle float strings by converting to int
        try:
            return int(float(value))
        except ValueError:
            logging.warning(f"Failed to convert {value} to int")
            return None
    if isinstance(value, float):
        return int(value)
    logging.warning(f"Failed to convert {value} to int")


def number_to_ordinal(number):
    """Convert an integer to its ordinal representation (e.g., 1 to '1st', 2 to '2nd')."""
    num = int(number)
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(num % 10, "th")
    return f"{num}{suffix}"


def fix_precinct_with_number(unit_label):
    # Regex to capture a number (with optional leading zeros) followed by the word "precinct"
    pattern = r"(\d+)\s*precinct"
    match = re.search(pattern, unit_label, re.IGNORECASE)

    if match:
        # Extract remove leading zeros, add ordinals to number
        number = match.group(1).lstrip("0") or "0"
        ordinal_number = number_to_ordinal(number)
        updated_unit_label = re.sub(
            r"\b0*" + match.group(1) + r"\b\s*precinct",
            ordinal_number + " precinct",
            unit_label,
            1,
            flags=re.IGNORECASE,
        )

        return updated_unit_label

    return unit_label  # Return the original string if no match is found


def map_ethnicity(ethnicity):
    if not ethnicity:
        return None

    ethnicity_mapping = {
        "black": Ethnicity.BLACK_AFRICAN_AMERICAN.value,
        "black or african american": Ethnicity.BLACK_AFRICAN_AMERICAN,
        "white": Ethnicity.WHITE.value,
        "asian": Ethnicity.ASIAN.value,
        "hispanic": Ethnicity.HISPANIC_LATINO.value,
        "hispanic or latino": Ethnicity.HISPANIC_LATINO.value,
        "native american": Ethnicity.AMERICAN_INDIAN_ALASKA_NATIVE.value,
        "native american or alaska native": Ethnicity.AMERICAN_INDIAN_ALASKA_NATIVE.value,
        "native hawaiian": Ethnicity.NATIVE_HAWAIIAN_PACIFIC_ISLANDER.value,
        "native hawaiian or pacific islander": Ethnicity.NATIVE_HAWAIIAN_PACIFIC_ISLANDER.value,
    }

    for key, value in ethnicity_mapping.items():
        if key in ethnicity.lower():
            return value

    return None


def map_gender(gender):
    if not gender:
        return None

    gender_mapping = {
        "male": Gender.MALE.value,
        "female": Gender.FEMALE.value,
    }

    for key, value in gender_mapping.items():
        if key in gender.lower():
            return value

    return None


def unit_regex(unit_signifiers=["Pct.", "No.", "Dist. No.", "District #", "Mud #"]):
    """
    Construct a regex pattern to match unit signifiers.
    """
    # Construct the regex pattern dynamically based on the provided unit signifiers
    signifiers_pattern = "|".join(re.escape(signifier) for signifier in unit_signifiers)
    unit_pattern = re.compile(
        rf"(.*?)({signifiers_pattern})\s*(\d+|\w+)$", re.IGNORECASE
    )
    return unit_pattern


def clean_agency_name(agency_name):
    """
    Remove duplicate occurrences of the word "Office" from the agency name.
    Example: "tarrant co. sheriff's office office" -> "tarrant co. sheriff's office"
    """
    # Use regex to replace multiple occurrences of "office" (case-insensitive) with a single "office"
    cleaned_name = re.sub(r"\boffice\b", "office", agency_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(
        r"\boffice\s+office\b", "office", cleaned_name, flags=re.IGNORECASE
    )
    return cleaned_name.strip()


def indentify_unit(agency_label, unit_pattern):
    """
    Identify the unit from the agency label.
    """
    agency_label = clean_agency_name(agency_label)
    match = unit_pattern.match(agency_label)
    if match:
        parent_agency = match.group(1).strip()
        unit_type = match.group(2).strip()
        unit_name = match.group(3).strip()
        full_unit_name = f"{unit_type} {unit_name}"
        return parent_agency, full_unit_name
    return agency_label, None


def classify_jurisdiction(name: str) -> str:
    """Classify agency jurisdiction based on its name."""
    name_lower = name.lower()
    if any(
        keyword in name_lower
        for keyword in ["federal", "national", "homeland", "u.s. marshals"]
    ):
        return "FEDERAL"
    if name_lower.startswith("illinois department of"):
        return "STATE"
    if "department of corrections" in name_lower:
        if "county" in name_lower:
            return "COUNTY"
        return "STATE"
    if any(keyword in name_lower for keyword in ["state police", "state's"]):
        return "STATE"
    if any(keyword in name_lower for keyword in ["railroad police"]):
        return "PRIVATE"
    if any(
        keyword in name_lower
        for keyword in [
            "sheriff",
            "county",
            "county sheriff",
            "county department",
            "co. sheriff",
            "co. const.",
            "co. correctional",
        ]
    ):
        return "COUNTY"
    if any(
        keyword in name_lower
        for keyword in [
            "isd",
            "independent school district",
            "school district",
            "university",
            "campus police",
        ]
    ):
        return "OTHER"
    if any(keyword in name_lower for keyword in ["police department", "police dept"]):
        return "MUNICIPAL"
    return "OTHER"
