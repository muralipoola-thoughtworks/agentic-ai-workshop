"""
Exercise 02: RAG Introduction
----------------------------
- Learn what Retrieval Augmented Generation (RAG) is
- Run a basic RAG query using the pipeline

Instructions:
- Edit this file to try different questions and observe how RAG uses documents.
"""

from modules.rag.pipeline import RAGPipeline

if __name__ == "__main__":
    rag = RAGPipeline()
    question = "What happens if inventory is out of stock?"
    result = rag.query(question)
    print("Question:", question)
    print("Answer:", result.get("answer", ""))
    print("Sources:", result.get("sources", []))
