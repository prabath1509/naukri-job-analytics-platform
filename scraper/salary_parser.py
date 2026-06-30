import re


def parse_salary(text):

    if not text:
        return None, None

    text = str(text).lower().strip()

    if text in ["not available", "nan", "none", ""]:
        return None, None

    # Remove commas and ₹ symbol
    text = text.replace(",", "")
    text = text.replace("₹", "")
    text = text.replace("rs.", "")
    text = text.replace("rs", "")

    # Example: 8-12 lpa
    match = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", text)

    if match:

        low = float(match.group(1))
        high = float(match.group(2))

        if "lpa" in text or "lakh" in text:
            return int(low * 100000), int(high * 100000)

        return int(low), int(high)

    # Example: 10 lpa
    match = re.search(r"(\d+(?:\.\d+)?)", text)

    if match:

        value = float(match.group(1))

        if "lpa" in text or "lakh" in text:
            value = int(value * 100000)

        return int(value), int(value)

    return None, None