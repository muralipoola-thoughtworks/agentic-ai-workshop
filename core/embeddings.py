"""Embedding provider wrapper for OpenAI and Azure OpenAI."""

from __future__ import annotations

from dataclasses import dataclass


from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

import config as cfg


@dataclass
class EmbeddingProvider:
    """Factory for creating embeddings clients."""

    provider: str | None = None

    def __post_init__(self) -> None:
        if self.provider is None:
            self.provider = cfg.EMBEDDING_PROVIDER

    def get_embeddings(self):
        """Return an embeddings client based on the selected provider."""
        if self.provider == "openai":
            return OpenAIEmbeddings(model=cfg.OPENAI_EMBEDDING_MODEL)

        if self.provider == "azure":
            return AzureOpenAIEmbeddings(
                azure_deployment=cfg.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
                api_version=cfg.AZURE_OPENAI_API_VERSION,
                azure_endpoint=cfg.AZURE_OPENAI_ENDPOINT,
            )

        if self.provider == "ollama":
            return OllamaEmbeddings(
                model=cfg.OLLAMA_EMBEDDING_MODEL,
                base_url=cfg.OLLAMA_BASE_URL
            )

        raise ValueError(
            "EMBEDDING_PROVIDER must be 'openai', 'azure', or 'ollama'. "
            f"Got: {self.provider}"
        )

    def switch_provider(self, provider: str) -> None:
        """Update the active provider at runtime."""
        self.provider = provider
