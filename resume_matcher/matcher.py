import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_matcher.pdf_parser import extract_resume_text

# -----------------------------------
# EXTRACT TEXT FROM PDF
# -----------------------------------


# -----------------------------------
# MATCH RESUME WITH JOBS
# -----------------------------------

def match_jobs(resume_text, jobs_df):

    jobs_df = jobs_df.copy()

    jobs_df["combined_text"] = (
        jobs_df["Title"].astype(str)
        + " "
        + jobs_df["Skills"].astype(str)
        + " "
        + jobs_df["Company"].astype(str)
    )

    matched_scores = []

    for job_text in jobs_df["combined_text"]:

        text = [resume_text, job_text]

        cv = CountVectorizer()

        matrix = cv.fit_transform(text)

        similarity = cosine_similarity(matrix)[0][1]

        matched_scores.append(
            round(similarity * 100, 2)
        )

    jobs_df["Match_Percentage"] = matched_scores

    jobs_df = jobs_df.sort_values(
        by="Match_Percentage",
        ascending=False
    )

    return jobs_df