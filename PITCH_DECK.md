# Bookly CS Agent — Pitch Deck (3–5 slides)

Copy each section into Google Slides, Keynote, or Pitch. Suggested visuals noted in *italics*.

---

## Slide 1: Thesis — Grounded, Clarify-First Support

**Headline:** The best CX agents don't guess — they clarify, then act on real data.

**Core belief:**
- Customers want **fast resolution**, but wrong answers (hallucinated tracking numbers, fake refund confirmations) destroy trust faster than one extra question.
- A great agent should feel human in *conversation* but machine-precise on *facts*.

**How Bookly reflects this:**
- Transactional queries (orders, refunds) always go through **tools**, never free-form generation
- Agent **asks one focused question at a time** when required info is missing
- Tool results are surfaced transparently in the UI (expandable "Tool: lookup_order" blocks)

*Visual: Simple diagram — User message → "Do I have order_id?" → Yes: Tool / No: Clarify*

**Speaker note:** "I'd rather add one turn than ship a confident lie."

---

## Slide 2: Architecture — How an inquiry flows

**Headline:** Thin orchestration layer + LLM reasoning + deterministic tools

```
┌─────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│ Chat UI │───▶│ FastAPI      │───▶│ BooklyAgent     │───▶│ Mock Bookly  │
│         │◀───│ /api/chat    │◀───│ (orchestrator)  │◀───│ APIs (JSON)  │
└─────────┘    └──────────────┘    └────────┬────────┘    └──────────────┘
                                            │
                         ┌──────────────────┼──────────────────┐
                         ▼                  ▼                  ▼
                   System prompt    ConversationMemory    OpenAI tools
                   (rules)          (messages + slots)    (4 functions)
```

**Components:**

| Component | Role |
|-----------|------|
| **Orchestrator** | Runs the LLM ↔ tool loop (up to 5 turns per user message) |
| **Tools** | `lookup_order`, `initiate_refund`, `get_policy`, `send_password_reset` |
| **Memory** | Per-session message history + extracted slots (`order_id`, `email`, `reason`) |
| **Prompts** | Clarify-first rules, demo context, tone guardrails |

*Visual: Flow chart for refund path — 3 clarifying turns → confirm → initiate_refund*

**Speaker note:** "I avoided all-in-one agent platforms on purpose — this is ~300 lines of orchestration I can explain line by line."

---

## Slide 3: Key Decision #1 — Tools over RAG for transactions

**Choice:** Order status and refunds use **function calling to mock APIs**, not vector search over docs.

**Trade-off:**
- ✅ Pro: Zero hallucination risk on order IDs, tracking numbers, refund amounts
- ✅ Pro: Actions (initiate_refund) are first-class, not "here's what you should do"
- ❌ Con: Each new action requires a new tool + integration (more eng work)

**Why worth it:** For ecommerce support, **wrong order data is a P0 incident**. RAG is great for policies; transactions need systems of record.

---

## Slide 4: Key Decision #2 — Clarify-first + slot memory

**Choice:** Hybrid approach — LLM handles natural language; `ConversationMemory` tracks required fields for multi-turn flows.

**Trade-off:**
- ✅ Pro: Refund flow reliably collects order_id → reason → email before acting
- ✅ Pro: Regex slot extraction catches structured inputs even if the LLM misses them
- ❌ Con: Not a full finite-state machine; edge cases may need tighter validation in production

**Why worth it:** Assignment requires multi-turn + clarifying questions. Pure end-to-end LLM often skips confirmation steps or calls tools with partial args.

**Demo moment:** "I want a refund" → agent asks for order ID → reason → email → *then* calls `initiate_refund`.

---

## Slide 5: What I'd do differently (production)

**First change:** **Eval harness + human handoff**

| Gap today | Production fix |
|-----------|----------------|
| No automated tests for tool selection | Golden-set evals: 50+ utterances → expected tool/intent |
| Mock data only | OMS + Stripe + Zendesk integrations |
| No escalation | Confidence threshold → summarize thread → route to human |
| Session memory in-process | Redis + customer auth for cross-device continuity |

**Why evals first:** Before scaling intents, you need to know if the agent *chooses the right action* — that's what enterprise buyers audit.

**Closing line:** "This prototype is intentionally narrow — two flows done well — because depth beats breadth in production CX."

---

## Appendix: Assignment checklist

- [x] Multi-turn interaction (refund slot filling)
- [x] Tool use (lookup_order, initiate_refund, get_policy, send_password_reset)
- [x] Clarifying question (order status without ID)
- [x] Interactive web demo + **Jupyter notebook for live presentation**
- [x] Direct API orchestration (no LangChain/CrewAI/etc.)
- [x] 3–5 slide pitch narrative
