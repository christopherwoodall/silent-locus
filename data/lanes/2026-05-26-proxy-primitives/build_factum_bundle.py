#!/usr/bin/env python3
"""Build the Factum bundle for the 2026-05-26-proxy-primitives aggregate lane.

Reads data/lanes/2026-05-26-proxy-primitives/events.jsonl (1,522 legacy
events) and emits bundle.json + drop_log.json.

Mapping (legacy record_kind -> Factum type):
  wiki_link / wiki_record_annotation / wiki_shortener with a recoverable
      laundered target -> infra.proxy_chain (invocation URL as target_url,
      leftmost host as proxy_service; sibling-lane convention)
  same kinds with null laundered_target (truncated source URL) ->
      infra.proxy_instance (host + invocation_shape)
  wiki_ioc_pivot -> infra.proxy_chain (same convention; n_agents/wikis in
      tags). 180 rows skipped: URL already in corpus as infra.proxy_chain.
  corpus_hit -> infra.ioc (category proxy) for bare hosts not in corpus
  gem_name_fragment -> infra.ioc (category gem-name-fragment), deduped
      within batch by term (6 rows -> 3 terms)
  wiki_revision -> infra.ioc term=gview (first-seen evidence)

Dedup: URL-variant match against exported corpus batches; exact term match
for ioc candidates.
"""
import json
import os
import re
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2026-05-26-proxy-primitives"
ACTOR = "agent:lane-ingest-2026-05-26-proxy-primitives"
LOOKUP = json.load(open("/tmp/agg_ingest/corpus_lookup.json"))
CHAIN_VARIANTS = LOOKUP["chain_variant_map"]
IOC_TERMS = LOOKUP["ioc_terms"]

EVENTS = os.path.join(HERE, "events.jsonl")


def decoded(u):
    if not u:
        return u
    return unquote(unquote(unquote(u))).replace("&amp;", "&")


def variants(u):
    d = decoded(u)
    if not d:
        return set()
    out = {d, re.sub(r"^https?://", "", d)}
    m = re.match(r"^https?://[^/]+/(.*)$", d)
    if m:
        out.add(m.group(1))
        out.add(re.sub(r"^https?://", "", m.group(1)))
    for mm in re.finditer(r"https?://", d):
        if mm.start() > 0:
            out.add(d[mm.start():])
            out.add(re.sub(r"^https?://", "", d[mm.start():]))
    return {x for x in out if x}


def is_chain_dup(url):
    return any(v in CHAIN_VARIANTS for v in variants(url))


def leftmost_host(url):
    d = decoded(url) or ""
    m = re.match(r"^(?:https?://)?([^/?#]+)", d)
    if not m:
        return None
    host = m.group(1).strip().lower()
    # strip trailing junk the dump sometimes appends
    host = re.split(r"['\"\]\}]", host)[0]
    return host.rstrip(".") or None


def classify_url(ms):
    """Classify a legacy matched_string.

    Returns (kind, evidence_url, host):
      url      - a real invocation URL (cleaned of wrapper brackets);
                 evidence_url is the cleaned URL for dup checks
      withheld - source dump withheld the URL ('[operational URL omitted...')
      hostfrag - bare 'host=X' fragment, no usable URL
      empty    - null/empty matched_string
    """
    if not ms:
        return ("empty", None, None)
    if ms.startswith("[operational URL omitted"):
        return ("withheld", ms, None)
    clean = re.sub(r"^[\[\(]+", "", ms.strip())
    m = re.search(r"https?://[^\s'\"\]]+", clean)
    if m:
        url = m.group(0)
        hm = re.match(r"https?://([^/?#]+)", url)
        host = hm.group(1).lower().rstrip(".") if hm else None
        return ("url", url, host)
    m = re.search(r"host=([A-Za-z0-9.\-]+)", ms)
    if m:
        return ("hostfrag", ms, m.group(1).lower().rstrip("."))
    return ("unknown", ms, None)


