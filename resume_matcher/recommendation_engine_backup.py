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

    # ==========================================
    # EXPERIENCE
    # ==========================================

    current_years = candidate_experience["Years"]

    required_years = job_info["Minimum Years"]

    if current_years < required_years:

        recommendations.append({

            "Priority":"High",

            "Category":"Experience",

            "Message":

            f"Job requires {required_years}+ years while your resume shows {current_years} year(s). Consider targeting Junior or Associate roles first."

        })

    # ==========================================
    # SKILLS
    # ==========================================

    if gap["Missing Skills"]:

        recommendations.append({

            "Priority":"High",

            "Category":"Skills",

            "Message":

            "Missing critical skills: "

            + ", ".join(

                gap["Missing Skills"]

            )

        })

    # ==========================================
    # EDUCATION
    # ==========================================

    if not candidate_education["Education Found"]:

        recommendations.append({

            "Priority":"Medium",

            "Category":"Education",

            "Message":

            "Education details were not detected. Include your degree and graduation year."

        })

    # ==========================================
    # PROJECTS
    # ==========================================

    if candidate_projects["Project Count"] < 2:

        recommendations.append({

            "Priority":"Medium",

            "Category":"Projects",

            "Message":

            "Add more end-to-end analytics projects demonstrating practical experience."

        })

    # ==========================================
    # CERTIFICATIONS
    # ==========================================

    if candidate_certifications["Certification Count"] == 0:

        recommendations.append({

            "Priority":"Low",

            "Category":"Certifications",

            "Message":

            "Add relevant certifications to strengthen your profile."

        })

    # ==========================================
    # RESUME STRUCTURE
    # ==========================================

    missing_sections = [

        section

        for section, present in structure["Sections"].items()

        if not present

    ]

    if missing_sections:

        recommendations.append({

            "Priority":"Medium",

            "Category":"Resume",

            "Message":

            "Missing sections: "

            + ", ".join(

                missing_sections

            )

        })

    # ==========================================
    # ATS SCORE
    # ==========================================

    if ats["ATS Score"] < 70:

        recommendations.append({

            "Priority":"High",

            "Category":"ATS",

            "Message":

            "Improve keyword coverage to increase ATS compatibility."

        })

    return recommendations