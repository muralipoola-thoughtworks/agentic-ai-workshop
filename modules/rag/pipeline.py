"""End-to-end RAG pipeline for the retail fulfillment demo."""

from __future__ import annotations

from typing import Dict, List

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from config import CHROMA_PERSIST_DIR, RETAIL_DOCS_DIR, VECTORSTORE_TYPE
from core.embeddings import EmbeddingProvider
from core.llm_provider import LLMProvider
from modules.rag.loader import load_documents
from modules.rag.retriever import build_retriever, build_vector_store


class RAGPipeline:
    """Builds a retriever and runs QA with source citations."""

    def __init__(self, data_dir: str | None = None):
        self.data_dir = data_dir or RETAIL_DOCS_DIR
        self.vector_store = None
        self.retriever = None
        self.chain = None

    def build(self) -> None:
        """Load documents and build vector store + retriever."""
        print(f"[RAGPipeline] Loading documents from: {self.data_dir}")
        documents = load_documents(self.data_dir)
        print(f"[RAGPipeline] Loaded {len(documents)} documents.")

        print(f"[RAGPipeline] Creating embeddings using provider: {EmbeddingProvider().provider}")
        embeddings = EmbeddingProvider().get_embeddings()
        print(f"[RAGPipeline] Embedding client: {type(embeddings).__name__}")

        print(f"[RAGPipeline] Building vector store: {VECTORSTORE_TYPE}")
        self.vector_store = build_vector_store(
            documents,
            embeddings,
            VECTORSTORE_TYPE,
            CHROMA_PERSIST_DIR,
        )
        print(f"[RAGPipeline] Vector store built: {type(self.vector_store).__name__}")
        self.retriever = build_retriever(self.vector_store)
        print(f"[RAGPipeline] Retriever built: {type(self.retriever).__name__}")

        llm = LLMProvider().get_llm()
        print(f"[RAGPipeline] LLM client: {type(llm).__name__}")
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer using the provided context.",
                ),
                ("human", "Question: {input}\n\nContext:\n{context}"),
            ]
        )
        qa_chain = create_stuff_documents_chain(llm, prompt)
        self.chain = create_retrieval_chain(self.retriever, qa_chain)
        print(f"[RAGPipeline] Retrieval chain initialized.")

    def query(self, question: str) -> Dict[str, List[str] | str]:
        """Run a RAG query and return answer plus sources."""
        if not self.chain:
            print("[RAGPipeline] Chain not built yet. Building now...")
            self.build()

        print(f"[RAGPipeline] Running query: {question}")
        result = self.chain.invoke({"input": question})
        print(f"[RAGPipeline] Query complete. Raw result: {result}")
        sources = [
            doc.metadata.get("source", "unknown")
            for doc in result.get("context", [])
        ]

        print(f"[RAGPipeline] Sources found: {sources}")
        return {
            "answer": result.get("answer", ""),
            "sources": sources,
        }
