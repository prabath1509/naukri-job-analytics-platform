import streamlit as st


def render_career_section(

    recommendations,

    roadmap,

    optimizer

):

    st.header("🚀 Career Development")

    st.subheader("💡 Recommendations")

    if recommendations:

        for item in recommendations:

            st.success(item)

    else:

        st.info(
            "No recommendations available."
        )

    st.divider()
    st.subheader("🗺 Career Roadmap")

    if roadmap:

        if isinstance(roadmap, list):

            for step in roadmap:

                st.write(f"• {step}")

        else:

            st.write(roadmap)

    else:

        st.info(
            "Career roadmap not available."
        )

    st.divider()
    st.subheader("⚡ Resume Optimizer")

    if optimizer:

        st.code(

            optimizer,

            language="text"

        )

    else:

        st.info(
            "Resume optimizer output not available."
        )