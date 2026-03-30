"""Vector store and retriever helpers for the retail RAG demo."""

from __future__ import annotations

from typing import List

from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_vector_store(
    documents: List[Document],
    embeddings,
    store_type: str,
    persist_dir: str | None = None,
):
    """Chunk documents and build the requested vector store."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    if store_type == "faiss":
        return FAISS.from_documents(chunks, embeddings)

    if store_type == "chroma":
        return Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=persist_dir,
        )

    raise ValueError("VECTORSTORE_TYPE must be 'faiss' or 'chroma'.")


def build_retriever(vector_store, k: int = 4):
    """Create a retriever with a simple top-k search."""
    return vector_store.as_retriever(search_kwargs={"k": k})
