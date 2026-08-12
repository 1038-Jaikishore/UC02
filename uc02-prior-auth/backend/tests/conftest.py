import pytest
import copy
from app.main import app
from app.database.mongodb import get_database

class MockCursor:
    def __init__(self, data):
        self.data = data

    def sort(self, key, order=1):
        if key == "created_at":
            self.data.sort(key=lambda x: x.get("created_at", ""), reverse=(order == -1))
        else:
            self.data.sort(key=lambda x: x.get(key, ""))
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

    def find(self, query=None):
        if not query:
            return MockCursor(self.data)
        
        # Simple simulation of OR matching with regex for patient search
        filtered = []
        for p in self.data:
            or_match = False
            if "$or" in query:
                for sub_q in query["$or"]:
                    for key, search_dict in sub_q.items():
                        search_pattern = search_dict.get("$regex", "")
                        # search in root or nested demographics
                        if "." in key:
                            parts = key.split(".")
                            val = p.get(parts[0], {}).get(parts[1], "")
                        else:
                            val = p.get(key, "")
                        
                        if search_pattern.lower() in str(val).lower():
                            or_match = True
                if or_match:
                    filtered.append(p)
            else:
                # Direct match query
                direct_match = True
                for k, v in query.items():
                    if p.get(k) != v:
                        direct_match = False
                if direct_match:
                    filtered.append(p)
                    
        return MockCursor(filtered)

    async def find_one(self, filter):
        # Handles queries by id or patient_id
        for doc in self.data:
            match = True
            for k, v in filter.items():
                if doc.get(k) != v:
                    match = False
            if match:
                return doc
        return None

    async def update_one(self, filter, update):
        matched = 0
        for doc in self.data:
            match = True
            for k, v in filter.items():
                if doc.get(k) != v:
                    match = False
            if match:
                matched = 1
                if "$set" in update:
                    for uk, uv in update["$set"].items():
                        doc[uk] = uv
        
        class MockUpdateResult:
            def __init__(self, matched_count):
                self.matched_count = matched_count
        return MockUpdateResult(matched)

    async def replace_one(self, filter, replacement, upsert=False):
        matched = False
        for i, doc in enumerate(self.data):
            match = True
            for k, v in filter.items():
                if doc.get(k) != v:
                    match = False
            if match:
                self.data[i] = copy.deepcopy(replacement)
                matched = True
                break
        if not matched and upsert:
            self.data.append(copy.deepcopy(replacement))
        
        class MockReplaceResult:
            def __init__(self, matched_count):
                self.matched_count = matched_count
        return MockReplaceResult(1 if matched else 0)

# Mock Patient Data
MOCK_PATIENTS = [
    {
        "patient_id": "PAT001",
        "demographics": {
            "patient_id": "PAT001",
            "first_name": "John",
            "last_name": "Doe",
            "dob": "1980-05-15",
            "age": 46,
            "gender": "M",
            "insurance_plan": "Aetna HMO",
            "member_id": "MEM12345",
            "summary_card_text": "Patient: PAT001 | Age: 46 | Coverage: Aetna HMO"
        },
        "conditions": [{"diagnosis_code": "M17.11", "diagnosis_name": "Osteoarthritis"}],
        "medications": [],
        "procedures": [],
        "diagnostic_results": [],
        "vital_signs": [],
        "encounters": [],
        "clinical_assessments": [],
        "functional_status": [],
        "allergies": [],
        "surgeries": [],
        "medical_equipment": [],
        "referrals": [],
        "family_history": [],
        "social_history": [],
        "immunizations": []
    },
    {
        "patient_id": "PAT002",
        "demographics": {
            "patient_id": "PAT002",
            "first_name": "Jane",
            "last_name": "Smith",
            "dob": "1975-10-20",
            "age": 50,
            "gender": "F",
            "insurance_plan": "Cigna",
            "member_id": "MEM67890",
            "summary_card_text": "Patient: PAT002 | Age: 50 | Coverage: Cigna"
        },
        "conditions": [],
        "medications": [],
        "procedures": [],
        "diagnostic_results": [],
        "vital_signs": [],
        "encounters": [],
        "clinical_assessments": [],
        "functional_status": [],
        "allergies": [],
        "surgeries": [],
        "medical_equipment": [],
        "referrals": [],
        "family_history": [],
        "social_history": [],
        "immunizations": []
    }
]

class MockDB:
    def __init__(self):
        from app.api.authorizations import INITIAL_DOCS
        self.prior_authorizations = MockCollection(copy.deepcopy(INITIAL_DOCS))
        self.patients = MockCollection(copy.deepcopy(MOCK_PATIENTS))
        self.clinical_extractions = MockCollection([])

mock_db_instance = MockDB()

async def override_get_database():
    return mock_db_instance

@pytest.fixture(autouse=True)
def setup_dependency_override():
    app.dependency_overrides[get_database] = override_get_database
    yield
    # Keep overrides for simple TestClient usage
