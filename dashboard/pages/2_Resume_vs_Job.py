import os
import sys
import sqlite3

import pandas as pd
import streamlit as st

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
from resume_matcher.report_generator import generate_pdf

from resume_matcher.resume_readiness import calculate_resume_readiness
from resume_matcher.resume_rewriter import generate_resume_rewrite
from resume_matcher.job_fit_engine import calculate_job_fit
from resume_matcher.interview_readiness import calculate_interview_readiness
from resume_matcher.interview_questions import generate_interview_questions
from resume_matcher.recruiter_engine import recruiter_decision

from dashboard.components.dashboard_metrics import render_dashboard_metrics
from dashboard.components.resume_section import render_resume_section
from dashboard.components.job_match_section import render_job_match_section
from dashboard.components.career_section import render_career_section
from dashboard.components.interview_section import render_interview_section
from dashboard.components.recruiter_section import render_recruiter_section
from dashboard.components.export_section import render_export_section

from services.resume_service import analyze_resume
from services.job_service import analyze_jobs
from services.career_service import analyze_career

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
    page_title="ATS Resume Checker",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ATS Resume Checker")

st.caption(
    "Analyze your resume against live jobs from your analytics platform."
)

jobs_df = load_jobs()
# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Resume")

uploaded_resume = st.sidebar.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_resume is None:
    st.info("Please upload your resume to continue.")
    st.stop()

resume_text = extract_resume_text(uploaded_resume)

# =====================================================
# JOB SELECTION
# =====================================================

st.sidebar.header("Job Selection")

job_titles = (
    jobs_df["Title"]
    .fillna("Unknown Role")
    .drop_duplicates()
    .sort_values()
    .tolist()
)
selected_job = st.sidebar.selectbox(
    "Choose Job",
    job_titles
)

selected_job_df = jobs_df[
    jobs_df["Title"] == selected_job
]

if selected_job_df.empty:
    st.error("Selected job not found.")
    st.stop()

job = selected_job_df.iloc[0]

job_description = ""

for column in [
    "Skills",
    "Experience",
    "Job_Category",
    "Role_Category",
    "Company",
    "Location",
    "Work_Mode"
]:
    if column in job.index and pd.notna(job[column]):
        job_description += f"{column}: {job[column]}\n"

job_description = job_description.strip()

if not job_description:
    st.error("Job description is empty.")
    st.stop()
# =====================================================
# ANALYSIS
# =====================================================

with st.spinner("Analyzing resume..."):

    # Resume Analysis
    resume_analysis = analyze_resume(
    resume_text,
    job_description
)

    # Job Analysis
    job_analysis = analyze_jobs(
    job,
    jobs_df,
    resume_text
)

    # Career Analysis
    career_analysis = analyze_career(
    resume_analysis["candidate_experience"],
    resume_analysis["candidate_education"],
    resume_analysis["candidate_projects"],
    resume_analysis["candidate_certifications"],
    job_analysis["job_info"],
    resume_analysis["ats"],
    resume_analysis["gap"],
    resume_analysis["structure"]
)

    # Resume Readiness
    readiness = calculate_resume_readiness(
    resume_analysis["ats"],
    resume_analysis["candidate_experience"],
    resume_analysis["candidate_projects"],
    resume_analysis["candidate_certifications"],
    resume_analysis["candidate_education"],
    resume_analysis["structure"],
    job_analysis["job_info"]
)

    # =====================================================
# AI Resume Rewrite
# =====================================================

rewrite = generate_resume_rewrite(
    resume_analysis["candidate_experience"],
    resume_analysis["candidate_projects"],
    resume_analysis["candidate_certifications"],
    resume_analysis["candidate_education"],
    job_analysis["job_info"]
)

# =====================================================
# Job Fit
# =====================================================

job_fit = calculate_job_fit(
    resume_analysis["ats"],
    resume_analysis["candidate_experience"],
    resume_analysis["candidate_projects"],
    resume_analysis["candidate_certifications"],
    resume_analysis["candidate_education"],
    job_analysis["job_info"],
    resume_analysis["gap"],
    resume_analysis["structure"]
)

# =====================================================
# Interview Readiness
# =====================================================

interview = calculate_interview_readiness(
    resume_analysis["ats"],
    resume_analysis["candidate_projects"],
    resume_analysis["candidate_certifications"],
    resume_analysis["candidate_experience"],
    resume_analysis["candidate_education"]
)

# =====================================================
# Interview Questions
# =====================================================

interview_questions = generate_interview_questions(
    job_analysis["job_info"],
    resume_analysis["gap"]
)

# =====================================================
# Recruiter Decision
# =====================================================

recruiter = recruiter_decision(
    job_fit,
    interview,
    career_analysis["recommendations"],
    resume_analysis["candidate_experience"],
    job_analysis["job_info"]
)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📊 Dashboard",
        "📄 Resume",
        "🎯 Job Match",
        "🛣 Career",
        "🎤 Interview",
        "👨‍💼 Recruiter",
        "📥 Export"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

with tab1:
    render_dashboard_metrics(
        resume_analysis["ats"],
        readiness,
        job_fit,
        interview,
        recruiter
    )
# =====================================================
# RESUME
# =====================================================

with tab2:
    render_resume_section(
        resume_analysis["ats"],
        resume_analysis["gap"],
        resume_analysis["structure"],
        readiness,
        resume_analysis["candidate_experience"],
        resume_analysis["candidate_education"],
        resume_analysis["candidate_projects"],
        resume_analysis["candidate_certifications"],
        rewrite
    )
# =====================================================
# JOB MATCH
# =====================================================

with tab3:
    render_job_match_section(
        job_analysis["job_info"],
        resume_analysis["gap"],
        job_analysis["matched_jobs"]
    )
# =====================================================
# CAREER
# =====================================================

with tab4:
    render_career_section(
        career_analysis["recommendations"],
        career_analysis["roadmap"],
        career_analysis["optimizer"]
    )
# =====================================================
# INTERVIEW
# =====================================================

with tab5:
    render_interview_section(
        interview,
        interview_questions
    )
# =====================================================
# RECRUITER
# =====================================================

with tab6:
    render_recruiter_section(
        recruiter
    )
# =====================================================
# EXPORT
# =====================================================

with tab7:

    output_file = "ATS_Report.pdf"

    generate_pdf(
        output_file,
        resume_analysis["ats"],
        resume_analysis["gap"],
        resume_analysis["structure"],
        career_analysis["recommendations"]
    )

    render_export_section(output_file)