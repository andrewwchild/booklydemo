# Bookly Customer Support Agent

AI-powered customer support for **Bookly**, an online bookstore. The agent handles order inquiries, returns, inventory checks, policy questions, and account support through natural conversation.

## Run locally

```bash
cd ~/Projects/bookly-cs-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Enable AI-powered responses (optional)
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Streamlit UI (recommended)
streamlit run app/streamlit_app.py

# FastAPI web UI
uvicorn app.main:app --reload --port 8000

# CLI
python scripts/cli.py
```

## Deploy

Host the Streamlit app on [Streamlit Community Cloud](https://share.streamlit.io) — see [DEPLOY.md](./DEPLOY.md).

- **Repository:** `andrewwchild/booklydemo`
- **Main file:** `app/streamlit_app.py`

## Capabilities

| Intent | Tool | Description |
|--------|------|-------------|
| Order status | `lookup_order` | Tracking, delivery, and order details |
| Returns | `verify_customer_identity` + `initiate_refund` | Identity check before processing returns |
| Escalation | `escalate_to_human` | Hand off to a specialist with conversation summary |
| Inventory | `check_stock` | Real-time book availability |
| Discovery | `research_books` | Recommendations by subject or topic |
| Policies | `get_policy` | Shipping, returns, and account help |
| Account | `send_password_reset` | Password reset emails |

## Architecture

```
Customer → Chat UI → BooklyAgent (orchestrator)
                        ├── ConversationMemory (session + slot filling)
                        ├── System prompt (clarify-first rules)
                        └── OpenAI function calling
                              └── Bookly APIs (orders, catalog, policies)
```

## Project structure

```
agent/          # Orchestration, prompts, memory
tools/          # Bookly service integrations + tool schemas
data/           # Orders, catalog, and policies
app/            # Streamlit + FastAPI interfaces
notebooks/      # Agent evaluation notebook
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Optional | Enables AI-powered conversation |
| `OPENAI_MODEL` | Optional | Defaults to `gpt-4o-mini` |

Without an API key, the rules-based engine handles structured requests.

## Eval harness

Run golden-set tests against the rules engine:

```bash
python evals/run_evals.py
```

The harness checks ~25 cases for correct tool selection, clarifying questions, and response content.

## License

MIT — see [LICENSE](./LICENSE).
