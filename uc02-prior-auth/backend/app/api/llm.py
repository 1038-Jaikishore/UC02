import time
from fastapi import APIRouter, HTTPException, status
from app.services import llm_client

router = APIRouter(prefix="/api/llm", tags=["llm"])

@router.get("/test")
async def test_llm_connection():
    """
    Performs a minimal test query to verify connection to the configured LLM provider.
    Propagates detailed configuration and provider errors if they occur.
    """
    config = llm_client.get_llm_config()
    
    # Check config validity first before connection attempt
    if not config["api_key"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="LLM_API_KEY is missing from environment variables."
        )
    if not config["model"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="LLM_MODEL is missing from environment variables."
        )
        
    start_time = time.time()
    try:
        messages = [{"role": "user", "content": "Respond with exactly the word 'pong'."}]
        response = await llm_client.generate_response(messages)
        latency = time.time() - start_time
        
        return {
            "status": "connected",
            "provider": config["provider"],
            "model": config["model"],
            "base_url": config["base_url"],
            "response": response.strip(),
            "latency_seconds": round(latency, 2)
        }
        
    except llm_client.LLMConfigurationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    except llm_client.LLMAuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        
    except llm_client.LLMRateLimitError as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))
        
    except llm_client.LLMTimeoutError as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e))
        
    except (llm_client.LLMConnectionError, llm_client.LLMAPIError) as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
        
    except llm_client.LLMException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
