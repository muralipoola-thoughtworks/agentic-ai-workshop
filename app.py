"""FastAPI application for the GenAI workshop demo."""

from __future__ import annotations

from fastapi import FastAPI

from models.schemas import (
    AgentQueryRequest,
    AgentQueryResponse,
    ExplainResponse,
    RAGQueryRequest,
    RAGQueryResponse,
)
from modules.agents.agent import RetailAgent
from modules.mcp.server import router as mcp_router
from modules.rag.pipeline import RAGPipeline

app = FastAPI(title="GenAI Workshop Demo", version="0.1.0")

app.include_router(mcp_router)

_rag_pipeline: RAGPipeline | None = None
_agent: RetailAgent | None = None


def _get_rag_pipeline() -> RAGPipeline:
    """Build or reuse the RAG pipeline."""
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
        _rag_pipeline.build()
    return _rag_pipeline


def _get_agent() -> RetailAgent:
    """Build or reuse the retail agent."""
    global _agent
    if _agent is None:
        _agent = RetailAgent()
    return _agent


@app.get("/explain", response_model=ExplainResponse)
def explain_concepts() -> ExplainResponse:
    """Return a concise explanation of core concepts."""
    explanation = (
        "LLM: A large language model trained to predict text. "
        "GenAI: Systems that create new content (text, images, code). "
        "Agent: An LLM that can decide to use tools to complete tasks. "
        "Agentic AI: A system where agents plan, act, and use tools in loops."
    )
    return ExplainResponse(explanation=explanation)


@app.post("/rag/query", response_model=RAGQueryResponse)
def rag_query(payload: RAGQueryRequest) -> RAGQueryResponse:
    """Run the retail RAG pipeline and return answer + sources."""
    pipeline = _get_rag_pipeline()
    result = pipeline.query(payload.query)
    return RAGQueryResponse(
        answer=result.get("answer", ""),
        sources=result.get("sources", []),
    )


@app.post("/agent/query", response_model=AgentQueryResponse)
def agent_query(payload: AgentQueryRequest) -> AgentQueryResponse:
    """Run the retail agent with tool usage and return reasoning steps."""
    agent = _get_agent()
    result = agent.run(payload.query)
    return AgentQueryResponse(
        answer=result.get("answer", ""),
        steps=result.get("steps", []),
    )
