# =========================================================
# AI POWERED JOB ANALYTICS PLATFORM
# dashboard/app.py
# =========================================================

import os
import sys
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PROJECT ROOT IMPORT PATH
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from analytics.experience_frequency import classify_experience
# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Powered Job Analytics Platform",
    page_icon="📊",
    layout="wide",
)


# =========================================================
# PATHS
# =========================================================

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "database",
    "jobs.db",
)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_jobs():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql("SELECT * FROM jobs", conn)
    finally:
        conn.close()

    return df


@st.cache_data
def load_analytics(filename):
    path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(path):
        return pd.DataFrame()

    return pd.read_csv(path)


df = load_jobs()

if df.empty:
    st.error("Job database is empty or database/jobs.db was not found.")
    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

text_columns = [
    "Title",
    "Company",
    "Location",
    "Experience",
    "Salary",
    "Skills",
    "Keyword",
    "Source",
    "Posted_Date",
    "Work_Mode",
    "Job_Link",
    "Role_Category",
]

for column in text_columns:
    if column in df.columns:
        df[column] = df[column].fillna("Not Available").astype(str)


df["Experience_Level"] = df["Experience"].apply(
    classify_experience
)

df["Experience_Level"] = df["Experience_Level"].fillna(
    "Not Available"
)


# =========================================================
# LOAD ANALYTICS OUTPUTS
# =========================================================

skill_frequency = load_analytics("skill_frequency.csv")
company_frequency = load_analytics("company_frequency.csv")
location_frequency = load_analytics("location_frequency.csv")
workmode_frequency = load_analytics("workmode_frequency.csv")
experience_frequency = load_analytics("experience_frequency.csv")
role_frequency = load_analytics("role_frequency.csv")
salary_frequency = load_analytics("salary_frequency.csv")
source_quality = load_analytics("source_quality.csv")
field_quality = load_analytics("field_quality.csv")


# =========================================================
# HEADER
# =========================================================

st.title("📊 AI Powered Job Analytics Platform")

st.markdown(
    """
    **Multi-source job market intelligence platform**

    Explore job demand, skills, companies, locations, experience,
    salaries, work modes and data-source quality.
    """
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")

search = st.sidebar.text_input(
    "Search Job Title"
)

source_filter = st.sidebar.multiselect(
    "Source",
    sorted(df["Source"].unique()),
)

workmode_filter = st.sidebar.multiselect(
    "Work Mode",
    sorted(df["Work_Mode"].unique()),
)

role_filter = st.sidebar.multiselect(
    "Role Category",
    sorted(df["Role_Category"].unique()),
)

role_chart_depth = st.sidebar.selectbox(
    "Role Chart Depth",
    ["Top 10", "Top 15", "Top 20", "All Roles"],
    index=1,
)

experience_options = [
    "Fresher",
    "0-2 Years",
    "2-5 Years",
    "5-10 Years",
    "10+ Years",
    "Not Available",
]

experience_filter = st.sidebar.multiselect(
    "Experience Level",
    experience_options,
)

company_filter = st.sidebar.multiselect(
    "Company",
    sorted(df["Company"].unique()),
)

location_search = st.sidebar.text_input(
    "Search Location"
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(
            search,
            case=False,
            na=False,
        )
    ]

if source_filter:
    filtered_df = filtered_df[
        filtered_df["Source"].isin(source_filter)
    ]

if workmode_filter:
    filtered_df = filtered_df[
        filtered_df["Work_Mode"].isin(workmode_filter)
    ]

if role_filter:
    filtered_df = filtered_df[
        filtered_df["Role_Category"].isin(role_filter)
    ]

if experience_filter:
    filtered_df = filtered_df[
        filtered_df["Experience_Level"].isin(
            experience_filter
        )
    ]

if company_filter:
    filtered_df = filtered_df[
        filtered_df["Company"].isin(company_filter)
    ]

if location_search:
    filtered_df = filtered_df[
        filtered_df["Location"].str.contains(
            location_search,
            case=False,
            na=False,
        )
    ]


# =========================================================
# KPI METRICS
# =========================================================

total_jobs = len(filtered_df)
companies = filtered_df["Company"].nunique()
locations = filtered_df["Location"].nunique()
sources = filtered_df["Source"].nunique()

remote_jobs = (
    filtered_df["Work_Mode"]
    .eq("Remote")
    .sum()
)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Total Jobs",
    f"{total_jobs:,}",
)

