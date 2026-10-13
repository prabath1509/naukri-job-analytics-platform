import pandas as pd
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timedelta
import re
import json

DATA_DIR = Path("data")
REPORT_DIR = Path("docs/case-study")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Find the latest available job snapshot.
files = sorted(DATA_DIR.glob("jobs_*.csv"))

if not files:
    raise FileNotFoundError(
        "No jobs_*.csv snapshots found in the data directory."
    )

dataset_path = max(files, key=lambda p: p.stat().st_mtime)

df = pd.read_csv(dataset_path, low_memory=False)
total = len(df)

print("\nDATA QUALITY AUDIT")
print("=" * 45)
print("Dataset:", dataset_path)
print("Records checked:", total)
print("Columns:", list(df.columns))


def get_column(name):
    """Return a dataset column, or an empty series if absent."""
    if name not in df.columns:
        return pd.Series("", index=df.index, dtype="object")

    return df[name].fillna("").astype(str).str.strip()


title = get_column("Title")
company = get_column("Company")
location = get_column("Location")
job_url = get_column("Job_Link")
posted_date = get_column("Posted_Date")


def missing_or_placeholder(series):
    placeholders = {
        "", "nan", "none", "null", "unknown",
        "not available", "n/a", "na"
    }
    return series.str.lower().isin(placeholders)


# 1. Missing or placeholder core fields.
missing_title = missing_or_placeholder(title)
missing_company = missing_or_placeholder(company)

# 2. Missing and invalid application URLs.
missing_url = missing_or_placeholder(job_url)


def valid_http_url(value):
    try:
        parsed = urlparse(value)
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
            and "." in parsed.netloc
        )
    except Exception:
        return False


invalid_url = (
    ~missing_url
    & ~job_url.apply(valid_http_url)
)

