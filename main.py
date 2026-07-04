# =========================================================
# NAUKRI JOB ANALYTICS PLATFORM
# MAIN PIPELINE
# =========================================================

import os
import time
import sqlite3
import logging
import traceback

import pandas as pd

# =========================================================
# SCRAPERS
# =========================================================

from scraper.naukri_scraper import scrape_naukri_jobs
from scraper.greenhouse_scraper import scrape_greenhouse
from scraper.lever_scraper import scrape_lever
from scraper.workday_scraper import scrape_workday
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.experience_parser import parse_experience
from scraper.salary_parser import parse_salary
from scraper.workmode_parser import detect_work_mode
from analytics.skill_frequency import generate_skill_frequency
from analytics.company_frequency import generate_company_frequency
from analytics.location_frequency import (
    generate_location_frequency,
    generate_workmode_frequency,
)
from analytics.experience_frequency import generate_experience_frequency
from scraper.job_classifier import classify_job
from analytics.role_frequency import generate_role_frequency
from analytics.salary_frequency import generate_salary_frequency
from analytics.source_quality import (
    generate_source_quality,
    generate_field_quality,
)

# Optional
try:
    from scraper.smartrecruiters_scraper import scrape_smartrecruiters
    SMART_AVAILABLE = True
except Exception:
    SMART_AVAILABLE = False

# =========================================================
# DATA ENRICHMENT
# =========================================================

from scraper.skill_normalizer import normalize_skill_list
from scraper.job_classifier import classify_job

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

NAUKRI_PAGES = 10

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

    "etl",

    "bi-developer"

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
# NAUKRI SCRAPER
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("SCRAPING NAUKRI")
logging.info("=" * 60)


MAX_WORKERS = 1

logging.info("")
logging.info("=" * 60)
logging.info("STARTING PARALLEL NAUKRI SCRAPING")
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

            logging.error(

                traceback.format_exc()

            )

# =========================================================
# GREENHOUSE
# =========================================================

greenhouse_jobs = safe_scrape(

    "Greenhouse",

    scrape_greenhouse

)

all_jobs.extend(

    greenhouse_jobs

)

# =========================================================
# LEVER
# =========================================================

lever_jobs = safe_scrape(

    "Lever",

    scrape_lever

)

all_jobs.extend(

    lever_jobs

)

# =========================================================
# WORKDAY
# =========================================================

workday_jobs = safe_scrape(

    "Workday",

    scrape_workday

)

all_jobs.extend(

    workday_jobs

)

# =========================================================
# SMARTRECRUITERS
# =========================================================

if SMART_AVAILABLE:

    smart_jobs = safe_scrape(

        "SmartRecruiters",

        scrape_smartrecruiters

    )

    all_jobs.extend(

        smart_jobs

    )

else:

    logging.info(

        "SmartRecruiters Disabled"

    )

# =========================================================
# SUMMARY
# =========================================================

logging.info("")

logging.info("=" * 60)

logging.info(

    f"TOTAL RAW JOBS : {len(all_jobs)}"

)

logging.info("=" * 60)

# =========================================================
# EMPTY CHECK
# =========================================================

