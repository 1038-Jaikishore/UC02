import pytest
import re
from fastapi.testclient import TestClient
from app.main import app
from app.database.mongodb import get_database

# Using conftest.py shared database mock

client = TestClient(app)

def test_list_patients_no_search():
    response = client.get("/api/patients")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["patient_id"] == "PAT001"
    assert data[1]["patient_id"] == "PAT002"

def test_list_patients_search_match():
    response = client.get("/api/patients?search=Jane")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Jane"

def test_list_patients_search_no_match():
    response = client.get("/api/patients?search=NonExistentName")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_get_patient_profile_success():
    response = client.get("/api/patients/PAT001")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "PAT001"
    assert data["demographics"]["first_name"] == "John"
    assert len(data["conditions"]) == 1

def test_get_patient_profile_not_found():
    response = client.get("/api/patients/PAT_INVALID")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
