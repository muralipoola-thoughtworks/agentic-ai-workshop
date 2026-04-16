"""App-wide configuration values."""

# LLM provider selection
MODEL_PROVIDER = "ollama"  # "ollama", "openai", "azure", or "gemini"
# Ollama settings
OLLAMA_MODEL = "mistral"
OLLAMA_BASE_URL = "http://localhost:11434"  # Set to "http://localhost:11434" if needed

# Common generation settings
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 512

# OpenAI settings
OPENAI_MODEL = "gpt-4o-mini"

# Azure OpenAI settings
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"
AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE.openai.azure.com"

# Gemini settings
GEMINI_MODEL = "gemini-2.5-flash-lite"

# Embeddings settings
# EMBEDDING_PROVIDER can be "openai", "azure", or "ollama"
EMBEDDING_PROVIDER = "ollama"  # "openai", "azure", or "ollama"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
# Ollama embedding model (recommended: nomic-embed-text)
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"

# RAG settings
VECTORSTORE_TYPE = "faiss"  # "faiss" or "chroma"
CHROMA_PERSIST_DIR = "./data/chroma"
RETAIL_DOCS_DIR = "./data/retail_docs"

# Data paths
DATA_DIR = "./data"
ORDERS_DATA_PATH = "./data/orders.json"
INVENTORY_DATA_PATH = "./data/inventory.json"

# General settings
VERBOSE_AGENT = True
