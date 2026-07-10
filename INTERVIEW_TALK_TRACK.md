# Bookly Interview Deck — Talk Track

Companion script for `Bookly_Interview_Deck.pptx`. Same text is embedded as speaker
notes on each slide — this doc is for rehearsing without opening presenter view.

Structured around the four questions a review panel actually asks:
1. **Thesis** — core belief, and how the build reflects it
2. **Architecture** — how one inquiry flows through the system
3. **Key decisions** — 2–3 choices that mattered most, with trade-offs
4. **What I'd change** — the first thing, with more time or in production

**Target length:** ~8–10 minutes for the full deck, ~90 seconds per slide.

---

## Slide 1 — Title

> "Thanks for having me — I want to walk through this the way you'd actually want to hear it: what I believe, how the system reflects that belief, the two or three decisions that mattered most, and what I'd change next. Then I'm happy to go anywhere you want to dig in."

---

## Slide 2 — The Thesis

**On slide:** *Never guess. Always check.*

> "My core belief is that a support agent earns trust one verified fact at a time, and loses it instantly the moment it states something wrong with confidence. So I built Bookly's agent around one rule that governs everything else: never guess, always check.
>
> Concretely, that means two things. First, if the agent doesn't have enough information to act — say, no order number — it asks one clear question instead of assuming. Second, once it does have enough information, the actual answer always comes from a real system — the order database, the catalog, the policy doc — never generated from the model's own memory.
>
> You'll see this rule show up three separate times today: in how the agent clarifies before acting, in how it fetches facts instead of inventing them, and in how it verifies identity before anything risky, like a refund."

---

## Slide 3 — Architecture: the flow of one inquiry

**On slide:** Customer → UI → Orchestrator → (Memory / Prompt / LLM decision) → Tool → real data → reply

> "Let me walk one message through the system, because the flow matters more than any single component.
>
> A customer types 'Where's my order?' That reaches the orchestrator — the piece of code that runs the whole loop. The orchestrator hands the message, plus the conversation memory so far, plus a system prompt describing the house rules, to the language model.
>
> The model's only job at that point is to decide: do I have enough information to act, or do I need to ask something? Here it doesn't have an order ID, so it asks for one — that's the clarify step.
>
> The customer replies 'ORD-1001'. Memory now has that slot filled, so on the next turn the model decides it has enough to act, and it calls a tool — `lookup_order` — which is the only thing allowed to touch the real order data. That tool comes back with a real UPS tracking number and delivery estimate, and the model turns that into a normal sentence.
>
> Four pieces, one loop: orchestrator runs it, memory remembers what's been collected, the prompt sets the rules, and tools are the only door to real facts."

---

## Slide 4 — Architecture: the four components

**On slide:** Orchestrator / Tools / Memory / Prompts — one job each

> "To define these plainly: the orchestrator is the loop itself — maybe 350 lines I can walk through line by line, no framework hiding what's happening.
>
> Tools are the agent's hands — the only code path that ever touches real order data, inventory, or policy text, which is exactly what makes hallucination structurally hard, not just discouraged by a prompt.
>
> Memory is short-term working notes — it's what lets a refund conversation collect an order ID, a reason, and an email across three separate turns without re-asking anything the customer already said.
>
> And the prompt is the house rules — one shared instruction set that tells the model to clarify before acting and to always prefer a tool over a guess, rather than writing a different prompt for every single intent."

---

## Slide 5 — Key decision 1: Facts come from tools, never from the model

**Chose / Traded off / Worth it because — on slide**

> "The first decision I'd defend hardest is splitting the system into a 'brain' and 'hands.' The model — the brain — only ever decides what to do next. It never gets to answer a factual question directly. The tools — the hands — are the only code path allowed to touch real data, and there are eight of them, each doing exactly one job.
>
> What I traded off is real: every new thing the agent can do requires me to write and register a new tool, which is slower than just letting the model freehand an answer. But I think that trade is obviously worth it here, because the failure mode on the other side isn't cosmetic — a wrong tracking number or a wrong refund amount is a real incident, not an awkward sentence. I'd rather spend the extra engineering time than ship a system that can sound confident and be wrong."

---

