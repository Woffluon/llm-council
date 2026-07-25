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
    "z-ai/glm-5.2",
    "z-ai/glm-5.2",
    "z-ai/glm-5.2",
    "z-ai/glm-5.2",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "z-ai/glm-5.2"

# API endpoints
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NVIDIA_NIM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"

