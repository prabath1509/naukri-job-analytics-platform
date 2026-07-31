def rewrite_professional_summary(

    candidate_experience,

    candidate_projects,

    candidate_certifications,

    candidate_education,

    job_info

):

    degree = candidate_education.get(

        "Degree"

    ) or "Bachelor's Degree"

    years = candidate_experience.get(

        "Years",

        0

    )

    project_count = candidate_projects.get(

        "Project Count",

        0

    )

    technologies = candidate_projects.get(

        "Technologies",

        []

    )

    tech_text = ", ".join(

        technologies[:6]

    )

    summary = (

        f"{job_info['Title']} candidate with "

        f"{years} year(s) of experience, "

        f"{degree}, "

        f"and hands-on exposure to "

        f"{tech_text}. "

        f"Completed {project_count} analytics "

        f"project(s) with a strong focus on "

        f"data analysis, visualization, "

        f"and business problem solving."

    )

    return summary


def rewrite_projects(

    candidate_projects

):

    rewritten = []

    for project in candidate_projects["Projects"]:

        rewritten.append(

            f"{project.title()} – "

            "Developed an end-to-end "

            "analytics solution using "

            "industry-standard tools "

            "and generated actionable "

            "business insights."

        )

    return rewritten


def rewrite_skills(

    candidate_projects

):

    skills = candidate_projects[

        "Technologies"

    ]

    return sorted(

        list(

            set(

                skills

            )

        )

    )


def generate_resume_rewrite(

    candidate_experience,

    candidate_projects,

    candidate_certifications,

    candidate_education,

    job_info

):

    return {

        "Summary":

        rewrite_professional_summary(

            candidate_experience,

            candidate_projects,

            candidate_certifications,

            candidate_education,

            job_info

        ),

        "Projects":

        rewrite_projects(

            candidate_projects

        ),

        "Skills":

        rewrite_skills(

            candidate_projects

        )

    }