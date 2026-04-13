"""Agentic AI demo using LangChain tools and ReAct-style reasoning."""

from __future__ import annotations

from typing import Any, Dict, List

from langchain.agents import AgentType, initialize_agent
from langchain_core.tools import Tool

from config import VERBOSE_AGENT
from core.llm_provider import LLMProvider
from modules.agents.tools import build_tools
from modules.rag.pipeline import RAGPipeline


def _build_rag_tool() -> Tool:
    """Wrap the RAG pipeline as a LangChain tool."""
    rag = RAGPipeline()

    def _rag_query(question: str) -> str:
        result = rag.query(question)
        sources = ", ".join(result.get("sources", []))
        return f"Answer: {result.get('answer', '')}\nSources: {sources}"

    return Tool(
        name="retail_rag_qa",
        description=(
            "Answer retail fulfillment policy questions using internal FAQs. "
            "Use for inventory, delivery delays, or fulfillment rules."
        ),
        func=_rag_query,
    )


class RetailAgent:
    """Agent that can answer questions and use retail tools."""

    def __init__(self) -> None:
        self.llm = LLMProvider().get_llm()
        self.tools = build_tools() + [_build_rag_tool()]
        self.executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=VERBOSE_AGENT,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
        )

    def run(self, query: str) -> Dict[str, Any]:
        """Run the agent and return answer plus reasoning steps."""
        result = self.executor.invoke({"input": query})
        steps: List[Dict[str, str]] = []
        for action, observation in result.get("intermediate_steps", []):
            steps.append(
                {
                    "tool": action.tool,
                    "input": str(action.tool_input),
                    "observation": str(observation),
                }
            )

        return {
            "answer": result.get("output", ""),
            "steps": steps,
        }
