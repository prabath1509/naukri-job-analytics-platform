from resume_matcher.recruiter_engine import recruiter_decision

def analyze_recruiter(
    job_fit,
    interview,
    recommendations,
    candidate_experience,
    job_info
):
    return recruiter_decision(
        job_fit,
        interview,
        recommendations,
        candidate_experience,
        job_info
    )