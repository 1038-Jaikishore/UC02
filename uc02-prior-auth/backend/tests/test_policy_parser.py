import os
import pytest
from unittest.mock import MagicMock, patch
from app.services import policy_parser
from app.models.policy import ParsedPage

POLICIES_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/policies"

def test_parse_single_pdf_integration():
    # Test with a real digital PDF from the Anthem directory
    filepath = os.path.join(POLICIES_DIR, "anthem", "CG-MED-62 Resting Electrocardiogram Screening in Adults.pdf")
    
    # Run parsing
    pages = policy_parser.parse_policy_pdf(filepath, "Anthem")
    
    # Assertions
    assert isinstance(pages, list)
    assert len(pages) == 4
    for p in pages:
        assert isinstance(p, ParsedPage)
        assert p.payer == "Anthem"
        assert p.source_file == "CG-MED-62 Resting Electrocardiogram Screening in Adults.pdf"
        assert p.page_number >= 1
        assert p.text != ""
        assert p.scanned is False

def test_parse_pdf_file_not_found():
    with pytest.raises(FileNotFoundError):
        policy_parser.parse_policy_pdf("nonexistent_policy.pdf", "UHC")

def test_parse_all_policies_integration():
    # Test batch parsing on the active 29 policies
    pages = policy_parser.parse_all_policies(POLICIES_DIR)
    
    # Assertions
    assert isinstance(pages, list)
    assert len(pages) == 268  # Sum of all pages in dataset summary
    
    # Verify count per payer
    anthem_pages = [p for p in pages if p.payer == "Anthem"]
    uhc_pages = [p for p in pages if p.payer == "Uhc"]
    
    assert len(anthem_pages) > 0
    assert len(uhc_pages) > 0
    assert len(pages) == len(anthem_pages) + len(uhc_pages)
