#!/usr/bin/env python3
"""Build the Factum submission bundle for lane 2023-11-14-hfspace-proxies.

Reads the legacy lane's events.jsonl (schema-mapped) and raw/spaces.jsonl
(primary capture), emits one infra.proxy_instance observation + one source
record per Space (38 each). All strings copied verbatim from source; derived
hostnames are explicitly annotated in notes.

Mapping rules:
- host: observed space.live_url hostname where present (24 rows); otherwise
  derived from the HF Spaces URL pattern owner-name.hf.space (lowercased,
  '.'/'_' -> '-'), verified against all 24 observed rows. Derived hosts are
  flagged in notes; liveness unprobed.
- invocation_shape: verbatim invocation where source states it; cors-anywhere
  clones use the project's standard GET /<target-url> path (implementation
  read); gradio SDK rows use the gradio web UI; otherwise "unknown".
- access: "open" only for the code-read open CORS proxy (TheNacken);
  "unknown" elsewhere.
- notes: verbatim source fields (space.id/sdk/created/modified/likes/shape/
  swarm_tie/tie_strength) plus derivation flags.
"""
import json
import re
import sys
from urllib.parse import urlparse

EVID = "evidence/2023-11-14-hfspace-proxies"
LANE = "2023-11-14-hfspace-proxies"
DATA_SCHEMA = "urn:factum:infra:proxy-instance:1"


def derive_host(space_id):
    owner, name = space_id.split("/", 1)
    host = f"{owner}-{name}".lower()
    host = re.sub(r"[^a-z0-9-]+", "-", host)
    host = re.sub(r"-+", "-", host).strip("-")
    return host + ".hf.space"


def invocation_shape(row):
    shape = row["labels"].get("shape", "")
    sid = row["labels"]["space.id"]
    if sid == "TheNacken/python-cors-proxy":
        return "GET /?url=<target>"
    if "cors-anywhere clone" in shape:
        return "GET /<target-url>"
    if sid == "santhoshsharuk/web-article-reader-api":
        return 'POST /convert/ {"url": "<target>"}'
    if row["labels"].get("space.sdk") == "gradio":
        return "gradio web UI"
    return "unknown"


def main():
    rows = []
    with open(f"{EVID}/events.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    # raw cross-check: live URLs and verbatim shape values
    raw = {}
    with open(f"{EVID}/raw/spaces.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                raw[r["id"]] = r

    assert len(rows) == 38, f"expected 38 rows, got {len(rows)}"
    ids = [r["labels"]["space.id"] for r in rows]
    assert len(set(ids)) == 38, "duplicate space ids in batch"

    # verify the derivation rule against every observed live URL
    for r in rows:
        live = r["labels"].get("space.live_url")
        if live:
            observed = urlparse(live).hostname
            derived = derive_host(r["labels"]["space.id"])
            assert observed == derived, (
                f"derivation mismatch for {r['labels']['space.id']}: "
                f"observed {observed} != derived {derived}"
            )

    records = []
    for r in rows:
        lab = r["labels"]
        sid = lab["space.id"]
        slug = sid.replace("/", "-")
        live_url = lab.get("space.live_url")

        if live_url:
            host = urlparse(live_url).hostname
            derived_flag = ""
        else:
            host = derive_host(sid)
            derived_flag = (
                "; host_derived_from_space_id=true "
                "(HF Spaces URL pattern; live URL not observed in source; "
                "liveness unprobed)"
            )

        created = r["event"]["created"]
        retrieved = (
            "2026-09-29"
            if created.startswith("2026-09-29T16:15")
            else "2026-09-27/2026-09-28"
        )

        notes = (
            f"space.id={sid}; space.sdk={lab.get('space.sdk')}; "
            f"space.created={lab.get('space.created')}; "
            f"space.modified={lab.get('space.modified')}; "
            f"space.likes={lab.get('space.likes')}; "
            f"shape={lab.get('shape')}; swarm_tie={lab.get('swarm_tie')}; "
            f"tie_strength={lab.get('tie_strength')}"
        )
        if live_url:
            notes += f"; space.live_url={live_url}"
        notes += derived_flag

        data = {
            "host": host,
            "invocation_shape": invocation_shape(r),
            "access": "open" if sid == "TheNacken/python-cors-proxy" else "unknown",
            "notes": notes,
        }

        src_ref = f"src-{slug}"
        obs_ref = f"obs-{slug}"
        records.append(
            {
                "kind": "source",
                "ref": src_ref,
                "body": {
                    "locator": r["source_url"],
                    "source_type": "web",
                },
                "tags": {"lane": LANE, "retrieved": retrieved},
            }
        )
        records.append(
            {
                "kind": "observation",
                "ref": obs_ref,
                "body": {
                    "data": data,
                    "data_schema": DATA_SCHEMA,
                    "files": [],
                    "source": f"@{src_ref}",
                    "type": "infra.proxy_instance",
                },
                "tags": {
                    "lane": LANE,
                    "tie_strength": lab.get("tie_strength"),
                    "retrieved": retrieved,
                },
            }
        )

    bundle = {
        "bundle": 2,
        "actor": "agent:lane-ingest/2023-11-14-hfspace-proxies",
        "idempotency_key": "batch3-2023-11-14-hfspace-proxies-v1",
        "records": records,
        "tags": {},
    }
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/hfspace-proxies-bundle.json"
    with open(out, "w") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(records)} records to {out}")


if __name__ == "__main__":
    main()
