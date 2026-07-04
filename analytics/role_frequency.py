# =========================================================
# analytics/role_frequency.py
# =========================================================

import os

import pandas as pd

from scraper.job_classifier import classify_job


# =========================================================
# CONFIGURATION
# =========================================================

OUTPUT_PATH = "data/role_frequency.csv"


# =========================================================
# GENERATE ROLE FREQUENCY
# =========================================================

def generate_role_frequency(df):

    print("\n========================================")
    print("GENERATING JOB ROLE DEMAND ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Role_Category",
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

    if "Title" not in df.columns:

        print("Title column not found.")

        return empty_df

    role_df = df.copy()

    # =====================================================
    # CLASSIFY JOB ROLES
    # =====================================================

    role_df["Role_Category"] = (
        role_df["Title"]
        .apply(classify_job)
    )

    role_df.dropna(
        subset=["Role_Category"],
        inplace=True,
    )

    if role_df.empty:

        print("No valid job roles found.")

        return empty_df

    # =====================================================
    # CLEAN ROLE CATEGORY
    # =====================================================

    role_df["Role_Category"] = (
        role_df["Role_Category"]
        .astype(str)
        .str.strip()
    )

    role_df = role_df[
        role_df["Role_Category"] != ""
    ]

    if role_df.empty:

        print("No valid job roles found after cleaning.")

        return empty_df

    # =====================================================
    # GROUP ROLE CATEGORIES
    # =====================================================

    result_df = (
        role_df
        .groupby(
            "Role_Category",
            as_index=False,
        )
        .agg(
            Job_Count=(
                "Role_Category",
                "size",
            )
        )
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    total_jobs = len(role_df)

    result_df["Percentage"] = (
        result_df["Job_Count"]
        / total_jobs
        * 100
    ).round(2)

    # =====================================================
    # SORT
    # =====================================================

    result_df.sort_values(
        by=[
            "Job_Count",
            "Role_Category",
        ],
        ascending=[
            False,
            True,
        ],
        inplace=True,
    )

    result_df.reset_index(
        drop=True,
        inplace=True,
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

    other_jobs = int(
        role_df["Role_Category"]
        .eq("Other")
        .sum()
    )

    other_percentage = round(
        other_jobs
        / total_jobs
        * 100,
        2,
    )

    print(
        f"Total Jobs       : "
        f"{total_jobs}"
    )

    print(
        f"Role Categories  : "
        f"{len(result_df)}"
    )

    print(
        f"Other Jobs       : "
        f"{other_jobs}"
    )

    print(
        f"Other Percentage : "
        f"{other_percentage}%"
    )

    print(
        f"CSV Saved        : "
        f"{OUTPUT_PATH}"
    )

    print("\nJOB ROLE DEMAND")

    print(
        result_df.to_string(
            index=False
        )
    )

    return result_df