## Slide 6 — Key decision 2: Clarify-first intent handling, with slot memory

> "The second decision was how to handle a customer who doesn't give you everything up front, which is the normal case, not the edge case. I gave the agent a small memory of what it's already asked for and what it's still waiting on. If something's missing, it asks exactly one focused question instead of guessing or dumping every question at once.
>
> And critically, once the agent is mid-flow — say, it just asked for an email during a refund — the next thing the customer types gets interpreted as the answer to that question first, before the system tries to re-guess their intent from scratch. That fixed a real bug I hit early on, where a reply could accidentally get reinterpreted as a brand-new request and restart the flow.
>
> The trade-off is that this is a purpose-built tracker, not a general dialogue-management framework — that's fine at eight well-scoped intents, and I'd say so plainly if this needed to grow to hundreds."

---

## Slide 7 — Key decision 3: Verify-before-act, as two separate gates

> "The third decision is specifically about refunds, because that's the riskiest action in the system — wrong person, wrong order, wrong amount. I split 'prove who you are' from 'is this specific request allowed' into two separate checks.
>
> First the agent verifies the customer's email matches the order on file. Only if that passes does it even attempt the refund — and the refund tool then separately checks whether the order is actually eligible, for example whether the return window already closed. Those are genuinely different questions with different correct responses, so I didn't want them collapsed into one fuzzy 'refund denied' message.
>
> The honest trade-off is friction — a real customer answers three or four questions before anything happens, and a less careful bot would feel snappier. I think that's the right trade for money leaving the business, and I can show it live: one refund that succeeds, and one where identity passes but the return window has already expired — two different correct outcomes, not one confusing error."

---

## Slide 8 — What I'd do differently

**On slide:** First change — confidence-based escalation. Also on the list: real auth, test the AI path, real OMS integration.

> "If I had one more week, the first thing I'd change is how the agent decides to escalate. Right now, handoff to a human only triggers when the customer explicitly asks for one — which is safe, but it's reactive. It misses the case where the agent itself is struggling — say, a tool keeps failing, or the customer is rephrasing the same question because nothing's landing — and the customer hasn't thought to ask for a person yet.
>
> I think that's actually the same principle as everything else I've shown you, just pointed inward: I built the agent to never guess about a fact, but I haven't yet built it to be honest about its own uncertainty. I didn't ship that here because a real confidence signal deserves more rigor than I could responsibly build in a take-home — it's easy to fake, and I didn't want to fake it.
>
> After that, in order: I'd replace email-match verification with real session or OTP-based authentication, extend the eval suite to actually test the AI conversation path instead of only the deterministic fallback, and swap the JSON data files for live order-management and inventory integrations — which the tool-based architecture is specifically designed to make a non-event, since the agent never needs to know where its data actually comes from."

---

## Slide 9 — Close

> "So to bring it back to the start: I believe a support agent's whole job is to be trustworthy on facts and honest about what it doesn't know yet, and every architectural choice I walked through today is that belief showing up as code — clarify before acting, get facts from real systems, verify before anything risky, and be honest with myself about what I'd still change.
>
> I'd rather go deep on a handful of flows I can fully defend than wide across a dozen I can't. Happy to open up the code, run the live demo, or go deeper on any single decision from here."

---

## Anticipated pushback (have these ready)

| If they push on... | Say... |
|---|---|
| "Isn't 8 tools + hand-rolled loop going to fall over at scale?" | Yes — I said so explicitly. This is the right shape at 8 intents; a framework or a proper state machine earns its keep once tool count or coordination needs grow past that. |
| "Why not let the model just answer, it's faster?" | Speed doesn't matter if the answer's wrong. One extra second beats a confidently wrong tracking number every time. |
| "Email-match isn't real security." | Correct — it's the minimum viable signal for a take-home. In production this is a logged-in session or OTP; I named that as the first thing I'd fix after escalation. |
| "How do you know it actually works, not just this demo?" | 33 golden-set test cases, run in under a second, 100% passing — checked before every change, not just eyeballed. |
| "What's the single biggest gap?" | The agent doesn't yet doubt itself — escalation is customer-triggered, not confidence-triggered. That's slide 8, and it's the first thing I'd build next. |
