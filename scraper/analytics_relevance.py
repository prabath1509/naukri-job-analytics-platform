import re


ANALYTICS_TITLE_PATTERNS = (
    # Data analyst
    r"\bdata analysts?\b",
    r"\bsenior data analysts?\b",
    r"\bdata analytics analysts?\b",

    # Business analyst
    r"\bbusiness analysts?\b",
    r"\bbusiness systems analysts?\b",

    # Research
    r"\bresearch analysts?\b",
    r"\bmarket research analysts?\b",
    r"\bresearch pricing analysts?\b",

    # Data science
    r"\bdata scientists?\b",
    r"\bdata science\b",
    r"\bmodel builders?\b",

    # Machine learning / AI
    r"\bmachine learning\b",
    r"\bml engineers?\b",
    r"\bmlops\b",
    r"\bai engineers?\b",
    r"\bartificial intelligence\b",
    r"\baiml\b",
    r"\bgenai\b",
    r"\bgenerative ai\b",

    # Data engineering / architecture
    r"\bdata engineers?\b",
    r"\bdata engineering\b",
    r"\banalytics engineers?\b",
    r"\bdata architects?\b",
    r"\bdata architecture\b",
    r"\bdata warehousing\b",

    # Analytics
    r"\badvanced analytics\b",
    r"\bperformance analytics\b",
    r"\bcampaign analytics\b",
    r"\bcredit analytics\b",
    r"\bcore analytics\b",
    r"\bcustomer servicing analytics\b",
    r"\bfraud analytics\b",
    r"\bpeople analytics\b",
    r"\bshared analytics\b",
    r"\bbusiness analytics\b",
    r"\bdata analytics\b",
    r"\banalytics consultants?\b",
    r"\banalytics leads?\b",
    r"\banalytics managers?\b",
    r"\banalytics analysts?\b",
    r"\banalytics and metrics\b",
    r"\banalytics & metrics\b",

    # Governance / data operations
    r"\bdata governance analysts?\b",
    r"\bdata enrichment analysts?\b",
    r"\bdata verification analysts?\b",

    # ETL / integration
    r"\betl\b",
    r"\binformatica\b",
    r"\bdata integration\b",
    r"\balteryx\b",

    # BI / visualization
    r"\bpower bi\b",
    r"\bpowerbi\b",
    r"\btableau\b",
    r"\blooker\b",
    r"\bzoho analytics\b",
    r"\bbusiness intelligence\b",
    r"\bbi developers?\b",
    r"\bbi analysts?\b",

    # Reporting
    r"\breporting analysts?\b",
    r"\breporting & analytics\b",
    r"\breporting and analytics\b",
    r"\breporting and forecasting\b",
    r"\brevenue reporting\b",

    # SQL / database
    r"\bsql developers?\b",
    r"\bsql server developers?\b",
    r"\bpl/sql\b",
    r"\bplsql\b",
    r"\bdatabase developers?\b",
    r"\bdatabase analysts?\b",

    # Python data roles
    r"\bpython developers?\b",
    r"\bpython engineers?\b",
    r"\bpython automation developers?\b",
    r"\bpython pyspark developers?\b",
    r"\bpyspark developers?\b",
)


ANALYTICS_TITLE_REGEXES = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in ANALYTICS_TITLE_PATTERNS
)


def is_analytics_relevant(title):
    if title is None:
        return False

    normalized_title = " ".join(
        str(title).strip().split()
    )

    if not normalized_title:
        return False

    return any(
        pattern.search(normalized_title)
        for pattern in ANALYTICS_TITLE_REGEXES
    )