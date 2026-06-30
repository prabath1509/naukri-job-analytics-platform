import requests
import logging


WORKDAY_COMPANIES = [
    {
        "company": "NVIDIA",
        "url": "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/ExternalCareerSite/jobs"
    },
    {
        "company": "Mastercard",
        "url": "https://mastercard.wd1.myworkdayjobs.com/wday/cxs/mastercard/CorporateCareers/jobs"
    },
    {
        "company": "GE Aerospace",
        "url": "https://geaerospace.wd5.myworkdayjobs.com/wday/cxs/geaerospace/External/jobs"
    }
]


def scrape_workday():

    jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for company in WORKDAY_COMPANIES:

        try:

            logging.info(f"Scraping Workday: {company['company']}")

            offset = 0

            while True:

                payload = {
                    "limit": 20,
                    "offset": offset,
                    "searchText": ""
                }

                response = requests.post(
                    company["url"],
                    json=payload,
                    headers=headers,
                    timeout=60
                )

                if response.status_code != 200:
                    break

                data = response.json()

                results = data.get("jobPostings", [])

                if not results:
                    break

                for job in results:

                    jobs.append({

                        "Title": job.get("title", ""),

                        "Company": company["company"],

                        "Location": job.get("locationsText", ""),

                        "Experience": "Not Available",

                        "Salary": "Not Available",

                        "Skills": [],

                        "Keyword": job.get("title", ""),

                        "Source": "Workday",

                        "Posted_Date": job.get("postedOn", ""),

                        "Job_Link": (
                            company["url"]
                            + "/job/"
                            + job.get("externalPath", "")
                        )

                    })

                offset += 20

        except Exception as e:

            logging.error(f"{company['company']} : {e}")

    logging.info(f"Workday Jobs Found: {len(jobs)}")

    return jobs