#!/usr/bin/env python3
"""Urlquery probe runner, phase 1: totals-only (limit=1) for all lane queries.
Idempotent: skips a query when its output file already holds valid JSON
with a total_hits field. Writes per-query JSON + .PROVENANCE.txt + .sha256.
Progress log: _probes.log in the same dir.
Run: python3 _run_probes.py  (from anywhere; paths are absolute)
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

# (slug, query string)
QUERIES = [
    # Part A shape 1: cloud-metadata reach
    ("a1_169_254_169_254", "169.254.169.254"),
    ("a1_fd00_ec2_254", "fd00:ec2::254"),
    ("a1_metadata_google_internal", "metadata.google.internal"),
    ("a1_100_100_100_200", "100.100.100.200"),
    # Part A shape 2: object-storage upload
    ("a2_upload_file", "upload-file"),
    ("a2_proxy_temp_file", "proxy_temp_file"),
    ("a2_probe_payload", "PROBE_PAYLOAD"),
    ("a2_put_probe", "put_probe"),
    ("a2_aliyuncs", "aliyuncs.com"),
    ("a2_oss_cn", "oss-cn-"),
    ("a2_azure_blob", "blob.core.windows.net"),
    ("a2_gcs", "storage.googleapis.com"),
    ("a2_s3", "s3.amazonaws.com"),
    ("a2_r2", "r2.dev"),
    # Part A shape 3: named probe hosts
    ("a3_routify", "routify"),
    # Part A shape 4: user-namespace escape
    ("a4_unshare", "unshare"),
    ("a4_unshare_U", "unshare -U"),
    ("a4_unshare_Urm", "unshare -Urm"),
    # Part A shape 5: download-then-execute
    ("a5_curl_o", "curl -o"),
    ("a5_wget_O", "wget -O"),
    # Part A shape 6: recon-then-egress markers
    ("a6_resolv_conf", "resolv.conf"),
    ("a6_uname_a", "uname -a"),
    # Part B concrete hosts
    ("b_routify_file_proxy_sg_full", "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com"),
    ("b_routify_file_proxy_sg", "routify-file-proxy-sg"),
    ("b_routify_alibaba_inc", "routify.alibaba-inc.com"),
    ("b_routify_online", "routify-online.alibaba-inc.com"),
    ("b_routify_pub", "routify-pub.alibaba-inc.com"),
    ("b_sanmaohe_full", "sanmaohe.oss-cn-beijing.aliyuncs.com"),
    ("b_sanmaohe", "sanmaohe"),
    ("b_upload_test_bin", "upload/test.bin"),
    # url.domain: syntax tests
    ("b_domain_routify_proxy", "url.domain:routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com"),
    ("b_domain_sanmaohe", "url.domain:sanmaohe.oss-cn-beijing.aliyuncs.com"),
    # date-window syntax test: routify submissions on/after Fleet B day
    ("b_date_routify_oct27", "routify date:[2026-10-27 TO 2026-10-28]"),
    # Appendix hosts from Fleet B (totals-only re-check)
    ("c_smaflowi", "smaflowi"),
    ("c_ysviposs", "ysviposs"),
    ("c_qtapi_flowmaeri", "qtapi.flowmaeri.top"),
    ("c_trustexc", "trustexc.top"),
    ("c_echo_res20", "echo-res20.oss-cn-hongkong.aliyuncs.com"),
    ("c_f4nt34", "f4nt34-oowqn-vqmf98.oss-cn-chengdu.aliyuncs.com"),
    ("c_50c5", "50c5.cc"),
    ("c_trace_v1_report", "trace/v1/report"),
]

def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    with open(os.path.join(OUT, "_probes.log"), "a") as fh:
        fh.write(line + "\n")

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, query in QUERIES:
        out = os.path.join(OUT, f"probe_{slug}.json")
        if os.path.exists(out):
            try:
                with open(out) as fh:
                    d = json.load(fh)
                if isinstance(d, dict) and "total_hits" in d:
                    log(f"SKIP {slug} total={d['total_hits']} (already captured)")
                    continue
            except Exception:
                pass
        log(f"QUERY {slug} :: {query}")
        try:
            r = subprocess.run(
                [sys.executable, UQ, "search", "--query", query, "--limit", "1"],
                capture_output=True, text=True, timeout=240, env=ENV,
            )
            raw = r.stdout
            d = json.loads(raw)
        except Exception as e:
            log(f"FAIL {slug} :: {e}")
            continue
        with open(out, "w") as fh:
            json.dump(d, fh, indent=2)
        h = sha256_of(out)
        with open(out + ".sha256", "w") as fh:
            fh.write(f"{h}  probe_{slug}.json\n")
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        with open(out + ".PROVENANCE.txt", "w") as fh:
            fh.write(f"source URL: urlquery api search query='{query}' limit=1 (via uq.py search)\n")
            fh.write(f"retrieval time UTC: {now}\n")
            fh.write("method: authenticated urlquery api search via uq.py (anonymous read of public reports; no login to urlquery.net web)\n")
            fh.write(f"sha256: {h}\n")
        total = d.get("total_hits", "?") if isinstance(d, dict) else "?"
        log(f"DONE {slug} total={total}")
    log("ALL PROBES DONE")

if __name__ == "__main__":
    main()
