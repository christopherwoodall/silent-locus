#!/usr/bin/env python3
"""Map Arquivo.pt CDX rows (2026-10-01 pull) into the openai-agent-traces corpus.

Source: data/2026-10-01-arquivo-pt/raw/*.cdx.jsonl.gz (read-only; never modified).
Output: openai-agent-traces/data/traces.jsonl (one mapped trace per deduped row).

Idempotency:
  * dedup key = timestamp + url (per incident slug); first-seen row wins.
  * trace_id = sha256("arquivo-pt|<slug>|<timestamp>|<url>") -> deterministic;
    re-runs produce identical trace_ids, never duplicates.
  * state.json records per-slug source sha256 + row counts. If the sources are
    unchanged and the output already holds the full mapped set, the mapper
    rewrites NOTHING except state.json last_run/last_verified timestamps
    (green re-run = no content change).
  * the mapper never invents rows: every trace comes from a real CDX row.

Order (ingest priority): the oai*-tagged DoE rows (the OpenAI-attributed core)
are emitted first, then the remaining DoE rows, then all other incident slugs
(alphabetical). Dedup is order-independent.

Stdlib only.
"""
import gzip
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qsl

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RAW_DIR = os.path.join(REPO, "data", "2026-10-01-arquivo-pt", "raw")
OUT_PATH = os.path.join(HERE, "data", "traces.jsonl")
STATE_PATH = os.path.join(HERE, "state.json")

DATASET = "openai-agent-traces"
SOURCE_SYSTEM = "arquivo-pt"
SOURCE_PULL = "2026-10-01 pull (collections/arquivo-pt)"

# filename prefix -> incident slug (matches Transluce incident numbering)
SLUGS = [
    ("doe-crdc", "doe-crdc"),
    ("kansas-kansasmemory", "kansas-kansasmemory"),
    ("maryland-edstats", "maryland-edstats"),
    ("bea-api", "bea-api"),
    ("lac-collectionsearch", "lac-collectionsearch"),
    ("navy-history", "navy-history"),
    ("nysed-enrollment", "nysed-enrollment"),
    ("illinois-iquery", "illinois-iquery"),
    ("calaccess", "calaccess"),
    ("omb-max", "omb-max"),
    ("doj-ojjdp", "doj-ojjdp"),
    ("sec", "sec"),
    ("cdc-wonder", "cdc-wonder"),
    ("texas-dshs", "texas-dshs"),
]

