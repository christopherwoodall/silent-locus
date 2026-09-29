#!/usr/bin/env python3
"""Build the university-shorteners-batch2 dataset (lane Q, batch 2).

Batch 2 covers NEW venues only (batch 1's data/2026-09-28-university-shorteners/
is untouched). One verifiable hit: goto.unm.edu/vbudg+ (5th public stats
page at the known-hit UNM venue — a control: 4 hits, zero agent markers).
The rest are documented clean negatives (login walls, 403s, dead hosts,
no public stats surfaces).

Reads a small in-repo evidence spec, writes evidence text files +
events.jsonl + SHA256SUMS + PROVENANCE.md, then
prints a manifest for ES ingest.

Usage: python3 build_dataset.py
"""
import json, hashlib, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TS = "2026-09-28T09:05:00Z"  # ~04:05 CDT

VBUDG_EVIDENCE = """SOURCE: https://goto.unm.edu/vbudg+
RETRIEVED: 2026-09-28 ~04:05 CDT via read-only GET (single page fetch)

Short URL: https://goto.unm.edu/vbudg
Long URL: https://go-unm.my.salesforce-sites.com/events/targetX_eventsb__events#/esr?eid=a12TO000008O2H3YAK (UNM events)

CREATED: March 26, 2025 @ 10:33 am
TRAFFIC: last 24h 0 hits; last 7d 4 hits; last 30d 4 hits; ALL TIME 4 hits (0.01/day)
BEST DAY: 2 hits on March 27, 2025 (daily series: Mar 27: 2, Mar 28: 1, Apr 01: 1)
LOCATION: US: 4 (all)

REFERRERS (1 referrer hit / 3 direct):
goto.unm.edu (via /admin/): 1

ANALYSIS: control page — the 5th public goto.unm.edu stats page (matches
joshuadavid/wikiagentswarminvestigation's 5 goto-unm slugs; batch 1 had 4).
4 hits over a week in March 2025, one internal referrer, ZERO agent-toolkit
markers and no task-family referrers. Agent traffic at this venue is
concentrated on specific slugs (7t6-o, discvr, reso, urphy21), not uniform.
"""

NEGATIVES = {
    "negative-probes/goto-ucr-edu_stats-login-walled_2026-09-28.txt": """VENUE: goto.ucr.edu (UC Riverside — NEW university YOURLS)
FOUND: https://goto.ucr.edu/ returns 200, meta generator "YOURLS 1.10.4"
(public front page live)
PROBE: https://goto.ucr.edu/KB0011332+ (slug from UCR's public ITS docs) -> 200
  with <title>Login — YOURLS</title>, <h1> login form. Stats pages are
  login-walled (instance policy), not publicly readable.
NOTE: non-'+' probes of other public slugs (PhishAlarm, wepasurvey) returned
  403 Forbidden (WAF). No link creation attempted (read-only).
VERDICT: clean negative — instance exists but offers no public stats surface.
""",
    "negative-probes/lnk-mcla-edu_403_2026-09-28.txt": """VENUE: lnk.mcla.edu (Massachusetts College of Liberal Arts YOURLS)
FOUND: docs at techhelp.mcla.edu confirm YOURLS at https://lnk.mcla.edu/
  (login via MCLA account required for shortening + stats)
PROBE: https://lnk.mcla.edu/ -> 403 Forbidden (campus firewall / IP restriction)
VERDICT: clean negative — inaccessible from the public internet; no bypass attempted.
""",
    "negative-probes/mlc-wels-edu_not-a-shortener_2026-09-28.txt": """VENUE: mlc-wels.edu (appeared on a public URL-shortener blocklist)
PROBE: https://mlc-wels.edu/ -> 200, Martin Luther College homepage (WELS College of Ministry).
  No shortener on this host.
VERDICT: negative — mislisted; not a shortener.
""",
    "negative-probes/go-aim-edu_403_2026-09-28.txt": """VENUE: go.aim.edu (appeared on a public URL-shortener blocklist)
PROBE: https://go.aim.edu/ -> 403 Forbidden (title only, 276 bytes)
VERDICT: clean negative — inaccessible; no public stats surface visible.
""",
    "negative-probes/da-gd_no-stats-surface_2026-09-28.txt": """VENUE: da.gd (community shortener; 54 hits as a REFERRER on goto.unm.edu/7t6-o)
PROBE: https://da.gd/ -> 200. It is a multipurpose URL utility with commands
  /help /ua /ip /w/<domain> /up/<site> /host /headers /dns /roll /status — a
  Swiss-army probe tool, not just a shortener.
VERDICT: no public per-link stats/referrer surface. Clean negative for the
  stats-page technique. (da.gd remains relevant as a cross-venue link format:
  agents point vanderbi.lt aliases at da.gd/coshorten/SECcountyM.)
""",
    "negative-probes/is-gd_403_2026-09-28.txt": """VENUE: is.gd (community shortener; 7 hits as referrer on goto.unm.edu/7t6-o)
PROBE: https://is.gd/ -> 403 for a non-browser user agent (blocks curl)
VERDICT: no public per-link stats surface is documented; none found. Negative.
""",
    "negative-probes/2dd-pl_cf-challenge_2026-09-28.txt": """VENUE: 2dd.pl (Polish community shortener; 45 hits as referrer on goto.unm.edu/7t6-o)
PROBE: https://2dd.pl/ -> 200 with <title>One moment, please...</title> —
  Cloudflare challenge wall.
VERDICT: clean negative — inaccessible; no bypass attempted.
""",
    "negative-probes/fooabc-com_dns-dead_2026-09-28.txt": """VENUE: fooabc.com (community shortener; 11 hits as referrer on goto.unm.edu/7t6-o)
PROBE: https://fooabc.com/ -> DNS resolution failure (exit 000)
VERDICT: negative — host is dead.
""",
}

