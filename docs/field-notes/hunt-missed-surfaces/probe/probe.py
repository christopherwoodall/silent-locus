#!/usr/bin/env python3
"""Lane 2 (PROBE) harness: polite fingerprint probes of queryable web surfaces.

Every probe is logged to probe-log.jsonl with the lane schema:
surface, probe_id, ts, target, http_code, bytes, result, fingerprints_matched, note.
Polite: <=1 request per 2s per host (per-host pacing enforced).
"""
import json, os, re, sys, time, subprocess, urllib.parse, hashlib

BASE = os.path.expanduser("~/workspace/silent-locus/collections/hunt-missed-surfaces/probe")
DATA = os.path.join(BASE, "data")
LOG = os.path.join(BASE, "probe-log.jsonl")
os.makedirs(DATA, exist_ok=True)

# Fingerprint set (from Transluce addendum + task brief). Case-insensitive.
FPS = [
    "zz=oai", "oai<digits>", "openai_research", "openairesearch",
    "openai research",
    "civilrightsdata", "bac-lac", "kansasmemory", "county.json",
    "virginia-projection.xls",
    "State_Id", "Measure_Id", "survey_Year_Key", "surveyYearKey",
    "Survey_Year_Key", "stateId", "measureId", "long_Nces_Id",
]

FP_RES = []
for fp in FPS:
    if fp == "oai<digits>":
        FP_RES.append(("oai<digits>", re.compile(r"oai\d{5,}", re.IGNORECASE)))
    else:
        FP_RES.append((fp, re.compile(re.escape(fp), re.IGNORECASE)))

_last_host = {}
PACE = 2.0  # seconds between requests to the same host


def host_of(url):
    return urllib.parse.urlparse(url).netloc.lower()


def polite(url):
    h = host_of(url)
    now = time.time()
    wait = PACE - (now - _last_host.get(h, 0))
    if wait > 0:
        time.sleep(wait)
    _last_host[h] = time.time()


def run_curl(url, method="GET", data=None, timeout=45, extra_args=()):
    body_file = os.path.join("/tmp", "probe_body.tmp")
    cmd = ["curl", "-sS", "--max-time", str(timeout), "-o", body_file,
           "-w", "%{http_code}", "-X", method]
    if data is not None:
        cmd += ["-d", data]
    cmd += list(extra_args)
    cmd += [url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15)
        code = r.stdout.strip() or "000"
        body = b""
        if os.path.exists(body_file):
            with open(body_file, "rb") as f:
                body = f.read()
        os.unlink(body_file) if os.path.exists(body_file) else None
        return code, body, r.stderr.strip()
    except subprocess.TimeoutExpired:
        return "000", b"", "curl: timeout (client-side)"
    except Exception as e:  # noqa: BLE001
        return "000", b"", f"curl: {e}"


def fp_scan(body):
    try:
        text = body.decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return []
    return sorted({name for name, rx in FP_RES if rx.search(text)})


def classify(code, method_note=""):
    if code == "200":
        return "ok"
    if code in ("404",):
        return "not-found"
    if code in ("401", "402", "403", "429"):
        return "auth-or-denied" if code in ("401", "402", "403") else "blocked-or-failed"
    if code.startswith("5") or code == "000" or code == "ERROR":
        return "blocked-or-failed"
    return "blocked-or-failed"


def probe(surface, probe_id, url, note="", method="GET", data=None,
          timeout=45, extra_args=(), result_override=None,
          save_body=True, max_save=262144, excerpt_note=False):
    polite(url)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    code, body, err = run_curl(url, method=method, data=data,
                               timeout=timeout, extra_args=extra_args)
    matches = fp_scan(body)
    result = result_override if result_override else classify(code)

    saved = ""
    if save_body and body:
        if len(body) <= max_save:
            fn = f"{probe_id}.body"
            with open(os.path.join(DATA, fn), "wb") as f:
                f.write(body)
            saved = f"data/{fn}"
        else:
            fn = f"{probe_id}.excerpt"
            with open(os.path.join(DATA, fn), "wb") as f:
                f.write(body[:16384])
            with open(os.path.join(DATA, f"{probe_id}.manifest"), "w") as mf:
                mf.write(f"body_bytes={len(body)} sha256={hashlib.sha256(body).hexdigest()} "
                         f"excerpt_bytes=16384\nurl={url}\n")
            saved = f"data/{fn}+manifest (body {len(body)} bytes > 1MB cap)"

    full_note = note
    if saved:
        full_note = (full_note + " | " if full_note else "") + f"saved: {saved}"
    if err and code in ("000", "ERROR"):
        full_note = (full_note + " | " if full_note else "") + f"transport: {err}"

    rec = {
        "surface": surface, "probe_id": probe_id, "ts": ts,
        "target": url, "http_code": code, "bytes": len(body),
        "result": result, "fingerprints_matched": matches,
        "note": full_note,
    }
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"[{code}] {probe_id}: {result} ({len(body)}b) matches={matches}")
    return rec


def main():
    # probes are supplied via a probes.jsonl plan file or argv; this entrypoint
    # is a no-op guard so accidental runs do nothing destructive.
    print("Lane-2 probe harness loaded. Use run_plan() from a plan script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
