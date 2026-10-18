#!/usr/bin/env python3
"""
infra_hunter.py — INFRASTRUCTURE HUNTER executor for the 2026-10-16
slow passive swarm crawl.

Passive-only (GET reads of public pages/APIs). No POSTs, no brute force,
no scanning. Reuses swarm-infra-crawler.py + ip_classifier.py discovery
and classification pattern.

Lanes:
  A. Webhook inbox discovery via urlquery (fleet-tag cross-queries +
     broader Nov-2025+ window + alt inbox services), creator IP + UA
     from public token metadata, IP classified per ip_classifier.
  B. Tunnel subdomains in urlquery observations
     (*.trycloudflare.com, *.ngrok.io, *.loca.lt, *.bore.pub, Nov 2025+).
  C. Known ntfy topic read-only GET (document proxy block, do not fight).

Output: raw JSON per search + PROVENANCE.txt per file under
data/lanes/2026-10-16-slow-swarm-crawl/infra-hunter/raw/
"""

import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

HOME = os.path.expanduser("~")
WORKSPACE = os.path.join(HOME, "workspace")
RAW_DIR = os.path.join(
    WORKSPACE, "silent-locus/data/lanes/2026-10-16-slow-swarm-crawl/"
    "infra-hunter/raw")
CONFIG_PATH = os.path.join(
    WORKSPACE, "silent-locus/scripts/swarm-infra-config.json")
ASN_CACHE_PATH = os.path.join(
    WORKSPACE, "goals/urlquery-agent-activity-hunt/hidden_files/"
    "swarm-infra-asn-cache.json")
UQ_HTMX = os.path.join(WORKSPACE, "skills/urlquery/bin/uq_htmx.py")

sys.path.insert(0, os.path.join(WORKSPACE, "silent-locus/scripts"))
from ip_classifier import classify_ip, load_cache

DELAY_UQ = 4
DELAY_WS = 3
START = "2025-11-01"
END = "2026-10-16"

SEARCHES = [
    ("inbox_webhook_broad", "webhook.site date:[2025-11-01 TO 2026-10-16]", 2),
    ("inbox_webhook_uqscan", "webhook.site uqscan date:[2025-11-01 TO 2026-10-16]", 1),
    ("inbox_webhook_uqframe", "webhook.site uqframe date:[2025-11-01 TO 2026-10-16]", 1),
    ("inbox_postb", "postb.in date:[2025-11-01 TO 2026-10-16]", 1),
    ("inbox_beeceptor", "beeceptor.com date:[2025-11-01 TO 2026-10-16]", 1),
    ("inbox_pipedream", "m.pipedream.net date:[2025-11-01 TO 2026-10-16]", 1),
    ("tunnel_trycloudflare", "trycloudflare.com date:[2025-11-01 TO 2026-10-16]", 1),
    ("tunnel_ngrok", "ngrok.io date:[2025-11-01 TO 2026-10-16]", 1),
    ("tunnel_loca", "loca.lt date:[2025-11-01 TO 2026-10-16]", 1),
    ("tunnel_bore", "bore.pub date:[2025-11-01 TO 2026-10-16]", 1),
]

UUID_RE = re.compile(
    r"webhook\.site/(?:token/|#?!?/?)?"
    r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-"
    r"[a-f0-9]{4}-[a-f0-9]{12})", re.IGNORECASE)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def save_raw(name, payload, source_desc, method):
    os.makedirs(RAW_DIR, exist_ok=True)
    path = os.path.join(RAW_DIR, name)
    with open(path, "w") as f:
        json.dump(payload, f, indent=1)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    prov = (
        f"source: {source_desc}\n"
        f"retrieved_utc: {now}\n"
        f"method: {method}\n"
        f"sha256: {sha256(path)}\n")
    with open(path + ".PROVENANCE.txt", "w") as f:
        f.write(prov)
    return path