# 3. Exact duplicate records.
# Detect repeated title + company + location combinations.
# These are potential duplicates, not confirmed duplicates.
normalized_title = (
    title.fillna("")
    .astype(str)
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

normalized_company = (
    company.fillna("")
    .astype(str)
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

normalized_location = (
    location.fillna("")
    .astype(str)
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

duplicate_title_company_location = (
    ~missing_title
    & ~missing_company
    & df.assign(
        _title=normalized_title,
        _company=normalized_company,
        _location=normalized_location
    ).duplicated(
        subset=["_title", "_company", "_location"],
        keep="first"
    )
)
# 4. Duplicate application URLs.
normalized_url = job_url.str.rstrip("/").str.lower()

duplicate_url = (
    ~missing_url
    & normalized_url.duplicated(keep="first")
)

# 5. Potentially inconsistent location formatting.
def normalize_location(value):
    value = value.lower().strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s*,\s*", ", ", value)
    return value


location_normalized = location.apply(normalize_location)

location_format_variants = (
    pd.DataFrame({
        "original": location,
        "normalized": location_normalized
    })
    .query("original != ''")
    .groupby("normalized")["original"]
    .nunique()
)

variant_groups = location_format_variants[
    location_format_variants > 1
]

# This flags formatting variants only.
# It does not assume that similar city names are the same place.
location_variant_count = int(variant_groups.sum())

# 6. Potentially outdated job listings.
# Only classify dates that can be interpreted reliably.
today = pd.Timestamp.today().normalize()

# Use the snapshot date for interpreting relative posting dates.
snapshot_date = pd.Timestamp("2026-07-31")

cutoff = snapshot_date - pd.Timedelta(days=30)

def parse_posted_date(value):
    value = str(value).strip().lower()

    if value in {
        "", "nan", "none", "null",
        "not available", "unknown"
    }:
        return pd.NaT

    # Handle dates relative to the dataset snapshot date.
    if value in {"today", "posted today", "just now", "recent"}:
        return snapshot_date

    if value in {"yesterday", "posted yesterday"}:
        return snapshot_date - pd.Timedelta(days=1)

    # Handle job postings from a few hours ago.
    if value in {"few hours ago", "a few hours ago"}:
        return snapshot_date

    # Handle future-starting jobs separately.
    if value.startswith("starts in"):
        return pd.NaT

    # Handle postings described as 30+ days old.
    if "30+" in value and "day" in value:
        return snapshot_date - pd.Timedelta(days=31)

    # Handle relative dates such as:
    # 3 weeks ago
    # Posted 18 Days Ago
    # Posted 2 Days Ago
    match = re.search(
        r"(\d+)\s*\+?\s*(day|week|month|year)s?\s*ago",
        value
    )

    if match:
        amount = int(match.group(1))
        unit = match.group(2)

        if unit == "day":
            days = amount
        elif unit == "week":
            days = amount * 7
        elif unit == "month":
            days = amount * 30
        else:
            days = amount * 365

        return snapshot_date - pd.Timedelta(days=days)

    # Handle values such as "3+ weeks ago".
    match = re.search(
        r"(\d+)\s*\+\s*(day|week|month|year)s?\s+ago",
        value
    )

    if match:
        amount = int(match.group(1))
        unit = match.group(2)

        multiplier = {
            "day": 1,
            "week": 7,
            "month": 30,
            "year": 365,
        }[unit]

        # A plus sign means the actual age is at least this amount.
        # Use the lower bound as a conservative estimate.
        days = amount * multiplier

        return snapshot_date - pd.Timedelta(days=days)

    # Handle explicit dates, such as "Starts : 13th Jul' 21".
    cleaned = re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", value)
    cleaned = cleaned.replace("starts :", "").strip()

    parsed = pd.to_datetime(cleaned, errors="coerce")

    if pd.isna(parsed):
        return pd.NaT

    if parsed.tzinfo is not None:
        parsed = parsed.tz_localize(None)

    return parsed.normalize()
parsed_dates = posted_date.apply(parse_posted_date)

# Identify future-starting jobs separately.
future_starting = (
    posted_date.fillna("")
    .astype(str)
    .str.strip()
    .str.lower()
    .str.startswith("starts in")
)

# Only count genuinely missing or unparseable dates.
unknown_posted_date = parsed_dates.isna() & ~future_starting

# Flag postings whose parsed dates are more than 30 days old.
outdated = parsed_dates.notna() & (parsed_dates < cutoff)

# 7. Build an issue report without modifying the source dataset.
issues = pd.DataFrame({
    "Title": title,
    "Company": company,
    "Location": location,
    "Job_Link": job_url,
    "Posted_Date": posted_date,
})

issues["missing_title"] = missing_title
issues["missing_company"] = missing_company
issues["missing_url"] = missing_url
issues["invalid_url"] = invalid_url
issues["duplicate_title_company_location"] = (
    duplicate_title_company_location
)
issues["duplicate_url"] = duplicate_url
issues["potentially_outdated"] = outdated
issues["posted_date_unparseable"] = unknown_posted_date
issues["future_starting"] = future_starting

issue_columns = [
    "missing_title",
    "missing_company",
    "missing_url",
    "invalid_url",
    "duplicate_title_company_location",
    "duplicate_url",
    "potentially_outdated",
    "posted_date_unparseable",
]

issues["issue_count"] = issues[issue_columns].sum(axis=1)

issue_rows = issues[issues["issue_count"] > 0].copy()

# Export records needing review.
issue_path = REPORT_DIR / "data_quality_issues.csv"
issue_rows.to_csv(issue_path, index=False)

# Export future-starting jobs separately.
future_starting_path = REPORT_DIR / "future_starting_jobs.csv"

future_starting_report = df.loc[
    future_starting,
    ["Title", "Company", "Location", "Posted_Date", "Job_Link"]
].copy()

future_starting_report.to_csv(
    future_starting_path,
    index=False
)

# Summary metrics.
summary = {
    "dataset": str(dataset_path),
    "audit_date": str(today.date()),
    "records_checked": int(total),
    "missing_or_placeholder_titles": int(missing_title.sum()),
    "missing_or_placeholder_companies": int(missing_company.sum()),
    "missing_application_urls": int(missing_url.sum()),
    "invalid_application_urls": int(invalid_url.sum()),
    "duplicate_title_company_location": int(
        duplicate_title_company_location.sum()
    ),
    "duplicate_application_urls": int(duplicate_url.sum()),
    "location_format_variant_groups": int(len(variant_groups)),
    "location_variant_records_in_groups": location_variant_count,
    "potentially_outdated_over_30_days": int(outdated.sum()),
    "future_starting_jobs": int(future_starting.sum()),
    "missing_or_unparseable_posted_dates": int(
        unknown_posted_date.sum()
    ),
    "records_flagged_for_review": int(len(issue_rows)),
    "source_dataset_modified": False,
}

summary_path = REPORT_DIR / "data_quality_summary.json"

with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("\nAUDIT RESULTS")
print("=" * 45)

for key, value in summary.items():
    print(f"{key}: {value}")

print("\nFiles created:")
print(issue_path)
print(summary_path)
print(future_starting_path)

print("\nNote:")
print(
    "URL checks are structural, not proof that an application "
    "page is reachable or the vacancy is still open."
)
print(
    "Location variants require review before merging. "
    "Similar formatting does not always mean the same location."
)