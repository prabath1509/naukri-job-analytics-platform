import pandas as pd
from pathlib import Path
from itertools import combinations

# Paths
DATASET_PATH = Path("data/jobs_20260731_173423.csv")
OUTPUT_PATH = Path("docs/case-study/duplicate_review.csv")

# Load the original dataset
df = pd.read_csv(DATASET_PATH, low_memory=False)

# Normalize fields used to identify candidate groups
df["_title"] = (
    df["Title"].fillna("").astype(str)
    .str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
)

df["_company"] = (
    df["Company"].fillna("").astype(str)
    .str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
)

df["_location"] = (
    df["Location"].fillna("").astype(str)
    .str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
)

# Exclude records without a title or company
valid = df["_title"].ne("") & df["_company"].ne("")

# Identify repeated title/company/location groups
group_columns = ["_title", "_company", "_location"]
grouped = df.loc[valid].groupby(group_columns, dropna=False)

review_rows = []

for key, group in grouped:
    if len(group) < 2:
        continue

    records = group.to_dict("records")

    for first, second in combinations(records, 2):
        same_url = (
            str(first.get("Job_Link", "")).strip().lower()
            == str(second.get("Job_Link", "")).strip().lower()
        )

        same_experience = (
            str(first.get("Experience", "")).strip().lower()
            == str(second.get("Experience", "")).strip().lower()
        )

        review_rows.append({
            "Title": first.get("Title", ""),
            "Company": first.get("Company", ""),
            "Location": first.get("Location", ""),
            "Experience_1": first.get("Experience", ""),
            "Experience_2": second.get("Experience", ""),
            "Source_1": first.get("Source", ""),
            "Source_2": second.get("Source", ""),
            "Job_Link_1": first.get("Job_Link", ""),
            "Job_Link_2": second.get("Job_Link", ""),
            "Same_URL": same_url,
            "Same_Experience": same_experience,
            "Review_Status": (
                "POTENTIAL_DUPLICATE_SAME_URL"
                if same_url
                else "MANUAL_REVIEW_DIFFERENT_URLS"
            ),
        })

# Export candidate pairs
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

review_df = pd.DataFrame(review_rows)

if not review_df.empty:
    review_df.to_csv(OUTPUT_PATH, index=False)

print("=" * 55)
print("DUPLICATE CANDIDATE REVIEW")
print("=" * 55)
print("Dataset records:", len(df))
print("Candidate pairs:", len(review_df))

if not review_df.empty:
    print("\nReview classifications:")
    print(review_df["Review_Status"].value_counts().to_string())

    print("\nPairs with identical URLs:", int(review_df["Same_URL"].sum()))
    print(
        "Pairs with identical experience labels:",
        int(review_df["Same_Experience"].sum())
    )

print("\nOriginal dataset modified: No")
print("Review report:", OUTPUT_PATH)