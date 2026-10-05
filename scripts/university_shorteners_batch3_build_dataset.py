#!/usr/bin/env python3
"""Build the university-shorteners-batch3 dataset (workstream B lane, 2026-09-28).

Batch 3 covers NEW venues only (batches 1 and 2 untouched).

HIT: go.uvm.edu (University of Vermont) — live YOURLS 1.10.3 with public
per-link `+` stats pages and search-engine-indexed `~` preview pages. Two
indexed preview slugs (-4s0q, tgmtq) + the freshest doc-sourced slug (xc26,
created 2026-09-24) probed live. Zero agent-toolkit markers on any
page. IMPORTANT CAVEAT: go.uvm.edu's PUBLIC stats expose traffic statistics
and traffic LOCATION only — the "Traffic Sources" (referrers) section from
UVM's KB is owner-only (visible after NetID/Duo login at /admin). So this
venue cannot leak the proxy-wrapper referrer fingerprint; it is recorded as
a control / public-stats venue, not a fingerprint hit.

NEGATIVES: go.sjf.edu (shortener retired, 302 -> www.sjf.edu homepage),
s.wnmu.edu (DNS dead), linktest.lse.ac.uk (403), test.yourls.org (connection
failed), 1aas.com (YOURLS live but `+` stats login-walled).

Writes evidence files + events.jsonl (3 docs) +
pattern-sweep.json + PROVENANCE.md + SHA256SUMS + progress.log.

Usage: python3 build_dataset.py
"""
import json, hashlib, os

BASE = os.path.dirname(os.path.abspath(__file__))
TS = "2026-09-28T11:45:00Z"  # ~06:45 CDT

