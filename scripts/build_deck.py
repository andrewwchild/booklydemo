#!/usr/bin/env python3
"""Generate the Bookly CS Agent pitch deck as PowerPoint."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUTPUT = Path(__file__).resolve().parent.parent / "Bookly_CS_Agent_Pitch.pptx"

# Colors
BG_DARK = RGBColor(15, 20, 25)
ACCENT = RGBColor(79, 140, 255)
TEXT = RGBColor(232, 237, 244)
MUTED = RGBColor(139, 156, 179)
GREEN = RGBColor(111, 207, 151)
RED = RGBColor(242, 153, 74)


def set_slide_bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, size=18, bold=False, color=TEXT, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return tf


def add_bullets(tf, items, size=16, color=TEXT, level=0):
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 and not tf.paragraphs[0].text else tf.add_paragraph()
        p.text = item
        p.level = level
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(8)


def add_notes(slide, text: str) -> None:
    notes = slide.notes_slide.notes_text_frame
    notes.text = text


def build_deck() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ── Slide 1: Title + Thesis ─────────────────────────────────────
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, BG_DARK)
    add_textbox(slide, Inches(0.8), Inches(0.6), Inches(11), Inches(0.6),
                "BOOKLY CUSTOMER SUPPORT AGENT", size=14, color=ACCENT, bold=True)
    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(11.5), Inches(1.2),
                "The best CX agents don't guess —\nthey clarify, then act on real data.",
                size=36, bold=True)
    tf = add_textbox(slide, Inches(0.8), Inches(2.8), Inches(5.5), Inches(3.5), "", size=16)
    add_bullets(tf, [
        "Wrong answers destroy trust faster than one extra question",
        "Human in conversation, machine-precise on facts",
        "Transactional queries always use tools — never free-form generation",
        "One focused clarifying question at a time when info is missing",
    ], size=17)
    add_textbox(slide, Inches(7), Inches(2.8), Inches(5.5), Inches(3.8),
                "User message\n      ↓\nHave order_id?\n   ↙     ↘\n Yes      No\n  ↓        ↓\nTool    Clarify",
                size=15, color=MUTED, align=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(0.8), Inches(6.5), Inches(11), Inches(0.5),
                "Bookly Customer Support  ·  bookly.com",
                size=12, color=MUTED)
    add_notes(slide, "I'd rather add one turn than ship a confident lie.")

    # ── Slide 2: Architecture ─────────────────────────────────────────
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, BG_DARK)
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
                "Architecture", size=14, color=ACCENT, bold=True)
    add_textbox(slide, Inches(0.8), Inches(1.0), Inches(11.5), Inches(0.9),
                "Thin orchestration + LLM reasoning + deterministic tools",
                size=30, bold=True)
    arch = (
        "Chat UI  →  BooklyAgent  →  Bookly Service APIs\n"
        "                              ├─ System prompt (clarify-first rules)\n"
        "                              ├─ ConversationMemory (slots + history)\n"
        "                              └─ OpenAI function calling (5 tools)"
    )
    add_textbox(slide, Inches(0.8), Inches(2.1), Inches(11.5), Inches(2.2), arch,
                size=15, color=MUTED)
    tf = add_textbox(slide, Inches(0.8), Inches(4.5), Inches(11), Inches(2.5), "", size=16)
    add_bullets(tf, [
        "Orchestrator — runs LLM ↔ tool loop (up to 5 turns per message)",
        "Tools — lookup_order · initiate_refund · check_stock · get_policy · send_password_reset",
        "Memory — per-session history + extracted slots",
        "Prompts — clarify-first rules and tone guardrails",
    ], size=17)
    add_notes(slide,
              "I avoided all-in-one agent platforms on purpose — ~300 lines of orchestration I can explain line by line.")

    # ── Slide 3: Decision 1 ─────────────────────────────────────────
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, BG_DARK)
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.5),
                "KEY DECISION #1", size=14, color=ACCENT, bold=True)
    add_textbox(slide, Inches(0.8), Inches(1.0), Inches(11.5), Inches(0.9),
                "Tools over RAG for transactions",
                size=32, bold=True)
    add_textbox(slide, Inches(0.8), Inches(2.0), Inches(11), Inches(0.6),
                "Order status, refunds, and inventory use function calling to Bookly APIs — not vector search.",
                size=18, color=MUTED)
    tf = add_textbox(slide, Inches(0.8), Inches(2.8), Inches(5.2), Inches(3.5), "Pros", size=18, bold=True, color=GREEN)
    add_bullets(tf, [
        "Zero hallucination risk on order IDs, tracking, refund amounts",
        "Actions (initiate_refund) are first-class — not instructions to the user",
    ], size=16, color=TEXT)
    tf = add_textbox(slide, Inches(6.5), Inches(2.8), Inches(5.5), Inches(3.5), "Trade-off", size=18, bold=True, color=RED)
    add_bullets(tf, [
        "Each new action requires a new tool + integration",
        "More eng work than dumping everything into a knowledge base",
    ], size=16, color=TEXT)
    add_textbox(slide, Inches(0.8), Inches(6.0), Inches(11.5), Inches(0.8),
                "Why worth it: Wrong order data is a P0 incident. RAG is great for policies; transactions need systems of record.",
                size=16, color=ACCENT, bold=True)

    # ── Slide 4: Decision 2 ─────────────────────────────────────────
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, BG_DARK)
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.5),
                "KEY DECISION #2", size=14, color=ACCENT, bold=True)
    add_textbox(slide, Inches(0.8), Inches(1.0), Inches(11.5), Inches(0.9),
                "Clarify-first + slot memory",
                size=32, bold=True)
    add_textbox(slide, Inches(0.8), Inches(2.0), Inches(11), Inches(0.6),
                "LLM handles natural language; ConversationMemory tracks required fields across turns.",
                size=18, color=MUTED)
    tf = add_textbox(slide, Inches(0.8), Inches(2.8), Inches(5.2), Inches(3.5), "Pros", size=18, bold=True, color=GREEN)
    add_bullets(tf, [
        "Refund flow collects order_id → reason → email before acting",
        "Regex slot extraction catches structured inputs the LLM might miss",
    ], size=16)
    tf = add_textbox(slide, Inches(6.5), Inches(2.8), Inches(5.5), Inches(3.5), "Trade-off", size=18, bold=True, color=RED)
    add_bullets(tf, [
        "Not a full finite-state machine",
        "Edge cases need tighter validation in production",
    ], size=16)
    add_textbox(slide, Inches(0.8), Inches(5.8), Inches(11.5), Inches(1.0),
                'Example: "I want a refund" → order ID → reason → email → initiate_refund',
                size=17, color=ACCENT, bold=True)

    # ── Slide 5: Production ─────────────────────────────────────────
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide, BG_DARK)
    add_textbox(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.5),
                "WHAT I'D DO DIFFERENTLY", size=14, color=ACCENT, bold=True)
    add_textbox(slide, Inches(0.8), Inches(1.0), Inches(11.5), Inches(0.9),
                "Eval harness + human handoff — first",
                size=32, bold=True)
    rows = [
        ("Gap today", "Production fix"),
        ("No automated tool-selection tests", "Golden-set evals: 50+ utterances → expected intent"),
        ("JSON data stores", "OMS + inventory + CRM integrations"),
        ("No escalation path", "Confidence threshold → summarize → route to human"),
        ("In-process session memory", "Redis + customer auth for cross-device continuity"),
    ]
    top = Inches(2.2)
    for i, (left, right) in enumerate(rows):
        y = top + Inches(i * 0.72)
        color = ACCENT if i == 0 else TEXT
        bold = i == 0
        sz = 15 if i == 0 else 14
        c = MUTED if i == 0 else TEXT
        add_textbox(slide, Inches(0.8), y, Inches(5.2), Inches(0.65), left, size=sz, bold=bold, color=c)
        add_textbox(slide, Inches(6.2), y, Inches(6.2), Inches(0.65), right, size=sz, bold=bold, color=c)
    add_textbox(slide, Inches(0.8), Inches(6.0), Inches(11.5), Inches(0.9),
                "Depth beats breadth — two flows done well beats ten done shallow.",
                size=18, color=ACCENT, bold=True)
    add_notes(slide,
              "Before scaling intents, you need to know if the agent chooses the right action — that's what enterprise buyers audit.")

    return prs


if __name__ == "__main__":
    deck = build_deck()
    deck.save(OUTPUT)
    print(f"Saved: {OUTPUT}")
