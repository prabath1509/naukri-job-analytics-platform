import re


TECHNOLOGIES = [

    "python",
    "sql",
    "power bi",
    "excel",
    "tableau",
    "streamlit",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "machine learning",
    "tensorflow",
    "scikit-learn",
    "azure",
    "aws",
    "snowflake",
    "spark",
    "hadoop",
    "postgresql",
    "mysql"

]


PROJECT_PATTERNS = [

    r"projects?(.*?)(education|experience|skills|certifications|$)"

]


def extract_projects(resume_text):

    text = resume_text.lower()

    projects = []

    technologies = []

    for pattern in PROJECT_PATTERNS:

        match = re.search(

            pattern,

            text,

            re.DOTALL

        )

        if match:

            section = match.group(1)

            lines = [

                line.strip()

                for line in section.split("\n")

                if line.strip()

            ]

            for line in lines:

                if len(line) > 5:

                    projects.append(line)

    for tech in TECHNOLOGIES:

        if tech in text:

            technologies.append(tech.title())

    return {

        "Projects": sorted(

            list(set(projects))

        ),

        "Project Count": len(

            set(projects)

        ),

        "Technologies": sorted(

            list(set(technologies))

        )

    }