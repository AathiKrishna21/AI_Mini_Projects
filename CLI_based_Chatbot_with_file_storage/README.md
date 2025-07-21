# Chatbot with LangChain

This directory contains a simple command-line chatbot powered by [LangChain](https://python.langchain.com/) and OpenAI models. The chatbot supports conversation history using a local file.

## Features

- Chat with an LLM (local or remote OpenAI-compatible endpoint)
- Conversation history stored in `messages.json`
- Easy configuration via environment variables
- Supports switching between local and remote models

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd chat
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in this directory with the following variables:

```
MODEL_MODE=local         # or 'remote'
LLM_MODEL_NAME=gpt-3.5-turbo   # (for local mode)
LLM_BASE_URL=http://localhost:8000/v1  # (for local mode)
OPENAI_API_KEY=your-api-key    # (for remote mode)
```

- For **local mode**, set `MODEL_MODE=local` and provide `LLM_MODEL_NAME` and `LLM_BASE_URL`.
- For **remote mode**, set `MODEL_MODE=remote` and provide `OPENAI_API_KEY`.

### 4. Run the chatbot

```sh
python main.py
```

Type your messages at the prompt. Type `exit` or `quit` to end the session.

## Files

- `main.py` — Main chatbot source code
- `requirements.txt` — Python dependencies
- `messages.json` — Stores chat history (created automatically)
- `.env` — Environment variables (not included, create your own)
