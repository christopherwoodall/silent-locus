#!/usr/bin/env python3
"""Independent validator for the JetBrains SWE bundle.

Re-derives expectations from source evidence (parquet + verified-findings.jsonl),
never from the builder's in-memory structures.
"""
import json, re, sys, collections

LANE = "jetbrains-swe-trajectories"
BUNDLE = "data/lanes/jetbrains-swe-trajectories/working/jetbrains-swe-bundle.json"
PARQUET = "data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet"
FINDINGS = "data/lanes/jetbrains-swe-trajectories/verified-findings.jsonl"

errors, warnings = [], []


def err(m): errors.append(m)
def warn(m): warnings.append(m)

bundle = json.load(open(BUNDLE))
recs = bundle["records"]
kinds = collections.Counter(r["kind"] for r in recs)
print("counts:", dict(kinds), "total:", len(recs))

# 1. every record has tags.lane
for r in recs:
    if r.get("tags", {}).get("lane") != LANE:
        err("missing/wrong tags.lane on %s" % r.get("ref"))

# 2. observations need observed_at + time_basis
for r in recs:
    if r["kind"] == "observation":
        b = r["body"]
        for k in ("observed_at", "time_basis", "type", "source", "data"):
            if k not in b or not b[k]:
                err("observation %s missing %s" % (r["ref"], k))

# 3. ref uniqueness + @ref resolution
refs = {r["ref"] for r in recs}
if len(refs) != len(recs): err("duplicate refs")
ref_re = re.compile(r"^@([A-Za-z0-9][A-Za-z0-9._-]{0,63})$")
def check_refs(node, where):
    if isinstance(node, dict):
        for v in node.values(): check_refs(v, where)
    elif isinstance(node, list):
        for v in node: check_refs(v, where)
    elif isinstance(node, str) and node.startswith("@"):
        if node[1:] not in refs:
            err("@ref %s unresolved in %s" % (node, where))
for r in recs:
    check_refs(r["body"], r["ref"])

# 4. the `resolved` column must not be used as observation data.
# A JSON key literally named "resolved" in body.data or tags is an error;
# provenance notes documenting its exclusion, or the word inside verbatim
# tool-command bytes (e.g. Django's ResolvedOuterRef), are not.
def uses_resolved_key(node, in_data_tags=False):
    if isinstance(node, dict):
        for k, v in node.items():
            if in_data_tags and k == "resolved":
                return True
            if uses_resolved_key(v, in_data_tags or k in ("data", "tags")):
                return True
    elif isinstance(node, list):
        for v in node:
            if uses_resolved_key(v, in_data_tags):
                return True
    return False
for r in recs:
    if uses_resolved_key(r):
        err("record %s uses resolved column" % r["ref"])

# 5. dataset.record tags vs parquet re-derivation
import pyarrow.parquet as pq
rows = pq.read_table(PARQUET).to_pylist()
assert len(rows) == 1785
drs = [r for r in recs if r["body"].get("type") == "dataset.record"]
if len(drs) != 1785: err("dataset.record count %d" % len(drs))
seen_iids = set()
for r in drs:
    t = r["tags"]; d = r["body"]["data"]
    i = int(t["row_index"]); prow = rows[i]
    if t["instance_id"] != prow["instance_id"]: err("iid mismatch %s" % r["ref"])
    if t["instance_id"] in seen_iids: err("dup iid " + t["instance_id"])
    seen_iids.add(t["instance_id"])
    if d["external_record_id"] != prow["instance_id"]: err("ext id mismatch " + r["ref"])
    if t["n_turns"] != str(prow["n_turns"]): err("n_turns " + r["ref"])
    if t["n_messages"] != str(prow["n_messages"]): err("n_messages " + r["ref"])
    if t["exit_status"] != prow["exit_status"]: err("exit " + r["ref"])
    ms = "+".join(sorted({m for m in prow["selected_models"] if m}))
    if t["model"] != ms: err("model " + r["ref"])
    if d["locator"]["row"]["index"] != i: err("locator row " + r["ref"])
