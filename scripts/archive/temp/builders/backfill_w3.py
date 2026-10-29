#!/usr/bin/env python3
"""Schema backfill 2026-09-29 (worker 3): pivot/hunt/forensics collections.

Mirrors scripts/backfill_schema_2026_09_28.py. Stdlib only, idempotent.
Rules:
  - Lossless: every original field survives. Non-canonical top-level keys
    move to labels (dotted lowercase keys); nested dicts flatten with dotted
    keys; empty nested dicts become null (documented in PROVENANCE); lists
    containing dicts/lists are JSON-encoded in place (documented).
  - Records that already carry event/fingerprint/@timestamp keep them
    verbatim. event.dataset is NEVER rewritten (yourls-resweep override
    preserved).
  - New event.created = backfill run time (UTC).
Usage: python3 temp/backfill_w3.py [--check]
"""

import hashlib
import json
import sys
import os
from datetime import datetime, timezone

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
SENTINEL = "1970-01-01T00:00:00Z"

CANONICAL_TOP = {
    "@timestamp", "event", "record_kind", "fingerprint", "labels",
    "observer", "retrieved_at", "retrieved_via", "source_url",
    "matched_string", "description", "note", "tags", "confidence",
    "sha256", "size_bytes", "file", "status", "observed_at",
}


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def new_event(dataset: str) -> dict:
    return {"dataset": dataset, "created": NOW}


def to_utc_z(ts: str) -> str:
    dt = datetime.fromisoformat(ts)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def loose_ts(value) -> str | None:
    if not value or not isinstance(value, str) or "x" in value:
        return None
    v = value.strip()
    try:
        if len(v) == 10:
            return to_utc_z(v + "T00:00:00+00:00")
        return to_utc_z(v)
    except ValueError:
        return None


