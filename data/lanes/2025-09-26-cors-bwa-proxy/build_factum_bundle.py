#!/usr/bin/env python3
"""Build the Factum bundle for the 2025-09-26-cors-bwa-proxy aggregate lane.

Reads data/lanes/2025-09-26-cors-bwa-proxy/events.jsonl (154 legacy events)
and emits a Factum bundle (bundle.json) plus drop_log.json.

Mapping (legacy record_kind -> Factum type):
  proxied_target (113) -> infra.proxy_chain   (47 new; 66 skipped: same
      proxied URL already in corpus as infra.proxy_chain, lane
      2026-10-01-intermediary-relays)
  proxy_ladder (29)    -> infra.proxy_chain   (aggregate edges; kept)
  proxy_family (6)     -> infra.proxy_instance (5 new; r.jina-ai.workers.dev
      skipped: already in corpus)
  venue_summary (6)    -> claims on the run record (venue coverage)

Dedup runs against /tmp/agg_ingest/corpus_lookup.json (exported batches).
"""
import json
import os
import re
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2025-09-26-cors-bwa-proxy"
ACTOR = "agent:lane-ingest-2025-09-26-cors-bwa-proxy"
LOOKUP = json.load(open("/tmp/agg_ingest/corpus_lookup.json"))
CHAIN_VARIANTS = LOOKUP["chain_variant_map"]
INST_HOSTS = LOOKUP["inst_hosts"]

EVENTS = os.path.join(HERE, "events.jsonl")
RAW_HOSTNAMES = os.path.join(HERE, "raw", "other_workers_dev_hostnames.json")


def variants(u):
    if not u:
        return set()
    u1 = unquote(unquote(unquote(u))).replace("&amp;", "&")
    out = {u1, re.sub(r"^https?://", "", u1)}
    m = re.match(r"^https?://[^/]+/(.*)$", u1)
    if m:
        out.add(m.group(1))
        out.add(re.sub(r"^https?://", "", m.group(1)))
    for mm in re.finditer(r"https?://", u1):
        if mm.start() > 0:
            out.add(u1[mm.start():])
            out.add(re.sub(r"^https?://", "", u1[mm.start():]))
    return {x for x in out if x}


def is_dup(url):
    return any(v in CHAIN_VARIANTS for v in variants(url))


def stag(d):
    """Tags dict with all-string values."""
    return {k: (v if isinstance(v, str) else json.dumps(v))
            for k, v in d.items() if v is not None}


INVOCATION_SHAPES = {
    "cors.hypnguyen.workers.dev":
        "https://cors.hypnguyen.workers.dev/?<percent-encoded-target-url>",
    "cors-get-proxy.sirjosh.workers.dev":
        "https://cors-get-proxy.sirjosh.workers.dev/?url=<target-url>",
    "cloudflare-cors-anywhere.hanpengchen.workers.dev":
        "https://cloudflare-cors-anywhere.hanpengchen.workers.dev/?<target-url>",
    "test.cors.workers.dev":
        "https://test.cors.workers.dev/?<target-url>",
    "cf-cors.findme-19.workers.dev":
        "https://cf-cors.findme-19.workers.dev/<target-url>",
}


