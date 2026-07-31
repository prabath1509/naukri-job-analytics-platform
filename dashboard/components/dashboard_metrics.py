import streamlit as st


def render_dashboard_metrics(
    ats,
    readiness,
    job_fit,
    interview,
    decision
):

    st.header("📊 Dashboard")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "ATS",
        f"{ats['ATS Score']}%"
    )

    c2.metric(
        "Readiness",
        f"{readiness['Overall']}%"
    )

    c3.metric(
        "Job Fit",
        f"{job_fit['Job Fit']}%"
    )

    c4.metric(
        "Interview",
        f"{interview['Overall']}%"
    )

    c5.metric(
        "Recruiter",
        decision["Decision"]
    )

    st.progress(
        job_fit["Job Fit"] / 100
    )