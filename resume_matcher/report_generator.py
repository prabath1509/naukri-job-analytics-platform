from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    ats,
    gap,
    structure,
    recommendations
):

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b>AI Powered ATS Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"ATS Score : {ats['ATS Score']}%",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            "<b>Matched Skills</b>",
            styles["Heading3"]
        )
    )

    for skill in ats["Matched Skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading3"]
        )
    )

    for skill in ats["Missing Skills"]:

        story.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,15))

    story.append(
        Paragraph(
            "<b>Recommendations</b>",
            styles["Heading3"]
        )
    )

    for item in recommendations:

        story.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )

    pdf.build(story)