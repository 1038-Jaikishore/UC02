import os
import re
import json
import fitz  # PyMuPDF

POLICIES_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/policies"

# Regex patterns
CPT_PATTERN = re.compile(r"\b\d{5}\b")  # matches 5 digit codes
HCPCS_PATTERN = re.compile(r"\b[A-Z]\d{4}\b")  # matches HCPCS e.g. J1234
ICD_PATTERN = re.compile(r"\b[A-Z]\d{2}\.\d[0-9A-Z]?\b")  # matches ICD-10 e.g. M17.11

# Date patterns (general search)
EFFECTIVE_DATE_PATTERN = re.compile(r"Effective\s+Date:\s*([^\n\r]+)", re.IGNORECASE)
REVISION_DATE_PATTERN = re.compile(r"(Revision|Revised|Published|Last\s+Review)\s+Date:\s*([^\n\r]+)", re.IGNORECASE)

def inspect_pdf(filepath, payer, filename):
    try:
        doc = fitz.open(filepath)
    except Exception as e:
        return {
            "payer": payer,
            "filename": filename,
            "relative_path": os.path.relpath(filepath, POLICIES_DIR),
            "page_count": 0,
            "title": "unknown",
            "policy_id": "unknown",
            "version": "unknown",
            "effective_date": "unknown",
            "revision_date": "unknown",
            "procedure_service": "unknown",
            "cpt_codes": [],
            "hcpcs_codes": [],
            "icd_codes": [],
            "sections": [],
            "extraction_status": "FAILED",
            "scanned": False,
            "warnings": [f"Failed to open PDF: {str(e)}"],
            "errors": [str(e)]
        }

    page_count = len(doc)
    text_content = ""
    scanned_pages = 0
    empty_pages = 0
    
    first_page_text = ""
    if page_count > 0:
        first_page_text = doc[0].get_text()

    # Extract sections by looking for potential section headings in the text
    section_candidates = [
        "Description", "Clinical Indications", "Coverage Guidelines",
        "Medical Necessity", "Exclusions", "Coding Section", "CPT/HCPCS Codes",
        "Billing Guidelines", "Definitions", "References", "Revision History",
        "Indications and Limitations"
    ]
    detected_sections = set()

    cpt_codes = set()
    hcpcs_codes = set()
    icd_codes = set()

    for page_num in range(page_count):
        page = doc[page_num]
        p_text = page.get_text()
        if not p_text.strip():
            empty_pages += 1
            # Check if it has images to determine if scanned
            if len(page.get_images()) > 0:
                scanned_pages += 1
            else:
                # truly empty
                pass
        else:
            text_content += "\n" + p_text
            
        # Scan for sections
        for sec in section_candidates:
            if re.search(r"\b" + re.escape(sec) + r"\b", p_text, re.IGNORECASE):
                detected_sections.add(sec)

        # Scan for codes
        for code in CPT_PATTERN.findall(p_text):
            # Ignore common numbers (like dates, page counts, or zip codes if not CPTs)
            cpt_codes.add(code)
        for code in HCPCS_PATTERN.findall(p_text):
            hcpcs_codes.add(code)
        for code in ICD_PATTERN.findall(p_text):
            icd_codes.add(code)

    # Clean CPT codes (e.g. exclude years like 2020, 2021, 2022, 2023, 2024, 2025, 2026, or counts like 00000)
    cleaned_cpt = []
    for c in cpt_codes:
        if c.startswith("0000") or c in ["2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "12000", "50000", "90000"]:
            continue
        cleaned_cpt.append(c)

    # Detect title
    title = "unknown"
    # For Anthem, often the first line or filename gives the title/code.
    # Let's inspect the first few lines of the first page.
    lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]
    if lines:
        title = lines[0]
        if len(title) < 5 and len(lines) > 1:
            title = lines[0] + " " + lines[1]
        if len(title) > 120:
            title = title[:120] + "..."

    # Detect Policy ID
    policy_id = "unknown"
    # Anthem policies often start with CG- or RAD. or SURG.
    id_match = re.search(r"\b(CG-[A-Z]+-\d+|[A-Z]+\.\d+)\b", first_page_text)
    if id_match:
        policy_id = id_match.group(1)
    else:
        # Check filename
        file_id_match = re.search(r"^([A-Z0-9\.\-]+)\s", filename)
        if file_id_match:
            policy_id = file_id_match.group(1)

    # Detect dates
    eff_match = EFFECTIVE_DATE_PATTERN.search(text_content)
    rev_match = REVISION_DATE_PATTERN.search(text_content)

    effective_date = eff_match.group(1).strip() if eff_match else "unknown"
    revision_date = rev_match.group(2).strip() if rev_match else "unknown"

    # Clean dates
    if len(effective_date) > 50:
        effective_date = effective_date[:50] + "..."
    if len(revision_date) > 50:
        revision_date = revision_date[:50] + "..."

    # Is it scanned/image-only?
    is_scanned = (scanned_pages == page_count and page_count > 0)
    is_partially_scanned = (scanned_pages > 0 and scanned_pages < page_count)

    warnings = []
    if is_scanned:
        warnings.append("Image-only/Scanned PDF (No extractable text).")
    if is_partially_scanned:
        warnings.append(f"Partially scanned PDF ({scanned_pages} of {page_count} pages are image-only).")
    if empty_pages > 0:
        warnings.append(f"Contains {empty_pages} empty pages.")

    doc.close()

    return {
        "payer": payer,
        "filename": filename,
        "relative_path": os.path.relpath(filepath, POLICIES_DIR),
        "page_count": page_count,
        "title": title,
        "policy_id": policy_id,
        "version": "unknown",
        "effective_date": effective_date,
        "revision_date": revision_date,
        "procedure_service": title,
        "cpt_codes": sorted(list(cleaned_cpt)),
        "hcpcs_codes": sorted(list(hcpcs_codes)),
        "icd_codes": sorted(list(icd_codes)),
        "sections": sorted(list(detected_sections)),
        "extraction_status": "SUCCESS" if not is_scanned else "OCR_REQUIRED",
        "scanned": is_scanned,
        "warnings": warnings,
        "errors": []
    }

def main():
    results = []
    
    # 1. Discover all files
    for root, dirs, files in os.walk(POLICIES_DIR):
        payer = os.path.basename(root)
        if payer not in ["anthem", "uhc"]:
            continue
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue
            filepath = os.path.join(root, file)
            info = inspect_pdf(filepath, payer.capitalize(), file)
            results.append(info)

    # Print a summary JSON or report
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
