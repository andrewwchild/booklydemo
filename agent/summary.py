from agent.memory import ConversationMemory


def build_conversation_summary(memory: ConversationMemory, *, max_turns: int = 12) -> str:
    """Format recent conversation turns for human agent handoff."""
    lines: list[str] = []
    for msg in memory.messages[-max_turns:]:
        role = "Customer" if msg["role"] == "user" else "Agent"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines) if lines else "No prior conversation."
