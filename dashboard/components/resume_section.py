import streamlit as st


def render_resume_section(

    ats,
    gap,
    structure,
    readiness,
    candidate_experience,
    candidate_education,
    candidate_projects,
    candidate_certifications,
    resume_rewrite

):

    st.header("📄 Resume Analysis")

    st.subheader("🎯 ATS Score")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "ATS Score",
            f"{ats['ATS Score']}%"
        )

    with c2:

        st.metric(
            "Resume Readiness",
            f"{readiness['Overall']}%"
        )

    st.progress(
        ats["ATS Score"] / 100
    )

    st.divider()
    st.subheader("📋 Resume Structure")

    for section, present in structure["Sections"].items():

        if present:

            st.success(f"✔ {section}")

        else:

            st.error(f"✘ {section}")
    st.divider()

    st.subheader("🛠 Skills")

    matched, missing = st.columns(2)

    with matched:

        st.write("### Current Skills")

        for skill in sorted(gap["Current Skills"]):

            st.success(skill)

    with missing:

        st.write("### Missing Skills")

        for skill in sorted(gap["Missing Skills"]):

            st.warning(skill)
    st.divider()

    st.subheader("💼 Experience")

    exp1, exp2 = st.columns(2)

    with exp1:

        st.metric(
            "Years",
            candidate_experience["Years"]
        )

    with exp2:

        st.metric(
            "Internships",
            candidate_experience["Internships"]
        )
    st.divider()

    st.subheader("🎓 Education")

    for key, value in candidate_education.items():

        st.write(f"**{key}** : {value}")
    st.divider()

    st.subheader("📂 Projects")

    for key, value in candidate_projects.items():

        st.write(f"**{key}** : {value}")
    st.divider()

    st.subheader("📜 Certifications")

    for key, value in candidate_certifications.items():

        st.write(f"**{key}** : {value}")
    st.divider()

    st.subheader("✍ AI Resume Rewrite")

    st.code(
        resume_rewrite,
        language="text"
    )
