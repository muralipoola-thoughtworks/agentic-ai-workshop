"""
Exercise 04: MCP Server & Tool API
----------------------------------
- Learn about Model Context Protocol (MCP) and tool APIs
- Build an agent that discovers and calls MCP tools

Instructions:
- Run the FastAPI server (see README)
- Ensure the FastAPI server is running (see README)
- Run this file to see the agent call MCP tools
- Edit this file to try other questions and tools
"""

import asyncio
from fastmcp import Client
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool

from core.llm_provider import LLMProvider

MCP_URL = "http://localhost:8000/mcp"


def _normalize_tool_input(raw_input):
    if isinstance(raw_input, dict):
        return raw_input
    if isinstance(raw_input, str):
        return {"input": raw_input}
    return {"input": str(raw_input)}


async def _call_mcp_tool(tool_name: str, args: dict) -> dict:
    async with Client(MCP_URL) as client:
        return await client.call_tool(tool_name, args)


def run_agent_in_process_mcp(query: str) -> dict:
    """Run an agent (create_agent) that uses MCP tools in-process."""
    llm = LLMProvider().get_llm()
    tools = asyncio.run(_build_mcp_tools())
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="You are a helpful assistant that can use MCP tools.",
        debug=False,
    )
    result = agent.invoke({"messages": [HumanMessage(content=query)]})
    messages = result.get("messages", [])
    answer = messages[-1].content if messages else ""
    steps = []

    for message in messages:
        message_type = type(message).__name__
        if message_type == "ToolMessage":
            steps.append(
                {
                    "tool": getattr(message, "name", ""),
                    "observation": getattr(message, "content", ""),
                }
            )

    return {
        "answer": answer,
        "steps": steps,
    }


async def _build_mcp_tools() -> list[Tool]:
    async with Client(MCP_URL) as client:
        raw_tools = await client.list_tools()

    tools = []
    for tool in raw_tools:
        tool_name = getattr(tool, "name", None) or str(tool)
        description = getattr(tool, "description", None) or "MCP tool"

        def _make_tool(name: str, desc: str) -> Tool:
            def _call_mcp(tool_input):
                args = _normalize_tool_input(tool_input)
                if "input" in args:
                    raw_value = args.get("input")
                    if name in {"order_status", "escalate"}:
                        args = {"order_id": raw_value}
                    elif name == "inventory":
                        args = {"product_id": raw_value}
                return asyncio.run(_call_mcp_tool(name, args))

            return Tool(
                name=name,
                description=desc,
                func=_call_mcp,
            )

        tools.append(_make_tool(tool_name, description))

    return tools


if __name__ == "__main__":
    print(run_agent_in_process_mcp("Check order status for ORD-1002"))
