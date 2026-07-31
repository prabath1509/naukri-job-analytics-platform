import streamlit as st


def render_interview_section(

    interview_readiness,

    interview_questions

    ):

    st.header("🎤 Interview")

    st.subheader("📊 Interview Readiness")

    if isinstance(interview_readiness, dict):

        for key, value in interview_readiness.items():

            st.metric(

                key,

                value

            )

    else:

        st.write(interview_readiness)

        st.divider()
    st.subheader("❓ Interview Questions")

    if interview_questions:

        if isinstance(interview_questions, list):

            for index, question in enumerate(interview_questions, start=1):

                st.write(f"**{index}.** {question}")

        else:

            st.write(interview_questions)

    else:

        st.info(
            "No interview questions available."
        )

    st.divider()
    st.subheader("💡 Interview Tips")

    tips = [

        "Review your resume before the interview.",

        "Prepare examples for your key projects.",

        "Practice SQL and Python coding questions.",

        "Be ready to explain your dashboards and analysis.",

        "Research the company and the job description."

    ]

    for tip in tips:

        st.success(tip)