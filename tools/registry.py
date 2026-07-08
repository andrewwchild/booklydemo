from typing import Any, Callable

from tools.bookly_tools import (
    check_stock,
    escalate_to_human,
    get_policy,
    initiate_refund,
    lookup_order,
    research_books,
    send_password_reset,
    verify_customer_identity,
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
            "name": "verify_customer_identity",
            "description": (
                "Verify that the customer's email matches the order before processing a return. "
                "Always call this before initiate_refund once you have order_id and customer_email."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID to verify, e.g. ORD-1001",
                    },
                    "customer_email": {
                        "type": "string",
                        "description": "Email the customer says is on the order",
                    },
                },
                "required": ["order_id", "customer_email"],
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
            "name": "research_books",
            "description": (
                "Search and recommend books by subject, topic, or keyword. "
                "Use when a customer asks for book recommendations, wants to browse by topic "
                "(e.g. bitcoin, psychology, science fiction), or mentions a subject without a specific title."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Subject or topic to research, e.g. 'bitcoin', 'self-help', 'programming'",
                    }
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": (
                "Check if a book is in stock and how many copies are available. "
                "Use when a customer asks about availability, inventory, or whether "
                "a specific title can be ordered. Requires a book title."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book_title": {
                        "type": "string",
                        "description": "Title of the book to check, e.g. 'Fourth Wing'",
                    }
                },
                "required": ["book_title"],
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
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": (
                "Hand off the conversation to a human support specialist with a summary. "
                "Use when the customer asks to speak to a person, is frustrated, or the issue "
                "cannot be resolved with available tools."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "conversation_summary": {
                        "type": "string",
                        "description": "Brief summary of the conversation so far for the human agent",
                    },
                    "reason": {
                        "type": "string",
                        "description": "Why the customer is being escalated",
                    },
                },
                "required": ["conversation_summary", "reason"],
            },
        },
    },
]

TOOL_HANDLERS: dict[str, ToolHandler] = {
    "lookup_order": lookup_order,
    "verify_customer_identity": verify_customer_identity,
    "initiate_refund": initiate_refund,
    "get_policy": get_policy,
    "check_stock": check_stock,
    "research_books": research_books,
    "send_password_reset": send_password_reset,
    "escalate_to_human": escalate_to_human,
}


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return {"error": f"Unknown tool: {name}"}
    return handler(**arguments)
