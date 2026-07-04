# =========================================================
# analytics/experience_frequency.py
# =========================================================

import os

import pandas as pd

from scraper.experience_parser import parse_experience


# =========================================================
# CONFIGURATION
# =========================================================

OUTPUT_PATH = "data/experience_frequency.csv"


EXPERIENCE_BUCKET_ORDER = [
    "Fresher",
    "0-2 Years",
    "2-5 Years",
    "5-10 Years",
    "10+ Years",
]


# =========================================================
# CLASSIFY EXPERIENCE
# =========================================================

def classify_experience(experience):

    min_exp, max_exp = parse_experience(experience)

    if min_exp is None:
        return None

    # Explicit fresher requirement
    if min_exp == 0 and max_exp == 0:
        return "Fresher"

    # Minimum required experience is used for
    # demand segmentation.
    if min_exp < 2:
        return "0-2 Years"

    if min_exp < 5:
        return "2-5 Years"

    if min_exp < 10:
        return "5-10 Years"

    return "10+ Years"


# =========================================================
# GENERATE EXPERIENCE FREQUENCY
# =========================================================

def generate_experience_frequency(df):

    print("\n========================================")
    print("GENERATING EXPERIENCE DEMAND ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Experience_Level",
            "Job_Count",
            "Percentage",
        ]
    )

    # =====================================================
    # VALIDATION
    # =====================================================

    if df is None or df.empty:

        print("DataFrame is empty.")

        return empty_df

    if "Experience" not in df.columns:

        print("Experience column not found.")

        return empty_df

    experience_df = df.copy()

    # =====================================================
    # CLASSIFY EXPERIENCE
    # =====================================================

    experience_df["Experience_Level"] = (
        experience_df["Experience"]
        .apply(classify_experience)
    )

    experience_df.dropna(
        subset=["Experience_Level"],
        inplace=True,
    )

    if experience_df.empty:

        print("No valid experience values found.")

        return empty_df

    # =====================================================
    # GROUP EXPERIENCE LEVELS
    # =====================================================

    result_df = (
        experience_df
        .groupby(
            "Experience_Level",
            as_index=False,
        )
        .agg(
            Job_Count=(
                "Experience_Level",
                "size",
            )
        )
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    total_classified_jobs = len(experience_df)

    result_df["Percentage"] = (
        result_df["Job_Count"]
        / total_classified_jobs
        * 100
    ).round(2)

    # =====================================================
    # APPLY BUCKET ORDER
    # =====================================================

    result_df["Experience_Level"] = pd.Categorical(
        result_df["Experience_Level"],
        categories=EXPERIENCE_BUCKET_ORDER,
        ordered=True,
    )

    result_df.sort_values(
        by="Experience_Level",
        inplace=True,
    )

    result_df.reset_index(
        drop=True,
        inplace=True,
    )

    result_df["Experience_Level"] = (
        result_df["Experience_Level"]
        .astype(str)
    )

    # =====================================================
    # SAVE CSV
    # =====================================================

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True,
    )

    result_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    total_jobs = len(df)

    unclassified_jobs = (
        total_jobs - total_classified_jobs
    )

    print(
        f"Total Jobs          : "
        f"{total_jobs}"
    )

    print(
        f"Classified Jobs     : "
        f"{total_classified_jobs}"
    )

    print(
        f"Unclassified Jobs   : "
        f"{unclassified_jobs}"
    )

    print(
        f"Experience Buckets  : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved           : "
        f"{OUTPUT_PATH}"
    )

    print("\nEXPERIENCE DEMAND")

    print(
        result_df.to_string(
            index=False
        )
    )

    return result_df