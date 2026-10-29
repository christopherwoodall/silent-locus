#!/usr/bin/env python3
"""Cryptologist live-liveness check for the five known bytebin fleet pastes.

Passive GET only, 6s spacing, few requests/min. Compares live bytes to the
Oct 7-8 cached copies and records SHA-256 both sides.
"""
import hashlib, os, sys, time, urllib.request, datetime

RAW = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/2026-10-16-slow-swarm-crawl/cryptologist/raw")
CACHED = os.path.expanduser(
    "~/workspace/silent-locus/evidence/transluce-api/deaddrop-grammar/raw")
UA = {"User-Agent": "swarm-hunt-passive-crawl/1.0"}

PASTES = [
    ("bytebin.rkslot.nl", "1UFK9Jock2ARPqwn"),
    ("bytebin.rkslot.nl", "UQltY2beSM1Oaczz"),
    ("bytebin.rkslot.nl", "sjqT4l3Op4Qrk9r1"),
    ("bytebin.lucko.me", "3a5hVHJkt9"),
    ("bytebin.lucko.me", "mviJXk5gnj"),
]

def sha(b): return hashlib.sha256(b).hexdigest()

def fetch(host, pid):
    url = f"https://{host}/{pid}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
results = []
for i, (host, pid) in enumerate(PASTES):
    cached_path = os.path.join(CACHED, f"paste_{host}_{pid}.html")
    cached_bytes = open(cached_path, "rb").read()
    cached_sha = sha(cached_bytes)
    try:
        status, body = fetch(host, pid)
        live_sha = sha(body)
        changed = live_sha != cached_sha
        out = os.path.join(RAW, f"bytebin-live-{host}-{pid}.html")
        open(out, "wb").write(body)
        line = f"{host}/{pid}: HTTP {status} live_sha={live_sha} cached_sha={cached_sha} changed={changed}"
    except Exception as e:
        line = f"{host}/{pid}: FETCH-FAILED {type(e).__name__}: {e}"
    print(line, flush=True)
    results.append(line)
    if i < len(PASTES) - 1:
        time.sleep(6)

prov = (f"source: https://bytebin.rkslot.nl, https://bytebin.lucko.me "
        f"(individual paste URLs; see bytebin-liveness.txt)\n"
        f"retrieval_time_utc: {now}\n"
        f"method: passive HTTPS GET, 6s spacing, UA swarm-hunt-passive-crawl/1.0\n"
        f"cached_reference: ~/workspace/silent-locus/evidence/transluce-api/"
        f"deaddrop-grammar/raw/ (Oct 7-8 capture)\n")
open(os.path.join(RAW, "bytebin-liveness.txt"), "w").write("\n".join(results) + "\n")
open(os.path.join(RAW, "PROVENANCE.txt"), "w").write(prov + "\n")
for l in results:
    open(os.path.join(RAW, "PROVENANCE.txt"), "a").write("# " + l + "\n")
