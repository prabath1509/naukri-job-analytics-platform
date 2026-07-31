import sqlite3
import time

import pandas as pd

from scraper.analytics_relevance import is_analytics_relevant
from scraper.naukri_scraper import scrape_naukri_jobs


TEST_KEYWORDS = [
    "bi-developer",
    "analytics-engineer",
]


conn = sqlite3.connect("database/jobs.db")
production = pd.read_sql(
    "SELECT Job_Link FROM jobs",
    conn,
)
conn.close()

production_links = {
    link
    for link in production["Job_Link"].dropna()
    if str(link).strip()
}

print("PHASE 56 KEYWORD IMPACT AUDIT")
print("=" * 100)

summary = []

total_new = 0

for keyword in TEST_KEYWORDS:

    print()
    print("=" * 100)
    print("KEYWORD:", keyword)
    print("=" * 100)

    start = time.time()

    jobs = scrape_naukri_jobs(
        keyword,
        pages=20,
    )

    relevant = [
        job
        for job in jobs
        if is_analytics_relevant(
            job.get("Title", "")
        )
    ]

    links = {
        job.get("Job_Link")
        for job in relevant
        if job.get("Job_Link")
    }

    new_links = (
        links
        - production_links
    )

    duplicate_links = (
        links
        & production_links
    )

    elapsed = time.time() - start

    total_new += len(new_links)

    summary.append(
        (
            keyword,
            len(jobs),
            len(relevant),
            len(links),
            len(new_links),
            len(duplicate_links),
            elapsed,
        )
    )

    print(f"RAW JOBS           : {len(jobs)}")
    print(f"RELEVANT JOBS      : {len(relevant)}")
    print(f"UNIQUE LINKS       : {len(links)}")
    print(f"NEW UNIQUE LINKS   : {len(new_links)}")
    print(f"DUPLICATE LINKS    : {len(duplicate_links)}")
    print(f"TIME               : {elapsed:.2f}s")

print()
print("=" * 100)
print("PHASE 56 SUMMARY")
print("=" * 100)

for (
    keyword,
    raw,
    relevant,
    unique,
    new,
    duplicate,
    elapsed,
) in summary:

    decision = (
        "KEEP"
        if new >= 20
        else "REMOVE"
    )

    print(
        f"{keyword:<22}"
        f"RAW:{raw:<5}"
        f"REL:{relevant:<5}"
        f"NEW:{new:<5}"
        f"DUP:{duplicate:<5}"
        f"DECISION:{decision}"
    )

print()
print("TOTAL NEW UNIQUE JOBS:", total_new)