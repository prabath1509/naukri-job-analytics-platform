from resume_matcher.job_analyzer import analyze_job
from resume_matcher.matcher import match_jobs


def analyze_jobs(job, jobs_df, resume_text):
    """
    Analyze the selected job and find matching jobs.
    """

    job_info = analyze_job(job)

    matched_jobs = match_jobs(
        resume_text,
        jobs_df
    )

    return {
        "job_info": job_info,
        "matched_jobs": matched_jobs,
    }