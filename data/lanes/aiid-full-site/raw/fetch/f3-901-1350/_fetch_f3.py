#!/usr/bin/env python3
"""FETCH lane F3 (incidents 901-1350) for AIID full-site fleet.
Passive curl GET only, no login/session/POST. Polite rate ~1 req/s + jitter.
429/403 = HARD STOP for host for the rest of the run.
Resumable: skips pages whose .html + .sha256 + .PROVENANCE.txt already exist.
Dedup: a report page linked by multiple incidents is fetched once; later
incidents reference the same file (noted as shared in the log).
Incident 1152 is skipped entirely (overlap_prior_ingest).
"""
import hashlib
import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
BASE = HOME / "workspace/silent-locus/data/lanes/aiid-full-site/raw/fetch/f3-901-1350"
INV = HOME / "workspace/silent-locus/data/lanes/aiid-full-site/raw/snapshot/SNAPSHOT-INVENTORY.json"
UA = "silent-locus-lane-scanner/1.0"
LIMIT = int(os.environ.get("F3_LIMIT_PAGES", "0"))  # smoke-test cap, 0 = unlimited

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch_one(url, dest):
    """Returns (http_code:int|None, reason:str). Writes dest only on 200."""
    tmp = dest.with_suffix(".html.tmp")
    cmd = [
        "curl", "-sS", "-L", "--max-time", "30",
        "-A", UA, "-o", str(tmp), "-w", "%{http_code}", url,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
    except subprocess.TimeoutExpired:
        return None, "curl-timeout-45s"
    code_raw = r.stdout.strip()
    try:
        code = int(code_raw)
    except ValueError:
        code = None
    if code == 200:
        tmp.replace(dest)
        return 200, "ok"
    if tmp.exists():
        tmp.unlink()
    if code is not None:
        return code, f"http-{code}"
    err = (r.stderr or "").strip().splitlines()
    return None, "curl-error: " + (err[-1] if err else "unknown")

def main():
    BASE.mkdir(parents=True, exist_ok=True)
    inv = json.loads(INV.read_text())
    incs = [x for x in inv["incidents"] if 901 <= x["incident_id"] <= 1350]
    incs.sort(key=lambda x: x["incident_id"])

    log_path = BASE / "FETCH-LOG.json"
    log = {}
    if log_path.exists():
        try:
            log = json.loads(log_path.read_text()).get("incidents", {})
            log = {int(k): v for k, v in log.items()}
        except Exception:
            log = {}
    host_stop = None
    pages_done = 0

    def save_log():
        doc = {
            "lane": "F3",
            "incident_range": "901-1350",
            "source_inventory": "data/lanes/aiid-full-site/raw/snapshot/SNAPSHOT-INVENTORY.json",
            "method": "curl passive GET, no login, no session, no POST",
            "user_agent": UA,
            "rate": "at most 1 request/second with small jitter, 30s timeout",
            "host_stop": host_stop,
            "incidents": {str(k): log[k] for k in sorted(log)},
        }
        tmp = BASE / f"FETCH-LOG.json.{os.getpid()}.tmp"
        tmp.write_text(json.dumps(doc, indent=2))
        tmp.replace(log_path)

    # Pre-seed the skipped overlap entry
    if 1152 not in log:
        log[1152] = {
            "incident_id": 1152,
            "status": "skipped_overlap_prior_ingest",
            "incident_page": None,
            "reports": [],
            "fetched_pages": 0,
            "unfetched_pages": 0,
            "note": "SKIPPED: overlap_prior_ingest in SNAPSHOT-INVENTORY.json (Replit incident, already ingested by incident-7050 fleet, batch 756a273f). Evidence lives in data/lanes/incident-7050-antigravity/raw/, not this dir. Incident page and 5 report pages (5577, 5578, 5593, 6113, 6126) NOT fetched by F3.",
        }

    fetched_reports = {}  # report_id -> file path (from prior log runs too)
    for ent in log.values():
        for rep in ent.get("reports", []):
            if rep.get("status") == "fetched" and rep.get("file"):
                fetched_reports[rep["report_id"]] = rep["file"]

    for inc in incs:
        iid = inc["incident_id"]
        if iid == 1152:
            continue
        ent = log.get(iid)
        if ent is None:
            ent = {"incident_id": iid, "incident_page": None, "reports": [], "note": ""}
            log[iid] = ent
        # Incident page
        ip = ent.get("incident_page")
        if ip is None or ip.get("status") != "fetched":
            dest = BASE / f"incident-{iid}.html"
            if dest.exists() and (dest.with_suffix("").with_suffix(".html.sha256").exists() or (BASE / f"incident-{iid}.html.sha256").exists()):
                pass  # handled below by generic resume check
            if dest.exists() and (BASE / f"incident-{iid}.html.sha256").exists() and (BASE / f"incident-{iid}.html.PROVENANCE.txt").exists():
                digest = sha256_of(dest)
                ip = {"url": inc["incident_page_url"], "status": "fetched",
                      "http_status": 200, "file": f"incident-{iid}.html",
                      "bytes": dest.stat().st_size, "sha256": digest,
                      "note": "resumed: file already present from prior run"}
                ent["incident_page"] = ip
            else:
                now = datetime.now(timezone.utc).isoformat()
                code, reason = fetch_one(inc["incident_page_url"], dest)
                if code in (403, 429):
                    host_stop = {"http_status": code, "url": inc["incident_page_url"],
                                 "at_utc": now, "action": "HARD STOP for host for rest of run; no retry, no workaround"}
                    ent["incident_page"] = {"url": inc["incident_page_url"], "status": "unfetched",
                                            "http_status": code, "file": None, "reason": reason + " -> host hard stop"}
                    save_log()
                    print(f"HARD STOP host: {code} on {inc['incident_page_url']}", flush=True)
                    return 2
                if code == 200:
                    digest = sha256_of(dest)
                    (BASE / f"incident-{iid}.html.sha256").write_text(f"{digest}  incident-{iid}.html\n")
                    (BASE / f"incident-{iid}.html.PROVENANCE.txt").write_text(
                        f"source_url: {inc['incident_page_url']}\nretrieved_utc: {now}\n"
                        f"method: curl -L --max-time 30 passive GET, no login, no session, no POST\n"
                        f"user_agent: {UA}\nhttp_status: 200\nsha256: {digest}\n")
                    ip = {"url": inc["incident_page_url"], "status": "fetched", "http_status": 200,
                          "file": f"incident-{iid}.html", "bytes": dest.stat().st_size, "sha256": digest}
                    pages_done += 1
                else:
                    ip = {"url": inc["incident_page_url"], "status": "unfetched",
                          "http_status": code, "file": None, "reason": reason}
                ent["incident_page"] = ip
                save_log()
                if LIMIT and pages_done >= LIMIT:
                    print(f"LIMIT reached ({LIMIT} new pages)", flush=True)
                    return 0
                time.sleep(1.0 + random.uniform(0, 0.5))
        # Report pages
        by_id = {r["report_id"]: r for r in ent.get("reports", [])}
        new_reports = []
        for rid, rurl in zip(inc["report_ids"], inc["report_page_urls"]):
            if rid in fetched_reports:
                new_reports.append({"report_id": rid, "url": rurl, "status": "fetched",
                                    "http_status": 200, "file": fetched_reports[rid],
                                    "shared_with_other_incident": True,
                                    "note": "same report page fetched once for another incident in range; shared file"})
                continue
            prev = by_id.get(rid)
            if prev is not None and prev.get("status") == "fetched":
                fetched_reports[rid] = prev["file"]
                new_reports.append(prev)
                continue
            dest = BASE / f"report-{rid}.html"
            if dest.exists() and (BASE / f"report-{rid}.html.sha256").exists() and (BASE / f"report-{rid}.html.PROVENANCE.txt").exists():
                digest = sha256_of(dest)
                rec = {"report_id": rid, "url": rurl, "status": "fetched", "http_status": 200,
                       "file": f"report-{rid}.html", "bytes": dest.stat().st_size, "sha256": digest,
                       "note": "resumed: file already present from prior run"}
                fetched_reports[rid] = rec["file"]
                new_reports.append(rec)
                continue
            now = datetime.now(timezone.utc).isoformat()
            code, reason = fetch_one(rurl, dest)
            if code in (403, 429):
                host_stop = {"http_status": code, "url": rurl, "at_utc": now,
                             "action": "HARD STOP for host for rest of run; no retry, no workaround"}
                new_reports.append({"report_id": rid, "url": rurl, "status": "unfetched",
                                    "http_status": code, "file": None, "reason": reason + " -> host hard stop"})
                ent["reports"] = new_reports
                save_log()
                print(f"HARD STOP host: {code} on {rurl}", flush=True)
                return 2
            if code == 200:
                digest = sha256_of(dest)
                (BASE / f"report-{rid}.html.sha256").write_text(f"{digest}  report-{rid}.html\n")
                (BASE / f"report-{rid}.html.PROVENANCE.txt").write_text(
                    f"source_url: {rurl}\nretrieved_utc: {now}\n"
                    f"method: curl -L --max-time 30 passive GET, no login, no session, no POST\n"
                    f"user_agent: {UA}\nhttp_status: 200\nsha256: {digest}\n")
                rec = {"report_id": rid, "url": rurl, "status": "fetched", "http_status": 200,
                       "file": f"report-{rid}.html", "bytes": dest.stat().st_size, "sha256": digest}
                fetched_reports[rid] = rec["file"]
                pages_done += 1
            else:
                rec = {"report_id": rid, "url": rurl, "status": "unfetched",
                       "http_status": code, "file": None, "reason": reason}
            new_reports.append(rec)
            save_log()
            if LIMIT and pages_done >= LIMIT:
                ent["reports"] = new_reports
                # pad remaining reports as not-attempted for this smoke run? No: keep partial; resume fills rest.
                save_log()
                print(f"LIMIT reached ({LIMIT} new pages)", flush=True)
                return 0
            time.sleep(1.0 + random.uniform(0, 0.5))
        ent["reports"] = new_reports
        ent["fetched_pages"] = (1 if ent["incident_page"] and ent["incident_page"].get("status") == "fetched" else 0) \
            + sum(1 for r in new_reports if r.get("status") == "fetched")
        ent["unfetched_pages"] = (1 if ent["incident_page"] and ent["incident_page"].get("status") != "fetched" else 0) \
            + sum(1 for r in new_reports if r.get("status") != "fetched")
        save_log()
    # Final counts on skipped entry
    log[1152]["fetched_pages"] = 0
    log[1152]["unfetched_pages"] = 0
    save_log()
    print("DONE: all incidents processed", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
