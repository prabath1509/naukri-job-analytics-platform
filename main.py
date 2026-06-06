# =========================================================
# main.py
# LARGE SCALE AI JOB SCRAPER
# =========================================================

import pandas as pd
import sqlite3
import logging
import time
import os

from scraper.naukri_scraper import scrape_naukri_jobs
from scraper.greenhouse_scraper import scrape_greenhouse
from scraper.lever_scraper import scrape_lever

# =========================================================
# CREATE FOLDERS
# =========================================================

os.makedirs("data", exist_ok=True)

os.makedirs("database", exist_ok=True)

# =========================================================
# LOGGING CONFIG
# =========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================================================
# LARGE SCALE KEYWORDS
# =========================================================

KEYWORDS = [

    "data-analyst",
    "business-analyst",
    "data-scientist",
    "data-engineer",
    "machine-learning-engineer",
    "analytics-engineer",
    "business-intelligence",
    "sql-developer",
    "power-bi-developer",
    "tableau-developer",
    "etl-developer",
    "reporting-analyst",
    "research-analyst",
    "data-analyst-fresher",
    "data-science-intern"
]

# =========================================================
# SCRAPE NAUKRI
# =========================================================

logging.info("STARTING NAUKRI SCRAPING")

naukri_jobs = []

for keyword in KEYWORDS:

    try:

        logging.info(

            f"SCRAPING KEYWORD: {keyword}"
        )

        jobs = scrape_naukri_jobs(

            keyword=keyword,

            pages=15
        )

        logging.info(

            f"{keyword}: {len(jobs)} jobs scraped"
        )

        naukri_jobs.extend(jobs)

    except Exception as e:

        logging.error(

            f"Naukri Error ({keyword}): {e}"
        )

# =========================================================
# SCRAPE GREENHOUSE
# =========================================================

logging.info("STARTING GREENHOUSE SCRAPING")

greenhouse_jobs = []

try:

    greenhouse_jobs = scrape_greenhouse()

    logging.info(

        f"Greenhouse Jobs: {len(greenhouse_jobs)}"
    )

except Exception as e:

    logging.error(

        f"Greenhouse Error: {e}"
    )

# =========================================================
# SCRAPE LEVER
# =========================================================

logging.info("STARTING LEVER SCRAPING")

lever_jobs = []

try:

    lever_jobs = scrape_lever()

    logging.info(

        f"Lever Jobs: {len(lever_jobs)}"
    )

except Exception as e:

    logging.error(

        f"Lever Error: {e}"
    )

# =========================================================
# COMBINE DATA
# =========================================================

all_jobs = (

    naukri_jobs +

    greenhouse_jobs +

    lever_jobs
)

logging.info(

    f"TOTAL RAW JOBS: {len(all_jobs)}"
)

# =========================================================
# CLEAN DATA
# =========================================================

cleaned_jobs = []

for job in all_jobs:

    try:

        title = str(

            job.get("Title", "Unknown")

        ).strip()

        company = str(

            job.get("Company", "Unknown")

        ).strip()

        location = str(

            job.get("Location", "Unknown")

        ).strip()

        experience = str(

            job.get("Experience", "Not Available")

        ).strip()

        salary = str(

            job.get("Salary", "Not Available")

        ).strip()

        skills = job.get("Skills", [])

        # =================================================
        # SKILLS CLEANING
        # =================================================

        if isinstance(skills, list):

            clean_skills = []

            for skill in skills:

                skill = str(skill).strip()

                if (

                    skill != ""

                    and skill.lower() != "nan"

                    and len(skill) > 1
                ):

                    clean_skills.append(skill)

            skills = ", ".join(clean_skills)

        else:

            skills = str(skills)

        if skills.strip() == "":

            skills = "Not Available"

        keyword = str(

            job.get("Keyword", "")

        ).replace("-", " ").title()

        source = str(

            job.get("Source", "Naukri")

        ).strip()

        posted_date = str(

            job.get("Posted_Date", "Recent")

        ).strip()

        job_link = str(

            job.get("Job_Link", "")

        ).strip()

        # =================================================
        # REMOVE INVALID JOBS
        # =================================================

        if (

            title.lower() == "unknown"

            or company.lower() == "unknown"
        ):

            continue

        cleaned_jobs.append({

            "Title": title,

            "Company": company,

            "Location": location,

            "Experience": experience,

            "Salary": salary,

            "Skills": skills,

            "Keyword": keyword,

            "Source": source,

            "Posted_Date": posted_date,

            "Job_Link": job_link
        })

    except Exception as e:

        logging.error(

            f"Cleaning Error: {e}"
        )

# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame(cleaned_jobs)

# =========================================================
# REMOVE DUPLICATES
# =========================================================

df.drop_duplicates(

    subset=[

        "Title",

        "Company",

        "Location"
    ],

    inplace=True
)

# =========================================================
# RESET INDEX
# =========================================================

df.reset_index(

    drop=True,

    inplace=True
)

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = [

    col.replace(" ", "_")
    .replace("-", "_")
    .replace("(", "")
    .replace(")", "")

    for col in df.columns
]

# =========================================================
# SAVE CSV
# =========================================================

timestamp = time.strftime(

    "%Y%m%d_%H%M%S"
)

csv_path = (

    f"data/jobs_{timestamp}.csv"
)

df.to_csv(

    csv_path,

    index=False
)

logging.info(

    f"CSV Saved: {csv_path}"
)

# =========================================================
# SAVE SQLITE DATABASE
# =========================================================

db_path = "database/jobs.db"

conn = sqlite3.connect(db_path)

df.to_sql(

    "jobs",

    conn,

    if_exists="replace",

    index=False
)

conn.close()

logging.info(

    f"Database Saved: {db_path}"
)

# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n=================================================")

print("SCRAPING COMPLETED SUCCESSFULLY")

print("=================================================")

print(

    f"\nTOTAL JOBS SCRAPED: {len(df)}"
)

print("\nTOP 5 JOBS:\n")

print(df.head())

print("\n=================================================")