#!/usr/bin/env python3
"""Finalize the CDX sweep: merge analysis + novelty grades into summary.json,
write CDX-SWEEP-SUMMARY.md. Idempotent."""
import json, os, collections

OUT = os.path.dirname(os.path.abspath(__file__))

def load(slug):
    p = os.path.join(OUT, slug + ".cdx.json")
    if not os.path.exists(p):
        return []
    rows = json.load(open(p))
    if rows and rows[0] == ["timestamp", "original", "statuscode", "mimetype", "digest"]:
        rows = rows[1:]
    return rows

progress = json.load(open(os.path.join(OUT, "progress.json")))

GRADES = {
    "r.jina.ai_domain": "OVERLAP/noise — public jina-reader laundering + Cloudflare-challenge crawler bulk (Jul 29-30 burst). No fleet markers (no zz=/uqscan=/uuid-beacon shapes).",
    "api.allorigins.win_domain": "OVERLAP/noise — 1717 proxy invocations hit public dev-test hosts (postman-echo.com 559, www.boubinarena.cz 118, pump.fun 40). No fleet markers. Jun 16 day bump = crawl of allorigins' own site pages.",
    "pastebin.com_domain": "UNKNOWN — query failed (Wayback backend 503 'Temporarily Offline' on all 6 attempts across two runs). NOT a zero. Needs re-run.",
    "webhook.site_28efa24e-f830-4d9f-a12b-fbb9e5035031_exact": "real zero (expected: inbox created 2026-10-14, after the May-Jul window).",
    "ntfy.sh_c6836_prefix": "real zero — in-window.",
    "ntfy.sh_kz1wu398dnq_prefix": "NEW-candidate — 1 in-window 200 (2026-07-06 04:44:26 UTC); archived body carries beacon message START \"tomas kopecky\" \"six million dollar man\". Topic in inventory (OVERLAP on topic id); message content NEW to repo (grep of lists/data/lanes/evidence found no match). Factum match check pending.",
    "ntfy.sh_mha3x_prefix": "real zero — in-window.",
    "ntfy.sh_o54445_prefix": "NEW-candidate — 1 in-window 200 (2026-07-08 15:07:11 UTC); archived body carries single-char beacon message \"S\". Topic in inventory (OVERLAP on topic id); message content NEW to repo.",
    "ntfy.sh_pz4kopsh1_prefix": "NEW-candidate — 1 in-window 200 (2026-07-06 03:51:14 UTC); archived body carries timestamp beacon \"go|1783309874200\". Topic in inventory (OVERLAP on topic id); message content NEW to repo.",
    "jqp.vercel.app_api_prefix": "OVERLAP/noise — 4 generic relay invocations (yahoo finance chart, cofc library IIIF manifests, da.gd/4OzSm analysis). No fleet markers.",
    "hysandbox.tencent-cloud.com_domain": "real zero — in-window (confirms 2026-10-23 probe).",
    "pre-amap-pc-ssr.amap.com_prefix": "real zero — in-window (confirms 2026-10-23 probe).",
    "da.gd_domain": "OVERLAP/noise (Anthropic label) — 4069 rows collapse to 96 unique digests; burst days are Wayback bulk crawls of the public shortener's 302 redirect space. No attribution to agent use from CDX alone.",
}

BURSTS = {
    "r.jina.ai_domain": "2026-07-29 (153 rows) + 2026-07-30 (496 rows) vs ~25/day baseline; ~47% are cdn-cgi/challenge-platform URLs (403/200 CF challenge bounces) + favicon — crawler artifact, not agent signal.",
    "api.allorigins.win_domain": "2026-06-16 (104 rows) = crawl of allorigins' own site assets/pages (77x 403). Rest of window steady ~10-40/day dev-test invocations.",
    "da.gd_domain": "2026-05-16 (420 rows): 418 distinct short codes, all 302s, 2 unique digests — Wayback bulk crawl of the shortener URL space. May mid-month cluster (05-06..05-19) is the same crawl sweep, not a burst of agent activity.",
}

summary = {}
for slug, v in progress.items():
    s = v["stats"]
    rows = load(slug)
    day = collections.Counter(r[0][:8] for r in rows)
    summary[slug] = {
        "matchType": s["matchType"], "url": s["url"], "label": s["label"],
        "ok": v["ok"], "attempts": s["attempts"],
        "capture_rows": s["capture_rows"], "unique_digests": s["unique_digests"],
        "status2xx": s.get("status2xx", 0), "capped_20000": s.get("capped", False),
        "per_day": dict(sorted(day.items())),
        "first_ts": s.get("first_ts"), "last_ts": s.get("last_ts"),
        "burst_note": BURSTS.get(slug),
        "novelty_grade": GRADES[slug],
    }

json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
print("summary.json written,", len(summary), "targets")
