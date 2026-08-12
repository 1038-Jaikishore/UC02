import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.models.extraction import ClinicalExtraction

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_mock_db():
    # Clear the global mock clinical_extractions data before each test
    from conftest import mock_db_instance
    mock_db_instance.clinical_extractions.data.clear()

def test_get_extraction_not_found():
    response = client.get("/api/authorizations/PA-NON-EXISTENT/extraction")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.anyio
@patch("app.services.clinical_extractor.extract_clinical_info")
async def test_get_extraction_trigger_dynamic(mock_extract):
    # Setup mock extractor return data
    mock_extraction_data = ClinicalExtraction(
        diagnosis="Osteoarthritis",
        requested_procedure="Total Knee Arthroplasty",
        symptom_duration_weeks=24,
        physiotherapy_weeks=12,
        medications_attempted=["Ibuprofen"],
        previous_imaging=["Knee X-Ray"],
        relevant_conditions=[],
        unknown_fields=[]
    )
    mock_extract.return_value = mock_extraction_data
    
    response = client.get("/api/authorizations/PA-4011/extraction")
    assert response.status_code == 200
    data = response.json()
    assert data["authorization_id"] == "PA-4011"
    assert data["structured_extraction"]["diagnosis"] == "Osteoarthritis"
    assert data["validation_status"] == "VALID"
    
    # Confirm it was saved to the DB
    from conftest import mock_db_instance
    db_records = mock_db_instance.clinical_extractions.data
    assert len(db_records) == 1
    assert db_records[0]["authorization_id"] == "PA-4011"

@pytest.mark.anyio
@patch("app.services.clinical_extractor.extract_clinical_info")
async def test_get_extraction_from_cache(mock_extract):
    # Pre-populate cache directly in mock DB
    from conftest import mock_db_instance
    mock_db_instance.clinical_extractions.data.append({
        "authorization_id": "PA-4011",
        "patient_id": "PT-1111",
        "structured_extraction": {
            "diagnosis": "Cached Osteoarthritis",
            "requested_procedure": "Total Knee Arthroplasty",
            "symptom_duration_weeks": 24,
            "physiotherapy_weeks": 12,
            "medications_attempted": ["Ibuprofen"],
            "previous_imaging": ["Knee X-Ray"],
            "relevant_conditions": [],
            "unknown_fields": []
        },
        "model": "google/gemini-2.5-flash",
        "timestamp": "2026-08-12T12:00:00Z",
        "extraction_version": "1.0.0",
        "validation_status": "VALID"
    })
    
    response = client.get("/api/authorizations/PA-4011/extraction")
    assert response.status_code == 200
    data = response.json()
    assert data["structured_extraction"]["diagnosis"] == "Cached Osteoarthritis"
    
    # Verify that the clinical_extractor was NOT invoked (loaded from database cache!)
    mock_extract.assert_not_called()

@pytest.mark.anyio
@patch("app.services.clinical_extractor.extract_clinical_info")
async def test_post_extraction_force_refresh(mock_extract):
    # Pre-populate cache directly in mock DB
    from conftest import mock_db_instance
    mock_db_instance.clinical_extractions.data.append({
        "authorization_id": "PA-4011",
        "patient_id": "PT-1111",
        "structured_extraction": {
            "diagnosis": "Cached Osteoarthritis",
            "requested_procedure": "Total Knee Arthroplasty",
            "symptom_duration_weeks": 24,
            "physiotherapy_weeks": 12,
            "medications_attempted": ["Ibuprofen"],
            "previous_imaging": ["Knee X-Ray"],
            "relevant_conditions": [],
            "unknown_fields": []
        },
        "model": "google/gemini-2.5-flash",
        "timestamp": "2026-08-12T12:00:00Z",
        "extraction_version": "1.0.0",
        "validation_status": "VALID"
    })
    
    # Setup new mock response to overwrite cache
    mock_extraction_data = ClinicalExtraction(
        diagnosis="Newly Refreshed Osteoarthritis",
        requested_procedure="Total Knee Arthroplasty",
        symptom_duration_weeks=24,
        physiotherapy_weeks=12,
        medications_attempted=["Ibuprofen"],
        previous_imaging=["Knee X-Ray"],
        relevant_conditions=[],
        unknown_fields=[]
    )
    mock_extract.return_value = mock_extraction_data
    
    # Force run extraction via POST
    response = client.post("/api/authorizations/PA-4011/extraction")
    assert response.status_code == 200
    data = response.json()
    assert data["structured_extraction"]["diagnosis"] == "Newly Refreshed Osteoarthritis"
    
    # Verify that the clinical_extractor WAS invoked to overwrite the cache
    mock_extract.assert_called_once()
    
    # Confirm it was updated in the DB
    from conftest import mock_db_instance
    db_records = mock_db_instance.clinical_extractions.data
    assert len(db_records) == 1
    assert db_records[0]["structured_extraction"]["diagnosis"] == "Newly Refreshed Osteoarthritis"
