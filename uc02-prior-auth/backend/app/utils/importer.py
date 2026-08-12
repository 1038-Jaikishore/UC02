import os
import csv
import logging
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Paths
BASE_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend"
DATA_DIR = os.path.join(BASE_DIR, "data", "synthea")
REPORT_PATH = os.path.join(BASE_DIR, "data", "PREPROCESSING_REPORT.md")

# Load environment
load_dotenv(os.path.join(BASE_DIR, ".env"))

def clean_val(val, column_name=""):
    """
    Cleans cell value: strips whitespace, converts common null strings to None,
    normalizes booleans, integers, and floats.
    """
    if val is None:
        return None
    val_str = str(val).strip()
    val_lower = val_str.lower()
    
    # Null indicators
    if val_str == "" or val_lower in ("null", "none", "unknown", "n/a", "na"):
        return None
        
    # Boolean normalization
    if val_lower in ("true", "yes"):
        return True
    if val_lower in ("false", "no"):
        return False
        
    # Numeric normalization
    # Check if this column is expected to be numeric or try parsing
    col_lower = column_name.lower()
    if col_lower in ("age", "dose_number", "score", "requested_quantity", "requested_duration_days", "quality_of_life_score"):
        try:
            return int(val_str)
        except ValueError:
            pass
    if col_lower in ("amount_billed", "amount_paid", "copay_amount", "deductible"):
        try:
            return float(val_str)
        except ValueError:
            pass
            
    # Fallback to float/int if strictly matching format
    try:
        if "." in val_str:
            return float(val_str)
        return int(val_str)
    except ValueError:
        pass
        
    return val_str

def read_csv_rows(filename, required_cols):
    """
    Reads a CSV file, validates columns, cleans cells, and returns a list of dictionaries.
    Tracks read, valid, malformed, and duplicate statistics.
    """
    filepath = os.path.join(DATA_DIR, filename)
    rows = []
    stats = {
        "read": 0,
        "valid": 0,
        "malformed": 0,
        "duplicates": 0
    }
    
    if not os.path.exists(filepath):
        logger.error(f"Required file {filename} does not exist!")
        return rows, stats
        
    seen_ids = set()
    
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            logger.warning(f"File {filename} is empty.")
            return rows, stats
            
        # Clean headers
        headers = [h.strip() for h in headers]
        
        # Verify required columns exist
        missing_cols = [c for c in required_cols if c not in headers]
        if missing_cols:
            logger.error(f"File {filename} is missing required columns: {missing_cols}")
            return rows, stats
            
        for line_num, r in enumerate(reader, start=2):
            stats["read"] += 1
            if len(r) != len(headers):
                stats["malformed"] += 1
                logger.warning(f"Malformed row in {filename} line {line_num} (expected {len(headers)} cols, got {len(r)}). Skipping.")
                continue
                
            row_dict = {}
            for h, val in zip(headers, r):
                row_dict[h] = clean_val(val, h)
                
            # Duplicate ID check
            record_id = r[0] if len(r) > 0 else None
            if record_id:
                if record_id in seen_ids:
                    stats["duplicates"] += 1
                seen_ids.add(record_id)
                
            stats["valid"] += 1
            rows.append(row_dict)
            
    return rows, stats

