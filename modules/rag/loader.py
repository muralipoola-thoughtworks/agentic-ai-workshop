"""Document loading helpers for the retail RAG demo."""

from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_documents(data_dir: str) -> List[Document]:
    """Load text and PDF files from the provided directory."""
    base_path = Path(data_dir)
    if not base_path.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    documents: List[Document] = []
    for path in base_path.rglob("*"):
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            documents.extend(loader.load())
        else:
            loader = TextLoader(str(path), encoding="utf-8")
            documents.extend(loader.load())

    if not documents:
        raise ValueError(f"No supported documents found in: {data_dir}")

    return documents
