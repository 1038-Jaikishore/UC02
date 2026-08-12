import pytest
import copy
from fastapi.testclient import TestClient
from app.main import app
from app.database.mongodb import get_database

# In-memory mock database classes to replace MongoDB operations
class MockCursor:
    def __init__(self, data):
        self.data = data

    def sort(self, key, order=-1):
        # simple sort by created_at
        self.data.sort(key=lambda x: x.get("created_at", ""), reverse=(order == -1))
        return self

    async def to_list(self, length):
        return self.data[:length]

class MockCollection:
    def __init__(self, initial_data):
        self.data = initial_data

    async def count_documents(self, filter):
        return len(self.data)

    async def insert_many(self, docs):
        for doc in docs:
            self.data.append(copy.deepcopy(doc))

    async def insert_one(self, doc):
        self.data.append(copy.deepcopy(doc))

    def find(self, filter=None):
        return MockCursor(self.data)

    async def find_one(self, filter):
        for doc in self.data:
            if all(doc.get(k) == v for k, v in filter.items()):
                return doc
        return None

class MockDB:
    def __init__(self):
        from app.api.authorizations import INITIAL_DOCS
        self.prior_authorizations = MockCollection(copy.deepcopy(INITIAL_DOCS))

mock_database_instance = MockDB()

async def override_get_database():
    return mock_database_instance

# Register dependency overrides
app.dependency_overrides[get_database] = override_get_database

client = TestClient(app)

def test_list_authorizations():
    response = client.get("/api/authorizations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    # Check structure
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
        "cpt_code": "29881"
    }
    response = client.post("/api/authorizations", json=payload)
    assert response.status_code == 422

def test_get_authorization_detail_success():
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
