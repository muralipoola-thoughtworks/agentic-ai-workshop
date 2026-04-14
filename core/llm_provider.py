"""LLM provider wrapper to switch between OpenAI and Azure OpenAI."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI, ChatOpenAI

import config as cfg


@dataclass
class LLMProvider:
    """Factory for creating LangChain chat model instances."""

    provider: str | None = None

    def __post_init__(self) -> None:
        if self.provider is None:
            self.provider = cfg.MODEL_PROVIDER

    def get_llm(self):
        """Return a LangChain LLM based on the selected provider."""
        if self.provider == "openai":
            print(f"Using OpenAI: {cfg.OPENAI_MODEL}")
            return ChatOpenAI(
                model=cfg.OPENAI_MODEL,
                temperature=cfg.LLM_TEMPERATURE,
                max_tokens=cfg.LLM_MAX_TOKENS,
            )

        if self.provider == "azure":
            print(f"Using Azure OpenAI: {cfg.AZURE_OPENAI_DEPLOYMENT}")
            return AzureChatOpenAI(
                azure_deployment=cfg.AZURE_OPENAI_DEPLOYMENT,
                api_version=cfg.AZURE_OPENAI_API_VERSION,
                azure_endpoint=cfg.AZURE_OPENAI_ENDPOINT,
                temperature=cfg.LLM_TEMPERATURE,
                max_tokens=cfg.LLM_MAX_TOKENS,
            )

        if self.provider == "ollama":
            print(f"Using Ollama: {cfg.OLLAMA_MODEL}")
            return ChatOllama(model=cfg.OLLAMA_MODEL, base_url=cfg.OLLAMA_BASE_URL)

        if self.provider == "gemini":
            print(f"Using Gemini: {cfg.GEMINI_MODEL}")
            return ChatGoogleGenerativeAI(
                model=cfg.GEMINI_MODEL,
                temperature=cfg.LLM_TEMPERATURE,
                max_output_tokens=cfg.LLM_MAX_TOKENS,
            )

        raise ValueError(
            "MODEL_PROVIDER must be 'ollama', 'openai', 'azure', or 'gemini'. "
            f"Got: {self.provider}"
        )

    def switch_provider(self, provider: str) -> None:
        """Update the active provider at runtime."""
        self.provider = provider
