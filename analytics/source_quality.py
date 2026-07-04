# =========================================================
# analytics/source_quality.py
# =========================================================

import os

import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

SOURCE_OUTPUT_PATH = "data/source_quality.csv"

FIELD_OUTPUT_PATH = "data/field_quality.csv"


QUALITY_FIELDS = [
    "Title",
    "Company",
    "Location",
    "Experience",
    "Salary",
    "Skills",
    "Job_Link",
]


INVALID_VALUES = {
    "",
    "nan",
    "none",
    "null",
    "unknown",
    "not available",
    "not disclosed",
}


# =========================================================
# VALID VALUE MASK
# =========================================================

def get_valid_mask(series):

    cleaned_series = (
        series
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    return ~cleaned_series.isin(
        INVALID_VALUES
    )


# =========================================================
# GENERATE SOURCE QUALITY
# =========================================================

def generate_source_quality(df):

    print("\n========================================")
    print("GENERATING SOURCE QUALITY ANALYTICS")
    print("========================================")

    source_columns = [
        "Source",
        "Job_Count",
        "Source_Share_Percentage",
    ]

    for field in QUALITY_FIELDS:

        source_columns.append(
            f"{field}_Coverage_Percentage"
        )

    empty_df = pd.DataFrame(
        columns=source_columns
    )

    # =====================================================
    # VALIDATION
    # =====================================================

    if df is None or df.empty:

        print("DataFrame is empty.")

        return empty_df

    if "Source" not in df.columns:

        print("Source column not found.")

        return empty_df

    quality_df = df.copy()

    quality_df["Source"] = (
        quality_df["Source"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    quality_df.loc[
        quality_df["Source"] == "",
        "Source",
    ] = "Unknown"

    total_jobs = len(quality_df)

    source_rows = []

    # =====================================================
    # SOURCE-LEVEL COVERAGE
    # =====================================================

    for source, source_df in quality_df.groupby(
        "Source",
        dropna=False,
    ):

        source_job_count = len(source_df)

        row = {
            "Source": source,
            "Job_Count": source_job_count,
            "Source_Share_Percentage": round(
                source_job_count
                / total_jobs
                * 100,
                2,
            ),
        }

        for field in QUALITY_FIELDS:

            coverage_column = (
                f"{field}_Coverage_Percentage"
            )

            if field not in source_df.columns:

                row[coverage_column] = 0.0

                continue

            valid_mask = get_valid_mask(
                source_df[field]
            )

            row[coverage_column] = round(
                valid_mask.mean() * 100,
                2,
            )

        source_rows.append(row)

    result_df = pd.DataFrame(
        source_rows
    )

    result_df.sort_values(
        by=[
            "Job_Count",
            "Source",
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
    # SAVE SOURCE QUALITY
    # =====================================================

    os.makedirs(
        os.path.dirname(SOURCE_OUTPUT_PATH),
        exist_ok=True,
    )

    result_df.to_csv(
        SOURCE_OUTPUT_PATH,
        index=False,
    )

    print(
        f"Total Jobs       : "
        f"{total_jobs}"
    )

    print(
        f"Sources          : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved        : "
        f"{SOURCE_OUTPUT_PATH}"
    )

    print("\nSOURCE QUALITY")

    print(
        result_df.to_string(
            index=False
        )
    )

    return result_df


# =========================================================
# GENERATE FIELD QUALITY
# =========================================================

def generate_field_quality(df):

    print("\n========================================")
    print("GENERATING FIELD QUALITY ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Field",
            "Valid_Count",
            "Missing_Invalid_Count",
            "Coverage_Percentage",
        ]
    )

    if df is None or df.empty:

        print("DataFrame is empty.")

        return empty_df

    total_jobs = len(df)

    field_rows = []

    for field in QUALITY_FIELDS:

        if field not in df.columns:

            valid_count = 0

        else:

            valid_mask = get_valid_mask(
                df[field]
            )

            valid_count = int(
                valid_mask.sum()
            )

        missing_invalid_count = (
            total_jobs - valid_count
        )

        coverage_percentage = round(
            valid_count
            / total_jobs
            * 100,
            2,
        )

        field_rows.append(
            {
                "Field": field,
                "Valid_Count": valid_count,
                "Missing_Invalid_Count": (
                    missing_invalid_count
                ),
                "Coverage_Percentage": (
                    coverage_percentage
                ),
            }
        )

    result_df = pd.DataFrame(
        field_rows
    )

    result_df.sort_values(
        by=[
            "Coverage_Percentage",
            "Field",
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
    # SAVE FIELD QUALITY
    # =====================================================

    os.makedirs(
        os.path.dirname(FIELD_OUTPUT_PATH),
        exist_ok=True,
    )

    result_df.to_csv(
        FIELD_OUTPUT_PATH,
        index=False,
    )

    print(
        f"Total Jobs       : "
        f"{total_jobs}"
    )

    print(
        f"Fields Audited   : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved        : "
        f"{FIELD_OUTPUT_PATH}"
    )

    print("\nFIELD QUALITY")

    print(
        result_df.to_string(
            index=False
        )
    )

    return result_df