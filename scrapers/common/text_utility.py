from typing import Optional

def strip_and_replace_text(text: str) -> Optional[str]:
    stripped_replaced_text = None
    if text:
        stripped_text = text.strip()
        stripped_replaced_text = stripped_text.replace("/n", "")
    return stripped_replaced_text
