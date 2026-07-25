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
from .logger import logger


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
        logger.error(f"[NVIDIA NIM] Missing NVIDIA_API_KEY in .env for model '{model}'")
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

    logger.info(f"[NVIDIA NIM] Requesting model '{actual_model}'...")

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                NVIDIA_NIM_API_URL,
                headers=headers,
                json=payload
            )
            if response.is_error:
                logger.error(f"[NVIDIA NIM] HTTP {response.status_code} Error for model '{actual_model}': {response.text}")
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']
            content = message.get('content') or ''
            logger.info(f"[NVIDIA NIM] Received response from model '{actual_model}' ({len(content)} chars)")

            return {
                'content': content,
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        logger.error(f"[NVIDIA NIM] Exception for model '{actual_model}': {e}")
        return None
