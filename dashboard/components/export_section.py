import os
import streamlit as st


def render_export_section(
    pdf_path,
    report_filename="ATS_Report.pdf"
):

    st.header("📄 Export Report")

    if os.path.exists(pdf_path):

        with open(pdf_path, "rb") as f:

            st.download_button(
                label="⬇ Download PDF Report",
                data=f,
                file_name=report_filename,
                mime="application/pdf",
                use_container_width=True
            )

    else:

        st.info("No report is available to download.")