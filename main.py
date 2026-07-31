# =========================================================
# NAUKRI JOB ANALYTICS PLATFORM
# MAIN PIPELINE
# =========================================================

import os
import time
import sqlite3
import logging
import traceback
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

# =========================================================
# SCRAPERS
# =========================================================

from scraper.naukri_scraper import scrape_naukri_jobs
from scraper.greenhouse_scraper import scrape_greenhouse
from scraper.lever_scraper import scrape_lever
from scraper.workday_scraper import scrape_workday
from scraper.smartrecruiters_scraper import scrape_smartrecruiters

# =========================================================
# PARSERS
# =========================================================

from scraper.experience_parser import parse_experience
from scraper.salary_parser import parse_salary
from scraper.workmode_parser import detect_work_mode

# =========================================================
# DATA ENRICHMENT
# =========================================================

from scraper.skill_normalizer import normalize_skill_list
from scraper.job_classifier import classify_job
from scraper.analytics_relevance import is_analytics_relevant

# =========================================================
# ANALYTICS
# =========================================================

from analytics.skill_frequency import generate_skill_frequency
from analytics.company_frequency import generate_company_frequency
from analytics.location_frequency import (
    generate_location_frequency,
    generate_workmode_frequency,
)
from analytics.experience_frequency import generate_experience_frequency
from analytics.role_frequency import generate_role_frequency
from analytics.salary_frequency import generate_salary_frequency
from analytics.source_quality import (
    generate_source_quality,
    generate_field_quality,
)

# =========================================================
# CREATE FOLDERS
# =========================================================

os.makedirs("data", exist_ok=True)
os.makedirs("database", exist_ok=True)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================================================
# CONFIGURATION
# =========================================================

NAUKRI_PAGES = 20
MAX_WORKERS = 1

KEYWORDS = [
    "data-analyst",
    "business-analyst",
    "data-scientist",
    "machine-learning",
    "power-bi",
    "sql",
    "python",
    "tableau",
    "data-engineer",
    "analytics",
    "reporting-analyst",
    "research-analyst",
    "business-intelligence",
    "analytics-engineer",
    "etl",
    "bi-developer",
]

# =========================================================
# STORAGE
# =========================================================

all_jobs = []
# =========================================================
# HELPER FUNCTION
# =========================================================

def safe_scrape(name, function):

    logging.info("")
    logging.info("=" * 60)
    logging.info(f"STARTING {name.upper()}")
    logging.info("=" * 60)

    try:

        jobs = function()

        logging.info(f"{name}: {len(jobs)} jobs")

        return jobs

    except Exception:

        logging.error(traceback.format_exc())

        return []


# =========================================================
# START TIMER
# =========================================================

start_time = time.time()

logging.info("")
logging.info("=" * 60)
logging.info("NAUKRI JOB ANALYTICS PLATFORM")
logging.info("=" * 60)

# =========================================================
# SCRAPE NAUKRI
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("SCRAPING NAUKRI")
logging.info("=" * 60)

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

    futures = {

        executor.submit(
            scrape_naukri_jobs,
            keyword,
            NAUKRI_PAGES
        ): keyword

        for keyword in KEYWORDS

    }

    for future in as_completed(futures):

        keyword = futures[future]

        try:

            jobs = future.result()

            logging.info(
                f"{keyword}: {len(jobs)} jobs"
            )

            all_jobs.extend(jobs)

        except Exception:

            logging.error(traceback.format_exc())


# =========================================================
# SCRAPE GREENHOUSE
# =========================================================

greenhouse_jobs = safe_scrape(
    "Greenhouse",
    scrape_greenhouse
)

all_jobs.extend(greenhouse_jobs)


# =========================================================
# SCRAPE LEVER
# =========================================================

lever_jobs = safe_scrape(
    "Lever",
    scrape_lever
)

all_jobs.extend(lever_jobs)


# =========================================================
# SCRAPE WORKDAY
# =========================================================

workday_jobs = safe_scrape(
    "Workday",
    scrape_workday
)

all_jobs.extend(workday_jobs)


# =========================================================
# SCRAPE SMARTRECRUITERS
# =========================================================

smart_jobs = safe_scrape(
    "SmartRecruiters",
    scrape_smartrecruiters
)

all_jobs.extend(smart_jobs)


# =========================================================
# SCRAPING SUMMARY
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info(f"TOTAL RAW JOBS : {len(all_jobs)}")
logging.info("=" * 60)


# =========================================================
# EMPTY CHECK
# =========================================================

if not all_jobs:

    logging.error("No jobs scraped.")

    raise SystemExit
# =========================================================
# CLEAN DATA
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("CLEANING DATA")
logging.info("=" * 60)

cleaned_jobs = []

