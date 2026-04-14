"""Agentic AI demo using LangChain tools and ReAct-style reasoning."""

from __future__ import annotations

from typing import Any, Dict, List

from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
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
        prompt = PromptTemplate.from_template(
            """You are a helpful assistant that can use tools.

    Available tools:
    {tools}

    Rules:
    - Use this exact format for tool calls.
    - Action must be a single tool name from [{tool_names}] on its own line.
    - Action Input must be a JSON object on its own line.

    Example:
    Question: Where is my order ORD-1002?
    Thought: I should look up the order status.
    Action: get_order_status
    Action Input: {{"order_id": "ORD-1002"}}
    Observation: {{"order_id": "ORD-1002", "status": "delayed"}}
    Thought: I should escalate if the order is delayed.
    Action: escalate_issue
    Action Input: {{"order_id": "ORD-1002"}}
    Observation: {{"order_id": "ORD-1002", "escalated": "yes"}}
    Thought: I now know the final answer
    Final Answer: Your order is delayed, so I escalated it.

    Now answer the real question.

    Question: {input}
    Thought: you should always think about what to do
    Action: one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (repeat Thought/Action/Action Input/Observation as needed)
    Thought: I now know the final answer
    Final Answer: the final answer to the question

    {agent_scratchpad}
    """
        )
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=prompt)
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
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
