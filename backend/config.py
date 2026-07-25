"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# NVIDIA NIM API key
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# Preset council models per provider
OPENROUTER_COUNCIL_MODELS = [
    "openai/gpt-4o",
    "google/gemini-2.5-pro",
    "anthropic/claude-3.5-sonnet",
    "z-ai/glm-5.2",
]
OPENROUTER_CHAIRMAN_MODEL = "google/gemini-2.5-pro"

NVIDIA_NIM_COUNCIL_MODELS = [
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "meta/llama-3.3-70b-instruct",
    "mistralai/mistral-large-2-instruct",
    "deepseek-ai/deepseek-r1",
]
NVIDIA_NIM_CHAIRMAN_MODEL = "meta/llama-3.3-70b-instruct"

# Default fallback council models
COUNCIL_MODELS = OPENROUTER_COUNCIL_MODELS
CHAIRMAN_MODEL = OPENROUTER_CHAIRMAN_MODEL

# API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NVIDIA_NIM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"

