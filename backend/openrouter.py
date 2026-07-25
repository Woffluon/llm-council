"""OpenRouter API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, OPENROUTER_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0,
    provider: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via OpenRouter API, NVIDIA NIM API, or Gemini API.

    Args:
        model: Model identifier
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds
        provider: Optional provider override ('openrouter', 'nvidia_nim', 'gemini')

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    from .config import PROVIDER as DEFAULT_PROVIDER, NVIDIA_NIM_COUNCIL_MODELS, NVIDIA_NIM_CHAIRMAN_MODEL, GEMINI_COUNCIL_MODELS, GEMINI_CHAIRMAN_MODEL

    active_provider = (provider or DEFAULT_PROVIDER).lower().strip()

    # Route 1: Gemini API
    is_gemini = (
        active_provider in ("gemini", "google")
        or model.startswith("gemini")
        or model in GEMINI_COUNCIL_MODELS
        or model == GEMINI_CHAIRMAN_MODEL
    )
    if is_gemini:
        from .gemini import query_gemini_model
        return await query_gemini_model(model, messages, timeout=timeout)

    # Route 2: NVIDIA NIM API
    is_nvidia = (
        active_provider in ("nvidia_nim", "nvidia")
        or model.startswith(("nim/", "nvidia/"))
        or model in NVIDIA_NIM_COUNCIL_MODELS
        or model == NVIDIA_NIM_CHAIRMAN_MODEL
    )
    if is_nvidia:
        from .nvidia_nim import query_nvidia_model
        return await query_nvidia_model(model, messages, timeout=timeout)

    # Route 3: OpenRouter API
    if not OPENROUTER_API_KEY:
        print(f"Error querying OpenRouter model {model}: OPENROUTER_API_KEY is missing or empty in .env.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]],
    provider: Optional[str] = None
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of model identifiers
        messages: List of message dicts to send to each model
        provider: Optional provider name ('openrouter' or 'nvidia_nim')

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages, provider=provider) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
