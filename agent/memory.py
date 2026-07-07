from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConversationMemory:
    """Per-session state for multi-turn flows."""

    messages: list[dict[str, Any]] = field(default_factory=list)
    pending_intent: str | None = None
    awaiting_slot: str | None = None
    slots: dict[str, str] = field(default_factory=dict)

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_result(self, tool_call_id: str, name: str, result: dict[str, Any]) -> None:
        self.messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": name,
                "content": str(result),
            }
        )

    def set_slot(self, key: str, value: str) -> None:
        self.slots[key] = value

    def missing_refund_slots(self) -> list[str]:
        required = ["order_id", "reason", "customer_email"]
        return [s for s in required if s not in self.slots or not self.slots[s]]

    def to_openai_messages(self) -> list[dict[str, Any]]:
        return list(self.messages)
