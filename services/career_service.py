from resume_matcher.recommendation_engine import (
    generate_recommendations
)

from resume_matcher.career_roadmap import (
    generate_career_roadmap
)

from resume_matcher.optimizer import (
    optimize_resume
)


def analyze_career(

    candidate_experience,

    candidate_education,

    candidate_projects,

    candidate_certifications,

    job_info,

    ats,

    gap,

    structure

):

    recommendations = generate_recommendations(

        candidate_experience,

        candidate_education,

        candidate_projects,

        candidate_certifications,

        job_info,

        ats,

        gap,

        structure

    )

    roadmap = generate_career_roadmap(
        gap
    )

    optimizer = optimize_resume(
        ats,
        gap,
        structure
    )

    return {

        "recommendations": recommendations,

        "roadmap": roadmap,

        "optimizer": optimizer

    }