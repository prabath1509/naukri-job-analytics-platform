from resume_matcher.resume_readiness import calculate_resume_readiness

def analyze_readiness(
    ats,
    candidate_experience,
    candidate_projects,
    candidate_certifications,
    candidate_education,
    structure,
    job_info
):
    return calculate_resume_readiness(
        ats,
        candidate_experience,
        candidate_projects,
        candidate_certifications,
        candidate_education,
        structure,
        job_info
    )