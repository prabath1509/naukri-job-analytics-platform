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

    h1, h2, h3 {

        color: white;
    }

    </style>
    """,

    unsafe_allow_html=True
)

# =========================================================
# LOAD DATABASE
# =========================================================

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

# =========================================================
# DATA CLEANING
# =========================================================

df = df.drop_duplicates()

# -----------------------------------------
# FILL NULL VALUES
# -----------------------------------------

fill_columns = [

    "Company",
    "Location",
    "Experience",
    "Skills",
    "Keyword",
    "Source"
]

for col in fill_columns:

    if col in df.columns:

        df[col] = df[col].fillna("Unknown")

# -----------------------------------------
# CLEAN EXPERIENCE
# -----------------------------------------

if "Experience" in df.columns:

    df["Experience"] = df["Experience"].replace(

        ["", "nan"],

        "Unknown"
    )

    top_exp = (

        df["Experience"]

        .value_counts()

        .head(10)

        .index
    )

    df["Experience"] = df["Experience"].apply(

        lambda x: x if x in top_exp else "Other"
    )

# -----------------------------------------
# CLEAN KEYWORD
# -----------------------------------------

if "Keyword" in df.columns:

    df["Keyword"] = (

        df["Keyword"]

        .astype(str)

        .str.replace("-", " ")

        .str.title()
    )

    df["Keyword"] = df["Keyword"].replace(

        "Official Company Jobs",

        "Company ATS Jobs"
    )

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Controls")

# -----------------------------------------
# SEARCH
# -----------------------------------------

search = st.sidebar.text_input(

    "Search Job Title"
)

# -----------------------------------------
# SOURCE FILTER
# -----------------------------------------

if "Source" in df.columns:

    source_filter = st.sidebar.multiselect(

        "Select Source",

        df["Source"].unique(),

        default=df["Source"].unique()
    )

else:

    source_filter = []

# -----------------------------------------
# LOCATION FILTER
# -----------------------------------------

if "Location" in df.columns:

    location_filter = st.sidebar.multiselect(

        "Select Location",

        sorted(df["Location"].unique()),

        default=sorted(df["Location"].unique())
    )

else:

    location_filter = []

# -----------------------------------------
# COMPANY FILTER
# -----------------------------------------

if "Company" in df.columns:

    company_filter = st.sidebar.multiselect(

        "Select Company",

        sorted(df["Company"].unique()),

        default=sorted(df["Company"].unique())
    )

else:

    company_filter = []

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

# -----------------------------------------
# SEARCH FILTER
# -----------------------------------------

if search:

    filtered_df = filtered_df[

        filtered_df["Title"]

        .str.contains(

            search,

            case=False,

            na=False
        )
    ]

# -----------------------------------------
# SOURCE FILTER
# -----------------------------------------

if len(source_filter) > 0:

    filtered_df = filtered_df[

        filtered_df["Source"]

        .isin(source_filter)
    ]

# -----------------------------------------
# LOCATION FILTER
# -----------------------------------------

if len(location_filter) > 0:

    filtered_df = filtered_df[

        filtered_df["Location"]

        .isin(location_filter)
    ]

# -----------------------------------------
# COMPANY FILTER
# -----------------------------------------

if len(company_filter) > 0:

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
# JOB SOURCES
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
# JOB CATEGORY
# =========================================================

st.subheader("📊 Jobs by Category")

category_counts = (

    filtered_df["Keyword"]

    .value_counts()

    .head(8)
)

fig = px.pie(

    names=category_counts.index,

    values=category_counts.values,

    hole=0.4
)

fig.update_traces(

    textposition="inside",

    textinfo="percent+label"
)

fig.update_layout(

    height=550
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

    xaxis_tickangle=-20,

    height=500
)

st.plotly_chart(

    fig,

    width="stretch"
)

# =========================================================
# TOP SKILLS
# =========================================================

st.subheader("🔥 Top Skills")

skills_series = (

    filtered_df["Skills"]

    .dropna()

    .astype(str)

    .str.split(r"[,/|]")

    .explode()
)

skills_series = (

    skills_series

    .str.strip()

    .str.title()
)

remove_skills = [

    "Not Available",

    "",

    "Nan",

    "Unknown"
]

skills_series = skills_series[

    ~skills_series.isin(remove_skills)
]

top_skills = (

    skills_series

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

    title="Top Skills Demand"
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
# LOCATION ANALYTICS
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

    xaxis_tickangle=-25,

    height=500
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

    st.success(

        f"Database Connected | Total Stored Jobs: {db_jobs['total_jobs'][0]}"
    )

    conn.close()

else:

    st.error(

        "Database not found"
    )

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
# JOB TABLE
# =========================================================

st.markdown("---")

st.subheader("📋 Job Listings")

show_columns = [

    "Title",
    "Company",
    "Experience",
    "Location",
    "Salary",
    "Source",
    "Job_Link"
]

available_columns = [

    col for col in show_columns

    if col in filtered_df.columns
]

st.dataframe(

    filtered_df[available_columns],

    width="stretch",
    height=600
)