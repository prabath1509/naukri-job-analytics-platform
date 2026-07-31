import re


def score_resume(text):

    score = 0

    details = {}

    sections = {

        "education":

            r"education",

        "experience":

            r"experience",

        "projects":

            r"project",

        "skills":

            r"skill",

        "certifications":

            r"certification"

    }

    for section, pattern in sections.items():

        found = bool(
            re.search(
                pattern,
                text,
                re.IGNORECASE
            )
        )

        details[section] = found

        if found:

            score += 20

    return {

        "Resume Structure Score":

            score,

        "Sections":

            details

    }