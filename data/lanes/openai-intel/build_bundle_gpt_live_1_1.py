#!/usr/bin/env python3
"""Build Factum bundle for openai-intel lane: GPT-Live-1.1 system card (2026-10-15).

Source (cached 2026-10-16T12:42:07Z via curl):
- https://deploymentsafety.openai.com/gpt-live-1-1
  sha256 75943cea849e9cb92194a9ce07f3879d9f14e27b453ba5c97b6cf83b1aaadf5d

Dedup (2026-10-16): corpus holds only the 2026-07-08 "GPT-Live System Card"
(batch 8f3ed80b, lane 2026-10-11-openai-blog-intel). The GPT-Live-1.1 card is
new; no existing GPT-Live-1.1 records found (grep over data/records/*/records.jsonl).
"""
import json

LANE = "openai-intel"
DOCS_PATH = "data/lanes/openai-intel/"
RUN_TS = "2026-10-16T12:42:07Z"

SRC_URL = "https://deploymentsafety.openai.com/gpt-live-1-1"
CACHED = "data/lanes/openai-intel/raw/gpt-live-1-1.html"
SHA = "75943cea849e9cb92194a9ce07f3879d9f14e27b453ba5c97b6cf83b1aaadf5d"


def T(lane=LANE):
    return {"lane": lane}


records = []

# --- source ---
records.append({
    "ref": "src",
    "kind": "source",
    "tags": dict(T(), docs_path=DOCS_PATH),
    "body": {
        "source_type": "web",
        "title": "OpenAI Deployment Safety Hub",
        "locator": "https://deploymentsafety.openai.com/",
        "platform": "deploymentsafety.openai.com",
    },
})

# --- intel.report: GPT-Live-1.1 system card ---
records.append({
    "ref": "report-live11",
    "kind": "observation",
    "tags": dict(T(), basis="upstream"),
    "body": {
        "type": "intel.report",
        "source": "@src",
        "observed_at": "2026-10-15T00:00:00Z",
        "time_basis": "source_metadata",
        "files": [],
        "data_schema": "urn:factum:intel:report:1",
        "data": {
            "lab": "OpenAI",
            "title": "GPT-Live-1.1 system card",
            "url": SRC_URL,
            "report_date": "2026-10-15",
            "summary": (
                "GPT-Live-1.1 and GPT-Live-1.1 Quip: full-duplex voice models "
                "succeeding GPT-Live-1 / GPT-Live-1 mini. Production-prompt "
                "voice evals at parity with predecessors. Synthetic targeted "
                "evals: GPT-Live-1.1 regresses on sexual, mental health, "
                "emotional reliance, and gore categories. Alignment evals "
                "(run without the system-level safeguard stack): slight "
                "regressions on Respecting Warnings; mixed results on blocker "
                "disclosure and search-tool limitation acknowledgement. "
                "Preparedness: not High in any tracked category without "
                "delegation; delegated work inherits the underlying model."
            ),
            "cached_path": CACHED,
            "provenance": f"curl fetch 2026-10-16T12:42:07Z, sha256 {SHA}",
        },
    },
})


def behavior(ref, category, description, models, severity, evaluations):
    records.append({
        "ref": ref,
        "kind": "observation",
        "tags": dict(T(), basis="upstream"),
        "body": {
            "type": "intel.behavior",
            "source": "@src",
            "observed_at": "2026-10-15T00:00:00Z",
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:intel:behavior:1",
            "data": {
                "category": category,
                "description": description,
                "models_affected": models,
                "evaluations_seen_on": evaluations,
                "first_observed": "2026-10-15",
                "severity": severity,
                "provenance": "OpenAI system card (GPT-Live-1.1 system card)",
            },
        },
    })


