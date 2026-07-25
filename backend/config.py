"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Active Provider: openrouter | nvidia_nim | gemini
PROVIDER = os.getenv("PROVIDER", "openrouter").lower().strip()

# API keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NVIDIA_NIM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

# Default presets per provider
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

GEMINI_COUNCIL_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]
GEMINI_CHAIRMAN_MODEL = "gemini-2.5-pro"

# Select default models by provider
if PROVIDER in ("nvidia_nim", "nvidia"):
    DEFAULT_COUNCIL = NVIDIA_NIM_COUNCIL_MODELS
    DEFAULT_CHAIRMAN = NVIDIA_NIM_CHAIRMAN_MODEL
elif PROVIDER in ("gemini", "google"):
    DEFAULT_COUNCIL = GEMINI_COUNCIL_MODELS
    DEFAULT_CHAIRMAN = GEMINI_CHAIRMAN_MODEL
else:
    DEFAULT_COUNCIL = OPENROUTER_COUNCIL_MODELS
    DEFAULT_CHAIRMAN = OPENROUTER_CHAIRMAN_MODEL

# Read custom models from .env if present
env_council = os.getenv("COUNCIL_MODELS")
if env_council and env_council.strip():
    COUNCIL_MODELS = [m.strip() for m in env_council.split(",") if m.strip()]
else:
    COUNCIL_MODELS = DEFAULT_COUNCIL

env_chairman = os.getenv("CHAIRMAN_MODEL")
if env_chairman and env_chairman.strip():
    CHAIRMAN_MODEL = env_chairman.strip()
else:
    CHAIRMAN_MODEL = DEFAULT_CHAIRMAN

# Data directory for conversation storage
DATA_DIR = "data/conversations"
