#!/usr/bin/env python3
"""CLI interface for Bookly customer support."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent

load_dotenv()


def main():
    agent = BooklyAgent()

    print("Bookly Support")
    print("Type 'quit' to exit.\n")
    print("Agent: Hi! I'm Bookly Support. How can I help?\n")

    memory = ConversationMemory()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        result = agent.chat(memory, user_input)
        for tc in result.get("tool_calls", []):
            print(f"  [{tc['name']}] {tc['result']}")
        print(f"Agent: {result['reply']}\n")


if __name__ == "__main__":
    main()
