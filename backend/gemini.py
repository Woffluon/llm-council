"""Google Gemini API client for making LLM requests via OpenAI-compatible endpoint."""

import httpx
from typing import List, Dict, Any, Optional
from .config import GEMINI_API_KEY, GEMINI_API_URL


async def query_gemini_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a model via Google Gemini API (OpenAI-compatible endpoint).

    Args:
        model: Gemini model identifier (e.g., "gemini-2.5-pro", "gemini-2.5-flash")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    if not GEMINI_API_KEY:
        print(f"Error querying Gemini model {model}: GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable is missing in .env.")
        return None

    # Strip optional "google/" or "gemini/" prefix if user included it in model string
    actual_model = model
    if actual_model.startswith("google/"):
        actual_model = actual_model[7:]
    elif actual_model.startswith("gemini/"):
        actual_model = actual_model[7:]

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": actual_model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                GEMINI_API_URL,
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
        print(f"Error querying Gemini model {model}: {e}")
        return None
