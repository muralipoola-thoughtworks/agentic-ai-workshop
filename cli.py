"""Lightweight CLI menu for the workshop demo."""

from __future__ import annotations

import config as cfg

from modules.agents.agent import RetailAgent
from modules.rag.pipeline import RAGPipeline


def _print_menu() -> None:
    print("\nGenAI Workshop CLI")
    print("1. Explain concepts")
    print("2. Run RAG demo")
    print("3. Run agent demo")
    print("4. Switch model provider")
    print("5. Exit")


def _explain() -> None:
    explanation = (
        "LLM: A large language model trained to predict text.\n"
        "GenAI: Systems that create new content (text, images, code).\n"
        "Agent: An LLM that can decide to use tools to complete tasks.\n"
        "Agentic AI: A system where agents plan, act, and use tools in loops."
    )
    print("\n" + explanation)


def _run_rag() -> None:
    question = input("\nEnter your RAG question: ").strip()
    if not question:
        print("No question provided.")
        return

    rag = RAGPipeline()
    result = rag.query(question)
    print("\nAnswer:")
    print(result.get("answer", ""))
    print("Sources:")
    for source in result.get("sources", []):
        print(f"- {source}")


def _run_agent() -> None:
    question = input("\nEnter your agent question: ").strip()
    if not question:
        print("No question provided.")
        return

    agent = RetailAgent()
    result = agent.run(question)
    print("\nAnswer:")
    print(result.get("answer", ""))
    print("\nSteps:")
    for step in result.get("steps", []):
        print(f"- Tool: {step.get('tool')}")
        print(f"  Input: {step.get('input')}")
        print(f"  Observation: {step.get('observation')}")


def _switch_provider() -> None:
    print("\nSelect model provider:")
    print("1. Ollama (local)")
    print("2. OpenAI")
    print("3. Azure OpenAI")
    print("4. Gemini")
    choice = input("\nSelect an option: ").strip()

    if choice == "1":
        cfg.MODEL_PROVIDER = "ollama"
        print("Switched to Ollama (local) for LLM. Embeddings unchanged.")
    elif choice == "2":
        cfg.MODEL_PROVIDER = "openai"
        cfg.EMBEDDING_PROVIDER = "openai"
        print("Switched to OpenAI for LLM and embeddings.")
    elif choice == "3":
        cfg.MODEL_PROVIDER = "azure"
        cfg.EMBEDDING_PROVIDER = "azure"
        print("Switched to Azure OpenAI for LLM and embeddings.")
    elif choice == "4":
        cfg.MODEL_PROVIDER = "gemini"
        print("Switched to Gemini for LLM. Embeddings unchanged.")
    else:
        print("Invalid choice. No changes made.")


def main() -> None:
    while True:
        _print_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            _explain()
        elif choice == "2":
            _run_rag()
        elif choice == "3":
            _run_agent()
        elif choice == "4":
            _switch_provider()
        elif choice == "5":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