print("dataset.record re-derivation OK; exit counts:",
      collections.Counter(rows[i]["exit_status"] for i in range(1785)))

# 6. behavior quotes verbatim vs findings file; tool_sequence vs parquet bytes
findings = {}
for line in open(FINDINGS):
    line = line.strip()
    if line:
        d = json.loads(line); findings[d["id"]] = d
beh = {r["tags"]["finding_id"]: r for r in recs
       if r["body"].get("type") == "intel.behavior"}
ts = {r["tags"]["finding_id"]: r for r in recs
      if r["body"].get("type") == "behavior.tool_sequence"}
if set(beh) != set(findings) or set(ts) != set(findings):
    err("finding coverage mismatch")
for fid, f in findings.items():
    b = beh[fid]
    if b["tags"]["verbatim_quote"] != f["verbatim_quote"]:
        err(fid + " quote mismatch")
    if b["tags"]["verifier_notes"] != f["verifier_notes"]:
        err(fid + " verifier_notes mismatch")
    # tool steps: command (sans truncation suffix) must be a verbatim prefix of
    # the bash block (or of message content for prose steps) in the cited bytes
    rowno = f["provenance"]["trajectory_row"]
    row = rows[rowno] if isinstance(rowno, int) else None
    steps = ts[fid]["body"]["data"]["steps"]
    if ts[fid]["body"]["data"]["length"] != len(steps): err(fid + " length mismatch")
    step_ranges = {"F-A-001": [10, 12, 14, 16], "F-A-002": [42, 44, 46],
                   "F-A-003": [26, 28],
                   "F-001": [20, 22, 24, 26, 28, 30, 32, 34],
                   "F-002": [20, 26],
                   "F-003": [22, 24, 26, 28, 30, 32, 34, 36, 38]}
    if fid in step_ranges and row is not None:
        exp = step_ranges[fid]
        if len(steps) != len(exp): err(fid + " step count %d != %d" % (len(steps), len(exp)))
        for st, mi in zip(steps, exp):
            content = row["messages"][mi]["content"] or ""
            cmd = st["command"]
            cmd = re.sub(r" \[truncated at \d+ chars\]$", "", cmd)
            m = re.search(r"```bash\n(.*?)```", content, re.DOTALL)
            if m:
                block = m.group(1).strip()
                if not block.startswith(cmd) and cmd not in block:
                    err(fid + " step msg%d command not verbatim in bytes" % mi)
            else:
                flat = content.replace("\n", " ")[:2000]
                if not flat.startswith(cmd):
                    err(fid + " step msg%d prose not verbatim prefix" % mi)
    if fid == "F-005":
        row1471 = rows[1471]
        if len(steps) < 1: err("F-005 exemplar has no steps")
        # first exemplar command must appear in row 1471 assistant bytes
        hay = " ".join(m["content"] or "" for m in row1471["messages"])
        cmd0 = re.sub(r" \[truncated at \d+ chars\]$", "", steps[0]["command"])
        if cmd0[:100] not in hay: err("F-005 exemplar cmd not in row 1471 bytes")
print("behavior coverage + quote verbatim OK:", len(beh), "findings")

# 7. edge counts + endpoints
edges = [r for r in recs if r["kind"] == "edge"]
pred = collections.Counter(r["body"]["predicate"] for r in edges)
print("edges:", dict(pred))
if pred["related_to"] != 1785: err("related_to count")
if pred["supports"] != 7: err("supports count")

# 8. top-level envelope
for k in ("bundle", "actor", "idempotency_key"):
    if k not in bundle: err("missing top-level " + k)
if bundle["actor"] != "agent:jetbrains-swe-ingestor": err("actor")
if bundle["idempotency_key"] != "jetbrains-swe-ingest-2026-10-17-v1": err("idem key")

print("ERRORS:", len(errors))
for e in errors[:20]: print("  E:", e)
print("WARNINGS:", len(warnings))
for w in warnings[:10]: print("  W:", w)
sys.exit(1 if errors else 0)
