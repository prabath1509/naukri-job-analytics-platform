import requests
import pandas as pd

from scraper.utils import clean_text

# -----------------------------------
# GREENHOUSE SCRAPER
# -----------------------------------

def scrape_greenhouse(company_name):

    url = (
        f"https://boards-api.greenhouse.io/v1/boards/"
        f"{company_name}/jobs"
    )

    response = requests.get(url)

    if response.status_code != 200:

        return pd.DataFrame()

    data = response.json()

    jobs = []

    for job in data.get("jobs", []):

        jobs.append({

            "Source": "Greenhouse",

            "Keyword": "Official Company Jobs",

            "Title": clean_text(
                job.get("title")
            ),

            "Company": company_name.title(),

            "Experience": "Not Available",

            "Location": clean_text(
                job.get(
                    "location",
                    {}
                ).get("name")
            ),

            "Salary": "Not Available",

            "Skills": "Not Available",

            "Posted_Date": clean_text(
                job.get("updated_at")
            ),

            "Job_Link": clean_text(
                job.get("absolute_url")
            )
        })

    return pd.DataFrame(jobs)