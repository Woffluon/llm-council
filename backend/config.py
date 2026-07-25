"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# NVIDIA NIM API key
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# Council members - list of model identifiers (OpenRouter or NVIDIA NIM)
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "x-ai/grok-4",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-3-pro-preview"

# API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NVIDIA_NIM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"

