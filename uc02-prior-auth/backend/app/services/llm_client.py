import os
import logging
from openai import AsyncOpenAI
import openai

logger = logging.getLogger(__name__)

# Base and custom LLM exceptions
class LLMException(Exception):
    """Base exception class for all LLM client errors."""
    pass

class LLMConfigurationError(LLMException):
    """Raised when environment variables or configurations are missing/invalid."""
    pass

class LLMAuthenticationError(LLMException):
    """Raised when authentication with the provider fails."""
    pass

class LLMRateLimitError(LLMException):
    """Raised when the client is rate-limited by the provider."""
    pass

class LLMTimeoutError(LLMException):
    """Raised when the API request times out."""
    pass

class LLMConnectionError(LLMException):
    """Raised when network connection fails."""
    pass

class LLMAPIError(LLMException):
    """Raised for general provider errors."""
    pass


def get_llm_config() -> dict:
    """Retrieves and checks LLM configuration parameters from environment variables."""
    provider = os.getenv("LLM_PROVIDER", "openrouter").lower().strip()
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    
    # Default Base URLs if not specified
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


def get_llm_client() -> AsyncOpenAI:
    """
    Initializes and returns an AsyncOpenAI compatible client.
    Does not validate connectivity, only instantiates the client using environment keys.
    """
    config = get_llm_config()
    
    if not config["api_key"]:
        raise LLMConfigurationError("LLM_API_KEY is not set in environment variables.")
        
    return AsyncOpenAI(
        base_url=config["base_url"],
        api_key=config["api_key"],
        timeout=30.0  # Safe timeout limit
    )


async def generate_response(messages: list, response_format: str = None, max_tokens: int = 1000) -> str:
    """
    Generates a response from the configured LLM provider asynchronously.
    Translates library exceptions into structured custom exceptions.
    """
    config = get_llm_config()
    
    if not config["api_key"]:
        raise LLMConfigurationError("LLM_API_KEY is missing from environment variables.")
        
    if not config["model"]:
        raise LLMConfigurationError("LLM_MODEL is missing from environment variables.")
        
    client = get_llm_client()
    
    # Extra payload fields for OpenRouter if needed
    extra_headers = {}
    if config["provider"] == "openrouter":
        extra_headers = {
            "HTTP-Referer": "https://github.com/1038-Jaikishore/UC02",
            "X-Title": "Prior Auth Triage Companion"
        }
        
    try:
        completion_args = {
            "model": config["model"],
            "messages": messages,
            "extra_headers": extra_headers,
            "max_tokens": max_tokens
        }
        
        # OpenRouter/OpenAI structured JSON format support if requested
        if response_format == "json_object":
            completion_args["response_format"] = {"type": "json_object"}
            
        logger.info(f"Sending completion request to provider '{config['provider']}' using model '{config['model']}'")
        
        response = await client.chat.completions.create(**completion_args)
        
        if not response.choices or len(response.choices) == 0:
            raise LLMAPIError("No response choices returned by the LLM provider.")
            
        content = response.choices[0].message.content
        if content is None:
            raise LLMAPIError("LLM provider returned empty/null message content.")
            
        return content

    except openai.AuthenticationError as e:
        logger.error(f"LLM Authentication Failed: {e}")
        raise LLMAuthenticationError(f"LLM provider authentication failed: {e.message}")
        
    except openai.RateLimitError as e:
        logger.error(f"LLM Rate Limited: {e}")
        raise LLMRateLimitError(f"LLM provider rate limit exceeded: {e.message}")
        
    except openai.APITimeoutError as e:
        logger.error(f"LLM Timeout Error: {e}")
        raise LLMTimeoutError("LLM provider request timed out.")
        
    except openai.APIConnectionError as e:
        logger.error(f"LLM Connection Error: {e}")
        raise LLMConnectionError(f"LLM provider connection failed: {e.message}")
        
    except openai.APIError as e:
        logger.error(f"LLM API Error: {e}")
        raise LLMAPIError(f"LLM provider API error: {e.message}")
        
    except Exception as e:
        logger.error(f"Unexpected LLM Error: {e}")
        raise LLMException(f"An unexpected LLM error occurred: {str(e)}")
