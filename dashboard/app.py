# =========================================================
# AI POWERED JOB ANALYTICS DASHBOARD
# FILE: dashboard/app.py
# =========================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="AI Job Analytics Platform",

    page_icon="📊",

    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3, h4 {
        color: white;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    table, th, td {
        border: 1px solid #333;
    }

    th {
        background-color: #1f2937;
        color: white;
        padding: 10px;
        text-align: left;
    }

    td {
        padding: 8px;
    }

    a {
        color: #4da6ff;
        text-decoration: none;
        font-weight: bold;
    }

    a:hover {
        color: #66ccff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = "database/jobs.db"

# =========================================================
# LOAD DATABASE
# =========================================================

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

# =========================================================
# REMOVE DUPLICATES
# =========================================================

df = df.drop_duplicates()

# =========================================================
# FILL NULL VALUES
# =========================================================

fill_columns = [

    "Title",
    "Company",
    "Location",
    "Experience",
    "Skills",
    "Keyword",
    "Source",
    "Salary",
    "Job_Link"
]

for col in fill_columns:

    if col in df.columns:

        df[col] = df[col].fillna("Unknown")

# =========================================================
# CLEAN SOURCE NAMES
# =========================================================

if "Source" in df.columns:

    df["Source"] = (

        df["Source"]

        .astype(str)

        .replace({

            "Official Company Jobs": "Company ATS",

            "Greenhouse Jobs": "Company ATS",

            "Lever Jobs": "Company ATS",

            "Lever": "Company ATS",

            "Ashby": "Company ATS",

            "Workday": "Company ATS",

            "Greenhouse": "Company ATS"
        })
    )

# =========================================================
# CLEAN KEYWORDS
# =========================================================

if "Keyword" in df.columns:

    df["Keyword"] = (

        df["Keyword"]

        .astype(str)

        .str.replace("-", " ")

        .str.title()
    )

# =========================================================
# CLEAN EXPERIENCE
# =========================================================

if "Experience" in df.columns:

    df["Experience"] = (

        df["Experience"]

        .astype(str)

        .str.strip()
    )

    remove_exp = [

        "Unknown",
        "Other",
        "Not Available",
        "",
        "nan",
        "None"
    ]

    df = df[

        ~df["Experience"]

        .isin(remove_exp)
    ]

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Controls")

# =========================================================
# SEARCH
# =========================================================

search = st.sidebar.text_input(

    "Search Job Title"
)

# =========================================================
# SOURCE FILTER
# =========================================================

source_filter = st.sidebar.multiselect(

    "Select Source",

    options=sorted(df["Source"].unique())
)

# =========================================================
# LOCATION FILTER
# =========================================================

location_filter = st.sidebar.multiselect(

    "Select Location",

    options=sorted(df["Location"].unique())
)

# =========================================================
# COMPANY FILTER
# =========================================================

company_filter = st.sidebar.multiselect(

    "Select Company",

    options=sorted(df["Company"].unique())
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

# =========================================================
# SEARCH FILTER
# =========================================================

if search:

    filtered_df = filtered_df[

        filtered_df["Title"]

        .str.contains(

            search,

            case=False,

            na=False
        )
    ]

# =========================================================
# SOURCE FILTER
# =========================================================

if source_filter:

    filtered_df = filtered_df[

        filtered_df["Source"]

        .isin(source_filter)
    ]

# =========================================================
# LOCATION FILTER
# =========================================================

if location_filter:

    filtered_df = filtered_df[

        filtered_df["Location"]

        .isin(location_filter)
    ]

# =========================================================
# COMPANY FILTER
# =========================================================

if company_filter:

    filtered_df = filtered_df[

        filtered_df["Company"]

        .isin(company_filter)
    ]

# =========================================================
# TITLE
# =========================================================

st.title("📊 AI Powered Job Analytics Platform")

st.markdown(

    "### Real-Time Multi-Source Job Market Intelligence"
)

# =========================================================
# METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Total Jobs",

        len(filtered_df)
    )

with col2:

    st.metric(

        "Companies Hiring",

        filtered_df["Company"].nunique()
    )

with col3:

    st.metric(

        "Locations",

        filtered_df["Location"].nunique()
    )

with col4:

    st.metric(

        "Sources",

        filtered_df["Source"].nunique()
    )

st.markdown("---")

# =========================================================
# JOB SOURCES CHART
# =========================================================

st.subheader("🌍 Job Sources")

source_counts = (

    filtered_df["Source"]

    .value_counts()
)

fig = px.pie(

    names=source_counts.index,

    values=source_counts.values,

    hole=0.5
)

fig.update_traces(

    textinfo="percent+label"
)

fig.update_layout(

    height=500
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# CATEGORY CHART
# =========================================================

st.subheader("📊 Top Job Categories")

category_df = filtered_df.copy()

category_df = category_df[

    category_df["Keyword"] != "Company Ats Jobs"
]

category_counts = (

    category_df["Keyword"]

    .value_counts()

    .head(5)
)

fig = px.bar(

    x=category_counts.index,

    y=category_counts.values,

    labels={

        "x": "Category",

        "y": "Jobs"
    },

    title="Top Job Categories"
)

fig.update_layout(

    xaxis_tickangle=-25,

    height=500
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# EXPERIENCE LEVELS
# =========================================================

st.subheader("💼 Experience Levels")

exp_counts = (

    filtered_df["Experience"]

    .value_counts()

    .head(10)
)

fig = px.bar(

    x=exp_counts.index,

    y=exp_counts.values,

    labels={

        "x": "Experience",

        "y": "Jobs"
    },

    title="Jobs by Experience"
)

fig.update_layout(

    xaxis_tickangle=-20,

    height=500
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# TOP COMPANIES
# =========================================================

st.subheader("🏢 Top Hiring Companies")

top_companies = (

    filtered_df["Company"]

    .value_counts()

    .head(10)
)

fig = px.bar(

    x=top_companies.index,

    y=top_companies.values,

    labels={

        "x": "Company",

        "y": "Jobs"
    },

    title="Top Hiring Companies"
)

fig.update_layout(

    xaxis_tickangle=-45,

    height=550
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# TOP SKILLS
# =========================================================

st.subheader("🔥 Most In-Demand Skills")

skills_text = (

    filtered_df["Skills"]

    .dropna()

    .astype(str)
)

all_skills = []

for row in skills_text:

    row = row.replace("|", ",")

    row = row.replace("/", ",")

    row = row.replace(";", ",")

    row = row.replace("\n", ",")

    parts = row.split(",")

    for skill in parts:

        skill = skill.strip().title()

        if (

            len(skill) < 2
            or len(skill) > 30
            or "Data Analysisdata" in skill
            or "Pythondevelopment" in skill
            or "Unknown" in skill
            or "Nan" in skill
            or skill.isdigit()
        ):

            continue

        all_skills.append(skill)

skills_df = pd.Series(all_skills)

top_skills = (

    skills_df

    .value_counts()

    .head(15)
)

fig = px.bar(

    x=top_skills.index,

    y=top_skills.values,

    labels={

        "x": "Skill",

        "y": "Jobs"
    },

    title="Top Skills in Demand"
)

fig.update_layout(

    xaxis_tickangle=-40,

    height=600
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# TOP LOCATIONS
# =========================================================

st.subheader("📍 Top Hiring Locations")

top_locations = (

    filtered_df["Location"]

    .value_counts()

    .head(10)
)

fig = px.bar(

    x=top_locations.index,

    y=top_locations.values,

    labels={

        "x": "Location",

        "y": "Jobs"
    },

    title="Top Hiring Locations"
)

fig.update_layout(

    xaxis_tickangle=-35,

    height=550
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# DATABASE STATUS
# =========================================================

st.markdown("---")

st.subheader("🗄 SQLite Database Status")

if os.path.exists(DB_PATH):

    conn = sqlite3.connect(DB_PATH)

    query = """

    SELECT COUNT(*) as total_jobs

    FROM jobs

    """

    db_jobs = pd.read_sql(

        query,

        conn
    )

    conn.close()

    st.success(

        f"Database Connected | Total Stored Jobs: {db_jobs['total_jobs'][0]}"
    )

else:

    st.error("Database not found")

# =========================================================
# DOWNLOAD CSV
# =========================================================

st.markdown("---")

csv = filtered_df.to_csv(

    index=False
)

st.download_button(

    label="📥 Download Jobs CSV",

    data=csv,

    file_name="jobs.csv",

    mime="text/csv"
)

# =========================================================
# JOB LISTINGS TABLE
# =========================================================

st.markdown("---")

st.subheader("📋 Job Listings")

display_df = filtered_df.copy()

# =========================================================
# CLICKABLE LINKS
# =========================================================

display_df["Apply"] = display_df["Job_Link"].apply(

    lambda x:

    f'<a href="{x}" target="_blank">Apply Now</a>'

    if x != "Unknown"

    else "N/A"
)

show_columns = [

    "Title",
    "Company",
    "Experience",
    "Location",
    "Salary",
    "Source",
    "Apply"
]

show_columns = [

    col for col in show_columns

    if col in display_df.columns
]

st.write(

    display_df[show_columns]

    .to_html(

        escape=False,

        index=False
    ),

    unsafe_allow_html=True
)