# -----------------------------------
# IMPORTS
# -----------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException
)

from webdriver_manager.chrome import ChromeDriverManager

from scraper.greenhouse_scraper import (
    scrape_greenhouse
)

from scraper.lever_scraper import (
    scrape_lever
)

from scraper.utils import (
    clean_text,
    create_job_key
)

import pandas as pd
import sqlite3
import logging
import time
import random

from datetime import datetime

# -----------------------------------
# LOGGING
# -----------------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------
# CREATE DRIVER
# -----------------------------------

def create_driver():

    options = webdriver.ChromeOptions()

    # -----------------------------------
    # IMPORTANT
    # KEEP HEADLESS DISABLED
    # -----------------------------------

    # options.add_argument("--headless=new")

    options.add_argument("--start-maximized")

    options.add_argument("--disable-gpu")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    # -----------------------------------
    # USER AGENT
    # -----------------------------------

    options.add_argument(

        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )

    # -----------------------------------
    # REMOVE AUTOMATION FLAGS
    # -----------------------------------

    options.add_experimental_option(

        "excludeSwitches",

        ["enable-automation"]
    )

    options.add_experimental_option(

        "useAutomationExtension",

        False
    )

    # -----------------------------------
    # DRIVER
    # -----------------------------------

    driver = webdriver.Chrome(

        service=Service(
            ChromeDriverManager().install()
        ),

        options=options
    )

    driver.set_page_load_timeout(40)

    return driver

# -----------------------------------
# DRIVER
# -----------------------------------

driver = create_driver()

# -----------------------------------
# KEYWORDS
# -----------------------------------

keywords = [

    "data-analyst",

    "business-analyst",

    "data-scientist",

    "python-developer",

    "data-engineer",

    "machine-learning-engineer",

    "ai-engineer",

    "sql-developer",

    "power-bi-developer",

    "tableau-developer",

    "etl-developer",

    "business-intelligence",

    "financial-analyst",

    "research-analyst",

    "product-analyst",

    "cloud-data-engineer",

    "analytics-manager",

    "deep-learning-engineer",

    "nlp-engineer"
]

# -----------------------------------
# NUMBER OF PAGES
# -----------------------------------

pages = 10

# -----------------------------------
# STORAGE
# -----------------------------------

all_jobs = []

# -----------------------------------
# GREENHOUSE COMPANIES
# -----------------------------------

greenhouse_companies = [

    "stripe",
    "notion",
    "databricks",
    "canva",
    "airbnb",
    "discord",
    "reddit",
    "figma",
    "hubspot",
    "shopify",
    "affirm",
    "brex",
    "doordash",
    "snowflake",
    "asana",
    "instacart",
    "openai",
    "robinhood",
    "flexport",
    "coinbase"
]

# -----------------------------------
# LEVER COMPANIES
# -----------------------------------

lever_companies = [

    "netflix",
    "coinbase",
    "udemy",
    "postman",
    "zapier",
    "rippling",
    "scale-ai",
    "miro",
    "eventbrite",
    "benchling",
    "coursera",
    "verkada",
    "lucid",
    "modern-treasury",
    "clearco"
]

# -----------------------------------
# NAUKRI SCRAPING
# -----------------------------------

