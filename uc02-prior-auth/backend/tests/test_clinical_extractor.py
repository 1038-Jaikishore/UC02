import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services import clinical_extractor, llm_client
from app.models.extraction import ClinicalExtraction

@pytest.mark.anyio
@patch("app.services.llm_client.generate_response")
async def test_extract_clinical_info_complete(mock_generate_response):
    # Simulated correct JSON payload from LLM
    mock_json = """{
        "diagnosis": "Degenerative disc disease",
        "requested_procedure": "Lumbar MRI",
        "symptom_duration_weeks": 12,
        "physiotherapy_weeks": 6,
        "medications_attempted": ["Ibuprofen", "Naproxen"],
        "previous_imaging": ["Lumbar X-Ray"],
        "relevant_conditions": ["Osteoarthritis"],
        "unknown_fields": []
    }"""
    mock_generate_response.return_value = mock_json
    
    notes = (
        "Patient presents with chronic lower back pain lasting for 12 weeks. "
        "Diagnosed with Degenerative disc disease and Osteoarthritis. "
        "Completed 6 weeks of physiotherapy. Attempted Ibuprofen and Naproxen with no relief. "
        "Lumbar X-ray completed. Requesting Lumbar MRI."
    )
    
    result = await clinical_extractor.extract_clinical_info(notes)
    assert isinstance(result, ClinicalExtraction)
    assert result.diagnosis == "Degenerative disc disease"
    assert result.requested_procedure == "Lumbar MRI"
    assert result.symptom_duration_weeks == 12
    assert result.physiotherapy_weeks == 6
    assert "Ibuprofen" in result.medications_attempted
    assert "Naproxen" in result.medications_attempted
    assert "Lumbar X-Ray" in result.previous_imaging
    assert "Osteoarthritis" in result.relevant_conditions
    assert len(result.unknown_fields) == 0

@pytest.mark.anyio
@patch("app.services.llm_client.generate_response")
async def test_extract_clinical_info_missing_values(mock_generate_response):
    # Simulated JSON with null/empty fields
    mock_json = """{
        "diagnosis": "Knee Pain",
        "requested_procedure": "Knee Arthroscopy",
        "symptom_duration_weeks": null,
        "physiotherapy_weeks": null,
        "medications_attempted": ["Meloxicam"],
        "previous_imaging": [],
        "relevant_conditions": [],
        "unknown_fields": ["symptom_duration_weeks", "physiotherapy_weeks", "previous_imaging"]
    }"""
    mock_generate_response.return_value = mock_json
    
    notes = "Patient reports severe knee pain. Attempted Meloxicam. Scheduled for Knee Arthroscopy."
    
    result = await clinical_extractor.extract_clinical_info(notes)
    assert isinstance(result, ClinicalExtraction)
    assert result.diagnosis == "Knee Pain"
    assert result.requested_procedure == "Knee Arthroscopy"
    assert result.symptom_duration_weeks is None
    assert result.physiotherapy_weeks is None
    assert result.medications_attempted == ["Meloxicam"]
    assert result.previous_imaging == []
    assert "symptom_duration_weeks" in result.unknown_fields

@pytest.mark.anyio
async def test_extract_clinical_info_empty_notes():
    result = await clinical_extractor.extract_clinical_info("")
    assert isinstance(result, ClinicalExtraction)
    assert result.diagnosis is None
    assert result.requested_procedure is None
    assert result.symptom_duration_weeks is None
    assert result.physiotherapy_weeks is None
    assert result.medications_attempted == []

@pytest.mark.anyio
@patch("app.services.llm_client.generate_response")
async def test_extract_clinical_info_api_error(mock_generate_response):
    # Simulate an authentication error propagated from client
    mock_generate_response.side_effect = llm_client.LLMAuthenticationError("Incorrect API key")
    
    with pytest.raises(llm_client.LLMAuthenticationError) as exc:
        await clinical_extractor.extract_clinical_info("Patient notes")
    assert "Incorrect API key" in str(exc.value)
