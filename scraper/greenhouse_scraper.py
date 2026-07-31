# =========================================================
# scraper/greenhouse_scraper.py
# =========================================================

import re
import logging
import requests

from bs4 import BeautifulSoup

GREENHOUSE_BOARDS = [

    "airbyte",
    "openai",
    "coinbase",
    "discord",
    "doordash",
    "figma",
    "instacart",
    "notion",
    "scaleai",
    "snowflake",
    "stripe",
    "brex",
    "datadog",
    "plaid",
    "rubrik",
    "asana",
    "zapier",
    "clickup",
    "canva",
    "grammarly"

]
# =========================================================
# CONFIGURATION
# =========================================================

HEADERS = {

    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )

}

REQUEST_TIMEOUT = 20

# =========================================================
# DATA ANALYTICS KEYWORDS
# =========================================================

DATA_KEYWORDS = [

    "data analyst",
    "business analyst",
    "research analyst",
    "reporting analyst",
    "analytics",

    "data scientist",

    "machine learning",

    "power bi",

    "tableau",

    "sql",

    "python",

    "data engineer",

    "analytics engineer",

    "business intelligence",

    "etl",

    "bi developer",

]

# =========================================================
# SKILL KEYWORDS
# =========================================================

SKILL_KEYWORDS = [

    "Python",
    "SQL",
    "Power BI",
    "Excel",
    "Tableau",

    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",

    "Spark",

    "AWS",
    "Azure",
    "GCP",

    "Snowflake",

    "ETL",

    "Machine Learning",

    "Statistics",

    "Git",

]

# =========================================================
# HELPERS
# =========================================================

def is_relevant_job(title):

    title = str(title).lower()

    return any(

        keyword in title

        for keyword in DATA_KEYWORDS

    )


def clean_text(text):

    if not text:

        return ""

    text = BeautifulSoup(
        text,
        "html.parser"
    ).get_text(" ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_skills(text):

    text = text.lower()

    skills = []

    for skill in SKILL_KEYWORDS:

        if skill.lower() in text:

            skills.append(skill)

    return sorted(set(skills))
    # =========================================================
# EXPERIENCE EXTRACTION
# =========================================================

def extract_experience(text):

    patterns = [

        r"\d+\+?\s*years?",
        r"\d+\s*-\s*\d+\s*years?",
        r"\d+\s*to\s*\d+\s*years?",
        r"minimum\s+\d+\s*years?",
        r"at least\s+\d+\s*years?",
        r"experience\s+of\s+\d+\+?\s*years?"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.I
        )

        if match:

            return match.group(0)

    return "Not Available"


# =========================================================
# SALARY EXTRACTION
# =========================================================

def extract_salary(text):

    patterns = [

        r"₹\s?[\d,]+(?:\s*-\s*₹?[\d,]+)?",

        r"\$[\d,]+(?:\s*-\s*\$?[\d,]+)?",

        r"\d+\s*-\s*\d+\s*LPA",

        r"\d+\+?\s*LPA",

        r"CTC\s*[:\-]?\s*₹?\s?[\d,]+"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.I
        )

        if match:

            return match.group(0)

    return "Not Available"


# =========================================================
# DOWNLOAD JOB DESCRIPTION
# =========================================================

def download_job_description(job_url):

    if not job_url:

        return ""

    try:

        response = requests.get(
            job_url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:

            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return clean_text(
            soup.get_text(" ")
        )

    except Exception as e:

        logging.debug(
            f"Description download failed: {e}"
        )

        return ""


# =========================================================
# BUILD JOB RECORD
# =========================================================

def build_job_record(job, company):

    title = job.get(
        "title",
        "Unknown"
    )

    job_link = job.get(
        "absolute_url",
        ""
    )

    description = download_job_description(
        job_link
    )

    return {

        "Title": title,

        "Company": company.title(),

        "Location": job.get(
            "location",
            {}
        ).get(
            "name",
            "Remote"
        ),

        "Experience": extract_experience(
            description
        ),

        "Salary": extract_salary(
            description
        ),

        "Skills": extract_skills(
            description
        ),

        "Keyword": "Data Analytics",

        "Source": "Greenhouse",

        "Posted_Date": "Recent",

        "Job_Link": job_link

    }
    # =========================================================
# MAIN SCRAPER
# =========================================================

def scrape_greenhouse():

    logging.info("")
    logging.info("=" * 60)
    logging.info("SCRAPING GREENHOUSE")
    logging.info("=" * 60)

    jobs = []

    total_companies = len(GREENHOUSE_BOARDS)

    logging.info(
        f"Boards Configured : {total_companies}"
    )

    for company in GREENHOUSE_BOARDS:

        try:

            api_url = (
                f"https://boards-api.greenhouse.io/v1/boards/"
                f"{company}/jobs"
            )

            response = requests.get(
                api_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code != 200:

                logging.warning(
                    f"{company}: HTTP {response.status_code}"
                )

                continue

            data = response.json()

            company_jobs = 0

            for job in data.get("jobs", []):

                title = job.get(
                    "title",
                    ""
                )

                if not is_relevant_job(title):

                    continue

                try:

                    record = build_job_record(
                        job,
                        company
                    )

                    jobs.append(record)

                    company_jobs += 1

                except Exception as e:

                    logging.debug(
                        f"{company}: Record Error : {e}"
                    )

            logging.info(
                f"{company:<25} {company_jobs} jobs"
            )

        except Exception as e:

            logging.warning(
                f"{company}: {e}"
            )

    logging.info("")
    logging.info("=" * 60)
    logging.info(
        f"Greenhouse Jobs Collected : {len(jobs)}"
    )
    logging.info("=" * 60)

    return jobs
    # =========================================================
# SELF TEST
# =========================================================

if __name__ == "__main__":

    greenhouse_jobs = scrape_greenhouse()

    print("\n" + "=" * 60)
    print("GREENHOUSE SCRAPER SUMMARY")
    print("=" * 60)

    print(f"Total Jobs : {len(greenhouse_jobs)}")

    if greenhouse_jobs:

        print("\nSample Job\n")

        sample = greenhouse_jobs[0]

        for key, value in sample.items():

            print(f"{key:<15}: {value}")

    else:

        print("No jobs were collected.")

    print("=" * 60)
    