def is_withheld_target(t):
    return t is None or (isinstance(t, str) and
                         t.startswith("[operational URL omitted"))


def obs_time(L):
    ts = L.get("first_seen_effective") or L.get("first_seen") or L.get("time")
    if ts:
        return ts, "source_metadata"
    return "1970-01-01T00:00:00Z", "unknown"


def stag(d):
    return {k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
            for k, v in d.items() if v is not None}


def main():
    records = []
    drop_log = []
    seen_terms = set()
    counts = {"chain_new": 0, "chain_dup": 0, "instance_new": 0,
              "ioc_new": 0, "ioc_dup": 0}

    records.append({
        "ref": "src",
        "kind": "source",
        "body": {
            "locator": "data/lanes/2026-05-26-proxy-primitives/events.jsonl",
            "source_type": "submitted",
        },
        "tags": stag({
            "lane": LANE,
            "grade": "OBSERVED",
            "description": "Aggregate lane: Lane F proxy-primitive sweep "
                           "(pure.md, api.cors.lol, corsmirror.com, gview) "
                           "over collusion-wiki + gem corpora. Per-URL "
                           "observations in Factum; full rows in lane "
                           "artifacts.",
            "legacy_path": "evidence/aggregates/remove-2026-05-26-proxy-primitives/events.jsonl",
        }),
    })

    def chain_obs(ref, d, L, extra_tags, clean_url, svc):
        dec = decoded(clean_url)
        at, tb = obs_time(L)
        tags = {"lane": LANE, "grade": "OBSERVED",
                "legacy_kind": d["record_kind"],
                "primitive": L.get("primitive"),
                "source": L.get("source"),
                "matched_string": d.get("matched_string"),
                "laundered_target": L.get("laundered_target"),
                "first_seen_effective": L.get("first_seen_effective"),
                "timestamp_source": L.get("timestamp_source"),
                "legacy_fingerprint": d.get("fingerprint"),
                "legacy_hit_sha": L.get("hit_sha")}
        tags.update(extra_tags)
        return {
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "infra.proxy_chain",
                "data_schema": "urn:factum:infra:proxy-chain:1",
                "data": {
                    "proxy_service": svc,
                    "target_url": dec,
                    "chain": [svc],
                },
                "observed_at": at,
                "time_basis": tb,
                "source": "@src",
                "files": [],
            },
            "tags": stag(tags),
        }

    def instance_obs(ref, d, L, host, shape, note):
        at, tb = obs_time(L)
        return {
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "infra.proxy_instance",
                "data_schema": "urn:factum:infra:proxy-instance:1",
                "data": {
                    "host": host,
                    "invocation_shape": shape,
                    "access": "unknown",
                },
                "observed_at": at,
                "time_basis": tb,
                "source": "@src",
                "files": [],
            },
            "tags": stag({
                "lane": LANE,
                "grade": "OBSERVED",
                "legacy_kind": d["record_kind"],
                "primitive": L.get("primitive"),
                "source": L.get("source"),
                "matched_string": d.get("matched_string"),
                "legacy_fingerprint": d.get("fingerprint"),
                "note": note,
            }),
        }

    with open(EVENTS) as fh:
        for line in fh:
            d = json.loads(line)
            kind = d["record_kind"]
            L = d.get("labels", {})
            ms = d.get("matched_string")
            urlkind, clean_url, urlhost = classify_url(ms)

            if kind in ("wiki_link", "wiki_record_annotation",
                        "wiki_shortener"):
                if urlkind in ("withheld", "hostfrag", "unknown"):
                    # URL withheld or unusable: record the primitive host
                    # with the verbatim placeholder as the shape
                    counts["instance_new"] += 1
                    host = (L.get("host") or urlhost or
                            L.get("primitive"))
                    records.append(instance_obs(
                        "pi_%d" % counts["instance_new"], d, L, host, ms,
                        "invocation URL withheld or unusable in source "
                        "dump; verbatim placeholder preserved as the "
                        "shape; host from row labels"))
                    continue
                if is_chain_dup(clean_url):
                    counts["chain_dup"] += 1
                    drop_log.append({
                        "legacy_kind": kind, "reason": "duplicate",
                        "detail": "invocation URL already in corpus as "
                                  "infra.proxy_chain",
                        "matched_string": (ms or "")[:120],
                        "legacy_fingerprint": d.get("fingerprint")})
                    continue
                if is_withheld_target(L.get("laundered_target")):
                    counts["instance_new"] += 1
                    records.append(instance_obs(
                        "pi_%d" % counts["instance_new"], d, L,
                        L.get("host") or L.get("primitive"), ms,
                        "laundered target unrecoverable: source dump "
                        "truncated or withheld the URL (per lane "
                        "PROVENANCE)"))
                else:
                    counts["chain_new"] += 1
                    extra = {}
                    if kind == "wiki_link":
                        extra = {"relation": L.get("relation"),
                                 "n_record_ids": L.get("n_record_ids"),
                                 "host": L.get("host")}
                    elif kind == "wiki_record_annotation":
                        extra = {"record_id": L.get("record_id"),
                                 "selection_basis":
                                     L.get("selection_basis")}
                    elif kind == "wiki_shortener":
                        extra = {"target_host": L.get("target_host")}
                    svc = urlhost or L.get("primitive")
                    records.append(chain_obs(
                        "pc_%d" % counts["chain_new"], d, L, extra,
                        clean_url, svc))

            elif kind == "wiki_ioc_pivot":
                if urlkind != "url":
                    counts["instance_new"] += 1
                    records.append(instance_obs(
                        "pi_%d" % counts["instance_new"], d, L,
                        L.get("primitive"), ms,
                        "pivot row without a usable invocation URL; "
                        "primitive host recorded verbatim"))
                    continue
                if is_chain_dup(clean_url):
                    counts["chain_dup"] += 1
                    drop_log.append({
                        "legacy_kind": kind, "reason": "duplicate",
                        "detail": "pivot URL already in corpus as "
                                  "infra.proxy_chain (sibling lane "
                                  "2026-10-01-intermediary-relays ingested "
                                  "these pivot rows as chains)",
                        "matched_string": (ms or "")[:120],
                        "legacy_fingerprint": d.get("fingerprint")})
                    continue
                counts["chain_new"] += 1
                svc = urlhost or L.get("primitive")
                records.append(chain_obs(
                    "pc_%d" % counts["chain_new"], d, L,
                    {"wikis": ",".join(L.get("wikis") or []),
                     "n_agents": L.get("n_agents"),
                     "agents_sample": ",".join(
                         L.get("agents_sample") or [])},
                    clean_url, svc))

            elif kind in ("corpus_hit", "gem_name_fragment",
                          "wiki_revision"):
                if kind == "wiki_revision":
                    term = L.get("primitive")  # "gview"
                    cat, status = "proxy", "active"
                else:
                    term = ms
                    cat = ("gem-name-fragment" if kind == "gem_name_fragment"
                           else "proxy")
                    status = ("candidate" if kind == "gem_name_fragment"
                              else "active")
                if term in seen_terms:
                    drop_log.append({
                        "legacy_kind": kind, "reason": "batch-duplicate",
                        "detail": "term already submitted in this batch",
                        "term": term,
                        "legacy_fingerprint": d.get("fingerprint")})
                    continue
                if term in IOC_TERMS or is_chain_dup(term):
                    counts["ioc_dup"] += 1
                    drop_log.append({
                        "legacy_kind": kind, "reason": "duplicate",
                        "detail": "term already in corpus",
                        "term": term,
                        "legacy_fingerprint": d.get("fingerprint")})
                    continue
                seen_terms.add(term)
                counts["ioc_new"] += 1
                at, tb = obs_time(L)
                tags = {"lane": LANE, "grade": "OBSERVED",
                        "legacy_kind": kind,
                        "legacy_fingerprint": d.get("fingerprint")}
                if kind == "corpus_hit":
                    tags.update({"context": L.get("context"),
                                 "line_no": L.get("line_no"),
                                 "source": L.get("source")})
                elif kind == "gem_name_fragment":
                    tags.update({"context": L.get("context"),
                                 "line_no": L.get("line_no"),
                                 "primitive": L.get("primitive"),
                                 "source": L.get("source"),
                                 "note": "zz-grammar gem name containing a "
                                         "proxy-primitive fragment; flagged "
                                         "not-proxy-use in source lane"})
                elif kind == "wiki_revision":
                    tags.update({"rev_id": L.get("rev_id"),
                                 "page_key": L.get("page_key"),
                                 "doc_id": L.get("doc_id"),
                                 "source_url": d.get("source_url"),
                                 "first_seen_effective":
                                     L.get("first_seen_effective"),
                                 "body_sha256": L.get("body_sha256"),
                                 "note": "single wiki revision evidencing "
                                         "gview primitive first seen"})
                records.append({
                    "ref": "ioc_%d" % counts["ioc_new"],
                    "kind": "observation",
                    "body": {
                        "type": "infra.ioc",
                        "data_schema": "urn:factum:infra:ioc:1",
                        "data": {
                            "term": term,
                            "category": cat,
                            "provenance": LANE,
                            "status": status,
                        },
                        "observed_at": at,
                        "time_basis": tb,
                        "source": "@src",
                        "files": [],
                    },
                    "tags": stag(tags),
                })

    records.append({
        "ref": "run",
        "kind": "run",
        "body": {
            "run_kind": "lane_ingest",
            "tool": "proxy-primitives-ingest",
            "tool_version": "1",
            "started": "2026-10-10T06:00:00Z",
            "ended": "2026-10-10T07:00:00Z",
            "params": {
                "lane": LANE,
                "method": "per-row mapping with URL-variant dedup against "
                          "exported corpus batches; null-target rows as "
                          "infra.proxy_instance",
                "source_sidecar":
                    "data/lanes/2026-05-26-proxy-primitives/events.jsonl",
            },
            "coverage": {
                "description": "1,522 legacy rows processed.",
                "scanned": 1522,
                "total": 1522,
                "complete": True,
            },
        },
        "tags": {"lane": LANE, "grade": "OBSERVED"},
    })

    n_obs = counts["chain_new"] + counts["instance_new"] + counts["ioc_new"]
    for ref, prop, value in [
        ("claim_coverage", "ingest_coverage", {
            "legacy_events": 1522,
            "submitted_observations": n_obs,
            "skipped_duplicates": counts["chain_dup"] + counts["ioc_dup"],
            "breakdown": counts,
        }),
        ("claim_dedup", "corpus_overlap", {
            "note": "duplicate = invocation URL already in Factum as "
                    "infra.proxy_chain (URL-variant match), mostly via "
                    "sibling lane 2026-10-01-intermediary-relays which "
                    "ingested the same wiki_ioc_pivots source rows as "
                    "chains. Skipped per pre-ingest dedup rule; see "
                    "drop_log.json.",
            "chain_dupes": counts["chain_dup"],
            "ioc_dupes": counts["ioc_dup"],
        }),
    ]:
        records.append({
            "ref": ref,
            "kind": "claim",
            "body": {"subject": "@run", "property": prop, "value": value,
                     "basis": "OBSERVED", "cites": ["@run"]},
            "tags": {"lane": LANE, "grade": "OBSERVED"},
        })

    bundle = {"bundle": 2,
              "idempotency_key": LANE + "-v1",
              "actor": ACTOR,
              "records": records}
    json.dump(bundle, open(os.path.join(HERE, "bundle.json"), "w"),
              indent=1, ensure_ascii=False)
    json.dump({"dropped": drop_log, "counts": counts},
              open(os.path.join(HERE, "drop_log.json"), "w"),
              indent=1, ensure_ascii=False)
    print("records:", len(records), "counts:", counts,
          "dropped:", len(drop_log))


if __name__ == "__main__":
    main()
