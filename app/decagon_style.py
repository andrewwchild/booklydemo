"""Decagon-inspired visual theme for Bookly support surfaces."""

DECAGON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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
}

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"], footer {
  display: none !important;
}

.block-container {
  max-width: 920px !important;
  padding-top: 0 !important;
  padding-bottom: 3rem !important;
}

/* Compact hero so chat controls appear sooner */
.bookly-hero {
  padding: 22px 28px 24px;
}

.bookly-hero h1 {
  font-size: clamp(1.45rem, 3vw, 2rem);
  margin-top: 12px;
}

.bookly-hero p {
  font-size: 0.95rem;
  margin-top: 10px;
}

.bookly-hero::after {
  width: 90px;
  height: 90px;
  top: 12%;
}

.bookly-stat {
  padding: 18px 16px;
}

.bookly-stat .n {
  font-size: 1.45rem;
}

.bookly-composer-label {
  margin: 20px 0 10px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--ink);
}

form[data-testid="stForm"] {
  margin: 0 0 8px !important;
  padding: 18px 18px 14px !important;
  border-radius: 22px !important;
  border: 2px solid var(--peri-border) !important;
  background: linear-gradient(180deg, #FFFFFF 0%, var(--peri-tint) 100%) !important;
  box-shadow: 0 10px 30px rgba(87, 84, 255, 0.12) !important;
}

form[data-testid="stForm"] [data-testid="stTextArea"] textarea {
  min-height: 88px !important;
  border: 2px solid var(--peri-border) !important;
  border-radius: 16px !important;
  background: #FFFFFF !important;
  color: var(--ink) !important;
  font-size: 1rem !important;
  line-height: 1.5 !important;
  padding: 1rem 1.1rem !important;
  box-shadow: inset 0 1px 2px rgba(10, 10, 11, 0.04) !important;
}

form[data-testid="stForm"] [data-testid="stTextArea"] textarea:focus {
  border-color: var(--peri) !important;
  box-shadow: 0 0 0 4px rgba(87, 84, 255, 0.16) !important;
}

form[data-testid="stForm"] .stButton > button {
  min-height: 48px !important;
  font-size: 0.95rem !important;
  padding: 0.7rem 1.4rem !important;
  background: var(--ink) !important;
  color: #FFFFFF !important;
  border-color: var(--ink) !important;
}

.bookly-composer-hint {
  margin: 0 0 16px;
  font-size: 0.8rem;
  color: var(--muted);
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

.bookly-hero-wrap { padding: 10px 0 0; }

.bookly-hero {
  position: relative;
  overflow: hidden;
  border-radius: 28px;
  background: linear-gradient(
    178deg,
    #CBC7F3 0%,
    #B9B0EE 42%,
    #BCA9E7 64%,
    #DDBBD8 84%,
    #EFCDD4 100%
  );
  padding: 34px 34px 38px;
}

.bookly-hero::after {
  content: "";
  position: absolute;
  right: 7%;
  top: 18%;
  width: 130px;
  height: 130px;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 34%, #F7F3FC, #D8CCEE 58%, #BFAEE2 100%);
  box-shadow: 0 0 80px 28px rgba(255, 255, 255, 0.3);
  opacity: 0.95;
}

.bookly-hero-inner { position: relative; z-index: 2; max-width: 34rem; }

.bookly-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
  font-weight: 500;
  color: #28243D;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(6px);
  padding: 8px 15px;
  border-radius: 999px;
}

.bookly-hero h1 {
  margin: 18px 0 0;
  font-size: clamp(1.9rem, 4vw, 2.8rem);
  font-weight: 500;
  letter-spacing: -0.02em;
  line-height: 1.08;
  color: #161425;
}

.bookly-hero p {
  margin: 14px 0 0;
  font-size: 1.02rem;
  color: #332F4A;
  line-height: 1.5;
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
  border-radius: 999px !important;
  border: 1px solid var(--peri-border) !important;
  background: var(--bg) !important;
  color: var(--peri-deep) !important;
  font-weight: 500 !important;
  font-size: 0.82rem !important;
  padding: 0.45rem 0.9rem !important;
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
  .bookly-hero { border-radius: 22px; padding: 26px 22px 30px; }
  .bookly-hero::after { width: 90px; height: 90px; right: 5%; top: 8%; }
}
"""


def render_shell_header(*, catalog_count: int, tool_count: int = 8, eval_count: int = 33) -> str:
    return f"""
<div class="bookly-shell">
  <div class="bookly-announce">
    <b>Bookly Support</b> · AI concierge for orders, returns, and recommendations ·
    <span class="accent">Powered by grounded tools</span>
  </div>
  <div class="bookly-nav">
    <div class="bookly-brand">
      <span class="mark">B</span>
      <span>Bookly</span>
      <span class="sub">Customer Support</span>
    </div>
  </div>
  <div class="bookly-hero-wrap">
    <div class="bookly-hero">
      <div class="bookly-hero-inner">
        <div class="bookly-pill">✦ Bookly Support · AI Concierge</div>
        <h1>The AI concierge for every book lover.</h1>
        <p>Order tracking, returns, topic recommendations, and account help —
        clarify-first, grounded in real Bookly data.</p>
      </div>
    </div>
  </div>
  <div class="bookly-stats">
    <div class="bookly-stats-grid">
      <div class="bookly-stat">
        <div class="n">{catalog_count}</div>
        <div class="l"><b>Titles</b> in our catalog</div>
      </div>
      <div class="bookly-stat">
        <div class="n">{tool_count}</div>
        <div class="l"><b>Tools</b> for grounded answers</div>
      </div>
      <div class="bookly-stat">
        <div class="n">{eval_count}</div>
        <div class="l"><b>Golden tests</b> in eval harness</div>
      </div>
      <div class="bookly-stat">
        <div class="n">24/7</div>
        <div class="l"><b>Support</b> always available</div>
      </div>
    </div>
  </div>
</div>
"""
