# LLM Council

![llmcouncil](header.jpg)

The idea of this repo is that instead of asking a question to a single LLM provider, you can group multiple models into your "LLM Council". This repository provides a simple, local web application that queries multiple LLMs, asks them to review and rank each other's responses anonymously, and synthesizes a final answer using a designated Chairman model.

The application supports **Google Gemini API**, **NVIDIA NIM API**, and **OpenRouter API** with complete configuration managed via `.env`.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all council LLMs individually, and responses are collected and displayed in tabs.
2. **Stage 2: Review**. Each model reviews and ranks the anonymized responses of all other models by accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman model synthesizes all responses and peer rankings into a comprehensive final answer.

## Features

- **Multi-Provider Support**: Built-in support for **Google Gemini API**, **NVIDIA NIM API**, and **OpenRouter API**.
- **100% Environment Configurable**: Provider selection, API keys, council models, and chairman models are all managed directly in `.env`.
- **Windows & Unix Launchers**: Easy one-click startup scripts (`start.bat` for Windows with error handling, `start.sh` for Linux/macOS).

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

### 2. Configure Environment (`.env`)

Copy `.env.example` to create your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` to set your desired provider, API key, and models:

```env
# Active Provider: openrouter | nvidia_nim | gemini
PROVIDER=gemini

# API Keys
OPENROUTER_API_KEY=sk-or-v1-...
NVIDIA_API_KEY=nvapi-...
GEMINI_API_KEY=AIzaSy...

# Council Models (comma-separated list of 4 models)
COUNCIL_MODELS=gemini-2.5-pro,gemini-2.5-flash,gemini-2.0-flash,gemini-1.5-pro

# Chairman Model (synthesizes final response)
CHAIRMAN_MODEL=gemini-2.5-pro
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

- **Backend:** FastAPI (Python 3.10+), async httpx, Google Gemini API, NVIDIA NIM API, OpenRouter API
- **Frontend:** React + Vite, react-markdown for rendering
- **Storage:** JSON files in `data/conversations/`
- **Package Management:** uv for Python, npm for JavaScript
