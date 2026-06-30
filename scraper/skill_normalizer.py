import re

SKILL_MAP = {
    # Programming
    "python": "Python",
    "py": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "c": "C",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "r": "R",

    # SQL
    "sql": "SQL",
    "mysql": "MySQL",
    "ms sql": "SQL Server",
    "sql server": "SQL Server",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "oracle sql": "Oracle SQL",

    # BI
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "power-bi": "Power BI",
    "tableau": "Tableau",
    "tableau desktop": "Tableau",
    "qlikview": "QlikView",
    "qlik sense": "Qlik Sense",
    "looker": "Looker",

    # Excel
    "excel": "Excel",
    "ms excel": "Excel",
    "microsoft excel": "Excel",

    # Python Libraries
    "numpy": "NumPy",
    "numpy library": "NumPy",
    "pandas": "Pandas",
    "pandas library": "Pandas",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "pytorch": "PyTorch",

    # Cloud
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "Google Cloud",

    # Big Data
    "spark": "Apache Spark",
    "apache spark": "Apache Spark",
    "hadoop": "Hadoop",
    "hive": "Hive",

    # ETL
    "airflow": "Apache Airflow",
    "ssis": "SSIS",
    "etl": "ETL",

    # Visualization
    "plotly": "Plotly",

    # Version Control
    "git": "Git",
    "github": "GitHub",

    # Analytics
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "statistics": "Statistics",
    "data analysis": "Data Analysis",
    "data analytics": "Data Analytics",
    "data visualization": "Data Visualization",
    "business intelligence": "Business Intelligence",

    # Platforms
    "snowflake": "Snowflake",
    "databricks": "Databricks",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
}


def normalize_skill(skill):

    if not skill:
        return ""

    skill = str(skill).strip().lower()
    skill = re.sub(r"\s+", " ", skill)

    if skill in SKILL_MAP:
        return SKILL_MAP[skill]

    acronyms = {
        "sql": "SQL",
        "qa": "QA",
        "ai": "AI",
        "bi": "BI",
        "ml": "ML",
        "etl": "ETL",
        "api": "API",
        "sap": "SAP",
        "crm": "CRM",
        "erp": "ERP",
        "plsql": "PL/SQL",
        "ssis": "SSIS",
        "o2c": "O2C",
        "mlflow": "MLflow",
        "pyspark": "PySpark",
        "servicenow": "ServiceNow",
    }

    if skill in acronyms:
        return acronyms[skill]

    return skill.title()


def normalize_skill_list(skill_string):

    if not skill_string:
        return ""

    skills = re.split(r",|/|;", str(skill_string))

    normalized = []

    for skill in skills:

        skill = normalize_skill(skill)

        if skill and skill not in normalized:
            normalized.append(skill)

    return ", ".join(sorted(normalized))