for job in all_jobs:

    try:

        # -------------------------------------------------
        # BASIC FIELDS
        # -------------------------------------------------

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

        keyword = str(
            job.get("Keyword", "")
        ).replace("-", " ").title()

        source = str(
            job.get("Source", "Unknown")
        ).strip()

        posted_date = str(
            job.get("Posted_Date", "Recent")
        ).strip()

        job_link = str(
            job.get("Job_Link", "")
        ).strip()

        # -------------------------------------------------
        # REMOVE INVALID RECORDS
        # -------------------------------------------------

        if (
            title.lower() == "unknown"
            or company.lower() == "unknown"
        ):
            continue

        # -------------------------------------------------
        # EXPERIENCE
        # -------------------------------------------------

        exp_min, exp_max = parse_experience(
            experience
        )

        # -------------------------------------------------
        # SALARY
        # -------------------------------------------------

        salary_min, salary_max = parse_salary(
            salary
        )

        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        if isinstance(skills, list):

            skills = ", ".join(

                str(skill).strip()

                for skill in skills

                if str(skill).strip()

            )

        else:

            skills = str(skills)

        skills = normalize_skill_list(skills)

        if not skills:
            skills = "Not Available"

        # -------------------------------------------------
        # WORK MODE
        # -------------------------------------------------

        work_mode = detect_work_mode(location)

        # -------------------------------------------------
        # JOB CATEGORY
        # -------------------------------------------------

        job_category = classify_job(title)

        # -------------------------------------------------
        # SAVE CLEAN RECORD
        # -------------------------------------------------

        cleaned_jobs.append({

            "Title": title,
            "Company": company,
            "Location": location,

            "Experience": experience,
            "Experience_Min": exp_min,
            "Experience_Max": exp_max,

            "Salary": salary,
            "Salary_Min": salary_min,
            "Salary_Max": salary_max,

            "Skills": skills,

            "Job_Category": job_category,

            "Keyword": keyword,
            "Source": source,
            "Posted_Date": posted_date,
            "Work_Mode": work_mode,
            "Job_Link": job_link,

        })

    except Exception as e:

        logging.warning(
            f"Cleaning Error: {e}"
        )

logging.info(
    f"Cleaned Jobs : {len(cleaned_jobs)}"
)
# =========================================================
# DATAFRAME
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("CREATING DATAFRAME")
logging.info("=" * 60)

df = pd.DataFrame(cleaned_jobs)

logging.info(f"Rows Before Cleaning : {len(df)}")

# =========================================================
# REMOVE DUPLICATES
# =========================================================

df.drop_duplicates(

    subset=[
        "Title",
        "Company",
        "Location",
    ],

    inplace=True

)

df.reset_index(
    drop=True,
    inplace=True
)

logging.info(f"Rows After Cleaning : {len(df)}")

# =========================================================
# ANALYTICS RELEVANCE GATE
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("ANALYTICS RELEVANCE GATE")
logging.info("=" * 60)

rows_before = len(df)

df = df[
    df["Title"]
    .fillna("")
    .apply(is_analytics_relevant)
].copy()

df.reset_index(
    drop=True,
    inplace=True
)

rows_after = len(df)

logging.info(f"Rows Before Gate : {rows_before}")
logging.info(f"Rows After Gate  : {rows_after}")
logging.info(f"Rows Removed     : {rows_before - rows_after}")

retention = (
    rows_after / rows_before * 100
    if rows_before else 0
)

logging.info(
    f"Retention Rate   : {retention:.2f}%"
)

# =========================================================
# WORK MODE
# =========================================================

if "Location" in df.columns:

    df["Work_Mode"] = (
        df["Location"]
        .fillna("")
        .apply(detect_work_mode)
    )

    logging.info("Work_Mode generated.")

else:

    logging.warning(
        "Location column missing."
    )

# =========================================================
# ROLE CATEGORY
# =========================================================

if "Title" in df.columns:

    df["Role_Category"] = (
        df["Title"]
        .fillna("")
        .apply(classify_job)
    )

    logging.info("Role_Category generated.")

else:

    logging.warning(
        "Title column missing."
    )
# =========================================================
# GENERATE ANALYTICS
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("GENERATING ANALYTICS")
logging.info("=" * 60)

# ---------------------------------------------------------
# Skill Frequency
# ---------------------------------------------------------

