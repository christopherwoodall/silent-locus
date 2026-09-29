#!/usr/bin/env python3
"""Schema backfill 2026-09-28: bring pre-convention datasets onto the shared schema.

Target layout (from conforming datasets + notes/schema/ecs-mapping.md):
  @timestamp, event {dataset, created}, record_kind, fingerprint,
  labels {dataset-specific fields, dotted keys}, plus existing canonical
  top-level fields (observer, source_url, description, note, tags, ...).

Rules:
  - Lossless: every original field survives (moved, never dropped), EXCEPT
    fields proven pure duplicates (admin _id == event_id, rollup _id ==
    labels.doc_id, webhook wave == labels.gem.wave) which are dropped and
    logged.
  - fingerprint = sha256 of a deterministic identity string (existing
    fingerprints are kept untouched).
  - event.created for new event dicts = backfill run time (UTC).
  - Fails loudly on unexpected top-level keys instead of dropping them.

Usage: python3 scripts/backfill_schema_2026_09_28.py [--check]
  --check: validate only, write nothing.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone

REPO = __file__.rsplit("/scripts/", 1)[0]
NOW = datetime.now(timezone.utc).isoformat()

CANONICAL_TOP = {
    "@timestamp", "event", "record_kind", "fingerprint", "labels",
    "observer", "retrieved_at", "retrieved_via", "source_url",
    "matched_string", "description", "note", "tags", "confidence",
    "sha256", "size_bytes", "file", "status",
    # NOTE: observed_at is NOT a canonical top-level field. The schema
    # contract (schema/record.schema.json: "Dataset-specific fields live
    # here [labels], never at top level") puts it under labels, which is
    # where every existing record carries it (labels.observed_at).
    # Keeping it here would let order()/validate() bless a top-level
    # observed_at that scripts/validate_schema.py (correctly) rejects.
}


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def new_event(dataset: str) -> dict:
    return {"dataset": dataset, "created": NOW}


def to_utc_z(ts: str) -> str:
    """Normalize an ISO-8601 timestamp to UTC with Z suffix."""
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def loose_ts(value) -> str | None:
    """Best-effort timestamp: full ISO, or date-only -> midnight UTC.
    Returns None for redacted (contains 'x'), None, or unparseable values."""
    if not value or not isinstance(value, str) or "x" in value:
        return None
    v = value.strip()
    try:
        if len(v) == 10:  # YYYY-MM-DD
            return to_utc_z(v + "T00:00:00+00:00")
        return to_utc_z(v)
    except ValueError:
        return None


def order(rec: dict) -> dict:
    """Stable human-friendly key order: canonical fields first."""
    first = ["@timestamp", "event", "record_kind", "fingerprint", "labels",
             "observer", "retrieved_at", "retrieved_via", "source_url",
             "matched_string", "description", "note", "tags", "confidence",
             "sha256", "size_bytes", "file", "status"]
    # (no "observed_at": schema contract keeps it under labels; see
    # CANONICAL_TOP note)
    out = {k: rec[k] for k in first if k in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def move_to_labels(rec: dict, fields: list[str], renames: dict | None = None) -> dict:
    """Move dataset-specific top-level fields under labels (dotted renames ok)."""
    renames = renames or {}
    labels = rec.get("labels", {})
    if not isinstance(labels, dict):
        raise ValueError(f"labels is not a dict: {type(labels)}")
    for f in fields:
        if f in rec:
            labels[renames.get(f, f)] = rec.pop(f)
    rec["labels"] = labels
    return rec


def expect_keys(rec: dict, allowed: set[str], ctx: str):
    extra = set(rec) - allowed - CANONICAL_TOP
    if extra:
        raise ValueError(f"{ctx}: unexpected top-level keys {sorted(extra)}")


# ---------------------------------------------------------------- transforms

def t_admin_explicit(rec: dict) -> dict:
    expect_keys(rec, {"event_id", "event_type", "wiki", "page", "page_key",
                      "time", "time_grade", "winning_clock",
                      "uncertainty_seconds", "request_time", "success_time",
                      "write_date", "rcs_date", "recent_changes_time",
                      "clock_delta_seconds", "success_observed",
                      "request_action", "change_summary", "actor_label",
                      "ip16", "revision_ref", "related_event_id",
                      "relation_type", "round_id", "page_held", "source_refs",
                      "clock_note", "_id"},
                "admin-deletions/explicit")
    assert rec["_id"] == rec["event_id"], "admin _id diverged from event_id!"
    rec.pop("_id")  # pure duplicate of event_id (verified on all 5,217 rows)
    eid = rec["event_id"]
    rec = move_to_labels(rec, ["event_id", "event_type", "wiki", "page",
                               "page_key", "time", "time_grade",
                               "winning_clock", "uncertainty_seconds",
                               "request_time", "success_time", "write_date",
                               "rcs_date", "recent_changes_time",
                               "clock_delta_seconds", "success_observed",
                               "request_action", "change_summary",
                               "actor_label", "ip16", "revision_ref",
                               "related_event_id", "relation_type",
                               "round_id", "page_held", "source_refs",
                               "clock_note"])
    rec["fingerprint"] = fp(eid)
    return order(rec)


def t_admin_rollup(rec: dict) -> dict:
    expect_keys(rec, {"_id"}, "admin-deletions/rollup")
    assert rec["_id"] == rec["labels"]["doc_id"], "rollup _id diverged!"
    rec.pop("_id")  # pure duplicate of labels.doc_id (verified on 26 rows)
    rec["fingerprint"] = fp(rec["labels"]["doc_id"])
    return order(rec)


def t_transfer_test(rec: dict) -> dict:
    expect_keys(rec, {"paste_id", "title", "author", "created_utc",
                      "body_bytes", "body_sha256", "body_markers",
                      "file_drops", "observed_utc", "checked_utc",
                      "http_status", "probed_utc", "pattern", "query",
                      "result", "scope", "searched_utc", "surface", "url"},
                "2026-07-21-transfer-test-family")
    rec = move_to_labels(rec, ["paste_id", "title", "author", "created_utc",
                               "body_bytes", "body_sha256", "body_markers",
                               "file_drops", "observed_utc", "checked_utc",
                               "http_status", "probed_utc", "pattern",
                               "query", "result", "scope", "searched_utc",
                               "surface"])
    # url and source_url never co-occur; coalesce to canonical source_url
    url = rec.pop("url", None)
    if not rec.get("source_url"):
        if url:
            rec["source_url"] = url
    elif url:
        rec["labels"]["url"] = url
    # note is canonical top-level; keep where it is
    rec["event"] = new_event("2026-07-21-transfer-test-family")
    lab = rec["labels"]
    for cand in ("created_utc", "probed_utc", "searched_utc", "checked_utc",
                 "observed_utc"):
        ts = loose_ts(lab.get(cand))
        if ts:
            rec["@timestamp"] = ts
            break
    # paste_id for pastes; probes/negatives fall back to kind+target
    # (url was coalesced into source_url above)
    pid = lab.get("paste_id")
    if pid:
        rec["fingerprint"] = fp(pid)
    else:
        target = (rec.get("source_url") or lab.get("query")
                  or lab.get("surface") or "")
        rec["fingerprint"] = fp(rec["record_kind"] + "|" + target)
    return order(rec)


def t_pastebin_sweep(rec: dict) -> dict:
    expect_keys(rec, {"venue", "observed_utc", "lane", "result",
                      "surface_url", "markers_checked", "detail"},
                "2026-09-28-pastebin-cluster-sweep")
    rec = move_to_labels(rec, ["venue", "observed_utc", "lane", "result",
                               "markers_checked", "detail"])
    rec["source_url"] = rec.pop("surface_url")  # canonical name, same value
    rec["event"] = new_event("2026-09-28-pastebin-cluster-sweep")
    rec["@timestamp"] = to_utc_z(rec["labels"]["observed_utc"])
    # existing md5 fingerprint kept untouched
    return order(rec)


def t_gem_graph_nodes(rec: dict) -> dict:
    expect_keys(rec, {"id", "label", "type", "subtype", "package", "status",
                      "first_seen", "last_seen", "timestamp_source",
                      "date_precision", "label_truncated", "value"},
                "gem-graph-nodes")
    gid = rec["id"]
    rec = move_to_labels(rec, ["id", "label", "type", "subtype", "package",
                               "status", "first_seen", "last_seen",
                               "timestamp_source", "date_precision",
                               "label_truncated", "value"],
                         renames={"id": "node.id", "label": "node.label",
                                  "type": "node.type",
                                  "subtype": "node.subtype",
                                  "package": "node.package",
                                  "status": "node.status",
                                  "label_truncated": "node.label_truncated",
                                  "value": "node.value"})
    rec["event"] = new_event("gem-graph-nodes")
    rec["record_kind"] = "graph_node"
    rec["@timestamp"] = to_utc_z(rec["labels"]["first_seen"])
    rec["fingerprint"] = fp(gid)
    return order(rec)


def t_collusion_wiki(rec: dict) -> dict:
    # Same event shape as admin-deletions explicit (shared tooling).
    fields = ["event_id", "event_type", "wiki", "page", "page_key", "time",
              "time_grade", "winning_clock", "uncertainty_seconds",
              "request_time", "success_time", "write_date", "rcs_date",
              "recent_changes_time", "clock_delta_seconds",
              "success_observed", "request_action", "change_summary",
              "actor_label", "ip16", "revision_ref", "related_event_id",
              "relation_type", "round_id", "page_held", "source_refs",
              "clock_note", "param_family"]
    expect_keys(rec, set(fields), "collusion-wiki/events")
    eid = rec["event_id"]
    rec = move_to_labels(rec, fields)
    rec["event"] = new_event("2026-05-17-collusion-wiki")
    rec["record_kind"] = "wiki_event"
    rec["@timestamp"] = to_utc_z(rec["labels"]["time"])
    rec["fingerprint"] = fp(eid)
    return order(rec)


def t_iowacollab(rec: dict) -> dict:
    expect_keys(rec, {"id", "body_sha256", "body_bytes", "title", "handle",
                      "source_urls", "wayback_view_snapshot",
                      "wayback_raw_snapshot", "body_origin",
                      "created_reported", "source_date_literals", "expire",
                      "relay_cluster", "corroboration", "origin_kinds",
                      "corpus_record_ids", "live_status", "live_checked_at",
                      "retrieved_via"},
                "2026-05-17-iowacollab-pastes")
    # retrieved_via is canonical top-level already; keep it there
    keep = rec.pop("retrieved_via")
    rec = move_to_labels(rec, ["id", "body_sha256", "body_bytes", "title",
                               "handle", "source_urls",
                               "wayback_view_snapshot",
                               "wayback_raw_snapshot", "body_origin",
                               "created_reported", "source_date_literals",
                               "expire", "relay_cluster", "corroboration",
                               "origin_kinds", "corpus_record_ids",
                               "live_status", "live_checked_at"])
    rec["retrieved_via"] = keep
    rec["event"] = new_event("2026-05-17-iowacollab-pastes")
    rec["record_kind"] = "relay_paste"
    # No clean timestamp exists (live_checked_at/created_reported are
    # annotated prose like "2026-09-28T03:2xZ (GET /view/<id> -> 404)").
    # Omit @timestamp rather than fabricate one.
    rec["fingerprint"] = fp(rec["labels"]["body_sha256"])
    return order(rec)


def t_timeline_anchors(rec: dict) -> dict:
    expect_keys(rec, {"_id"}, "2026-03-07-timeline-anchors")
    aid = rec.pop("_id")
    labels = rec.setdefault("labels", {})
    labels["_id"] = aid  # ES artifact preserved under labels
    rec["@timestamp"] = to_utc_z(rec["@timestamp"])  # fixes the +02:00 row
    rec["fingerprint"] = fp(aid)
    return order(rec)


def t_webhook_deaddrops(rec: dict) -> dict:
    expect_keys(rec, {"doc_id", "gem", "package", "version", "published_at",
                      "published_at_source", "wave", "marker",
                      "matched_pattern", "evidence", "evidence_level",
                      "diff_url", "in_corpus_harvest", "jfrog_inventory",
                      "jfrog_xray_id", "meta_authors", "meta_homepage",
                      "meta_summary", "source", "versions", "version_count"},
                "2026-05-12-webhook-deaddrops")
    if "wave" in rec:
        assert rec["wave"] == rec["labels"].get("gem.wave"), "wave diverged!"
        rec.pop("wave")  # pure duplicate of labels.gem.wave (verified)
    doc_id = rec["doc_id"]
    rec = move_to_labels(rec, ["doc_id", "gem", "package", "version",
                               "published_at", "published_at_source",
                               "marker", "matched_pattern", "evidence",
                               "evidence_level", "diff_url",
                               "in_corpus_harvest", "jfrog_inventory",
                               "jfrog_xray_id", "meta_authors",
                               "meta_homepage", "meta_summary", "source",
                               "versions", "version_count"],
                         renames={"doc_id": "doc_id",
                                  "gem": "gem.name",
                                  "package": "gem.package",
                                  "version": "gem.version",
                                  "published_at": "published.at",
                                  "published_at_source":
                                      "published.at_source",
                                  "marker": "marker",
                                  "matched_pattern": "matched_pattern",
                                  "evidence": "evidence",
                                  "evidence_level": "evidence.level_detail",
                                  "diff_url": "diff_url",
                                  "in_corpus_harvest": "in_corpus_harvest",
                                  "jfrog_inventory": "jfrog.inventory",
                                  "jfrog_xray_id": "jfrog.xray_id",
                                  "meta_authors": "meta.authors",
                                  "meta_homepage": "meta.homepage",
                                  "meta_summary": "meta.summary",
                                  "source": "source",
                                  "versions": "versions",
                                  "version_count": "version_count"})
    rec["fingerprint"] = fp(doc_id)
    return order(rec)


def t_gem_ioc_log(rec: dict) -> dict:
    expect_keys(rec, {"gem", "version", "published_at", "authors",
                      "expected_sha256", "download_url", "diff_url",
                      "diffend_versions", "error", "extracted_at",
                      "extracted_to", "file_count", "files",
                      "ioc_distinct_values", "meta_authors",
                      "meta_description", "meta_homepage", "meta_licenses",
                      "meta_summary", "published_at_source", "sha_mismatch"},
                "gem-ioc-log")
    rec = move_to_labels(rec, ["gem", "version", "published_at", "authors",
                               "expected_sha256", "diff_url",
                               "diffend_versions", "error", "extracted_at",
                               "extracted_to", "file_count", "files",
                               "ioc_distinct_values", "meta_authors",
                               "meta_description", "meta_homepage",
                               "meta_licenses", "meta_summary",
                               "published_at_source", "sha_mismatch"],
                         renames={"gem": "gem.name",
                                  "version": "gem.version",
                                  "published_at": "published.at",
                                  "authors": "authors",
                                  "expected_sha256": "expected_sha256",
                                  "diff_url": "diff_url",
                                  "diffend_versions": "diffend.versions",
                                  "error": "error",
                                  "extracted_at": "extracted.at",
                                  "extracted_to": "extracted.to",
                                  "file_count": "extracted.file_count",
                                  "files": "files",
                                  "ioc_distinct_values":
                                      "ioc.distinct_values",
                                  "meta_authors": "meta.authors",
                                  "meta_description": "meta.description",
                                  "meta_homepage": "meta.homepage",
                                  "meta_licenses": "meta.licenses",
                                  "meta_summary": "meta.summary",
                                  "published_at_source":
                                      "published.at_source",
                                  "sha_mismatch": "sha_mismatch"})
    if "download_url" in rec:
        # canonical name, same value (only 3 of 1262 rows carry it)
        rec["source_url"] = rec.pop("download_url")
    # retrieved_via / retrieved_at / sha256 / size_bytes / note already
    # canonical top-level; keep where they are
    rec["event"] = new_event("gem-ioc-log")
    for cand in ("retrieved_at", "extracted_at", "published_at"):
        ts = loose_ts(rec.get(cand))
        if ts:
            rec["@timestamp"] = ts
            break
    rec["fingerprint"] = fp(rec["labels"]["gem.name"] + "|" +
                            (rec["labels"].get("gem.version") or ""))
    return order(rec)


JOBS = [
    ("data/2026-06-04-admin-deletions/events.jsonl",
     t_admin_explicit),
    ("data/2026-06-04-admin-deletions/rollup.jsonl",
     t_admin_rollup),
    ("data/2026-07-21-transfer-test-family/events.jsonl",
     t_transfer_test),
    ("data/2026-09-28-pastebin-cluster-sweep/events.jsonl",
     t_pastebin_sweep),
    ("data/2025-03-04-rubygems-goimport-campaign/raw/gem-graph-nodes.jsonl",
     t_gem_graph_nodes),
    ("data/2026-05-17-collusion-wiki/events.jsonl",
     t_collusion_wiki),
    ("data/2026-05-17-iowacollab-pastes/events.jsonl",
     t_iowacollab),
    ("data/2026-03-07-timeline-anchors/events.jsonl",
     t_timeline_anchors),
    ("data/2026-05-12-webhook-deaddrops/events.jsonl",
     t_webhook_deaddrops),
    ("data/2025-03-04-rubygems-goimport-campaign/raw/gem-ioc-log.jsonl",
     t_gem_ioc_log),
]


def validate(rec: dict, ctx: str):
    """Post-transform conformance check."""
    assert rec.get("event", {}).get("dataset"), f"{ctx}: event.dataset missing"
    assert rec.get("record_kind"), f"{ctx}: record_kind missing"
    assert rec.get("fingerprint"), f"{ctx}: fingerprint missing"
    assert isinstance(rec.get("labels"), dict), f"{ctx}: labels not a dict"
    stray = set(rec) - CANONICAL_TOP
    assert not stray, f"{ctx}: non-canonical top-level keys {sorted(stray)}"
    if "@timestamp" in rec:
        to_utc_z(rec["@timestamp"])  # raises if unparseable


def main():
    check_only = "--check" in sys.argv
    total = 0
    for rel, fn in JOBS:
        p = f"{REPO}/{rel}"
        lines = open(p).read().splitlines()
        out = []
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            rec = fn(json.loads(line))
            validate(rec, f"{rel}:{i}")
            out.append(json.dumps(rec, ensure_ascii=False))
        total += len(out)
        if not check_only:
            open(p, "w").write("\n".join(out) + "\n")
        print(f"{'checked' if check_only else 'rewrote'} {rel}: "
              f"{len(out)} records")
    print(f"total: {total} records")


if __name__ == "__main__":
    main()
