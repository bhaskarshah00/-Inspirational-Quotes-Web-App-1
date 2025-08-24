# QuoteWave (Fixed)

- Robust backend with retries and **offline fallback** quotes.
- **Image proxy**: backend streams image bytes to avoid CORS/403 and broken images.
- Works even when external APIs are down (placeholder image + offline quotes).

## Run locally
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py  # open http://127.0.0.1:5000
```

## Useful endpoints
- `/api/random`  `/api/today`  → JSON (always returns something)
- `/api/image`   → image bytes (safe to use directly as <img src>)
- `/api/debug`   → quick status
- `/health`      → ok

## Deploy
Use `gunicorn` with the provided Procfile on Render/Heroku or run `gunicorn app:app` on your server.
