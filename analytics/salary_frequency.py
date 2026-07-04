# =========================================================
# analytics/salary_frequency.py
# =========================================================

import os

import pandas as pd

from scraper.salary_parser import parse_salary


# =========================================================
# CONFIGURATION
# =========================================================

OUTPUT_PATH = "data/salary_frequency.csv"


SALARY_BUCKET_ORDER = [
    "Unpaid",
    "0-3 LPA",
    "3-5 LPA",
    "5-10 LPA",
    "10-15 LPA",
    "15-25 LPA",
    "25+ LPA",
]


# =========================================================
# CLASSIFY SALARY
# =========================================================

def classify_salary(salary):

    min_salary, max_salary = parse_salary(salary)

    if min_salary is None:
        return None

    # =====================================================
    # UNPAID
    # =====================================================

    if (
        min_salary == 0
        and max_salary == 0
    ):
        return "Unpaid"

    # =====================================================
    # USE MIDPOINT FOR SALARY SEGMENTATION
    # =====================================================

    if max_salary is None:

        salary_value = min_salary

    else:

        salary_value = (
            min_salary + max_salary
        ) / 2

    # =====================================================
    # SALARY BUCKETS
    # =====================================================

    if salary_value < 3:
        return "0-3 LPA"

    if salary_value < 5:
        return "3-5 LPA"

    if salary_value < 10:
        return "5-10 LPA"

    if salary_value < 15:
        return "10-15 LPA"

    if salary_value < 25:
        return "15-25 LPA"

    return "25+ LPA"


# =========================================================
# GENERATE SALARY FREQUENCY
# =========================================================

def generate_salary_frequency(df):

    print("\n========================================")
    print("GENERATING SALARY DEMAND ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Salary_Bucket",
            "Job_Count",
            "Parsed_Share_Percentage",
            "Paid_Share_Percentage",
        ]
    )

    # =====================================================
    # VALIDATION
    # =====================================================

    if df is None or df.empty:

        print("DataFrame is empty.")

        return empty_df

    if "Salary" not in df.columns:

        print("Salary column not found.")

        return empty_df

    salary_df = df.copy()

    # =====================================================
    # CLASSIFY SALARY
    # =====================================================

    salary_df["Salary_Bucket"] = (
        salary_df["Salary"]
        .apply(classify_salary)
    )

    salary_df.dropna(
        subset=["Salary_Bucket"],
        inplace=True,
    )

    if salary_df.empty:

        print("No valid salary values found.")

        return empty_df

    # =====================================================
    # GROUP SALARY BUCKETS
    # =====================================================

    result_df = (
        salary_df
        .groupby(
            "Salary_Bucket",
            as_index=False,
        )
        .agg(
            Job_Count=(
                "Salary_Bucket",
                "size",
            )
        )
    )

    # =====================================================
    # CALCULATE PERCENTAGES
    # =====================================================

    total_parsed_jobs = len(salary_df)

    unpaid_jobs = int(
        salary_df["Salary_Bucket"]
        .eq("Unpaid")
        .sum()
    )

    paid_salary_jobs = (
        total_parsed_jobs - unpaid_jobs
    )

    result_df["Parsed_Share_Percentage"] = (
        result_df["Job_Count"]
        / total_parsed_jobs
        * 100
    ).round(2)

    result_df["Paid_Share_Percentage"] = (
        result_df.apply(
            lambda row: (
                0.0
                if row["Salary_Bucket"] == "Unpaid"
                or paid_salary_jobs == 0
                else round(
                    row["Job_Count"]
                    / paid_salary_jobs
                    * 100,
                    2,
                )
            ),
            axis=1,
        )
    )

    # =====================================================
    # APPLY BUCKET ORDER
    # =====================================================

    result_df["Salary_Bucket"] = pd.Categorical(
        result_df["Salary_Bucket"],
        categories=SALARY_BUCKET_ORDER,
        ordered=True,
    )

    result_df.sort_values(
        by="Salary_Bucket",
        inplace=True,
    )

    result_df.reset_index(
        drop=True,
        inplace=True,
    )

    result_df["Salary_Bucket"] = (
        result_df["Salary_Bucket"]
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

    undisclosed_jobs = (
        total_jobs - total_parsed_jobs
    )

    print(
        f"Total Jobs          : "
        f"{total_jobs}"
    )

    print(
        f"Parsed Salaries     : "
        f"{total_parsed_jobs}"
    )

    print(
        f"Paid Salary Jobs    : "
        f"{paid_salary_jobs}"
    )

    print(
        f"Unpaid Jobs         : "
        f"{unpaid_jobs}"
    )

    print(
        f"Undisclosed Jobs    : "
        f"{undisclosed_jobs}"
    )

    print(
        f"Salary Buckets      : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved           : "
        f"{OUTPUT_PATH}"
    )

    print("\nSALARY DEMAND")

    print(
        result_df.to_string(
            index=False
        )
    )

    return result_df