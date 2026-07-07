# Deploy Bookly Agent (public URL)

The fastest way to host the **Streamlit UI** for free is **Streamlit Community Cloud**. It connects to your GitHub repo and gives you a public link like:

`https://booklydemo.streamlit.app`

---

## Step 1: Push latest code to GitHub

Make sure your repo is up to date:

```bash
cd ~/Projects/bookly-cs-agent
git add .
git commit -m "Prepare Streamlit cloud deploy"
git push origin main
```

Repo: https://github.com/andrewwchild/booklydemo

---

## Step 2: Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Sign in with **GitHub**
3. Click **New app**
4. Fill in:
   - **Repository:** `andrewwchild/booklydemo`
   - **Branch:** `main`
   - **Main file path:** `app/streamlit_app.py`
5. Click **Deploy**

First deploy takes 2–3 minutes.

---

## Step 3: Add your OpenAI key (optional)

Without this, the app runs in **mock mode** (fine for demo).

1. In Streamlit Cloud → your app → **Settings** (⚙️)
2. **Secrets** → paste:

```toml
OPENAI_API_KEY = "sk-your-key-here"
```

3. **Save** → app reboots automatically

---

## Step 4: Share the link

Copy the app URL from Streamlit Cloud and use it in your interview — no localhost needed.

---

## Other hosting options

| Platform | Best for |
|----------|----------|
| **Streamlit Cloud** | Easiest for this app (recommended) |
| **Hugging Face Spaces** | Also free; pick Streamlit as SDK |
| **Railway / Render** | FastAPI backend + custom frontend |
| **Colab notebook** | Already set up — good for technical walkthrough |

---

## Troubleshooting

**App crashes on startup**
- Check Streamlit Cloud logs
- Confirm main file path is `app/streamlit_app.py`

**"No module named agent"**
- Fixed in `streamlit_app.py` — push latest code

**Slow first load**
- Free tier sleeps after inactivity; first visitor wakes it (~30 sec)
