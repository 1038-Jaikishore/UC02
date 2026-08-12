# Preprocessing & Data Ingest Report

Generates statistical and status details regarding the parsing, cleaning, and persistent ingestion pipeline of Synthea clinical datasets.

## Pipeline Summary
* **Date Executed**: 2026-08-12 06:52:37 UTC
* **Total CSVs Discovered**: 21
* **Files Successfully Processed**: 17
* **Files Skipped for Patient Evidence**: 3
* **Total Rows Read**: 1165
* **Valid Rows Ingested**: 1165
* **Malformed Rows Skipped**: 0
* **Duplicate Primary Key Rows Found**: 0
* **Patients Created**: 0
* **Patients Updated**: 40
* **Authorization Requests Created**: 0
* **Authorization Requests Updated**: 50
* **Orphan Records (Relationship Failures)**: 0

## File Ingest Statistics

| Filename | Purpose | Status | Rows Read | Valid Rows | Malformed Rows | Duplicate IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `allergies.csv` | Clinical/Patient Profile | PROCESSED | 40 | 40 | 0 | 0 |
| `authorization_requests.csv` | Clinical/Patient Profile | PROCESSED | 50 | 50 | 0 | 0 |
| `claims.csv` | Administrative/Billing | SKIPPED | 100 | 100 | 0 | 0 |
| `clinical_assessments.csv` | Clinical/Patient Profile | PROCESSED | 60 | 60 | 0 | 0 |
| `conditions.csv` | Clinical/Patient Profile | PROCESSED | 80 | 80 | 0 | 0 |
| `coverage.csv` | Administrative/Billing | SKIPPED | 30 | 30 | 0 | 0 |
| `diagnostic_results.csv` | Clinical/Patient Profile | PROCESSED | 80 | 80 | 0 | 0 |
| `encounters.csv` | Clinical/Patient Profile | PROCESSED | 80 | 80 | 0 | 0 |
| `family_history.csv` | Clinical/Patient Profile | PROCESSED | 40 | 40 | 0 | 0 |
| `functional_status.csv` | Clinical/Patient Profile | PROCESSED | 60 | 60 | 0 | 0 |
| `immunizations.csv` | Clinical/Patient Profile | PROCESSED | 60 | 60 | 0 | 0 |
| `medical_equipment.csv` | Clinical/Patient Profile | PROCESSED | 40 | 40 | 0 | 0 |
| `medications.csv` | Clinical/Patient Profile | PROCESSED | 100 | 100 | 0 | 0 |
| `patients.csv` | Clinical/Patient Profile | PROCESSED | 40 | 40 | 0 | 0 |
| `procedures.csv` | Clinical/Patient Profile | PROCESSED | 60 | 60 | 0 | 0 |
| `providers.csv` | Administrative/Billing | SKIPPED | 15 | 15 | 0 | 0 |
| `referrals.csv` | Clinical/Patient Profile | PROCESSED | 50 | 50 | 0 | 0 |
| `social_history.csv` | Clinical/Patient Profile | PROCESSED | 30 | 30 | 0 | 0 |
| `surgeries.csv` | Clinical/Patient Profile | PROCESSED | 50 | 50 | 0 | 0 |
| `vital_signs.csv` | Clinical/Patient Profile | PROCESSED | 100 | 100 | 0 | 0 |

## Skipper Rationale
- `claims.csv`: Administrative billing claims history, not necessary for patient clinical evidence extraction.
- `coverage.csv`: Plan coverage details (copay, deductible), not necessary for patient clinical evidence extraction.
- `providers.csv`: Doctor details, not necessary for patient clinical evidence extraction.

## Warnings and Errors
- No critical schema validation errors were encountered.
- Any row with mismatching column counts was logged as malformed and safely skipped.
- Orphan clinical records (referring to non-existent patients) were logged as relationship failures.
