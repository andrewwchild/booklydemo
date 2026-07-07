#!/usr/bin/env python3
"""Run golden-set evals against the Bookly support agent (rules engine)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agent.memory import ConversationMemory
from agent.orchestrator import BooklyAgent


def run_case(agent: BooklyAgent, case: dict) -> dict:
    memory = ConversationMemory()
    all_tools: list[str] = []
    last_reply = ""

    for turn in case["turns"]:
        result = agent.chat(memory, turn)
        last_reply = result["reply"]
        all_tools.extend(tc["name"] for tc in result.get("tool_calls", []))

    return {"tools": all_tools, "reply": last_reply}


def check_case(case: dict, result: dict) -> list[str]:
    errors: list[str] = []
    expected_tools = case.get("expect_tools", [])
    actual_tools = result["tools"]

    for tool in expected_tools:
        if tool not in actual_tools:
            errors.append(f"missing tool '{tool}' (got {actual_tools})")

    for phrase in case.get("expect_reply_contains", []):
        if phrase.lower() not in result["reply"].lower():
            errors.append(f"reply missing '{phrase}'")

    if case.get("expect_no_tools") and actual_tools:
        errors.append(f"expected no tools, got {actual_tools}")

    return errors


def main() -> int:
    golden_path = Path(__file__).parent / "golden_set.json"
    cases = json.loads(golden_path.read_text())["cases"]

    agent = BooklyAgent()
    if agent.llm_enabled:
        print("Note: running against rules engine (clear OPENAI_API_KEY for consistency)\n")

    # Force rules engine for deterministic evals
    agent.llm_enabled = False
    agent._client = None

    passed = 0
    failed = 0

    print(f"Running {len(cases)} eval cases...\n")
    print(f"{'ID':<30} {'STATUS':<8} DETAIL")
    print("-" * 70)

    for case in cases:
        result = run_case(agent, case)
        errors = check_case(case, result)
        if errors:
            failed += 1
            print(f"{case['id']:<30} {'FAIL':<8} {'; '.join(errors)}")
        else:
            passed += 1
            print(f"{case['id']:<30} {'PASS':<8}")

    print("-" * 70)
    print(f"Results: {passed} passed, {failed} failed, {len(cases)} total")
    pct = (passed / len(cases) * 100) if cases else 0
    print(f"Pass rate: {pct:.0f}%")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