PROVENANCE = """# PROVENANCE — university-shorteners-batch2 dataset

## Scope

Batch 2 (lane Q, 2026-09-28) sweeps NEW venues only — batch 1's
data/2026-09-28-university-shorteners/ is untouched. Source of candidates: (1) a new
goto.unm.edu slug (`vbudg+`) surfaced via search-engine index of UNM's public
stats pages; (2) new university YOURLS candidates from web search
(`goto.ucr.edu`, `lnk.mcla.edu`); (3) referrer-surfaced community shorteners
from batch 1 (`da.gd`, `is.gd`, `2dd.pl`, `fooabc.com`); (4) two more
edu-domain candidates from a public URL-shortener blocklist
(`mlc-wels.edu`, `go.aim.edu`). Community YOURLS already swept by
brausepulver/collusion-wiki-link-shorteners (yourls.space, yourls.biz,
hko.nu, yourls.pro, ns3.dnscores.com, IP-nip.io hosts) are saturated ground
and were NOT re-swept.

## Method (read-only, passive)

- Direct GETs only to public read endpoints: per-link `+` stats pages and
  front pages.
- Never: shortening/action/API-write endpoints, logins, form submissions,
  counter increments, mass target fetching, challenge solving.
- Login-walled `+` stats (goto.ucr.edu, per instance policy) were recorded
  and not bypassed. 403/Cloudflare/DNS-dead hosts recorded as-is.
- Slug sources: search-engine-indexed `+` pages and UCR's own public ITS
  documentation (KB0011332). No slugs were guessed.

## Contents

- `goto-unm-edu/vbudg_stats_2026-09-28.txt` — the one verifiable hit
  (control page; 4 hits, no agent markers).
- `negative-probes/*.txt` — 8 documented negatives.
- `events.jsonl` — 1 Elastic-ready doc (the vbudg hit).
- `SHA256SUMS` — checksums of every file above.
- `progress.log` — resumable run log.

## Elastic

Index `university-shorteners-batch2`, canonical shared schema
(notes/gems-es-mapping.json), `labels.shortener.scope` distinguishes
university vs community. Negatives are documented here and in the notes
report, not in Elastic (same convention as batch 1).

## Guards honored

Read-only research only. No submissions/uploads/accounts/logins/posts/
counter increments/payload execution. Agents/infrastructure traces only —
no operator identity, registrant details, or person-focused attribution.
No credentials reproduced. No absolute home-directory paths in logs/docs.
"""


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    os.makedirs(os.path.join(BASE, "goto-unm-edu"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "negative-probes"), exist_ok=True)

    ev_path = os.path.join(BASE, "goto-unm-edu", "vbudg_stats_2026-09-28.txt")
    with open(ev_path, "w") as f:
        f.write(VBUDG_EVIDENCE)
    ev_sha = sha256(ev_path)
    ev_size = os.path.getsize(ev_path)

    for rel, text in sorted(NEGATIVES.items()):
        p = os.path.join(BASE, rel)
        with open(p, "w") as f:
            f.write(text)

    with open(os.path.join(BASE, "PROVENANCE.md"), "w") as f:
        f.write(PROVENANCE)

    doc = {
        "@timestamp": TS,
        "description": "Public yourls_stats_page on goto.unm.edu (University of New Mexico): https://goto.unm.edu/vbudg -> https://go-unm.my.salesforce-sites.com/events/targetX_eventsb__events#/esr?eid=a12TO000008O2H3YAK (UNM events) — CONTROL: 4 hits total, no agent markers",
        "event": {"created": TS, "dataset": "university-shorteners-batch2"},
        "file": "goto-unm-edu/vbudg_stats_2026-09-28.txt",
        "labels": {
            "long_url": "https://go-unm.my.salesforce-sites.com/events/targetX_eventsb__events#/esr?eid=a12TO000008O2H3YAK (UNM events)",
            "pattern_families": {
                "cross_venue": ["goto.unm.edu"],
                "liveness_param": [],
                "proxy_wrapper": [],
                "task_family": [],
            },
            "referrers": {"goto.unm.edu": 1},
            "short_url": "https://goto.unm.edu/vbudg",
            "shortener.instance": "goto.unm.edu",
            "shortener.org": "University of New Mexico",
            "shortener.scope": "university",
        },
        "matched_string": "https://goto.unm.edu/vbudg",
        "note": "Control page: public stats but only 4 hits (Mar 26-Apr 1 2025), one internal referrer, zero agent-toolkit/task-family markers. Shows agent traffic at this venue concentrates on specific slugs.",
        "observer": {"product": "muse", "type": "research-agent", "vendor": "meta"},
        "record_kind": "yourls_stats_page",
        "retrieved_at": TS,
        "retrieved_via": "read-only page-text fetch",
        "sha256": ev_sha,
        "size_bytes": ev_size,
        "source_url": "https://goto.unm.edu/vbudg+",
        "status": "live",
        "tags": ["yourls", "public-stats", "scope:university", "read-only",
                 "status:live", "control:no-agent-markers"],
    }
    jpath = os.path.join(BASE, "events.jsonl")
    with open(jpath, "w") as f:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    log = os.path.join(BASE, "progress.log")
    with open(log, "w") as f:
        f.write("[2026-09-28T09:05Z] LANE Q batch2 start: new venues only.\n")
        f.write("[2026-09-28T09:05Z] HIT (control): goto.unm.edu/vbudg+ live — 4 hits, 1 internal referrer, zero agent markers. Saved.\n")
        f.write("[2026-09-28T09:05Z] NEGATIVE: goto.ucr.edu YOURLS 1.10.4 front page live, but slug+ stats redirect to login — private. Recorded.\n")
        f.write("[2026-09-28T09:05Z] NEGATIVE: lnk.mcla.edu -> 403 (campus firewall). mlc-wels.edu -> not a shortener (college homepage). go.aim.edu -> 403. Recorded.\n")
        f.write("[2026-09-28T09:05Z] NEGATIVE: da.gd -> multipurpose URL utility, no per-link stats surface. is.gd -> 403 for curl UA. 2dd.pl -> Cloudflare challenge. fooabc.com -> DNS dead. Recorded.\n")
        f.write("[2026-09-28T09:05Z] DATASET BUILT: 1 evidence + 8 negative-probe files + jsonl (1 doc) + PROVENANCE.md + SHA256SUMS.\n")

    sums = []
    for root, _, files in os.walk(BASE):
        for fn in sorted(files):
            if fn in ("SHA256SUMS", "build_dataset.py"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, BASE)
            sums.append("%s  %s" % (sha256(p), rel))
    with open(os.path.join(BASE, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sorted(sums)) + "\n")

    print("files:", len(sums), "| jsonl docs: 1 | evidence sha:", ev_sha[:16])


if __name__ == "__main__":
    main()
