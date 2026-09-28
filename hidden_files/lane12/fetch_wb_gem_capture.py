#!/usr/bin/env python3
"""Lane12 follow-up: fetch the single Wayback HIT read-only.

Capture: https://web.archive.org/web/20260810004952id_/https://rubygems.org/gems/zztargettest18587
(id_ suffix requests original response bytes without Wayback toolbar rewriting.)

Saves:
  data/wayback-gem-capture/wb_rubygems-org_gems_zztargettest18587_20260810004952.id.html  (id_ replay)
  data/wayback-gem-capture/wb_rubygems-org_gems_zztargettest18587_20260810004952.html      (plain replay fallback)
  data/wayback-gem-capture/fetch_meta.json  (statuses, headers, timestamps, sizes)

Read-only: no credentials, no submissions. Parses only; nothing executed.
"""
import json, sys, urllib.request, urllib.error, datetime, hashlib, os

LANE = os.path.join("data", "wayback-gem-capture")
TARGET = "https://rubygems.org/gems/zztargettest18587"
TS = "20260810004952"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "silent-locus-research/1.0 (read-only research; contact via repo)"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.status, dict(resp.getheaders()), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers.items()), e.read()

def main():
    os.makedirs(LANE, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {"fetched_at_utc": now, "target": TARGET, "capture_ts": TS, "attempts": []}
    out_id = os.path.join(LANE, f"wb_rubygems-org_gems_zztargettest18587_{TS}.id.html")
    out_plain = os.path.join(LANE, f"wb_rubygems-org_gems_zztargettest18587_{TS}.html")

    id_url = f"https://web.archive.org/web/{TS}id_/{TARGET}"
    status, headers, body = fetch(id_url)
    meta["attempts"].append({
        "url": id_url, "status": status,
        "content_type": headers.get("Content-Type"),
        "content_length_hdr": headers.get("Content-Length"),
        "bytes": len(body or b""),
    })
    if body and status in (200,):
        with open(out_id, "wb") as f:
            f.write(body)
    else:
        plain_url = f"https://web.archive.org/web/{TS}/{TARGET}"
        status2, headers2, body2 = fetch(plain_url)
        meta["attempts"].append({
            "url": plain_url, "status": status2,
            "content_type": headers2.get("Content-Type"),
            "content_length_hdr": headers2.get("Content-Length"),
            "bytes": len(body2 or b""),
        })
        if body2 and status2 in (200,):
            with open(out_plain, "wb") as f:
                f.write(body2)
        else:
            meta["verdict"] = "fetch_failed"

    meta["verdict"] = meta.get("verdict") or "captured"
    with open(os.path.join(LANE, "fetch_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
