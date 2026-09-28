#!/usr/bin/env python3
"""Build the university-shorteners dataset: pattern sweep + normalized JSONL + manifest."""
import json, re, hashlib, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent
EVIDENCE = {
    "u-ethz-ch/nB1nv_stats_2026-09-28.txt": {
        "instance": "u.ethz.ch", "org": "ETH Zürich", "kind": "yourls_stats_page",
        "short_url": "https://u.ethz.ch/nB1nv",
        "long_url": "https://eth4d.ethz.ch/news-and-events/eth4d-news/2020/0[...] (ETH for Development / Pioneer Fellowship)",
        "source_url": "https://u.ethz.ch/nB1nv+?jqpaccess=1", "scope": "university",
    },
    "goto-unm-edu/7t6-o_stats_2026-09-28.txt": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_page",
        "short_url": "https://goto.unm.edu/7t6-o",
        "long_url": "https://unmanderson.secure.force.com/events/targetX_eventsb__events#/esr?eid=a128W000006no0jQAA",
        "source_url": "https://goto.unm.edu/7t6-o+", "scope": "university",
    },
    "goto-unm-edu/discvr_stats_2026-09-28.txt": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_page",
        "short_url": "https://goto.unm.edu/discvr",
        "long_url": "https://library.unm.edu/services/disc.php#tab5 (DISC VR Page)",
        "source_url": "https://goto.unm.edu/discvr+", "scope": "university",
    },
    "goto-unm-edu/reso_stats_2026-09-28.txt": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_page",
        "short_url": "https://goto.unm.edu/reso",
        "long_url": "https://sust.unm.edu/news/2021/10/a-review-of-resolutio[...] (ASUNM resolutions)",
        "source_url": "https://goto.unm.edu/reso+", "scope": "university",
    },
    "goto-unm-edu/urphy21_stats_2026-09-28.txt": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_page",
        "short_url": "https://goto.unm.edu/urphy21",
        "long_url": "https://unm.zoom.us/meeting/register/tJUvd-CqrT4qHN08Xs[...] (Zoom registration)",
        "source_url": "https://goto.unm.edu/urphy21+", "scope": "university",
    },
    "url-popcat-xyz/5vtSk2RG2f_info_2026-09-28.txt": {
        "instance": "url.popcat.xyz", "org": "popcat.xyz community", "kind": "shortener_info_page",
        "short_url": "https://url.popcat.xyz/5vtSk2RG2f",
        "long_url": "https://chatgpt.com/c/69da0686-9680-8321-ae7c-4aafe7e3f2f4",
        "source_url": "https://url.popcat.xyz/5vtSk2RG2f/info", "scope": "community",
    },
    "url-popcat-xyz/IRZTIxDlZ_info_2026-09-28.txt": {
        "instance": "url.popcat.xyz", "org": "popcat.xyz community", "kind": "shortener_info_page",
        "short_url": "https://url.popcat.xyz/IRZTIxDlZ",
        "long_url": "https://chatgpt.com/c/69da0686-9680-8321-ae7c-4aafe7e3f2f4",
        "source_url": "https://url.popcat.xyz/IRZTIxDlZ/info", "scope": "community",
    },
    "goto-unm-edu/7t6-o_referrer_urls_daily_2026-09-28.json": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_detail",
        "short_url": "https://goto.unm.edu/7t6-o#detail-2026-09-28",
        "long_url": "per-slug full referrer-URL table + daily traffic series",
        "source_url": "https://goto.unm.edu/7t6-o+", "scope": "university", "json_evidence": True,
    },
    "goto-unm-edu/discvr_referrer_urls_daily_2026-09-28.json": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_detail",
        "short_url": "https://goto.unm.edu/discvr#detail-2026-09-28",
        "long_url": "per-slug full referrer-URL table + daily traffic series",
        "source_url": "https://goto.unm.edu/discvr+", "scope": "university", "json_evidence": True,
    },
    "goto-unm-edu/reso_referrer_urls_daily_2026-09-28.json": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_detail",
        "short_url": "https://goto.unm.edu/reso#detail-2026-09-28",
        "long_url": "per-slug full referrer-URL table + daily traffic series",
        "source_url": "https://goto.unm.edu/reso+", "scope": "university", "json_evidence": True,
    },
    "goto-unm-edu/urphy21_referrer_urls_daily_2026-09-28.json": {
        "instance": "goto.unm.edu", "org": "University of New Mexico", "kind": "yourls_stats_detail",
        "short_url": "https://goto.unm.edu/urphy21#detail-2026-09-28",
        "long_url": "per-slug full referrer-URL table + daily traffic series",
        "source_url": "https://goto.unm.edu/urphy21+", "scope": "university", "json_evidence": True,
    },
}

