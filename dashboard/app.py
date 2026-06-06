# =========================================================
# AI JOB ANALYTICS DASHBOARD
# dashboard/app.py
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
    page_title="AI Powered Job Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# LOAD DATABASE
# =========================================================

DB_PATH = "database/jobs.db"

if not os.path.exists(DB_PATH):
    st.error("Database not found")
    st.stop()

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    "SELECT * FROM jobs",
    conn
)

conn.close()

# =========================================================
# CLEAN DATA
# =========================================================

df = df.drop_duplicates()

df.fillna("Not Available", inplace=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙ Dashboard Filters")

search = st.sidebar.text_input(
    "Search Job Title"
)

source_filter = st.sidebar.multiselect(
    "Select Source",
    sorted(df["Source"].astype(str).unique())
)

location_filter = st.sidebar.multiselect(
    "Select Location",
    sorted(df["Location"].astype(str).unique())
)

experience_filter = st.sidebar.multiselect(
    "Select Experience",
    sorted(
        df["Experience"]
        .astype(str)
        .replace("Not Available", pd.NA)
        .dropna()
        .unique()
    )
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Title"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if source_filter:
    filtered_df = filtered_df[
        filtered_df["Source"]
        .isin(source_filter)
    ]

if location_filter:
    filtered_df = filtered_df[
        filtered_df["Location"]
        .isin(location_filter)
    ]

if experience_filter:
    filtered_df = filtered_df[
        filtered_df["Experience"]
        .isin(experience_filter)
    ]

# =========================================================
# HEADER
# =========================================================

st.title("📊 AI Powered Job Analytics Platform")

st.markdown(
    "### Real-Time Multi-Source Job Market Intelligence"
)

# =========================================================
# METRICS
# =========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Jobs",
    len(filtered_df)
)

c2.metric(
    "Companies Hiring",
    filtered_df["Company"].nunique()
)

c3.metric(
    "Locations",
    filtered_df["Location"].nunique()
)

c4.metric(
    "Sources",
    filtered_df["Source"].nunique()
)

st.markdown("---")

# =========================================================
# DOWNLOAD DATASET
# =========================================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Dataset",
    data=csv,
    file_name="job_dataset.csv",
    mime="text/csv"
)

# =========================================================
# JOB SOURCES
# =========================================================

st.header("🌍 Job Sources")

source_counts = (
    filtered_df["Source"]
    .value_counts()
)

fig = px.pie(
    names=source_counts.index,
    values=source_counts.values,
    hole=0.5,
    title="Jobs by Source"
)

fig.update_traces(
    textinfo="label+percent"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# TOP JOB CATEGORIES
# =========================================================

st.header("📈 Top Job Categories")

category_df = (
    filtered_df["Keyword"]
    .astype(str)
    .value_counts()
    .head(10)
    .reset_index()
)

category_df.columns = [
    "Category",
    "Jobs"
]

fig = px.bar(
    category_df,
    x="Category",
    y="Jobs",
    title="Top Job Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# EXPERIENCE ANALYSIS
# =========================================================

st.header("📊 Experience Distribution")

exp_df = filtered_df[
    filtered_df["Experience"] != "Not Available"
]

if len(exp_df) > 0:

    experience_counts = (
        exp_df["Experience"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    experience_counts.columns = [
        "Experience",
        "Jobs"
    ]

    fig = px.bar(
        experience_counts,
        x="Experience",
        y="Jobs",
        title="Jobs by Experience"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# TOP COMPANIES
# =========================================================

st.header("🏢 Top Hiring Companies")

company_df = (
    filtered_df["Company"]
    .value_counts()
    .head(10)
    .reset_index()
)

company_df.columns = [
    "Company",
    "Jobs"
]

fig = px.bar(
    company_df,
    x="Company",
    y="Jobs",
    title="Top Hiring Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# SKILLS ANALYSIS
# =========================================================

st.header("🔥 Most In-Demand Skills")

all_skills = []

for skill_string in filtered_df["Skills"]:

    if pd.isna(skill_string):
        continue

    if str(skill_string).lower() == "not available":
        continue

    skills = str(skill_string).split(",")

    for skill in skills:

        skill = skill.strip().title()

        if len(skill) > 2:
            all_skills.append(skill)

if len(all_skills) > 0:

    skills_df = pd.DataFrame(
        all_skills,
        columns=["Skill"]
    )

    top_skills = (
        skills_df["Skill"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top_skills.columns = [
        "Skill",
        "Jobs"
    ]

    fig = px.bar(
        top_skills,
        x="Skill",
        y="Jobs",
        title="Top Skills in Demand"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# JOB LISTINGS
# =========================================================

st.header("📋 Job Listings")

display_df = filtered_df.copy()

display_df["Apply"] = display_df["Job_Link"].apply(
    lambda x:
    f'<a href="{x}" target="_blank">Apply</a>'
    if str(x).startswith("http")
    else "N/A"
)

columns = [
    "Title",
    "Company",
    "Location",
    "Experience",
    "Source",
    "Apply"
]

st.write(
    display_df[columns]
    .to_html(
        escape=False,
        index=False
    ),
    unsafe_allow_html=True
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    f"Dashboard Generated from {len(filtered_df):,} Jobs"
)