try:

    skill_frequency_df = generate_skill_frequency(df)

    logging.info(
        f"Skill Frequency : {len(skill_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Skill Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Company Frequency
# ---------------------------------------------------------

try:

    company_frequency_df = generate_company_frequency(df)

    logging.info(
        f"Company Frequency : {len(company_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Company Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Location Frequency
# ---------------------------------------------------------

try:

    location_frequency_df = generate_location_frequency(df)

    logging.info(
        f"Location Frequency : {len(location_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Location Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Work Mode Frequency
# ---------------------------------------------------------

try:

    workmode_frequency_df = generate_workmode_frequency(df)

    logging.info(
        f"Work Mode Frequency : {len(workmode_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Work Mode Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Experience Frequency
# ---------------------------------------------------------

try:

    experience_frequency_df = generate_experience_frequency(df)

    logging.info(
        f"Experience Frequency : {len(experience_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Experience Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Role Frequency
# ---------------------------------------------------------

try:

    role_frequency_df = generate_role_frequency(df)

    logging.info(
        f"Role Frequency : {len(role_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Role Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Salary Frequency
# ---------------------------------------------------------

try:

    salary_frequency_df = generate_salary_frequency(df)

    logging.info(
        f"Salary Frequency : {len(salary_frequency_df)}"
    )

except Exception as e:

    logging.error(
        f"Salary Frequency Error : {e}"
    )

# ---------------------------------------------------------
# Source Quality
# ---------------------------------------------------------

try:

    source_quality_df = generate_source_quality(df)

    field_quality_df = generate_field_quality(df)

    logging.info(
        f"Source Quality : {len(source_quality_df)}"
    )

    logging.info(
        f"Field Quality : {len(field_quality_df)}"
    )

except Exception as e:

    logging.error(
        f"Source Quality Error : {e}"
    )
# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("FINALIZING DATASET")
logging.info("=" * 60)

df.columns = [
    col.replace(" ", "_")
       .replace("-", "_")
       .replace("(", "")
       .replace(")", "")
    for col in df.columns
]

# =========================================================
# SORT DATA
# =========================================================

df.sort_values(
    by=["Company", "Title"],
    inplace=True
)

df.reset_index(
    drop=True,
    inplace=True
)

logging.info(f"Final Dataset Rows : {len(df)}")

# =========================================================
# PUBLICATION QUALITY GATE
# =========================================================

IS_CI = os.getenv("CI", "").lower() == "true"

MIN_PUBLISH_JOBS = 2000
MIN_PUBLISH_SOURCES = 3

required_sources = set()

if not IS_CI:
    required_sources.add("Naukri")

publish_sources = set(
    df["Source"]
    .dropna()
    .astype(str)
    .str.strip()
)

errors = []

if len(df) < MIN_PUBLISH_JOBS:
    errors.append(
        f"Job count ({len(df)}) is below {MIN_PUBLISH_JOBS}"
    )

if len(publish_sources) < MIN_PUBLISH_SOURCES:
    errors.append(
        f"Only {len(publish_sources)} sources found"
    )

missing_sources = required_sources - publish_sources

if missing_sources:
    errors.append(
        "Missing required sources: "
        + ", ".join(sorted(missing_sources))
    )

if errors:

    logging.critical("")
    logging.critical("=" * 60)
    logging.critical("PUBLICATION QUALITY GATE FAILED")
    logging.critical("=" * 60)

    for err in errors:
        logging.critical(err)

    raise RuntimeError(
        "Publication blocked:\n"
        + "\n".join(errors)
    )

logging.info("Publication Quality Gate Passed")

# =========================================================
# SAVE CSV
# =========================================================

timestamp = time.strftime("%Y%m%d_%H%M%S")

csv_path = os.path.join(
    "data",
    f"jobs_{timestamp}.csv"
)

df.to_csv(
    csv_path,
    index=False,
    encoding="utf-8-sig"
)

logging.info(f"CSV Saved : {csv_path}")

# =========================================================
# SQLITE DATABASE
# =========================================================

db_path = os.path.join(
    "database",
    "jobs.db"
)

with sqlite3.connect(db_path) as conn:

    df.to_sql(
        "jobs",
        conn,
        if_exists="replace",
        index=False
    )

logging.info("SQLite Updated Successfully")

# =========================================================
# SNAPSHOT RETENTION
# =========================================================

RETENTION = 5

snapshots = sorted(
    Path("data").glob("jobs_*.csv"),
    key=lambda x: x.name,
    reverse=True
)

for snapshot in snapshots[RETENTION:]:

    try:

        snapshot.unlink()

        logging.info(
            f"Removed Snapshot : {snapshot.name}"
        )

    except Exception as e:

        logging.warning(e)

# =========================================================
# PROJECT SUMMARY
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("PROJECT SUMMARY")
logging.info("=" * 60)

logging.info(f"Raw Jobs        : {len(all_jobs)}")
logging.info(f"Final Jobs      : {len(df)}")
logging.info(f"Companies       : {df['Company'].nunique()}")
logging.info(f"Sources         : {df['Source'].nunique()}")

logging.info("")

logging.info("Jobs by Source")

for source, count in (
    df["Source"]
      .value_counts()
      .sort_index()
      .items()
):

    logging.info(
        f"{source:<20} {count}"
    )

logging.info("")

logging.info("Jobs by Category")

for category, count in (
    df["Job_Category"]
      .value_counts()
      .sort_index()
      .items()
):

    logging.info(
        f"{category:<30} {count}"
    )

# =========================================================
# EXECUTION TIME
# =========================================================

elapsed = round(
    time.time() - start_time,
    2
)

logging.info("")
logging.info("=" * 60)
logging.info("SCRAPING COMPLETED")
logging.info("=" * 60)

logging.info(f"Execution Time : {elapsed} sec")
logging.info(f"CSV File       : {csv_path}")
logging.info(f"Database       : {db_path}")

print("\n" + "=" * 60)
print("JOB SCRAPER COMPLETED")
print("=" * 60)
print(f"Raw Jobs   : {len(all_jobs)}")
print(f"Final Jobs : {len(df)}")
print(f"Companies  : {df['Company'].nunique()}")
print(f"Sources    : {df['Source'].nunique()}")
print(f"CSV        : {csv_path}")
print(f"Database   : {db_path}")
print(f"Time       : {elapsed} sec")
print("=" * 60)