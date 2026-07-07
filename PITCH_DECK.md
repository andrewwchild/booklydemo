# Bookly Support — Architecture Overview

## Slide 1: Thesis — Grounded, Clarify-First Support

**Headline:** The best CX agents don't guess — they clarify, then act on real data.

- Wrong answers destroy trust faster than one extra question
- Human in conversation, machine-precise on facts
- Transactional queries always use tools — never free-form generation
- One focused clarifying question at a time when info is missing

---

## Slide 2: Architecture

**Headline:** Thin orchestration + LLM reasoning + service integrations

```
Customer → Chat UI → BooklyAgent (orchestrator)
                        ├── ConversationMemory (slots + history)
                        ├── System prompt (clarify-first rules)
                        └── OpenAI function calling
                              └── Bookly APIs (orders, catalog, policies)
```

| Component | Role |
|-----------|------|
| **Orchestrator** | Runs the LLM ↔ tool loop |
| **Tools** | lookup_order · initiate_refund · check_stock · get_policy · send_password_reset |
| **Memory** | Per-session history + extracted slots |
| **Prompts** | Clarify-first rules and tone guardrails |

---

## Slide 3: Key Decision — Tools over RAG for transactions

**Choice:** Order status, refunds, and inventory use function calling to Bookly APIs.

- Zero hallucination risk on order IDs, tracking, stock levels
- Actions (initiate_refund) are first-class operations
- Trade-off: each new capability requires a new tool integration

---

## Slide 4: Key Decision — Clarify-first + slot memory

**Choice:** LLM handles natural language; ConversationMemory tracks required fields.

- Refund flow collects order_id → reason → email before acting
- Regex slot extraction supplements the LLM
- Trade-off: production would add tighter validation and auth

---

## Slide 5: Production Roadmap

| Today | Next |
|-------|------|
| JSON data stores | OMS + inventory + CRM integrations |
| No automated evals | Golden-set intent and tool-selection tests |
| No escalation | Confidence threshold → human handoff |
| In-process sessions | Redis + authenticated customer sessions |

**Principle:** Depth beats breadth — nail core flows before scaling intents.
