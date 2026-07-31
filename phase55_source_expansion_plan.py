import sqlite3
import pandas as pd

TARGET_JOBS = 10000

conn = sqlite3.connect("database/jobs.db")
df = pd.read_sql("SELECT * FROM jobs", conn)
conn.close()

current_jobs = len(df)

source_counts = (
    df["Source"]
    .value_counts()
    .sort_values(ascending=False)
)

print("PHASE 55 SOURCE EXPANSION PLAN")
print("=" * 80)

print("CURRENT JOBS :", current_jobs)
print("TARGET JOBS  :", TARGET_JOBS)
print("JOB GAP      :", TARGET_JOBS - current_jobs)

print()
print("CURRENT SOURCES")
print("=" * 80)

for source, count in source_counts.items():

    print(
        f"{source:<20}"
        f"JOBS:{count:<6}"
        f"SHARE:{count/current_jobs*100:6.2f}%"
    )

print()
print("=" * 80)
print("ESTIMATED EXPANSION OPPORTUNITIES")
print("=" * 80)

expansion = [
    ("Expand Naukri keywords", 1500),
    ("Add verified ATS source #4", 800),
    ("Add verified ATS source #5", 700),
    ("Increase Workday companies", 500),
    ("Increase Greenhouse boards", 400),
    ("Improve Naukri pagination", 700),
    ("Improve duplicate recovery", 300),
]

running_total = current_jobs

for name, gain in expansion:

    running_total += gain

    print(
        f"{name:<35}"
        f"+{gain:<5}"
        f"Projected:{running_total}"
    )

print()
print("=" * 80)

if running_total >= TARGET_JOBS:
    print("TARGET APPEARS ACHIEVABLE")
else:
    print("ADDITIONAL SOURCES REQUIRED")