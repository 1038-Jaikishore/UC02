import re
import logging
from typing import List
from app.models.policy import ParsedPage, PolicyChunk

logger = logging.getLogger(__name__)

# Standard policy section headers to search for
SECTION_HEADERS = [
    "Medical Necessity",
    "Clinical Indications",
    "Coverage Guidelines",
    "Coding Section",
    "Exclusions",
    "Description",
    "Definitions",
    "References",
    "Revision History",
    "Indications and Limitations",
    "Prior Authorization Requirements"
]

# Construct a regex that matches any of the section headers as standalone terms/lines
HEADER_REGEX = re.compile(
    r"\b(" + "|".join(re.escape(h) for h in SECTION_HEADERS) + r")\b",
    re.IGNORECASE
)

def split_text_by_sections(text: str) -> List[dict]:
    """
    Slices a text block into segments based on detected section headers.
    Returns a list of dicts with 'section' and 'text'.
    """
    matches = list(HEADER_REGEX.finditer(text))
    if not matches:
        return [{"section": "General", "text": text.strip()}]

    segments = []
    
    # 1. Handle any text prior to the first detected section
    first_match = matches[0]
    if first_match.start() > 0:
        pre_text = text[:first_match.start()].strip()
        if pre_text:
            segments.append({"section": "General", "text": pre_text})

    # 2. Slice text between successive matches
    for i in range(len(matches)):
        start_idx = matches[i].start()
        header_name = matches[i].group(1)
        
        # Determine clean header case matching standard list
        matched_header = next((h for h in SECTION_HEADERS if h.lower() == header_name.lower()), header_name)

        if i + 1 < len(matches):
            end_idx = matches[i+1].start()
        else:
            end_idx = len(text)
            
        segment_text = text[start_idx:end_idx].strip()
        if segment_text:
            segments.append({"section": matched_header, "text": segment_text})

    return segments

def split_long_segment(text: str, max_chars: int = 2000, overlap: int = 200) -> List[str]:
    """
    Splits an excessively long text segment into smaller sub-chunks by paragraphs.
    Avoids arbitrary word/character truncation.
    """
    if len(text) <= max_chars + 100:
        return [text]

    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # If a single paragraph is larger than max_chars, split it
        if len(para) > max_chars:
            sentences = re.split(r"(?<=[.!?])\s+", para)
            # If paragraph cannot be split by sentences, split by index slices
            if len(sentences) == 1 and len(para) > max_chars:
                for idx in range(0, len(para), max_chars):
                    slice_t = para[idx:idx + max_chars]
                    if current_length + len(slice_t) > max_chars and current_chunk:
                        chunks.append("\n".join(current_chunk))
                        current_chunk = []
                        current_length = 0
                    current_chunk.append(slice_t)
                    current_length += len(slice_t)
            else:
                for sentence in sentences:
                    if current_length + len(sentence) > max_chars and current_chunk:
                        chunks.append("\n".join(current_chunk))
                        current_chunk = []
                        current_length = 0
                    current_chunk.append(sentence)
                    current_length += len(sentence)
        else:
            if current_length + len(para) > max_chars and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                # Small overlap: retain the last paragraph if possible
                overlap_para = current_chunk[-1] if len(current_chunk[-1]) < overlap else ""
                current_chunk = [overlap_para] if overlap_para else []
                current_length = len(overlap_para)
                
            current_chunk.append(para)
            current_length += len(para)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks

def chunk_page(page: ParsedPage, start_index: int) -> List[PolicyChunk]:
    """
    Splits a ParsedPage into one or more PolicyChunk objects.
    Maintains provenance metadata.
    """
    segments = split_text_by_sections(page.text)
    chunks = []
    current_idx = start_index

    for seg in segments:
        sub_texts = split_long_segment(seg["text"])
        for sub_t in sub_texts:
            chunks.append(PolicyChunk(
                source_type="PAYER",
                source_name=page.payer,
                policy_name=page.policy_name,
                policy_id=page.policy_id,
                effective_date=page.effective_date,
                source_file=page.source_file,
                page_number=page.page_number,
                section=seg["section"],
                text=sub_t,
                chunk_index=current_idx
            ))
            current_idx += 1

    return chunks

def chunk_all_pages(pages: List[ParsedPage]) -> List[PolicyChunk]:
    """
    Processes all parsed pages and returns a flat list of PolicyChunks.
    Guarantees no cross-policy or cross-payer merging.
    """
    all_chunks = []
    global_index = 0

    for page in pages:
        page_chunks = chunk_page(page, global_index)
        all_chunks.extend(page_chunks)
        global_index += len(page_chunks)

    logger.info(f"Chunked {len(pages)} pages into {len(all_chunks)} policy chunks.")
    return all_chunks
