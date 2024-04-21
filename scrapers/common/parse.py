from typing import Optional


def parse_string_to_number(string: Optional[str]) -> Optional[int]:
    try:
        return int(string)
    except TypeError:
        # Handle None input
        return None
    except ValueError as e:
        # Parsing decimals is not implemented yet
        raise NotImplementedError(e)
