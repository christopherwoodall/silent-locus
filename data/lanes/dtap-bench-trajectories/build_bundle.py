#!/usr/bin/env python3
"""DTap-Bench trajectory factum ingest bundle builder.

Reads:
  raw/**/{*.json,judge_result.json} + per-file .PROVENANCE.txt / .sha256 (byte store, local-only)
  raw/LICENSE.note, raw/SCRAPE-PROGRESS.json
  working/verified-findings.jsonl (23 verified PRIMARY findings, byte-checked)

Writes: bundle-dtap-bench.json (factum bundle v2) + build-report.json

Bundle design:
  1 source record    — HF dataset AI-Secure/DTap-Bench-Agent-Trajectories @ rev
  1 run record       — the scrape (partial: download still in flight)
  1 dataset.snapshot — scrape output at revision
  22 artifact records — one per distinct finding-trajectory file (sha256 + size)
  22 dataset.record observations — one lean record per finding trajectory
      (NO conversation content: raw JSON is the byte store)
  23 intel.behavior observations — one per verified finding
  23 behavior.tool_sequence observations — decisive step window per finding,
      steps recorded faithfully as {index, role, action}. A012's python chunks
      (explosives documentation) are withheld from the bundle by design; the
      raw trajectory remains the byte store.
  Edges: run --related_to--> dataset.record (22),
      intel.behavior --supports--> dataset.record (23),
      behavior.tool_sequence --supports--> intel.behavior (23).
"""
import json, os, sys, hashlib, datetime, re, glob

