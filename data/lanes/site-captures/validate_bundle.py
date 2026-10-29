#!/usr/bin/env python3
"""Independent adversarial check of bundle.site-captures.json.

Re-derives expectations from the LEGACY evidence (evidence/site-captures/),
not from build_bundle.py or the lane raw/ copy. Fails loudly on any mismatch.
"""
import json, os, hashlib, sys

REPO = os.path.expanduser("~/workspace/silent-locus")
LEGACY = os.path.join(REPO, "evidence/site-captures")
BUNDLE = os.path.join(REPO, "data/lanes/site-captures/bundle.site-captures.json")
LANE_RAW = os.path.join(REPO, "data/lanes/site-captures/raw")

errors = []
def check(cond, msg):
    if not cond:
        errors.append(msg)

# --- 1. legacy ground truth ---
legacy = {}
for d in sorted(os.listdir(LEGACY)):
    j = json.load(open(os.path.join(LEGACY, d, "surface_capture.json")))
    bp = os.path.join(LEGACY, d, "surface_capture_body.txt")
    body = open(bp, "rb").read() if os.path.exists(bp) else None
    if body is not None:
        h = hashlib.sha256(body).hexdigest()
        if h != j["sha256"]:
            # allow the documented LF-normalization recovery
            crlf = body.replace(b"\n", b"\r\n").replace(b"\r\r\n", b"\r\n")
            if hashlib.sha256(crlf).hexdigest() == j["sha256"] and len(crlf) == j["bytes"]:
                pass  # recoverable; builder must carry raw_file_note
            else:
                check(False, f"{d}: body bytes do not match capture sha256 and are not LF-recoverable")
    legacy[d] = (j, body)
check(len(legacy) == 33, f"legacy site count {len(legacy)} != 33")

bundle = json.load(open(BUNDLE))
check(bundle.get("bundle") == 2, "bundle version != 2")
check(bundle.get("actor") == "agent:lane-ingest/site-captures", "actor mismatch")
check(bool(bundle.get("idempotency_key")), "missing idempotency_key")
recs = bundle["records"]
refs = [r["ref"] for r in recs]
check(len(refs) == len(set(refs)), "duplicate refs")

kinds = {}
for r in recs:
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
check(kinds.get("observation") == 33, f"observations {kinds.get('observation')} != 33")
check(kinds.get("source") == 1, "source count != 1")
check(kinds.get("run") == 1, "run count != 1")
check(kinds.get("claim") == 1, "claim count != 1")

by_ref = {r["ref"]: r for r in recs}

# --- 2. per-observation checks against legacy ---
n_ok = n_fail = 0
for d, (j, body) in legacy.items():
    matches = [r for r in recs if r["kind"] == "observation"
               and r["body"]["data"]["requested_url"] == j["url"]]
    check(len(matches) == 1, f"{d}: {len(matches)} observations for url {j['url']}")
    if not matches:
        continue
    r = matches[0]
    b = r["body"]
    check(b["type"] == "web.capture", f"{d}: wrong type")
    check(b["source"] == "@src", f"{d}: bad source ref")
    check(b["run"] == "@run1", f"{d}: bad run ref")
    check(b["observed_at"] == j["retrieved_at_utc"].replace("+00:00", "Z"), f"{d}: observed_at mismatch")
    check(b["time_basis"] == "collector_clock", f"{d}: time_basis")
    check(b["data_schema"] == "urn:factum:web:web-capture:1", f"{d}: data_schema")
    check(b["data"]["capture_kind"] == "http", f"{d}: capture_kind")
    if j.get("http_status"):
        check(b["data"].get("http_status") == j["http_status"], f"{d}: http_status mismatch")
        n_ok += 1
    else:
        check("http_status" not in b["data"], f"{d}: unexpected http_status in data")
        n_fail += 1
    t = r["tags"]
    check(t.get("lane") == "site-captures", f"{d}: lane tag")
    for k, v in t.items():
        check(isinstance(v, str), f"{d}: tag {k} is not a string: {v!r}")
    if body is not None:
        check(t.get("sha256") == j["sha256"], f"{d}: sha256 tag mismatch")
        check(t.get("bytes") == str(j["bytes"]), f"{d}: bytes tag mismatch")
        cp = os.path.join(REPO, t.get("cached_path", ""))
        check(os.path.isfile(cp), f"{d}: cached_path missing: {t.get('cached_path')}")
        if os.path.isfile(cp):
            disk = open(cp, "rb").read()
            okbytes = (hashlib.sha256(disk).hexdigest() == j["sha256"] or
                       hashlib.sha256(disk.replace(b"\n", b"\r\n").replace(b"\r\r\n", b"\r\n")).hexdigest() == j["sha256"])
            check(okbytes, f"{d}: cached file bytes do not reproduce capture hash")
            if hashlib.sha256(disk).hexdigest() != j["sha256"]:
                check("raw_file_note" in t, f"{d}: LF-normalized body lacks raw_file_note")
    else:
        check(t.get("error") == j["error"], f"{d}: error tag mismatch")
        check("cached_path" not in t, f"{d}: failed capture should not have cached_path")
check(n_ok == 24 and n_fail == 9, f"ok/fail counts {n_ok}/{n_fail} != 24/9")

# --- 3. claim checks ---
claim = [r for r in recs if r["kind"] == "claim"][0]
cb = claim["body"]
check(cb["subject"] == "@run1", "claim subject")
check(cb["basis"] == "OBSERVED", "claim basis")
check(len(cb["cites"]) == 33, f"claim cites {len(cb['cites'])} != 33")
for c in cb["cites"]:
    key = c[1:] if c.startswith("@") else c
    check(key in by_ref and by_ref[key]["kind"] == "observation", f"claim cite {c} does not resolve to an observation")
v = cb["value"]
check(v["probed"] == 33 and v["http_200_with_bytes"] == 24 and v["failed"] == 9, "claim value counts")
check(v["failed_breakdown"]["http_404"] == 7, "404 count")
check(v["failed_breakdown"]["connection_failure"] == 2, "connfail count")
check(len(v["failed_hosts"]) == 9, "failed_hosts list")

# --- 4. run/source checks ---
run = [r for r in recs if r["kind"] == "run"][0]
rb = run["body"]
check(rb["run_kind"] == "agent_surface_capture_sweep", "run_kind")
check(rb["coverage"]["scanned"] == 33 and rb["coverage"]["total"] == 33 and rb["coverage"]["complete"] is True, "run coverage")
src = [r for r in recs if r["kind"] == "source"][0]
check(src["body"]["locator"] == "data/lanes/site-captures/", "source locator")
check(src["tags"].get("legacy_path") == "evidence/site-captures/", "source legacy_path tag")

# --- 5. no symlinks under the lane dir ---
for root, dirs, files in os.walk(os.path.join(REPO, "data/lanes/site-captures")):
    for n in dirs + files:
        check(not os.path.islink(os.path.join(root, n)), f"symlink found: {os.path.join(root, n)}")

if errors:
    print(f"VALIDATION FAILED ({len(errors)}):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("VALIDATION PASSED: 36 records, 33 observations, all checks green")
