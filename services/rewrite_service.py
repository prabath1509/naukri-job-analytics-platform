from resume_matcher.job_fit_engine import calculate_job_fit

def analyze_job_fit(
    ats,
    candidate_experience,
    candidate_projects,
    candidate_certifications,
    candidate_education,
    job_info,
    gap,
    structure
):
    return calculate_job_fit(
        ats,
        candidate_experience,
        candidate_projects,
        candidate_certifications,
        candidate_education,
        job_info,
        gap,
        structure
    )