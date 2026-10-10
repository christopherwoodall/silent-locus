#!/usr/bin/env python3
"""Build the Factum submission bundle for lane 2026-09-12-jsonhero-docs-archive.

Reads the legacy lane's events.jsonl (grain: one record per doc, 6 rows) and
emits one source + one observation per doc, plus one source + one
dataset.snapshot observation preserving the recovery_census rollup.

Mapping rules (all strings copied verbatim from source; nothing redacted):
- recovered doc (swJMw8b6VwDC): web.capture observation of the Wayback
  id_-suffixed capture URL (HTTP 200, capture_kind http). observed_at is the
  Wayback capture time; time_basis source_metadata.
- 5 not_archived docs: reachability.check observations against the Wayback
  CDX API, outcome response, error carrying the zero-capture verdict.
  observed_at is the lane date 2026-09-28 (legacy_documented), per the lane's
  documented timestamp convention; verdicts are medium confidence because
  archive.today was unreachable from the collection network (Wayback-only).
- census: dataset.snapshot with row_count 6, coverage complete.
- corpus_url_occurrences values are UPSTREAM counts from the corpus scan,
  recorded verbatim in tags, not as observed evidence.
- Capture bytes are preserved at data/lanes/<lane>/raw/ (Git-retained lane
  documents); observations carry the repo-relative byte path in tags.
"""
import json
import sys

LANE = "2026-09-12-jsonhero-docs-archive"
EVID = "evidence/2026-09-12-jsonhero-docs-archive"
DATA_DIR = f"data/lanes/{LANE}"

CAPTURE_SCHEMA = "urn:factum:web:web-capture:1"
REACH_SCHEMA = "urn:factum:web:reachability-check:1"
SNAP_SCHEMA = "urn:factum:datasets:snapshot:1"


def main():
    rows = []
    with open(f"{EVID}/events.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    assert len(rows) == 6, f"expected 6 rows, got {len(rows)}"
    ids = [r["labels"]["doc.id"] for r in rows]
    assert len(set(ids)) == 6, "duplicate doc ids in batch"

    records = []

    for r in rows:
        lab = r["labels"]
        doc_id = lab["doc.id"]
        status = lab["doc.recovery_status"]
        occ = lab["doc.corpus_url_occurrences"]
        doc_url = r["source_url"]

        src_ref = f"src-{doc_id}"
        obs_ref = f"obs-{doc_id}"

        if status == "recovered":
            cap_url = lab["doc.capture.url"]
            assert r["sha256"] == lab["doc.sha256"]
            assert r["size_bytes"] == lab["doc.byte_size"] == 95501
            records.append(
                {
                    "kind": "source",
                    "ref": src_ref,
                    "body": {
                        "locator": cap_url,
                        "source_type": "web",
                        "title": (
                            "Wayback capture (id_ raw bytes) of "
                            f"https://jsonhero.io/j/{doc_id} @ 2026-09-12T07:50:05Z"
                        ),
                    },
                    "tags": {"lane": LANE, "retrieved": "2026-09-28T03:05:00Z"},
                }
            )
            data = {
                "requested_url": doc_url,
                "final_url": cap_url,
                "http_status": 200,
                "capture_kind": "http",
                "tool": "Wayback id_ suffix fetch (raw bytes, no Wayback rewriting)",
            }
            records.append(
                {
                    "kind": "observation",
                    "ref": obs_ref,
                    "body": {
                        "type": "web.capture",
                        "data_schema": CAPTURE_SCHEMA,
                        "data": data,
                        "observed_at": "2026-09-12T07:50:05Z",
                        "time_basis": "source_metadata",
                        "source": f"@{src_ref}",
                        "files": [],
                    },
                    "tags": {
                        "lane": LANE,
                        "doc.id": doc_id,
                        "doc.sha256": lab["doc.sha256"],
                        "doc.byte_size": lab["doc.byte_size"],
                        "doc.corpus_url_occurrences": occ,
                        "doc.capture_bytes_path": (
                            f"{DATA_DIR}/raw/swJMw8b6VwDC_20260912075005.html"
                        ),
                        "doc.note": lab["doc.note"],
                    },
                }
            )
        else:
            assert status == "not_archived", f"unexpected status {status}"
            records.append(
                {
                    "kind": "source",
                    "ref": src_ref,
                    "body": {
                        "locator": "https://web.archive.org/cdx/search/cdx",
                        "source_type": "web",
                        "title": f"Wayback CDX API (zero-capture verdict for {doc_id}, 2026-09-28)",
                    },
                    "tags": {"lane": LANE, "retrieved": "2026-09-28"},
                }
            )
            data = {
                "target": "https://web.archive.org/cdx/search/cdx",
                "method": "GET",
                "outcome": "response",
                "error": (
                    f"CDX returned zero captures for jsonhero.io/j/{doc_id}* "
                    "(exact + wildcard). Wayback-only verdict: archive.today "
                    "unreachable from this network."
                ),
            }
            records.append(
                {
                    "kind": "observation",
                    "ref": obs_ref,
                    "body": {
                        "type": "reachability.check",
                        "data_schema": REACH_SCHEMA,
                        "data": data,
                        "observed_at": "2026-09-28T00:00:00Z",
                        "time_basis": "legacy_documented",
                        "source": f"@{src_ref}",
                        "files": [],
                    },
                    "tags": {
                        "lane": LANE,
                        "doc.id": doc_id,
                        "doc.url": doc_url,
                        "doc.corpus_url_occurrences": occ,
                        "confidence": r["confidence"],
                        "doc.note": lab["doc.note"],
                    },
                }
            )

    # recovery census rollup
    with open(f"{EVID}/rollup.jsonl") as f:
        census = json.loads(f.readline())
    clab = census["labels"]
    assert clab["census.total"] == 6
    assert set(clab["census.not_archived_doc_ids"]) == set(ids) - {
        clab["census.recovered_doc_ids"][0]
    }
    records.append(
        {
            "kind": "source",
            "ref": "src-census",
            "body": {
                "locator": "https://web.archive.org/cdx/search/cdx",
                "source_type": "web",
                "title": "Wayback CDX API (archive-recovery census, 2026-09-28)",
            },
            "tags": {"lane": LANE, "retrieved": "2026-09-28"},
        }
    )
    records.append(
        {
            "kind": "observation",
            "ref": "obs-census",
            "body": {
                "type": "dataset.snapshot",
                "data_schema": SNAP_SCHEMA,
                "data": {
                    "dataset_uri": LANE,
                    "coverage": "complete",
                    "row_count": clab["census.total"],
                    "revision": "2026-09-29T04:18:29Z events build",
                },
                "observed_at": "2026-09-28T00:00:00Z",
                "time_basis": "legacy_documented",
                "source": "@src-census",
                "files": [],
            },
            "tags": {
                "lane": LANE,
                "census.recovered": clab["census.recovered"],
                "census.not_archived": clab["census.not_archived"],
                "census.recovered_doc_ids": clab["census.recovered_doc_ids"],
                "census.verdict_scope": clab["census.verdict_scope"],
                "confidence": census["confidence"],
            },
        }
    )

    bundle = {
        "bundle": 2,
        "actor": "agent:lane-ingest/2026-09-12-jsonhero-docs-archive",
        "idempotency_key": "batch5-2026-09-12-jsonhero-docs-archive-v1",
        "records": records,
        "tags": {},
    }
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/jsonhero-archive-bundle.json"
    with open(out, "w") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(records)} records to {out}")


if __name__ == "__main__":
    main()
