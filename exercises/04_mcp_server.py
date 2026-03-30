"""
Exercise 04: MCP Server & Tool API
----------------------------------
- Learn about Model Context Protocol (MCP) and tool APIs
- Try calling the MCP tool endpoints directly

Instructions:
- Run the FastAPI server (see README)
- Use requests or curl to POST to /tools/order-status, /tools/inventory, /tools/escalate
- Edit this file to automate or experiment with tool API calls.
"""

import requests

BASE_URL = "http://localhost:8000"

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
