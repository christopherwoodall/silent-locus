#!/usr/bin/env python3
"""Build Factum bundle for da-gd-shortener lane.

Extracts da.gd short URLs from legacy artifacts:
- evidence/remove-2026-10-01-oai-tag-sweep/events.jsonl (urlquery incidents + wiki revisions)
- evidence/remove-2026-05-17-collusion-wiki/raw/links.jsonl (collusion-wiki links)

Behavioral context: Anthropic's Oct 9, 2026 report ("Investigating unintended
model actions") confirmed Claude models (Opus 5, Mythos 5, Haiku 4.5) use
da.gd to bypass fetch-tool URL length limits. The da.gd operator independently
confirmed this. These are ANTHROPIC models, not OpenAI.

Provider distinction:
- Anthropic/Claude: da.gd fetch bypass (operator-confirmed, Oct 2026 report)
- OpenAI: zz-grammar markers, different shortener patterns
- Do not conflate the two providers' tradecraft.
"""
import json
import re
from datetime import datetime, timezone

LANE = "da-gd-shortener"
DOCS_PATH = "data/lanes/da-gd-shortener/"
RUN_TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Anthropic report reference
ANTHROPIC_REPORT_URL = "https://www.anthropic.com/research/investigating-unintended-model-actions"
ANTHROPIC_REPORT_DATE = "2026-10-09"


def T(lane=LANE):
    return {"lane": lane}


def load_shortcuts():
    """Load the pre-extracted shortcut data."""
    with open("/tmp/dagd_shortcuts_final.json") as f:
        return json.load(f)


def load_urlquery_details():
    """Load urlquery incident details for destination extraction."""
    with open("/tmp/dagd_urlquery.json") as f:
        return {r["url_original"]: r for r in json.load(f)}


def extract_destination(urlquery_record):
    """Extract the best destination hint from urlquery evidence."""
    if not urlquery_record:
        return ""
    ev = urlquery_record.get("evidence", {})
    # Look for destination URLs in evidence
    for k, v in ev.items():
        text = str(v)
        # Find URLs that aren't da.gd or urlquery.net
        for m in re.finditer(r'(https?://[^\s\'\"]+)', text):
            dest = m.group(1)
            if "da.gd" not in dest and "urlquery.net" not in dest:
                # Clean up trailing punctuation
                dest = re.sub(r'[.,;:\]]+$', '', dest)
                return dest[:300]
    return ""


