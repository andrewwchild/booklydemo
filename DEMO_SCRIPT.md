# Bookly CS Agent — Live Demo Script

**Duration:** 12–15 minutes (demo + architecture)  
**UI:** Streamlit (`streamlit run app/streamlit_app.py`) or deployed at `booklydemo.streamlit.app`  
**Backup:** `python evals/run_evals.py` if live demo fails

---

## Before You Start

- [ ] Streamlit app open, fresh conversation
- [ ] Optional: terminal with `python evals/run_evals.py` ready
- [ ] Know these demo orders by heart:

| Order | Email | Status | Use for |
|-------|-------|--------|---------|
| ORD-1001 | alice@example.com | Shipped (UPS) | Happy-path order lookup |
| ORD-1006 | frank@example.com | Delayed | Empathy + real data |
| ORD-1003 | carol@example.com | Delivered | Successful refund |
| ORD-1004 | david@example.com | Delivered, window expired | Policy enforcement |
| ORD-1008 | — | Cancelled | Edge-case status |

| Book | Stock |
|------|-------|
| Fourth Wing | Out of stock |
| Atomic Habits | In stock |

---

## Part 1 — Opening (30 sec)

> "Bookly is a fictional online bookstore. Support gets the same five questions over and over: where's my order, can I return this, is this book in stock, what's your policy, and I can't log in.
>
> My thesis: **the best support agents don't guess — they clarify, then act on real data.** Wrong answers destroy trust faster than one extra question.
>
> I built a grounded, clarify-first agent with seven tools, identity verification before refunds, human handoff, and a 30-case eval harness. Let me show you."

---

## Part 2 — Live Demo (8 min)

### Flow 1: Clarify-first order lookup (~90 sec)

**Say:** "Customers rarely give you everything upfront. Watch what happens when I ask vaguely."

| You type | What to highlight |
|----------|-------------------|
| `Where is my order?` | Agent asks for order ID — does **not** hallucinate a status |
| `ORD-1001` | Calls `lookup_order` → real UPS tracking, delivery estimate |

**Talking point:** "The LLM handles natural language. Facts come from tools. If I only had an order ID, the rules engine would still route correctly — that's covered in evals."

---

### Flow 2: Delayed shipment — empathy + facts (~60 sec)

**Click:** New conversation

| You type | What to highlight |
|----------|-------------------|
| `ORD-1006` | Delayed status with carrier reason ("Weather delay in Memphis hub") |

**Say:** "This is grounded data, not generated fluff. In production this same tool hits the OMS. The agent can acknowledge frustration in natural language while the facts stay deterministic."

---

### Flow 3: Inventory check (~60 sec)

| You type | What to highlight |
|----------|-------------------|
| `Is Fourth Wing in stock?` | Out of stock + restock context |
| `Do you have Atomic Habits?` | In stock with price |

**Say:** "Stock levels change constantly — you can't RAG your way to '47 copies left.' This has to be a live API call."

---

### Flow 4: Policy FAQ (~45 sec)

| You type | What to highlight |
|----------|-------------------|
| `What's your return policy?` | `get_policy` → official 30-day window text |

**Say:** "Policies are a good RAG candidate in production, but for a prototype I kept them in a structured store so the agent always returns the canonical answer."

---

### Flow 5: Multi-turn refund + identity verification (~2 min) ⭐

**Click:** New conversation

**Say:** "Returns are the highest-risk flow — wrong refund, wrong person, wrong amount. I require three slots plus identity verification."

| Turn | You type | What to highlight |
|------|----------|-------------------|
| 1 | `I want a refund` | Asks for order ID |
| 2 | `ORD-1003` | Asks for reason — **does not** jump to order lookup |
| 3 | `The book arrived damaged` | Asks for email |
| 4 | `carol@example.com` | `verify_customer_identity` → then `initiate_refund` → refund ID + label |

**Say:** "Verify before act. Email must match the order record. Only then do we initiate the return. This is the pattern I'd use with real auth — OTP, account session, or email match."

---

### Flow 6: Edge case — policy enforcement (~60 sec)

**Click:** New conversation

| Turn | You type | What to highlight |
|------|----------|-------------------|
| 1–4 | Refund flow for ORD-1004, `david@example.com`, reason `wrong item` | Identity passes, but refund rejected — "Return window expired" |

**Say:** "The agent doesn't override business rules. Verification ≠ approval. Eligibility is checked in the refund tool against order metadata."

---

### Flow 7: Human handoff (~60 sec)

**Click:** New conversation

| You type | What to highlight |
|----------|-------------------|
| `Where is my order?` | Clarify |
| `ORD-1001` | Lookup succeeds |
| `I need to speak to a real person` | `escalate_to_human` → ticket ID + summary for specialist |

**Say:** "Every escalation includes conversation context so the human doesn't make the customer repeat themselves. In production this creates a Zendesk/Intercom ticket with the transcript."

---

### Flow 8 (optional, 30 sec): Password reset

| You type | What to highlight |
|----------|-------------------|
| `I can't log in` | Asks for email |
| `alice@example.com` | `send_password_reset` |

---

## Part 3 — Eval harness (90 sec)

**Run in terminal:**

```bash
python evals/run_evals.py
```

**Say:** "I don't trust vibe-based testing. Thirty golden cases cover clarify-first behavior, tool selection, multi-turn slot filling, identity checks, escalation, and edge cases. They run against the rules engine in under a second — CI-ready. When the LLM path changes, I'd add LLM-as-judge or snapshot tests for phrasing."

---

## Part 4 — Architecture walkthrough (3 min)

Use this diagram:

```
Customer → Streamlit UI → BooklyAgent (orchestrator)
                              ├── ConversationMemory (history + slots)
                              ├── System prompt (clarify-first rules)
                              └── OpenAI function calling
                                    └── Bookly tools (orders, catalog, policies)
```

**Walk layer by layer:**

1. **UI** — Streamlit for fast demo deploy; production would be chat widget + authenticated session
2. **Orchestrator** — Thin loop: LLM reasons → tool call → result → final reply. No LangChain.
3. **Memory** — Per-session slots (`order_id`, `reason`, `email`, `book_title`) so multi-turn flows don't re-ask
4. **Tools** — Seven functions with JSON schemas; swap JSON files for real APIs without touching the agent
5. **Dual engine** — LLM when API key present; rules-based fallback for offline demo and deterministic evals

---

## Part 5 — Close (30 sec)

> "To summarize: clarify before acting, tools for facts, verify before refunds, escalate with context, and test with golden cases. Next steps would be OMS/inventory integrations, authenticated sessions, confidence-based escalation, and production observability.
>
> Happy to go deeper on any decision."

---

## If Something Breaks

| Problem | Recovery |
|---------|----------|
| Streamlit down | `uvicorn app.main:app --port 8000` or CLI |
| LLM slow/errors | Works without API key — rules engine |
| Wrong reply | New conversation + use exact demo inputs above |
| Skeptic on quality | Run `python evals/run_evals.py` live |
