import logging
import time

import requests


WORKDAY_COMPANIES = [
    {
        "company": "Mastercard",
        "url": "https://mastercard.wd1.myworkdayjobs.com/wday/cxs/mastercard/CorporateCareers/jobs",
    },
    {
        "company": "Salesforce",
        "url": "https://salesforce.wd12.myworkdayjobs.com/wday/cxs/salesforce/External_Career_Site/jobs",
    },
    {
        "company": "Adobe",
        "url": "https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/external_experienced/jobs",
    },
    {
        "company": "Intel",
        "url": "https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs",
    },
    {
        "company": "PayPal",
        "url": "https://paypal.wd1.myworkdayjobs.com/wday/cxs/paypal/jobs/jobs",
    },
    {
        "company": "Autodesk",
        "url": "https://autodesk.wd1.myworkdayjobs.com/wday/cxs/autodesk/Ext/jobs",
    },
]


PAGE_SIZE = 20
MAX_PAGES = 100
REQUEST_TIMEOUT = 30


def scrape_workday():

    jobs = []

    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    })

    for company in WORKDAY_COMPANIES:

        company_name = company["company"]
        url = company["url"]

        logging.info(f"Scraping Workday: {company_name}")

        company_jobs = []
        seen_paths = set()

        try:

            offset = 0
            page = 1
            total = None

            while page <= MAX_PAGES:

                payload = {
                    "limit": PAGE_SIZE,
                    "offset": offset,
                    "searchText": "",
                }

                started = time.time()

                response = session.post(
                    url,
                    json=payload,
                    timeout=REQUEST_TIMEOUT,
                )

                elapsed = time.time() - started

                logging.info(
                    f"{company_name} | Page {page} | "
                    f"Offset {offset} | Status {response.status_code} | "
                    f"{elapsed:.2f}s"
                )

                if response.status_code != 200:

                    logging.warning(
                        f"{company_name}: HTTP {response.status_code}"
                    )

                    break

                data = response.json()

                results = data.get("jobPostings", [])

                if total is None:

                    total = data.get("total")

                    logging.info(
                        f"{company_name}: Workday total = {total}"
                    )

                if not results:

                    logging.info(
                        f"{company_name}: empty page reached"
                    )

                    break

                new_jobs = 0

                for job in results:

                    external_path = str(
                        job.get("externalPath", "")
                    ).strip()

                    if not external_path:
                        continue

                    if external_path in seen_paths:
                        continue

                    seen_paths.add(external_path)

                    job_link = (
                        url.split("/wday/cxs/")[0]
                        + external_path
                    )

                    company_jobs.append({
                        "Title": job.get("title", ""),
                        "Company": company_name,
                        "Location": job.get("locationsText", ""),
                        "Experience": "Not Available",
                        "Salary": "Not Available",
                        "Skills": [],
                        "Keyword": job.get("title", ""),
                        "Source": "Workday",
                        "Posted_Date": job.get("postedOn", ""),
                        "Job_Link": job_link,
                    })

                    new_jobs += 1

                logging.info(
                    f"{company_name} | Page jobs: {len(results)} | "
                    f"New jobs: {new_jobs} | "
                    f"Collected: {len(company_jobs)}"
                )

                if new_jobs == 0:

                    logging.warning(
                        f"{company_name}: no new jobs; "
                        f"stopping pagination"
                    )

                    break

                offset += len(results)
                page += 1

                if total is not None and offset >= int(total):

                    logging.info(
                        f"{company_name}: reached Workday total {total}"
                    )

                    break

        except requests.Timeout:

            logging.error(
                f"{company_name}: request timed out"
            )

        except requests.RequestException as exc:

            logging.error(
                f"{company_name}: request failed: {exc}"
            )

        except Exception as exc:

            logging.exception(
                f"{company_name}: unexpected error: {exc}"
            )

        logging.info(
            f"{company_name}: {len(company_jobs)} unique jobs"
        )

        jobs.extend(company_jobs)

    session.close()

    logging.info(
        f"Workday Jobs Found: {len(jobs)}"
    )

    return jobs