def calculate_job_fit(

    ats,

    candidate_experience,

    candidate_projects,

    candidate_certifications,

    candidate_education,

    job_info,

    gap,

    structure

):

    # -------------------------
    # Skills
    # -------------------------

    skills_score = ats["ATS Score"]

    # -------------------------
    # Experience
    # -------------------------

    required = max(

        job_info["Minimum Years"],

        1

    )

    current = candidate_experience["Years"]

    experience_score = min(

        round(

            current / required * 100

        ),

        100

    )

    # -------------------------
    # Projects
    # -------------------------

    project_score = min(

        candidate_projects["Project Count"] * 25,

        100

    )

    # -------------------------
    # Certifications
    # -------------------------

    certification_score = min(

        candidate_certifications["Certification Count"] * 20,

        100

    )

    # -------------------------
    # Education
    # -------------------------

    education_score = (

        100

        if candidate_education["Education Found"]

        else 0

    )

    # -------------------------
    # Resume Structure
    # -------------------------

    total = len(

        structure["Sections"]

    )

    present = sum(

        structure["Sections"].values()

    )

    structure_score = round(

        present / total * 100

    )

    # -------------------------
    # Final Job Fit
    # -------------------------

    fit = round(

        skills_score * 0.35 +

        experience_score * 0.25 +

        project_score * 0.15 +

        education_score * 0.10 +

        certification_score * 0.05 +

        structure_score * 0.10

    )

    if fit >= 90:

        label = "Excellent"

    elif fit >= 75:

        label = "Good"

    elif fit >= 60:

        label = "Average"

    else:

        label = "Low"

    return {

        "Job Fit": fit,

        "Label": label,

        "Strengths":

            ats["Matched Skills"],

        "Weaknesses":

            gap["Missing Skills"]

    }