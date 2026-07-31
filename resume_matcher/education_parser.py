import re


DEGREE_PATTERNS = [
    "bachelor of technology",
    "b.tech",
    "btech",
    "bachelor of engineering",
    "b.e",
    "be",
    "master of technology",
    "m.tech",
    "mtech",
    "master of science",
    "m.sc",
    "msc",
    "master of business administration",
    "mba",
    "bachelor of science",
    "b.sc",
    "bsc"
]


BRANCH_PATTERNS = [
    "computer science",
    "computer science engineering",
    "information technology",
    "electronics",
    "electronics and communication",
    "mechanical",
    "civil",
    "electrical",
    "artificial intelligence",
    "data science"
]


def extract_education(resume_text):

    text = resume_text.lower()

    degree = None

    branch = None

    graduation_year = None

    # -----------------------------
    # Degree
    # -----------------------------

    for item in DEGREE_PATTERNS:

        if item in text:

            degree = item

            break

    # -----------------------------
    # Branch
    # -----------------------------

    for item in BRANCH_PATTERNS:

        if item in text:

            branch = item

            break

    # -----------------------------
    # Graduation Year
    # -----------------------------

    years = re.findall(
        r"(20\d{2})",
        text
    )

    if years:

        graduation_year = max(
            map(int, years)
        )

    return {

        "Degree": degree,

        "Branch": branch,

        "Graduation Year": graduation_year,

        "Education Found": degree is not None

    }