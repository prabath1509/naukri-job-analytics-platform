# ==========================================================
# scraper/lever_scraper.py
# ==========================================================

import logging
import requests

# Companies that still commonly expose Lever JSON endpoints
COMPANIES = {
    "figma": "Figma",
    "mongodb": "MongoDB",
    "scale-ai": "Scale AI",
    "applydigital": "Apply Digital",
    "brightwheel": "Brightwheel",
    "postscript": "Postscript",
    "sourcegraph": "Sourcegraph",
    "1password": "1Password"
}


def scrape_lever():

    jobs = []

    for slug, company in COMPANIES.items():

        logging.info(f"Scraping Lever: {company}")

        try:

            url = f"https://api.lever.co/v0/postings/{slug}?mode=json"

            response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
            )

            if response.status_code != 200:
                logging.warning(
                    f"{company}: {response.status_code}"
                )
                continue

            data = response.json()

            if not isinstance(data, list):
                continue

            for job in data:

                categories = job.get("categories", {})

                jobs.append({

                    "Title": job.get("text", "Unknown"),

                    "Company": company,

                    "Location": categories.get(
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

            logging.warning(
                f"{company}: {e}"
            )

    logging.info(
        f"Lever Jobs Found: {len(jobs)}"
    )

    return jobs