# Deploying Harvest Atlas so it survives your laptop shutting down

The app is a **Python/Flask server** (NASA POWER + OpenLandMap + Groq), so it needs
a Python host. Static hosting (Netlify/GitHub Pages) will not work - the page calls
`/select` and `/recommend`, which need the backend.

---

## Why `python main.py` is wrong on a server

`main.py`'s `main()` runs an interactive terminal chat loop that calls `input()`.
On a host with no keyboard that raises `EOFError` and the process exits. Use
`serve.py` instead - it exposes the Flask app as `app` for gunicorn:

```
gunicorn --workers 1 --threads 8 --timeout 300 --bind 0.0.0.0:$PORT serve:app
```

**Keep `--workers 1`.** The app stores the selected field in process memory, so
extra workers would each see empty state and "Diagnose this field" would fail.

---

## Option A - Hugging Face Spaces (free, no credit card)

1. Create an account at https://huggingface.co/join
2. Create a token: https://huggingface.co/settings/tokens (type: **Write**)
3. Create a Space -> **Docker** SDK -> **Blank** (free CPU basic)
4. Add secrets under *Settings -> Variables and secrets*:
   - `GROQ_API_KEY`, `GROQ_API_KEY_2` (optional), `GROQ_MODEL`
   - `EARTHDATA_USERNAME`, `EARTHDATA_PASSWORD` (optional)
5. Upload everything in this folder (the `Dockerfile` is already set up, port 7860)

URL: `https://<your-username>-<space-name>.hf.space`

Free tier sleeps after ~48h of no traffic, then wakes on the next visit.

---

## Option B - Render (free, no credit card)

1. Push this folder to a **GitHub** repo (make sure `.env` is NOT committed)
2. Render -> New -> Blueprint -> pick the repo. `render.yaml` is already included
3. Paste the env vars when prompted
4. Deploy

URL: `https://harvest-atlas-XXXX.onrender.com`

Free instances sleep after 15 min idle; first load after that takes ~50 s.

---

## Option C - Railway / Fly.io / Google Cloud Run

Same build: `pip install -r requirements.txt`, start command above. Railway and Fly
now generally require a payment method.

---

## Required environment variables

| Variable | Required | Purpose |
|---|---|---|
| `GROQ_API_KEY` | yes, for scenarios | AI rotation comparison (`/recommend`) |
| `GROQ_API_KEY_2`, `_3` | optional | Fallback keys on rate limit |
| `GROQ_MODEL` | optional | Default `openai/gpt-oss-120b` |
| `EARTHDATA_USERNAME` / `EARTHDATA_PASSWORD` | optional | NASA AppEEARS satellite samples |
| `PORT` | host-injected | Binding port |

Without any Groq key the map and NASA diagnostics still work; only the three AI
scenarios return a 503 with a clear message.

---

## Pre-flight checks (already verified locally)

- [x] Page renders: 180 KB, title "Harvest Atlas - NASA crop rotation lab"
- [x] `POST /select` returns live NASA POWER agro-climatology
- [x] `POST /recommend` returns scored scenarios via Groq
- [x] App imports and serves with **no** env vars set (no crash at startup)
- [x] `.gitignore` fixed - it previously excluded `main.py`, which breaks deploys
