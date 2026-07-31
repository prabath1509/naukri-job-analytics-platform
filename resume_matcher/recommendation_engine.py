def experience_rules(candidate_experience, job_info):

    recommendations = []

    current = candidate_experience["Years"]

    required = job_info["Minimum Years"]

    if current < required:

        recommendations.append({

            "Priority": "High",

            "Category": "Experience",

            "Message":
            f"This role requires at least {required} years of experience, while your resume shows {current}. Consider targeting Junior or Associate roles first."

        })

    return recommendations


def skill_rules(gap):

    recommendations = []

    if gap["Missing Skills"]:

        recommendations.append({

            "Priority": "High",

            "Category": "Skills",

            "Message":
            "Focus on these missing skills: "
            + ", ".join(gap["Missing Skills"])

        })

    return recommendations


def education_rules(candidate_education):

    recommendations = []

    if not candidate_education["Education Found"]:

        recommendations.append({

            "Priority": "Medium",

            "Category": "Education",

            "Message":
            "Education details were not detected. Include degree, branch, and graduation year."

        })

    return recommendations


def project_rules(candidate_projects):

    recommendations = []

    if candidate_projects["Project Count"] < 2:

        recommendations.append({

            "Priority": "Medium",

            "Category": "Projects",

            "Message":
            "Add at least two analytics projects demonstrating business impact."

        })

    return recommendations


def certification_rules(candidate_certifications):

    recommendations = []

    if candidate_certifications["Certification Count"] == 0:

        recommendations.append({

            "Priority": "Low",

            "Category": "Certifications",

            "Message":
            "Consider earning Microsoft, Google, IBM, or AWS certifications."

        })

    return recommendations


def structure_rules(structure):

    recommendations = []

    missing = [

        section

        for section, present

        in structure["Sections"].items()

        if not present

    ]

    if missing:

        recommendations.append({

            "Priority": "Medium",

            "Category": "Resume",

            "Message":
            "Missing resume sections: "
            + ", ".join(missing)

        })

    return recommendations


def ats_rules(ats):

    recommendations = []

    if ats["ATS Score"] < 70:

        recommendations.append({

            "Priority": "High",

            "Category": "ATS",

            "Message":
            "Improve keyword coverage to increase ATS compatibility."

        })

    return recommendations


def generate_recommendations(

    candidate_experience,

    candidate_education,

    candidate_projects,

    candidate_certifications,

    job_info,

    ats,

    gap,

    structure

):

    recommendations = []

    recommendations.extend(

        experience_rules(

            candidate_experience,

            job_info

        )

    )

    recommendations.extend(

        skill_rules(

            gap

        )

    )

    recommendations.extend(

        education_rules(

            candidate_education

        )

    )

    recommendations.extend(

        project_rules(

            candidate_projects

        )

    )

    recommendations.extend(

        certification_rules(

            candidate_certifications

        )

    )

    recommendations.extend(

        structure_rules(

            structure

        )

    )

    recommendations.extend(

        ats_rules(

            ats

        )

    )

    return recommendations