"""Pydantic schemas for API requests and responses."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ExplainResponse(BaseModel):
    """Explains key GenAI concepts for the workshop."""

    explanation: str


class RAGQueryRequest(BaseModel):
    """Request body for RAG queries."""

    query: str = Field(..., description="User question")


class RAGQueryResponse(BaseModel):
    """Response for RAG queries."""

    answer: str
    sources: List[str]


class AgentQueryRequest(BaseModel):
    """Request body for agent queries."""

    query: str = Field(..., description="User question")


class OrderStatusRequest(BaseModel):
    """Request body for order status tools."""

    order_id: str = Field(..., description="Customer order identifier")


class InventoryRequest(BaseModel):
    """Request body for inventory tools."""

    product_id: str = Field(..., description="Product identifier")


class EscalateRequest(BaseModel):
    """Request body for escalation tools."""

    order_id: str = Field(..., description="Customer order identifier")


class AgentStep(BaseModel):
    """Intermediate agent step for explainability."""

    tool: str
    input: str
    observation: str


class AgentQueryResponse(BaseModel):
    """Response for agent queries."""

    answer: str
    steps: List[AgentStep]
