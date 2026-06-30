import re


def parse_experience(text):

    if not text:
        return None, None

    text = str(text).lower().strip()

    # Freshers
    if "fresher" in text:
        return 0, 0

    # 0-2 years
    match = re.search(r"(\d+)\s*[-to]+\s*(\d+)", text)

    if match:

        return int(match.group(1)), int(match.group(2))

    # 3+ years
    match = re.search(r"(\d+)\+", text)

    if match:

        return int(match.group(1)), None

    # 5 years
    match = re.search(r"(\d+)", text)

    if match:

        value = int(match.group(1))

        return value, value

    return None, None