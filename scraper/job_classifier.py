# =========================================================
# scraper/job_classifier.py
# =========================================================


def classify_job(title: str):

    if title is None:
        return "Other"

    title = str(title).lower().strip()

    if not title:
        return "Other"

    # =====================================================
    # DATA ANALYST
    # =====================================================

    if (
        "data analyst" in title
        or "data analytics analyst" in title
    ):
        return "Data Analyst"

    # =====================================================
    # BUSINESS ANALYST
    # =====================================================

    if "business analyst" in title:
        return "Business Analyst"

    # =====================================================
    # RESEARCH ANALYST
    # =====================================================

    if (
        "research analyst" in title
        or "research analysts" in title
        or "market research analyst" in title
    ):
        return "Research Analyst"

    # =====================================================
    # DATA SCIENCE
    # =====================================================

    if (
        "data scientist" in title
        or "data science" in title
    ):
        return "Data Scientist"

    # =====================================================
    # MACHINE LEARNING / AI
    # =====================================================

    if (
        "machine learning" in title
        or "ml engineer" in title
        or "mlops" in title
        or "ai engineer" in title
        or "artificial intelligence" in title
        or "aiml" in title
    ):
        return "Machine Learning / AI"

    # =====================================================
    # DATA ENGINEERING
    # =====================================================

    if (
        "data engineer" in title
        or "analytics engineer" in title
        or "data architect" in title
    ):
        return "Data Engineering"

    # =====================================================
    # ETL / DATA INTEGRATION
    # =====================================================

    if (
        "etl" in title
        or "informatica" in title
        or "data integration" in title
    ):
        return "ETL / Data Integration"

    # =====================================================
    # BUSINESS INTELLIGENCE
    # =====================================================

    if (
        "power bi" in title
        or "powerbi" in title
        or "tableau" in title
        or "business intelligence" in title
        or "bi developer" in title
        or "bi analyst" in title
        or "reporting analyst" in title
    ):
        return "Business Intelligence"

    # =====================================================
    # SQL / DATABASE
    # =====================================================

    if (
        "sql developer" in title
        or "pl/sql" in title
        or "plsql" in title
        or "database developer" in title
        or "database analyst" in title
    ):
        return "SQL / Database"

    # =====================================================
    # PYTHON
    # =====================================================

    if (
        "python developer" in title
        or "python engineer" in title
    ):
        return "Python Development"

    # =====================================================
    # GENERAL ANALYST
    # =====================================================

    if "analyst" in title:
        return "Other Analyst"

    # =====================================================
    # SOFTWARE DEVELOPMENT
    # =====================================================

    if (
        "software engineer" in title
        or "software developer" in title
        or "application developer" in title
        or "developer" in title
    ):
        return "Software Development"

    # =====================================================
    # INTERNSHIP
    # =====================================================

    if (
        "intern" in title
        or "internship" in title
    ):
        return "Internship"

    return "Other"