for keyword in keywords:

    logging.info(
        f"Starting Keyword: {keyword}"
    )

    for page in range(1, pages + 1):

        try:

            # -----------------------------------
            # RESTART DRIVER
            # -----------------------------------

            if page % 3 == 0:

                try:
                    driver.quit()
                except:
                    pass

                time.sleep(3)

                driver = create_driver()

                logging.info(
                    "Driver Restarted"
                )

            # -----------------------------------
            # URL
            # -----------------------------------

            url = (

                f"https://www.naukri.com/"
                f"{keyword}-jobs-{page}"
            )

            logging.info(
                f"Opening {url}"
            )

            driver.get(url)

            # -----------------------------------
            # WAIT
            # -----------------------------------

            WebDriverWait(driver, 20).until(

                EC.presence_of_element_located(

                    (
                        By.CSS_SELECTOR,
                        "div.cust-job-tuple"
                    )
                )
            )

            # -----------------------------------
            # SCROLL
            # -----------------------------------

            driver.execute_script(

                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(
                random.uniform(2, 4)
            )

            # -----------------------------------
            # GET JOBS
            # -----------------------------------

            jobs = driver.find_elements(

                By.CSS_SELECTOR,

                "div.cust-job-tuple"
            )

            logging.info(
                f"Jobs Found: {len(jobs)}"
            )

            # -----------------------------------
            # HUMAN DELAY
            # -----------------------------------

            time.sleep(
                random.uniform(6, 12)
            )

            # -----------------------------------
            # JOB LOOP
            # -----------------------------------

            for job in jobs:

                try:

                    title = clean_text(

                        job.find_element(

                            By.CSS_SELECTOR,

                            "a.title"
                        ).text
                    )

                except:

                    title = "Not Available"

                try:

                    company = clean_text(

                        job.find_element(

                            By.CLASS_NAME,

                            "comp-name"
                        ).text
                    )

                except:

                    company = "Not Available"

                try:

                    experience = clean_text(

                        job.find_element(

                            By.CLASS_NAME,

                            "expwdth"
                        ).text
                    )

                except:

                    experience = "Not Available"

                try:

                    location = clean_text(

                        job.find_element(

                            By.CLASS_NAME,

                            "locWdth"
                        ).text
                    )

                except:

                    location = "Not Available"

                try:

                    salary = clean_text(

                        job.find_element(

                            By.CLASS_NAME,

                            "sal-wrap"
                        ).text
                    )

                except:

                    salary = "Not Available"

                try:

                    skills = clean_text(

                        job.find_element(

                            By.CLASS_NAME,

                            "tags-gt"
                        ).text
                    )

                except:

                    skills = "Not Available"

                try:

                    posted_date = clean_text(

                        job.find_element(

                            By.CLASS_NAME,

                            "job-post-day"
                        ).text
                    )

                except:

                    posted_date = "Not Available"

                try:

                    job_link = (

                        job.find_element(

                            By.CSS_SELECTOR,

                            "a.title"
                        ).get_attribute("href")
                    )

                except:

                    job_link = "Not Available"

                # -----------------------------------
                # STORE
                # -----------------------------------

                all_jobs.append({

                    "Source": "Naukri",

                    "Keyword": keyword,

                    "Title": title,

                    "Company": company,

                    "Experience": experience,

                    "Location": location,

                    "Salary": salary,

                    "Skills": skills,

                    "Posted_Date": posted_date,

                    "Job_Link": job_link
                })

            logging.info(
                f"Page {page} Completed"
            )

        except (

            TimeoutException,

            WebDriverException,

            Exception

        ) as e:

            logging.error(
                f"Page {page} Error: {e}"
            )

            try:
                driver.quit()
            except:
                pass

            time.sleep(5)

            driver = create_driver()

            continue

# -----------------------------------
# CLOSE DRIVER
# -----------------------------------

try:
    driver.quit()
except:
    pass

# -----------------------------------
# CREATE DATAFRAME
# -----------------------------------

naukri_df = pd.DataFrame(all_jobs)

logging.info(
    f"Naukri Jobs: {len(naukri_df)}"
)

# -----------------------------------
# GREENHOUSE JOBS
# -----------------------------------

greenhouse_jobs = []

for company in greenhouse_companies:

    try:

        temp_df = scrape_greenhouse(company)

        greenhouse_jobs.append(temp_df)

        logging.info(
            f"Greenhouse Scraped: {company}"
        )

    except Exception as e:

        logging.error(
            f"Greenhouse Error: {e}"
        )

# -----------------------------------
# LEVER JOBS
# -----------------------------------

lever_jobs = []

for company in lever_companies:

    try:

        temp_df = scrape_lever(company)

        lever_jobs.append(temp_df)

        logging.info(
            f"Lever Scraped: {company}"
        )

    except Exception as e:

        logging.error(
            f"Lever Error: {e}"
        )

# -----------------------------------
# COMBINE ALL DATA
# -----------------------------------

all_dfs = [naukri_df]

if greenhouse_jobs:
    all_dfs.extend(greenhouse_jobs)

if lever_jobs:
    all_dfs.extend(lever_jobs)

df = pd.concat(

    all_dfs,

    ignore_index=True
)

# -----------------------------------
# REMOVE EMPTY TITLES
# -----------------------------------

df = df[
    df["Title"] != "Not Available"
]

# -----------------------------------
# CREATE UNIQUE KEY
# -----------------------------------

df["job_key"] = df.apply(

    create_job_key,

    axis=1
)

# -----------------------------------
# REMOVE DUPLICATES
# -----------------------------------

df.drop_duplicates(

    subset=["job_key"],

    inplace=True
)

# -----------------------------------
# DATABASE
# -----------------------------------

db_path = (

    r"C:\Users\PRABATH\OneDrive\Desktop"
    r"\naukri_scraper_project"
    r"\database\jobs.db"
)

conn = sqlite3.connect(db_path)

# -----------------------------------
# LOAD EXISTING DATA
# -----------------------------------

try:

    existing_df = pd.read_sql(

        "SELECT * FROM jobs",

        conn
    )

    combined_df = pd.concat(

        [existing_df, df],

        ignore_index=True
    )

    combined_df["job_key"] = combined_df.apply(

        create_job_key,

        axis=1
    )

    combined_df.drop_duplicates(

        subset=["job_key"],

        inplace=True
    )

    combined_df.drop(

        columns=["job_key"],

        inplace=True
    )

    df = combined_df

except:

    pass

# -----------------------------------
# FINAL CLEANUP
# -----------------------------------

if "job_key" in df.columns:

    df.drop(

        columns=["job_key"],

        inplace=True
    )

# -----------------------------------
# SAVE DATABASE
# -----------------------------------

df.to_sql(

    "jobs",

    conn,

    if_exists="replace",

    index=False
)

conn.close()

logging.info(
    "Database Saved"
)

# -----------------------------------
# SAVE CSV
# -----------------------------------

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

csv_path = (

    rf"C:\Users\PRABATH\OneDrive\Desktop"
    rf"\naukri_scraper_project\data"
    rf"\jobs_{timestamp}.csv"
)

df.to_csv(

    csv_path,

    index=False
)

logging.info(
    f"CSV Saved: {csv_path}"
)

# -----------------------------------
# FINAL OUTPUT
# -----------------------------------

print("\nSCRAPING COMPLETED")

print(f"\nTOTAL JOBS IN DATABASE: {len(df)}")

print(df.head())