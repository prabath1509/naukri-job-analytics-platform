# 🤖 AI-Powered Job Analytics Platform

A production-style job market analytics platform that automatically collects, cleans, validates, analyzes, and visualizes job opportunities from multiple recruitment sources.

The platform provides real-time insights into hiring trends, skills demand, company hiring activity, locations, work modes, salary availability, and role distributions through an interactive Streamlit dashboard.

---

## 🌐 Live Dashboard

🔗 https://naukri-job-analytics-platform-fyyympr7t2vqc2sg4snwzf.streamlit.app/

---

# 📌 Project Overview

Finding quality job market insights requires collecting data from multiple recruitment platforms, cleaning inconsistent information, removing duplicates, validating data quality, and presenting meaningful analytics.

This project automates the complete workflow through an end-to-end ETL pipeline.

The system:

- Scrapes jobs from multiple sources
- Cleans and standardizes records
- Removes duplicate listings
- Parses and enriches job information
- Generates analytical datasets
- Stores data in SQLite
- Produces interactive dashboards
- Tracks field quality and source quality
- Validates production datasets
- Publishes only validated datasets
- Automates recurring data collection using GitHub Actions

---

# ✨ Key Features

### 🌐 Multi-Source Job Aggregation

The platform supports job collection from multiple recruitment and ATS sources:

- Naukri
- Greenhouse
- Workday
- Lever
- SmartRecruiters

---

### ⚙️ Automated ETL Pipeline

- Job scraping
- Data collection
- Data cleaning
- Data transformation
- Data validation
- Duplicate removal
- Field standardization
- Experience parsing
- Salary parsing
- Skill processing
- SQLite storage
- Analytics generation

---

### 📊 Interactive Analytics Dashboard

Explore:

- Hiring companies
- Job locations
- Experience requirements
- Skills demand
- Salary availability
- Work mode trends
- Role distribution
- Source comparison
- Job listings

---

### 🔎 Job Explorer

Search and explore collected job opportunities using:

- Job Title
- Company
- Location
- Experience
- Salary
- Skills
- Source
- Direct Job Link

---

### 📈 Data Quality Intelligence

Automatically measures:

- Field completeness
- Source quality
- Missing values
- Coverage percentage
- Dataset validation
- Duplicate job links
- Required-field availability

---

### 🛡️ Publication Quality Gate

The project prevents publishing poor-quality datasets.

Validation includes:

- Minimum job count
- Minimum source count
- Required data sources
- Required-field validation
- Dataset integrity checks
- Duplicate detection
- Data-quality checks

Only datasets that satisfy the configured quality requirements are published.

---

### 📦 Snapshot Management

- Automatic snapshot creation
- Snapshot validation
- Snapshot retention
- Historical dataset preservation
- Production dataset protection

If a new scraping run fails quality checks, the previous validated production dataset can be preserved.

---

### 🤖 Resume Matcher

Includes an AI-assisted resume matching module to compare resumes with job descriptions and help identify relevant opportunities.

---

### 🔄 GitHub Automation

GitHub Actions automatically:

- Run scraper
- Execute scheduled data collection
- Validate dataset
- Update SQLite
- Generate analytics
- Publish validated data
- Preserve previous production dataset when quality checks fail
- Automate recurring pipeline execution

---

# 🏗️ System Architecture

