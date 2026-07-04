# =========================================================
# analytics/company_frequency.py
# =========================================================

import os

import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

OUTPUT_PATH = "data/company_frequency.csv"


INVALID_COMPANIES = {
    "",
    "nan",
    "none",
    "null",
    "unknown",
    "not available",
}


PLACEHOLDER_COMPANIES = {
    "leading client",
    "confidential",
    "confidential company",
    "client of",
    "client",
    "hiring for client",
    "leading company",
    "leading mnc",
    "leading organisation",
    "leading organization",
    "undisclosed",
}


COMPANY_ALIASES = {
    "tcs": "Tata Consultancy Services",
    "tata consultancy services ltd": "Tata Consultancy Services",
    "tata consultancy services limited": "Tata Consultancy Services",

    "accenture solutions pvt ltd": "Accenture",
    "accenture solutions private limited": "Accenture",

    "infosys limited": "Infosys",
    "infosys ltd": "Infosys",

    "wipro limited": "Wipro",
    "wipro ltd": "Wipro",

    "ibm india": "IBM",
    "ibm india pvt ltd": "IBM",
    "international business machines": "IBM",

    "capgemini india": "Capgemini",
    "capgemini technology services india limited": "Capgemini",

    "ernst and young": "EY",
    "ernst & young": "EY",
    "ey india": "EY",

    "crisil analytices": "Crisil",
    "crisil analytics": "Crisil",
    "crisil limited": "Crisil",
}


# =========================================================
# CLEAN COMPANY NAME
# =========================================================

def clean_company(company):

    if company is None:
        return None

    company = str(company).strip()

    company_key = company.casefold()

    if company_key in INVALID_COMPANIES:
        return None

    if company_key in PLACEHOLDER_COMPANIES:
        return None

    if company_key in COMPANY_ALIASES:
        return COMPANY_ALIASES[company_key]

    return company


# =========================================================
# GENERATE COMPANY FREQUENCY
# =========================================================

def generate_company_frequency(df):

    print("\n========================================")
    print("GENERATING COMPANY DEMAND ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Company",
            "Job_Count",
            "Percentage",
            "Sources",
        ]
    )

    if df is None or df.empty:

        print("DataFrame is empty.")

        return empty_df

    if "Company" not in df.columns:

        print("Company column not found.")

        return empty_df

    company_df = df.copy()

    # =====================================================
    # CLEAN COMPANIES
    # =====================================================

    company_df["Company"] = (
        company_df["Company"]
        .apply(clean_company)
    )

    company_df.dropna(
        subset=["Company"],
        inplace=True,
    )

    if company_df.empty:

        print("No valid companies found.")

        return empty_df

    # =====================================================
    # SOURCE FALLBACK
    # =====================================================

    if "Source" not in company_df.columns:

        company_df["Source"] = "Unknown"

    company_df["Source"] = (
        company_df["Source"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # =====================================================
    # CASE-INSENSITIVE COMPANY KEY
    # =====================================================

    company_df["Company_Key"] = (
        company_df["Company"]
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    # =====================================================
    # GROUP COMPANIES
    # =====================================================

    result_df = (
        company_df
        .groupby(
            "Company_Key",
            as_index=False,
        )
        .agg(
            Company=("Company", "first"),
            Job_Count=("Company", "size"),
            Sources=(
                "Source",
                lambda values: ", ".join(
                    sorted(
                        {
                            str(value).strip()
                            for value in values
                            if str(value).strip()
                        }
                    )
                ),
            ),
        )
    )

    result_df.drop(
        columns=["Company_Key"],
        inplace=True,
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    total_jobs = len(company_df)

    result_df["Percentage"] = (
        result_df["Job_Count"]
        / total_jobs
        * 100
    ).round(2)

    # =====================================================
    # COLUMN ORDER
    # =====================================================

    result_df = result_df[
        [
            "Company",
            "Job_Count",
            "Percentage",
            "Sources",
        ]
    ]

    # =====================================================
    # SORT
    # =====================================================

    result_df.sort_values(
        by=[
            "Job_Count",
            "Company",
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

    print(f"Total Jobs       : {total_jobs}")

    print(
        f"Unique Companies : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved        : "
        f"{OUTPUT_PATH}"
    )

    print("\nTOP 20 HIRING COMPANIES")

    print(
        result_df
        .head(20)
        .to_string(index=False)
    )

    return result_df