k2.metric(
    "Companies Hiring",
    f"{companies:,}",
)

k3.metric(
    "Locations",
    f"{locations:,}",
)

k4.metric(
    "Sources",
    sources,
)

k5.metric(
    "Remote Jobs",
    f"{remote_jobs:,}",
)

st.divider()


# =========================================================
# FILTERED DATA DOWNLOAD
# =========================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_job_dataset.csv",
    mime="text/csv",
)

st.caption(
    f"Showing analytics for {len(filtered_df):,} "
    f"of {len(df):,} jobs."
)


# =========================================================
# FILTERED SOURCE AND ROLE ANALYTICS
# =========================================================

left, right = st.columns(2)

with left:
    st.subheader("Jobs by Source")

    source_counts = (
        filtered_df["Source"]
        .value_counts()
        .reset_index()
    )

    source_counts.columns = [
        "Source",
        "Jobs",
    ]

    fig = px.pie(
        source_counts,
        names="Source",
        values="Jobs",
        hole=0.5,
    )

    fig.update_traces(
        textinfo="label+percent"
    )

    st.plotly_chart(
    fig,
    width="stretch"
)


with right:
    st.subheader("Role Demand")

    role_counts = (
        filtered_df["Role_Category"]
        .value_counts()
    )

    role_depth_map = {
        "Top 10": 10,
        "Top 15": 15,
        "Top 20": 20,
    }

    if role_chart_depth in role_depth_map:
        role_counts = role_counts.head(
            role_depth_map[role_chart_depth]
        )

    role_counts = (
        role_counts
        .sort_values()
        .reset_index()
    )
    role_counts.columns = [
        "Role Category",
        "Jobs",
    ]

    fig = px.bar(
        role_counts,
        x="Jobs",
        y="Role Category",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =========================================================
# SKILL DEMAND
# =========================================================

st.subheader("🔥 Most In-Demand Skills")

all_skills = []

for skill_string in filtered_df["Skills"]:
    value = str(skill_string).strip()

    if value.casefold() in {
        "",
        "not available",
        "nan",
        "none",
        "unknown",
    }:
        continue

    for skill in value.split(","):
        skill = skill.strip()

        if len(skill) > 1:
            all_skills.append(skill)


if all_skills:
    filtered_skills = pd.Series(
        all_skills
    ).value_counts().head(20)

    skill_df = filtered_skills.reset_index()

    skill_df.columns = [
        "Skill",
        "Jobs",
    ]

    skill_df = skill_df.sort_values(
        "Jobs"
    )

    fig = px.bar(
        skill_df,
        x="Jobs",
        y="Skill",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

else:
    st.info(
        "No skill data is available for the selected filters."
    )


# =========================================================
# COMPANY AND LOCATION DEMAND
# =========================================================

left, right = st.columns(2)

with left:
    st.subheader("Top Hiring Companies")

    company_counts = (
        filtered_df["Company"]
        .value_counts()
        .head(15)
        .sort_values()
        .reset_index()
    )

    company_counts.columns = [
        "Company",
        "Jobs",
    ]

    fig = px.bar(
        company_counts,
        x="Jobs",
        y="Company",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


with right:
    st.subheader("Top Job Locations")

    locations = []

    for location_string in filtered_df["Location"]:
        value = str(location_string).strip()

        if value.casefold() in {
            "",
            "not available",
            "unknown",
            "nan",
        }:
            continue

        value = value.replace(
            "Hybrid - ",
            ""
        )

        value = value.replace(
            "Remote - ",
            ""
        )

        for location in value.split(","):
            location = location.strip()

            if location:
                locations.append(location)

    location_counts = (
        pd.Series(locations)
        .value_counts()
        .head(15)
        .sort_values()
        .reset_index()
    )

    location_counts.columns = [
        "Location",
        "Jobs",
    ]

    fig = px.bar(
        location_counts,
        x="Jobs",
        y="Location",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =========================================================
# WORK MODE AND EXPERIENCE
# =========================================================

left, right = st.columns(2)

with left:
    st.subheader("Work Mode Distribution")

    workmode_counts = (
        filtered_df["Work_Mode"]
        .value_counts()
        .reset_index()
    )

    workmode_counts.columns = [
        "Work Mode",
        "Jobs",
    ]

    fig = px.pie(
        workmode_counts,
        names="Work Mode",
        values="Jobs",
        hole=0.45,
    )

    fig.update_traces(
        textinfo="label+percent"
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


with right:
    st.subheader("Experience Demand")

    experience_order = [
        "Fresher",
        "0-2 Years",
        "2-5 Years",
        "5-10 Years",
        "10+ Years",
    ]

    experience_counts = (
        filtered_df[
            filtered_df["Experience_Level"]
            != "Not Available"
        ]["Experience_Level"]
        .value_counts()
        .reindex(
            experience_order,
            fill_value=0,
        )
        .reset_index()
    )

    experience_counts.columns = [
        "Experience Level",
        "Jobs",
    ]

    fig = px.bar(
        experience_counts,
        x="Experience Level",
        y="Jobs",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# =========================================================
# SALARY ANALYTICS
# =========================================================

st.subheader("Salary Demand")

if not salary_frequency.empty:
    parsed_salary_jobs = int(
        salary_frequency["Job_Count"].sum()
    )

    salary_coverage = (
        parsed_salary_jobs / len(df) * 100
    )

    st.info(
        f"Salary analytics is based on "
        f"{parsed_salary_jobs:,} parsed salary records "
        f"({salary_coverage:.2f}% of the current dataset). "
        "Salary values are not disclosed for most jobs."
    )

    paid_salary = salary_frequency[
        salary_frequency["Salary_Bucket"]
        != "Unpaid"
    ].copy()

    fig = px.bar(
        paid_salary,
        x="Salary_Bucket",
        y="Job_Count",
        hover_data=[
            "Paid_Share_Percentage"
        ],
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

else:
    st.info(
        "Salary analytics file is not available."
    )


# =========================================================
# DATA QUALITY
# =========================================================

st.subheader("Data Quality Intelligence")

quality_tab, source_tab = st.tabs(
    [
        "Field Coverage",
        "Source Quality",
    ]
)


with quality_tab:
    if not field_quality.empty:
        quality_df = field_quality.sort_values(
            "Coverage_Percentage"
        )

        fig = px.bar(
            quality_df,
            x="Coverage_Percentage",
            y="Field",
            orientation="h",
            text="Coverage_Percentage",
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%"
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

        st.dataframe(
            field_quality,
            width="stretch",
            hide_index=True,
        )


with source_tab:
    if not source_quality.empty:
        st.dataframe(
            source_quality,
            width="stretch",
            hide_index=True,
        )


# =========================================================
# JOB LISTINGS
# =========================================================

st.subheader("📋 Job Listings")

listing_columns = [
    "Title",
    "Company",
    "Location",
    "Experience",
    "Work_Mode",
    "Role_Category",
    "Source",
    "Posted_Date",
    "Job_Link",
]

job_listings = filtered_df[
    listing_columns
].copy()

st.dataframe(
    job_listings,
    width="stretch",
    hide_index=True,
    column_config={
        "Job_Link": st.column_config.LinkColumn(
            "Apply",
            display_text="Open Job",
        )
    },
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    f"AI Powered Job Analytics Platform | "
    f"{len(df):,} validated jobs | "
    f"{df['Source'].nunique()} job sources"
)
