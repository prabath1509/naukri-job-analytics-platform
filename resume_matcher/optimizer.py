def optimize_resume(
    ats,
    gap,
    structure
):

    improvements = []

    # ---------------------------------
    # Missing Skills
    # ---------------------------------

    for skill in gap["Missing Skills"]:

        improvements.append(
            f"Add '{skill.title()}' if you have practical experience."
        )

    # ---------------------------------
    # Resume Sections
    # ---------------------------------

    for section, present in structure["Sections"].items():

        if not present:

            improvements.append(
                f"Include a {section.title()} section."
            )

    # ---------------------------------
    # General Suggestions
    # ---------------------------------

    improvements.extend(
        [
            "Quantify achievements with numbers and percentages.",
            "Use strong action verbs.",
            "Tailor your resume to the selected job.",
            "Highlight Power BI dashboards.",
            "Mention SQL optimization work."
        ]
    )

    return improvements