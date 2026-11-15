"""Production entry point for Harvest Atlas.

`main.py` is written as a desktop app: its `main()` also runs an interactive
terminal chat loop that calls input(), which cannot work on a server. This module
imports the Flask app and exposes it as `app` for WSGI servers (gunicorn), so the
web UI runs without the terminal loop.

Do not use `python main.py` on a host: it will block on input() and die.

Local run:
    python serve.py

Production run:
    gunicorn --workers 1 --threads 8 --timeout 300 --bind 0.0.0.0:$PORT serve:app

NOTE: keep --workers 1. The app keeps the selected field and its NASA data in
process memory (module-level globals), so multiple worker processes would each
see a different, empty state and the diagnose/scenario flow would break.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main  # noqa: E402  (loads .env if present, defines Flask `app`)

# WSGI target for gunicorn/uwsgi.
app = main.app

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    print(f"Harvest Atlas serving on http://{host}:{port}", flush=True)
    app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
