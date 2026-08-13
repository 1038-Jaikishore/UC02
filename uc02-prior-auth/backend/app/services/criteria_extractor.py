import json
import logging
from typing import List, Tuple
from app.services import llm_client
from app.models.policy import PolicyChunk
from app.models.criteria import PolicyCriteriaOutput

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert healthcare policy analyst. Your task is to extract structured medical necessity criteria rules from the provided policy text document chunks.

You must output a valid JSON object matching this structure exactly:
{
  "policy_name": "The standard name of the medical policy",
  "criteria": [
    {
      "criterion_id": "C1",
      "description": "Clear statement of the clinical requirement (e.g., 'Conservative therapy attempted for at least 6 weeks')",
      "required": true,
      "operator": ">=",
      "required_value": 6,
      "unit": "weeks",
      "source_page": 6,
      "source_section": "Medical Necessity"
    }
  ]
}

Strict Rules:
1. Extract ONLY criteria explicitly supported by the text chunks.
2. ZERO-HALLUCINATION: Never invent values for treatment durations, symptom durations, medication attempts, age thresholds, or exclusion categories. If a value (operator, required_value, or unit) is not explicitly quantified or specified in the text, you must set them to null.
3. Every criterion MUST carry its source provenance: source_page and source_section MUST match exactly the chunk metadata from which it was extracted.
4. If multiple chunks represent different parts of the same policy, merge the criteria list and attribute each criterion to its specific page/section chunk index source.
5. Operator must be one of: ">=", "<=", "==", "contains", "not_contains", or null.
6. Ensure the output is valid, parsable JSON. Do not include markdown code block wrappers (like ```json) or any explanation outside of the JSON object.
"""

async def extract_policy_criteria(chunks: List[Tuple[PolicyChunk, float]]) -> PolicyCriteriaOutput:
    """
    Calls the LLM to extract structured criteria from the retrieved policy chunks.
    Validates the structured response using the Pydantic schema.
    """
    if not chunks:
        return PolicyCriteriaOutput(policy_name="Unknown Policy", criteria=[])

    # 1. Compile context from retrieved chunks
    context_parts = []
    policy_name = chunks[0][0].policy_name
    
    for idx, (chunk, score) in enumerate(chunks):
        context_parts.append(
            f"Chunk #{idx+1} Metadata:\n"
            f"- Source Page: {chunk.page_number}\n"
            f"- Source Section: {chunk.section}\n"
            f"- Policy Name: {chunk.policy_name}\n"
            f"- Payer: {chunk.source_name}\n"
            f"Text Content:\n"
            f"\"\"\"\n{chunk.text}\n\"\"\"\n"
            f"----------------------------------------"
        )
        
    user_content = (
        f"Retrieved Medical Policy Chunks:\n\n"
        + "\n".join(context_parts)
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content}
    ]

    try:
        raw_response = await llm_client.generate_response(
            messages=messages,
            response_format="json_object"
        )
        
        # Clean any accidental markdown wrapper artifacts
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        # Validate Pydantic schema
        output = PolicyCriteriaOutput.model_validate_json(cleaned_response)
        logger.info(f"Successfully extracted {len(output.criteria)} criteria for policy: {policy_name}")
        return output
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode LLM response as JSON: {raw_response}. Error: {e}")
        raise ValueError(f"LLM returned an invalid JSON structure: {str(e)}")
    except Exception as e:
        logger.error(f"Error during criteria extraction: {e}")
        raise e
