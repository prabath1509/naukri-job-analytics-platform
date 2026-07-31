def calculate_resume_readiness(

    ats,

    candidate_experience,

    candidate_projects,

    candidate_certifications,

    candidate_education,

    structure,

    job_info

):

    # -----------------------------
    # Skills Score
    # -----------------------------

    skills_score = ats["ATS Score"]

    # -----------------------------
    # Experience Score
    # -----------------------------

    required = max(job_info["Minimum Years"], 1)
    current = candidate_experience["Years"]

    experience_score = min(
        round((current / required) * 100),
        100
    )

    # -----------------------------
    # Projects Score
    # -----------------------------

    project_score = min(
        candidate_projects["Project Count"] * 25,
        100
    )

    # -----------------------------
    # Certification Score
    # -----------------------------

    certification_score = min(
        candidate_certifications["Certification Count"] * 20,
        100
    )

    # -----------------------------
    # Education Score
    # -----------------------------

    education_score = (
        100
        if candidate_education["Education Found"]
        else 0
    )

    # -----------------------------
    # Resume Structure Score
    # -----------------------------

    total = len(structure["Sections"])

    present = sum(
        structure["Sections"].values()
    )

    structure_score = round(
        (present / total) * 100
    )

    # -----------------------------
    # Overall Score
    # -----------------------------

    overall = round(

        skills_score * 0.35 +

        experience_score * 0.25 +

        project_score * 0.10 +

        certification_score * 0.05 +

        education_score * 0.10 +

        structure_score * 0.15

    )

    return {

        "Overall": overall,

        "Skills": skills_score,

        "Experience": experience_score,

        "Projects": project_score,

        "Certifications": certification_score,

        "Education": education_score,

        "Structure": structure_score

    }