import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_authorizations():
    response = client.get("/api/authorizations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    # Check that initial objects have correct structure
    first_item = data[0]
    assert "id" in first_item
    assert "patient_id" in first_item
    assert "cpt_code" in first_item

def test_create_authorization_success():
    payload = {
        "patient_id": "PT-9999",
        "diagnosis": "Acute meniscus tear",
        "diagnosis_code": "S83.206A",
        "requested_procedure": "Knee arthroscopy",
        "cpt_code": "29881",
        "clinical_notes": "Patient reports severe locking and pain in right knee.",
        "priority": "Urgent"
    }
    response = client.post("/api/authorizations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"].startswith("PA-")
    assert data["patient_id"] == "PT-9999"
    assert data["status"] == "PENDING_REVIEW"
    assert data["priority"] == "Urgent"

def test_create_authorization_validation_error():
    payload = {
        "patient_id": "PT-9999",
        # Missing diagnosis and other required fields
        "cpt_code": "29881"
    }
    response = client.post("/api/authorizations", json=payload)
    assert response.status_code == 422  # Validation error

def test_get_authorization_detail_success():
    # Fetch list to get a valid ID
    list_response = client.get("/api/authorizations")
    valid_id = list_response.json()[0]["id"]

    response = client.get(f"/api/authorizations/{valid_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == valid_id

def test_get_authorization_detail_not_found():
    response = client.get("/api/authorizations/PA-INVALID-ID")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