def order(rec: dict) -> dict:
    first = ["@timestamp", "event", "record_kind", "fingerprint", "labels",
             "observer", "retrieved_at", "retrieved_via", "source_url",
             "matched_string", "description", "note", "tags", "confidence",
             "sha256", "size_bytes", "file", "status", "observed_at"]
    out = {k: rec[k] for k in first if k in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def labelify(value):
    """Make a value safe for flat ECS labels, losslessly."""
    if isinstance(value, dict):
        if not value:
            return None  # empty nested dict -> null (documented)
        raise ValueError("non-empty dict should have been flattened")
    if isinstance(value, list) and any(isinstance(i, (dict, list))
                                       for i in value):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return value


def flatten_into(labels: dict, key: str, value):
    if isinstance(value, dict) and value:
        for k, v in value.items():
            flatten_into(labels, f"{key}.{k}", v)
    else:
        labels[key] = labelify(value)


def move_to_labels(rec: dict, fields: list[str],
                   renames: dict | None = None) -> dict:
    renames = renames or {}
    labels = rec.get("labels", {})
    if not isinstance(labels, dict):
        raise ValueError(f"labels is not a dict: {type(labels)}")
    for f in fields:
        if f in rec:
            flatten_into(labels, renames.get(f, f), rec.pop(f))
    # also flatten any pre-existing nested labels (e.g. yourls empty dicts)
    for k in list(labels):
        v = labels[k]
        if isinstance(v, dict):
            labels.pop(k)
            flatten_into(labels, k, v)
        else:
            labels[k] = labelify(v)
    rec["labels"] = labels
    return rec


def expect_keys(rec: dict, allowed: set[str], ctx: str):
    extra = set(rec) - allowed - CANONICAL_TOP
    if extra:
        raise ValueError(f"{ctx}: unexpected top-level keys {sorted(extra)}")


def set_ts(rec: dict, value, source: str):
    """Set @timestamp from value, else sentinel; always record provenance."""
    ts = loose_ts(value)
    if ts:
        rec["@timestamp"] = ts
        rec["labels"]["timestamp_source"] = source
    else:
        rec["@timestamp"] = SENTINEL
        rec["labels"]["timestamp_source"] = "fallback:no_recoverable_date"


def uniq(fps: list[str], ctx: str, allow_dups: bool = False):
    # gomod-hunt contains exact duplicate rows (identical Path|Version|
    # Timestamp); identical records deterministically share a fingerprint.
    if not allow_dups:
        assert len(set(fps)) == len(fps), f"{ctx}: fingerprint collision!"


# ---------------------------------------------------------------- transforms

def t_exfil(rec: dict) -> dict:
    fields = ["identifier_id", "kind", "value", "full_payload", "carrier_gem",
              "carrier_version", "carrier_field", "wave", "xray_id", "source",
              "local_saved_copy", "in_our_diffend_corpus", "attribution_note",
              "upload_utc"]
    expect_keys(rec, set(fields), "exfil-endpoint-pivot")
    iid = rec["identifier_id"]
    rec = move_to_labels(rec, fields)
    rec["event"] = new_event("exfil-endpoint-pivot")
    rec["record_kind"] = "exfil_identifier"
    # upload_utc is messy multi-value prose; wave (2026-07-07) is the clean
    # campaign date for all rows -> midnight UTC.
    set_ts(rec, rec["labels"].get("wave"), "labels:wave")
    rec["fingerprint"] = fp(iid)
    return order(rec)


def t_forged_flag(rec: dict) -> dict:
    fields = ["task_id", "input_form", "flag_input", "flag", "flag_digest",
              "construction", "construction_version"]
    expect_keys(rec, set(fields), "forged-flag-hunt")
    flag = rec["flag"]
    rec = move_to_labels(rec, fields)
    rec["event"] = new_event("forged-flag-hunt")
    rec["record_kind"] = "forged_flag_ioc"
    set_ts(rec, None, "")
    rec["fingerprint"] = fp(flag)
    return order(rec)


def t_gem_temporal_check(rec: dict) -> dict:
    expect_keys(rec, {"name", "ok", "status"}, "gem-temporal-pivot/check")
    name = rec["name"]
    rec = move_to_labels(rec, ["name", "ok", "status"],
                         renames={"name": "gem.name"})
    rec["event"] = new_event("gem-temporal-pivot")
    rec["record_kind"] = "diffend_probe"
    rec["status"] = "probe-failed"
    set_ts(rec, None, "")
    rec["fingerprint"] = fp("diffend_targeted_check|" + name)
    return order(rec)


def t_gem_temporal_sweep(rec: dict) -> dict:
    expect_keys(rec, {"name", "in_diffend", "http_status", "versions",
                      "out_of_window"}, "gem-temporal-pivot/sweep")
    name = rec["name"]
    rec = move_to_labels(rec, ["name", "in_diffend", "http_status",
                               "versions", "out_of_window"],
                         renames={"name": "gem.name"})
    rec["event"] = new_event("gem-temporal-pivot")
    rec["record_kind"] = "diffend_probe"
    set_ts(rec, None, "")
    rec["fingerprint"] = fp("diffend_temporal_sweep|" + name)
    return order(rec)


def t_gomod(rec: dict) -> dict:
    expect_keys(rec, {"Path", "Version", "Timestamp"}, "gomod-hunt")
    ident = rec["Path"] + "|" + rec["Version"]
    ts = rec["Timestamp"]
    rec = move_to_labels(rec, ["Path", "Version", "Timestamp"],
                         renames={"Path": "gomod.path",
                                  "Version": "gomod.version",
                                  "Timestamp": "gomod.timestamp"})
    rec["event"] = new_event("gomod-hunt")
    rec["record_kind"] = "gomod_proxy_match"
    set_ts(rec, ts, "labels:gomod.timestamp")
    rec["fingerprint"] = fp(ident)
    return order(rec)


def t_july6(rec: dict) -> dict:
    # Already schema-shaped; only fingerprint is missing.
    expect_keys(rec, set(), "july6-staging")
    if "fingerprint" not in rec:
        rec["fingerprint"] = fp(rec["labels"]["doc_id"])
    return order(rec)


def t_july7_specimens(rec: dict) -> dict:
    fields = ["author", "exfil_endpoint", "exfil_kind", "engine_probe",
              "field", "gem", "mechanism", "payload_bytes", "payload_note",
              "source", "version", "xray_id", "upload_utc"]
    expect_keys(rec, set(fields), "july7-gem-forensics/specimens")
    xr = rec["xray_id"]
    upl = rec.get("upload_utc")
    rec = move_to_labels(rec, fields,
                         renames={"gem": "gem.name",
                                  "version": "gem.version",
                                  "field": "gem.field"})
    rec["event"] = new_event("july7-gem-forensics")
    rec["record_kind"] = "campaign_specimen"
    set_ts(rec, upl, "labels:upload_utc")
    rec["fingerprint"] = fp(xr)
    return order(rec)


def t_july7_payloads(rec: dict) -> dict:
    expect_keys(rec, {"gem", "version", "source_file", "text_lines_scanned",
                      "payload_lines", "payload_line_count"},
                "july7-gem-forensics/payloads")
    ident = rec["gem"] + "|" + rec["version"] + "|" + rec["source_file"]
    rec = move_to_labels(rec, ["gem", "version", "source_file",
                               "text_lines_scanned", "payload_lines",
                               "payload_line_count"],
                         renames={"gem": "gem.name",
                                  "version": "gem.version"})
    rec["event"] = new_event("july7-gem-forensics")
    rec["record_kind"] = "payload_reconstruction"
    set_ts(rec, None, "")
    rec["fingerprint"] = fp(ident)
    return order(rec)


def t_pastebin_pivot(rec: dict) -> dict:
    fields = ["date", "evidence_grade", "hit_id", "marker_matched", "source",
              "url_or_id", "verbatim_snippet", "why_agent_linked",
              "writer_assessment"]
    expect_keys(rec, set(fields), "pastebin-pivot")
    hid = rec["hit_id"]
    date = rec["date"]
    rec = move_to_labels(rec, fields)
    rec["event"] = new_event("pastebin-pivot")
    rec["record_kind"] = "pastebin_pivot_hit"
    set_ts(rec, date, "labels:date")
    rec["fingerprint"] = fp(hid)
    return order(rec)


def t_separate_eval(rec: dict) -> dict:
    fields = ["artifact_shape_fit", "date", "mechanism_match", "name",
              "operator", "sources", "task_list", "verdict", "verdict_reason"]
    expect_keys(rec, set(fields), "separate-eval-test")
    name = rec["name"]
    rec = move_to_labels(rec, fields)
    rec["event"] = new_event("separate-eval-test")
    rec["record_kind"] = "eval_candidate"
    # date is prose ("2025-05 (arXiv 2505.15216)"), not an event time.
    set_ts(rec, None, "")
    rec["fingerprint"] = fp(name)
    return order(rec)


def t_wayback(rec: dict) -> dict:
    fields = ["archived_go_import_tag", "archived_owner", "archived_page_state",
              "archived_version_tab", "archived_yanked_by", "bytes",
              "diffend_import_path", "diffend_payload_url", "diffend_summary",
              "diffend_vcs", "kind", "replay_status", "replay_url",
              "saved_file", "target", "verdict", "wayback_capture_ts"]
    expect_keys(rec, set(fields) | {"sha256"}, "wayback-gem-capture")
    ts_raw = rec["wayback_capture_ts"]  # wayback 14-digit capture stamp
    ident = rec["target"] + "|" + ts_raw
    replay = rec["replay_url"]
    rec = move_to_labels(rec, fields,
                         renames={"replay_url": "wayback.replay_url",
                                  "wayback_capture_ts":
                                      "wayback.capture_ts_raw"})
    rec["source_url"] = replay  # canonical name, same value
    rec["event"] = new_event("wayback-gem-capture")
    rec["record_kind"] = "wayback_capture"
    try:
        dt = datetime.strptime(ts_raw, "%Y%m%d%H%M%S").replace(
            tzinfo=timezone.utc)
        rec["@timestamp"] = dt.isoformat().replace("+00:00", "Z")
        rec["labels"]["timestamp_source"] = "labels:wayback.capture_ts_raw"
    except ValueError:
        set_ts(rec, None, "")
    rec["fingerprint"] = fp(ident)
    return order(rec)


def t_xss_census(rec: dict) -> dict:
    fields = ["payload_id", "family", "tier", "mechanism", "text_bytes",
              "text", "truncated", "first_seen", "markers_present",
              "markers_absent", "notes", "source", "source_ref"]
    expect_keys(rec, set(fields) | {"sha256"}, "xss-ssti-census")
    pid = rec["payload_id"]
    fs = rec.get("first_seen")  # e.g. "July 07, 2026 07:47" (UTC) or None
    rec = move_to_labels(rec, fields)
    rec["event"] = new_event("xss-ssti-census")
    rec["record_kind"] = "xss_ssti_payload"
    ts = None
    if fs:
        try:
            ts = datetime.strptime(fs, "%B %d, %Y %H:%M").replace(
                tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        except ValueError:
            ts = None
    if ts:
        rec["@timestamp"] = ts
        rec["labels"]["timestamp_source"] = "labels:first_seen"
    else:
        set_ts(rec, None, "")
    rec["fingerprint"] = fp(pid)
    return order(rec)


def t_yourls(rec: dict) -> dict:
    # Already schema-shaped except fingerprint. event.dataset
    # "yourls-resweep" is a registered override -- preserve verbatim.
    expect_keys(rec, set(), "yourls-resweep")
    rec = move_to_labels(rec, [])  # flattens empty nested dicts to null
    if "fingerprint" not in rec:
        rec["fingerprint"] = fp(rec["labels"]["event_id"])
    return order(rec)


JOBS = [
    ("data/exfil-endpoint-pivot/identifiers.jsonl", t_exfil),
    ("data/forged-flag-hunt/iocs.jsonl", t_forged_flag),
    ("data/gem-temporal-pivot/diffend_targeted_check.jsonl",
     t_gem_temporal_check),
    ("data/gem-temporal-pivot/diffend_temporal_sweep.jsonl",
     t_gem_temporal_sweep),
    *[("data/gomod-hunt/matches_%d.jsonl" % i, t_gomod) for i in range(1, 9)],
    ("data/july6-staging/hits.jsonl", t_july6),
    ("data/july7-gem-forensics/campaign-specimens-jfrog.jsonl",
     t_july7_specimens),
    ("data/july7-gem-forensics/payload-reconstructions.jsonl",
     t_july7_payloads),
    ("data/pastebin-pivot/hits.jsonl", t_pastebin_pivot),
    ("data/separate-eval-test/candidates.jsonl", t_separate_eval),
    ("data/wayback-gem-capture/hits.jsonl", t_wayback),
    ("data/xss-ssti-census/payloads.jsonl", t_xss_census),
    ("data/yourls-resweep-2026-09-28/yourls-resweep-2026-09-28.jsonl",
     t_yourls),
]


def validate(rec: dict, ctx: str):
    assert rec.get("event", {}).get("dataset"), f"{ctx}: event.dataset missing"
    assert rec.get("record_kind"), f"{ctx}: record_kind missing"
    assert rec.get("fingerprint"), f"{ctx}: fingerprint missing"
    assert isinstance(rec.get("labels"), dict), f"{ctx}: labels not a dict"
    stray = set(rec) - CANONICAL_TOP
    assert not stray, f"{ctx}: non-canonical top-level keys {sorted(stray)}"
    to_utc_z(rec["@timestamp"])


def main():
    check_only = "--check" in sys.argv
    total = 0
    for rel, fn in JOBS:
        allow = rel.startswith("data/gomod-hunt/")
        p = f"{REPO}/{rel}"
        lines = open(p, encoding="utf-8").read().splitlines()
        out, fps = [], []
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            rec = json.loads(line)
            if (rec.get("fingerprint") and rec.get("event") and
                    rec.get("record_kind") and
                    not (set(rec) - CANONICAL_TOP)):
                rec = order(move_to_labels(rec, []))  # already transformed
            else:
                rec = fn(rec)
            validate(rec, f"{rel}:{i}")
            fps.append(rec["fingerprint"])
            out.append(json.dumps(rec, ensure_ascii=False))
        uniq(fps, rel, allow_dups=allow)
        total += len(out)
        if not check_only:
            open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
        print(f"{'checked' if check_only else 'rewrote'} {rel}: "
              f"{len(out)} records")
    print(f"total: {total} records")


if __name__ == "__main__":
    main()
