#!/usr/bin/env python3
"""Build the Factum aggregate bundle for the 2026-10-01 oai-tag-sweep lane.

Aggregation (not 1:1): 96,353 annotated sweep events collapse to
  - 1 run record (the aggregation pass),
  - 1 source record (lane locator),
  - 15 intel.behavior observations (one per fired indicator),
  - 3 OBSERVED claims (coverage, multi-indicator rate, temporal distribution).

Reads agg.json (per-indicator prevalence, date ranges, verbatim exemplars)
produced by aggregate.py from data/lanes/oai-tag-sweep/events.jsonl and
cross-checked against sweep_summary.json.

Usage: python3 build_factum_bundle.py  -> /tmp/oai_agg/bundle.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
AGG = json.load(open(os.path.join(HERE, "agg.json")))
LANE = "oai-tag-sweep"

# (plain-English pattern definition, verdict note or "")
INDICATOR_DEFS = {
    "oai_prefix": (
        "Token-boundary match for 'oai' followed by a word character "
        "(regex: (?:^|[^a-z0-9])oai[-_a-z0-9], case-insensitive). The oai* "
        "agent-tag grammar marker.",
        "Marker verdict (verified against bytes): the 4 frozen-urlquery hits "
        "are ALL false positives (OAItest7z645xgm httpbin probe, "
        "OAIJS1782002787694412133 httpbun probe title, persistent.oaistatic.com "
        "ChatGPT asset domain, utm_oaid ad param) - zero genuine "
        "Transluce-style oai* agent tags in the frozen urlquery corpus. The "
        "2,026 wiki hits are genuine DSE-grammar labels "
        "(e.g. dse~OAIFlatheadBridgeTestMay24X@45, grammar:oai tags), "
        "wiki-side, agent-authored. The 632 rubygems hits are oai gem names "
        "(existing watchlist surface)."),
    "zz_label": (
        "Token-boundary match for 'zz' followed by a word character "
        "(regex: (?:^|[^a-z0-9])zz[a-z0-9_-], case-insensitive). The zz label "
        "grammar marker.",
        ""),
    "epoch_nonce": (
        "Ten-digit epoch timestamp in the 1[78]xxxxxxxx range "
        "(regex: (?:^|[^0-9])(1[78]\\d{8})(?:[^0-9]|$)). Nonce/timestamp "
        "marker used as a cache-buster or run identifier.",
        ""),
    "httpbun_httpbin": (
        "Reference to httpbin or httpbun (regex: httpb[u]?in, "
        "case-insensitive). HTTP echo/probe service used in agent probes.",
        ""),
    "jina_allorigins_dagd": (
        "Reference to r.jina.ai, allorigins, or dagd relay hosts "
        "(regex: r\\.jina\\.ai|allorigins|dagd, case-insensitive). "
        "Reader/proxy relay services.",
        ""),
    "uniq_nonce_param": (
        "URL query parameter uniq=, nonce=, _t= or cb= with 6+ digits "
        "(regex: [?&](uniq|nonce|_t|cb)=\\d{6,}, case-insensitive). "
        "Cache-busting nonce parameter.",
        ""),
    "arquivo_pt": (
        "Reference to arquivo.pt (regex: arquivo\\.pt, case-insensitive). "
        "Portuguese web archive.",
        "Marker verdict (verified against bytes): the 1 urlquery hit is a scan "
        "OF the arquivo.pt homepage (2026-09-25), not relay use. The 8 wiki "
        "hits are Nightingale investigation notes documenting our own DataUSA "
        "bundle reproduction (Jun 16-17). Zero agent relay-use of arquivo.pt "
        "in our vantage."),
    "markdown_new": (
        "Reference to markdown.new (regex: markdown\\.new, case-insensitive). "
        "Markdown conversion proxy service.",
        "Marker verdict (verified against bytes): the 11 urlquery hits split "
        "into 7 tinyurl-chain scans (May 11-13) and 4 agent uses of "
        "markdown.new/r.jina.ai/... chains (May 14 datastudio, May 17 "
        "alexandria.ucsb.edu), plus our own reproduction (Sep 24) and one May "
        "27 API conversion. The 2,628 wiki hits are wiki revisions documenting "
        "agent converter use."),
    "cors_conversion_proxy": (
        "CORS proxy or converter host: corsproxy, cors.lol, workers.dev, "
        "sirjosh, corsfix, cors-anywhere, 12ft.io, 1ft.io, textise, textance, "
        "googleusercontent, translate.google (case-insensitive).",
        ""),
    "exposed_key_in_url": (
        "API key / token style query parameter in a URL: apikey, "
        "subscription-key, access-key, auth-token, secret, token, private-key "
        "(regex: [?&](api[-_]?key|...)=, case-insensitive).",
        ""),
    "double_slash_path": (
        "Double slash inside a URL path (regex: https?://[^/\\s]+/[^\\s?]*//). "
        "Typical of chained converter/proxy URLs (e.g. "
        "https://markdown.new/https://...).",
        ""),
    "file_suffix_antibot": (
        "File suffix (.json/.xml/.csv/.txt/.pdf) or output=/raw=/url=/debug= "
        "parameter in a URL (case-insensitive). Machine-readable fetch "
        "marker.",
        ""),
    "direct_ip_route": (
        "Literal IPv4 address as URL host (regex: https?://\\d{1,3}(\\.\\d{1,3}){3}). "
        "Direct-IP routing, bypassing DNS.",
        ""),
    "goimport_canary": (
        "go-import meta tag (regex: go-import, case-insensitive). Go module "
        "proxy canary marker.",
        ""),
    "collusion_wiki_ref": (
        "Literal reference to collusion.wiki (regex: collusion\\.wiki, "
        "case-insensitive).",
        "Marker verdict: tautological on the wiki corpus - every collusion-wiki "
        "revision cites its own source, so the wiki hit count equals the wiki "
        "corpus size. The 5 urlquery hits are reports that mention "
        "collusion.wiki."),
}

SEVERITY = {
    "collusion_wiki_ref": "minimal",   # tautological self-match on wiki corpus
    "arquivo_pt": "minimal",           # 9 hits, zero agent relay use
    "direct_ip_route": "low",
}
ALSO_IN_TERMINA = {"oai_prefix", "epoch_nonce", "markdown_new"}

SRC_LABEL = {"frozen:collusion-wiki": "collusion-wiki",
             "frozen:urlquery-incidents": "urlquery-incidents",
             "frozen:rubygems-goimport": "rubygems-goimport",
             "transluce-dataset": "transluce-dataset"}


def behavior_description(ind, d):
    pattern, verdict = INDICATOR_DEFS[ind]
    per = ", ".join(f"{SRC_LABEL[s]}={c}" for s, c in
                    sorted(d["per_source"].items()))
    lines = [
        f"Indicator '{ind}' from the 2026-10-01 oai-tag sweep.",
        f"Pattern: {pattern}",
        f"Prevalence: {d['total_hits']} annotated hits "
        f"({per}); first seen {d['first_seen'][:10]}, "
        f"last seen {d['last_seen'][:10]}.",
    ]
    if verdict:
        lines.append(verdict)
    lines.append("Exemplar evidence (verbatim sweep-sidecar snippets):")
    for x in d["exemplars"]:
        lines.append(f"- [{SRC_LABEL[x['source']]} {x['event_time'][:10]}] "
                     f"{x['snippet']}")
    lines.append("Severity is marker-presence severity for a research sweep, "
                 "not an impact assessment.")
    return "\n".join(lines)


def main():
    records = []

    records.append({
        "ref": "src",
        "kind": "source",
        "body": {
            "locator": "data/lanes/oai-tag-sweep/events.jsonl",
            "source_type": "submitted",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "description": "Aggregated oai-tag-sweep lane: 96,353 annotated "
                           "indicator-match events across 4 frozen sources "
                           "(sweep run 2026-10-01). Per-indicator aggregates "
                           "live in Factum; full rows stay in the lane "
                           "artifacts.",
            "legacy_path": "evidence/remove-2026-10-01-oai-tag-sweep/events.jsonl",
        },
    })

    records.append({
        "ref": "run",
        "kind": "run",
        "body": {
            "run_kind": "lane_aggregation",
            "tool": "oai-tag-sweep-aggregate",
            "tool_version": "1",
            "started": "2026-10-10T04:00:00Z",
            "ended": "2026-10-10T05:00:00Z",
            "params": {
                "lane": LANE,
                "method": "per-indicator prevalence + verbatim exemplar "
                          "extraction from the sweep sidecar, independently "
                          "re-derived and cross-checked against "
                          "sweep_summary.json (totals, per-indicator "
                          "per-source counts, 2+ indicator rate all match)",
                "source_sidecar": "evidence/2026-10-01-oai-tag-sweep/events.jsonl",
                "sweep_script": "evidence/2026-10-01-oai-tag-sweep/sweep_indicators.py",
            },
            "coverage": {
                "description": "Aggregated 96,353 annotated sweep events from "
                               "138,696 frozen records (urlquery-incidents "
                               "51,643; collusion-wiki 80,434; "
                               "rubygems-goimport 6,619) plus the 38,160-row "
                               "Transluce dataset (9 hits).",
                "scanned": 138696,
                "total": 138696,
                "complete": True,
            },
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
        },
    })

    beh_refs = []
    for ind in sorted(AGG["indicators"]):
        d = AGG["indicators"][ind]
        ref = "beh_" + ind
        beh_refs.append("@" + ref)
        tags = {"lane": LANE, "grade": "OBSERVED", "indicator": ind}
        if ind in ALSO_IN_TERMINA:
            tags["also_observed_in_lane"] = "2026-09-05-termina-digital"
        records.append({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "intel.behavior",
                "data_schema": "urn:factum:intel:behavior:1",
                "data": {
                    "category": ind,
                    "description": behavior_description(ind, d),
                    "provenance": "2026-10-01-oai-tag-sweep",
                    "first_observed": d["first_seen"][:10],
                    "severity": SEVERITY.get(ind, "low"),
                },
                "observed_at": "2026-10-01T00:00:00Z",
                "time_basis": "legacy_documented",
                "source": "@src",
                "files": [],
            },
            "tags": tags,
        })

    claims = [
        ("claim_coverage", "sweep_coverage", {
            "total_annotated_events": 96353,
            "frozen_records_scanned": 138696,
            "per_source_scanned": {
                "urlquery-incidents": 51643, "collusion-wiki": 80434,
                "rubygems-goimport": 6619, "transluce-dataset-rows": 38160},
            "per_source_hits": {
                "urlquery-incidents": 12938, "collusion-wiki": 80434,
                "rubygems-goimport": 2972, "transluce-dataset": 9},
            "sweep_run_date": "2026-10-01",
            "indicators_defined": 18, "indicators_fired": 15,
        }),
        ("claim_multi", "multi_indicator_rate", {
            "events_with_ge2_indicators": 25699,
            "pct_of_annotated": 26.7,
            "overlap_days_ge2_sources": 58,
        }),
        ("claim_temporal", "temporal_distribution", {
            "event_time_span": "2025-03-04 to 2026-09-27",
            "burst_minutes_ge8_hits": 1665,
            "largest_burst": {"minute": "2026-06-18T20:10Z", "hits": 665,
                              "source": "collusion-wiki"},
            "window_note": "Hit-days concentrate in may2026_visible_middle "
                           "(2026-05-01..2026-09-26); day-level counts per "
                           "known window are in the lane temporal_overlaps.md.",
        }),
    ]
    for ref, prop, value in claims:
        records.append({
            "ref": ref,
            "kind": "claim",
            "body": {
                "subject": "@run",
                "property": prop,
                "value": value,
                "basis": "OBSERVED",
                "cites": ["@run"],
            },
            "tags": {"lane": LANE, "grade": "OBSERVED"},
        })

    bundle = {
        "bundle": 2,
        "actor": "agent:lane-ingest-oai-tag-sweep",
        "idempotency_key": "oai-tag-sweep-aggregate-v1",
        "records": records,
    }
    out = "/tmp/oai_agg/bundle.json"
    json.dump(bundle, open(out, "w"), indent=1)
    print(f"wrote {out}: {len(records)} records "
          f"(1 run, 1 source, {len(beh_refs)} intel.behavior, 3 claims)")


if __name__ == "__main__":
    main()
