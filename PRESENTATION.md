# Live Presentation Guide

Use this for your Decagon interview. You have **two surfaces** — pick based on room setup:

| Surface | Best when | Command |
|---------|-----------|---------|
| **Notebook** | Screen share in Zoom / walking through architecture | `jupyter notebook notebooks/bookly_demo.ipynb` |
| **Web UI** | In-person or you want a polished chat feel | `uvicorn app.main:app --port 8000` |

Both call the same `BooklyAgent` code path.

---

## Before the call (5 min checklist)

1. **Colab:** Push repo to GitHub, set `REPO_URL` in notebook Step 1, add `OPENAI_API_KEY` secret (optional)
2. **Local:** `cd ~/Projects/bookly-cs-agent && source .venv/bin/activate`
3. Optional but recommended: set `OPENAI_API_KEY` for natural language
4. **Restart kernel** (notebook) or refresh browser (web) so session state is clean
5. Have test data visible: ORD-1001 / alice@example.com, ORD-1003 / carol@example.com

---

## Suggested flow (~8–10 min total)

### 1. Thesis (30 sec — while showing Slide 1)

> "My thesis is grounded, clarify-first support. The agent never guesses order data — it asks, then uses tools."

### 2. Notebook or web demo (4–5 min)

Run these **in order** — each hits a different assignment requirement:

| Step | You type | What to call out |
|------|----------|------------------|
| A | "Where is my order?" | **Clarifying question** — no tool yet |
| B | "ORD-1001" | **Tool use** — `lookup_order`, real tracking data |
| C | "I want a refund" | **Multi-turn** begins — asks for reason |
| D | "damaged book" | Slot filling — asks for email |
| E | "alice@example.com" | **Action** — `initiate_refund` executes |
| F | "What's your return policy?" | Policy FAQ via `get_policy` |

**Pro tip:** Expand the tool call output in the notebook — interviewers love seeing args + results.

### 3. Architecture (2 min — Slide 2)

Point to notebook cells that show tools + system prompt, or open `agent/orchestrator.py`.

### 4. Key decisions + tradeoffs (2 min — Slides 3–4)

Lead with: tools over RAG for transactions, slot memory for multi-turn.

### 5. What you'd do differently (1 min — Slide 5)

Eval harness first, then human handoff.

---

## Handling live demo risks

| Risk | Fallback |
|------|----------|
| API key fails / rate limit | Mock mode works offline — say "I built a deterministic fallback for reliability" |
| Typo in order ID | Shows error handling — "No order found" is intentional |
| Awkward pause | Narrate: "It's asking for order ID before calling the tool — that's by design" |
| They ask a curveball | Type it live — the LLM path handles free-form; mock handles scripted flows |

---

## Quick reset between demos

**Notebook:** Run the "Reset session" cell.

**Web UI:** Refresh the page.

**CLI:** Restart the script.
