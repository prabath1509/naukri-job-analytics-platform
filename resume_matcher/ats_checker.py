from resume_matcher.keyword_matcher import extract_skills


def calculate_ats_score(resume_text, job_text=""):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_text)

    if len(job_skills) == 0:

        score = min(
            len(resume_skills) * 5,
            100
        )

        return {
            "ATS Score": score,
            "Resume Skills": resume_skills,
            "Job Skills": [],
            "Matched Skills": resume_skills,
            "Missing Skills": []
        }

    matched = sorted(
        set(resume_skills)
        &
        set(job_skills)
    )

    missing = sorted(
        set(job_skills)
        -
        set(resume_skills)
    )

    score = round(
        len(matched)
        /
        len(job_skills)
        * 100,
        2
    )

    return {

        "ATS Score": score,

        "Resume Skills": resume_skills,

        "Job Skills": job_skills,

        "Matched Skills": matched,

        "Missing Skills": missing

    }