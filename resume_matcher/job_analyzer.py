import re


CATEGORY_RULES = {
    "Data Analytics": [
        "data analyst",
        "analytics",
        "business analyst",
        "reporting analyst"
    ],

    "Data Science": [
        "data scientist",
        "machine learning",
        "ml engineer",
        "ai engineer"
    ],

    "Data Engineering": [
        "data engineer",
        "etl",
        "big data",
        "pipeline"
    ],

    "Business Intelligence": [
        "power bi",
        "tableau",
        "bi developer",
        "business intelligence"
    ]
}


def detect_category(title):

    title = str(title).lower()

    for category, keywords in CATEGORY_RULES.items():

        if any(keyword in title for keyword in keywords):

            return category

    return "Other"


def detect_seniority(title):

    title = str(title).lower()

    if "intern" in title:

        return "Intern"

    elif "junior" in title:

        return "Junior"

    elif "associate" in title:

        return "Associate"

    elif "senior" in title:

        return "Senior"

    elif "lead" in title:

        return "Lead"

    elif "manager" in title:

        return "Manager"

    return "Mid-Level"


def parse_experience(exp):

    exp = str(exp)

    numbers = re.findall(r"\d+", exp)

    if len(numbers) >= 2:

        return int(numbers[0]), int(numbers[1])

    elif len(numbers) == 1:

        return int(numbers[0]), int(numbers[0])

    return 0, 0


def parse_skills(skills):

    if skills is None:

        return []

    return sorted(

        list(

            {

                s.strip()

                for s in str(skills).split(",")

                if s.strip()

            }

        )

    )


def analyze_job(job):

    minimum, maximum = parse_experience(

        job.get(

            "Experience",

            ""

        )

    )

    return {

        "Title": job.get(

            "Title",

            ""

        ),

        "Company": job.get(

            "Company",

            ""

        ),

        "Category": detect_category(

            job.get(

                "Title",

                ""

            )

        ),

        "Seniority": detect_seniority(

            job.get(

                "Title",

                ""

            )

        ),

        "Minimum Years": minimum,

        "Maximum Years": maximum,

        "Skills": parse_skills(

            job.get(

                "Skills",

                ""

            )

        )

    }