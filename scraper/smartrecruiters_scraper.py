# =========================================================
# scraper/smartrecruiters_scraper.py
# =========================================================

import requests
import logging
from scraper.ats_source_registry import (SMARTRECRUITERS_COMPANIES,)

def scrape_smartrecruiters():

    jobs = []

    headers = {

        "User-Agent": "Mozilla/5.0"

    }

    for company in SMARTRECRUITERS_COMPANIES:

        try:

            logging.info(

                f"Scraping SmartRecruiters: {company}"

            )

            offset = 0

            while True:

                url = (

                    f"https://api.smartrecruiters.com/v1/companies/"
                    f"{company}/postings"
                    f"?limit=100&offset={offset}"

                )

                response = requests.get(

                    url,

                    headers=headers,

                    timeout=60

                )

                if response.status_code != 200:

                    break

                data = response.json()

                postings = data.get(

                    "content",

                    []

                )

                if len(postings) == 0:

                    break

                for job in postings:

                    jobs.append({

                        "Title":

                            job.get("name", ""),

                        "Company":

                            company.title(),

                        "Location":

                            job.get("location", {}).get(

                                "city",

                                "Unknown"

                            ),

                        "Experience":

                            "Not Available",

                        "Salary":

                            "Not Available",

                        "Skills":

                            [],

                        "Keyword":

                            job.get(

                                "name",

                                ""

                            ),

                        "Source":

                            "SmartRecruiters",

                        "Posted_Date":

                            job.get(

                                "releasedDate",

                                ""

                            ),

                        "Job_Link":

                            "https://jobs.smartrecruiters.com/"

                            + company

                            + "/"

                            + job.get(

                                "id",

                                ""

                            )

                    })

                offset += 100

        except Exception as e:

            logging.error(

                f"{company}: {e}"

            )

    logging.info(

        f"SmartRecruiters Jobs Found: {len(jobs)}"

    )

    return jobs