from __future__ import annotations
import requests
from langchain_core.tools import Tool
def get_weather(city: str) -> str:
    """Get weather for a given city using wttr.in."""
    try:
        url = f"https://wttr.in/{city}?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Failed to get weather: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def build_weather_tool():
    return [
        Tool(
            name="get_weather",
            description="Get the current weather for a given city (e.g., 'San Francisco').",
            func=get_weather,
        )
    ]

import json
from pathlib import Path
from typing import Any, Dict, List

from pydantic.v1 import BaseModel, Field
from langchain_core.tools import StructuredTool

from config import INVENTORY_DATA_PATH, ORDERS_DATA_PATH


def _coerce_id(value: Any, key: str) -> str:
    if isinstance(value, dict):
        inner = value.get(key)
        return str(inner) if inner is not None else str(value)

    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{"):
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError:
                return value
            if isinstance(parsed, dict) and key in parsed:
                return str(parsed[key])
        return value

    return str(value)


def _load_json(path: str) -> List[Dict[str, str]]:
    """Load a JSON list from disk."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")

    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


class OrderStatusInput(BaseModel):
    """Input for order status lookup."""

    order_id: str = Field(..., description="Customer order identifier")


class InventoryInput(BaseModel):
    """Input for inventory lookup."""

    product_id: str = Field(..., description="Product identifier")


class EscalationInput(BaseModel):
    """Input for escalation requests."""

    order_id: str = Field(..., description="Customer order identifier")


def get_order_status(order_id: str) -> Dict[str, str]:
    """Return order status and ETA for a given order."""
    order_id = _coerce_id(order_id, "order_id")
    orders = _load_json(ORDERS_DATA_PATH)
    for order in orders:
        if order.get("order_id") == order_id:
            return order

    return {
        "order_id": order_id,
        "status": "unknown",
        "eta": "unknown",
        "note": "Order ID not found",
    }


def check_inventory(product_id: str) -> Dict[str, str]:
    """Return inventory details for a product."""
    product_id = _coerce_id(product_id, "product_id")
    inventory = _load_json(INVENTORY_DATA_PATH)
    for item in inventory:
        if item.get("product_id") == product_id:
            return item

    return {
        "product_id": product_id,
        "available": "no",
        "stock_level": "0",
        "note": "Product ID not found",
    }


def escalate_issue(order_id: str) -> Dict[str, str]:
    """Simulate escalation for delayed orders."""
    order_id = _coerce_id(order_id, "order_id")
    order = get_order_status(order_id)
    if order.get("status") == "delayed":
        return {
            "order_id": order_id,
            "escalated": "yes",
            "message": "Escalation created with priority handling.",
        }

    return {
        "order_id": order_id,
        "escalated": "no",
        "message": "Escalation not required for current status.",
    }


def build_tools():
    """Return LangChain tools for the agent."""
    return [
        StructuredTool.from_function(
            func=get_order_status,
            name="get_order_status",
            description="Get order status and ETA by order_id.",
            args_schema=OrderStatusInput,
        ),
        StructuredTool.from_function(
            func=check_inventory,
            name="check_inventory",
            description="Check inventory by product_id.",
            args_schema=InventoryInput,
        ),
        StructuredTool.from_function(
            func=escalate_issue,
            name="escalate_issue",
            description="Escalate delayed orders by order_id.",
            args_schema=EscalationInput,
        ),
    ]
