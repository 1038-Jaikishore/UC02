import pytest
from app.models.policy import ParsedPage, PolicyChunk
from app.services import policy_parser, policy_chunker

POLICIES_DIR = "/Users/jaikishorep/Desktop/UC02/uc02-prior-auth/backend/data/policies"

def test_split_text_by_sections():
    sample_text = (
        "This is some title page intro.\n"
        "Description:\n"
        "This policy describes bariatric surgeries.\n"
        "Medical Necessity:\n"
        "Surgery is medically necessary if BMI >= 40."
    )
    
    segments = policy_chunker.split_text_by_sections(sample_text)
    
    assert len(segments) == 3
    assert segments[0]["section"] == "General"
    assert "intro" in segments[0]["text"]
    
    assert segments[1]["section"] == "Description"
    assert "bariatric" in segments[1]["text"]
    
    assert segments[2]["section"] == "Medical Necessity"
    assert "BMI" in segments[2]["text"]

def test_split_long_segment():
    long_para = "A" * 3000
    chunks = policy_chunker.split_long_segment(long_para, max_chars=2000)
    
    assert len(chunks) == 2
    assert len(chunks[0]) <= 2000
    assert len(chunks[1]) <= 2000

def test_chunk_page_metadata():
    page = ParsedPage(
        payer="Anthem",
        policy_name="Obesity Policy",
        policy_id="CG-SURG-83",
        effective_date="Nov 2025",
        source_file="severe_obesity.pdf",
        page_number=2,
        text="Description:\nObesity is a health issue.\nMedical Necessity:\nMust be age > 18.",
        scanned=False
    )
    
    chunks = policy_chunker.chunk_page(page, start_index=10)
    
    assert len(chunks) == 2
    
    c1 = chunks[0]
    assert c1.source_name == "Anthem"
    assert c1.policy_name == "Obesity Policy"
    assert c1.policy_id == "CG-SURG-83"
    assert c1.effective_date == "Nov 2025"
    assert c1.source_file == "severe_obesity.pdf"
    assert c1.page_number == 2
    assert c1.section == "Description"
    assert c1.chunk_index == 10
    
    c2 = chunks[1]
    assert c2.section == "Medical Necessity"
    assert c2.chunk_index == 11

def test_chunk_all_pages_integration():
    # Parse all 29 policies (268 pages)
    pages = policy_parser.parse_all_policies(POLICIES_DIR)
    
    # Chunk all pages
    chunks = policy_chunker.chunk_all_pages(pages)
    
    assert isinstance(chunks, list)
    assert len(chunks) >= 268  # Since some pages split into multiple sections/paragraphs
    
    # Verify sequential indexes
    for idx, c in enumerate(chunks):
        assert isinstance(c, PolicyChunk)
        assert c.chunk_index == idx
        assert c.text != ""
        assert c.section != ""
        assert c.source_name in ["Anthem", "Uhc"]
