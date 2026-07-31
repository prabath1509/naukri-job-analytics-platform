import re


def extract_experience(resume_text):

    text = resume_text.lower()

    years = []

    patterns = [

        r"(\d+)\+?\s*years",

        r"(\d+)\s*yrs",

        r"(\d+)\s*year"

    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text
        )

        for match in matches:

            years.append(
                int(match)
            )

    internships = len(
        re.findall(
            r"intern",
            text
        )
    )

    return {

        "Years": max(years) if years else 0,

        "Internships": internships

    }