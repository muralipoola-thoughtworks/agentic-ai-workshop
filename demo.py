"""Run a simple demo flow without starting the API server."""

from __future__ import annotations

from modules.agents.agent import RetailAgent
from modules.rag.pipeline import RAGPipeline


def run_demo() -> None:
    """Run the RAG and agent demos with sample questions."""
    print("\n--- RAG Demo ---")
    rag = RAGPipeline()
    rag_result = rag.query("What happens if inventory is out of stock?")
    print("Answer:")
    print(rag_result.get("answer", ""))
    print("Sources:")
    for source in rag_result.get("sources", []):
        print(f"- {source}")

    print("\n--- Agent Demo ---")
    agent = RetailAgent()
    agent_result = agent.run("Where is my order ORD-1002 and should I escalate?")
    print("Answer:")
    print(agent_result.get("answer", ""))
    print("Steps:")
    for step in agent_result.get("steps", []):
        print(f"- Tool: {step.get('tool')}")
        print(f"  Input: {step.get('input')}")
        print(f"  Observation: {step.get('observation')}")


if __name__ == "__main__":
    run_demo()