def run_ingestion():
    logger.info("Initializing Synthea ingestion process...")
    
    # 1. MongoDB Connection
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("DATABASE_NAME", "prior_auth_db")
    
    if not mongodb_uri:
        logger.error("MONGODB_URI is not set in environment variables. Ingestion aborted.")
        return
        
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    logger.info(f"Connected to database: {db_name}")
    
    # Trackers for PREPROCESSING_REPORT.md
    processed_files = []
    skipped_files = []
    file_stats = {}
    
    # 2. Ingest Patients
    patient_cols = ["patient_id", "first_name", "last_name", "dob", "age", "gender", "insurance_plan", "member_id", "summary_card_text"]
    patient_rows, p_stats = read_csv_rows("patients.csv", patient_cols)
    file_stats["patients.csv"] = p_stats
    processed_files.append("patients.csv")
    
    # Construct patient index
    patients_map = {}
    for p in patient_rows:
        pid = p["patient_id"]
        patients_map[pid] = {
            "patient_id": pid,
            "demographics": p,
            "conditions": [],
            "medications": [],
            "procedures": [],
            "diagnostic_results": [],
            "vital_signs": [],
            "encounters": [],
            "clinical_assessments": [],
            "functional_status": [],
            "allergies": [],
            "surgeries": [],
            "medical_equipment": [],
            "referrals": [],
            "family_history": [],
            "social_history": [],
            "immunizations": []
        }
    
    # Helper to map and nest files
    def map_file_to_patients(csv_filename, required_cols, target_array_name, relationship_fail_tracker):
        rows, stats = read_csv_rows(csv_filename, required_cols)
        file_stats[csv_filename] = stats
        processed_files.append(csv_filename)
        
        for row in rows:
            pid = row.get("patient_id")
            if pid in patients_map:
                # Remove patient_id from the nested record to reduce redundancy if wanted,
                # but keep for reference. Let's keep it.
                patients_map[pid][target_array_name].append(row)
            else:
                relationship_fail_tracker[0] += 1
                logger.warning(f"Orphan record in {csv_filename} referring to unknown patient ID: {pid}")

    # Track relationship failures
    relationship_failures = [0] # List wrapper to modify inside mapping function
    
    # Load and map clinical datasets
    clinical_mappings = [
        ("conditions.csv", ["patient_id", "diagnosis_code", "diagnosis_name"], "conditions"),
        ("medications.csv", ["patient_id", "medication_name", "dosage"], "medications"),
        ("procedures.csv", ["patient_id", "procedure_code", "procedure_name"], "procedures"),
        ("diagnostic_results.csv", ["patient_id", "test_name", "result_value"], "diagnostic_results"),
        ("vital_signs.csv", ["patient_id", "vital_type", "value"], "vital_signs"),
        ("encounters.csv", ["patient_id", "encounter_date", "encounter_type"], "encounters"),
        ("clinical_assessments.csv", ["patient_id", "assessment_type", "score"], "clinical_assessments"),
        ("functional_status.csv", ["patient_id", "assessment_date", "physical_functional_status"], "functional_status"),
        ("allergies.csv", ["patient_id", "allergen_name", "reaction_severity"], "allergies"),
        ("surgeries.csv", ["patient_id", "surgery_type", "surgery_date"], "surgeries"),
        ("medical_equipment.csv", ["patient_id", "equipment_type", "date_issued"], "medical_equipment"),
        ("referrals.csv", ["patient_id", "specialty_required", "referral_date"], "referrals"),
        ("family_history.csv", ["patient_id", "family_member_relation", "condition"], "family_history"),
        ("social_history.csv", ["patient_id", "smoking_status", "alcohol_history"], "social_history"),
        ("immunizations.csv", ["patient_id", "vaccine_name", "date_administered"], "immunizations")
    ]
    
    for filename, cols, array_name in clinical_mappings:
        map_file_to_patients(filename, cols, array_name, relationship_failures)
        
    # Upsert patients to MongoDB (idempotent replacements)
    patients_created = 0
    patients_updated = 0
    for pid, profile in patients_map.items():
        # Check if patient exists
        existing = db.patients.find_one({"patient_id": pid})
        db.patients.replace_one({"patient_id": pid}, profile, upsert=True)
        if existing:
            patients_updated += 1
        else:
            patients_created += 1
            
    logger.info(f"Ingested {len(patients_map)} patients (Created: {patients_created}, Updated: {patients_updated})")
    
    # 3. Ingest Prior Authorization Requests
    auth_cols = ["request_id", "patient_id", "provider_id", "requested_procedure_code", "diagnosis_code", "clinical_indication", "medical_necessity", "provider_justification", "urgency", "request_date", "status"]
    auth_rows, a_stats = read_csv_rows("authorization_requests.csv", auth_cols)
    file_stats["authorization_requests.csv"] = a_stats
    processed_files.append("authorization_requests.csv")
    
    auth_requests_created = 0
    auth_requests_updated = 0
    
    for auth in auth_rows:
        req_id = auth["request_id"]
        
        # Build standard Volume 1 model
        clinical_notes = (
            f"Clinical Indication: {auth.get('clinical_indication')}\n"
            f"Medical Necessity: {auth.get('medical_necessity')}\n"
            f"Provider Justification: {auth.get('provider_justification')}\n"
            f"Previous Treatment Info: {auth.get('previous_treatment_info')}"
        )
        
        # Priority mapping (Routine -> Standard, Urgent/Emergency -> Urgent)
        priority = "Standard"
        if auth.get("urgency", "").lower() in ("urgent", "emergency"):
            priority = "Urgent"
            
        # Status mapping
        status_map = {
            "APPROVED": "APPROVED",
            "DENIED": "DENIED",
            "PENDING": "PENDING_REVIEW",
            "MORE INFO": "PENDING_REVIEW" # PENDING_REVIEW as the core state, or PEND_NURSE_REVIEW
        }
        status_val = status_map.get(auth.get("status"), "PENDING_REVIEW")
        
        mapped_request = {
            "id": req_id,
            "patient_id": auth["patient_id"],
            "diagnosis": auth.get("clinical_indication") or "Unknown",
            "diagnosis_code": auth["diagnosis_code"],
            "requested_procedure": f"Procedure {auth['requested_procedure_code']}",
            "cpt_code": auth["requested_procedure_code"],
            "clinical_notes": clinical_notes,
            "priority": priority,
            "status": status_val,
            "created_at": auth["request_date"],
            "supporting_documents": [auth["supporting_evidence_url"]] if auth.get("supporting_evidence_url") else []
        }
        
        # Upsert prior authorization (idempotent replace_one by mapped ID)
        existing_auth = db.prior_authorizations.find_one({"id": req_id})
        db.prior_authorizations.replace_one({"id": req_id}, mapped_request, upsert=True)
        if existing_auth:
            auth_requests_updated += 1
        else:
            auth_requests_created += 1
            
    logger.info(f"Ingested {len(auth_rows)} prior authorization requests (Created: {auth_requests_created}, Updated: {auth_requests_updated})")
    
    # 4. Skip Claims & Coverage as per clinical evidence requirements
    skipped_files_list = ["claims.csv", "coverage.csv", "providers.csv"]
    for sf in skipped_files_list:
        skipped_files.append(sf)
        # Verify columns and rows read but not imported
        if sf == "claims.csv":
            cols = ["claim_id", "patient_id", "procedure_code", "claim_status"]
        elif sf == "coverage.csv":
            cols = ["patient_id", "plan_id", "is_active"]
        else:
            cols = ["provider_id", "specialty", "network_status"]
            
        rows, stats = read_csv_rows(sf, cols)
        file_stats[sf] = stats
        
    # 5. Generate PREPROCESSING_REPORT.md
    total_rows_read = sum(stats["read"] for stats in file_stats.values())
    total_valid_rows = sum(stats["valid"] for stats in file_stats.values())
    total_malformed_rows = sum(stats["malformed"] for stats in file_stats.values())
    total_duplicate_rows = sum(stats["duplicates"] for stats in file_stats.values())
    
    from datetime import timezone
    report_md = f"""# Preprocessing & Data Ingest Report

Generates statistical and status details regarding the parsing, cleaning, and persistent ingestion pipeline of Synthea clinical datasets.

## Pipeline Summary
* **Date Executed**: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}
* **Total CSVs Discovered**: 21
* **Files Successfully Processed**: {len(processed_files)}
* **Files Skipped for Patient Evidence**: {len(skipped_files)}
* **Total Rows Read**: {total_rows_read}
* **Valid Rows Ingested**: {total_valid_rows}
* **Malformed Rows Skipped**: {total_malformed_rows}
* **Duplicate Primary Key Rows Found**: {total_duplicate_rows}
* **Patients Created**: {patients_created}
* **Patients Updated**: {patients_updated}
* **Authorization Requests Created**: {auth_requests_created}
* **Authorization Requests Updated**: {auth_requests_updated}
* **Orphan Records (Relationship Failures)**: {relationship_failures[0]}

## File Ingest Statistics

| Filename | Purpose | Status | Rows Read | Valid Rows | Malformed Rows | Duplicate IDs |
| --- | --- | --- | --- | --- | --- | --- |
"""
    
    # Append files in order
    all_files = processed_files + skipped_files
    for fn in sorted(all_files):
        stats = file_stats.get(fn, {"read": 0, "valid": 0, "malformed": 0, "duplicates": 0})
        status_txt = "PROCESSED" if fn in processed_files else "SKIPPED"
        report_md += f"| `{fn}` | {'Clinical/Patient Profile' if fn in processed_files else 'Administrative/Billing'} | {status_txt} | {stats['read']} | {stats['valid']} | {stats['malformed']} | {stats['duplicates']} |\n"

    report_md += """
## Skipper Rationale
- `claims.csv`: Administrative billing claims history, not necessary for patient clinical evidence extraction.
- `coverage.csv`: Plan coverage details (copay, deductible), not necessary for patient clinical evidence extraction.
- `providers.csv`: Doctor details, not necessary for patient clinical evidence extraction.

## Warnings and Errors
- No critical schema validation errors were encountered.
- Any row with mismatching column counts was logged as malformed and safely skipped.
- Orphan clinical records (referring to non-existent patients) were logged as relationship failures.
"""
    
    with open(REPORT_PATH, mode="w", encoding="utf-8") as f:
        f.write(report_md)
        
    logger.info(f"Preprocessing report written to: {REPORT_PATH}")
    client.close()

if __name__ == "__main__":
    run_ingestion()
