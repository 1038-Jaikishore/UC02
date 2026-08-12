import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import openai
from app.main import app
from app.services import llm_client

client = TestClient(app)

def test_llm_config_retrieval(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-key")
    monkeypatch.setenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setenv("LLM_MODEL", "google/gemini-2.5-flash")
    
    config = llm_client.get_llm_config()
    assert config["provider"] == "openrouter"
    assert config["api_key"] == "sk-test-key"
    assert config["base_url"] == "https://openrouter.ai/api/v1"
    assert config["model"] == "google/gemini-2.5-flash"

def test_llm_client_missing_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(llm_client.LLMConfigurationError) as exc:
        llm_client.get_llm_client()
    assert "LLM_API_KEY is not set" in str(exc.value)

@pytest.mark.anyio
@patch("app.services.llm_client.AsyncOpenAI")
async def test_generate_response_success(mock_openai_class, monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-key")
    monkeypatch.setenv("LLM_MODEL", "google/gemini-2.5-flash")
    
    # Mocking the completions return payload
    mock_choice = MagicMock()
    mock_choice.message.content = "pong"
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
    mock_openai_class.return_value = mock_client
    
    messages = [{"role": "user", "content": "ping"}]
    res = await llm_client.generate_response(messages)
    assert res == "pong"
    
    # Verify calls
    mock_client.chat.completions.create.assert_called_once_with(
        model="google/gemini-2.5-flash",
        messages=messages,
        extra_headers={
            "HTTP-Referer": "https://github.com/1038-Jaikishore/UC02",
            "X-Title": "Prior Auth Triage Companion"
        },
        max_tokens=1000
    )

@pytest.mark.anyio
@patch("app.services.llm_client.AsyncOpenAI")
async def test_generate_response_auth_error(mock_openai_class, monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_API_KEY", "sk-invalid-key")
    monkeypatch.setenv("LLM_MODEL", "google/gemini-2.5-flash")
    
    # Mock authentication exception
    mock_client = MagicMock()
    # Create valid HTTPX response and request for OpenAI exception structure
    mock_request = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 401
    
    mock_client.chat.completions.create = AsyncMock(
        side_effect=openai.AuthenticationError(
            message="Incorrect API key provided",
            response=mock_response,
            body=None
        )
    )
    mock_openai_class.return_value = mock_client
    
    with pytest.raises(llm_client.LLMAuthenticationError) as exc:
        await llm_client.generate_response([{"role": "user", "content": "ping"}])
    assert "authentication failed" in str(exc.value)

@pytest.mark.anyio
@patch("app.services.llm_client.AsyncOpenAI")
async def test_generate_response_rate_limit(mock_openai_class, monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-key")
    monkeypatch.setenv("LLM_MODEL", "google/gemini-2.5-flash")
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 429
    
    mock_client.chat.completions.create = AsyncMock(
        side_effect=openai.RateLimitError(
            message="Rate limit reached",
            response=mock_response,
            body=None
        )
    )
    mock_openai_class.return_value = mock_client
    
    with pytest.raises(llm_client.LLMRateLimitError) as exc:
        await llm_client.generate_response([{"role": "user", "content": "ping"}])
    assert "rate limit exceeded" in str(exc.value)

@patch("app.services.llm_client.AsyncOpenAI")
def test_api_test_endpoint_success(mock_openai_class, monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-key")
    monkeypatch.setenv("LLM_MODEL", "google/gemini-2.5-flash")
    
    mock_choice = MagicMock()
    mock_choice.message.content = "pong"
    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
    mock_openai_class.return_value = mock_client
    
    response = client.get("/api/llm/test")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "connected"
    assert data["provider"] == "openrouter"
    assert data["model"] == "google/gemini-2.5-flash"
    assert data["response"] == "pong"

def test_api_test_endpoint_missing_key(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    response = client.get("/api/llm/test")
    assert response.status_code == 400
    assert "api_key is missing" in response.json()["detail"].lower()
