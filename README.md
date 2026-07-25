# LLM Council

![llmcouncil](header.jpg)

The idea of this repo is that instead of asking a question to a single LLM provider, you can group multiple models into your "LLM Council". This repository provides a simple, local web application that queries multiple LLMs, asks them to review and rank each other's responses anonymously, and synthesizes a final answer using a designated Chairman model.

The application supports both **OpenRouter API** and **NVIDIA NIM API** with dynamic provider selection directly from the user interface.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all council LLMs individually, and responses are collected and displayed in tabs.
2. **Stage 2: Review**. Each model reviews and ranks the anonymized responses of all other models by accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman model synthesizes all responses and peer rankings into a comprehensive final answer.

## Features

- **Multi-Provider Support**: Supports both **OpenRouter** and **NVIDIA NIM API** endpoints out of the box.
- **Dynamic Provider Switcher**: Select between OpenRouter and NVIDIA NIM providers per-conversation directly from the UI.
- **Model Customization UI**: Customize individual council member models (Stage 1 & 2) and the chairman model (Stage 3) dynamically per query directly in the interface.
- **Windows & Unix Launchers**: Easy one-click startup scripts (`start.bat` for Windows with error handling, `start.sh` for Linux/macOS).
- **Preset Council Configurations**: Curated default models for each provider (e.g. OpenAI, Gemini, Claude, GLM, Llama 3.3, Nemotron, DeepSeek R1).

## Setup

### 1. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for Python project management.

**Backend:**
```bash
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure API Keys

Copy `.env.example` to create your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and insert your API keys:

```env
# OpenRouter API Key (https://openrouter.ai/)
OPENROUTER_API_KEY=sk-or-v1-...

# NVIDIA NIM API Key (https://build.nvidia.com/)
NVIDIA_API_KEY=nvapi-...
```

### 3. Model Configuration

Edit `backend/config.py` to customize the models for each provider:

```python
# OpenRouter preset
OPENROUTER_COUNCIL_MODELS = [
    "openai/gpt-4o",
    "google/gemini-2.5-pro",
    "anthropic/claude-3.5-sonnet",
    "z-ai/glm-5.2",
]
OPENROUTER_CHAIRMAN_MODEL = "google/gemini-2.5-pro"

# NVIDIA NIM preset
NVIDIA_NIM_COUNCIL_MODELS = [
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "meta/llama-3.3-70b-instruct",
    "mistralai/mistral-large-2-instruct",
    "deepseek-ai/deepseek-r1",
]
NVIDIA_NIM_CHAIRMAN_MODEL = "meta/llama-3.3-70b-instruct"
```

## Running the Application

**On Windows:**
```cmd
start.bat
```

**On Linux / macOS:**
```bash
./start.sh
```

**Manual Execution:**

Terminal 1 (Backend):
```bash
uv run python -m backend.main
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## Tech Stack

- **Backend:** FastAPI (Python 3.10+), async httpx, OpenRouter API & NVIDIA NIM API
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
