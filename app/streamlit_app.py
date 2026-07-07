"""Streamlit chat UI for the Bookly customer support agent."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
import streamlit as st

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent
from tools.bookly_tools import list_catalog_summary, list_orders

load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="Bookly Support",
    page_icon="📚",
    layout="centered",
)

# Streamlit Cloud secrets (optional — falls back to mock mode)
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


def init_session() -> None:
    if "agent" not in st.session_state:
        st.session_state.agent = BooklyAgent()
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I'm Bookly Support. I can help with order status, returns, "
                    "shipping policies, or password resets. What can I help with today?"
                ),
            }
        ]


def reset_chat() -> None:
    st.session_state.memory = ConversationMemory()
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm Bookly Support. I can help with order status, returns, "
                "shipping policies, or password resets. What can I help with today?"
            ),
        }
    ]


def handle_message(text: str) -> None:
    st.session_state.messages.append({"role": "user", "content": text})
    result = st.session_state.agent.chat(st.session_state.memory, text)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["reply"],
            "tool_calls": result.get("tool_calls", []),
            "mode": result.get("mode"),
        }
    )


init_session()
agent = st.session_state.agent
mode_label = f"Live · {agent.model}" if not agent.use_mock else "Mock (no API key)"

st.title("📚 Bookly Support")
st.caption(f"AI Customer Service Agent — {mode_label}")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("New chat", use_container_width=True):
        reset_chat()
        st.rerun()

st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        for tc in msg.get("tool_calls", []):
            with st.expander(f"🔧 Tool: {tc['name']}", expanded=False):
                st.markdown("**Arguments**")
                st.json(tc["arguments"])
                st.markdown("**Result**")
                st.json(tc["result"])

st.markdown("**Try a demo scenario:**")
cols = st.columns(len(QUICK_PROMPTS))
for col, prompt in zip(cols, QUICK_PROMPTS):
    if col.button(prompt, use_container_width=True):
        handle_message(prompt)
        st.rerun()

if user_input := st.chat_input("Type your message…"):
    handle_message(user_input)
    st.rerun()

with st.sidebar:
    st.header("Demo data")
    st.caption(f"{list_orders()['count']} sample orders (ORD-1001 – ORD-1015)")
    rows = ["| Order | Email | Status |", "|-------|-------|--------|"]
    for o in list_orders()["orders"]:
        rows.append(f"| {o['order_id']} | {o['email']} | {o['status'].title()} |")
    st.markdown("\n".join(rows))
    with st.expander("Interesting scenarios"):
        st.markdown(
            """
- **ORD-1006** — delayed shipment (weather)
- **ORD-1007** — out for delivery today
- **ORD-1008** — cancelled order
- **ORD-1004** — return window expired
- **ORD-1010** — good refund demo with `jack@example.com`
            """
        )
    catalog = list_catalog_summary()
    st.header("Catalog")
    st.caption(f"{catalog['total_titles']} titles · {catalog['out_of_stock']} out of stock")
    st.markdown("**Out of stock:** " + ", ".join(catalog["out_of_stock_titles"][:5]) + ", …")
    st.header("Demo script")
    st.markdown(
        """
1. **Order status** → give `ORD-1001`
2. **Refund** → order ID, reason, email
3. **Policy** → return policy question
        """
    )