if len(all_jobs) == 0:

    logging.error(

        "No jobs scraped."

    )

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

        title = str(
            job.get("Title", "Unknown")
        ).strip()

        company = str(
            job.get("Company", "Unknown")
        ).strip()

        location = str(
            job.get("Location", "Unknown")
        ).strip()

        work_mode = detect_work_mode(location)

        experience = str(
            job.get("Experience", "Not Available")
        ).strip()
        exp_min, exp_max = parse_experience(experience)

        salary = str(
            job.get("Salary", "Not Available")
        ).strip()
        salary_min, salary_max = parse_salary(salary)
        skills = job.get(
            "Skills",
            []
        )

        # ================================================
        # SKILL CLEANING
        # ================================================

        if isinstance(skills, list):

            skills = ", ".join(

                str(skill).strip()

                for skill in skills

                if str(skill).strip()

            )

        else:

            skills = str(skills)

        if skills.strip() == "":

            skills = "Not Available"

        # ================================================
        # NORMALIZE SKILLS
        # ================================================

        skills = normalize_skill_list(skills)

        # ================================================
        # OTHER FIELDS
        # ================================================

        keyword = str(
            job.get("Keyword", "")
        ).replace("-", " ").title()

        source = str(
            job.get("Source", "Unknown")
        )

        posted_date = str(
            job.get("Posted_Date", "Recent")
        )

        job_link = str(
            job.get("Job_Link", "")
        )

        # ================================================
        # REMOVE BAD RECORDS
        # ================================================

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

            "Experience_Min": exp_min,

            "Experience_Max": exp_max,

            "Salary": salary,

            "Salary_Min": salary_min,

            "Salary_Max": salary_max,

            "Skills": skills,

            "Job_Category": classify_job(title),

            "Keyword": keyword,

            "Source": source,

            "Posted_Date": posted_date,

            "Work_Mode": work_mode,

            "Job_Link": job_link

        })

    except Exception as e:

        logging.warning(

            f"Cleaning Error : {e}"

        )

# =========================================================
# DATAFRAME
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("CREATING DATAFRAME")
logging.info("=" * 60)

df = pd.DataFrame(cleaned_jobs)

logging.info(

    f"Rows Before Cleaning : {len(df)}"

)

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

df.reset_index(

    drop=True,

    inplace=True

)

logging.info(

    f"Rows After Cleaning : {len(df)}"

)
# =========================================================
# GENERATE WORK MODE
# =========================================================

try:

    if "Location" in df.columns:

        df["Work_Mode"] = (
            df["Location"]
            .fillna("")
            .apply(detect_work_mode)
        )

        logging.info(
            "Work_Mode column generated successfully"
        )

    else:

        logging.warning(
            "Location column not found. "
            "Work_Mode could not be generated."
        )

except Exception as e:

    logging.error(
        f"Work Mode Generation Error: {e}"
    )
# =========================================================
# GENERATE ROLE CATEGORY
# =========================================================

try:

    if "Title" in df.columns:

        df["Role_Category"] = (
            df["Title"]
            .fillna("")
            .apply(classify_job)
        )

        logging.info(
            "Role_Category column generated successfully"
        )

    else:

        logging.warning(
            "Title column not found. "
            "Role_Category could not be generated."
        )

except Exception as e:

    logging.error(
        f"Role Category Generation Error: {e}"
    )
# =========================================================
# SKILL FREQUENCY ANALYTICS
# =========================================================

try:

    skill_frequency_df = generate_skill_frequency(df)

    logging.info(
        f"Skill Frequency Generated: "
        f"{len(skill_frequency_df)} skills"
    )

except Exception as e:

    logging.error(
        f"Skill Frequency Error: {e}"
    )
# =========================================================
# COMPANY DEMAND ANALYTICS
# =========================================================

try:

    company_frequency_df = generate_company_frequency(df)

    logging.info(
        f"Company Demand Analytics Generated: "
        f"{len(company_frequency_df)} companies"
    )

except Exception as e:

    logging.error(
        f"Company Demand Analytics Error: {e}"
    )
# =========================================================
# LOCATION DEMAND ANALYTICS
# =========================================================

try:

    location_frequency_df = (
        generate_location_frequency(df)
    )

    logging.info(
        f"Location Demand Analytics Generated: "
        f"{len(location_frequency_df)} locations"
    )

except Exception as e:

    logging.error(
        f"Location Demand Analytics Error: {e}"
    )


# =========================================================
# WORK MODE ANALYTICS
# =========================================================

try:

    workmode_frequency_df = (
        generate_workmode_frequency(df)
    )

    logging.info(
        f"Work Mode Analytics Generated: "
        f"{len(workmode_frequency_df)} modes"
    )

except Exception as e:

    logging.error(
        f"Work Mode Analytics Error: {e}"
    )
# =========================================================
# EXPERIENCE DEMAND ANALYTICS
# =========================================================

