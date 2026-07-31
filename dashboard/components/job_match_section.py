import streamlit as st
import plotly.graph_objects as go


def render_job_match_section(

    job_info,

    gap,

    matched_jobs

    ):

    st.header("💼 Job Match")

    st.subheader("📌 Job Information")

    left, right = st.columns(2)

    with left:

        st.write("### Position")

        st.write(job_info["Title"])

        st.write("### Category")

        st.write(job_info["Category"])

        st.write("### Experience")

        st.write(
            f"{job_info['Minimum Years']}+ Years"
        )

    with right:

        st.write("### Company")

        st.write(job_info["Company"])

        st.write("### Seniority")

        st.write(job_info["Seniority"])

        st.write("### Required Skills")

        for skill in job_info["Skills"]:

            st.success(skill)

        st.divider()
    st.subheader("🛠 Skill Gap")

    matched_col, missing_col = st.columns(2)

    with matched_col:

        st.write("### Current Skills")

        for skill in sorted(gap["Current Skills"]):

            st.success(skill)

    with missing_col:

        st.write("### Missing Skills")

        for skill in sorted(gap["Missing Skills"]):

            st.warning(skill)
    st.divider()

    st.subheader("🏆 Top Matching Jobs")

    top_jobs = matched_jobs.sort_values(
        by="Match_Percentage",
        ascending=False
    )

    st.dataframe(

        top_jobs[
            [
                "Title",
                "Company",
                "Location",
                "Match_Percentage"
            ]
        ],

        use_container_width=True,

        hide_index=True

    )
    # =====================================================
    # OVERALL MATCH
    # =====================================================

    st.divider()

    st.subheader("🎯 Overall Match")

    matched_count = len(gap["Current Skills"])

    missing_count = len(gap["Missing Skills"])

    total = matched_count + missing_count

    coverage = 0

    if total > 0:

        coverage = round(

            matched_count / total * 100

        )

    st.metric(

        "Match Percentage",

        f"{coverage}%"

    )

    st.progress(

        coverage / 100

    )
    st.divider()

    if coverage >= 90:

        st.success(
            "Excellent Resume Match"
        )

    elif coverage >= 75:

        st.success(
            "Good Resume Match"
        )

    elif coverage >= 60:

        st.warning(
            "Average Resume Match"
        )

    else:

        st.error(
            "Poor Resume Match"
        )
    st.divider()

    st.subheader("📊 Match Summary")

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric(

        "Current Skills",

        matched_count

    )

    summary2.metric(

        "Missing Skills",

        missing_count

    )

    summary3.metric(

        "Coverage",

        f"{coverage}%"

    )
    st.divider()

    st.subheader("🏅 Best Opportunities")

    best_jobs = matched_jobs.sort_values(

        by="Match_Percentage",

        ascending=False

    ).head(5)

    st.dataframe(

        best_jobs,

        use_container_width=True,

        hide_index=True

    )