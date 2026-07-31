def generate_recommendations(
    ats,
    gap,
    structure
):

    recommendations = []

    # -----------------------------------
    # Missing Skills
    # -----------------------------------

    for skill in gap["Missing Skills"]:

        recommendations.append(
            f"Add '{skill.title()}' to your resume if you have experience."
        )

    # -----------------------------------
    # Resume Structure
    # -----------------------------------

    for section, present in structure["Sections"].items():

        if not present:

            recommendations.append(
                f"Add a '{section.title()}' section."
            )

    # -----------------------------------
    # ATS Score
    # -----------------------------------

    score = ats["ATS Score"]

    if score < 60:

        recommendations.append(
            "Your resume needs significant optimization."
        )

    elif score < 80:

        recommendations.append(
            "Improve keyword coverage to increase ATS score."
        )

    else:

        recommendations.append(
            "Your resume is well optimized."
        )

    return recommendations