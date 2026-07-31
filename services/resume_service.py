from resume_matcher.experience_parser import extract_experience
from resume_matcher.education_parser import extract_education
from resume_matcher.project_parser import extract_projects
from resume_matcher.certification_parser import extract_certifications
from resume_matcher.ats_checker import calculate_ats_score
from resume_matcher.skill_gap import analyze_skill_gap
from resume_matcher.resume_scorer import score_resume


def analyze_resume(resume_text, job_text):

    candidate_experience = extract_experience(
        resume_text
    )

    candidate_education = extract_education(
        resume_text
    )

    candidate_projects = extract_projects(
        resume_text
    )

    candidate_certifications = extract_certifications(
        resume_text
    )

    ats = calculate_ats_score(
        resume_text,
        job_text
    )

    gap = analyze_skill_gap(
        resume_text,
        job_text
    )

    structure = score_resume(
        resume_text
    )

    return {
        "candidate_experience": candidate_experience,
        "candidate_education": candidate_education,
        "candidate_projects": candidate_projects,
        "candidate_certifications": candidate_certifications,
        "ats": ats,
        "gap": gap,
        "structure": structure,
    }