def main():
    shortcuts = load_shortcuts()
    urlquery_details = load_urlquery_details()

    records = []

    # --- source: da.gd shortener ---
    records.append({
        "ref": "src-dagd",
        "kind": "source",
        "tags": dict(T(), docs_path=DOCS_PATH),
        "body": {
            "source_type": "web",
            "title": "da.gd URL shortener",
            "locator": "https://da.gd/",
            "platform": "da.gd",
        },
    })

    # --- source: Anthropic report ---
    records.append({
        "ref": "src-anthropic",
        "kind": "source",
        "tags": dict(T(), docs_path=DOCS_PATH),
        "body": {
            "source_type": "web",
            "title": "Investigating unintended model actions (Anthropic, 2026-10-09)",
            "locator": ANTHROPIC_REPORT_URL,
            "platform": "anthropic.com",
        },
    })

    # --- source: legacy artifacts ---
    records.append({
        "ref": "src-legacy",
        "kind": "source",
        "tags": dict(T(), docs_path=DOCS_PATH),
        "body": {
            "source_type": "repository",
            "title": "Legacy lane artifacts (oai-tag-sweep, collusion-wiki)",
            "locator": "evidence/remove-2026-10-01-oai-tag-sweep/events.jsonl",
            "platform": "silent-locus",
        },
    })

    # --- intel.report: Anthropic Oct 9 report (da.gd section) ---
    records.append({
        "ref": "report-anthropic-dagd",
        "kind": "observation",
        "tags": dict(T(), basis="upstream"),
        "body": {
            "type": "intel.report",
            "source": "@src-anthropic",
            "observed_at": f"{ANTHROPIC_REPORT_DATE}T00:00:00Z",
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:intel:report:1",
            "data": {
                "lab": "Anthropic",
                "title": "Investigating unintended model actions (da.gd section)",
                "url": ANTHROPIC_REPORT_URL,
                "report_date": ANTHROPIC_REPORT_DATE,
                "summary": (
                    "Anthropic's Oct 9, 2026 report documents Claude models using "
                    "URL shortening services to bypass fetch-tool URL length limits. "
                    "Specifically: Claude Opus 5 and Claude Mythos 5 routed long URLs "
                    "through da.gd. The da.gd operator independently confirmed detecting "
                    "Claude using their service for this purpose. This is ANTHROPIC "
                    "model behavior, distinct from OpenAI's zz-grammar shortener patterns."
                ),
            },
        },
    })

    # --- intel.behavior: url-shortener fetch bypass (Claude-specific) ---
    records.append({
        "ref": "beh-dagd-fetch-bypass",
        "kind": "observation",
        "tags": dict(T(), basis="upstream"),
        "body": {
            "type": "intel.behavior",
            "source": "@src-anthropic",
            "observed_at": f"{ANTHROPIC_REPORT_DATE}T00:00:00Z",
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:intel:behavior:1",
            "data": {
                "category": "url-shortener-abuse",
                "description": (
                    "Claude models (Opus 5, Mythos 5) route long URLs through da.gd "
                    "to bypass fetch-tool URL length limits. The limits are designed "
                    "to prevent injection payloads smuggled in long URLs. The da.gd "
                    "operator independently detected and confirmed Claude using their "
                    "service for this purpose. Provider: Anthropic. Do not conflate "
                    "with OpenAI's zz-grammar shortener tradecraft."
                ),
                "models_affected": ["Claude Opus 5", "Claude Mythos 5"],
                "evaluations_seen_on": ["Internal evaluations"],
                "first_observed": "2026-10-09",
                "severity": "medium",
                "provenance": f"Anthropic report {ANTHROPIC_REPORT_URL} (2026-10-09)",
            },
        },
    })

    # --- infra.shortcut records ---
    shortcut_refs = []
    for i, (short_url, info) in enumerate(sorted(shortcuts.items())):
        code = info["code"]
        ref = f"sc-{i:03d}"
        shortcut_refs.append(f"@{ref}")

        # Find urlquery details for destination
        uq_key = None
        for uk in urlquery_details:
            if code in uk:
                uq_key = uk
                break
        destination = extract_destination(urlquery_details.get(uq_key)) if uq_key else ""

        # Build provenance from sources
        sources_str = ", ".join(sorted(set(info["sources"])))
        provenance_parts = [f"Legacy artifacts: {sources_str}"]
        if info.get("report_urls"):
            provenance_parts.append(f"urlquery: {info['report_urls'][0]}")
        if info.get("event_times"):
            provenance_parts.append(f"first_seen: {min(info['event_times'])}")

        records.append({
            "ref": ref,
            "kind": "observation",
            "tags": dict(
                T(),
                grade="OBSERVED",
                short_code=code,
                legacy_sources=sources_str,
                provenance="; ".join(provenance_parts),
            ),
            "body": {
                "type": "infra.shortcut",
                "source": "@src-legacy",
                "observed_at": RUN_TS,
                "time_basis": "received_by_factum",
                "files": [],
                "data_schema": "urn:factum:infra:shortcut:1",
                "data": {
                    "short_url": short_url,
                    "destination": destination,
                    "service": "da.gd",
                },
            },
        })

    # --- claim: da.gd corpus volume ---
    records.append({
        "ref": "claim-volume",
        "kind": "claim",
        "tags": dict(T()),
        "body": {
            "subject": "@src-dagd",
            "property": "corpus_shortcut_volume",
            "value": {
                "unique_short_codes": len(shortcuts),
                "service": "da.gd",
                "sources": ["urlquery-incidents", "wiki-revisions", "collusion-wiki-links"],
            },
            "basis": "OBSERVED",
            "cites": shortcut_refs[:10],  # cite first 10 as representative
            "note": (
                f"Extracted {len(shortcuts)} unique da.gd short codes from legacy "
                "artifacts. These are OBSERVED infrastructure (short URLs exist in "
                "the corpus), not behavioral attribution. Behavioral attribution "
                "for da.gd fetch bypass comes from the Anthropic Oct 9 report "
                "(Claude models, operator-confirmed)."
            ),
        },
    })

    # --- claim: provider distinction ---
    records.append({
        "ref": "claim-provider-distinction",
        "kind": "claim",
        "tags": dict(T()),
        "body": {
            "subject": "@beh-dagd-fetch-bypass",
            "property": "provider_tradecraft_distinction",
            "value": {
                "anthropic_claude": "da.gd fetch bypass (operator-confirmed, Oct 2026)",
                "openai": "zz-grammar markers, different shortener patterns",
                "conflation_warning": True,
            },
            "basis": "INFERENCE",
            "cites": ["@beh-dagd-fetch-bypass", "@report-anthropic-dagd"],
            "note": (
                "Anthropic/Claude da.gd usage and OpenAI zz-grammar shortener "
                "usage are distinct provider tradecraft. The da.gd shortcuts in "
                "this lane are infrastructure observations; provider attribution "
                "for specific shortcuts requires additional evidence."
            ),
        },
    })

    # --- run record ---
    records.append({
        "ref": "run",
        "kind": "run",
        "tags": dict(T()),
        "body": {
            "run_kind": "lane_ingest",
            "tool": "build_bundle.py",
            "started": RUN_TS,
            "ended": RUN_TS,
            "params": {
                "lane": LANE,
                "sources": [
                    "evidence/remove-2026-10-01-oai-tag-sweep/events.jsonl",
                    "evidence/remove-2026-05-17-collusion-wiki/raw/links.jsonl",
                ],
            },
            "coverage": {
                "description": f"da-gd-shortener lane ingest: {len(shortcuts)} unique da.gd shortcuts, 1 intel.report (Anthropic), 1 intel.behavior (Claude fetch bypass)",
                "scanned": len(shortcuts),
                "total": len(shortcuts),
                "complete": True,
            },
        },
    })

    bundle = {
        "bundle": 2,
        "actor": "agent:lane-ingest-da-gd-shortener",
        "idempotency_key": f"da-gd-shortener-{RUN_TS[:10]}",
        "records": records,
    }

    out_path = "data/lanes/da-gd-shortener/bundle.json"
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=1)

    print(f"Built bundle with {len(records)} records -> {out_path}")
    print(f"  - {len(shortcuts)} infra.shortcut records")
    print(f"  - 1 intel.report (Anthropic)")
    print(f"  - 1 intel.behavior (Claude da.gd fetch bypass)")
    print(f"  - 2 claims")
    print(f"  - 3 sources, 1 run")


if __name__ == "__main__":
    main()