OAI_RE = re.compile(r"(?:^|[?&])zz=(oai\d+)", re.IGNORECASE)
SQLI_MARKERS = (" OR ", "or 1=1", "1=1", "--", "/*")
XSS_MARKERS = ("<script", "%3c", "onerror", "alert(")
FUZZ_MARKERS = ("debug=1", "?output=", "?raw=", "?url=", "output=", "raw=")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cdx_ts_to_iso(ts):
    # "20260616185927" -> "2026-06-16T18:59:27Z"
    try:
        dt = datetime.strptime(ts, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None


def trace_id_for(slug, timestamp, url):
    return hashlib.sha256(
        f"{SOURCE_SYSTEM}|{slug}|{timestamp}|{url}".encode("utf-8")
    ).hexdigest()


def extract_features(slug, url):
    """Extracted features from the captured URL. Only what the bytes hold."""
    feats = {"query_param_names": [], "oai_tag": None, "probe_flags": []}
    try:
        q = urlparse(url).query
    except Exception:
        return feats
    try:
        params = parse_qsl(q, keep_blank_values=True)
    except Exception:
        return feats
    names = []
    for name, value in params:
        if name not in names:
            names.append(name)
        if name.lower() == "zz" and value.lower().startswith("oai"):
            feats["oai_tag"] = value
    feats["query_param_names"] = names
    # DoE SQLi/fuzz ladder markers (per Transluce claim 3 / our addendum)
    if slug == "doe-crdc":
        low = q.lower()
        if "state_id" in low and (" or " in low or "%20or%20" in low or "+" in q):
            feats["probe_flags"].append("sqli_probe")
        if any(k.lower() in low for k in ("survey_year_key", "measure_id")):
            feats["probe_flags"].append("crdc_measure_params")
        if "fuzz" in low or re.search(r"state_id=\d+,\d+", q, re.I):
            feats["probe_flags"].append("fuzz_ladder")
    # LAC payload markers (13 documented payloads)
    if slug == "lac-collectionsearch":
        low = url.lower()
        if any(m in low for m in ("1 or 1=1", "%20or%20")):
            feats["probe_flags"].append("sqli_probe")
        if any(m in low for m in ("<", "%3c")):
            feats["probe_flags"].append("xss_probe")
        if "2147483648" in low:
            feats["probe_flags"].append("integer_overflow_probe")
        if any(m in low for m in ("?output=", "?raw=", "?url=", "debug=1")):
            feats["probe_flags"].append("fuzz_probe")
    return feats


def map_row(slug, row, source_file, line_no):
    """CDX row -> corpus record. Mirrors schema/record.schema.json required fields."""
    timestamp = row.get("timestamp", "")
    url = row.get("url", "")
    feats = extract_features(slug, url)
    oai_tag = feats.pop("oai_tag")
    provider = "openai" if oai_tag else None
    # eval-family attribution: the Jun-17 zz=oai DoE cluster is the confirmed
    # dsqa_250 incident traffic (Transluce claim 3 / deepsearchqa lane).
    eval_family = (
        "deepsearchqa/dsqa_250"
        if (slug == "doe-crdc" and provider == "openai")
        else None
    )
    tid = trace_id_for(slug, timestamp, url)
    body = {
        "_id": tid,  # loader uses the doc's own _id -> deterministic ES id
        "trace_id": tid,
        "@timestamp": cdx_ts_to_iso(timestamp),
        "record_kind": "arquivo_pt_capture",
        "event": {
            "dataset": DATASET,
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "fingerprint": None,  # filled below
        "labels": {
            "incident": slug,
            "source_system": SOURCE_SYSTEM,
            "source_pull": SOURCE_PULL,
            "source_file": f"data/2026-10-01-arquivo-pt/raw/{os.path.basename(source_file)}",
            "source_line": line_no,
            "cdx_timestamp": timestamp,
            "collection": row.get("collection"),
            "source_coll": row.get("source-coll"),
            "warc_filename": row.get("filename"),
            "warc_offset": row.get("offset"),
            "warc_length": row.get("length"),
        },
        "attribution": {
            "provider": provider,
            "eval_family": eval_family,
            "agent_instance": None,
            "note": (
                "provider=openai only where zz=oai<digits> tag present in the "
                "captured URL; eval_family deepsearchqa/dsqa_250 only for the "
                "Jun-17 DoE zz=oai cluster (confirmed dsqa_250 traffic); "
                "agent_instance never attributed (no row-level evidence). "
                "zz=oai values are candidate session labels, not attribution."
            ),
        },
        "source_url": url,
        "status": str(row.get("status", "")),
        "mime": row.get("mime"),
        "digest": row.get("digest"),
        "size_bytes": int(row["length"]) if str(row.get("length", "")).isdigit() else None,
        "file": f"data/2026-10-01-arquivo-pt/raw/{os.path.basename(source_file)}",
        "tags": ["oai-tagged"] if oai_tag else [],
        "features": feats,
        "notable_query_params": {
            k: v for k, v in (("zz", oai_tag),)
        } if oai_tag else {},
    }
    fp_src = json.dumps(
        {"trace_id": tid, "url": url, "timestamp": timestamp,
         "status": body["status"], "digest": body["digest"]},
        sort_keys=True, separators=(",", ":"),
    )
    body["fingerprint"] = hashlib.sha256(fp_src.encode()).hexdigest()
    return body, oai_tag is not None


def read_rows(path):
    """Yield (line_no, row) from a .cdx.jsonl.gz; empty files yield nothing."""
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            yield i, json.loads(line)


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    state = {}
    if os.path.exists(STATE_PATH):
        try:
            state = json.load(open(STATE_PATH))
        except Exception:
            state = {}
    slugs_state = state.setdefault("slugs", {})

    # --- phase 1: collect + dedup (order-independent) ---
    per_slug = {}  # slug -> {"seen": {key: (line_no, row)}, "dups": int, "oai": int, "src": path}
    for prefix, slug in SLUGS:
        path = os.path.join(RAW_DIR, f"{prefix}.cdx.jsonl.gz")
        entry = {"seen": {}, "dups": 0, "oai": 0, "src": path,
                 "sha256": sha256_file(path)}
        if os.path.getsize(path) == 0:
            per_slug[slug] = entry
            continue
        for line_no, row in read_rows(path):
            key = (str(row.get("timestamp", "")), str(row.get("url", "")))
            if key in entry["seen"]:
                entry["dups"] += 1
                continue
            if OAI_RE.search(str(row.get("url", ""))):
                entry["oai"] += 1
            entry["seen"][key] = (line_no, row)
        per_slug[slug] = entry

    # --- phase 2: idempotency check ---
    complete = True
    for slug, entry in per_slug.items():
        prev = slugs_state.get(slug, {})
        if (
            prev.get("status") not in ("complete", "complete_empty_source")
            or prev.get("source_sha256") != entry["sha256"]
            or prev.get("mapped_rows") != len(entry["seen"])
        ):
            complete = False
            break
    out_exists = os.path.exists(OUT_PATH)
    if complete and out_exists:
        state["last_run"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        state["last_verified"] = state["last_run"]
        state["note"] = ("idempotent re-run: sources unchanged, output complete; "
                         "no rows rewritten")
        json.dump(state, open(STATE_PATH, "w"), indent=2, sort_keys=True)
        print("IDEMPOTENT: sources unchanged, nothing rewritten.")
        print(f"traces: {sum(v['mapped_rows'] for v in slugs_state.values())}")
        return

    # --- phase 3: map + write (priority order: oai-tagged DoE first) ---
    def emit_order():
        # doe-crdc: oai-tagged rows first, then the rest
        doe = per_slug["doe-crdc"]
        items = sorted(doe["seen"].items(), key=lambda kv: kv[1][0])
        for key, (ln, row) in items:
            if OAI_RE.search(str(row.get("url", ""))):
                yield "doe-crdc", ln, row
        for key, (ln, row) in items:
            if not OAI_RE.search(str(row.get("url", ""))):
                yield "doe-crdc", ln, row
        for slug in sorted(per_slug):
            if slug == "doe-crdc":
                continue
            items = sorted(per_slug[slug]["seen"].items(), key=lambda kv: kv[1][0])
            for key, (ln, row) in items:
                yield slug, ln, row

    mapped_counts = {slug: 0 for slug in per_slug}
    with open(OUT_PATH, "w", encoding="utf-8") as out:
        for slug, line_no, row in emit_order():
            body, _ = map_row(slug, row, per_slug[slug]["src"], line_no)
            out.write(json.dumps(body, separators=(",", ":"), sort_keys=True) + "\n")
            mapped_counts[slug] += 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for slug, entry in per_slug.items():
        raw_rows = len(entry["seen"]) + entry["dups"]
        slugs_state[slug] = {
            "source_file": f"data/2026-10-01-arquivo-pt/raw/{os.path.basename(entry['src'])}",
            "source_sha256": entry["sha256"],
            "source_rows": raw_rows,
            "deduped_rows": len(entry["seen"]),
            "duplicates_dropped": entry["dups"],
            "mapped_rows": mapped_counts[slug],
            "oai_tagged_rows": entry["oai"],
            "status": "complete",
        }
        if raw_rows == 0:
            slugs_state[slug]["status"] = "complete_empty_source"
    state["corpus"] = DATASET
    state["source_system"] = SOURCE_SYSTEM
    state["total_mapped"] = sum(mapped_counts.values())
    state["last_run"] = now
    state["note"] = ("oai-tagged DoE rows emitted first; deterministic trace_ids; "
                     "no invented rows")
    json.dump(state, open(STATE_PATH, "w"), indent=2, sort_keys=True)
    print(f"MAPPED {sum(mapped_counts.values())} traces -> {OUT_PATH}")


if __name__ == "__main__":
    main()