EVIDENCE = {
    "go-uvm-edu/-4s0q_stats_2026-09-28.txt": """SOURCE: https://go.uvm.edu/-4s0q+
RETRIEVED: 2026-09-28 ~06:40 CDT via read-only GET (single page fetch)
ALSO INDEXED: http://go.uvm.edu/-4s0q~ (search-engine-indexed YOURLS preview page)

Short URL: https://go.uvm.edu/-4s0q
Long URL: http://proquest.safaribooksonline.com/book/operating-systems/9780735669635/ddot-moving-your-data-and-settings-to-windows-8/transferring_your_data_to_windows_8_with_html (Safari Books Online, Windows 8 book)
Software: Powered by YOURLS v 1.10.3

CREATED: October 18, 2013 @ 8:40 am
TRAFFIC: last 24h 0 hits; last 7d 0 hits; last 30d 3 hits; ALL TIME 266 hits
BEST DAY: 4 hits on October 18, 2013 (creation day)
LOCATION: US: 131, CA: 30, MD: 26, CN: 15, SA: 13, DE: 10, RU: 6, ...
REFERRERS: NOT exposed on the public stats page (UVM instance hides
  "Traffic Sources" from anonymous viewers; owner-only per UVM KB article
  url-shortener-go-uvm-edu, updated 2026-04-09).

PATTERN SWEEP: zero proxy-wrapper markers (jqp/pure.md/md.succ.ai/r.jina.ai/
  allorigins/corsproxy/cors.bwa/markdown.new/proxymule), zero task-family
  markers (sec.gov/api.census.gov/api.datausa.io/pxweb/tableau), zero
  10-digit epoch nonces, zero zz/oai/tryzz agent grammars.

ANALYSIS: control page — a 2013 UVM library link whose traffic is flat
organic decay (3 hits/30d). Public `+` stats confirmed OPEN on go.uvm.edu,
but the instance's stats policy withholds referrers from anonymous viewers,
so this venue cannot leak the agent proxy-stack fingerprint.
""",
    "go-uvm-edu/tgmtq_stats_2026-09-28.txt": """SOURCE: https://go.uvm.edu/tgmtq+
RETRIEVED: 2026-09-28 ~06:40 CDT via read-only GET (single page fetch)
ALSO INDEXED: https://go.uvm.edu/tgmtq~ (search-engine-indexed YOURLS preview page)

Short URL: https://go.uvm.edu/tgmtq
Long URL: http://blog.uvm.edu/whysecurity/2013/11/05/traveling-abroad-without-making-the-news-mobile-tech-edition/ (UVM "Why?security" blog)
Software: Powered by YOURLS v 1.10.3

CREATED: November 6, 2013 @ 10:30 am
TRAFFIC: last 24h 0 hits; last 7d 0 hits; last 30d 0 hits; ALL TIME 334 hits
BEST DAY: 90 hits on November 6, 2013 (creation day)
LOCATION: US: 205, CN: 23, RU: 16, DE: 15, GB: 12, ...
REFERRERS: NOT exposed on the public stats page (owner-only per UVM KB).

PATTERN SWEEP: zero proxy-wrapper markers, zero task-family markers, zero
  epoch nonces, zero agent grammars.

ANALYSIS: control page — a 2013 security-blog link with a creation-day spike
  (90 hits) and long organic decay. Confirms public `+` stats are open on
  go.uvm.edu while referrers stay hidden from anonymous viewers.
""",
    "go-uvm-edu/xc26_stats_2026-09-28.txt": """SOURCE: https://go.uvm.edu/xc26+
RETRIEVED: 2026-09-28 ~06:41 CDT via read-only GET (single page fetch)
SLUG SOURCE: newenglandnewspress.com article on UVM cross country (2026-09-26)
  advertising "go.uvm.edu/xc26" for the BSN/NIKE team store — doc-sourced slug,
  not guessed.

Short URL: https://go.uvm.edu/xc26
Long URL: https://bsnteamsports.com/shop/sL2qvphmme (UVM cross country team store)
Software: Powered by YOURLS v 1.10.3

CREATED: September 24, 2026 @ 8:33 pm
TRAFFIC: last 24h 0 hits; last 7d 1 hit; last 30d 1 hit; ALL TIME 1 hit
BEST DAY: 1 hit on September 24, 2026 (creation day)
LOCATION: US: 1
REFERRERS: NOT exposed on the public stats page (owner-only per UVM KB).

PATTERN SWEEP: zero proxy-wrapper markers, zero task-family markers, zero
  epoch nonces, zero agent grammars.

ANALYSIS: control page — the freshest public go.uvm.edu slug found (created
  2026-09-24, 4 days before retrieval). Public `+` stats confirmed live on
  current links, too. Single organic hit, no agent fingerprint.
""",
}

NEGATIVES = {
    "negative-probes/go-sjf-edu_retired_2026-09-28.txt": """VENUE: go.sjf.edu (St. John Fisher University — appeared on a public URL-shortener blocklist)
PROBE: https://go.sjf.edu/ -> 302 Found, Location: https://www.sjf.edu/ (university homepage).
  The shortener domain no longer serves shortening; it redirects to the apex site.
  www.sjf.edu references go.sjf.edu/map (legacy), but no shortener stats surface exists.
VERDICT: negative — shortener retired. No public stats surface.
""",
    "negative-probes/s-wnmu-edu_dns-dead_2026-09-28.txt": """VENUE: s.wnmu.edu (Western New Mexico University — appeared on a public URL-shortener blocklist)
PROBE: https://s.wnmu.edu/ -> DNS resolution failure (HTTP 000), A record absent.
VERDICT: negative — host is dead.
""",
    "negative-probes/linktest-lse-ac-uk_403_2026-09-28.txt": """VENUE: linktest.lse.ac.uk (London School of Economics — appeared on a public URL-shortener blocklist)
PROBE: https://linktest.lse.ac.uk/ -> 403 Forbidden (284 bytes, non-browser UA; WAF/ACL).
VERDICT: negative — inaccessible from the public internet; no bypass attempted.
""",
    "negative-probes/test-yourls-org_dead_2026-09-28.txt": """VENUE: test.yourls.org (YOURLS project's official public test instance)
PROBE: https://test.yourls.org/ -> connection failure (HTTP 000) — host unreachable.
  (Corroborates brausepulver's earlier finding: "unreachable at probe time".)
VERDICT: negative — dead.
""",
    "negative-probes/1aas-com_stats-login-walled_2026-09-28.txt": """VENUE: 1aas.com (community YOURLS instance — public front page with "Top 10 Links",
  surfaced via web search for YOURLS-powered community shorteners)
PROBE: https://1aas.com/ -> 200 (30,011 bytes, YOURLS-powered, open front page).
  https://1aas.com/gum+ (top link, 19k+ clicks) -> 200 with <title>Login — YOURLS</title>.
  Public per-link stats are login-walled; only the front page's "Top 10" click counts are public.
VERDICT: clean negative for the public-stats technique — no login attempted, no link created.
  (Instance content is SEO/backlink-farm spam, consistent with t.mdcdev.me's profile.)
""",
}

