"""Decagon-inspired visual theme for Bookly support surfaces."""

DECAGON_CSS = """
@font-face {
  font-family: Circular;
  src: url("https://cdn.prod.website-files.com/683e5da0b6d8a19de4875ae7/6a04985de05b82f9d9de1893_CircularXXSub-Book.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: Circular;
  src: url("https://cdn.prod.website-files.com/683e5da0b6d8a19de4875ae7/6a04985eb7510dfdda152e64_CircularXXSub-Medium.woff2") format("woff2");
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: Circular;
  src: url("https://cdn.prod.website-files.com/683e5da0b6d8a19de4875ae7/6a04985d569d553286179732_CircularXXSub-Bold.woff2") format("woff2");
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

:root {
  --ink: #0A0A0B;
  --ink-2: #3F3F44;
  --muted: #6E6E76;
  --line: #E6E6E4;
  --line-soft: #ECECEA;
  --peri: #5754FF;
  --peri-deep: #4340D6;
  --peri-soft: #ECECFF;
  --peri-tint: #F5F5FF;
  --peri-border: #DBDAF9;
  --bg: #FFFFFF;
  --bg-soft: #F4F4F2;
  --dark: #0E0E10;
  --font: Circular, -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  --control-h: 40px;
  --control-font: 0.82rem;
  --control-radius: 12px;
  --widget-pad-x: 16px;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] *:not([data-testid="stIconMaterial"]):not(.material-icons) {
  font-family: var(--font) !important;
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--ink) !important;
  -webkit-font-smoothing: antialiased;
}

.bookly-shell, .bookly-shell h1, .bookly-shell p, .bookly-shell b {
  font-family: var(--font) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"], footer {
  display: none !important;
}

.block-container {
  max-width: 920px !important;
  padding-top: 0 !important;
  padding-bottom: 3rem !important;
}

/* Hero — compact header band */
.bookly-hero-wrap { padding: 5px 0 0; }

.bookly-hero {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  background: linear-gradient(
    178deg,
    #CBC7F3 0%,
    #B9B0EE 42%,
    #BCA9E7 64%,
    #DDBBD8 84%,
    #EFCDD4 100%
  );
  padding: 14px 18px 16px;
}

.bookly-hero::after {
  content: "";
  position: absolute;
  right: 7%;
  top: 14%;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 34%, #F7F3FC, #D8CCEE 58%, #BFAEE2 100%);
  box-shadow: 0 0 40px 14px rgba(255, 255, 255, 0.3);
  opacity: 0.95;
}

.bookly-hero-inner { position: relative; z-index: 2; max-width: 26rem; }

.bookly-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.72rem;
  font-weight: 500;
  color: #28243D;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(6px);
  padding: 5px 10px;
  border-radius: 999px;
}

.bookly-hero h1 {
  margin: 8px 0 0;
  font-size: clamp(1rem, 2.2vw, 1.4rem);
  font-weight: 500;
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: #161425;
}

.bookly-hero p {
  margin: 6px 0 0;
  font-size: 0.82rem;
  color: #332F4A;
  line-height: 1.4;
}

.bookly-composer-label {
  margin: 20px 0 10px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--ink);
}

/* Self-contained chat widget */
div[data-testid="stVerticalBlockBorderWrapper"] {
  border: 2px solid var(--peri-border) !important;
  border-radius: 22px !important;
  background: #FFFFFF !important;
  box-shadow: 0 12px 36px rgba(87, 84, 255, 0.1) !important;
  overflow: hidden !important;
  margin-top: 18px !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
  padding-top: 0 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stHorizontalBlock"]:first-of-type {
  align-items: center !important;
  padding: 0.7rem var(--widget-pad-x) !important;
  margin: 0 !important;
  border-bottom: 1px solid var(--line-soft) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stMarkdownContainer"] p {
  margin: 0 !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  line-height: var(--control-h) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stHorizontalBlock"]:first-of-type .stButton {
  width: 100% !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {
  height: var(--control-h) !important;
  min-height: var(--control-h) !important;
  width: 100% !important;
  font-size: var(--control-font) !important;
  padding: 0 0.85rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stChatMessage"] {
  padding-left: 0.25rem !important;
  padding-right: 0.25rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] > div[style*="overflow"] {
  border-bottom: 1px solid var(--line-soft) !important;
  background: var(--bg-soft) !important;
}

.bookly-widget-footer-start {
  background: var(--bg-soft);
  padding: 10px var(--widget-pad-x) 0;
}

.bookly-chip-label {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  color: var(--muted);
}

.bookly-widget-footer-start ~ div[data-testid="stHorizontalBlock"] {
  background: var(--bg-soft) !important;
  padding: 0 var(--widget-pad-x) 8px !important;
  margin-top: 0 !important;
  gap: 0.5rem !important;
}

.bookly-widget-footer-start ~ div[data-testid="stHorizontalBlock"] [data-testid="column"] {
  display: flex !important;
  min-width: 0 !important;
}

.bookly-widget-footer-start ~ div[data-testid="stHorizontalBlock"] .stButton {
  width: 100% !important;
}

.bookly-widget-footer-start ~ div[data-testid="stHorizontalBlock"] .stButton > button {
  height: var(--control-h) !important;
  min-height: var(--control-h) !important;
  width: 100% !important;
  font-size: var(--control-font) !important;
  padding: 0 0.65rem !important;
  border-radius: 999px !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] {
  margin: 0 !important;
  padding: 8px var(--widget-pad-x) 14px !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  background: var(--bg-soft) !important;
  border-top: 1px solid var(--line-soft) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] [data-testid="stTextInput"] {
  width: 100% !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] [data-testid="stTextInput"] input {
  height: var(--control-h) !important;
  min-height: var(--control-h) !important;
  border: 2px solid var(--peri-border) !important;
  border-radius: var(--control-radius) !important;
  background: #FFFFFF !important;
  color: var(--ink) !important;
  font-size: var(--control-font) !important;
  line-height: 1.2 !important;
  padding: 0 0.9rem !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] [data-testid="stTextInput"] input:focus {
  border-color: var(--peri) !important;
  box-shadow: 0 0 0 4px rgba(87, 84, 255, 0.14) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] [data-testid="column"] {
  display: flex !important;
  align-items: center !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] .stButton {
  width: 100% !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] .stButton > button {
  height: var(--control-h) !important;
  min-height: var(--control-h) !important;
  width: 100% !important;
  font-size: var(--control-font) !important;
  padding: 0 1rem !important;
  border-radius: var(--control-radius) !important;
  background: var(--ink) !important;
  color: #FFFFFF !important;
  border-color: var(--ink) !important;
}

/* Legacy standalone composer (unused) */
form[data-testid="stForm"] {
  margin: 0 0 8px !important;
  padding: 18px 18px 14px !important;
  border-radius: 22px !important;
  border: 2px solid var(--peri-border) !important;
  background: linear-gradient(180deg, #FFFFFF 0%, var(--peri-tint) 100%) !important;
  box-shadow: 0 10px 30px rgba(87, 84, 255, 0.12) !important;
}

.bookly-chat-panel {
  margin-top: 8px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--bg-soft);
  max-height: 42vh;
  overflow-y: auto;
}

/* Hide Streamlit's fixed bottom chat input if any legacy widget remains */
[data-testid="stBottomBlock"],
[data-testid="stChatInput"] {
  display: none !important;
}

.bookly-shell { margin: 0 -1rem; }

.bookly-announce {
  text-align: center;
  font-size: 0.82rem;
  color: var(--ink-2);
  padding: 10px 20px;
  border-bottom: 1px solid var(--line-soft);
  background: var(--bg);
}

.bookly-announce b { color: var(--ink); font-weight: 600; }
.bookly-announce .accent { color: var(--peri-deep); font-weight: 500; }

.bookly-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0 18px;
  border-bottom: 1px solid var(--line-soft);
}

.bookly-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: var(--ink);
  font-size: 0.95rem;
}

.bookly-brand .mark {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, #5754FF 0%, #9B99FF 100%);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.72rem;
  font-weight: 700;
}

.bookly-brand .sub {
  color: var(--muted);
  font-weight: 500;
}

.bookly-stats {
  margin-top: 10px;
  background: var(--dark);
  border-radius: 28px;
  color: white;
  overflow: hidden;
}

.bookly-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}

.bookly-stat {
  padding: 28px 22px;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.bookly-stat:last-child { border-right: none; }

.bookly-stat .n {
  font-size: 1.8rem;
  letter-spacing: -0.02em;
  line-height: 1.1;
  background: linear-gradient(115deg, #E3E2FF 5%, #9B99FF 55%, #7370FF 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 600;
}

.bookly-stat .l {
  margin-top: 8px;
  font-size: 0.82rem;
  color: #A5A5AE;
  line-height: 1.4;
}

.section-label {
  margin: 24px 0 10px;
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--muted);
}

[data-testid="stChatMessage"] {
  background: transparent !important;
  border: none !important;
  padding: 0.35rem 0 !important;
}

[data-testid="stChatMessageAvatarAssistant"] {
  background: linear-gradient(135deg, #5754FF, #9B99FF) !important;
  color: white !important;
}

[data-testid="stChatMessageAvatarUser"] {
  background: var(--ink) !important;
  color: white !important;
}

[data-testid="stChatMessageContent"] {
  background: var(--bg-soft) !important;
  border: 1px solid var(--line) !important;
  color: var(--ink) !important;
  border-radius: 18px !important;
  padding: 0.85rem 1rem !important;
  line-height: 1.55 !important;
  box-shadow: none !important;
}

[data-testid="stChatMessage"][data-testid*="user"] [data-testid="stChatMessageContent"],
.stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
  background: var(--peri-tint) !important;
  border-color: var(--peri-border) !important;
}

div[data-testid="stChatInput"] {
  border-top: 1px solid var(--line-soft);
  padding-top: 0.75rem;
}

div[data-testid="stChatInput"] textarea {
  border: 1px solid var(--line) !important;
  border-radius: 999px !important;
  background: var(--bg) !important;
  color: var(--ink) !important;
  padding: 0.8rem 1.1rem !important;
}

div[data-testid="stChatInput"] textarea:focus {
  border-color: var(--peri) !important;
  box-shadow: 0 0 0 3px rgba(87, 84, 255, 0.12) !important;
}
/* Hide Streamlit's fixed bottom chat input */
[data-testid="stBottomBlock"],
[data-testid="stChatInput"] {
  display: none !important;
}

.stButton > button {
  border-radius: var(--control-radius) !important;
  border: 1px solid var(--peri-border) !important;
  background: var(--bg) !important;
  color: var(--peri-deep) !important;
  font-weight: 500 !important;
  font-size: var(--control-font) !important;
  height: var(--control-h) !important;
  min-height: var(--control-h) !important;
  padding: 0 0.9rem !important;
  transition: all 0.18s ease !important;
}

.stButton > button:hover {
  background: var(--peri-tint) !important;
  border-color: #C6C4F7 !important;
  color: var(--peri-deep) !important;
}

.stButton > button[kind="primary"],
.bookly-reset button {
  background: var(--ink) !important;
  color: white !important;
  border-color: var(--ink) !important;
}

.stButton > button[kind="primary"]:hover,
.bookly-reset button:hover {
  background: #232327 !important;
}

@media (max-width: 760px) {
  .bookly-stats-grid { grid-template-columns: 1fr 1fr; }
  .bookly-stat:nth-child(2) { border-right: none; }
  .bookly-stat { border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
  .bookly-stat:nth-last-child(-n+2) { border-bottom: none; }
  .bookly-hero { border-radius: 14px; padding: 12px 14px 14px; }
  .bookly-hero::after { width: 48px; height: 48px; right: 5%; top: 10%; }
  div[data-testid="stVerticalBlockBorderWrapper"] form[data-testid="stForm"] [data-testid="column"]:first-child {
    min-width: 0 !important;
  }
}
"""


