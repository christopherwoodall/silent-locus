#!/usr/bin/env python3
"""Urlquery fetch runner, phase 2: full/small sets + 50-row newest samples.
Idempotent: skips a fetch when its output file already holds valid JSON
with a total_hits field. Writes per-fetch JSON + .PROVENANCE.txt + .sha256.
Progress log: _fetch.log in the same dir.
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

# (slug, query, limit, offset)
FETCHES = [
    # Small sets: fetch in full (limit above total)
    ("f_b_routify_fullhost", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com", 50, 0),
    ("f_b_routify_oct27", "routify date:[2026-10-27 TO 2026-10-28]", 50, 0),
    ("f_c_trustexc", "trustexc.top", 50, 0),
    ("f_c_echo_res20", "echo-res20.oss-cn-hongkong.aliyuncs.com", 50, 0),
    ("f_a2_probe_payload", "PROBE_PAYLOAD", 50, 0),
    # Routify full set: 79 total, two pages
    ("f_a3_routify_p0", "routify", 50, 0),
    ("f_a3_routify_p1", "routify", 50, 50),
    # Shape 1: metadata.google.internal, 223 total, first page
    ("f_a1_metadata_google", "metadata.google.internal", 50, 0),
    # Baselines, newest 100 each (two pages)
    ("f_a2_aliyuncs_p0", "aliyuncs.com", 50, 0),
    ("f_a2_aliyuncs_p1", "aliyuncs.com", 50, 50),
    ("f_a2_oss_cn_p0", "oss-cn-", 50, 0),
    ("f_a2_oss_cn_p1", "oss-cn-", 50, 50),
    # Shape samples, newest 50 each
    ("f_a4_unshare", "unshare", 50, 0),
    ("f_a4_unshare_U", "unshare -U", 50, 0),
    ("f_a4_unshare_Urm", "unshare -Urm", 50, 0),
    ("f_a5_curl_o", "curl -o", 50, 0),
    ("f_a5_wget_O", "wget -O", 50, 0),
    ("f_a6_resolv_conf", "resolv.conf", 50, 0),
    ("f_a6_resolv_conf_p1", "resolv.conf", 50, 50),
    ("f_a6_uname_a", "uname -a", 50, 0),
    ("f_a2_upload_file", "upload-file", 50, 0),
    ("f_a2_azure_blob", "blob.core.windows.net", 50, 0),
    ("f_a2_gcs", "storage.googleapis.com", 50, 0),
    ("f_a2_s3", "s3.amazonaws.com", 50, 0),
    ("f_a2_r2", "r2.dev", 50, 0),
    ("f_c_qtapi", "qtapi.flowmaeri.top", 50, 0),
    ("f_c_trace", "trace/v1/report", 50, 0),
]

def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "_fetch.log"), "a") as fh:
        fh.write(line + "\n")

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, query, limit, offset in FETCHES:
        out = os.path.join(OUT, f"fetch_{slug}.json")
        if os.path.exists(out):
            try:
                with open(out) as fh:
                    d = json.load(fh)
                if isinstance(d, dict) and "total_hits" in d:
                    log(f"SKIP {slug} total={d['total_hits']} fetched={len(d.get('reports') or [])}")
                    continue
            except Exception:
                pass
        log(f"FETCH {slug} :: {query} limit={limit} offset={offset}")
        try:
            r = subprocess.run(
                [sys.executable, UQ, "search", "--query", query,
                 "--limit", str(limit), "--offset", str(offset)],
                capture_output=True, text=True, timeout=300, env=ENV,
            )
            d = json.loads(r.stdout)
        except Exception as e:
            log(f"FAIL {slug} :: {e}")
            continue
        with open(out, "w") as fh:
            json.dump(d, fh, indent=2)
        h = sha256_of(out)
        with open(out + ".sha256", "w") as fh:
            fh.write(f"{h}  fetch_{slug}.json\n")
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        with open(out + ".PROVENANCE.txt", "w") as fh:
            fh.write(f"source URL: urlquery api search query='{query}' limit={limit} offset={offset} (via uq.py search)\n")
            fh.write(f"retrieval time UTC: {now}\n")
            fh.write("method: authenticated urlquery api search via uq.py (anonymous read of public reports; no login to urlquery.net web)\n")
            fh.write(f"sha256: {h}\n")
        log(f"DONE {slug} total={d.get('total_hits')} fetched={len(d.get('reports') or [])}")
    log("ALL FETCHES DONE")

if __name__ == "__main__":
    main()
