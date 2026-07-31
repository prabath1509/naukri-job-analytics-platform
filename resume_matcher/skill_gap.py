from resume_matcher.keyword_matcher import extract_skills


def analyze_skill_gap(
        resume_text,
        job_text
):

    resume = set(
        extract_skills(resume_text)
    )

    job = set(
        extract_skills(job_text)
    )

    return {

        "Current Skills":

            sorted(resume),

        "Required Skills":

            sorted(job),

        "Missing Skills":

            sorted(job - resume),

        "Extra Skills":

            sorted(resume - job)

    }