PATTERN_SWEEP = [
    {"file": "go-uvm-edu/-4s0q_stats_2026-09-28.txt",
     "pattern_families": {"cross_venue": ["go.uvm.edu"], "liveness_param": [],
                          "proxy_wrapper": [], "task_family": []}},
    {"file": "go-uvm-edu/tgmtq_stats_2026-09-28.txt",
     "pattern_families": {"cross_venue": ["go.uvm.edu"], "liveness_param": [],
                          "proxy_wrapper": [], "task_family": []}},
    {"file": "go-uvm-edu/xc26_stats_2026-09-28.txt",
     "pattern_families": {"cross_venue": ["go.uvm.edu"], "liveness_param": [],
                          "proxy_wrapper": [], "task_family": []}},
]

PROVENANCE = """# PROVENANCE — university-shorteners-batch3 dataset

## Scope

Batch 3 (workstream B, 2026-09-28) sweeps NEW venues only — batches 1 and 2
(`data/2026-09-28-university-shorteners/`, `data/2026-09-28-university-shorteners-batch2/`) are
untouched. Source of candidates: (1) `go.uvm.edu` (University of Vermont
YOURLS) surfaced via a public URL-shortener blocklist (hagezi/dns-blocklists
issues) plus search-engine-indexed `~` preview pages; (2) three more blocklist
edu/community candidates (`go.sjf.edu`, `s.wnmu.edu`, `linktest.lse.ac.uk`);
(3) `test.yourls.org` (official YOURLS test instance, from Brausepulver's
`5_new_yourls_instances.md`); (4) `1aas.com` community YOURLS (web search).

## Method (read-only, passive)

- Direct GETs only to public read endpoints: per-link `+` stats pages, `~`
  preview pages, front pages.
- Never: shortening/action/API-write endpoints, logins, form submissions,
  counter increments, mass target fetching, challenge solving.
- Slug sources: search-engine-indexed `~` pages (`-4s0q~`, `tgmtq~`) and
  UVM public docs / press (`xc26` from a 2026-09-26 news article;
  `may3`, `vtpitchchallenge`, `myuvm`, `sublet`, `phcourses`, `vk62t` from
  UVM KB/press pages — checked live, recorded in progress.log, not indexed).
  No slugs were guessed.
- Login-walled `+` stats (1aas.com) recorded and not bypassed.
  403/DNS-dead/retired hosts recorded as-is.

## Key finding / caveat

go.uvm.edu's PUBLIC stats pages expose traffic statistics and traffic
LOCATION only — the "Traffic Sources" (referrers) section is owner-only
(per UVM's own KB article `url-shortener-go-uvm-edu`, updated 2026-04-09,
which lists referrers under "View link statistics" requiring NetID+Duo).
So go.uvm.edu CONFIRMS the public-`+`-stats surface on a fourth university
instance but CANNOT leak the agent proxy-stack referrer fingerprint. It is
indexed as a control (public-stats venue, zero agent markers), not as a
fingerprint hit.

## Contents

- `go-uvm-edu/-4s0q_stats_2026-09-28.txt` — indexed `~` preview page slug,
  2013 library link, 266 hits all-time, zero markers.
- `go-uvm-edu/tgmtq_stats_2026-09-28.txt` — indexed `~` preview page slug,
  2013 security-blog link, 334 hits all-time, zero markers.
- `go-uvm-edu/xc26_stats_2026-09-28.txt` — freshest public slug found
  (created 2026-09-24), team-store link, 1 hit, zero markers.
- `negative-probes/*.txt` — 5 documented negatives.
- `events.jsonl` — 3 Elastic-ready docs (the 3 UVM hits).
- `pattern-sweep.json` — per-file pattern-family sweep (all families empty).
- `SHA256SUMS` — checksums of every file above.
- `progress.log` — resumable run log.

## Elastic

Index `university-shorteners-batch3`, canonical shared schema
(notes/gems-es-mapping.json), `labels.shortener.scope` = university.
Negatives are documented here and in the notes report, not in Elastic
(same convention as batches 1 and 2).

## Guards honored

Read-only research only. No submissions/uploads/accounts/logins/posts/
counter increments/payload execution. Agents/infrastructure traces only —
no operator identity, registrant details, or person-focused attribution.
No credentials reproduced. No absolute home-directory paths in logs/docs.
"""

