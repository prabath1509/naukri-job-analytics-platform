# =========================================================
# scraper/naukri_scraper.py
# ULTRA STABLE NAUKRI SCRAPER
# =========================================================

import time

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager


# =========================================================
# CREATE DRIVER
# =========================================================

def create_driver():

    options = Options()

    options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")

    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument(
        "user-agent=Mozilla/5.0"
    )

    driver = webdriver.Chrome(

        service=Service(
            ChromeDriverManager().install()
        ),

        options=options
    )

    return driver


# =========================================================
# SCRAPER
# =========================================================

def scrape_naukri_jobs(keyword, pages=10):

    jobs = []

    # =====================================================
    # LOOP PAGES
    # =====================================================

    for page in range(1, pages + 1):

        driver = None

        try:

            # =============================================
            # NEW DRIVER EVERY PAGE
            # =============================================

            driver = create_driver()

            wait = WebDriverWait(driver, 15)

            url = (
                f"https://www.naukri.com/"
                f"{keyword}-jobs-{page}"
            )

            print(f"\nOpening: {url}")

            driver.get(url)

            time.sleep(4)

            # =============================================
            # WAIT FOR JOBS
            # =============================================

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

            print(f"Found {len(cards)} jobs")

            # =============================================
            # LOOP CARDS
            # =============================================

            for card in cards:

                try:

                    title = card.find_element(

                        By.CSS_SELECTOR,
                        "a.title"
                    ).text.strip()

                except:

                    title = "Unknown"

                try:

                    company = card.find_element(

                        By.CSS_SELECTOR,
                        "a.comp-name"
                    ).text.strip()

                except:

                    company = "Unknown"

                try:

                    location = card.find_element(

                        By.CSS_SELECTOR,
                        "span.locWdth"
                    ).text.strip()

                except:

                    location = "Unknown"

                try:

                    experience = card.find_element(

                        By.CSS_SELECTOR,
                        "span.expwdth"
                    ).text.strip()

                except:

                    experience = "Not Available"

                try:

                    salary = card.find_element(

                        By.CSS_SELECTOR,
                        "span.sal"
                    ).text.strip()

                except:

                    salary = "Not Available"

                # =========================================
                # SKILLS
                # =========================================

                skills = []

                try:

                    skill_elements = card.find_elements(

                        By.CSS_SELECTOR,
                        "ul.tags-gt li"
                    )

                    skills = [

                        s.text.strip()

                        for s in skill_elements

                        if s.text.strip() != ""
                    ]

                except:

                    pass

                # =========================================
                # LINK
                # =========================================

                try:

                    link = card.find_element(

                        By.CSS_SELECTOR,
                        "a.title"
                    ).get_attribute("href")

                except:

                    link = ""

                # =========================================
                # POSTED DATE
                # =========================================

                try:

                    posted = card.find_element(

                        By.CSS_SELECTOR,
                        "span.job-post-day"
                    ).text.strip()

                except:

                    posted = "Recent"

                # =========================================
                # SAVE
                # =========================================

                jobs.append({

                    "Title": title,

                    "Company": company,

                    "Location": location,

                    "Experience": experience,

                    "Salary": salary,

                    "Skills": skills,

                    "Keyword": keyword,

                    "Source": "Naukri",

                    "Posted_Date": posted,

                    "Job_Link": link
                })

        except Exception as e:

            print(f"Page {page} Error: {e}")

        finally:

            # =============================================
            # CLOSE DRIVER EVERY PAGE
            # =============================================

            try:

                if driver:

                    driver.quit()

            except:

                pass

        # =================================================
        # SMALL DELAY
        # =================================================

        time.sleep(2)

    return jobs