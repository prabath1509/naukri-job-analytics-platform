import re

# -----------------------------------
# CLEAN TEXT
# -----------------------------------

def clean_text(text):

    if text is None:
        return "Not Available"

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# -----------------------------------
# NORMALIZE COMPANY
# -----------------------------------

def normalize_company(company):

    company = clean_text(company)

    return company.lower()

# -----------------------------------
# NORMALIZE TITLE
# -----------------------------------

def normalize_title(title):

    title = clean_text(title)

    return title.lower()

# -----------------------------------
# CREATE DEDUPLICATION KEY
# -----------------------------------

def create_job_key(row):

    title = normalize_title(
        row.get("Title")
    )

    company = normalize_company(
        row.get("Company")
    )

    location = clean_text(
        row.get("Location")
    ).lower()

    return f"{title}_{company}_{location}"