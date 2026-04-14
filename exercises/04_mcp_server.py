"""
Exercise 04: MCP Server & Tool API
----------------------------------
- Learn about Model Context Protocol (MCP) and tool APIs
- Try calling both the simple REST tool endpoints and the FastMCP server

Instructions:
- Run the FastAPI server (see README)
- Use requests or curl to POST to /tools/order-status, /tools/inventory, /tools/escalate
- Use FastMCP client to call tools at /mcp
- Edit this file to automate or experiment with tool API calls.
"""

import asyncio

import requests
from fastmcp import Client

BASE_URL = "http://localhost:8000"
MCP_URL = f"{BASE_URL}/mcp"

async def run_fastmcp_calls() -> None:
    async with Client(MCP_URL) as client:
        tools = await client.list_tools()
        print("FastMCP Tools:", tools)

        result = await client.call_tool("order_status", {"order_id": "ORD-1002"})
        print("FastMCP Order Status:", result)

        result = await client.call_tool("inventory", {"product_id": "SKU-BETA"})
        print("FastMCP Inventory:", result)

        result = await client.call_tool("escalate", {"order_id": "ORD-1002"})
        print("FastMCP Escalation:", result)


if __name__ == "__main__":
    # Example: Get order status
    resp = requests.post(f"{BASE_URL}/tools/order-status", json={"order_id": "ORD-1002"})
    print("Order Status:", resp.json())

    # Example: Check inventory
    resp = requests.post(f"{BASE_URL}/tools/inventory", json={"product_id": "SKU-BETA"})
    print("Inventory:", resp.json())

    # Example: Escalate issue
    resp = requests.post(f"{BASE_URL}/tools/escalate", json={"order_id": "ORD-1002"})
    print("Escalation:", resp.json())

    asyncio.run(run_fastmcp_calls())
