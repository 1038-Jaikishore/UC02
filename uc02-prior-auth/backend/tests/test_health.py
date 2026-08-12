import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_health_check():
    # Use context manager so FastAPI startup/shutdown event handlers are run
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        # It should be healthy if MongoDB Atlas successfully connected
        assert data["status"] in ("healthy", "degraded")
        assert "environment" in data
        assert "mongodb_connected" in data
