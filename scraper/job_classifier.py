# =========================================================
# scraper/job_classifier.py
# =========================================================

# ==========================================================
# scraper/job_classifier.py
# ==========================================================

def classify_job(title: str):

    title = str(title).lower()

    if "data analyst" in title:
        return "Data Analyst"

    if "business analyst" in title:
        return "Business Analyst"

    if "data scientist" in title:
        return "Data Scientist"

    if "machine learning" in title or "ml engineer" in title:
        return "Machine Learning"

    if "data engineer" in title:
        return "Data Engineer"

    if "python" in title:
        return "Python"

    if "sql" in title:
        return "SQL"

    if "power bi" in title or "tableau" in title:
        return "Business Intelligence"

    if "software" in title or "developer" in title:
        return "Software Development"

    return "Other"