LANE = "dtap-bench-trajectories"
ACTOR = "agent:dtap-bench-ingestor"
IDEMPOTENCY = "dtap-bench-ingest-2026-10-17-v1"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
WORKING = os.path.join(HERE, "working")
FINDINGS_PATH = os.path.join(WORKING, "verified-findings.jsonl")
OUT_BUNDLE = os.path.join(HERE, "bundle-dtap-bench.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "AI-Secure/DTap-Bench-Agent-Trajectories"
REVISION = "836caf2fdd78b888ddd14fb62dc038e932e17898"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
RAW_REL = "data/lanes/dtap-bench-trajectories/raw"


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_provenance(path):
    prov = {}
    pp = path + ".PROVENANCE.txt"
    if not os.path.isfile(pp):
        return prov
    for line in open(pp):
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            prov[k.strip()] = v.strip()
    return prov


def parse_range(spec):
    ids = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            ids.extend(range(int(lo), int(hi) + 1))
        else:
            ids.append(int(part))
    return ids


def step_summary(step):
    """Faithful compact rendering of one trajectory step."""
    role = step.get("role", "?")
    sid = step.get("step_id", "?")
    if role == "agent":
        action = step.get("action", "")
        md = step.get("metadata", {}) or {}
        if action == "send_message_to_user":
            msg = md.get("message", "")
            return {"index": sid, "role": role, "action": "send_message_to_user",
                    "message": msg[:2000]}
        return {"index": sid, "role": role, "action": action[:1000],
                "tool": md.get("tool_name", ""), "params": md.get("tool_params", {})}
    state = step.get("state", "")
    return {"index": sid, "role": role,
            "state": state[:1000] if isinstance(state, str) else str(state)[:1000]}


def main():
    findings = [json.loads(l) for l in open(FINDINGS_PATH) if l.strip()]
    meta = findings[-1]
    assert meta["id"] == "_meta", "last line must be _meta"
    findings = findings[:-1]
    assert meta["verified_count"] == len(findings) == 23, \
        "expected 23 findings, got %d" % len(findings)
    f_mtime = os.path.getmtime(FINDINGS_PATH)
    obs_at = datetime.datetime.fromtimestamp(f_mtime, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    prog = json.load(open(os.path.join(RAW, "SCRAPE-PROGRESS.json")))

    # ---- distinct trajectory files (A020 -> its 2 byte-verified judge files) ----
    traj_files = []  # (finding_ids, raw_rel_path)
    seen = {}
    for f in findings:
        t = f["trajectory"]
        if t.startswith("META:"):
            rels = [
                "claudesdk/claude-opus-4-6/macos/malicious/direct/data-theft/1/judge_result.json",
                "claudesdk/claude-opus-4-6/legal/malicious/indirect/biased_sentencing/14/judge_result.json",
            ]
        else:
            rels = [t[len(RAW_REL + "/"):]]
        for r in rels:
            seen.setdefault(r, []).append(f["id"])
    for r, fids in sorted(seen.items()):
        p = os.path.join(RAW, r)
        if not os.path.isfile(p):
            fail("trajectory file missing: " + r)
        traj_files.append((fids, r, p))

    # ---- dedup: direct scan of data/records for a prior dtap-bench batch ----
    rec_dir = os.path.join(HERE, "..", "..", "records")
    prior = []
    if os.path.isdir(rec_dir):
        for b in os.listdir(rec_dir):
            mp = os.path.join(rec_dir, b, "manifest.json")
            if os.path.isfile(mp):
                try:
                    m = json.load(open(mp))
                    lane = (m.get("lane") or m.get("tags", {}).get("lane") or "")
                    if "dtap" in str(m).lower() or lane == LANE:
                        prior.append(b)
                except Exception:
                    pass
    if prior:
        fail("prior dtap-bench batch already exported: %r" % prior)
    print("dedup: no prior dtap-bench batch in data/records/")

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        if len(ref) > 64:
            fail("ref exceeds 64 chars: " + ref)
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- source / run / snapshot ----
    rec("source-dtap-bench", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "AI-Secure/DTap-Bench-Agent-Trajectories: agent trajectories + judge verdicts across 10 harness/model pairs, 14 envs, benign/malicious splits",
        "platform": "huggingface",
    }, {"dataset": HF_DATASET, "revision": REVISION, "license": "apache-2.0",
        "hf_url": HF_URL})

    rec("run-dtap-bench", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get per-file via direct resolve-cache URLs",
        "started": "2026-10-17T05:30:00Z",
        "ended": prog.get("updated_utc", ""),
        "params": {
            "inputs": [HF_URL + "/resolve/" + REVISION],
            "dataset_revision": REVISION,
            "method": "per-file curl -L with sha256 sidecars + PROVENANCE.txt (huggingface_hub broken on this VM); 12-way parallel, idempotent resume",
        },
        "coverage": {
            "complete": False,
            "scanned": prog.get("files_done", 0),
            "total": prog.get("files_total", 133728),
            "description": "Download in flight at bundle build time; review sample drawn from downloaded files.",
        },
    }, {"dataset": HF_DATASET, "revision": REVISION})

    rec("snap-dtap-bench", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-dtap-bench",
        "run": "@run-dtap-bench",
        "observed_at": prog.get("updated_utc", ""),
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": REVISION,
            "coverage": "partial",
            "file_count": prog.get("files_done", 0),
            "file_total": prog.get("files_total", 133728),
        },
    }, {"dataset": HF_DATASET, "revision": REVISION})

    # ---- artifacts + dataset.records ----
    art_ref, traj_ref = {}, {}
    for i, (fids, r, p) in enumerate(traj_files):
        prov = read_provenance(p)
        digest = sha256_file(p)
        sidecar = p + ".sha256"
        if os.path.isfile(sidecar):
            sc = open(sidecar).read().split()[0]
            if sc != digest:
                fail("sha256 sidecar mismatch: " + r)
        aref = "art-dtap-%02d" % (i + 1)
        art_ref[r] = aref
        rec(aref, "artifact", {"sha256": digest, "size": os.path.getsize(p)}, {
            "filename": os.path.basename(r), "raw_path": RAW_REL + "/" + r,
            "retrieved_utc": prov.get("retrieved_utc", "")})

        # parse harness/model/env/split from path
        parts = r.split("/")
        harness, model, env = parts[0], parts[1], parts[2]
        split = "judge" if r.endswith("judge_result.json") else parts[3]
        tref = "traj-dtap-%02d" % (i + 1)
        traj_ref[r] = tref
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-dtap-bench",
            "run": "@run-dtap-bench",
            "observed_at": prov.get("retrieved_utc", ""),
            "time_basis": "collector_clock",
            "files": [{"artifact": "@" + aref, "role": "raw-trajectory",
                       "filename": os.path.basename(r)}],
            "data": {
                "snapshot": "@snap-dtap-bench",
                "locator": {"artifact": "@" + aref, "whole": True},
                "external_record_id": r,
            },
        }, {
            "harness": harness, "model": model, "env": env, "split": split,
            "raw_path": RAW_REL + "/" + r, "file_sha256": digest,
            "finding_ids": ",".join(fids),
        })
        rec("edge-run-dtap-%02d" % (i + 1), "edge", {
            "subject": "@run-dtap-bench", "predicate": "related_to",
            "object": "@" + tref, "basis": "OBSERVED", "cites": ["@" + tref],
            "note": "scrape run produced the trajectory record",
        }, {"raw_path": r})

    # ---- findings ----
    for i, f in enumerate(findings):
        fid = f["id"]
        n = i + 1
        # resolve trajectory file(s)
        if f["trajectory"].startswith("META:"):
            rels = [
                "claudesdk/claude-opus-4-6/macos/malicious/direct/data-theft/1/judge_result.json",
                "claudesdk/claude-opus-4-6/legal/malicious/indirect/biased_sentencing/14/judge_result.json",
            ]
        else:
            rels = [f["trajectory"][len(RAW_REL + "/"):]]

        # tool sequence from decisive steps
        steps = []
        if f["step_range"] == "n/a":
            for r in rels:
                j = json.load(open(os.path.join(RAW, r)))
                steps.append({"index": 0, "role": "judge",
                              "action": "attack_message",
                              "message": str(j.get("attack_message", ""))[:1500],
                              "attack_success": j.get("attack_success")})
        else:
            ids = parse_range(f["step_range"])
            r = rels[0]
            t = json.load(open(os.path.join(RAW, r)))
            by_id = {s.get("step_id"): s for s in t["trajectory"]}
            for sid in ids:
                s = by_id.get(sid)
                if s is None:
                    fail("finding %s step_id %d not in %s" % (fid, sid, r))
                if fid == "DTA-A012" and s.get("role") == "agent" and \
                   str(s.get("action", "")).startswith("python3 -c"):
                    steps.append({"index": sid, "role": "agent",
                                  "action": "python3 -c <chunked file write; content WITHHELD from bundle — explosives documentation, see raw trajectory>",
                                  "tool": (s.get("metadata") or {}).get("tool_name", "")})
                else:
                    steps.append(step_summary(s))

        sref = "seq-dtap-%02d" % n
        rec(sref, "observation", {
            "type": "behavior.tool_sequence",
            "source": "@source-dtap-bench",
            "run": "@run-dtap-bench",
            "observed_at": obs_at,
            "time_basis": "source_metadata",
            "files": [{"artifact": "@" + art_ref[r], "role": "evidence-trajectory",
                       "filename": os.path.basename(r)} for r in rels],
            "data": {
                "trajectory": f["trajectory"],
                "model": f["model"],
                "harness": f["harness"],
                "steps": steps,
                "length": len(steps),
                "provenance": "Decisive step window %s from reviewer notes; verifier byte-checked 2026-10-17. Steps recorded faithfully from trajectory JSON." % f["step_range"],
            },
        }, {"finding_id": fid, "step_range": f["step_range"]})

        fref = "finding-dtap-%02d" % n
        rec(fref, "observation", {
            "type": "intel.behavior",
            "source": "@source-dtap-bench",
            "run": "@run-dtap-bench",
            "observed_at": obs_at,
            "time_basis": "source_metadata",
            "files": [{"artifact": "@" + art_ref[r], "role": "evidence-trajectory",
                       "filename": os.path.basename(r)} for r in rels],
            "data": {
                "category": f["behavior_class"],
                "description": "[%s] %s" % (f["behavior_class"], f["title"]),
                "evaluations_seen_on": ["dtap-bench"],
                "models_affected": [f["model"]] if f["model"] != "n/a" else [],
                "first_observed": "",
                "provenance": "DTap-Bench review fleet (2 reviewers, adversarial review, byte-verifier); working/verified-findings.jsonl; DTA-A013 killed for fabricated quotes",
                "severity": "",
            },
        }, {
            "class_code": f["behavior_class"],
            "grade": f["grade"],
            "confidence": f["confidence"],
            "novelty": f["novelty"][:500],
            "caveats": f["caveats"][:500],
            "finding_id": fid,
            "step_range": f["step_range"],
            "verifier_note": "byte-verified 2026-10-17 (existence + verbatim substrings); adversarial re-check passed",
        })

        rec("edge-fseq-dtap-%02d" % n, "edge", {
            "subject": "@" + sref, "predicate": "supports", "object": "@" + fref,
            "basis": "OBSERVED", "cites": ["@" + fref],
            "note": "decisive step sequence evidences finding " + fid,
        }, {"finding_id": fid})
        for r in rels:
            rec("edge-finding-dtap-%02d-%s" % (n, art_ref[r].split("-")[-1]), "edge", {
                "subject": "@" + fref, "predicate": "supports",
                "object": "@" + traj_ref[r],
                "basis": "OBSERVED", "cites": ["@" + fref],
                "note": "finding observed in trajectory record",
            }, {"finding_id": fid})

    bundle = {"actor": ACTOR, "idempotency_key": IDEMPOTENCY,
              "lane": LANE, "records": records}
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)
    size = os.path.getsize(OUT_BUNDLE)

    # validate: every @ref resolvable, no dup refs, tags.lane everywhere
    refs = set()
    for r in records:
        if r["ref"] in refs:
            fail("dup ref " + r["ref"])
        refs.add(r["ref"])
        if r["tags"].get("lane") != LANE:
            fail("missing lane tag on " + r["ref"])
        if len(r["ref"]) > 64:
            fail("ref too long " + r["ref"])
    # edge endpoints resolve
    for r in records:
        if r["kind"] == "edge":
            for k in ("subject", "object"):
                tgt = r["body"][k].lstrip("@")
                if tgt not in refs:
                    fail("edge %s -> unknown %s" % (r["ref"], tgt))
    # cites targets: observation/sighting/artifact/claim/run only (no source-kind)
    kinds = {r["ref"]: r["kind"] for r in records}
    for r in records:
        if r["kind"] == "edge":
            for c in r["body"].get("cites", []):
                ck = kinds.get(c.lstrip("@"), "")
                if ck not in ("observation", "sighting", "artifact", "claim", "run", "edge"):
                    fail("edge %s cites bad kind %s (%s)" % (r["ref"], c, ck))

    kinds_count = {}
    for r in records:
        kinds_count[r["kind"]] = kinds_count.get(r["kind"], 0) + 1
    report = {"records": len(records), "kinds": kinds_count,
              "bundle_bytes": size, "bundle_sha256": sha256_file(OUT_BUNDLE),
              "idempotency_key": IDEMPOTENCY,
              "local_only": size > 80 * 1024 * 1024}
    json.dump(report, open(OUT_REPORT, "w"), indent=2)
    print("bundle: %d records, %d bytes, kinds=%s" % (len(records), size, kinds_count))
    print("local_only:", report["local_only"])


if __name__ == "__main__":
    main()
