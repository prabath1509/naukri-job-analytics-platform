import streamlit as st


def render_recruiter_section(decision):

    st.header("👔 Recruiter Decision")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Hire Score",
        f"{decision['Hire Score']}%"
    )

    c2.metric(
        "Decision",
        decision["Decision"]
    )

    c3.metric(
        "Interview Ready",
        f"{decision['Interview Readiness']}%"
    )

    st.subheader("⚠ Hiring Risks")

    if decision["Risks"]:

        for risk in decision["Risks"]:

            st.warning(risk)

    else:

        st.success(
            "No major hiring risks detected."
        )