import requests
import pandas as pd

from scraper.utils import clean_text

# -----------------------------------
# LEVER SCRAPER
# -----------------------------------

def scrape_lever(company_name):

    url = (
        f"https://api.lever.co/v0/postings/"
        f"{company_name}"
    )

    response = requests.get(url)

    if response.status_code != 200:

        return pd.DataFrame()

    data = response.json()

    jobs = []

    for job in data:

        jobs.append({

            "Source": "Lever",

            "Keyword": "Official Company Jobs",

            "Title": clean_text(
                job.get("text")
            ),

            "Company": company_name.title(),

            "Experience": "Not Available",

            "Location": clean_text(
                job.get(
                    "categories",
                    {}
                ).get("location")
            ),

            "Salary": "Not Available",

            "Skills": "Not Available",

            "Posted_Date": "Not Available",

            "Job_Link": clean_text(
                job.get("hostedUrl")
            )
        })

    return pd.DataFrame(jobs)