```text
                    Job Sources
                         │
                         ▼
                   Web Scrapers
                         │
                         ▼
              Cleaning & Standardization
                         │
                         ▼
                Data Enrichment
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
       Experience     Salary       Skills
         Parsing      Parsing     Processing
             │           │           │
             └───────────┼───────────┘
                         ▼
                 Duplicate Removal
                         │
                         ▼
              Publication Quality Gate
                         │
                         ▼
                  SQLite Database
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Analytics CSV Files     Data Quality Metrics
             │                       │
             └───────────┬───────────┘
                         ▼
                Streamlit Dashboard
# ⚙ Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| Dashboard | Streamlit |
| Database | SQLite |
| Visualization | Plotly |
| Data Analysis | Pandas, NumPy |
| Web Scraping | Selenium, Requests, BeautifulSoup |
| HTML Parsing | lxml |
| Automation | GitHub Actions |
| Version Control | Git |
| Deployment | Streamlit Community Cloud |

---

# 📊 Current Dataset Statistics

Latest Production Dataset

| Metric | Value |
|--------|------:|
| Total Jobs | 4,832 |
| Companies | 1,969 |
| Sources | 3 |
| Duplicate Links | 0 |
| Job Link Coverage | 100% |
| Company Coverage | 100% |
| Title Coverage | 100% |
| Location Coverage | 99.63% |
| Experience Coverage | 84.93% |
| Skills Coverage | 84.91% |
| Salary Coverage | 12.42% |

---

# 📈 Dashboard Features

The dashboard provides:

## Executive KPIs

- Total Jobs
- Companies Hiring
- Locations
- Data Sources

---

## Interactive Filters

- Job Title
- Company
- Source
- Work Mode
- Experience
- Role Category

---

## Visual Analytics

- Hiring by Company
- Hiring by Location
- Work Mode Distribution
- Experience Distribution
- Role Categories
- Salary Availability
- Source Distribution
- Skill Demand

---

## Data Quality Dashboard

Includes:

- Field Quality
- Source Quality
- Coverage Analytics
- Missing Value Analysis

---

## Job Explorer

Searchable table with:

- Job Title
- Company
- Location
- Experience
- Salary
- Skills
- Source
- Direct Job Link

---

# 📂 Repository Structure

```
naukri-job-analytics-platform/

│
├── dashboard/
│   └── app.py
│
├── scraper/
│   ├── naukri_scraper.py
│   ├── greenhouse_scraper.py
│   ├── workday_scraper.py
│   ├── lever_scraper.py
│   ├── smartrecruiters_scraper.py
│   └── ats_source_registry.py
│
├── data/
│
├── database/
│
├── resume_matcher/
│
├── analytics/
│
├── notebooks/
│
├── .github/
│   └── workflows/
│
├── scheduler.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/prabath1509/naukri-job-analytics-platform.git

cd naukri-job-analytics-platform
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Project

Run the scraper

```bash
python main.py
```

Launch dashboard

```bash
streamlit run dashboard/app.py
```

---

# 🔄 ETL Workflow

```
Collect Jobs
      │
      ▼
Clean Records
      │
      ▼
Standardize Fields
      │
      ▼
Parse Experience / Salary / Skills
      │
      ▼
Remove Duplicates
      │
      ▼
Validate Dataset
      │
      ▼
Update SQLite
      │
      ▼
Generate Analytics
      │
      ▼
Launch Dashboard
```

---

# 📋 Data Quality Framework

Every production run includes:

- Source Quality Analytics
- Field Quality Analytics
- Publication Quality Gate
- Duplicate Detection
- Snapshot Validation
- Dataset Integrity Checks

Only validated datasets are published.

---

# 🤖 Automation

GitHub Actions automatically:

- Execute scheduled scraping
- Validate dataset quality
- Preserve production datasets
- Update SQLite database
- Publish analytics
- Prevent bad deployments

---

# 📌 Key Highlights

✔ Production-style ETL pipeline

✔ Multi-source scraping

✔ Automated quality validation

✔ SQLite data warehouse

✔ Interactive dashboard

✔ Automated deployment workflow

✔ Resume matching module

✔ Snapshot retention

✔ Zero duplicate job links

---

# 🔮 Future Enhancements

Planned improvements:

- Additional ATS integrations
- AI-powered skill recommendations
- Resume semantic matching
- Salary normalization
- Historical trend analysis
- Job recommendation engine
- REST API
- Power BI integration
- Predictive hiring analytics

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Krishna Prabath**

Aspiring Data Analyst | Python | SQL | Power BI | Data Visualization | Web Scraping

### Connect with me

GitHub:
https://github.com/prabath1509

LinkedIn:
https://www.linkedin.com/in/srinadhukrishnaprabath

Portfolio:
https://prabath1509.github.io/portfolio/

---

⭐ If you found this project useful, consider giving it a star on GitHub.
