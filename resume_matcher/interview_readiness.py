def calculate_interview_readiness(

    ats,

    candidate_projects,

    candidate_certifications,

    candidate_experience,

    candidate_education

):

    technical = min(

        ats["ATS Score"],

        100

    )

    project_score = min(

        candidate_projects["Project Count"] * 20,

        100

    )

    certification_score = min(

        candidate_certifications["Certification Count"] * 20,

        100

    )

    experience_score = min(

        candidate_experience["Years"] * 20,

        100

    )

    education_score = (

        100

        if candidate_education["Education Found"]

        else 0

    )

    behavioral = round(

        (experience_score + education_score) / 2

    )

    communication = round(

        (project_score + certification_score) / 2

    )

    overall = round(

        technical * 0.40 +

        behavioral * 0.30 +

        communication * 0.30

    )

    return {

        "Technical": technical,

        "Behavioral": behavioral,

        "Communication": communication,

        "Overall": overall

    }