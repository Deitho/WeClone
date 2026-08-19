import re


def extract_json_from_text(text: str) -> str:
    """Extract JSON content from text, supporting JSON blocks in markdown format."""
    json_pattern = r"```json\s*(.*?)\s*```"
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()
