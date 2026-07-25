"""NVIDIA NIM API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import NVIDIA_API_KEY, NVIDIA_NIM_API_URL


async def query_nvidia_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a model via NVIDIA NIM API.

    Args:
        model: NVIDIA model identifier (e.g., "meta/llama-3.3-70b-instruct" or "nvidia/llama-3.1-nemotron-70b-instruct")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    if not NVIDIA_API_KEY:
        print(f"Error querying NVIDIA model {model}: NVIDIA_API_KEY environment variable is missing.")
        return None

    # Strip optional "nim/" prefix if present
    actual_model = model[4:] if model.startswith("nim/") else model

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": actual_model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                NVIDIA_NIM_API_URL,
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
        print(f"Error querying NVIDIA NIM model {model}: {e}")
        return None
