#!/usr/bin/env python3
"""CLI demo for Bookly CS agent — no server required."""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent

load_dotenv()


def main():
    agent = BooklyAgent()
    memory = ConversationMemory()
    mode = "mock" if agent.use_mock else "live"

    print("Bookly Support CLI")
    print(f"Mode: {mode}")
    print("Type 'quit' to exit.\n")
    print("Agent: Hi! I'm Bookly Support. How can I help?\n")

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
            print(f"  [tool: {tc['name']}] {tc['result']}")
        print(f"Agent: {result['reply']}\n")


if __name__ == "__main__":
    main()