def render_shell_header(*, catalog_count: int, tool_count: int = 8, eval_count: int = 33) -> str:
    return f"""
<div class="bookly-shell">
  <div class="bookly-announce">
    <b>Bookly Support</b> · Your AI concierge for orders, returns, and book picks ·
    <span class="accent">Backed by real-time tools</span>
  </div>
  <div class="bookly-nav">
    <div class="bookly-brand">
      <span class="mark">B</span>
      <span>Bookly</span>
      <span class="sub">Support Team</span>
    </div>
  </div>
  <div class="bookly-hero-wrap">
    <div class="bookly-hero">
      <div class="bookly-hero-inner">
        <div class="bookly-pill">✦ Bookly Support · AI Assistant</div>
        <h1>Your AI concierge for every reader.</h1>
        <p>Track orders, start returns, get book picks, and account help —
        we clarify first, using live Bookly data.</p>
      </div>
    </div>
  </div>
  <div class="bookly-stats">
    <div class="bookly-stats-grid">
      <div class="bookly-stat">
        <div class="n">{catalog_count}</div>
        <div class="l"><b>Titles</b> in catalog</div>
      </div>
      <div class="bookly-stat">
        <div class="n">{tool_count}</div>
        <div class="l"><b>Tools</b> for reliable answers</div>
      </div>
      <div class="bookly-stat">
        <div class="n">{eval_count}</div>
        <div class="l"><b>Regression tests</b> in eval suite</div>
      </div>
      <div class="bookly-stat">
        <div class="n">24/7</div>
        <div class="l"><b>Help</b> always on</div>
      </div>
    </div>
  </div>
</div>
"""
