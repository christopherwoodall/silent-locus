#!/usr/bin/env python3
"""Urlquery detail runner: fetch full reports for screened candidate rows,
plus the routify offset-49 gap row and the exact PROBE_PAYLOAD_ABC123 probe.
Idempotent: skips when the output file already holds valid JSON.
Raw detail files keep full bytes (never redacted); the lane summary must
carry parameter names and path shape only, never query values or tokens.
"""
import hashlib
import json
import os
import subprocess
import sys
import datetime

OUT = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-egress-broad-hunt/raw/urlquery")
UQ = os.path.expanduser("~/workspace/custom-connectors/custom.legacy-urlquery/bin/uq.py")
ENV = dict(os.environ, PYTHONPATH="/opt/muse/skills/custom-connector-setup/bin")

# (slug, report_id, why)
DETAILS = [
    ("d_routify_new_charlesg", "342ac40c-aabe-4b27-88d2-0bdd669e9aeb", "only post-Fleet-B routify row; page-content match suspected"),
    ("d_metadata_claude", "45a8f376-dc94-44cf-989a-b450c1f77507", "metadata.google.internal sample, claude.ai sign-in page"),
    ("d_probe_payload_uhbs", "a8da83f0-de34-4864-9829-ef4638595ed8", "PROBE_PAYLOAD sample, UHBS docs page"),
    ("d_echo_res20_trustxx", "e4a7d94c-8ba0-4d9a-a10c-099b2ab31677", "echo-res20 row new to Fleet B fetch, trustxx.co"),
    ("d_oss_cn_postfleetb", "226f3d6c-742c-403d-a568-09a27ca77907", "only post-Fleet-B oss-cn row, aanbiedingenzrpnl.shop"),
    ("d_unshare_dforge", "d4a013c7-f91d-4e11-913f-4a529cfee810", "unshare sample, dforge.site repeated-submission cluster"),
    ("d_resolv_testztest", "ad59ef43-0fde-4147-a673-665010182dc3", "resolv.conf sample, testztest.me DNS-monitor hostname"),
    ("d_routify_barehost_retry", "0bec7c6c-f196-4bea-914b-4d3c80b3beba", "retry of Fleet B 401 detail for the bare routify proxy host row"),
    ("d_aliyuncs_smaflowi_new", "dd8433a0-0fa1-40ca-af14-d1306266d437", "newest post-Fleet-B aliyuncs row, smaflowi.vip cluster continuation check"),
]

def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "_detail.log"), "a") as fh:
        fh.write(line + "\n")

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def write_capture(out, d, prov_lines):
    with open(out, "w") as fh:
        json.dump(d, fh, indent=2)
    h = sha256_of(out)
    with open(out + ".sha256", "w") as fh:
        fh.write(f"{h}  {os.path.basename(out)}\n")
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    with open(out + ".PROVENANCE.txt", "w") as fh:
        for ln in prov_lines:
            fh.write(ln + "\n")
        fh.write(f"retrieval time UTC: {now}\n")
        fh.write("method: authenticated urlquery api via uq.py (anonymous read of public reports; no login to urlquery.net web)\n")
        fh.write(f"sha256: {h}\n")
    return h

def main():
    os.makedirs(OUT, exist_ok=True)
    # Gap row: routify offset 49 (p0 fetched 49, p1 started at 50)
    gap_out = os.path.join(OUT, "fetch_f_a3_routify_gap49.json")
    if not (os.path.exists(gap_out) and "total_hits" in open(gap_out).read()):
        log("FETCH routify gap offset=49")
        try:
            r = subprocess.run([sys.executable, UQ, "search", "--query", "routify",
                                "--limit", "1", "--offset", "49"],
                               capture_output=True, text=True, timeout=300, env=ENV)
            d = json.loads(r.stdout)
            write_capture(gap_out, d, ["source URL: urlquery api search query='routify' limit=1 offset=49 (via uq.py search)"])
            log(f"DONE gap total={d.get('total_hits')} rows={d.get('reports')}")
        except Exception as e:
            log(f"FAIL gap :: {e}")
    else:
        log("SKIP gap (already captured)")
    # Exact Cohere payload string probe
    probe_out = os.path.join(OUT, "probe_a2_probe_payload_abc123.json")
    if not (os.path.exists(probe_out) and "total_hits" in open(probe_out).read()):
        log("PROBE PROBE_PAYLOAD_ABC123")
        try:
            r = subprocess.run([sys.executable, UQ, "search", "--query", "PROBE_PAYLOAD_ABC123",
                                "--limit", "50", "--offset", "0"],
                               capture_output=True, text=True, timeout=300, env=ENV)
            d = json.loads(r.stdout)
            write_capture(probe_out, d, ["source URL: urlquery api search query='PROBE_PAYLOAD_ABC123' limit=50 (via uq.py search)"])
            log(f"DONE exact-payload total={d.get('total_hits')} fetched={len(d.get('reports') or [])}")
        except Exception as e:
            log(f"FAIL exact-payload :: {e}")
    else:
        log("SKIP exact-payload (already captured)")
    for slug, rid, why in DETAILS:
        out = os.path.join(OUT, f"detail_{slug}.json")
        if os.path.exists(out):
            try:
                d = json.load(open(out))
                if isinstance(d, dict) and ("report_id" in d or "error" in d):
                    log(f"SKIP {slug} ({why[:40]}...)")
                    continue
            except Exception:
                pass
        log(f"DETAIL {slug} :: {rid} ({why})")
        try:
            r = subprocess.run([sys.executable, UQ, "report", rid],
                               capture_output=True, text=True, timeout=300, env=ENV)
            d = json.loads(r.stdout)
        except Exception as e:
            log(f"FAIL {slug} :: {e}")
            continue
        write_capture(out, d, [f"source URL: urlquery api report {rid} (via uq.py report)", f"reason: {why}"])
        keys = list(d.keys()) if isinstance(d, dict) else type(d)
        log(f"DONE {slug} keys={keys}")
    log("ALL DETAILS DONE")

if __name__ == "__main__":
    main()
