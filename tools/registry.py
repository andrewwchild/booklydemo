from typing import Any, Callable

from tools.bookly_tools import (
    get_policy,
    initiate_refund,
    lookup_order,
    send_password_reset,
)

ToolHandler = Callable[..., dict[str, Any]]

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": (
                "Look up order status, tracking, and delivery details. "
                "Use when a customer asks about order status or tracking. "
                "Requires a valid order ID (e.g. ORD-1001)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The customer's order ID, e.g. ORD-1001",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "initiate_refund",
            "description": (
                "Start a return/refund for an eligible order. "
                "Only call after you have order_id, reason, AND customer_email. "
                "Confirm details with the customer before calling."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID to refund, e.g. ORD-1001",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Customer's reason for the return",
                    },
                    "customer_email": {
                        "type": "string",
                        "description": "Email on the order for verification",
                    },
                },
                "required": ["order_id", "reason", "customer_email"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_policy",
            "description": (
                "Get official Bookly policy text for shipping, returns, or password reset. "
                "Use for general FAQ questions — do not invent policy details."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "enum": ["shipping", "returns", "password_reset"],
                        "description": "Policy area to retrieve",
                    }
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_password_reset",
            "description": (
                "Send a password reset email. Use when customer cannot log in "
                "and has provided their email address."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "Customer's account email",
                    }
                },
                "required": ["email"],
            },
        },
    },
]

TOOL_HANDLERS: dict[str, ToolHandler] = {
    "lookup_order": lookup_order,
    "initiate_refund": initiate_refund,
    "get_policy": get_policy,
    "send_password_reset": send_password_reset,
}


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return {"error": f"Unknown tool: {name}"}
    return handler(**arguments)
