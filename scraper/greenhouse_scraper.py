# =========================================================
# scraper/greenhouse_scraper.py
# =========================================================

import requests

# =========================================================
# scraper/greenhouse_scraper.py
# DATA ANALYTICS FOCUSED GREENHOUSE SCRAPER
# =========================================================

import requests

DATA_KEYWORDS = [

    "data analyst",
    "business analyst",
    "data scientist",
    "machine learning",
    "analytics",
    "business intelligence",
    "sql",
    "python",
    "power bi",
    "tableau",
    "data engineer",
    "etl",
    "reporting analyst",
    "research analyst",
    "bi analyst",
    "bi developer",
    "data architect"
]


def scrape_greenhouse():

    companies = [
    "databricks",
    "airbnb",
    "stripe",
    "figma",
    "reddit",
    "robinhood",
    "affirm",
    "asana",
    "pinterest",
    "lyft",
    "scaleai",
    "instacart",
    "anthropic",
    "samsara",
    "twilio",
    "brex",
    "coinbase",
    "okta",
    "toast",
    "cloudflare",
    "gusto",
    "discord",
    "dropbox",
    "webflow",
    "squarespace",
]

    jobs = []

    for company in companies:

        try:

            url = (
                f"https://boards-api.greenhouse.io/v1/boards/"
                f"{company}/jobs"
            )

            response = requests.get(
                url,
                timeout=30
            )

            data = response.json()

            for job in data.get("jobs", []):

                title = job.get(
                    "title",
                    "Unknown"
                )

                title_lower = title.lower()

                # =====================================
                # DATA ANALYTICS FILTER
                # =====================================

                if not any(
                    keyword in title_lower
                    for keyword in DATA_KEYWORDS
                ):
                    continue

                jobs.append({

                    "Title": title,

                    "Company": company.title(),

                    "Location": job.get(
                        "location",
                        {}
                    ).get(
                        "name",
                        "Remote"
                    ),

                    "Experience": "Not Available",

                    "Salary": "Not Available",

                    "Skills": [],

                    "Keyword": "Data Analytics",

                    "Source": "Greenhouse",

                    "Posted_Date": "Recent",

                    "Job_Link": job.get(
                        "absolute_url",
                        ""
                    )
                })

        except Exception as e:

            print(
                f"Greenhouse Error ({company}): {e}"
            )

    print(
        f"Greenhouse Jobs Found: {len(jobs)}"
    )

    return jobs