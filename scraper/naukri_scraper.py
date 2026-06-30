# =========================================================
# scraper/naukri_scraper.py
# =========================================================

import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# =========================================================
# CONFIGURATION
# =========================================================

MAX_RETRIES = 3

# =========================================================
# CREATE CHROME DRIVER
# =========================================================

def create_driver():

    options = Options()

    # Headless Chrome
    #options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument("--log-level=3")

    options.add_experimental_option(

        "excludeSwitches",

        ["enable-automation"]

    )

    options.add_experimental_option(

        "useAutomationExtension",

        False

    )

    driver = webdriver.Chrome(

        service=Service(

            ChromeDriverManager().install()

        ),

        options=options

    )

    driver.set_page_load_timeout(60)

    driver.maximize_window()

    return driver

# =========================================================
# PAGE SCROLL
# =========================================================

def scroll_page(driver):

    driver.execute_script(

        "window.scrollTo(0, document.body.scrollHeight);"

    )

    time.sleep(

        random.uniform(1.5,3)

    )

    driver.execute_script(

        "window.scrollTo(0,0);"

    )

    time.sleep(

        random.uniform(1,2)

    )
# =========================================================
# SCRAPE NAUKRI JOBS
# =========================================================

def scrape_naukri_jobs(keyword, pages=10):

    jobs = []

    seen_links = set()

    driver = None

    try:

        logging.info("=" * 60)
        logging.info(f"Keyword : {keyword}")
        logging.info("=" * 60)

        driver = create_driver()

        wait = WebDriverWait(driver, 20)

        # =================================================
        # LOOP PAGES
        # =================================================

        for page in range(1, pages + 1):

            success = False

            # =============================================
            # RETRY FAILED PAGE
            # =============================================

            for attempt in range(MAX_RETRIES):

                try:

                    url = (
                        f"https://www.naukri.com/"
                        f"{keyword}-jobs-{page}"
                    )

                    logging.info(
                        f"Opening Page {page}"
                    )

                    driver.get(url)

                    time.sleep(10)

                    driver.save_screenshot(f"page_{page}.png")

                    with open(f"page_{page}.html","w",encoding="utf-8") as f:
                        f.write(driver.page_source)

                    scroll_page(driver)

                    wait.until(

                        EC.presence_of_element_located(

                            (
                                By.CSS_SELECTOR,
                                "div.srp-jobtuple-wrapper"
                            )

                        )

                    )

                    cards = driver.find_elements(

                        By.CSS_SELECTOR,

                        "div.srp-jobtuple-wrapper"

                    )

                    if len(cards) == 0:

                        logging.warning(

                            f"No jobs on page {page}"

                        )

                        break

                    logging.info(

                        f"Page {page} : {len(cards)} jobs"

                    )

                    success = True

                    break

                except Exception as e:

                    logging.warning(

                        f"Retry {attempt+1}/{MAX_RETRIES}"

                    )

                    logging.warning(str(e))

                    time.sleep(

                        random.uniform(2,5)

                    )

            if not success:

                logging.warning(

                    f"Skipping page {page}"

                )

                continue

            # =============================================
            # LOOP JOB CARDS
            # =============================================

            for card in cards:
                                # ==========================================
                # TITLE
                # ==========================================

                try:

                    title = card.find_element(

                        By.CSS_SELECTOR,

                        "a.title"

                    ).text.strip()

                except:

                    title = "Unknown"

                # ==========================================
                # COMPANY
                # ==========================================

                try:

                    company = card.find_element(

                        By.CSS_SELECTOR,

                        "a.comp-name"

                    ).text.strip()

                except:

                    company = "Unknown"

                # ==========================================
                # LOCATION
                # ==========================================

                try:

                    location = card.find_element(

                        By.CSS_SELECTOR,

                        "span.locWdth"

                    ).text.strip()

                except:

                    location = "Unknown"

                # ==========================================
                # EXPERIENCE
                # ==========================================

                try:

                    experience = card.find_element(

                        By.CSS_SELECTOR,

                        "span.expwdth"

                    ).text.strip()

                except:

                    experience = "Not Available"

                # ==========================================
                # SALARY
                # ==========================================

                try:

                    salary = card.find_element(

                        By.CSS_SELECTOR,

                        "span.sal"

                    ).text.strip()

                except:

                    salary = "Not Available"

                # ==========================================
                # SKILLS
                # ==========================================

                skills = []

                try:

                    skill_elements = card.find_elements(

                        By.CSS_SELECTOR,

                        "ul.tags-gt li"

                    )

                    for skill in skill_elements:

                        text = skill.text.strip()

                        if text:

                            skills.append(text)

                except:

                    pass

                # ==========================================
                # JOB LINK
                # ==========================================

                try:

                    job_link = card.find_element(

                        By.CSS_SELECTOR,

                        "a.title"

                    ).get_attribute("href")

                except:

                    job_link = ""

                # ==========================================
                # REMOVE DUPLICATES
                # ==========================================

                if job_link in seen_links:

                    continue

                seen_links.add(job_link)

                # ==========================================
                # POSTED DATE
                # ==========================================

                try:

                    posted_date = card.find_element(

                        By.CSS_SELECTOR,

                        "span.job-post-day"

                    ).text.strip()

                except:

                    posted_date = "Recent"

                # ==========================================
                # KEYWORD
                # ==========================================

                keyword_name = keyword.replace(

                    "-",

                    " "

                ).title()

                # ==========================================
                # SAVE JOB
                # ==========================================

                jobs.append({

                    "Title": title,

                    "Company": company,

                    "Location": location,

                    "Experience": experience,

                    "Salary": salary,

                    "Skills": skills,

                    "Keyword": keyword_name,

                    "Source": "Naukri",

                    "Posted_Date": posted_date,

                    "Job_Link": job_link

                })

            logging.info(

                f"Collected {len(jobs)} jobs so far."

            )
                    # =================================================
        # END PAGE LOOP
        # =================================================

        logging.info("")
        logging.info("=" * 60)
        logging.info(
            f"{keyword} Completed"
        )
        logging.info(
            f"Total Jobs : {len(jobs)}"
        )
        logging.info("=" * 60)

    except Exception as e:

        logging.error(
            f"Fatal Error ({keyword}) : {e}"
        )

    finally:

        # =============================================
        # CLOSE BROWSER
        # =============================================

        if driver:

            try:

                driver.quit()

                logging.info(
                    "Chrome Driver Closed"
                )

            except Exception:

                pass

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique_jobs = []

    seen = set()

    for job in jobs:

        key = (

            job["Title"],

            job["Company"],

            job["Location"]

        )

        if key not in seen:

            seen.add(key)

            unique_jobs.append(job)

    logging.info("")
    logging.info("=" * 60)
    logging.info(
        f"Keyword          : {keyword}"
    )
    logging.info(
        f"Jobs Collected   : {len(jobs)}"
    )
    logging.info(
        f"Unique Jobs      : {len(unique_jobs)}"
    )
    logging.info("=" * 60)

    return unique_jobs