# Data Quality Audit



## 1. Overview



This audit evaluates the completeness, consistency, and potential duplication of the job records collected for the Naukri Job Analytics Platform.



The audit was performed on the dataset snapshot:



`data/jobs_20260731_173423.csv`



The dataset contains 4,325 records and 17 columns.



The audit script generates separate reports and does not modify the original source CSV.



## 2. Audit Scope



The following checks were performed:



- Missing or placeholder job titles

- Missing or placeholder company names

- Missing application URLs

- Structurally invalid application URLs

- Duplicate title-company-location combinations

- Duplicate application URLs

- Location formatting variants

- Potentially outdated posting dates

- Missing or unparseable posting dates

- Future-starting job classifications



## 3. Audit Results



| Validation Check | Result |

|---|---:|

| Records checked | 4,325 |

| Columns checked | 17 |

| Missing or placeholder titles | 0 |

| Missing or placeholder companies | 0 |

| Missing application URLs | 0 |

| Structurally invalid URLs | 0 |

| Duplicate title-company-location candidates | 22 |

| Duplicate application URLs | 0 |

| Location formatting variant groups | 0 |

| Potentially outdated postings | 107 |

| Future-starting jobs | 46 |

| Missing or unparseable posting dates | 0 |

| Records flagged for review | 128 |

| Original source dataset modified | No |



## 4. Key Findings



### 4.1 Record Completeness



No missing or placeholder job titles, company names, or application URLs were detected by the audit.



All application URLs passed the structural validation implemented in the script.



Structural URL validation does not establish that a page is reachable, that the vacancy is still open, or that an application can be submitted.



### 4.2 Duplicate Candidates



The audit flagged 22 later records with title-company-location combinations matching earlier records after normalization.



These are duplicate candidates, not confirmed duplicate jobs.



Different application URLs, requisition identifiers, locations, or experience requirements may represent distinct vacancies. Therefore, the audit does not automatically delete these records.



The candidates should be reviewed before any deduplication is performed.



### 4.3 Potentially Outdated Postings



The audit identified 107 potentially outdated records:



- 106 records contain the label `Posted 30+ Days Ago`.

- One record contains the historic date `Starts : 13th Jul' 21`.



The historic-date record should be investigated separately.



An old posting date does not prove that a vacancy is closed. Application pages should be checked before records are classified as expired.



### 4.4 Future-Starting Jobs



The audit identified 46 records with the posting-date label `Starts in 1-3 months`.



These records are classified separately because the label describes a future start period rather than a missing or unparseable posting date.



The exact meaning of the label should be interpreted in the context of the source website's date terminology.



### 4.5 Posting-Date Classification



The audit reported zero missing or unparseable posting dates after future-starting records were separated from that category.



This result reflects the implemented parser and classification rules. It does not guarantee that every source label represents an exact date.



Relative posting dates should be interpreted using the dataset's collection or snapshot date, where that date can be confirmed.



### 4.6 Location Consistency



The audit detected zero location-format variant groups under its current normalization rules.



This does not prove that all locations are semantically consistent. For example, different names can refer to the same geographic area, and similar-looking labels can refer to different locations.



Further location standardization may be useful in a future iteration.



## 5. Methodology



The audit script reads the dataset snapshot, applies validation rules, and produces separate reports.



The original source CSV is preserved.



Generated reports:



- `docs/case-study/data_quality_issues.csv`

- `docs/case-study/data_quality_summary.json`

- `docs/case-study/future_starting_jobs.csv`



The duplicate-review workflow also produces:



- `docs/case-study/duplicate_review.csv`



The issue report includes the records flagged by the implemented validation checks. The future-starting report separates future-starting records for independent review.



## 6. Limitations



The audit has the following limitations:



1. Structural URL validation does not confirm live page availability.

2. Posting age does not confirm that a vacancy is expired.

3. Matching title, company, and location values do not prove that two records represent the same vacancy.

4. Zero detected location variants does not establish complete geographic consistency.

5. Relative posting-date labels may be approximate.

6. Future-starting labels require interpretation in the context of the source website.

7. The audit results depend on the validation and parsing rules implemented in the audit script.



## 7. Recommended Improvements



Future iterations could include:



- Checking application-page reachability with appropriate request limits and error handling.

- Reviewing duplicate candidates using requisition IDs and application URLs.

- Standardizing locations using a controlled geographic mapping.

- Preserving the original posting-date text alongside normalized dates.

- Recording the actual collection timestamp for each snapshot.

- Tracking changes in vacancy availability across repeated snapshots.

- Adding automated regression tests for posting-date parsing.



## 8. Conclusion



The audit provides an initial, reproducible assessment of the 4,325-record dataset.



It found no missing titles, company names, or application URLs under the implemented checks. It also identified duplicate candidates, potentially outdated postings, and future-starting jobs for further review.



The original source CSV remained unchanged, and uncertain records were flagged rather than automatically deleted.



The results provide a foundation for improving data reliability and documenting the dataset's limitations before downstream analysis.