DOCS = [
    {
        "slug": "-4s0q",
        "file": "go-uvm-edu/-4s0q_stats_2026-09-28.txt",
        "long_url": "http://proquest.safaribooksonline.com/book/operating-systems/9780735669635/ddot-moving-your-data-and-settings-to-windows-8/transferring_your_data_to_windows_8_with_html (Safari Books Online)",
        "created": "October 18, 2013 @ 8:40 am",
        "traffic": "last 24h 0 hits; last 7d 0 hits; last 30d 3 hits; ALL TIME 266 hits",
        "best": "4 hits on October 18, 2013",
        "location": "US 131, CA 30, MD 26, CN 15, SA 13, DE 10",
        "preview_url": "http://go.uvm.edu/-4s0q~",
    },
    {
        "slug": "tgmtq",
        "file": "go-uvm-edu/tgmtq_stats_2026-09-28.txt",
        "long_url": "http://blog.uvm.edu/whysecurity/2013/11/05/traveling-abroad-without-making-the-news-mobile-tech-edition/ (UVM Why?security blog)",
        "created": "November 6, 2013 @ 10:30 am",
        "traffic": "last 24h 0 hits; last 7d 0 hits; last 30d 0 hits; ALL TIME 334 hits",
        "best": "90 hits on November 6, 2013",
        "location": "US 205, CN 23, RU 16, DE 15, GB 12",
        "preview_url": "https://go.uvm.edu/tgmtq~",
    },
    {
        "slug": "xc26",
        "file": "go-uvm-edu/xc26_stats_2026-09-28.txt",
        "long_url": "https://bsnteamsports.com/shop/sL2qvphmme (UVM cross country team store)",
        "created": "September 24, 2026 @ 8:33 pm",
        "traffic": "last 24h 0 hits; last 7d 1 hit; last 30d 1 hit; ALL TIME 1 hit",
        "best": "1 hit on September 24, 2026",
        "location": "US 1",
        "preview_url": None,
    },
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def make_doc(d):
    return {
        "@timestamp": TS,
        "description": "Public yourls_stats_page on go.uvm.edu (University of Vermont, YOURLS 1.10.3): https://go.uvm.edu/%s -> %s — CONTROL: %s, zero agent markers; public stats hide referrers (owner-only)" % (
            d["slug"], d["long_url"], d["traffic"]),
        "event": {"created": TS, "dataset": "university-shorteners-batch3"},
        "file": d["file"],
        "labels": {
            "long_url": d["long_url"],
            "pattern_families": {
                "cross_venue": ["go.uvm.edu"],
                "liveness_param": [],
                "proxy_wrapper": [],
                "task_family": [],
            },
            "referrers": {},
            "referrers_hidden": True,
            "short_url": "https://go.uvm.edu/%s" % d["slug"],
            "shortener.instance": "go.uvm.edu",
            "shortener.org": "University of Vermont",
            "shortener.scope": "university",
            "traffic": d["traffic"],
            "traffic_location": d["location"],
            "created": d["created"],
            "best_day": d["best"],
        },
        "matched_string": "https://go.uvm.edu/%s" % d["slug"],
        "note": "Control page: public YOURLS 1.10.3 stats (traffic + location) but referrers hidden from anonymous viewers per UVM policy — cannot leak the agent proxy-stack fingerprint. Zero toolkit/task-family markers. See PROVENANCE.md.",
        "observer": {"product": "muse", "type": "research-agent", "vendor": "meta"},
        "record_kind": "yourls_stats_page",
        "retrieved_at": TS,
        "retrieved_via": "read-only page-text fetch",
        "sha256": sha256(os.path.join(BASE, d["file"])),
        "size_bytes": os.path.getsize(os.path.join(BASE, d["file"])),
        "source_url": "https://go.uvm.edu/%s+" % d["slug"],
        "status": "live",
        "tags": ["yourls", "public-stats", "scope:university",
                 "referrers:hidden-by-policy", "read-only", "status:live",
                 "control:no-agent-markers"],
    }


def main():
    os.makedirs(os.path.join(BASE, "go-uvm-edu"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "negative-probes"), exist_ok=True)

    for rel, text in sorted(EVIDENCE.items()):
        with open(os.path.join(BASE, rel), "w") as f:
            f.write(text)
    for rel, text in sorted(NEGATIVES.items()):
        with open(os.path.join(BASE, rel), "w") as f:
            f.write(text)
    with open(os.path.join(BASE, "PROVENANCE.md"), "w") as f:
        f.write(PROVENANCE)
    with open(os.path.join(BASE, "pattern-sweep.json"), "w") as f:
        json.dump(PATTERN_SWEEP, f, indent=2, ensure_ascii=False)
        f.write("\n")

    jpath = os.path.join(BASE, "events.jsonl")
    with open(jpath, "w") as f:
        for d in DOCS:
            f.write(json.dumps(make_doc(d), ensure_ascii=False) + "\n")

    with open(os.path.join(BASE, "progress.log"), "w") as f:
        f.write("[2026-09-28T11:45Z] WORKSTREAM B batch3 start: new venues only.\n")
        f.write("[2026-09-28T11:45Z] HIT (control): go.uvm.edu (UVM, YOURLS 1.10.3) public + stats live on 9 slugs; referrers owner-only so no fingerprint possible; zero markers. Saved 3 evidence files.\n")
        f.write("[2026-09-28T11:45Z] CHECKED-CLEAN: go.uvm.edu slugs may3/vtpitchchallenge/myuvm/sublet/phcourses/vk62t (from UVM docs) — all live, zero agent markers; recorded in progress.log, not indexed.\n")
        f.write("[2026-09-28T11:45Z] NEGATIVE: go.sjf.edu -> 302 to www.sjf.edu homepage (shortener retired). s.wnmu.edu -> DNS dead. linktest.lse.ac.uk -> 403. test.yourls.org -> connection failed. 1aas.com -> YOURLS live but + stats login-walled. Recorded.\n")
        f.write("[2026-09-28T11:45Z] DATASET BUILT: 3 evidence + 5 negative-probe files + jsonl (3 docs) + pattern-sweep.json + PROVENANCE.md + SHA256SUMS.\n")

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

    print("files:", len(sums), "| jsonl docs:", len(DOCS))


if __name__ == "__main__":
    main()
