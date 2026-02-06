# Steve Hof — Math & Statistics Tutoring (FastAPI + Jinja + HTMX + Tailwind)

A minimal, modern Python web stack:

- **FastAPI**: fast, type‑safe web framework built on Starlette
- **Jinja2**: server‑rendered HTML templates (excellent for SEO and speed)
- **HTMX**: sprinkle interactivity without a SPA; progressive enhancement
- **Tailwind CSS (CDN)**: rapid, responsive UI (swap to CLI later if you want)

## Quickstart (macOS, Poetry)

```bash
# 1) Unzip this project somewhere on your Mac
# 2) In the project root:
poetry install
poetry run uvicorn app.main:app --reload
# Visit http://127.0.0.1:8000
```

## Dev tips
- Update copy, rates, and sections in `app/templates/index.html`.
- Replace `app/emailer.py` with your actual email provider (Mailgun/SendGrid/Resend) and add keys to `.env`.
- When ready, consider Tailwind CLI for a production CSS build.
- Add analytics (Plausible, GA4) via `<script/>` in `base.html`.

## Deploy options
- **Fly.io** (easy Docker, global); **Render.com**; **Railway.app**; or a small VPS.
- Add a Procfile or Dockerfile; point domain DNS (e.g., stevehof.com) to your host.

## Testing
```bash
poetry run pytest -q
```
