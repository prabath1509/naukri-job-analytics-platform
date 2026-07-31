import os
import sys
import sqlite3

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =====================================================
# IMPORTS
# =====================================================

from resume_matcher.pdf_parser import extract_resume_text
from resume_matcher.matcher import match_jobs
from resume_matcher.ats_checker import calculate_ats_score
from resume_matcher.skill_gap import analyze_skill_gap
from resume_matcher.resume_scorer import score_resume
from resume_matcher.recommendations import (
    generate_recommendations
)
from resume_matcher.report_generator import (
    generate_pdf
)
# =====================================================
# DATABASE
# =====================================================

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

# =====================================================
# PAGE
# =====================================================

st.set_page_config(
    page_title="Resume vs Job",
    page_icon="📄",
    layout="wide"
)

st.title("⚖ Resume vs Job Comparison")

st.caption(
    "Analyze your resume against live jobs from your analytics platform."
)

jobs_df = load_jobs()

# =====================================================
# INPUTS
# =====================================================

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_resume is None:

    st.info("Please upload your resume to begin.")

    st.stop()

job_titles = sorted(
    jobs_df["Title"].dropna().unique()
)

selected_job = st.selectbox(
    "Select Target Job",
    job_titles
)

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

if not analyze:

    st.stop()
# =====================================================
# EXTRACT RESUME
# =====================================================

resume_text = extract_resume_text(
    uploaded_resume
)

# =====================================================
# TARGET JOB
# =====================================================

job = jobs_df[
    jobs_df["Title"] == selected_job
].iloc[0]

job_text = " ".join(
    [
        str(job["Title"]),
        str(job["Skills"]),
        str(job["Company"])
    ]
)

# =====================================================
# RUN ANALYSIS
# =====================================================

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

recommendations = generate_recommendations(
    ats,
    gap,
    structure
)

report_file = "ATS_Report.pdf"

generate_pdf(
    report_file,
    ats,
    gap,
    structure,
    recommendations
)
matched_jobs = match_jobs(
    resume_text,
    jobs_df
)
st.success("✅ Resume analyzed successfully.")

# =====================================================
# RESUME SUMMARY
# =====================================================

st.subheader("📋 Resume Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "🎯 ATS Score",
        f"{ats['ATS Score']}%"
    )
with c2:
    st.metric(
        "Matched Skills",
        len(ats["Matched Skills"])
    )

with c3:
    st.metric(
        "Missing Skills",
        len(ats["Missing Skills"])
    )
with c4:

    st.metric(
        "Resume Score",
        f'{structure["Resume Structure Score"]}%'
    )
# =====================================================
# ATS SCORE
# =====================================================

st.divider()

st.write("")

st.subheader("🎯 ATS Score")

score = ats["ATS Score"]

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%"},
        title={"text": "ATS Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#1f77b4"},
            "steps": [
                {"range": [0, 60], "color": "#f8d7da"},
                {"range": [60, 80], "color": "#fff3cd"},
                {"range": [80, 100], "color": "#d4edda"},
            ],
        },
    )
)

gauge.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(
    gauge,
    use_container_width=True
)
if score >= 90:

    st.success("Excellent Match")

elif score >= 75:

    st.success("Good Match")

elif score >= 60:

    st.warning("Fair Match")

else:

    st.error("Needs Improvement")
# =====================================================
# SKILLS
# =====================================================

st.divider()

st.write("")

left, right = st.columns(2)

with left:

    st.subheader("✅ Matched Skills")

    if ats["Matched Skills"]:

        for skill in ats["Matched Skills"]:

            st.success(skill.title())

    else:

        st.info("No matched skills found.")

with right:

    st.subheader("❌ Missing Skills")

    if ats["Missing Skills"]:

        for skill in ats["Missing Skills"]:

            st.error(skill.title())

    else:

        st.success("No missing skills.")
# =====================================================
# RESUME STRUCTURE
# =====================================================

st.divider()

st.write("")

st.subheader("📄 Resume Structure")

sections = structure["Sections"]

for section, present in sections.items():

    if present:

        st.success(f"✔ {section.title()}")

    else:

        st.warning(f"✖ {section.title()}")
# =====================================================
# SKILL GAP
# =====================================================

st.divider()

st.write("")

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
# =====================================================
# AI RECOMMENDATIONS
# =====================================================

st.divider()

st.write("")

st.subheader("💡 AI Resume Recommendations")

for recommendation in recommendations:

    st.success(f"✔ {recommendation}")
st.divider()

st.write("")

st.subheader("📥 Download ATS Report")

with open(report_file, "rb") as pdf:

    st.download_button(
        label="Download PDF Report",
        data=pdf,
        file_name="ATS_Report.pdf",
        mime="application/pdf"
    )
# =====================================================
# TOP MATCHING JOBS
# =====================================================

st.divider()

st.write("")

st.subheader("💼 Top Matching Jobs")

top_jobs = matched_jobs.sort_values(
    by="Match_Percentage:Match %",
    ascending=False
)

st.dataframe(
    top_jobs[
        [
            "Title",
            "Company",
            "Location",
            "Experience",
            "Match %"
        ]
    ].head(10),
    use_container_width=True,
    hide_index=True
)