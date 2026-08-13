import os
import json
from inspect_policies import inspect_pdf

POLICIES_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/policies"
OUTPUT_FILE = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/POLICY_DATASET_SCHEMA.md"

def generate_markdown(policies):
    # Sort policies by payer and then name
    policies.sort(key=lambda x: (x["payer"], x["filename"]))

    anthem_count = sum(1 for p in policies if p["payer"].lower() == "anthem")
    uhc_count = sum(1 for p in policies if p["payer"].lower() == "uhc")
    total_pages = sum(p["page_count"] for p in policies)
    total_policies = len(policies)

    md = []
    md.append("# Medical Policy Dataset Schema")
    md.append("")
    md.append("This document profiles all discovered medical policy PDF documents in the system repository, establishing document structure, page counts, CPT/HCPCS codes, and parsing viability for downstream RAG extraction.")
    md.append("")
    
    # Summary Section
    md.append("## Dataset Summary")
    md.append("")
    md.append(f"- **Anthem policies**: {anthem_count}")
    md.append(f"- **UHC policies**: {uhc_count}")
    md.append(f"- **Total policies**: {total_policies}")
    md.append(f"- **Total pages**: {total_pages}")
    md.append("")

    # Detailed Table
    md.append("## Policy Inventory Table")
    md.append("")
    md.append("| Payer | Filename | Relative Path | Pages | Policy Title | Policy ID | Effective Date | CPT Codes | HCPCS Codes | Sections | Extraction Status |")
    md.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")

    for p in policies:
        payer = p["payer"]
        filename = p["filename"]
        rel_path = p["relative_path"]
        pages = p["page_count"]
        title = p["title"]
        policy_id = p["policy_id"]
        eff_date = p["effective_date"]
        
        cpts = ", ".join(p["cpt_codes"][:8]) + ("..." if len(p["cpt_codes"]) > 8 else "")
        if not cpts:
            cpts = "none"
            
        hcpcs = ", ".join(p["hcpcs_codes"][:5]) + ("..." if len(p["hcpcs_codes"]) > 5 else "")
        if not hcpcs:
            hcpcs = "none"

        sections = ", ".join(p["sections"][:4]) + ("..." if len(p["sections"]) > 4 else "")
        if not sections:
            sections = "none"

        status = p["extraction_status"]
        if p["warnings"]:
            status += " (Warning: " + "; ".join(p["warnings"]) + ")"

        md.append(f"| {payer} | {filename} | {rel_path} | {pages} | {title} | {policy_id} | {eff_date} | {cpts} | {hcpcs} | {sections} | {status} |")

    md.append("")
    md.append("## Document Metadata Details")
    md.append("")
    
    for p in policies:
        md.append(f"### {p['payer']}: {p['filename']}")
        md.append("")
        md.append(f"- **Relative Path**: `{p['relative_path']}`")
        md.append(f"- **Page Count**: {p['page_count']}")
        md.append(f"- **Policy Title**: {p['title']}")
        md.append(f"- **Policy ID**: {p['policy_id']}")
        md.append(f"- **Effective Date**: {p['effective_date']}")
        md.append(f"- **Revision Date**: {p['revision_date']}")
        md.append(f"- **CPT Reference Codes**: `{p['cpt_codes']}`")
        md.append(f"- **HCPCS Reference Codes**: `{p['hcpcs_codes']}`")
        md.append(f"- **ICD Reference Codes**: `{p['icd_codes']}`")
        md.append(f"- **Sections Detected**: {p['sections']}")
        md.append(f"- **Extraction Status**: `{p['extraction_status']}`")
        if p["warnings"]:
            md.append(f"- **Warnings**: `{p['warnings']}`")
        md.append("")
        md.append("---")
        md.append("")

    return "\n".join(md)

def main():
    policies = []
    for root, dirs, files in os.walk(POLICIES_DIR):
        payer = os.path.basename(root)
        if payer not in ["anthem", "uhc"]:
            continue
        for file in files:
            if not file.lower().endswith(".pdf"):
                continue
            filepath = os.path.join(root, file)
            info = inspect_pdf(filepath, payer.capitalize(), file)
            policies.append(info)
            
    markdown_content = generate_markdown(policies)
    with open(OUTPUT_FILE, "w") as f:
        f.write(markdown_content)
    print(f"Dataset schema written successfully to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
