#!/usr/bin/env python3
"""Lantern-1 worker: fetch shard-1 targets reusing fetch_panels.fetch_one exactly.

Atomic single-line appends to shared fetch-log.jsonl (open in append mode,
write one line, flush, fsync). No HTML parsing, raw bytes only.
"""
import json, os, sys, time

WORK = os.path.expanduser("~/workspace/silent-locus/data/lanes/cairn-panels/working")
sys.path.insert(0, WORK)
from fetch_panels import fetch_one, UA, SKIP_PORTS  # noqa: E402

REQUIRED = ["ip", "port", "harness", "url", "reachable", "http_status",
            "final_url", "size", "content_type", "fetch_error",
            "skipped", "skip_reason"]

def normalize(rec, ip, port, harness):
    """Shape fetch_one's record into the exact log schema."""
    if rec.get("skipped"):
        return {"ip": ip, "port": port, "harness": harness,
                "url": None, "reachable": False,
                "http_status": None, "final_url": None, "size": 0,
                "content_type": None, "fetch_error": None,
                "skipped": True, "skip_reason": rec.get("skip_reason")}
    out = {"ip": ip, "port": port, "harness": harness,
           "url": rec.get("url"), "reachable": bool(rec.get("reachable")),
           "http_status": rec.get("http_status"), "final_url": rec.get("final_url"),
           "size": rec.get("size") or 0,
           "content_type": rec.get("content_type"),
           "fetch_error": rec.get("fetch_error"), "skipped": False,
           "skip_reason": None}
    assert all(k in out for k in REQUIRED), out.keys()
    return out

def atomic_append(path, line):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        os.write(fd, (line + "\n").encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)

def main():
    shard = json.load(open(os.path.join(WORK, "fetch-shard-1.json"), encoding="utf-8"))
    fl_path = os.path.join(WORK, "fetch-log.jsonl")
    # resume: skip (ip,port) already logged as reachable by anyone
    done = set()
    if os.path.exists(fl_path):
        for line in open(fl_path, encoding="utf-8"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("reachable"):
                done.add((d["ip"], d["port"]))
    todo = [t for t in shard if (t["ip"], t["port"]) not in done]
    print(f"shard: {len(shard)}, already reachable: {len(done)}, remaining: {len(todo)}", flush=True)
    ok = fail = skipped = 0
    for i, t in enumerate(todo):
        ip, port, harness = t["ip"], t["port"], t["harness"]
        try:
            rec = fetch_one(ip, port, harness)
            rec = normalize(rec, ip, port, harness)
            if rec["skipped"]:
                skipped += 1
            elif rec["reachable"]:
                ok += 1
            else:
                fail += 1
        except Exception as e:
            rec = {"ip": ip, "port": port, "harness": harness, "url": None,
                   "reachable": False, "http_status": None, "final_url": None,
                   "size": 0, "content_type": None,
                   "fetch_error": f"worker_exception: {e!r}", "skipped": False,
                   "skip_reason": None}
            fail += 1
        atomic_append(fl_path, json.dumps(rec))
        status = (rec.get("http_status") or rec.get("fetch_error") or rec.get("skip_reason") or "?")
        print(f"[{i+1}/{len(todo)}] {ip}:{port} ({harness}) -> {status}", flush=True)
        time.sleep(1.5)  # politeness
    print(f"DONE ok={ok} fail={fail} skipped={skipped}", flush=True)

if __name__ == "__main__":
    main()
