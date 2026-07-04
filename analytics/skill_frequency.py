# =========================================================
# analytics/skill_frequency.py
# =========================================================

import os
from collections import Counter

import pandas as pd

from scraper.skill_normalizer import normalize_skill


# =========================================================
# CONFIGURATION
# =========================================================

OUTPUT_PATH = "data/skill_frequency.csv"

INVALID_SKILLS = {
    "",
    "nan",
    "none",
    "null",
    "not available",
    "unknown",
}


# =========================================================
# CLEAN AND NORMALIZE SKILL
# =========================================================

def clean_skill(skill):

    if skill is None:
        return None

    skill = str(skill).strip()

    if skill.lower() in INVALID_SKILLS:
        return None

    skill = normalize_skill(skill)

    if not skill:
        return None

    skill = str(skill).strip()

    if skill.lower() in INVALID_SKILLS:
        return None

    return skill


# =========================================================
# GENERATE SKILL FREQUENCY
# =========================================================

def generate_skill_frequency(df):

    print("\n========================================")
    print("GENERATING SKILL FREQUENCY")
    print("========================================")

    empty_df = pd.DataFrame(
        columns=[
            "Skill",
            "Frequency",
            "Percentage",
        ]
    )

    if df is None or df.empty:

        print("DataFrame is empty.")

        return empty_df

    if "Skills" not in df.columns:

        print("Skills column not found.")

        return empty_df

    skill_counter = Counter()

    jobs_with_skills = 0

    # =====================================================
    # PROCESS JOB SKILLS
    # =====================================================

    for skills in df["Skills"].fillna(""):

        skills = str(skills).strip()

        if skills.lower() in INVALID_SKILLS:
            continue

        skill_list = skills.split(",")

        # Dictionary is used for case-insensitive
        # deduplication inside one job.
        unique_skills = {}

        for skill in skill_list:

            skill = clean_skill(skill)

            if skill is None:
                continue

            skill_key = skill.casefold()

            unique_skills[skill_key] = skill

        if unique_skills:

            jobs_with_skills += 1

        for skill in unique_skills.values():

            skill_counter[skill] += 1

    # =====================================================
    # CREATE DATAFRAME
    # =====================================================

    skill_df = pd.DataFrame(
        skill_counter.items(),
        columns=[
            "Skill",
            "Frequency",
        ],
    )

    if skill_df.empty:

        print("No valid skills found.")

        return empty_df

    # =====================================================
    # FINAL CASE-INSENSITIVE MERGE
    # =====================================================

    skill_df["Skill_Key"] = (
        skill_df["Skill"]
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    skill_df = (
        skill_df
        .groupby(
            "Skill_Key",
            as_index=False,
        )
        .agg(
            Skill=("Skill", "first"),
            Frequency=("Frequency", "sum"),
        )
    )

    skill_df.drop(
        columns=["Skill_Key"],
        inplace=True,
    )

    # =====================================================
    # CALCULATE PERCENTAGE
    # =====================================================

    if jobs_with_skills > 0:

        skill_df["Percentage"] = (
            skill_df["Frequency"]
            / jobs_with_skills
            * 100
        ).round(2)

    else:

        skill_df["Percentage"] = 0.0

    # =====================================================
    # SORT
    # =====================================================

    skill_df.sort_values(
        by=[
            "Frequency",
            "Skill",
        ],
        ascending=[
            False,
            True,
        ],
        inplace=True,
    )

    skill_df.reset_index(
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

    skill_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    print(
        f"Jobs With Skills : "
        f"{jobs_with_skills}"
    )

    print(
        f"Unique Skills    : "
        f"{len(skill_df)}"
    )

    print(
        f"CSV Saved        : "
        f"{OUTPUT_PATH}"
    )

    print("\nTOP 20 SKILLS")

    print(
        skill_df
        .head(20)
        .to_string(index=False)
    )

    return skill_df