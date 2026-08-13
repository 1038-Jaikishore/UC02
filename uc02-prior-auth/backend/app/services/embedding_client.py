import os
import logging
from typing import List
from openai import AsyncOpenAI, OpenAIError
from app.services.llm_client import LLMConfigurationError, LLMConnectionError, LLMAPIError

logger = logging.getLogger(__name__)

def get_embedding_config() -> dict:
    """Retrieves and checks embedding configuration parameters from environment variables."""
    provider = os.getenv("EMBEDDING_PROVIDER", "openrouter").lower().strip()
    api_key = os.getenv("EMBEDDING_API_KEY")
    base_url = os.getenv("EMBEDDING_BASE_URL")
    model = os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small")
    
    # Fallback to LLM key if embedding key is missing (for ease of dev setup)
    if not api_key:
        api_key = os.getenv("LLM_API_KEY")
        
    if not base_url:
        if provider == "openrouter":
            base_url = "https://openrouter.ai/api/v1"
        else:
            base_url = "https://api.openai.com/v1"
            
    return {
        "provider": provider,
        "api_key": api_key,
        "base_url": base_url,
        "model": model
    }

def get_embedding_client() -> AsyncOpenAI:
    """Instantiates and returns an AsyncOpenAI compatible client for embeddings."""
    config = get_embedding_config()
    
    if not config["api_key"]:
        raise LLMConfigurationError("EMBEDDING_API_KEY (or LLM_API_KEY) is not set in environment variables.")
        
    return AsyncOpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        timeout=30.0
    )

async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates vector embeddings for a list of input texts.
    Retries or maps exceptions cleanly.
    """
    if not texts:
        return []
        
    config = get_embedding_config()
    client = get_embedding_client()
    
    try:
        response = await client.embeddings.create(
            input=texts,
            model=config["model"]
        )
        # Extract embeddings sorted by index
        embeddings = [data.embedding for data in response.data]
        return embeddings
    except OpenAIError as oe:
        logger.error(f"OpenAI/OpenRouter embedding API error: {oe}")
        raise LLMAPIError(f"Embedding API failed: {str(oe)}")
    except Exception as e:
        logger.error(f"Embedding network or internal connection error: {e}")
        raise LLMConnectionError(f"Embedding connection failed: {str(e)}")
