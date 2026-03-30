"""MCP-like tool server routes for learning purposes."""

from __future__ import annotations

from fastapi import APIRouter

from models.schemas import EscalateRequest, InventoryRequest, OrderStatusRequest
from modules.agents.tools import check_inventory, escalate_issue, get_order_status

router = APIRouter()


# These endpoints simulate a Model Context Protocol (MCP) tool server.
# Each route exposes a tool as a lightweight HTTP API that an agent can call.


@router.post("/tools/order-status")
def tool_order_status(payload: OrderStatusRequest):
    """Return order status details."""
    return get_order_status(payload.order_id)


@router.post("/tools/inventory")
def tool_inventory(payload: InventoryRequest):
    """Return inventory details."""
    return check_inventory(payload.product_id)


@router.post("/tools/escalate")
def tool_escalate(payload: EscalateRequest):
    """Return escalation outcome for an order."""
    return escalate_issue(payload.order_id)
