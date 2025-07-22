# Facts Search Project

This project uses LangChain and Chroma to store and search interesting facts from a text file using embeddings.

## Features

- Loads facts from `facts.txt`
- Splits facts into chunks for embedding
- Stores facts in a Chroma vector database
- Supports semantic search using a local or remote embedding model

## Setup

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Add your facts to `facts.txt` (one fact per line).

3. Run the main script:
    ```sh
    python main.py
    ```

## Configuration

- Embedding mode can be set to "local" or "remote" in `create_embeddings`.
- Local embedding endpoint and model can be customized in `LLMSCustomEmbeddings`.

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

## Files

- `main.py` — Main source code
- `facts.txt` — List of facts to index and search
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation
- `promt` — Contains prompt templates or instructions used for querying or interacting with the model.
- `redundent_file_filter` — Utility or script for filtering out redundant files or facts before indexing or searching.

## Example Usage

```sh
python main.py
```
You will see search results for the sample query in the script based on similarity search.

```sh
python prompt.py
```
You can get results through ai for the questions asked by user.
