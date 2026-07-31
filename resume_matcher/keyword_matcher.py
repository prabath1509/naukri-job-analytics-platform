import re


COMMON_SKILLS = {
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "statistics",
    "machine learning",
    "deep learning",
    "etl",
    "spark",
    "snowflake",
    "aws",
    "azure",
    "gcp",
    "git",
    "mysql",
    "postgresql",
    "oracle",
    "data analysis",
    "data visualization",
}


def extract_skills(text):

    text = text.lower()

    found = set()

    for skill in COMMON_SKILLS:

        if re.search(r"\b" + re.escape(skill) + r"\b", text):

            found.add(skill)

    return sorted(found)