# -----------------------------------
# IMPORTS
# -----------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import sqlite3
import os
import subprocess
import sys
import sqlite3

# -----------------------------------
# PROJECT ROOT IMPORT FIX
# -----------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# -----------------------------------
# RESUME MATCHER IMPORT
# -----------------------------------

from resume_matcher.matcher import (
    extract_resume_text,
    match_jobs
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Naukri Job Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #374151;
    padding: 15px;
    border-radius: 10px;
}

section[data-testid="stSidebar"] {
    background-color: #1e293b;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("⚙ Controls")

# -----------------------------------
# RUN SCRAPER BUTTON
# -----------------------------------

if st.sidebar.button("Run Live Scraper"):

    with st.spinner("Scraping latest jobs..."):

        try:

            scraper_path = (
                r"C:\Users\PRABATH\OneDrive\Desktop\naukri_scraper_project\main.py"
            )

            subprocess.run(
                ["python", scraper_path]
            )

            st.sidebar.success(
                "Scraping Completed"
            )

        except Exception as e:

            st.sidebar.error(
                f"Error: {e}"
            )

# -----------------------------------
# LOAD LATEST CSV
# -----------------------------------

# -----------------------------------
# LOAD DATA FROM SQLITE DATABASE
# -----------------------------------

DB_PATH = "database/jobs.db"

if os.path.exists(DB_PATH):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(

        "SELECT * FROM jobs",

        conn
    )

    conn.close()

else:

    st.error("Database not found")

    st.stop()

# -----------------------------------
# FILTERS
# -----------------------------------

st.sidebar.title("🔍 Filters")

# SOURCE FILTER

selected_sources = st.sidebar.multiselect(
    "Select Source",
    sorted(
        df["Source"]
        .dropna()
        .unique()
    )
)

# SEARCH FILTER

search = st.sidebar.text_input(
    "Search Job Title"
)

# LOCATION FILTER

selected_locations = st.sidebar.multiselect(
    "Select Location",
    sorted(
        df["Location"]
        .dropna()
        .unique()
    )
)

# COMPANY FILTER

selected_companies = st.sidebar.multiselect(
    "Select Company",
    sorted(
        df["Company"]
        .dropna()
        .unique()
    )
)

# EXPERIENCE FILTER

selected_experience = st.sidebar.multiselect(
    "Select Experience",
    sorted(
        df["Experience"]
        .dropna()
        .unique()
    )
)

# KEYWORD FILTER

if "Keyword" in df.columns:

    selected_keywords = st.sidebar.multiselect(
        "Select Job Keyword",
        sorted(
            df["Keyword"]
            .dropna()
            .unique()
        )
    )

# -----------------------------------
# APPLY FILTERS
# -----------------------------------

if selected_sources:

    df = df[
        df["Source"]
        .isin(selected_sources)
    ]

if search:

    df = df[
        df["Title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if selected_locations:

    df = df[
        df["Location"]
        .isin(selected_locations)
    ]

if selected_companies:

    df = df[
        df["Company"]
        .isin(selected_companies)
    ]

if selected_experience:

    df = df[
        df["Experience"]
        .isin(selected_experience)
    ]

if "Keyword" in df.columns:

    if selected_keywords:

        df = df[
            df["Keyword"]
            .isin(selected_keywords)
        ]

# -----------------------------------
# TITLE
# -----------------------------------

st.title("📊 Multi-Source Job Analytics Dashboard")

st.markdown(
    "## Real-Time Job Market Insights"
)

st.markdown("---")

# -----------------------------------
# KPI METRICS
# -----------------------------------

total_jobs = len(df)

total_companies = (
    df["Company"]
    .nunique()
)

total_locations = (
    df["Location"]
    .nunique()
)

avg_jobs_per_company = round(
    total_jobs / total_companies,
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Jobs",
    total_jobs
)

col2.metric(
    "Companies Hiring",
    total_companies
)

col3.metric(
    "Locations",
    total_locations
)

col4.metric(
    "Avg Jobs / Company",
    avg_jobs_per_company
)

st.markdown("---")

# -----------------------------------
# JOB TABLE
# -----------------------------------

st.subheader("📋 Job Listings")

display_df = df.copy()

display_df["Skills"] = (
    display_df["Skills"]
    .astype(str)
    .str[:40]
)

st.data_editor(

    display_df,

    column_config={

        "Job_Link":
        st.column_config.LinkColumn(
            "Apply Link",
            display_text="Open Job"
        )
    },

    hide_index=True,

    use_container_width=True,

    height=500
)

# -----------------------------------
# RESUME MATCHER AI
# -----------------------------------

st.markdown("---")

st.subheader("📄 Resume Matcher AI")

uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_resume is not None:

    with st.spinner("Analyzing Resume..."):

        resume_text = extract_resume_text(
            uploaded_resume
        )

        matched_jobs = match_jobs(
            resume_text,
            df
        )

        st.success(
            "Resume Analyzed Successfully"
        )

        st.subheader(
            "🎯 Top Matching Jobs"
        )

        st.data_editor(

            matched_jobs[
                [
                    "Source",
                    "Title",
                    "Company",
                    "Skills",
                    "Match_Percentage",
                    "Job_Link"
                ]
            ].head(20),

            column_config={

                "Job_Link":
                st.column_config.LinkColumn(
                    "Apply Link"
                )
            },

            hide_index=True,

            use_container_width=True,

            height=500
        )

# -----------------------------------
# TOP COMPANIES
# -----------------------------------

st.subheader("🏢 Top Hiring Companies")

top_companies = (

    df["Company"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_companies.columns = [
    "Company",
    "Jobs"
]

fig1 = px.bar(

    top_companies,

    x="Company",
    y="Jobs",

    title="Top Hiring Companies"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -----------------------------------
# TOP LOCATIONS
# -----------------------------------

st.subheader("📍 Top Hiring Locations")

top_locations = (

    df["Location"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_locations.columns = [
    "Location",
    "Jobs"
]

fig2 = px.pie(

    top_locations,

    names="Location",
    values="Jobs",

    title="Location Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# TOP SKILLS ANALYSIS
# -----------------------------------

st.subheader("🛠 Most Demanded Skills")

skills_series = (

    df["Skills"]
    .dropna()
    .astype(str)
)

skills_list = []

known_skills = [

    "Python",
    "SQL",
    "Excel",
    "Tableau",
    "Power BI",
    "Machine Learning",
    "Data Analysis",
    "Statistics",
    "Pandas",
    "NumPy",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Visualization",
    "ETL",
    "Spark",
    "Hadoop",
    "AWS",
    "Azure",
    "Git",
    "TensorFlow",
    "PyTorch",
    "Business Analysis",
    "Data Engineering",
    "Airflow",
    "Snowflake",
    "BigQuery"
]

for text in skills_series:

    lower_text = text.lower()

    for skill in known_skills:

        if skill.lower() in lower_text:

            skills_list.append(skill)

top_skills = Counter(
    skills_list
).most_common(15)

skills_df = pd.DataFrame(

    top_skills,

    columns=[
        "Skill",
        "Count"
    ]
)

skills_df = skills_df.sort_values(
    by="Count",
    ascending=True
)

fig3 = px.bar(

    skills_df,

    x="Count",
    y="Skill",

    orientation="h",

    text="Count",

    title="Top Skills Demand"
)

fig3.update_layout(

    height=600,

    yaxis=dict(
        title=""
    ),

    xaxis=dict(
        title="Job Count"
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# EXPERIENCE ANALYSIS
# -----------------------------------

st.subheader("💼 Experience Requirements")

experience_df = (

    df["Experience"]
    .value_counts()
    .head(10)
    .reset_index()
)

experience_df.columns = [
    "Experience",
    "Jobs"
]

fig4 = px.bar(

    experience_df,

    x="Experience",
    y="Jobs",

    title="Experience Distribution"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -----------------------------------
# KEYWORD ANALYSIS
# -----------------------------------

if "Keyword" in df.columns:

    st.subheader("🔑 Job Category Distribution")

    keyword_df = (

        df["Keyword"]
        .value_counts()
        .reset_index()
    )

    keyword_df.columns = [
        "Keyword",
        "Jobs"
    ]

    fig5 = px.pie(

        keyword_df,

        names="Keyword",
        values="Jobs",

        title="Jobs by Category"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# -----------------------------------
# SOURCE DISTRIBUTION
# -----------------------------------

st.subheader("🌐 Job Sources")

source_df = (
    df["Source"]
    .value_counts()
    .reset_index()
)

source_df.columns = [
    "Source",
    "Jobs"
]

fig6 = px.pie(

    source_df,

    names="Source",
    values="Jobs",

    title="Jobs by Source"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# -----------------------------------
# DOWNLOAD BUTTON
# -----------------------------------

st.markdown("---")

csv = df.to_csv(index=False)

st.download_button(

    label="⬇ Download Filtered Jobs",

    data=csv,

    file_name="filtered_jobs.csv",

    mime="text/csv"
)

# -----------------------------------
# DATABASE STATUS
# -----------------------------------

# -----------------------------------
# DATABASE STATUS
# -----------------------------------

st.markdown("---")

st.subheader("🗄 SQLite Database Status")

db_path = "database/jobs.db"

if os.path.exists(db_path):

    conn = sqlite3.connect(db_path)

    query = """

    SELECT COUNT(*) as total_jobs

    FROM jobs

    """

    db_jobs = pd.read_sql(

        query,

        conn
    )

    st.success(

        f"Database Connected | Total Stored Jobs: {db_jobs['total_jobs'][0]}"
    )

    conn.close()

else:

    st.error(

        "Database not found"
    )

st.markdown("""
### 🚀 Project Features

- Multi-Source Job Scraping
- Naukri + Official Company Jobs
- Greenhouse ATS Integration
- Lever ATS Integration
- SQLite Database Storage
- Resume Matcher AI
- Interactive Dashboard
- Plotly Visualizations
- Search & Filtering
- Downloadable Job Dataset
- Skills Analytics
- Job Source Analytics
""")