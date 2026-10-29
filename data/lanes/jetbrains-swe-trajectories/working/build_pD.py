#!/usr/bin/env python3
"""Build bundle-pD.json: edges for the JetBrains SWE ingest.

Reads assigned record IDs from the local Factum DB (read-only) by lane tags:
  run id, snapshot id, 1,785 dataset.record ids (by row_index), 7 intel.behavior ids.
Writes working/bundle-pD.json with idempotency key <KEY>-pD.
"""
import json, sqlite3, sys

LANE = "jetbrains-swe-trajectories"
WORK_DIR = "data/lanes/jetbrains-swe-trajectories/working"
ACTOR = "agent:jetbrains-swe-ingestor"
KEY = "jetbrains-swe-ingest-2026-10-17-v1"
FINDINGS_PATH = "data/lanes/jetbrains-swe-trajectories/verified-findings.jsonl"

db = sqlite3.connect("file:data/.local/factum.db?mode=ro", uri=True)
cur = db.cursor()

def one(sql, args):
    r = cur.execute(sql, args).fetchone()
    if not r:
        sys.exit("missing: " + sql + " " + str(args))
    return r[0]

LANE_TAG = "(select record_id from record_tags where key='lane' and value='%s')" % LANE

run_id = one("select id from records where kind='run' and id in " + LANE_TAG + " limit 1", ())
snap_id = one("select id from records where document like '%urn:factum:datasets:snapshot:1%' and id in " + LANE_TAG + " limit 1", ())

rec_ids = {}
for row in cur.execute("select id, document from records where kind='observation' and document like '%urn:factum:datasets:record:1%' and id in " + LANE_TAG):
    d = json.loads(row[1])
    rec_ids[d["tags"]["row_index"]] = row[0]
print("dataset.record ids:", len(rec_ids))
assert len(rec_ids) == 1785, len(rec_ids)

beh_ids = {}
for row in cur.execute("select id, document from records where kind='observation' and document like '%urn:factum:intel:behavior:1%' and id in " + LANE_TAG):
    d = json.loads(row[1])
    beh_ids[d["tags"]["finding_id"]] = row[0]
print("intel.behavior ids:", beh_ids.keys())
assert len(beh_ids) == 7, len(beh_ids)

records = []
for i in range(1785):
    ref = "rec-%04d" % i
    obj = rec_ids[str(i)]
    records.append({"ref": "e-run-%04d" % i, "kind": "edge",
                    "body": {"subject": run_id, "predicate": "related_to",
                             "object": obj, "basis": "OBSERVED",
                             "cites": [run_id, obj],
                             "note": "ingest run produced this trajectory record"},
                    "tags": {"lane": LANE}})

findings = {}
for line in open(FINDINGS_PATH):
    line = line.strip()
    if line:
        d = json.loads(line); findings[d["id"]] = d
for fid, f in findings.items():
    rowno = f["provenance"]["trajectory_row"]
    obj = snap_id if fid == "F-005" else rec_ids[str(rowno)]
    subj = beh_ids[fid]
    records.append({"ref": "e-sup-" + fid, "kind": "edge",
                    "body": {"subject": subj, "predicate": "supports",
                             "object": obj, "basis": "OBSERVED",
                             "cites": [subj, obj],
                             "note": ("behavior finding verified against trajectory bytes"
                                      if fid != "F-005"
                                      else "corpus-wide methodological caveat")},
                    "tags": {"lane": LANE}})

refs = [r["ref"] for r in records]
assert len(refs) == len(set(refs))
bundle = {"bundle": 2, "actor": ACTOR, "idempotency_key": KEY + "-pD",
          "records": records}
out = WORK_DIR + "/bundle-pD.json"
json.dump(bundle, open(out, "w"), ensure_ascii=False)
print("wrote", out, len(records), "edges")
