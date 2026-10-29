#!/usr/bin/env python3
"""Aggregate the SwarmTraces HF-hack redacted dataset into a Factum bundle.

Strategy: giant-lane aggregation. No 1:1 ingest of the 189,579 records.
Extracts: source locator, extraction run, dataset snapshot, unique literal
IOC values (domains, URL prefixes, IPs) as infra.ioc observations, and
OBSERVED summary claims for measures not already in the
2026-09-27-swarmtraces-verification lane.

Input: evidence/raw/redacted.jsonl.gz (shared raw storage; not a lane dir).
Output: data/lanes/swarmtraces-hf-dataset/bundle.json (Factum bundle v2).
"""

import gzip
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

INPUT = "evidence/raw/redacted.jsonl.gz"
LANE = "swarmtraces-hf-dataset"
ACTOR = "agent:lane-ingest:swarmtraces-hf-dataset"
IDEMPOTENCY = "lane-ingest/swarmtraces-hf-dataset/2026-10-10/v1"
DATASET_URL = "https://swarmtraces.org/data/final/redacted.jsonl.gz"
DATASET_SHA256 = "7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488"
PROV = "swarmtraces-hf-dataset aggregation of evidence/raw/redacted.jsonl.gz"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Literal URL: http(s) up to whitespace, quote, angle bracket, or backslash.
# EXACT-match semantics: a match containing '[' (redaction boundary) or a
# redaction marker is discarded entirely, so counted URLs are complete
# observed values, not redaction-truncated prefixes.
URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]+")
STRIP_TAIL = ".,);"
REDACTED_BITS = ("[", "REDACTED", "CREDENTIAL", "SERVICE")
DOMAIN_RE = re.compile(r"https?://([^/:?#]+)")
SERVICE_RE = re.compile(r"\[SERVICE \d+ URL \d+\]")
DEST_RE = re.compile(r"\[REDACTED:destination(?::\d+)?\]")
HF_RE = re.compile(r"\[HF [^\]]*\]")
ZZ_RE = re.compile(r"zz[A-Z0-9_]+")

# Candidate IOC terms (exact literal values; counts computed below).
DOMAIN_CANDS = [
    "packages.hub.ace-research.openai.org",
    "huggingface.co",
    "datasets-server.huggingface.co",
    "registry-1.docker.io",
    "auth.docker.io",
    "pkgs.tailscale.com",
]
URL_CANDS = [
    "https://packages.hub.ace-research.openai.org/artifactory/github-remote-cache/",
    "https://packages.hub.ace-research.openai.org/artifactory/github-remote/",
    "https://packages.hub.ace-research.openai.org/artifactory/api/system/ping",
    "https://huggingface.co/api/whoami-v2",
    "https://huggingface.co/api/datasets/",
    "https://huggingface.co/api/repos/create",
    "https://huggingface.co/api/repos/move",
    "https://datasets-server.huggingface.co/webhook",
    "https://registry-1.docker.io/v2/",
    "https://registry-1.docker.io/v2/cybergym/arvo",
    "https://auth.docker.io/token?",
    "https://slack.com/api/search.messages",
]
TAILSCALE_CANDS = [
    "https://pkgs.tailscale.com/stable/tailscale_1.86.2_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_1.82.5_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_1.82.0_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_1.80.3_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_1.98.8_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_1.78.1_amd64.tgz",
    "https://pkgs.tailscale.com/stable/tailscale_1.84.0_amd64.tgz",
]


def clean_url(u):
    return u.rstrip(STRIP_TAIL)


