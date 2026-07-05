# =========================================================
# scraper/job_classifier.py
# =========================================================

import re
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
    # ADVANCED ANALYTICS
    # =====================================================

    if (
        "advanced analytics" in title
        or "analytics lead" in title
        or "analytics manager" in title
    ):
        return "Advanced Analytics"

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
    # PRODUCT MANAGEMENT
    # =====================================================

    if (
        "product manager" in title
        or "product management" in title
        or "product development" in title
    ):
        return "Product Management"

    # =====================================================
    # SITE RELIABILITY
    # =====================================================

    if (
        "site reliability" in title
        or title == "sre"
        or title.startswith("sre ")
        or " sre " in title
    ):
        return "Site Reliability Engineering"

    # =====================================================
    # SOLUTIONS ARCHITECTURE
    # =====================================================

    if (
        "solution architect" in title
        or "solutions architect" in title
        or "martech solutions architect" in title
    ):
        return "Solutions Architecture"

    # =====================================================
    # SECURITY
    # =====================================================

    if (
        "security engineer" in title
        or "information security" in title
        or "cybersecurity" in title
    ):
        return "Security"

    # =====================================================
    # QA / TESTING
    # =====================================================

    if (
        "qa automation" in title
        or "quality assurance" in title
        or "test engineer" in title
    ):
        return "QA / Testing"

    # =====================================================
    # CONSULTING
    # =====================================================

    if (
        "consultant" in title
        or "consulting" in title
    ):
        return "Consulting"

    # =====================================================
    # PROJECT / PROGRAM MANAGEMENT
    # =====================================================

    if (
        "project manager" in title
        or "program manager" in title
        or "programme manager" in title
    ):
        return "Project / Program Management"

    # =====================================================
    # BUSINESS DEVELOPMENT
    # =====================================================

    if "business development" in title:
        return "Business Development"

    # =====================================================
    # ACCOUNT MANAGEMENT
    # =====================================================

    if "account management" in title:
        return "Account Management"

    # =====================================================
    # CUSTOMER SUCCESS
    # =====================================================

    if "customer success" in title:
        return "Customer Success"

    # =====================================================
    # FINANCE / ACCOUNTING
    # =====================================================

    if (
        "finance" in title
        or "accountant" in title
        or "accounting" in title
        or "treasury" in title
    ):
        return "Finance / Accounting"

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

    if re.search(r"\bintern(?:ship)?\b", title):
        return "Internship"

    return "Other"