PATTERNS = {
    "proxy_wrapper": [r"jqp", r"md\.succ\.ai", r"allorigins", r"proxymule", r"pure\.md",
                      r"corsmirror", r"markdown\.new", r"microlink", r"corsproxy", r"cors\.sh",
                      r"cors\.bwa", r"r\.jina\.ai"],
    "epoch_nonce": [r"\b\d{10}\b"],
    "generated_grammar": [r"\bzz\w+", r"\boai\w+", r"tryzz", r"\bamass\d+", r"maagent\w+",
                          r"mafresh\d+", r"zzagent\d+"],
    "task_family": [r"sec\.gov", r"investor\.gov", r"county\.json", r"census\.gov",
                    r"datausa", r"pxweb", r"nso\.gov\.vn", r"gso\.gov\.vn"],
    "liveness_param": [r"dummyagent", r"jqpaccess"],
    "cross_venue": [r"vanderbi\.lt", r"uoft\.me", r"goto\.unm\.edu", r"u\.ethz\.ch",
                    r"da\.gd", r"is\.gd", r"2dd\.pl", r"jsonhero"],
}

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
docs, manifest_lines, sweep_report = [], [], []

for rel, meta in EVIDENCE.items():
    p = ROOT / rel
    raw = p.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    manifest_lines.append(f"{sha}  {rel}")
    text = raw.decode("utf-8", errors="replace")

    fam_hits = {}
    for fam, pats in PATTERNS.items():
        hits = set()
        for pat in pats:
            hits.update(m.group(0) for m in re.finditer(pat, text, re.IGNORECASE))
        if hits:
            fam_hits[fam] = sorted(hits)
    sweep_report.append({"file": rel, "pattern_families": fam_hits})

    referrers = {}
    for m in re.finditer(r"^([a-z0-9][a-z0-9.\-]*\.[a-z]{2,}):\s*(\d+)$", text, re.M | re.I):
        referrers[m.group(1).lower()] = int(m.group(2))

    labels_extra = {}
    desc = (f"Public {meta['kind']} on {meta['instance']} ({meta['org']}): "
            f"{meta['short_url']} -> {meta['long_url']}")
    retrieved_via = "read-only page-text fetch"
    if meta.get("json_evidence"):
        ev = json.loads(text)
        hosts = ev.get("referrer_hosts", [])
        nurls = sum(h.get("url_count", 0) for h in hosts)
        flat_urls = []
        for h in hosts:
            for u in h.get("urls", []):
                flat_urls.append({"host": h["host"], "url": u["url"], "hits": u["hits"]})
        labels_extra = {
            "referrer_url_count": str(nurls),
            "referrer_urls": flat_urls,
            "daily_all_time": ev.get("daily_all_time", []),
            "daily_last_30": ev.get("daily_last_30", []),
            "traffic_summary": ev.get("traffic_summary", {}),
            "best_day": ev.get("best_day") or {},
        }
        desc = (f"YOURLS public stats detail for {meta['short_url']}: "
                f"{nurls} full per-URL referrer rows across {len(hosts)} hosts, "
                f"all-time decimated daily series ({len(ev.get('daily_all_time', []))} points), "
                f"last-30d daily series. Credential-like query values redacted. "
                f"Source: {meta['source_url']}.")
        retrieved_via = "read-only raw HTML fetch + offline parse"

    doc = {
        "@timestamp": now,
        "event": {"dataset": "university-shorteners", "created": now},
        "record_kind": meta["kind"],
        "status": "live",
        "source_url": meta["source_url"],
        "retrieved_at": now,
        "retrieved_via": retrieved_via,
        "sha256": sha,
        "size_bytes": len(raw),
        "file": rel,
        "matched_string": meta["short_url"],
        "description": desc,
        "tags": ["yourls", "public-stats", f"scope:{meta['scope']}", "agent-toolkit-referrers",
                 "read-only", "status:live"],
        "labels": {
            "shortener.instance": meta["instance"],
            "shortener.org": meta["org"],
            "shortener.scope": meta["scope"],
            "short_url": meta["short_url"],
            "long_url": meta["long_url"],
            "referrers": referrers,
            "pattern_families": fam_hits,
            **labels_extra,
        },
        "note": "Agent proxy-wrapper toolkit + task-family referrers logged verbatim by YOURLS on official university/community infrastructure. See PROVENANCE.md.",
        "observer": {"product": "muse", "type": "research-agent", "vendor": "meta"},
    }
    docs.append(doc)

with open(ROOT / "university-shorteners.jsonl", "w") as f:
    for d in docs:
        f.write(json.dumps(d, sort_keys=True) + "\n")
with open(ROOT / "SHA256SUMS", "w") as f:
    f.write("\n".join(manifest_lines) + "\n")
with open(ROOT / "pattern-sweep.json", "w") as f:
    json.dump(sweep_report, f, indent=2, sort_keys=True)

fam_totals = {}
for s in sweep_report:
    for fam, hits in s["pattern_families"].items():
        fam_totals.setdefault(fam, set()).update(hits)
print(f"docs={len(docs)}")
for fam in sorted(fam_totals):
    print(f"{fam}: {len(fam_totals[fam])} distinct -> {sorted(fam_totals[fam])[:12]}")
