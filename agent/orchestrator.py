import json
import os
import re
from typing import Any

from openai import OpenAI

from agent.memory import ConversationMemory
from agent.prompts import SYSTEM_PROMPT
from agent.summary import build_conversation_summary
from tools.bookly_tools import _load_catalog
from tools.registry import TOOL_DEFINITIONS, execute_tool


class BooklyAgent:
    """Orchestrates LLM reasoning, tool calls, and conversation memory."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm_enabled = bool(self.api_key)
        self._client = OpenAI(api_key=self.api_key) if self.llm_enabled else None

    def chat(self, memory: ConversationMemory, user_message: str) -> dict[str, Any]:
        memory.add_user_message(user_message)
        self._extract_slots(memory, user_message)

        if self.llm_enabled:
            return self._llm_response(memory)

        return self._rules_based_response(memory, user_message)

    def _llm_response(self, memory: ConversationMemory) -> dict[str, Any]:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, *memory.to_openai_messages()]
        tool_calls_made: list[dict[str, Any]] = []

        for _ in range(5):
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            choice = response.choices[0]
            assistant_msg = choice.message

            if assistant_msg.tool_calls:
                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_msg.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments,
                                },
                            }
                            for tc in assistant_msg.tool_calls
                        ],
                    }
                )
                for tc in assistant_msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    result = execute_tool(tc.function.name, args)
                    tool_calls_made.append(
                        {"name": tc.function.name, "arguments": args, "result": result}
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(result),
                        }
                    )
                continue

            reply = assistant_msg.content or "I'm sorry, I couldn't generate a response."
            memory.add_assistant_message(reply)
            return {
                "reply": reply,
                "tool_calls": tool_calls_made,
                "engine": "ai",
            }

        reply = "I need a moment — could you rephrase your question?"
        memory.add_assistant_message(reply)
        return {"reply": reply, "tool_calls": tool_calls_made, "engine": "ai"}

    def _extract_slots(self, memory: ConversationMemory, text: str) -> None:
        order_match = re.search(r"ORD-\d{4}", text, re.IGNORECASE)
        if order_match:
            memory.set_slot("order_id", order_match.group().upper())

        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
        if email_match:
            memory.set_slot("customer_email", email_match.group().lower())

        lower = text.lower()
        refund_reasons = [
            "damaged",
            "wrong item",
            "wrong book",
            "not as described",
            "changed my mind",
            "duplicate",
            "late delivery",
        ]
        for reason in refund_reasons:
            if reason in lower:
                memory.set_slot("reason", reason)
                break

        self._extract_book_title(memory, text)
        if self._is_book_research_query(text):
            topic = self._extract_topic(text)
            if topic:
                memory.set_slot("topic", topic)

    def _extract_topic(self, text: str) -> str:
        lower = text.lower().strip()
        prefixes = (
            "books about ",
            "book about ",
            "books on ",
            "book on ",
            "recommend books on ",
            "recommendations for ",
            "recommend ",
            "looking for books on ",
            "looking for books about ",
        )
        for prefix in prefixes:
            if lower.startswith(prefix):
                return text[len(prefix) :].strip()
        return text.strip()

    def _is_book_research_query(self, text: str) -> bool:
        lower = text.lower().strip()
        triggers = [
            "books about",
            "book about",
            "books on",
            "book on",
            "recommend",
            "recommendation",
            "suggest",
            "looking for a book",
            "looking for books",
            "best books",
            "read about",
            "learn about",
            "help me find",
            "search for books",
            "what books",
            "any books",
        ]
        if any(t in lower for t in triggers):
            return True

        words = lower.split()
        if 1 <= len(words) <= 3:
            blocked = [
                "refund",
                "return",
                "order",
                "track",
                "tracking",
                "shipment",
                "delivery",
                "password",
                "login",
                "reset",
                "policy",
                "shipping",
                "hello",
                "hi",
                "hey",
                "help",
                "speak",
                "human",
                "stock",
            ]
            if re.search(r"ORD-\d{4}", text, re.IGNORECASE):
                return False
            if re.search(r"[\w.+-]+@[\w.-]+\.\w+", text):
                return False
            if any(b in lower for b in blocked):
                return False
            return True
        return False

    def _extract_book_title(self, memory: ConversationMemory, text: str) -> None:
        catalog = _load_catalog()["books"]
        lower = text.lower()
        # Prefer longest title match to avoid partial hits
        matches = [b for b in catalog if b["title"].lower() in lower]
        if matches:
            best = max(matches, key=lambda b: len(b["title"]))
            memory.set_slot("book_title", best["title"])

    def _detect_escalation(self, text: str) -> bool:
        lower = text.lower()
        triggers = [
            "speak to",
            "talk to",
            "real person",
            "human",
            "representative",
            "someone else",
            "manager",
            "supervisor",
            "escalate",
            "agent please",
        ]
        return any(t in lower for t in triggers)

    def _handle_escalation(
        self, memory: ConversationMemory, user_message: str, tool_calls: list[dict[str, Any]]
    ) -> str:
        summary = build_conversation_summary(memory)
        reason = user_message.strip() or "Customer requested a human agent"
        args = {"conversation_summary": summary, "reason": reason}
        result = execute_tool("escalate_to_human", args)
        tool_calls.append({"name": "escalate_to_human", "arguments": args, "result": result})
        memory.pending_intent = None
        memory.awaiting_slot = None
        return result["message"]

    def _detect_intent(self, text: str) -> str | None:
        lower = text.lower()
        if re.search(r"ORD-\d{4}", text, re.IGNORECASE):
            return "order_status"
        if any(w in lower for w in ["return policy", "shipping policy", "policy"]):
            return "policy"
        if any(w in lower for w in ["refund", "return", "send back"]):
            return "refund"
        if any(w in lower for w in ["in stock", "instock", "available", "availability", "inventory"]):
            return "stock"
        if any(w in lower for w in ["do you have", "do you carry", "do you sell"]):
            return "stock"
        if self._is_book_research_query(text):
            return "book_research"
        if any(w in lower for w in ["order", "tracking", "shipment", "delivery", "where"]):
            return "order_status"
        if any(w in lower for w in ["password", "login", "reset", "log in", "can't log"]):
            return "password_reset"
        if any(w in lower for w in ["shipping", "ship", "policy", "return policy"]):
            return "policy"
        if any(w in lower for w in ["hi", "hello", "hey"]):
            return "greeting"
        return None

    def _format_order_reply(self, result: dict[str, Any]) -> str:
        if not result.get("found"):
            return result["message"]
        if result["status"] == "processing":
            return (
                f"Order {result['order_id']} is still processing. "
                f"Estimated delivery: {result['estimated_delivery']}."
            )
        if result["status"] == "shipped":
            return (
                f"Order {result['order_id']} shipped via {result['carrier']} on "
                f"{result['shipped_date']}. Tracking: {result['tracking_number']}. "
                f"Estimated delivery: {result['estimated_delivery']}."
            )
        if result["status"] == "out_for_delivery":
            return (
                f"Order {result['order_id']} is out for delivery today via {result['carrier']}. "
                f"Tracking: {result['tracking_number']}."
            )
        if result["status"] == "delayed":
            reason = result.get("delay_reason", "carrier delay")
            return (
                f"Order {result['order_id']} is delayed — {reason}. "
                f"New estimated delivery: {result['estimated_delivery']}. "
                f"Tracking: {result['tracking_number']}."
            )
        if result["status"] == "cancelled":
            return (
                f"Order {result['order_id']} was cancelled on {result.get('cancelled_date', 'N/A')}. "
                f"Reason: {result.get('cancel_reason', 'N/A')}."
            )
        return (
            f"Order {result['order_id']} was delivered on {result.get('delivered_date', 'N/A')}. "
            f"Items: {', '.join(result['items'])}."
        )

    def _handle_order_status(
        self, memory: ConversationMemory, tool_calls: list[dict[str, Any]]
    ) -> str:
        if "order_id" not in memory.slots:
            memory.pending_intent = "order_status"
            memory.awaiting_slot = "order_id"
            return (
                "I can look that up for you. What's your order ID?"
            )

        args = {"order_id": memory.slots["order_id"]}
        result = execute_tool("lookup_order", args)
        tool_calls.append({"name": "lookup_order", "arguments": args, "result": result})
        memory.pending_intent = None
        memory.awaiting_slot = None
        return self._format_order_reply(result)

    def _handle_stock_check(
        self, memory: ConversationMemory, user_message: str, tool_calls: list[dict[str, Any]]
    ) -> str:
        if "book_title" not in memory.slots:
            memory.pending_intent = "stock"
            memory.awaiting_slot = "book_title"
            return (
                "I can check availability for you. Which book title are you looking for?"
            )

        args = {"book_title": memory.slots["book_title"]}
        result = execute_tool("check_stock", args)
        tool_calls.append({"name": "check_stock", "arguments": args, "result": result})
        memory.pending_intent = None
        memory.awaiting_slot = None
        return result["message"]

    def _handle_book_research(
        self, memory: ConversationMemory, user_message: str, tool_calls: list[dict[str, Any]]
    ) -> str:
        topic = memory.slots.get("topic") or self._extract_topic(user_message)
        if not topic:
            memory.pending_intent = "book_research"
            memory.awaiting_slot = "topic"
            return (
                "I'd love to help you find something to read. "
                "What subject or topic are you interested in? (e.g. bitcoin, psychology, fantasy)"
            )

        args = {"topic": topic}
        result = execute_tool("research_books", args)
        tool_calls.append({"name": "research_books", "arguments": args, "result": result})
        memory.pending_intent = None
        memory.awaiting_slot = None
        return result["message"]

    def _handle_refund(self, memory: ConversationMemory, tool_calls: list[dict[str, Any]]) -> str:
        missing = memory.missing_refund_slots()
        memory.pending_intent = "refund"

        if "order_id" in missing:
            memory.awaiting_slot = "order_id"
            return (
                "I'd be happy to help with your return. "
                "Could you share your order ID? (e.g. ORD-1001)"
            )
        if "reason" in missing:
            memory.awaiting_slot = "reason"
            return (
                f"Got it — order {memory.slots['order_id']}. "
                "What's the reason for your return? (e.g., damaged, wrong item, changed my mind)"
            )
        if "customer_email" in missing:
            memory.awaiting_slot = "customer_email"
            return (
                "Almost done. What email address is on the order? "
                "I need this to verify your account before processing the return."
            )

        args = {
            "order_id": memory.slots["order_id"],
            "customer_email": memory.slots["customer_email"],
        }
        verify_result = execute_tool("verify_customer_identity", args)
        tool_calls.append(
            {"name": "verify_customer_identity", "arguments": args, "result": verify_result}
        )
        if not verify_result.get("verified"):
            memory.pending_intent = None
            memory.awaiting_slot = None
            return verify_result["message"]

        refund_args = {
            "order_id": memory.slots["order_id"],
            "reason": memory.slots["reason"],
            "customer_email": memory.slots["customer_email"],
        }
        result = execute_tool("initiate_refund", refund_args)
        tool_calls.append({"name": "initiate_refund", "arguments": refund_args, "result": result})
        memory.pending_intent = None
        memory.awaiting_slot = None
        memory.slots.clear()
        return result["message"]

    def _rules_based_response(self, memory: ConversationMemory, user_message: str) -> dict[str, Any]:
        """Rules-based response path when the AI engine is unavailable."""
        lower = user_message.lower()
        tool_calls: list[dict[str, Any]] = []
        intent = self._detect_intent(user_message)

        if self._detect_escalation(user_message):
            reply = self._handle_escalation(memory, user_message, tool_calls)
            memory.add_assistant_message(reply)
            return {"reply": reply, "tool_calls": tool_calls, "engine": "rules"}

        if intent:
            if intent == "greeting":
                memory.pending_intent = None
            elif memory.awaiting_slot is None:
                memory.pending_intent = intent

        # Continue in-flight flows when user replies with a slot value
        if memory.pending_intent == "refund" or intent == "refund":
            reply = self._handle_refund(memory, tool_calls)
        elif memory.pending_intent == "order_status" or (
            memory.awaiting_slot == "order_id" and "order_id" in memory.slots
        ):
            reply = self._handle_order_status(memory, tool_calls)
        elif memory.pending_intent == "stock" or intent == "stock":
            reply = self._handle_stock_check(memory, user_message, tool_calls)
        elif memory.pending_intent == "book_research" or intent == "book_research":
            reply = self._handle_book_research(memory, user_message, tool_calls)
        elif memory.pending_intent == "password_reset" or intent == "password_reset":
            if "customer_email" not in memory.slots:
                memory.pending_intent = "password_reset"
                memory.awaiting_slot = "customer_email"
                reply = "I can send a password reset link. What email is on your Bookly account?"
            else:
                args = {"email": memory.slots["customer_email"]}
                result = execute_tool("send_password_reset", args)
                tool_calls.append({"name": "send_password_reset", "arguments": args, "result": result})
                memory.pending_intent = None
                memory.awaiting_slot = None
                reply = result["message"]
        elif intent == "order_status":
            reply = self._handle_order_status(memory, tool_calls)
        elif intent == "policy":
            topic = "returns" if "return" in lower else "shipping"
            args = {"topic": topic}
            result = execute_tool("get_policy", args)
            tool_calls.append({"name": "get_policy", "arguments": args, "result": result})
            policy = result["policy"]
            reply = " ".join(policy.values()) if isinstance(policy, dict) else str(policy)
        elif intent == "greeting":
            reply = (
                "Hello! I'm Bookly Support. I can assist with orders, returns, "
                "availability, book picks, shipping policies, or password resets. "
                "What can I help you with today?"
            )
        elif memory.awaiting_slot == "customer_email" and "customer_email" in memory.slots:
            args = {"email": memory.slots["customer_email"]}
            result = execute_tool("send_password_reset", args)
            tool_calls.append({"name": "send_password_reset", "arguments": args, "result": result})
            memory.pending_intent = None
            memory.awaiting_slot = None
            reply = result["message"]
        elif memory.awaiting_slot == "book_title" and "book_title" in memory.slots:
            reply = self._handle_stock_check(memory, user_message, tool_calls)
        elif memory.awaiting_slot == "topic" and "topic" in memory.slots:
            reply = self._handle_book_research(memory, user_message, tool_calls)
        elif memory.awaiting_slot and memory.awaiting_slot in memory.slots:
            if memory.pending_intent == "refund":
                reply = self._handle_refund(memory, tool_calls)
            elif memory.pending_intent == "order_status":
                reply = self._handle_order_status(memory, tool_calls)
            elif memory.pending_intent == "stock":
                reply = self._handle_stock_check(memory, user_message, tool_calls)
            elif memory.pending_intent == "book_research":
                reply = self._handle_book_research(memory, user_message, tool_calls)
            else:
                reply = (
                    "I want to make sure I help with the right thing. "
                    "Are you asking about an order, book recommendations, availability, a return/refund, "
                    "shipping policy, or account access?"
                )
        else:
            reply = (
                "I want to make sure I help with the right thing. "
                "Are you asking about an order, book recommendations, availability, a return/refund, "
                "shipping policy, or account access?"
            )

        memory.add_assistant_message(reply)
        return {"reply": reply, "tool_calls": tool_calls, "engine": "rules"}
