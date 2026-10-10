#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-09-09-pixelleak-glow-labs.

Reads evidence/2026-09-09-pixelleak-glow-labs/events.jsonl (10 legacy events)
and emits a Factum bundle JSON on stdout.

Cleaner rules applied:
- Descriptions are byte-identical to the legacy events.jsonl descriptions.
- Report quotes are pulled FULL from raw/pixelleak-blog.html (the legacy
  events.jsonl payloads were truncated mid-sentence). Whitespace collapsed,
  original Unicode punctuation (U+2019, U+2014, curly quotes) preserved.
- No invented timestamps, URLs, or IDs. Report publication date 2026-09-29
  recovered from the page byline (<div class="author-blog-date">) and the
  HTML comment "<!-- Last Published: Tue Sep 29 2026 17:03:52 GMT+0000 -->".
- Every record tagged {"lane": "2026-09-09-pixelleak-glow-labs"}.
- No edges created during ingest (cites on events/claims are record bodies).
"""
import json
import re
import sys

LANE = "2026-09-09-pixelleak-glow-labs"
ACTOR = "agent:lane-ingest-2026-09-09-pixelleak-glow-labs"
LEGACY = "evidence/2026-09-09-pixelleak-glow-labs"
GLOW_URL = ("https://www.glow.io/blogs/how-ai-agents-exposed-"
            "developer-screenshots-from-leading-tech-companies")
RETRIEVED_AT = "2026-09-29T22:52:55Z"
REPORT_DATE = "2026-09-29"
EVENTS_SHA256 = ("d5af572d1dd761494aa555e6bf59c786723b9e46a1a5fb91d39da4a5b922bfd5")

# --- full report text from raw/ ------------------------------------------------
raw = open(f"{LEGACY}/raw/pixelleak-blog.html", encoding="utf-8").read()
text = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
text = re.sub(r"<[^>]+>", " ", text)
import html as _html
text = _html.unescape(text)
text = text.replace("\\n", "\n")
text = re.sub(r"[ \t\xa0\u200b\u200d]+", " ", text)
text = re.sub(r" *\n *", "\n", text)
text = re.sub(r"\n{2,}", "\n", text)
# fix tag-boundary spacing artifact: "organizations</strong>," -> "organizations ,"
text = re.sub(r" ([,.;:!?])", r"\1", text)


def quote(start_marker, end_marker):
    i = text.find(start_marker)
    if i < 0:
        raise SystemExit(f"start marker not found: {start_marker!r}")
    j = text.find(end_marker, i)
    if j < 0:
        raise SystemExit(f"end marker not found: {end_marker!r}")
    return text[i:j + len(end_marker)].strip()


QUOTES = {
    # event 2 disclosure_outreach
    "ev2": quote(
        "Glow Labs reached out to organizations identified",
        "others are also affected."),
    # event 3 technique
    "ev3": quote(
        "The agents figured out that they could make the image available",
        "consider the security implications."),
    # event 4 tooling
    "ev4": quote(
        "Around a third of affected organizations had developers running gitshot",
        "anyone that knows where to look."),
    # event 5 skill_propagation
    "ev5": quote(
        "Agents serving multiple engineers started publicly publishing",
        "weeks or months away from release."),
    # event 6 victim_observation (manufacturer)
    "ev6": quote(
        "At one manufacturer with over 100,000 employees",
        "involved in the UI fix."),
    # event 7 victim_observation (100+ accounts) - full paragraph
    "ev7": quote(
        "Over 100 public accounts were found leaking internal development work",
        "became standard practice."),
    # event 8 scale_figures
    "ev8": (
        quote("Glow Labs has identified over 13,000 internal images",
              "Fortune 500 travel company.")
        + " " + quote("The security leak, impacting 900+ code repositories",
                      "Several are Fortune 500 companies.")
        + " " + quote("93% of the cases had images that sat in a repository",
                      "their own username.")),
    # event 9 lab_repro (agent chain-of-thought, curly quotes in source)
    "ev9": quote("\u201cinternal_sweeper is private",
                 "pinned to a commit SHA.\u201d"),
    # event 10 remediation_guidance
    "ev10": (
        quote("Auditing your own GitHub organization is not enough.",
              "review their accounts.")
        + " " + quote("Check releases and gists, not just files:",
                      "rotate whatever is legible in the pictures.")
        + " " + quote("Harden AI tool configurations",
                      "rather than with each developer.")
        + " " + quote("Get control over \u201cShadow AI\u201d",
                      "keep your git tooling current")),
}

# --- legacy events ---------------------------------------------------------------
events = [json.loads(l) for l in open(f"{LEGACY}/events.jsonl")]
assert len(events) == 10, f"expected 10 events, got {len(events)}"
# positional mapping: legacy record_kinds in file order (victim_observation x2)
_LEGACY_KINDS = ["report_capture", "disclosure_outreach", "technique", "tooling",
                 "skill_propagation", "victim_observation", "victim_observation",
                 "scale_figures", "lab_repro", "remediation_guidance"]
assert [e["record_kind"] for e in events] == _LEGACY_KINDS, "legacy event order changed"
DESC = {
    "report_capture": events[0]["description"],
    "disclosure_outreach": events[1]["description"],
    "technique": events[2]["description"],
    "tooling": events[3]["description"],
    "skill_propagation": events[4]["description"],
    "victim_manufacturer": events[5]["description"],
    "victim_accounts": events[6]["description"],
    "scale_figures": events[7]["description"],
    "lab_repro": events[8]["description"],
    "remediation_guidance": events[9]["description"],
}


def tags(extra):
    t = {"lane": LANE}
    t.update(extra)
    return t


records = []

# 1. source
records.append({
    "kind": "source", "ref": "src",
    "body": {"locator": GLOW_URL, "source_type": "submitted"},
    "tags": tags({
        "description": "Glow Labs PixelLeak blog post (vendor report)",
        "provenance": f"legacy lane {LEGACY} (build_pixelleak.py, 2026-09-29)",
    }),
})

# 2. dataset.snapshot of the legacy extraction
records.append({
    "kind": "observation", "ref": "snap",
    "body": {
        "type": "dataset.snapshot",
        "data_schema": "urn:factum:datasets:snapshot:1",
        "data": {
            "dataset_uri": f"{LEGACY}/events.jsonl",
            "revision": f"sha256:{EVENTS_SHA256}",
            "row_count": 10,
            "coverage": "complete",
        },
        "files": [],
        "source": "@src",
        "observed_at": RETRIEVED_AT,
        "time_basis": "source_metadata",
    },
    "tags": tags({
        "description": ("pixelleak-glow-labs: 10 claim-level extraction events "
                        "(1 confirmed capture, 9 vendor-reported claims)"),
        "provenance": f"legacy lane {LEGACY}/events.jsonl",
    }),
})

# 3. intel.report — the vendor report itself
records.append({
    "kind": "observation", "ref": "report",
    "body": {
        "type": "intel.report",
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "Glow Labs",
            "title": ("PixelLeak: How AI Agents Exposed Developer Screenshots "
                      "from Leading Tech Companies"),
            "url": GLOW_URL,
            "report_date": REPORT_DATE,
            "cached_path": f"data/lanes/{LANE}/raw/pixelleak-blog.html",
            "summary": ("Vendor report: AI coding agents unable to attach "
                        "screenshots via the GitHub CLI worked around the "
                        "limitation by publishing internal screenshots to "
                        "public GitHub repos; 13,000+ images across 300+ orgs "
                        "(vendor-reported)."),
            "provenance": (f"legacy lane {LEGACY}; report_date recovered from "
                           "page byline (author-blog-date div) and HTML "
                           "'Last Published' comment"),
        },
        "files": [],
        "source": "@src",
        "observed_at": RETRIEVED_AT,
        "time_basis": "source_metadata",
    },
    "tags": tags({
        "confidence": "reported",
        "description": "Glow Labs PixelLeak vendor report (upstream material)",
        "vendor_caveat": ("Glow Labs sells endpoint-AI runtime protection; "
                          "figures are vendor-reported, not independently "
                          "verified"),
    }),
})

# 4. web.capture — the HTML artifact capture (legacy event 1, confirmed)
records.append({
    "kind": "observation", "ref": "cap",
    "body": {
        "type": "web.capture",
        "data_schema": "urn:factum:web:web-capture:1",
        "data": {
            "requested_url": GLOW_URL,
            "capture_kind": "http",
            "tool": ("urllib live GET, research UA, 30s timeout, "
                     "3-attempt backoff"),
        },
        "files": [],
        "source": "@src",
        "observed_at": RETRIEVED_AT,
        "time_basis": "source_metadata",
    },
    "tags": tags({
        "confidence": "confirmed",
        "legacy_record_kind": "report_capture",
        "description": DESC["report_capture"],
        "sha256": "ebfa83981f580aa9216f29b81ade002c8393cd75be12d9d2df9c9bcc9ae9e973",
        "size_bytes": "88121",
        "artifact": "raw/pixelleak-blog.html",
    }),
})

# 5. infra.dead_drop — the public-repo image dead-drop technique (event 3)
records.append({
    "kind": "observation", "ref": "dd",
    "body": {
        "type": "infra.dead_drop",
        "data_schema": "urn:factum:infra:dead-drop:1",
        "data": {
            "service": "github.com",
            "endpoint_kind": "other",
            "beacon_type": "capture",
            "markers": ["_gitshot"],
            "payload_summary": ("AI coding agents unable to attach screenshots "
                                "via the GitHub CLI published internal "
                                "screenshots/screen recordings to adjacent "
                                "public GitHub repos (employee personal "
                                "accounts; gitshot _gitshot release tags) so "
                                "human reviewers could see them"),
        },
        "files": [],
        "source": "@src",
        "observed_at": RETRIEVED_AT,
        "time_basis": "source_metadata",
    },
    "tags": tags({
        "confidence": "reported",
        "legacy_record_kind": "technique",
        "description": DESC["technique"],
        "report_quote": QUOTES["ev3"],
        "ttp": "public-repo image dead drop",
    }),
})

# 6. infra.package — gitshot (event 4)
records.append({
    "kind": "observation", "ref": "pkg",
    "body": {
        "type": "infra.package",
        "data_schema": "urn:factum:infra:package:1",
        "data": {
            "name": "gitshot",
            "mechanism": ("Open-source tool that publishes screenshots for "
                          "code reviews under a _gitshot release tag; agents "
                          "at ~1/3 of affected orgs adopted it to overcome "
                          "the GitHub CLI image-attachment limitation"),
            "provenance": ("Glow Labs PixelLeak report (vendor-reported); "
                           f"lane {LANE}"),
        },
        "files": [],
        "source": "@src",
        "observed_at": RETRIEVED_AT,
        "time_basis": "source_metadata",
    },
    "tags": tags({
        "confidence": "reported",
        "legacy_record_kind": "tooling",
        "description": DESC["tooling"],
        "report_quote": QUOTES["ev4"],
    }),
})

# 7. infra.ioc — the _gitshot tag (event 4)
records.append({
    "kind": "observation", "ref": "ioc",
    "body": {
        "type": "infra.ioc",
        "data_schema": "urn:factum:infra:ioc:1",
        "data": {
            "term": "_gitshot",
            "category": "marker",
            "status": "active",
            "provenance": f"{LANE} / Glow Labs PixelLeak report",
        },
        "files": [],
        "source": "@src",
        "observed_at": RETRIEVED_AT,
        "time_basis": "source_metadata",
    },
    "tags": tags({
        "confidence": "reported",
        "legacy_record_kind": "tooling",
        "description": "gitshot release tag under which published screenshots are downloadable by anyone",
    }),
})


def event(ref, legacy_kind, occurred, quote_key, desc_key=None, extra_tags=None):
    t = {
        "confidence": "reported",
        "legacy_record_kind": legacy_kind,
        "description": DESC[desc_key or legacy_kind],
        "report_quote": QUOTES[quote_key],
    }
    if extra_tags:
        t.update(extra_tags)
    return {
        "kind": "event", "ref": ref,
        "body": {
            "event_type": "incident.reported",
            "title": DESC[desc_key or legacy_kind],
            "occurred": occurred,
            "cites": ["@report"],
            "data": {},
            "data_schema": "urn:factum:core:empty:1",
        },
        "tags": tags(t),
    }


# 8. disclosure outreach (event 2)
records.append(event("ev2", "disclosure_outreach",
                     {"basis": "source_text", "on_date": "2026-09-09"},
                     "ev2"))

# 9. skill propagation (event 5)
records.append(event("ev5", "skill_propagation",
                     {"basis": "source_text", "raw": "early July"},
                     "ev5"))

# 10-11. victim observations (events 6, 7)
records.append(event("ev6", "victim_observation",
                     {"basis": "unknown"}, "ev6",
                     desc_key="victim_manufacturer"))
records[-1]["tags"]["victim_class"] = "100k+ employee manufacturer (billing-screen screenshots)"
records.append(event("ev7", "victim_observation",
                     {"basis": "unknown"}, "ev7",
                     desc_key="victim_accounts"))
records[-1]["tags"]["victim_class"] = ("100+ public accounts: frontier AI lab, "
                                        "financial services firm, payments company")

# 12. claim — vendor-reported scale figures (event 8), graded UPSTREAM
records.append({
    "kind": "claim", "ref": "cl8",
    "body": {
        "subject": "@report",
        "property": "reported_scale",
        "value": {
            "internal_images": "13000+",
            "organizations": "300+",
            "repositories": "900+",
            "personal_account_share": "93%",
        },
        "basis": "UPSTREAM",
        "cites": ["@report"],
        "note": ("Glow Labs' vendor-reported scale figures; not independently "
                 "verified by us"),
    },
    "tags": tags({
        "confidence": "reported",
        "legacy_record_kind": "scale_figures",
        "description": DESC["scale_figures"],
        "report_quote": QUOTES["ev8"],
    }),
})

# 13. lab repro (event 9)
records.append(event("ev9", "lab_repro",
                     {"basis": "unknown"}, "ev9",
                     extra_tags={"model": "Claude Code Opus 5",
                      "note": "single-model lab anecdote; chain-of-thought quoted, not field evidence"}))

# 14. claim — remediation guidance (event 10), graded UPSTREAM
records.append({
    "kind": "claim", "ref": "cl10",
    "body": {
        "subject": "@report",
        "property": "remediation_guidance",
        "value": {
            "guidance": [
                "Audit people, not just orgs (include departed employees)",
                "Check releases and gists, not just files",
                "Do not trust text-only scanners (they read text, not pixels)",
                "Get control over Shadow AI; no blanket auto-approval",
                "Control shared agentic skills",
                "Remove unvetted packages like gitshot",
                "If exposed: remove everywhere, ask copy-holders to do the same, rotate anything legible in the pictures",
            ],
        },
        "basis": "UPSTREAM",
        "cites": ["@report"],
        "note": "Report author's remediation recommendations, quoted verbatim in report_quote",
    },
    "tags": tags({
        "confidence": "reported",
        "legacy_record_kind": "remediation_guidance",
        "description": DESC["remediation_guidance"],
        "report_quote": QUOTES["ev10"],
    }),
})

bundle = {
    "bundle": 2,
    "actor": ACTOR,
    "idempotency_key": f"lane-ingest-{LANE}-v1",
    "records": records,
    "tags": {},
}

# in-batch dedup check by primary key field
seen = set()
for r in records:
    b = r.get("body", {})
    d = b.get("data", {})
    key = (r["kind"], b.get("type"), d.get("term") or d.get("name") or
           b.get("title") or r["ref"])
    assert key not in seen, f"duplicate key in batch: {key}"
    seen.add(key)

json.dump(bundle, sys.stdout, ensure_ascii=False, indent=1)
print(f"\n# {len(records)} records", file=sys.stderr)