try:

    experience_frequency_df = (
        generate_experience_frequency(df)
    )

    logging.info(
        f"Experience Demand Analytics Generated: "
        f"{len(experience_frequency_df)} levels"
    )

except Exception as e:

    logging.error(
        f"Experience Demand Analytics Error: {e}"
    )
# =========================================================
# JOB ROLE DEMAND ANALYTICS
# =========================================================

try:

    role_frequency_df = (
        generate_role_frequency(df)
    )

    logging.info(
        f"Job Role Demand Analytics Generated: "
        f"{len(role_frequency_df)} categories"
    )

except Exception as e:

    logging.error(
        f"Job Role Demand Analytics Error: {e}"
    )
# =========================================================
# SALARY DEMAND ANALYTICS
# =========================================================

try:

    salary_frequency_df = (
        generate_salary_frequency(df)
    )

    logging.info(
        f"Salary Demand Analytics Generated: "
        f"{len(salary_frequency_df)} buckets"
    )

except Exception as e:

    logging.error(
        f"Salary Demand Analytics Error: {e}"
    )
# =========================================================
# SOURCE AND FIELD QUALITY ANALYTICS
# =========================================================

try:

    source_quality_df = (
        generate_source_quality(df)
    )

    field_quality_df = (
        generate_field_quality(df)
    )

    logging.info(
        f"Source Quality Analytics Generated: "
        f"{len(source_quality_df)} sources"
    )

    logging.info(
        f"Field Quality Analytics Generated: "
        f"{len(field_quality_df)} fields"
    )

except Exception as e:

    logging.error(
        f"Source and Field Quality Analytics Error: {e}"
    )
# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================

df.columns = [

    col.replace(" ", "_")
       .replace("-", "_")
       .replace("(", "")
       .replace(")", "")

    for col in df.columns

]

# =========================================================
# SORT
# =========================================================

df.sort_values(

    by=[

        "Company",

        "Title"

    ],

    inplace=True

)

df.reset_index(

    drop=True,

    inplace=True

)

logging.info("Cleaning Completed.")
# =========================================================
# SAVE CSV
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("SAVING CSV")
logging.info("=" * 60)

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
# SAVE SQLITE DATABASE
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("UPDATING SQLITE DATABASE")
logging.info("=" * 60)

db_path = os.path.join(
    "database",
    "jobs.db"
)

conn = sqlite3.connect(db_path)

df.to_sql(
    "jobs",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()
conn.close()

logging.info("Database Updated Successfully")

# =========================================================
# SUMMARY
# =========================================================

logging.info("")
logging.info("=" * 60)
logging.info("PROJECT SUMMARY")
logging.info("=" * 60)

logging.info(f"Total Raw Jobs      : {len(all_jobs)}")
logging.info(f"Final Clean Jobs    : {len(df)}")
logging.info(f"Unique Companies    : {df['Company'].nunique()}")

if "Source" in df.columns:

    logging.info("")
    logging.info("Jobs by Source")

    source_counts = (
        df["Source"]
        .value_counts()
        .sort_index()
    )

    for source, count in source_counts.items():

        logging.info(
            f"{source:<20} {count}"
        )

if "Job_Category" in df.columns:

    logging.info("")
    logging.info("Jobs by Category")

    category_counts = (
        df["Job_Category"]
        .value_counts()
        .sort_index()
    )

    for category, count in category_counts.items():

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
logging.info("SCRAPING COMPLETED SUCCESSFULLY")
logging.info("=" * 60)

logging.info(f"Execution Time : {elapsed} seconds")
logging.info(f"CSV File       : {csv_path}")
logging.info(f"Database       : {db_path}")

print("\n" + "=" * 60)
print("JOB SCRAPER COMPLETED SUCCESSFULLY")
print("=" * 60)
print(f"Raw Jobs      : {len(all_jobs)}")
print(f"Clean Jobs    : {len(df)}")
print(f"Companies     : {df['Company'].nunique()}")
print(f"CSV           : {csv_path}")
print(f"Database      : {db_path}")
print(f"Time          : {elapsed} seconds")
print("=" * 60)