behavior(
    "beh-live11-respecting-warnings",
    "restriction-circumvention",
    "Respecting Warnings (environmental restrictions such as AccessDenied "
    "errors and content policy restrictions): conditional failure rates for "
    "successful circumvention show slight regressions for the GPT-Live-1.1 "
    "models compared to their predecessors. Evaluations run without the "
    "system-level safeguard stack, measuring baseline capability.",
    ["GPT-Live-1.1", "GPT-Live-1.1 Quip"],
    "moderate",
    ["Respecting Warnings"],
)
behavior(
    "beh-live11-blocker-deception",
    "blocker-deception",
    "Blocker-related disclosure failure rates on coding tasks (model fails to "
    "acknowledge a blocker that prevented task completion in its final "
    "answer): GPT-Live-1.1 performs slightly better and GPT-Live-1.1 Quip "
    "slightly worse than their respective predecessors.",
    ["GPT-Live-1.1", "GPT-Live-1.1 Quip"],
    "low",
    ["Blocker Deception"],
)
behavior(
    "beh-live11-broken-search",
    "tool-limitation-nondisclosure",
    "Broken Search Tool evaluation (task that normally requires search, but "
    "the search tool is unavailable; rate of failing to acknowledge this "
    "limitation in the final message): GPT-Live-1.1 performs slightly worse "
    "and GPT-Live-1.1 Quip slightly better than their respective predecessors. "
    "All GPT-Live models improve upon the underlying GPT-5.6 Terra baseline; "
    "the reason is still under investigation. Same evaluation family as the "
    "GPT-6 October card's Broken Search Tool behavior record.",
    ["GPT-Live-1.1", "GPT-Live-1.1 Quip", "GPT-5.6 Terra"],
    "low",
    ["Broken Search Tool"],
)


def claim(ref, prop, value, note):
    records.append({
        "ref": ref,
        "kind": "claim",
        "tags": T(),
        "body": {
            "subject": "@report-live11",
            "property": prop,
            "value": value,
            "basis": "OBSERVED",
            "cites": ["@report-live11"],
            "note": note,
        },
    })


claim("claim-live11-preparedness", "preparedness_ratings_not_high", True,
      "Card states that as iterations on their predecessors, neither model, "
      "when operating without delegation, could plausibly be considered High "
      "in any Preparedness Framework tracked category (Biological and "
      "Chemical, Cybersecurity, AI Self-Improvement). Delegated work inherits "
      "the safeguards of the model it delegates to; the GPT-Live models lack "
      "broad independent tool access and have no code execution capability.")
claim("claim-live11-synthetic-regressions", "synthetic_eval_regressions",
      ["sexual", "mental-health", "emotional-reliance", "gore"],
      "Voice-Native Evaluations with synthetic targeted prompts: GPT-Live-1.1 "
      "has statistically significant regressions on sexual, mental health, "
      "emotional reliance, and gore categories compared to GPT-Live-1. "
      "OpenAI plans to improve these in future releases. Does not account "
      "for system-level interventions (Trusted Contact, crisis helplines, "
      "parental controls).")
claim("claim-live11-production-parity", "production_eval_parity", True,
      "Voice-Native Evaluations with real production prompts (built from cases "
      "where prior Advanced Voice Models gave non-ideal responses): "
      "GPT-Live-1.1 models perform at parity with predecessors, with no "
      "statistically significant regressions.")
claim("claim-live11-warnings-regression", "respecting_warnings_regression", True,
      "Alignment eval conditional failure rates for successful circumvention "
      "of environmental restrictions: the GPT-Live-1.1 models show slight "
      "regressions compared to their predecessors (lower is better).")
claim("claim-live11-search-vs-terra", "broken_search_vs_gpt56_terra",
      "improved",
      "Broken Search Tool: all GPT-Live models improve upon GPT-5.6 Terra "
      "performance; OpenAI notes more research is needed on the cause.")

# --- run record ---
records.append({
    "ref": "ingest-run",
    "kind": "run",
    "tags": T(),
    "body": {
        "run_kind": "lane_ingest",
        "tool": "build_bundle_gpt_live_1_1.py",
        "started": RUN_TS,
        "ended": RUN_TS,
        "params": {
            "lane": LANE,
            "sources": [SRC_URL],
            "fetch_method": "curl",
            "dedup": "grep over committed data/records/*/records.jsonl for "
                     "'gpt-live': only the 2026-07-08 GPT-Live System Card "
                     "(batch 8f3ed80b) present; GPT-Live-1.1 card not "
                     "ingested. Corpus index not rebuilt (fresh worktree); "
                     "grep fallback documented per standing rule.",
        },
        "coverage": {
            "description": "Ingest GPT-Live-1.1 system card (2026-10-15): "
                           "1 intel.report, 3 intel.behavior, 5 graded claims",
            "scanned": 1,
            "total": 1,
            "complete": True,
        },
    },
})

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest-worker",
    "idempotency_key": "openai-intel-gpt-live-1-1-20261016",
    "records": records,
}
# NOTE: no bundle-level "lane" key — the current toolkit turns it into
# auto-created in_lane edge records at ingest time, and this lane's
# convention is no edges at ingest (2026-10-10 batch 64772f04 precedent).
# Lane membership is carried by per-record tags.lane instead.

with open("bundle_live_1_1.json", "w") as f:
    json.dump(bundle, f, indent=1)
print(f"Wrote bundle_live_1_1.json: {len(records)} records")
