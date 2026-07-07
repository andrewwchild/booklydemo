# Bookly Customer Support Agent

A conversational AI agent for **Bookly**, a fictional online bookstore — built as a Decagon Solutions Engineering take-home prototype.

**Thesis:** Great CX agents are *grounded, clarify-first, and action-capable*. They never hallucinate transactional data, ask focused questions before acting, and use tools for authoritative answers.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/andrewwchild/booklydemo/blob/main/notebooks/bookly_demo.ipynb)

> Colab link: `https://colab.research.google.com/github/andrewwchild/booklydemo/blob/main/notebooks/bookly_demo.ipynb`

## Push to GitHub

```bash
cd ~/Projects/bookly-cs-agent
git init
git add .
git commit -m "Bookly CS agent take-home prototype"
git branch -M main
git remote add origin https://github.com/andrewwchild/booklydemo.git
git push -u origin main
```

Or use **Cursor → Source Control → Publish to GitHub** (creates the remote for you).

## Quick start

### Google Colab (live presentation)

1. Push this repo to GitHub
2. Click **Open in Colab** above (or open `notebooks/bookly_demo.ipynb` from GitHub → Open in Colab)
3. Run **Step 1** → **Step 2** → demo cells
4. (Optional) Add Colab Secret `OPENAI_API_KEY` via the 🔑 sidebar

No `REPO_URL` configuration needed when opening from GitHub.

### Local

```bash
cd ~/Projects/bookly-cs-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Optional: enable live LLM (recommended for live presentation)
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Option A: Jupyter notebook (great for live screen share)
jupyter notebook notebooks/bookly_demo.ipynb

# Option B: Web chat UI (FastAPI)
uvicorn app.main:app --reload --port 8000

# Option C: Streamlit UI (quick polished demo)
streamlit run app/streamlit_app.py
```

Open [http://localhost:8000](http://localhost:8000) for the FastAPI web UI, or [http://localhost:8501](http://localhost:8501) for Streamlit.

### Deploy publicly (free)

Host the Streamlit app on the internet via **Streamlit Community Cloud** — see [DEPLOY.md](./DEPLOY.md).

Quick version:
1. Push repo to GitHub
2. Go to https://share.streamlit.io → **New app**
3. Repo: `andrewwchild/booklydemo` · Main file: `app/streamlit_app.py`
4. Deploy → share the public URL

Works **without an API key** in deterministic mock mode — reliable for live presentations if the network fails.

See [PRESENTATION.md](./PRESENTATION.md) for a live demo script and checklist.

## Live presentation script (~5 min)

Run cells in `notebooks/bookly_demo.ipynb` **in order**:

1. **Clarifying question:** "Where is my order?" → agent asks for order ID
2. **Tool use:** "ORD-1001" → `lookup_order` runs, shows UPS tracking
3. **Multi-turn refund:** "I want a refund" → reason → email → `initiate_refund` executes
4. **Policy FAQ:** "What's your return policy?" → `get_policy` returns official text
5. **Stock check:** "Is Fourth Wing in stock?" → `check_stock` returns catalog data

### Test data (15 orders)

| Order ID  | Email               | Status           | Notes |
|-----------|---------------------|------------------|-------|
| ORD-1001  | alice@example.com   | Shipped          | Standard tracking demo |
| ORD-1002  | bob@example.com     | Processing       | Not return-eligible |
| ORD-1003  | carol@example.com   | Delivered        | Refund demo |
| ORD-1004  | david@example.com   | Delivered        | Return window expired |
| ORD-1005  | emma@example.com    | Shipped          | |
| ORD-1006  | frank@example.com   | Delayed          | Weather delay |
| ORD-1007  | grace@example.com   | Out for delivery | |
| ORD-1008  | henry@example.com   | Cancelled        | |
| ORD-1009  | iris@example.com    | Processing       | |
| ORD-1010  | jack@example.com    | Delivered        | Refund demo |
| ORD-1011  | kate@example.com    | Shipped          | |
| ORD-1012  | liam@example.com    | Delivered        | |
| ORD-1013  | mia@example.com     | Processing       | Gift order |
| ORD-1014  | noah@example.com    | Shipped          | |
| ORD-1015  | olivia@example.com  | Delivered        | |

## Architecture

```
User → FastAPI /api/chat → BooklyAgent (orchestrator)
                              ├── ConversationMemory (session state + slot filling)
                              ├── System prompt (clarify-first rules)
                              └── OpenAI function calling loop
                                    └── Tools: lookup_order, initiate_refund,
                                        get_policy, send_password_reset
```

See [PITCH_DECK.md](./PITCH_DECK.md) for the 3–5 slide narrative.

## Project structure

```
agent/          # Orchestration, prompts, memory, demo helpers
tools/          # Mock Bookly backend + OpenAI tool schemas
data/           # Mock orders & policies (JSON)
app/            # FastAPI server + chat UI
notebooks/      # Live presentation notebook
```

## Key technical decisions

1. **Tools over RAG for transactional queries** — order status and refunds need authoritative data, not embeddings.
2. **Explicit slot filling in memory** — refund flow tracks `order_id`, `reason`, `customer_email` across turns; regex extraction supplements the LLM.
3. **Clarify-before-act prompt + mock fallback** — agent must gather required fields before tool calls; mock mode demonstrates the same flows without an API key.

## Production next steps

- Auth + customer identity verification (OAuth/session)
- Real OMS/CRM integrations instead of JSON mocks
- Eval suite (intent accuracy, tool selection, hallucination checks)
- Human handoff with conversation summary
- Rate limiting, PII redaction in logs, audit trail for refunds

## License

MIT — see [LICENSE](./LICENSE).
