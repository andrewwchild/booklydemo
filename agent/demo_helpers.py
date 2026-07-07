"""Pretty-print helpers for notebook and live presentation demos."""

from __future__ import annotations

from typing import Any

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent


def print_turn(user_message: str, result: dict[str, Any], *, show_tools: bool = True) -> None:
    """Display one conversation turn with optional tool call details."""
    print(f"Customer: {user_message}\n")
    if show_tools and result.get("tool_calls"):
        for tc in result["tool_calls"]:
            print(f"  🔧 Tool: {tc['name']}")
            print(f"     Args:   {tc['arguments']}")
            print(f"     Result: {tc['result']}\n")
    print(f"Agent: {result['reply']}\n")
    print("—" * 60)


def run_demo_script(
    agent: BooklyAgent,
    memory: ConversationMemory,
    messages: list[str],
    *,
    show_tools: bool = True,
) -> None:
    """Run a scripted sequence of user messages (for notebook walkthrough)."""
    for msg in messages:
        result = agent.chat(memory, msg)
        print_turn(msg, result, show_tools=show_tools)


def new_session(agent: BooklyAgent) -> tuple[BooklyAgent, ConversationMemory]:
    """Start a fresh agent session."""
    return agent, ConversationMemory()
