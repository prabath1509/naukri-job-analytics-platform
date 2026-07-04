# =========================================================
# analytics/location_frequency.py
# =========================================================

import os

import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

LOCATION_OUTPUT_PATH = "data/location_frequency.csv"
WORKMODE_OUTPUT_PATH = "data/workmode_frequency.csv"


INVALID_LOCATIONS = {
    "",
    "nan",
    "none",
    "null",
    "unknown",
    "not available",
}


INVALID_WORK_MODES = {
    "",
    "nan",
    "none",
    "null",
    "unknown",
    "not available",
}


# =========================================================
# LOCATION ALIASES
# =========================================================

LOCATION_ALIASES = {
    "bangalore": "Bengaluru",
    "bengaluru": "Bengaluru",
    "bangalore rural": "Bengaluru",

    "hyderabad/secunderabad": "Hyderabad",
    "hyderabad": "Hyderabad",
    "secunderabad": "Hyderabad",

    "delhi / ncr": "Delhi NCR",
    "delhi ncr": "Delhi NCR",
    "ncr": "Delhi NCR",

    "new delhi": "Delhi",
    "delhi": "Delhi",

    "mumbai": "Mumbai",
    "mumbai suburban": "Mumbai",
    "mumbai (all areas)": "Mumbai",

    "pune": "Pune",

    "chennai": "Chennai",

    "gurgaon": "Gurugram",
    "gurugram": "Gurugram",

    "noida": "Noida",

    "kolkata": "Kolkata",
    "calcutta": "Kolkata",

    "ahmedabad": "Ahmedabad",

    "jaipur": "Jaipur",

    "coimbatore": "Coimbatore",

    "kochi": "Kochi",
    "cochin": "Kochi",
}


# =========================================================
# WORK MODE ALIASES
# =========================================================

WORKMODE_ALIASES = {
    "remote": "Remote",
    "work from home": "Remote",
    "work-from-home": "Remote",
    "wfh": "Remote",

    "hybrid": "Hybrid",

    "on-site": "On-site",
    "onsite": "On-site",
    "on site": "On-site",
    "office": "On-site",
    "office based": "On-site",
    "office-based": "On-site",
}


# =========================================================
# CLEAN LOCATION
# =========================================================

def clean_location(location):

    if location is None:
        return None

    location = str(location).strip()

    location_key = location.casefold()

    if location_key in INVALID_LOCATIONS:
        return None

    # =====================================================
    # REMOVE PURE WORK MODE VALUES
    # =====================================================

    pure_work_modes = {
        "remote",
        "hybrid",
        "work from home",
        "work-from-home",
        "wfh",
        "on-site",
        "onsite",
        "on site",
    }

    if location_key in pure_work_modes:
        return None

    # =====================================================
    # REMOVE WORK MODE PREFIX
    # =====================================================

    work_mode_prefixes = (
        "remote - ",
        "remote – ",
        "remote — ",
        "hybrid - ",
        "hybrid – ",
        "hybrid — ",
        "on-site - ",
        "on-site – ",
        "on-site — ",
        "onsite - ",
        "onsite – ",
        "onsite — ",
        "on site - ",
        "on site – ",
        "on site — ",
    )

    for prefix in work_mode_prefixes:

        if location_key.startswith(prefix):

            location = location[
                len(prefix):
            ].strip()

            location_key = location.casefold()

            break

    if location_key in INVALID_LOCATIONS:
        return None

    if location_key in pure_work_modes:
        return None

    # =====================================================
    # LOCATION ALIAS
    # =====================================================

    if location_key in LOCATION_ALIASES:
        return LOCATION_ALIASES[location_key]

    return location


# =========================================================
# CLEAN WORK MODE
# =========================================================

def clean_work_mode(work_mode):

    if work_mode is None:
        return None

    work_mode = str(work_mode).strip()

    work_mode_key = work_mode.casefold()

    if work_mode_key in INVALID_WORK_MODES:
        return None

    if work_mode_key in WORKMODE_ALIASES:
        return WORKMODE_ALIASES[work_mode_key]

    # =====================================================
    # DETECT WORK MODE FROM TEXT
    # =====================================================

    if (
        "remote" in work_mode_key
        or "work from home" in work_mode_key
        or "work-from-home" in work_mode_key
        or "wfh" in work_mode_key
    ):
        return "Remote"

    if "hybrid" in work_mode_key:
        return "Hybrid"

    if (
        "on-site" in work_mode_key
        or "onsite" in work_mode_key
        or "on site" in work_mode_key
    ):
        return "On-site"

    return work_mode


# =========================================================
# GENERATE LOCATION FREQUENCY
# =========================================================