def main():
    records = []
    drop_log = []

    records.append({
        "ref": "src",
        "kind": "source",
        "body": {
            "locator": "data/lanes/2025-09-26-cors-bwa-proxy/events.jsonl",
            "source_type": "submitted",
        },
        "tags": stag({
            "lane": LANE,
            "grade": "OBSERVED",
            "description": "Aggregate lane: cors.bwa.workers.dev cross-corpus "
                           "proxy-primitive sweep (113 proxied_target, 29 "
                           "proxy_ladder, 6 proxy_family, 6 venue_summary). "
                           "Per-URL observations live in Factum; full rows "
                           "stay in the lane artifacts.",
            "legacy_path": "evidence/aggregates/remove-2025-09-26-cors-bwa-proxy/events.jsonl",
        }),
    })

    counts = {"proxied_target_new": 0, "proxied_target_dup": 0,
              "proxy_ladder": 0, "proxy_family_new": 0,
              "proxy_family_dup": 0, "venue_summary": 0}
    venue_rows = []

    with open(EVENTS) as fh:
        for line in fh:
            d = json.loads(line)
            kind = d["record_kind"]
            L = d.get("labels", {})

            if kind == "proxied_target":
                full = d.get("matched_string")
                dec = L.get("decoded_target")
                if is_dup(full) or is_dup(dec):
                    counts["proxied_target_dup"] += 1
                    drop_log.append({"legacy_kind": kind, "reason": "duplicate",
                                     "detail": "proxied URL already in corpus "
                                     "as infra.proxy_chain (lane "
                                     "2026-10-01-intermediary-relays)",
                                     "matched_string": d.get("matched_string"),
                                     "legacy_fingerprint": d.get("fingerprint")})
                    continue
                counts["proxied_target_new"] += 1
                layers = [x.strip() for x in
                          L.get("chain_layers", "").split(">")]
                records.append({
                    "ref": "pt_%d" % counts["proxied_target_new"],
                    "kind": "observation",
                    "body": {
                        "type": "infra.proxy_chain",
                        "data_schema": "urn:factum:infra:proxy-chain:1",
                        "data": {
                            "proxy_service": "cors.bwa.workers.dev",
                            "target_url": full,
                            "chain": layers,
                        },
                        "observed_at": L.get("incident_ts"),
                        "time_basis": "source_metadata",
                        "source": "@src",
                        "files": [],
                    },
                    "tags": stag({
                        "lane": LANE,
                        "grade": "OBSERVED",
                        "legacy_kind": kind,
                        "venue": L.get("source_index"),
                        "task_family": L.get("task_family"),
                        "target_host": L.get("target_host"),
                        "decoded_target": dec,
                        "doc_id": L.get("doc_id"),
                        "source_url": d.get("source_url"),
                        "matched_string": d.get("matched_string"),
                        "legacy_fingerprint": d.get("fingerprint"),
                    }),
                })

            elif kind == "proxy_ladder":
                counts["proxy_ladder"] += 1
                outer = L.get("outer_wrapper")
                proxy = L.get("proxy")
                target = L.get("target_host")
                chain = [outer, proxy, target] if outer != proxy else \
                    [proxy, target]
                records.append({
                    "ref": "pl_%d" % counts["proxy_ladder"],
                    "kind": "observation",
                    "body": {
                        "type": "infra.proxy_chain",
                        "data_schema": "urn:factum:infra:proxy-chain:1",
                        "data": {
                            "proxy_service": proxy,
                            "target_url": target,
                            "chain": chain,
                        },
                        "observed_at": "2026-09-28T05:30:00Z",
                        "time_basis": "legacy_documented",
                        "source": "@src",
                        "files": [],
                    },
                    "tags": stag({
                        "lane": LANE,
                        "grade": "OBSERVED",
                        "legacy_kind": kind,
                        "occurrences": L.get("occurrences"),
                        "venues": L.get("venues"),
                        "edge": L.get("edge"),
                        "legacy_fingerprint": d.get("fingerprint"),
                        "note": "aggregate edge: target_url is the destination "
                                "host (ladder analysis output), not a full URL",
                    }),
                })

            elif kind == "proxy_family":
                host = L.get("proxy_host")
                if host in INST_HOSTS:
                    counts["proxy_family_dup"] += 1
                    drop_log.append({
                        "legacy_kind": kind, "reason": "duplicate",
                        "detail": "proxy_instance for %s already in corpus "
                                  "(lane %s)" % (host, INST_HOSTS[host][0]),
                        "legacy_fingerprint": d.get("fingerprint")})
                    continue
                counts["proxy_family_new"] += 1
                records.append({
                    "ref": "pf_%d" % counts["proxy_family_new"],
                    "kind": "observation",
                    "body": {
                        "type": "infra.proxy_instance",
                        "data_schema": "urn:factum:infra:proxy-instance:1",
                        "data": {
                            "host": host,
                            "invocation_shape": INVOCATION_SHAPES[host],
                            "access": "unknown",
                        },
                        "observed_at": "2026-09-28T05:30:00Z",
                        "time_basis": "legacy_documented",
                        "source": "@src",
                        "files": [],
                    },
                    "tags": stag({
                        "lane": LANE,
                        "grade": "OBSERVED",
                        "legacy_kind": kind,
                        "n_docs": L.get("n_docs"),
                        "n_occurrences": L.get("n_occurrences"),
                        "docs_per_index": L.get("docs_per_index"),
                        "top_targets": L.get("top_targets"),
                        "legacy_fingerprint": d.get("fingerprint"),
                        "shape_note": "invocation shape generalized from "
                                      "raw/other_workers_dev_hostnames.json "
                                      "sample_raw (passive corpus sweep; no "
                                      "live probing performed)",
                    }),
                })

            elif kind == "venue_summary":
                counts["venue_summary"] += 1
                venue_rows.append({
                    "venue": L.get("venue"),
                    "hit_count": L.get("hit_count"),
                    "context": L.get("context"),
                })

    records.append({
        "ref": "run",
        "kind": "run",
        "body": {
            "run_kind": "lane_ingest",
            "tool": "cors-bwa-proxy-ingest",
            "tool_version": "1",
            "started": "2026-10-10T06:00:00Z",
            "ended": "2026-10-10T06:30:00Z",
            "params": {
                "lane": LANE,
                "method": "per-row mapping from events.jsonl with "
                          "URL-variant dedup against exported corpus "
                          "batches; venue summaries as claims",
                "source_sidecar": "data/lanes/2025-09-26-cors-bwa-proxy/events.jsonl",
            },
            "coverage": {
                "description": "154 legacy aggregate events processed: 81 "
                               "submitted as observations, 6 venue summaries "
                               "as claims, 67 skipped as corpus duplicates.",
                "scanned": 154,
                "total": 154,
                "complete": True,
            },
        },
        "tags": {"lane": LANE, "grade": "OBSERVED"},
    })

    n_obs = (counts["proxied_target_new"] + counts["proxy_ladder"] +
             counts["proxy_family_new"])
    claims = [
        ("claim_coverage", "ingest_coverage", {
            "legacy_events": 154,
            "submitted_observations": n_obs,
            "venue_summary_claims": len(venue_rows),
            "skipped_duplicates": (counts["proxied_target_dup"] +
                                   counts["proxy_family_dup"]),
            "breakdown": counts,
        }),
        ("claim_dedup", "corpus_overlap", {
            "proxied_target_dupes_in_2026-10-01-intermediary-relays":
                counts["proxied_target_dup"],
            "proxy_family_dupes": counts["proxy_family_dup"],
            "note": "duplicate = same proxied URL already in Factum as "
                    "infra.proxy_chain (URL-variant match), or same host as "
                    "infra.proxy_instance. Skipped per pre-ingest dedup rule; "
                    "overlap listed in drop_log.json.",
        }),
        ("claim_venues", "venue_footprint", {
            "venues": venue_rows,
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
        "idempotency_key": "2025-09-26-cors-bwa-proxy-v1",
        "actor": ACTOR,
        "records": records,
    }
    json.dump(bundle, open(os.path.join(HERE, "bundle.json"), "w"),
              indent=1, ensure_ascii=False)
    json.dump({"dropped": drop_log,
               "counts": counts},
              open(os.path.join(HERE, "drop_log.json"), "w"),
              indent=1, ensure_ascii=False)
    print("records:", len(records), "counts:", counts)


if __name__ == "__main__":
    main()
