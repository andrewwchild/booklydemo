"""Streamlit chat UI for Bookly customer support."""

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
from app.decagon_style import DECAGON_CSS, render_shell_header
from data.loader import load_catalog

load_dotenv(ROOT / ".env")

st.set_page_config(
    page_title="Bookly Support",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    if key := st.secrets.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = key
except Exception:
    pass

QUICK_PROMPTS = [
    "Where is my order?",
    "Books about bitcoin",
    "I want a refund",
    "Is Fourth Wing in stock?",
    "What's your return policy?",
    "I need to speak to a real person",
]

GREETING = (
    "Hello! I'm Bookly Support. I can assist with orders, returns, "
    "availability, book picks, shipping policies, or password resets. "
    "What can I help you with today?"
)


def _catalog_count() -> int:
    return len(load_catalog()["books"])


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
    cleaned = text.strip()
    if not cleaned:
        return
    st.session_state.messages.append({"role": "user", "content": cleaned})
    result = st.session_state.agent.chat(st.session_state.memory, cleaned)
    st.session_state.messages.append(
        {"role": "assistant", "content": result["reply"]}
    )


init_session()

st.markdown(f"<style>{DECAGON_CSS}</style>", unsafe_allow_html=True)
st.markdown(
    render_shell_header(catalog_count=_catalog_count()),
    unsafe_allow_html=True,
)

_, reset_col, _ = st.columns([5, 1.4, 5])
with reset_col:
    st.markdown('<div class="bookly-reset">', unsafe_allow_html=True)
    if st.button("New chat", use_container_width=True):
        reset_chat()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="bookly-composer-label">Message Bookly</div>', unsafe_allow_html=True)

with st.form("bookly_composer", clear_on_submit=True, border=False):
    user_input = st.text_area(
        "message",
        placeholder="Type a question about orders, books, returns, or policies…",
        label_visibility="collapsed",
        height=88,
    )
    send_col, _ = st.columns([1.2, 4])
    with send_col:
        submitted = st.form_submit_button("Send", use_container_width=True)

st.markdown(
    '<p class="bookly-composer-hint">Hit Send, or pick a suggestion below.</p>',
    unsafe_allow_html=True,
)

if submitted and user_input:
    handle_message(user_input)
    st.rerun()

st.markdown('<div class="section-label">Chat history</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown('<div class="section-label">Quick suggestions</div>', unsafe_allow_html=True)
cols = st.columns(len(QUICK_PROMPTS))
for col, prompt in zip(cols, QUICK_PROMPTS):
    if col.button(prompt, use_container_width=True):
        handle_message(prompt)
        st.rerun()