def generate_location_frequency(df):

    print("\n========================================")
    print("GENERATING LOCATION DEMAND ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Location",
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

    if "Location" not in df.columns:

        print("Location column not found.")

        return empty_df

    # =====================================================
    # COPY DATAFRAME
    # =====================================================

    location_df = df.copy()

    # Preserve original job identity before explode
    location_df["_Job_Row_ID"] = location_df.index

    # =====================================================
    # INITIAL LOCATION CLEANING
    # =====================================================

    location_df["Location"] = (
        location_df["Location"]
        .apply(clean_location)
    )

    location_df.dropna(
        subset=["Location"],
        inplace=True,
    )

    if location_df.empty:

        print("No valid locations found.")

        return empty_df

    # =====================================================
    # SPLIT MULTI-LOCATION JOBS
    # =====================================================

    location_df["Location"] = (
        location_df["Location"]
        .astype(str)
        .str.split(",")
    )

    location_df = location_df.explode(
        "Location"
    )

    # =====================================================
    # CLEAN EACH LOCATION AFTER SPLIT
    # =====================================================

    location_df["Location"] = (
        location_df["Location"]
        .apply(clean_location)
    )

    location_df.dropna(
        subset=["Location"],
        inplace=True,
    )

    if location_df.empty:

        print("No valid locations found after splitting.")

        return empty_df

    # =====================================================
    # CREATE LOCATION KEY
    # =====================================================

    location_df["Location_Key"] = (
        location_df["Location"]
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    # =====================================================
    # REMOVE DUPLICATE LOCATION PER JOB
    # =====================================================

    location_df.drop_duplicates(
        subset=[
            "_Job_Row_ID",
            "Location_Key",
        ],
        inplace=True,
    )

    # =====================================================
    # GROUP LOCATIONS
    # =====================================================

    result_df = (
        location_df
        .groupby(
            "Location_Key",
            as_index=False,
        )
        .agg(
            Location=("Location", "first"),
            Job_Count=("Location", "size"),
        )
    )

    result_df.drop(
        columns=["Location_Key"],
        inplace=True,
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    total_jobs = len(df)

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
            "Location",
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
        os.path.dirname(LOCATION_OUTPUT_PATH),
        exist_ok=True,
    )

    result_df.to_csv(
        LOCATION_OUTPUT_PATH,
        index=False,
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    print(
        f"Total Jobs       : "
        f"{total_jobs}"
    )

    print(
        f"Unique Locations : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved        : "
        f"{LOCATION_OUTPUT_PATH}"
    )

    print("\nTOP 20 JOB LOCATIONS")

    print(
        result_df
        .head(20)
        .to_string(index=False)
    )

    return result_df


# =========================================================
# GENERATE WORK MODE FREQUENCY
# =========================================================

def generate_workmode_frequency(df):

    print("\n========================================")
    print("GENERATING WORK MODE ANALYTICS")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Work_Mode",
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

    workmode_df = df.copy()

    # =====================================================
    # USE WORK_MODE COLUMN IF AVAILABLE
    # OTHERWISE DERIVE FROM LOCATION
    # =====================================================

    if "Work_Mode" in workmode_df.columns:

        print("Work mode source : Work_Mode column")

        workmode_df["Work_Mode"] = (
            workmode_df["Work_Mode"]
            .apply(clean_work_mode)
        )

    elif "Location" in workmode_df.columns:

        print("Work mode source : Derived from Location")

        def detect_mode_from_location(location):

            if location is None:
                return "On-site"

            location = str(location).strip()

            location_key = location.casefold()

            if (
                "remote" in location_key
                or "work from home" in location_key
                or "work-from-home" in location_key
                or "wfh" in location_key
            ):
                return "Remote"

            if "hybrid" in location_key:
                return "Hybrid"

            return "On-site"

        workmode_df["Work_Mode"] = (
            workmode_df["Location"]
            .apply(detect_mode_from_location)
        )

    else:

        print(
            "Neither Work_Mode nor Location "
            "column found."
        )

        return empty_df

    # =====================================================
    # CLEAN WORK MODE
    # =====================================================

    workmode_df["Work_Mode"] = (
        workmode_df["Work_Mode"]
        .apply(clean_work_mode)
    )

    workmode_df.dropna(
        subset=["Work_Mode"],
        inplace=True,
    )

    if workmode_df.empty:

        print("No valid work modes found.")

        return empty_df

    # =====================================================
    # CREATE WORK MODE KEY
    # =====================================================

    workmode_df["Work_Mode_Key"] = (
        workmode_df["Work_Mode"]
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    # =====================================================
    # GROUP WORK MODES
    # =====================================================

    result_df = (
        workmode_df
        .groupby(
            "Work_Mode_Key",
            as_index=False,
        )
        .agg(
            Work_Mode=("Work_Mode", "first"),
            Job_Count=("Work_Mode", "size"),
        )
    )

    result_df.drop(
        columns=["Work_Mode_Key"],
        inplace=True,
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    total_jobs = len(workmode_df)

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
            "Work_Mode",
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
        os.path.dirname(WORKMODE_OUTPUT_PATH),
        exist_ok=True,
    )

    result_df.to_csv(
        WORKMODE_OUTPUT_PATH,
        index=False,
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    print(
        f"Total Jobs       : "
        f"{total_jobs}"
    )

    print(
        f"Work Modes       : "
        f"{len(result_df)}"
    )

    print(
        f"CSV Saved        : "
        f"{WORKMODE_OUTPUT_PATH}"
    )

    print("\nWORK MODE DEMAND")

    print(
        result_df.to_string(
            index=False
        )
    )

    return result_df