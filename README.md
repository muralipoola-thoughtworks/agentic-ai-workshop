# GenAI Workshop Demo (Retail Fulfillment)

A simple, modular demo app that explains LLMs, runs a retail RAG pipeline, and showcases an agent that uses tools.


## Setup Pre-Requisites

1. Install [uv](https://github.com/astral-sh/uv) (if not already installed):

```bash
# Option 1: Install uv globally (recommended)
curl -Ls https://astral.sh/uv/install.sh | sh
# or, with pip (not recommended for production):
# pip install uv
```

2. Create and activate a Python 3.11 virtual environment with uv:

```bash
uv venv --python=python3.11
source .venv/bin/activate
```

3. Install dependencies with uv:

```bash
uv pip install -r requirements.txt
```

4. Set your LLM credentials (Optional):

OpenAI:
```bash
export OPENAI_API_KEY="your-key"
```

Azure OpenAI:
```bash
export AZURE_OPENAI_API_KEY="your-key"
```

Gemini:
```bash
export GOOGLE_API_KEY="your-key"
```

Weather API:
```bash
export WEATHER_API_KEY="your-weather-api-key"
```

Update [config.py](config.py) to switch providers:
```python
MODEL_PROVIDER = "ollama"  # "openai", "azure", or "gemini"
```


## Ollama Setup (for Local LLM)

1. Install Ollama (macOS/Linux/Windows):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Start the Ollama service (if not already running):

```bash
ollama serve &
```


3. Pull the Mistral model (for LLM) and nomic-embed-text (for embeddings):

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

## Run the API

```bash
uvicorn app:app --reload
```

API is available at http://127.0.0.1:8000

## How to Run Workshop Exercises

To run any exercise in the `exercises/` folder, follow these steps:

1. **Always run from the project root directory** (the folder containing `app.py`, `core/`, etc.).
  - This avoids import errors like `ModuleNotFoundError: No module named 'core'`.

2. **Run an exercise script:**
  ```bash
  python exercises/01_llm_basics.py
  ```

  Or, using Python's module syntax:
  ```bash
  python -m exercises.01_llm_basics
  ```

3. **If you must run from a subfolder**, set the `PYTHONPATH` to the project root:
  ```bash
  PYTHONPATH=. python exercises/01_llm_basics.py
  ```

4. **Troubleshooting:**
  - If you see import errors, double-check you are running from the project root.
  - Ensure your virtual environment is activated and all dependencies are installed.
  - See [exercises/README.md](exercises/README.md) for more details and exercise descriptions.


## Demo Flow

1. Ask a RAG question:
```bash
curl -X POST http://127.0.0.1:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What happens if inventory is out of stock?"}'
```

2. Ask an agent question that uses tools:
```bash
curl -X POST http://127.0.0.1:8000/agent/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Where is my order ORD-1002 and should I escalate?"}'
```

3. Inspect tool steps in the response to see multi-step reasoning.

Or run the local demo script without starting the API:

```bash
python demo.py
```

You can also use the interactive CLI menu:

```bash
python cli.py
```

Use option 4 in the CLI menu to switch between Ollama (local), OpenAI, Azure OpenAI, and Gemini providers.

## MCP Simulation

The tool endpoints simulate a lightweight MCP server so an agent can call tools via HTTP:

- POST `/tools/order-status` (body: `{ "order_id": "ORD-1001" }`)
- POST `/tools/inventory` (body: `{ "product_id": "SKU-ALPHA" }`)
- POST `/tools/escalate` (body: `{ "order_id": "ORD-1002" }`)

## Endpoints

- GET `/explain` - Explain LLM vs GenAI vs Agent vs Agentic AI
- POST `/rag/query` - Retail RAG pipeline
- POST `/agent/query` - Agent with tools and reasoning steps
- POST `/tools/*` - MCP-like tool routes


## Architecture Overview

- `core/llm_provider.py` - Switch OpenAI/Azure/Ollama LLMs
- `core/embeddings.py` - Embedding provider wrapper (supports OpenAI, Azure, Ollama local embeddings via nomic-embed-text)
- `modules/rag/` - RAG pipeline (loader, vector store, retriever)
- `modules/agents/` - Agent and tools
- `modules/mcp/` - MCP-like tool server routes
- `models/schemas.py` - Pydantic request/response models

## Sample Data

- [data/orders.json](data/orders.json)
- [data/inventory.json](data/inventory.json)
- [data/retail_docs](data/retail_docs)

## Notes

- Keep the default models small for fast demos.
- All data is local and safe to modify.
- To use local embeddings, set `EMBEDDING_PROVIDER = "ollama"` in `config.py` and ensure `OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"` is set. The system will use Ollama's local embedding model for vector search (FAISS/Chroma).

## Workshop Exercises

Step-by-step exercises are in the [exercises/](exercises/) folder. See [exercises/README.md](exercises/README.md) for details and mapping to workshop topics.

> **Recommended Python Version:**
> Use Python 3.11 for all workshop exercises. 

