"""FastMCP tool server wiring for the workshop demo."""

from __future__ import annotations

from fastmcp import FastMCP

from modules.agents.tools import check_inventory, escalate_issue, get_order_status

mcp_server = FastMCP(
    name="Retail MCP",
    instructions="Tools for order status, inventory lookup, and escalation.",
)


@mcp_server.tool(name="order_status", description="Return order status details.")
def tool_order_status(order_id: str):
    """Return order status details."""
    return get_order_status(order_id)


@mcp_server.tool(name="inventory", description="Return inventory details.")
def tool_inventory(product_id: str):
    """Return inventory details."""
    return check_inventory(product_id)


@mcp_server.tool(name="escalate", description="Return escalation outcome for an order.")
def tool_escalate(order_id: str):
    """Return escalation outcome for an order."""
    return escalate_issue(order_id)
