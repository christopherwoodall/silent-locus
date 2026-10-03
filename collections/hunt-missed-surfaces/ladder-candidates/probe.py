#!/usr/bin/env python3
"""Read-only curl probes of 5 ladder-candidate relay/proxy surfaces.

Surfaces: jqp.vercel.app, bitily.in (/admin), s.jina.ai, exa.ai, tinyurl.com.
No accounts, no API keys, no content-creating submissions. The single live
fetch through jqp's proxy is a read-only GET of a public government JSON
file (the SEC incident target) to verify the documented URL grammar.
Idempotent: results keyed by probe name in state.json; reruns skip done.
Polite pacing: 2s between requests. Every request logged to data/probe-log.jsonl.
"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STATE = ROOT / "state.json"
LOG = DATA / "probe-log.jsonl"

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return {"http": r.status, "bytes": len(body),
                    "body": body.decode("utf-8", errors="replace"), "error": None}
    except Exception as e:
        code = getattr(e, "code", None)
        return {"http": code, "bytes": 0, "body": "", "error": str(e)[:160]}

def text_of(body):
    t = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", t)

PROBES = [
    # --- jqp.vercel.app: server-side jq fetch proxy ---
    ("jqp-home", "https://jqp.vercel.app/"),
    ("jqp-readme", "https://raw.githubusercontent.com/sighrobot/jqp/main/README.md"),
    ("jqp-api-noparams", "https://jqp.vercel.app/api/v0"),
    ("jqp-api-history", "https://jqp.vercel.app/api/history"),
    ("jqp-history", "https://jqp.vercel.app/history"),
    ("jqp-recent", "https://jqp.vercel.app/recent"),
    ("jqp-api-recent", "https://jqp.vercel.app/api/recent"),
    ("jqp-gallery", "https://jqp.vercel.app/gallery"),
    # live grammar verification: one read-only fetch of the SEC incident target
    ("jqp-grammar-sec", "https://jqp.vercel.app/api/v0?url="
     + urllib.parse.quote("https://www.sec.gov/files/county.json", safe="")
     + "&jq=" + urllib.parse.quote("keys", safe="")),
    # --- bitily.in: YOURLS shortener, /admin reportedly searchable ---
    ("bitily-admin", "https://bitily.in/admin"),
    ("bitily-root", "https://bitily.in/"),
    ("bitily-mylabi", "https://bitily.in/MYLABI/"),
    # --- s.jina.ai: Jina search API ---
    ("sjina-root", "https://s.jina.ai/"),
    ("jina-reader", "https://jina.ai/reader"),
    # --- Exa (exa.ai): commercial search/fetch ---
    ("exa-home", "https://exa.ai/"),
    ("exa-search", "https://exa.ai/search"),
    ("exa-recent", "https://exa.ai/recent"),
    ("exa-trending", "https://exa.ai/trending"),
    ("exa-playground", "https://exa.ai/playground"),
    # --- tinyurl.com: shortener ---
    ("tinyurl-home", "https://tinyurl.com/"),
]

def analyze(name, url, res):
    body, sig = res["body"], {}
    t = text_of(body).lower()
    if name.startswith("jqp"):
        sig["is_proxy"] = "serverless proxy" in t or "jq-web" in t
        sig["history_endpoint"] = res["http"] not in (404,) and "history" in name
        sig["login_form"] = "password" in t and "log in" in t
        if name == "jqp-grammar-sec":
            sig["grammar_works"] = res["http"] == 200 and body.strip().startswith("[")
            sig["preview"] = body[:120]
        if name == "jqp-home":
            sig["public_listing_hint"] = any(k in t for k in ["history", "recent queries", "gallery"])
    elif name.startswith("bitily"):
        sig["login_gated"] = "please log in" in t
        sig["is_yourls"] = "yourls" in t
        sig["lists_links"] = "long url" in t and "short url" in t and "clicks" in t
    elif name in ("sjina-root",):
        sig["key_required"] = "authentication is required" in t or "api key" in t
        sig["publishes_queries"] = any(k in t for k in ["trending queries", "recent searches", "query log", "public log"])
    elif name == "jina-reader":
        sig["publishes_queries"] = any(k in t for k in ["recent searches", "query log", "public log", "trending queries"])
    elif name.startswith("exa"):
        sig["history_login_gated"] = "sign in to see your history" in t
        sig["publishes_telemetry"] = any(k in t for k in ["public log", "query log", "recent searches"])
    elif name.startswith("tinyurl"):
        sig["recent_listing"] = any(k in t for k in ["recent links", "latest links", "public links", "link directory"])
    return sig

def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for name, url in PROBES:
        if name in state and state[name].get("done"):
            print(f"skip {name} (done)")
            continue
        res = get(url)
        rec = {"name": name, "url": url, "done": True,
               "http": res["http"], "bytes": res["bytes"], "error": res["error"],
               "signals": analyze(name, url, res)}
        state[name] = rec
        with LOG.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
        print(f"{name}: http={res['http']} bytes={res['bytes']} {json.dumps(rec['signals'])[:160]}")
        time.sleep(2)
    print("done.")

if __name__ == "__main__":
    main()
