import os
import re
import logging
from typing import List, Optional
import fitz  # PyMuPDF
from app.models.policy import ParsedPage

logger = logging.getLogger(__name__)

# Metadata regex patterns
EFFECTIVE_DATE_PATTERN = re.compile(r"Effective\s+Date:\s*([^\n\r]+)", re.IGNORECASE)
CPT_PATTERN = re.compile(r"\b\d{5}\b")
HCPCS_PATTERN = re.compile(r"\b[A-Z]\d{4}\b")


def parse_policy_pdf(filepath: str, payer: str) -> List[ParsedPage]:
    """
    Parses a single medical policy PDF document page-by-page.
    Extracts text, metadata, checks for scanned/empty pages, and logs unreadable issues.
    """
    if not os.path.exists(filepath):
        logger.error(f"Policy file not found: {filepath}")
        raise FileNotFoundError(f"Policy file not found: {filepath}")

    filename = os.path.basename(filepath)
    payer = payer.capitalize()
    
    try:
        doc = fitz.open(filepath)
    except Exception as e:
        logger.error(f"Failed to open PDF file {filepath} using PyMuPDF: {e}")
        raise ValueError(f"Failed to open PDF file {filepath}: {str(e)}")

    page_count = len(doc)
    parsed_pages = []
    
    # 1. Inspect first page to extract metadata
    first_page_text = ""
    if page_count > 0:
        first_page_text = doc[0].get_text()

    # Extract Policy ID
    policy_id = None
    id_match = re.search(r"\b(CG-[A-Z]+-\d+|[A-Z]+\.\d+)\b", first_page_text)
    if id_match:
        policy_id = id_match.group(1)
    else:
        # Check filename as fallback
        file_id_match = re.search(r"^([A-Z0-9\.\-]+)\s", filename)
        if file_id_match:
            policy_id = file_id_match.group(1)

    # Extract Title / Name
    policy_name = filename.replace(".pdf", "")
    lines = [l.strip() for l in first_page_text.split("\n") if l.strip()]
    if lines:
        detected_title = lines[0]
        if len(detected_title) < 5 and len(lines) > 1:
            detected_title = lines[0] + " " + lines[1]
        # Verify it's a plausible title length
        if 5 < len(detected_title) < 120:
            policy_name = detected_title

    # Extract dates
    whole_text = ""
    for page in doc:
        whole_text += "\n" + page.get_text()

    eff_match = EFFECTIVE_DATE_PATTERN.search(whole_text)
    effective_date = eff_match.group(1).strip() if eff_match else None
    if effective_date and len(effective_date) > 50:
        effective_date = effective_date[:50]

    # 2. Iterate page-by-page
    for page_num in range(page_count):
        page = doc[page_num]
        page_index = page_num + 1  # 1-indexed for reader citation transparency
        
        text = page.get_text()
        scanned = False
        
        # Validation checks
        if not text.strip():
            # If no text but contains images, it is a scanned page requiring OCR
            image_count = len(page.get_images())
            if image_count > 0:
                scanned = True
                logger.warning(
                    f"Warning: Page {page_index} of policy '{filename}' appears to be image-only / scanned."
                )
            else:
                logger.warning(
                    f"Warning: Page {page_index} of policy '{filename}' is empty."
                )
                
        # Scan and clean codes
        cpt_raw = CPT_PATTERN.findall(text)
        hcpcs_raw = HCPCS_PATTERN.findall(text)
        
        cpt_codes = set()
        for c in cpt_raw:
            if c.startswith("0000") or c in ["2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "12000", "50000", "90000"]:
                continue
            cpt_codes.add(c)

        parsed_pages.append(ParsedPage(
            payer=payer,
            policy_name=policy_name,
            policy_id=policy_id,
            effective_date=effective_date,
            source_file=filename,
            page_number=page_index,
            text=text,
            scanned=scanned,
            cpt_codes=sorted(list(cpt_codes)),
            hcpcs_codes=sorted(list(set(hcpcs_raw)))
        ))

    doc.close()
    return parsed_pages

def parse_all_policies(policies_dir: str) -> List[ParsedPage]:
    """
    Crawls the medical policy directories recursively and parses all PDFs.
    Returns a flat list of ParsedPage objects.
    """
    all_pages = []
    
    if not os.path.exists(policies_dir):
        logger.error(f"Policies folder not found at: {policies_dir}")
        raise FileNotFoundError(f"Policies folder not found at: {policies_dir}")

    for root, dirs, files in os.walk(policies_dir):
        payer = os.path.basename(root)
        if payer.lower() not in ["anthem", "uhc"]:
            continue
            
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue
                
            filepath = os.path.join(root, file)
            logger.info(f"Parsing policy PDF: {filepath}")
            
            try:
                pages = parse_policy_pdf(filepath, payer)
                all_pages.extend(pages)
            except Exception as e:
                logger.error(f"Parsing failed for file {file}: {e}")
                # We raise to follow error-fixing protocol: do not swallow exceptions silently
                raise e

    logger.info(f"Successfully batch-parsed {len(all_pages)} total policy pages.")
    return all_pages
