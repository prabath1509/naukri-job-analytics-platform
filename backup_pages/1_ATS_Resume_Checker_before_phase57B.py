import os
import sys
import sqlite3

import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from resume_matcher.pdf_parser import (
    extract_resume_text
)

from resume_matcher.matcher import (
    match_jobs
)

from resume_matcher.ats_checker import (
    calculate_ats_score
)

from resume_matcher.skill_gap import (
    analyze_skill_gap
)

from resume_matcher.resume_scorer import (
    score_resume
)

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "database",
    "jobs.db"
)


@st.cache_data
def load_jobs():

    conn = sqlite3.connect(DB_PATH)

    try:

        df = pd.read_sql(
            "SELECT * FROM jobs",
            conn
        )

    finally:

        conn.close()

    return df


st.set_page_config(
    page_title="ATS Resume Checker",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ATS Resume Checker")

jobs_df = load_jobs()

uploaded_resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_resume is not None:

    resume_text = extract_resume_text(
        uploaded_resume
    )

    job_titles = sorted(
        jobs_df["Title"].dropna().unique()
    )

    selected_job = st.selectbox(
        "Target Job",
        job_titles
    )

    if st.button(
        "Analyze Resume"
    ):

        job = jobs_df[
            jobs_df["Title"] == selected_job
        ].iloc[0]

        job_text = " ".join([
            str(job["Title"]),
            str(job["Skills"]),
            str(job["Company"])
        ])

        ats = calculate_ats_score(
            resume_text,
            job_text
        )

        gap = analyze_skill_gap(
            resume_text,
            job_text
        )

        structure = score_resume(
            resume_text
        )
st.write("ATS OUTPUT")
st.write(ats)

st.write("GAP OUTPUT")
st.write(gap)

st.write("STRUCTURE OUTPUT")
st.write(structure)
# ==========================================
# RESUME SUMMARY
# ==========================================

st.subheader("📋 Resume Summary")

summary1, summary2, summary3 = st.columns(3)

with summary1:

    st.metric(
        "Skills Found",
        len(gap["Current Skills"])
    )

with summary2:

    st.metric(
        "Matched Skills",
        len(ats["Matched Skills"])
    )

with summary3:

    st.metric(
        "Missing Skills",
        len(ats["Missing Skills"])
    )

        # ==========================================
# ATS SCORE
# ==========================================

score = ats["ATS Score"]

st.metric(
    "🎯 ATS Score",
    f"{score}%"
)

st.progress(score / 100)

if score >= 90:

    st.success(
        "Excellent Match"
    )

elif score >= 75:

    st.success(
        "Good Match"
    )

elif score >= 60:

    st.warning(
        "Fair Match"
    )

else:

    st.error(
        "Needs Improvement"
    )

col1, col2 = st.columns(2)
with col1:

    st.subheader("✅ Matched Skills")

    if ats["Matched Skills"]:

        for skill in ats["Matched Skills"]:

            st.success(skill.title())

    else:

        st.info("No matched skills found.")
with col2:

    st.subheader("❌ Missing Skills")

    if ats["Missing Skills"]:

        for skill in ats["Missing Skills"]:

            st.error(skill.title())

    else:

        st.success("No missing skills.")
    # =========================================================
# RESUME STRUCTURE
# =========================================================

st.subheader("📄 Resume Structure")

sections = structure["Sections"]

for section, present in sections.items():

    if present:

        st.success(f"✔ {section.title()}")

    else:

        st.warning(f"✖ {section.title()}")


# =========================================================
# SKILL GAP
# =========================================================

st.subheader("📉 Skill Gap")

left, right = st.columns(2)

with left:

    st.markdown("### Current Skills")

    for skill in gap["Current Skills"]:

        st.success(skill.title())

with right:

    st.markdown("### Missing Skills")

    if gap["Missing Skills"]:

        for skill in gap["Missing Skills"]:

            st.error(skill.title())

    else:

        st.success("No missing skills.")

    st.subheader(
            "Top Matching Jobs"
        )

    matched = match_jobs(
            resume_text,
            jobs_df
        )

    st.dataframe(
            matched[
                [
                    "Title",
                    "Company",
                    "Match_Percentage"
                ]
            ].head(10),
            use_container_width=True
        )