"""Streamlit chat UI for Bookly customer support."""

import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
import streamlit as st

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent

load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="Bookly Support",
    page_icon="📚",
    layout="centered",
)

try:
    if key := st.secrets.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = key
except Exception:
    pass

QUICK_PROMPTS = [
    "Where is my order?",
    "I want a refund",
    "Is Fourth Wing in stock?",
    "What's your return policy?",
]

GREETING = (
    "Hi! I'm Bookly Support. I can help with order status, returns, "
    "book availability, shipping policies, or password resets. How can I help you today?"
)


def _load_orders() -> list[dict[str, Any]]:
    path = ROOT / "data" / "orders.json"
    with open(path) as f:
        orders = json.load(f)
    return [
        {"order_id": oid, "email": o["customer_email"], "status": o["status"]}
        for oid, o in sorted(orders.items())
    ]


def _load_catalog_summary() -> dict[str, Any]:
    path = ROOT / "data" / "catalog.json"
    with open(path) as f:
        books = json.load(f)["books"]
    out = [b["title"] for b in books if not b["in_stock"]]
    return {
        "total_titles": len(books),
        "out_of_stock": len(out),
        "out_of_stock_titles": out,
    }


def init_session() -> None:
    if "agent" not in st.session_state:
        st.session_state.agent = BooklyAgent()
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": GREETING}]


def reset_chat() -> None:
    st.session_state.memory = ConversationMemory()
    st.session_state.messages = [{"role": "assistant", "content": GREETING}]


def handle_message(text: str) -> None:
    st.session_state.messages.append({"role": "user", "content": text})
    result = st.session_state.agent.chat(st.session_state.memory, text)
    st.session_state.messages.append(
        {"role": "assistant", "content": result["reply"]}
    )


init_session()

st.title("📚 Bookly Support")
st.caption("We're here to help with your orders and account.")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("New conversation", use_container_width=True):
        reset_chat()
        st.rerun()

st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown("**Common questions:**")
cols = st.columns(len(QUICK_PROMPTS))
for col, prompt in zip(cols, QUICK_PROMPTS):
    if col.button(prompt, use_container_width=True):
        handle_message(prompt)
        st.rerun()

if user_input := st.chat_input("How can we help?"):
    handle_message(user_input)
    st.rerun()

with st.sidebar:
    st.header("Policies")
    st.markdown(
        """
**Returns:** 30 days from delivery  
**Shipping:** Free over $25  
**Support hours:** 24/7
        """
    )
    catalog = _load_catalog_summary()
    st.header("Catalog")
    st.caption(f"{catalog['total_titles']} titles in our store")
    if catalog["out_of_stock"]:
        st.markdown(
            "**Currently unavailable:** "
            + ", ".join(catalog["out_of_stock_titles"][:4])
            + ("…" if len(catalog["out_of_stock_titles"]) > 4 else "")
        )
