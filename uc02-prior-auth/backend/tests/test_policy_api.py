import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.models.policy import PolicyChunk
from app.models.criteria import PolicyCriteriaOutput, PolicyCriterion
from app.services.policy_retriever import RetrievalResult

def test_post_policy_retrieval_mock_anthem():
    with TestClient(app) as client:
        response = client.post(
            "/api/policies/retrieval",
            json={
                "diagnosis": "Chronic back pain",
                "requested_procedure": "Lumbar MRI scan",
                "cpt_code": "72148",
                "payer": "Anthem",
                "mock": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["policy_name"] == "Lumbar MRI Policy"
        assert len(data["criteria"]) == 1
        assert data["criteria"][0]["criterion_id"] == "C1"
        assert data["criteria"][0]["unit"] == "weeks"
        assert len(data["chunks"]) == 1
        assert data["chunks"][0]["source_name"] == "Anthem"

def test_post_policy_retrieval_mock_uhc():
    with TestClient(app) as client:
        response = client.post(
            "/api/policies/retrieval",
            json={
                "diagnosis": "Wrist pain",
                "requested_procedure": "Wrist surgery",
                "cpt_code": "25441",
                "payer": "Uhc",
                "mock": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "SUCCESS"
        assert data["policy_name"] == "Wrist Surgery Policy"
        assert len(data["criteria"]) == 1
        assert data["criteria"][0]["operator"] == "=="
        assert len(data["chunks"]) == 1
        assert data["chunks"][0]["source_name"] == "Uhc"

def test_post_policy_retrieval_unknown_payer():
    with TestClient(app) as client:
        response = client.post(
            "/api/policies/retrieval",
            json={
                "diagnosis": "Severe back pain",
                "requested_procedure": "Lumbar MRI scan",
                "cpt_code": "72148",
                "payer": "UnknownPayer",
                "mock": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "PAYER_UNKNOWN"
        assert len(data["criteria"]) == 0
        assert len(data["chunks"]) == 0

@pytest.mark.anyio
async def test_post_policy_retrieval_live_success():
    chunk = PolicyChunk(
        source_type="PAYER",
        source_name="Anthem",
        policy_name="Obesity Policy",
        source_file="obesity.pdf",
        page_number=2,
        section="Medical Necessity",
        text="Medically necessary surgical criteria guidelines.",
        chunk_index=5
    )
    
    mock_retrieval = RetrievalResult(status="SUCCESS", chunks=[(chunk, 0.85)])
    mock_criteria = PolicyCriteriaOutput(
        policy_name="Obesity Policy",
        criteria=[
            PolicyCriterion(
                criterion_id="C1",
                description="Guidelines met",
                required=True,
                source_page=2,
                source_section="Medical Necessity"
            )
        ]
    )

    with patch("app.api.policies.retrieve_relevant_policies", new_callable=AsyncMock) as mock_ret, \
         patch("app.api.policies.extract_policy_criteria", new_callable=AsyncMock) as mock_ext:
        
        mock_ret.return_value = mock_retrieval
        mock_ext.return_value = mock_criteria
        
        with TestClient(app) as client:
            response = client.post(
                "/api/policies/retrieval",
                json={
                    "diagnosis": "Morbid obesity",
                    "requested_procedure": "Bariatric surgery",
                    "cpt_code": "43770",
                    "payer": "Anthem",
                    "mock": False
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "SUCCESS"
            assert data["policy_name"] == "Obesity Policy"
            assert len(data["criteria"]) == 1
            assert data["criteria"][0]["criterion_id"] == "C1"
            assert len(data["chunks"]) == 1
            assert data["chunks"][0]["chunk_index"] == 5
