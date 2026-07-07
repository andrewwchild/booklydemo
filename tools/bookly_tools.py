import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_orders() -> dict[str, Any]:
    with open(DATA_DIR / "orders.json") as f:
        return json.load(f)


def _load_policies() -> dict[str, Any]:
    with open(DATA_DIR / "policies.json") as f:
        return json.load(f)


def _load_catalog() -> dict[str, Any]:
    with open(DATA_DIR / "catalog.json") as f:
        return json.load(f)


def _format_stock_message(book: dict[str, Any]) -> str:
    if book["in_stock"]:
        qty = book["quantity"]
        note = f" ({qty} copies left)" if qty <= 10 else ""
        return (
            f"Yes — **{book['title']}** by {book['author']} is in stock{note}. "
            f"${book['price']:.2f} ({book['format']})."
        )
    restock = book.get("restock_date")
    extra = book.get("note", "")
    msg = f"Sorry — **{book['title']}** is currently out of stock."
    if restock:
        msg += f" Expected restock: {restock}."
    if extra:
        msg += f" {extra}"
    return msg


def check_stock(book_title: str) -> dict[str, Any]:
    """Check whether a book is in stock and how many copies are available."""
    catalog = _load_catalog()
    query = book_title.strip().lower()
    if not query:
        return {
            "found": False,
            "message": "Please provide a book title to check availability.",
        }

    books = catalog["books"]
    exact = [b for b in books if b["title"].lower() == query]
    partial = [b for b in books if query in b["title"].lower() and b not in exact]

    if exact:
        matches = exact
    elif partial:
        matches = partial
    else:
        return {
            "found": False,
            "query": book_title,
            "message": (
                f"No book found matching '{book_title}'. "
                "Try the full title, e.g. 'Fourth Wing' or 'Project Hail Mary'."
            ),
        }

    if len(matches) > 1:
        return {
            "found": True,
            "multiple": True,
            "query": book_title,
            "matches": [
                {
                    "title": m["title"],
                    "author": m["author"],
                    "in_stock": m["in_stock"],
                    "quantity": m["quantity"],
                    "price": m["price"],
                }
                for m in matches
            ],
            "message": (
                f"I found {len(matches)} matches for '{book_title}': "
                + ", ".join(f"{m['title']} ({'in stock' if m['in_stock'] else 'out of stock'})" for m in matches)
                + ". Which one did you mean?"
            ),
        }

    book = matches[0]
    return {
        "found": True,
        "multiple": False,
        "sku": book["sku"],
        "title": book["title"],
        "author": book["author"],
        "in_stock": book["in_stock"],
        "quantity": book["quantity"],
        "price": book["price"],
        "format": book["format"],
        "restock_date": book.get("restock_date"),
        "message": _format_stock_message(book).replace("**", ""),
    }


def list_catalog_summary() -> dict[str, Any]:
    """Return catalog stats for UI display."""
    books = _load_catalog()["books"]
    in_stock = [b for b in books if b["in_stock"]]
    out_of_stock = [b for b in books if not b["in_stock"]]
    return {
        "total_titles": len(books),
        "in_stock": len(in_stock),
        "out_of_stock": len(out_of_stock),
        "out_of_stock_titles": [b["title"] for b in out_of_stock],
    }


def list_orders() -> dict[str, Any]:
    """Return a summary of all orders for display."""
    orders = _load_orders()
    rows = []
    for oid in sorted(orders):
        o = orders[oid]
        rows.append({
            "order_id": oid,
            "email": o["customer_email"],
            "status": o["status"],
            "items": len(o["items"]),
            "total": o["total"],
        })
    return {"count": len(rows), "orders": rows}


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


def verify_customer_identity(order_id: str, customer_email: str) -> dict[str, Any]:
    """Verify that the customer's email matches the order before processing a return."""
    orders = _load_orders()
    order_id = order_id.strip().upper()
    email = customer_email.strip().lower()

    if order_id not in orders:
        return {
            "verified": False,
            "order_id": order_id,
            "message": f"We couldn't find order {order_id}. Please check your order ID.",
        }

    order = orders[order_id]
    on_file = order.get("customer_email", "").lower()
    if on_file != email:
        return {
            "verified": False,
            "order_id": order_id,
            "message": (
                "The email you provided doesn't match our records for this order. "
                "Please verify the email used at checkout."
            ),
        }

    name = order.get("customer_name", "valued customer")
    return {
        "verified": True,
        "order_id": order_id,
        "customer_email": email,
        "customer_name": name,
        "message": f"Identity verified for order {order_id} ({name}).",
    }


def escalate_to_human(conversation_summary: str, reason: str) -> dict[str, Any]:
    """Create a support ticket and hand off to a human agent with conversation context."""
    import uuid

    ticket_id = f"ESC-{uuid.uuid4().hex[:6].upper()}"
    return {
        "success": True,
        "ticket_id": ticket_id,
        "reason": reason,
        "summary": conversation_summary,
        "estimated_wait": "5 minutes",
        "message": (
            f"I've escalated this to a Bookly specialist. Your ticket number is {ticket_id}. "
            f"An agent will join within 5 minutes with full context from our conversation."
        ),
    }


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
        detail = order.get("return_ineligible_reason") or f"status: {order['status']}"
        return {
            "success": False,
            "order_id": order_id,
            "message": f"Order {order_id} is not eligible for return ({detail}).",
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
    """Send a password reset link to the customer's email."""
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