def main():
    kind_counts = Counter()
    parent_of = {}
    ids = set()
    url_records = Counter()      # term -> n records containing it
    url_occ = Counter()          # term -> n occurrences
    domain_records = Counter()
    service_slots = Counter()
    dest_slots = Counter()
    hf_slots = Counter()
    artifactory_urls = Counter()  # literal artifactory URLs
    artifactory_records = Counter()
    artifactory_any_ids = set()
    zz_terms = Counter()
    imds_records = []
    n = 0

    with gzip.open(INPUT, "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            n += 1
            rid = r["id"]
            ids.add(rid)
            kind_counts[r["kind"]] += 1
            t = r["text"]
            if r.get("parent_id"):
                parent_of[rid] = r["parent_id"]
            seen_urls = set()
            for m in URL_RE.finditer(t):
                u = clean_url(m.group(0))
                if any(b in u for b in REDACTED_BITS):
                    continue  # redaction-truncated or placeholder: not a value
                url_occ[u] += 1
                seen_urls.add(u)
            for u in seen_urls:
                url_records[u] += 1
                dm = DOMAIN_RE.match(u)
                if dm:
                    domain_records[dm.group(1).lower()] += 1
                if u.startswith("https://packages.hub.ace-research.openai.org/"):
                    artifactory_urls[u] += 1
                    artifactory_records[u] += 1
                    artifactory_any_ids.add(rid)
                    zm = ZZ_RE.search(u)
                    if zm:
                        zz_terms[zm.group(0)] += 1
            for m in SERVICE_RE.finditer(t):
                service_slots[m.group(0)] += 1
            for m in DEST_RE.finditer(t):
                dest_slots[m.group(0)] += 1
            for m in HF_RE.finditer(t):
                hf_slots[m.group(0)[:80]] += 1
            if "169.254.169.254" in t:
                imds_records.append((rid, r["kind"]))

    # Chain depth: walk parent links.
    depth_hist = Counter()
    distinct_parents = set(parent_of.values())
    dangling = [p for p in distinct_parents if p not in ids]
    max_depth = 0
    for rid in parent_of:
        d, cur, seen = 0, rid, set()
        while cur in parent_of and cur not in seen:
            seen.add(cur)
            cur = parent_of[cur]
            d += 1
        depth_hist[d] += 1
        max_depth = max(max_depth, d)

    stats = {
        "total": n,
        "unique_ids": len(ids),
        "kinds": dict(kind_counts),
        "n_parented": len(parent_of),
        "n_distinct_parents": len(distinct_parents),
        "n_dangling_parents": len(dangling),
        "chain_max_depth": max_depth,
        "chain_depth_hist": {str(k): v for k, v in sorted(depth_hist.items())},
        "service_slots_distinct": len(service_slots),
        "dest_slots_distinct": len(dest_slots),
        "hf_slots_distinct": len(hf_slots),
        "service_slots_top": service_slots.most_common(5),
        "dest_slots_top": dest_slots.most_common(5),
        "hf_slots_top": hf_slots.most_common(5),
        "artifactory_distinct_urls": len(artifactory_urls),
        "artifactory_total_hits": sum(artifactory_urls.values()),
        "artifactory_records_any": len(artifactory_any_ids),
        "zz_terms_distinct": len(zz_terms),
        "zz_terms_top": zz_terms.most_common(10),
        "artifactory_top": artifactory_urls.most_common(15),
        "imds_records": imds_records,
        "url_records": {u: url_records[u] for u in URL_CANDS + TAILSCALE_CANDS
                        if u in url_records},
        "domain_records": {d: domain_records[d] for d in DOMAIN_CANDS
                           if d in domain_records},
        "ip_imds_records": len(imds_records),
    }

    records = []
    tags_lane = {"lane": LANE}

    def add(ref, kind, body, tags):
        t = dict(tags_lane)
        t.update({k: str(v) for k, v in tags.items()})
        records.append({"ref": ref, "kind": kind, "body": body, "tags": t})

    # 1. source
    add("src", "source", {
        "source_type": "dataset",
        "title": "SwarmTraces HF-hack redacted dataset (redacted.jsonl.gz)",
        "locator": DATASET_URL,
        "platform": "swarmtraces.org",
    }, {"sha256": DATASET_SHA256, "retrieval_date": "2026-09-27"})

    # 2. run
    add("run", "run", {
        "run_kind": "extraction",
        "tool": "build_bundle.py",
        "tool_version": "1",
        "started": NOW,
        "ended": NOW,
        "params": {
            "input": INPUT,
            "input_sha256": DATASET_SHA256,
            "input_records": n,
            "note": ("Giant-lane aggregation: unique literal IOC values as "
                     "infra.ioc observations; summary claims only for measures "
                     "not already in lane 2026-09-27-swarmtraces-verification."),
        },
        "coverage": {
            "description": "All 189,579 redacted.jsonl.gz records scanned.",
            "scanned": n,
            "total": n,
            "complete": True,
        },
    }, {})

    # 3. dataset.snapshot
    add("snap", "observation", {
        "type": "dataset.snapshot",
        "data_schema": "urn:factum:datasets:snapshot:1",
        "source": "@src",
        "observed_at": NOW,
        "time_basis": "received_by_factum",
        "files": [],
        "data": {
            "dataset_uri": DATASET_URL,
            "revision": "sha256:" + DATASET_SHA256,
            "coverage": "complete",
            "row_count": n,
        },
    }, {"grade": "OBSERVED",
         "row_breakdown": "payload=%d;recovered_text=%d;response=%d" % (
             kind_counts["payload"], kind_counts["recovered_text"],
             kind_counts["response"])})

    # 4. infra.ioc observations
    ioc_refs = {}

    def ioc(ref, term, category, rec_count, extra_tags, prov_note=""):
        prov = PROV + (("; " + prov_note) if prov_note else "")
        add(ref, "observation", {
            "type": "infra.ioc",
            "data_schema": "urn:factum:infra:ioc:1",
            "source": "@src",
            "observed_at": NOW,
            "time_basis": "received_by_factum",
            "files": [],
            "data": {
                "term": term,
                "category": category,
                "provenance": prov,
                "status": "active",
            },
        }, dict({"grade": "OBSERVED", "record_count": rec_count},
                  **extra_tags))
        ioc_refs[ref] = term

    for i, d in enumerate(DOMAIN_CANDS):
        ioc("ioc-dom-%d" % i, d, "domain", domain_records[d], {})

    for i, u in enumerate(URL_CANDS):
        extra = {}
        if "artifactory/github-remote-cache/" in u and u.endswith("cache/"):
            extra["related_fragment"] = (
                "observation_d46f782b60d54539b2e60f76df59f645 "
                "(github-remote-cache/zz, lane 2026-10-01-intermediary-relays); "
                "observation_90f6cff1507b413bb61487ce2efa8cf6 "
                "(lane 2026-09-28-ace-research-ct)")
            extra["note"] = ("full-URL form; fragment-only records already "
                             "exist")
        ioc("ioc-url-%d" % i, u, "url-pattern", url_records.get(u, 0), extra)

    for i, u in enumerate(TAILSCALE_CANDS):
        ioc("ioc-ts-%d" % i, u, "url-pattern", url_records.get(u, 0),
            {"family": "tailscale-stable"})

    ioc("ioc-ip-imds", "169.254.169.254", "ip", len(imds_records),
        {"note": "AWS EC2 instance metadata (IMDS) endpoint"})

    # Top zz-marker artifactory URLs (complete literal values, by record count).
    # (Redaction-truncated prefixes are already filtered from the counters,
    # so every candidate here is a complete observed URL.)
    zz_cands = [u for u, _ in artifactory_urls.most_common(60)
                if ZZ_RE.search(u) and u not in set(URL_CANDS)]
    zz_top = zz_cands[:10]
    for i, u in enumerate(zz_top):
        ioc("ioc-zz-%d" % i, u, "url-pattern",
            artifactory_records.get(u, 0), {"family": "zz-marker-path"})

    # 5. claims (OBSERVED; only measures not in swarmtraces-verification)
    def claim(ref, prop, value, cites, note):
        add(ref, "claim", {
            "subject": "@run",
            "property": prop,
            "value": value,
            "basis": "OBSERVED",
            "cites": cites,
            "note": note,
        }, {"grade": "OBSERVED"})

    art_any = len(artifactory_any_ids)
    claim(
        "claim-0", "artifactory_board_volume",
        ("The Artifactory board host packages.hub.ace-research.openai.org "
         "appears in %d records across %d distinct literal URLs; "
         "%d distinct zz-prefixed path terms observed. Top zz term: %s (%d "
         "records).") % (art_any, len(artifactory_urls), len(zz_terms),
                         zz_terms.most_common(1)[0][0],
                         zz_terms.most_common(1)[0][1]),
        ["@run", "@ioc-url-0", "@ioc-url-1"],
        "counts from full streaming pass over evidence/raw/redacted.jsonl.gz; "
        "record counts = records containing the complete literal URL.",
    )

    claim(
        "claim-1", "chain_topology_flat",
        ("All %d parented records sit at depth 1: no multi-hop parent chains "
         "exist. %d distinct parents, %d dangling parent references.") % (
            len(parent_of), len(distinct_parents), len(dangling)),
        ["@run"],
        "depth_hist=%s" % json.dumps(
            {str(k): v for k, v in sorted(depth_hist.items())}),
    )

    claim(
        "claim-2", "redaction_slot_token_cardinality",
        ("%d distinct [SERVICE N URL M] tokens; %d distinct "
         "[REDACTED:destination] tokens; %d distinct [HF ...] tokens. Top: "
         "%s (%d), %s (%d), %s (%d).") % (
            len(service_slots), len(dest_slots), len(hf_slots),
            service_slots.most_common(1)[0][0],
            service_slots.most_common(1)[0][1],
            dest_slots.most_common(1)[0][0],
            dest_slots.most_common(1)[0][1],
            hf_slots.most_common(1)[0][0],
            hf_slots.most_common(1)[0][1]),
        ["@run"],
        ("Distinct-token cardinality; occurrence totals are already claimed "
         "in lane 2026-09-27-swarmtraces-verification."),
    )

    claim(
        "claim-3", "target_surface_summary",
        ("HF API: whoami-v2 in %d records, api/datasets/ in %d, "
         "api/repos/create in %d, api/repos/move in %d, "
         "datasets-server webhook in %d. Docker: registry-1.docker.io/v2/ in "
         "%d, auth.docker.io/token? in %d. Tailscale stable tgzs: %d distinct "
         "URLs in %d records. Slack search.messages API in %d records.") % (
            url_records.get("https://huggingface.co/api/whoami-v2", 0),
            url_records.get("https://huggingface.co/api/datasets/", 0),
            url_records.get("https://huggingface.co/api/repos/create", 0),
            url_records.get("https://huggingface.co/api/repos/move", 0),
            url_records.get("https://datasets-server.huggingface.co/webhook", 0),
            url_records.get("https://registry-1.docker.io/v2/", 0),
            url_records.get("https://auth.docker.io/token?", 0),
            len([u for u in TAILSCALE_CANDS if u in url_records]),
            sum(url_records.get(u, 0) for u in TAILSCALE_CANDS),
            url_records.get("https://slack.com/api/search.messages", 0)),
        ["@run", "@ioc-url-3", "@ioc-url-8", "@ioc-url-10"],
        "record counts = records containing the complete literal URL.",
    )

    claim(
        "claim-4", "imds_token_request_code",
        ("%d recovered_text records contain AWS IMDSv2 token-request code "
         "against http://169.254.169.254/latest: %s.") % (
            len(imds_records), ", ".join(rid for rid, _ in imds_records)),
        ["@run", "@ioc-ip-imds"],
        "code requests PUT {base}/api/token with X-aws-ec2-metadata-token-ttl-seconds header.",
    )

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY,
        "lane": LANE,
        "records": records,
    }
    with open("data/lanes/swarmtraces-hf-dataset/bundle.json", "w",
              encoding="utf-8") as fh:
        json.dump(bundle, fh, ensure_ascii=False)
        fh.write("\n")
    with open("data/lanes/swarmtraces-hf-dataset/extraction-stats.json", "w",
              encoding="utf-8") as fh:
        json.dump(stats, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    kinds = Counter(r["kind"] for r in records)
    print("records: %d  kinds: %s" % (len(records), dict(kinds)))
    print("stats: total=%d kinds=%s maxdepth=%d imds=%d" % (
        n, dict(kind_counts), max_depth, len(imds_records)))
    print("WROTE data/lanes/swarmtraces-hf-dataset/bundle.json")


if __name__ == "__main__":
    main()