def uq_search(query, limit=48, offset=0):
    result = subprocess.run(
        [sys.executable, UQ_HTMX, "search", "--query", query,
         "--limit", str(limit), "--offset", str(offset)],
        capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        return {"transport_error": result.stderr[:300]}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return {"transport_error": f"bad json: {e}"}


def token_metadata(uuid):
    url = f"https://webhook.site/token/{uuid}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "swarm-infra-crawler/1.0 (research)",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"http": resp.status,
                    "data": json.loads(resp.read().decode("utf-8",
                                                          "replace"))}
    except urllib.error.HTTPError as e:
        return {"http": e.code, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": str(e)[:300]}


def main():
    config = json.load(open(CONFIG_PATH))
    cache = load_cache(ASN_CACHE_PATH)

    all_reports = {}
    print(f"infra_hunter run {datetime.datetime.now(datetime.timezone.utc).isoformat()}")
    for slug, query, pages in SEARCHES:
        merged = []
        transport_errors = []
        for page in range(pages):
            r = uq_search(query, limit=48, offset=page * 48)
            time.sleep(DELAY_UQ)
            if "transport_error" in r:
                transport_errors.append(r["transport_error"])
                continue
            reports = r.get("reports", [])
            merged.extend(reports)
            if len(reports) < 48:
                break
        save_raw(f"{slug}.json",
                 {"query": query, "retrieved_reports": merged,
                  "transport_errors": transport_errors},
                 f"urlquery htmx search API: {query}",
                 "python3 skills/urlquery/bin/uq_htmx.py search")
        print(f"  {slug}: {len(merged)} reports"
              f" ({'ERR: ' + '; '.join(transport_errors) if transport_errors else 'ok'})")
        for rep in merged:
            rid = rep.get("report_id") or rep.get("url", "")
            all_reports[rid] = rep

    # Extract inbox UUIDs
    inboxes = {}  # uuid -> source info
    for rid, rep in all_reports.items():
        url = rep.get("url", "")
        for m in UUID_RE.findall(url):
            inboxes.setdefault(m, []).append(
                {"report_id": rid, "url": url[:500]})

    # Also scan full report text fields that came back (tags etc.)
    for rid, rep in all_reports.items():
        blob = json.dumps(rep)
        for m in UUID_RE.findall(blob):
            inboxes.setdefault(m, []).append(
                {"report_id": rid, "url": rep.get("url", "")[:500]})

    print(f"\n{len(inboxes)} distinct inbox UUIDs harvested")
    save_raw("inbox_uuid_index.json",
             {"uuids": {u: v for u, v in inboxes.items()}},
             "derived from urlquery search results above",
             "regex extraction from cached search JSON")

    # Creator IP + UA extraction for each inbox (passive GET)
    extractions = []
    for i, uuid in enumerate(sorted(inboxes)):
        meta = token_metadata(uuid)
        time.sleep(DELAY_WS)
        rec = {"uuid": uuid, "sources": inboxes[uuid],
               "raw_response": meta}
        if meta.get("http") == 200 and isinstance(meta.get("data"), dict):
            d = meta["data"]
            cip = d.get("ip")
            rec["creator_ip"] = cip
            rec["creator_ua"] = d.get("user_agent")
            rec["created_at"] = d.get("created_at")
            if cip:
                rec["classification"] = classify_ip(
                    cip, config, ASN_CACHE_PATH)
        extractions.append(rec)
        print(f"  [{i+1}/{len(inboxes)}] {uuid[:8]}... -> "
              f"{meta.get('http', meta.get('error'))}")
    save_raw("creator_extractions.json",
             {"extractions": extractions},
             "GET https://webhook.site/token/<uuid> Accept: application/json",
             "urllib GET, one per inbox")

    # Known ntfy topic read-only check (expect proxy block)
    ntfy_topics = config.get("ntfy_topics", [])
    ntfy_results = []
    for topic in ntfy_topics:
        req = urllib.request.Request(f"https://ntfy.sh/{topic}",
                                     headers={"User-Agent":
                                              "infra-hunter/1.0 (research)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                ntfy_results.append(
                    {"topic": topic, "http": resp.status,
                     "body_head": resp.read(500).decode("utf-8",
                                                        "replace")})
        except Exception as e:
            ntfy_results.append({"topic": topic, "error": str(e)[:300]})
        print(f"  ntfy {topic}: {ntfy_results[-1].get('http', ntfy_results[-1].get('error'))}")
    save_raw("ntfy_check.json", {"results": ntfy_results},
             "https://ntfy.sh/<topic> (known topics only)",
             "urllib GET read-only")

    print(f"\nDone. Raw files in {RAW_DIR}")


if __name__ == "__main__":
    main()
