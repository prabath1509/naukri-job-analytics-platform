def recruiter_decision(

    job_fit,

    interview,

    recommendations,

    candidate_experience,

    job_info

):

    score = job_fit["Job Fit"]

    if score >= 90:

        decision = "Strongly Recommend"

    elif score >= 75:

        decision = "Recommend Interview"

    elif score >= 60:

        decision = "Consider"

    else:

        decision = "Not Recommended"

    risks = []

    if candidate_experience["Years"] < job_info["Minimum Years"]:

        risks.append(

            "Experience Gap"

        )

    for item in recommendations:

        if item["Priority"] == "High":

            risks.append(

                item["Category"]

            )

    return {

        "Hire Score": score,

        "Decision": decision,

        "Interview Readiness":

            interview["Overall"],

        "Risks":

            sorted(

                list(

                    set(

                        risks

                    )

                )

            )

    }