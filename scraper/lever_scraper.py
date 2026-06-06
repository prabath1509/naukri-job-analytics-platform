# =========================================================
# scraper/lever_scraper.py
# =========================================================

import requests

# =========================================================
# LEVER SCRAPER
# =========================================================

def scrape_lever():

    companies = [

        "netflix",

        "coinbase",

        "discord",

        "udemy",

        "brex",

        "canva",

        "ramp",

        "rippling"
    ]

    jobs = []

    for company in companies:

        try:

            url = (
                f"https://api.lever.co/v0/postings/"
                f"{company}?mode=json"
            )

            response = requests.get(url)

            data = response.json()

            for job in data:

                jobs.append({

                    "Title": job.get(
                        "text",
                        "Unknown"
                    ),

                    "Company": company.title(),

                    "Location": job.get(
                        "categories",
                        {}
                    ).get(
                        "location",
                        "Remote"
                    ),

                    "Experience": "Not Available",

                    "Salary": "Not Available",

                    "Skills": [],

                    "Keyword": job.get(
                        "text",
                        ""
                    ),

                    "Source": "Lever",

                    "Posted_Date": "Recent",

                    "Job_Link": job.get(
                        "hostedUrl",
                        ""
                    )
                })

        except Exception as e:

            print(
                f"{company} Error: {e}"
            )

    return jobs