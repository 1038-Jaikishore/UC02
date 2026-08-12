import json
import logging
from app.services import llm_client
from app.models.extraction import ClinicalExtraction

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert clinical data extraction assistant. Your job is to extract specific clinical facts from the provider's prior authorization clinical notes.

You must output a valid JSON object matching the following structure exactly:
{
  "diagnosis": "The primary diagnosed condition (string, or null if unspecified)",
  "requested_procedure": "The name of the requested procedure (string, or null if unspecified)",
  "symptom_duration_weeks": (integer representation of symptom duration in weeks, or null if unspecified),
  "physiotherapy_weeks": (integer representation of physiotherapy completed in weeks, or null if unspecified),
  "medications_attempted": ["List of anti-inflammatory, steroid, or other relevant medications tried (array of strings)"],
  "previous_imaging": ["List of previous scans/imaging received (array of strings)"],
  "relevant_conditions": ["Other relevant chronic/underlying health conditions (array of strings)"],
  "unknown_fields": ["List of clinical concepts, therapies, or durations whose status is completely missing or unspecified in the text"]
}

Strict Rules:
1. Extract ONLY facts explicitly stated in the text.
2. Never infer, extrapolate, or assume clinical history. If a detail is missing (e.g., symptom duration is not given, or drug attempt durations are missing), it must remain null or empty.
3. Convert timeframes to weeks mathematically if specified in months/days (e.g. 2 months -> 8 weeks). If only an approximate duration is given, make a conservative estimate.
4. Do not offer a medical opinion, recommendation, or advice on whether the request should be approved or denied.
5. Ensure the output is valid, parsable JSON. Do not include any markdown styling, conversational text, or explanation outside of the JSON object.
"""

async def extract_clinical_info(clinical_notes: str) -> ClinicalExtraction:
    """
    Parses clinical notes and extracts structured clinical evidence fields using the configured LLM.
    Validates the response structure using Pydantic.
    """
    if not clinical_notes or not clinical_notes.strip():
        # Handle empty notes gracefully by returning an empty model
        return ClinicalExtraction()
        
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Prior Authorization Clinical Notes:\n{clinical_notes}"}
    ]
    
    try:
        raw_response = await llm_client.generate_response(
            messages=messages,
            response_format="json_object"
        )
        
        # Clean any accidental markdown wrappers if the provider ignores response_format
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        # Validate Pydantic schema
        extraction = ClinicalExtraction.model_validate_json(cleaned_response)
        logger.info(f"Clinical facts successfully extracted and validated for note: {clinical_notes[:50]}...")
        return extraction
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode LLM response as JSON: {raw_response}. Error: {e}")
        raise ValueError(f"LLM returned an invalid JSON structure: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error during clinical extraction: {e}")
        # Propagate custom LLM provider errors directly
        raise e
