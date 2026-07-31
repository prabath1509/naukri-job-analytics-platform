import sqlite3
import pandas as pd

conn = sqlite3.connect("database/jobs.db")
df = pd.read_sql("SELECT Title FROM jobs", conn)
conn.close()

titles = (
    df["Title"]
    .fillna("")
    .str.lower()
)

CURRENT_KEYWORDS = {
    "data analyst",
    "business analyst",
    "research analyst",
    "data scientist",
    "machine learning",
    "data engineer",
    "business intelligence",
    "power bi",
    "tableau",
    "sql",
    "python",
    "business-intelligence",
    "bi-developer",
    "analytics-engineer",
    "etl",
}

CANDIDATE_KEYWORDS = [
    "mis analyst",
    "reporting analyst",
    "bi developer",
    "analytics engineer",
    "decision scientist",
    "data analytics",
    "data governance",
    "data quality",
    "master data",
    "information analyst",
    "commercial analyst",
    "pricing analyst",
    "marketing analyst",
    "product analyst",
    "risk analyst",
    "credit analyst",
    "operations analyst",
    "fp&a",
    "financial analyst",
    "customer insights",
    "business intelligence developer",
    "visualization",
    "business-intelligence",
    "bi-developer",
    "analytics-engineer",
    "etl",
]

print("PHASE 55 KEYWORD GAP AUDIT")
print("=" * 90)

results = []

for keyword in CANDIDATE_KEYWORDS:

    count = titles.str.contains(
        keyword,
        regex=False,
    ).sum()

    results.append((keyword, int(count)))

results.sort(
    key=lambda x: x[1],
    reverse=True,
)

print(f"{'Keyword':35} {'Existing Jobs':>15}")
print("-" * 90)

for keyword, count in results:

    print(f"{keyword:35} {count:15}")

print()
print("=" * 90)

recommended = [
    x
    for x in results
    if x[1] >= 20
]

print("HIGH PRIORITY KEYWORDS")
print("-" * 90)

for keyword, count in recommended:

    print(f"{keyword:35} {count}")