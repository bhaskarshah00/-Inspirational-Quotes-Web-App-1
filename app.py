import io
import os
import random
import time
from datetime import datetime
from typing import Dict, Any, Optional

import requests
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)

# ---------- Config ----------
REQUEST_TIMEOUT = 7  # seconds
USER_AGENT = "QuoteWave/1.1 (+https://example.com)"
HEADERS = {"User-Agent": USER_AGENT, "Accept": "application/json, text/plain;q=0.9,*/*;q=0.8"}

# External sources
RANDOM_SOURCES = [
    {"name": "zenquotes", "url": "https://zenquotes.io/api/random", "type": "zen"},
    {"name": "quotable",  "url": "https://api.quotable.io/random",  "type": "quotable"},
]
TODAY_SOURCES = [
    {"name": "zenquotes_today", "url": "https://zenquotes.io/api/today", "type": "zen_today"},
    {"name": "quotable",        "url": "https://api.quotable.io/random", "type": "quotable"},
]
IMAGE_SOURCES = [
    {"name": "zenquotes_image", "url": "https://zenquotes.io/api/image", "type": "zen_image"},
    {"name": "picsum",          "url": "https://picsum.photos/1200/700?nature", "type": "picsum"},
]

# Offline fallback quotes so UI always works even without internet
OFFLINE_QUOTES = [
    {"text": "Make it work, make it right, make it fast.", "author": "Kent Beck", "source": "offline"},
    {"text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman", "source": "offline"},
    {"text": "Whether you think you can or you think you can’t, you’re right.", "author": "Henry Ford", "source": "offline"},
    {"text": "Action is the foundational key to all success.", "author": "Pablo Picasso", "source": "offline"},
]

# Simple in-memory cache (last good result)
CACHE = {
    "random": None,  # type: Optional[Dict[str, Any]]
    "today": None,   # type: Optional[Dict[str, Any]]
}

# Session with basic retry behavior
SESSION = requests.Session()


def http_get(url: str, stream: bool = False) -> requests.Response:
    r = SESSION.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, stream=stream)
    r.raise_for_status()
    return r


def normalize_from_zen(data) -> Dict[str, Any]:
    # zenquotes returns a list of objects
    try:
        obj = data[0] if isinstance(data, list) and data else {}
        return {
            "text": obj.get("q") or obj.get("quote") or "",
            "author": obj.get("a") or obj.get("author") or "Unknown",
            "source": "zenquotes",
        }
    except Exception:
        return {"text": "", "author": "Unknown", "source": "zenquotes"}


def normalize_from_quotable(data) -> Dict[str, Any]:
    try:
        return {
            "text": data.get("content", ""),
            "author": data.get("author", "Unknown"),
            "source": "quotable",
        }
    except Exception:
        return {"text": "", "author": "Unknown", "source": "quotable"}


def try_sources(kind: str, preferred: Optional[str] = None) -> Dict[str, Any]:
    if kind == "random":
        sources = RANDOM_SOURCES[:]
    else:
        sources = TODAY_SOURCES[:]

    if preferred and preferred != "auto":
        sources = sorted(sources, key=lambda s: 0 if preferred in (s["name"], s["type"]) else 1)
    else:
        random.shuffle(sources)

    for src in sources:
        try:
            resp = http_get(src["url"])
            data = resp.json()
            if src["type"].startswith("zen"):
                # today uses same shape as random
                norm = normalize_from_zen(data)
            else:
                norm = normalize_from_quotable(data)
            if norm.get("text"):
                payload = {
                    "ok": True,
                    "quote": norm,
                    "fetched_at": datetime.utcnow().isoformat() + "Z",
                    "provider": src["name"],
                }
                CACHE[kind] = payload
                return payload
        except Exception:
            continue

    # If everything failed, use cache or offline
    if CACHE.get(kind):
        return {**CACHE[kind], "ok": True, "cached": True}
    fallback = random.choice(OFFLINE_QUOTES)
    return {
        "ok": True,
        "quote": fallback,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "provider": "offline",
        "offline": True,
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/api/random")
def api_random():
    preferred = request.args.get("source")
    return jsonify(try_sources("random", preferred))


@app.get("/api/today")
def api_today():
    preferred = request.args.get("source")
    return jsonify(try_sources("today", preferred))


@app.get("/api/image")
def api_image():
    # Proxy the image BYTES to avoid hotlink/CORS/403 issues.
    preferred = request.args.get("source", "auto")
    sources = IMAGE_SOURCES[:]
    if preferred and preferred != "auto":
        sources = sorted(sources, key=lambda s: 0 if preferred in (s["name"], s["type"]) else 1)
    else:
        random.shuffle(sources)

    for src in sources:
        try:
            resp = http_get(src["url"], stream=True)
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            data = resp.content  # small enough for memory
            return send_file(io.BytesIO(data), mimetype=content_type)
        except Exception:
            continue

    # Offline 1x1 PNG placeholder
    placeholder = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10'
        b'\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x0cIDATx\x9cc````\x00\x00'
        b'\x00\x06\x00\x03\xc3\x0c\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    return send_file(io.BytesIO(placeholder), mimetype="image/png")


@app.get("/health")
def health():
    return {"status": "ok", "time": time.time()}


@app.get("/api/debug")
def debug():
    return {
        "cache_keys": {k: bool(v) for k, v in CACHE.items()},
        "random_sources": [s["name"] for s in RANDOM_SOURCES],
        "today_sources": [s["name"] for s in TODAY_SOURCES],
        "image_sources": [s["name"] for s in IMAGE_SOURCES],
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
