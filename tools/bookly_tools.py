import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_orders() -> dict[str, Any]:
    with open(DATA_DIR / "mock_orders.json") as f:
        return json.load(f)


def _load_policies() -> dict[str, Any]:
    with open(DATA_DIR / "policies.json") as f:
        return json.load(f)


def lookup_order(order_id: str) -> dict[str, Any]:
    """Look up order status and shipping details by order ID."""
    orders = _load_orders()
    order_id = order_id.strip().upper()
    if order_id not in orders:
        return {
            "found": False,
            "order_id": order_id,
            "message": f"No order found with ID {order_id}. Please double-check the ID from your confirmation email.",
        }
    order = orders[order_id]
    return {"found": True, **order}


def initiate_refund(order_id: str, reason: str, customer_email: str) -> dict[str, Any]:
    """Start a return/refund request for an eligible order."""
    orders = _load_orders()
    order_id = order_id.strip().upper()
    if order_id not in orders:
        return {
            "success": False,
            "message": f"Order {order_id} not found. Cannot process refund.",
        }

    order = orders[order_id]
    if order.get("customer_email", "").lower() != customer_email.strip().lower():
        return {
            "success": False,
            "message": "Email does not match our records for this order. Please verify your account email.",
        }

    if not order.get("eligible_for_return", False):
        return {
            "success": False,
            "order_id": order_id,
            "message": f"Order {order_id} is not yet eligible for return (status: {order['status']}).",
        }

    refund_id = f"RFD-{order_id.replace('ORD-', '')}"
    return {
        "success": True,
        "refund_id": refund_id,
        "order_id": order_id,
        "reason": reason,
        "amount": order["total"],
        "message": (
            f"Return initiated for order {order_id}. Refund ID: {refund_id}. "
            f"A prepaid return label will be emailed to {customer_email} within 24 hours. "
            f"Refund of ${order['total']:.2f} will process within 5-7 business days after we receive the item."
        ),
    }


def get_policy(topic: str) -> dict[str, Any]:
    """Retrieve Bookly policy information for shipping, returns, or password reset."""
    policies = _load_policies()
    topic = topic.strip().lower()

    aliases = {
        "ship": "shipping",
        "shipping": "shipping",
        "delivery": "shipping",
        "return": "returns",
        "returns": "returns",
        "refund": "returns",
        "refunds": "returns",
        "password": "password_reset",
        "password_reset": "password_reset",
        "login": "password_reset",
        "account": "password_reset",
    }

    key = aliases.get(topic, topic)
    if key not in policies:
        available = ", ".join(sorted(set(aliases.values())))
        return {
            "found": False,
            "topic": topic,
            "message": f"Unknown policy topic '{topic}'. Available topics: {available}.",
        }

    return {"found": True, "topic": key, "policy": policies[key]}


def send_password_reset(email: str) -> dict[str, Any]:
    """Send a password reset link to the customer's email (mocked)."""
    email = email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        return {
            "success": False,
            "message": "Please provide a valid email address.",
        }

    return {
        "success": True,
        "email": email,
        "message": (
            f"Password reset link sent to {email}. "
            "Check your inbox (and spam folder). The link expires in 1 hour."
        ),
    }
