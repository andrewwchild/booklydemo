"""Helpers for interactive chat sessions in notebooks and scripts."""

from __future__ import annotations

from typing import Any

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent


def print_turn(user_message: str, result: dict[str, Any], *, show_tools: bool = True) -> None:
    """Display one conversation turn with optional tool call details."""
    print(f"Customer: {user_message}\n")
    if show_tools and result.get("tool_calls"):
        for tc in result["tool_calls"]:
            print(f"  🔧 {tc['name']}")
            print(f"     Args:   {tc['arguments']}")
            print(f"     Result: {tc['result']}\n")
    print(f"Agent: {result['reply']}\n")
    print("—" * 60)


def run_conversation(
    agent: BooklyAgent,
    memory: ConversationMemory,
    messages: list[str],
    *,
    show_tools: bool = True,
) -> None:
    """Run a sequence of user messages through the agent."""
    for msg in messages:
        result = agent.chat(memory, msg)
        print_turn(msg, result, show_tools=show_tools)


def new_session(agent: BooklyAgent) -> tuple[BooklyAgent, ConversationMemory]:
    """Start a fresh conversation session."""
    return agent, ConversationMemory()
