# Deploy Bookly Support

Host the Streamlit app on **Streamlit Community Cloud** for a public URL like:

`https://booklydemo.streamlit.app`

## Deploy

1. Push the latest code to GitHub
2. Go to **https://share.streamlit.io** → sign in with GitHub
3. **New app** → set:
   - **Repository:** `andrewwchild/booklydemo`
   - **Branch:** `main`
   - **Main file path:** `app/streamlit_app.py`
4. Click **Deploy**

## Secrets (optional)

For AI-powered responses, add in **Settings → Secrets**:

```toml
OPENAI_API_KEY = "sk-your-key-here"
```

Without this, the rules-based engine handles customer requests.

## Troubleshooting

- **Import errors:** Ensure `requirements.txt` includes `-e .`
- **Slow cold start:** Free tier apps sleep after inactivity (~30s to wake)
- **Logs:** Manage app → Logs
