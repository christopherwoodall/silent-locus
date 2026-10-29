#!/usr/bin/env python3
"""Follow-up fixes 2026-09-28 (after backfill_schema_2026_09_28.py).

1. iowacollab-pastes: set @timestamp from source-verified paste creation
   times. Sources:
   - 34cb12da / d379207f / 538faa12: data/2026-09-04-thecolony-ai/raw/wiki_incident_page.html
     sect.12 ("<id> -- created <ISO>" per paste; verified verbatim).
   - df40f1f1: paste body literal ts=1781641251 -> 2026-06-16T20:20:51Z
     (tool-verified; body on disk at data/2026-05-17-iowacollab-pastes/raw/df40f1f1.txt).
   Wayback snapshot times are capture times, not creation times, and are
   kept in labels only. live_checked_at stays as the annotated prose string.

2. pastebin-cluster-sweep: recompute fingerprint as sha256 (current
   convention) over venue + "|" + source_url, replacing the legacy md5-era
   value. Deterministic; old value not preserved (no external references).

Idempotent: re-running is a no-op once applied.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone

REPO = __file__.rsplit("/scripts/", 1)[0]

IOWA_TS = {
    "34cb12da": "2026-05-17T12:47:48Z",  # wiki sect.12
    "d379207f": "2026-05-26T15:39:32Z",  # wiki sect.12
    "538faa12": "2026-06-16T20:08:40Z",  # wiki sect.12
    "df40f1f1": "2026-06-16T20:20:51Z",  # body ts=1781641251, tool-verified
}


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def rewrite(path: str, fn) -> int:
    p = f"{REPO}/{path}"
    out = []
    for line in open(p):
        if not line.strip():
            continue
        out.append(json.dumps(fn(json.loads(line)), ensure_ascii=False))
    open(p, "w").write("\n".join(out) + "\n")
    return len(out)


def fix_iowa(rec: dict) -> dict:
    pid = rec["labels"]["id"]
    assert pid in IOWA_TS, f"unknown iowa paste id {pid}"
    rec["@timestamp"] = IOWA_TS[pid]
    # validate parseable
    datetime.fromisoformat(rec["@timestamp"].replace("Z", "+00:00"))
    return rec


def fix_pastebin_fp(rec: dict) -> dict:
    ident = rec["labels"]["venue"] + "|" + (rec.get("source_url") or "")
    rec["fingerprint"] = fp(ident)
    assert len(rec["fingerprint"]) == 64
    return rec


def main():
    check_only = "--check" in sys.argv
    if check_only:
        # validate only
        for line in open(f"{REPO}/data/2026-05-17-iowacollab-pastes/events.jsonl"):
            if line.strip():
                r = json.loads(line)
                assert r["labels"]["id"] in IOWA_TS
        for line in open(f"{REPO}/data/2026-09-28-pastebin-cluster-sweep/events.jsonl"):
            if line.strip():
                r = json.loads(line)
                assert r["labels"]["venue"]  # source_url optional (finding)
        print("check ok")
        return
    n1 = rewrite("data/2026-05-17-iowacollab-pastes/events.jsonl", fix_iowa)
    n2 = rewrite("data/2026-09-28-pastebin-cluster-sweep/events.jsonl", fix_pastebin_fp)
    print(f"iowacollab-pastes: {n1} records timestamped; "
          f"pastebin-cluster-sweep: {n2} fingerprints recomputed (sha256)")


if __name__ == "__main__":
    main()
