#!/usr/bin/env python3
"""WORKSTREAM C2 — Lane J re-sweep of the 167 UNVERIFIED negatives.

The lane-J Diffend sweep (scripts/sweep_july7.py, urllib, PACE=3s) left 167
names as "fetch_failed:RemoteDisconnected: Remote end closed connection
without response". Those are UNVERIFIED negatives, not confirmed absences.

This script re-sweeps exactly those 167 names with GENTLER pacing than the
failed attempt:
  - curl subprocess for fetching (urllib's TLS handshake gets dropped by
    Diffend's edge; curl succeeded on the same URLs in the Diffend retry lane)
  - PACE = 6.0s between requests (vs 3.0s in the failed attempt)
  - MAX_ATTEMPTS = 3 with BACKOFFS = [30, 240] on connection-close
  - 180s cooldown every 10 names; 600s cooldown after 4 consecutive failures
  - single-threaded, read-only, no auth

Resumable: re-runs skip names already in the resweep output file. At the end
the resweep rows are merged back into the main July-7 JSONL, replacing ONLY
the 167 previously-unverified rows; verified rows are never touched.

Output: data/2026-07-07-july7-wave/raw/diffend_sweep_resweep_july7.jsonl (+ progress.log).
"""
import html
import json
import os
import re
import subprocess
import sys
import time

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATADIR = os.path.join(PROJ, "data", "2026-07-07-july7-wave")
MAIN = os.path.join(DATADIR, "raw/diffend_sweep_results_july7.jsonl")
RESWEEP = os.path.join(DATADIR, "raw/diffend_sweep_resweep_july7.jsonl")
LOG = os.path.join(DATADIR, "progress.log")

DIFFEND = "https://my.diffend.io"
UA = "rubygems-july7-resweep/1.0 (read-only inventory re-sweep; no install)"
PACE = 6.0
MAX_ATTEMPTS = 3
BACKOFFS = [30, 240]
COOLDOWN_EVERY = 10
COOLDOWN_SECS = 180
FAIL_COOLDOWN = 600
FAIL_COOLDOWN_AT = 4

MECH_PATTERNS = [
    ("go-import", re.compile(r"go-import", re.I)),
    ("jina-laundered", re.compile(r"[rs]\.jina\.ai", re.I)),
    ("webhook-deaddrop", re.compile(r"web_hooks?|A000|ZZEND|southpxdatapp", re.I)),
    ("xss-exfil", re.compile(
        r"oast\.online|webhook\.site|<script|onerror=|alert\s*\(|"
        r"javascript:|expression\(|<style", re.I)),
    ("ssti-probe", re.compile(
        r"\$\{7\*7\}|\{\{\s*7\*7|<%=\s*7\*7\s*%>|<%25=\s*7\*7\s*%>|"
        r"\*\{|constructor", re.I)),
    ("county-json", re.compile(r"county\.json", re.I)),
    ("empty-summary", re.compile(r"summary:\s*x\b", re.I)),
]

GRAMMAR_PATTERNS = [
    ("epoch_suffix", re.compile(r"\d{10,13}$")),
    ("try_zz", re.compile(r"try[a-z][0-9]zz")),
    ("zz_prefix", re.compile(r"^zz")),
    ("oai_prefix", re.compile(r"^oai")),
    ("goimport_name", re.compile(r"goimport|go_import", re.I)),
    ("proxy_name", re.compile(r"proxy", re.I)),
    ("probe_name", re.compile(r"probe", re.I)),
    ("fetch_name", re.compile(r"fetch", re.I)),
    ("yard_name", re.compile(r"yard", re.I)),
    ("xss_name", re.compile(r"xss", re.I)),
    ("ssti_name", re.compile(r"ssti", re.I)),
    ("apex_name", re.compile(r"apex", re.I)),
    ("attacker_name", re.compile(r"attacker", re.I)),
    ("test_name", re.compile(r"^test-", re.I)),
]


def name_grammars(name):
    return [label for label, rx in GRAMMAR_PATTERNS if rx.search(name)]


def log(msg):
    line = "%s %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def curl_get(url):
    """(body_text|None, http_code|int, err_str|None). Follows redirects."""
    try:
        p = subprocess.run(
            ["curl", "-sSL", "-A", UA, "--max-time", "90",
             "-o", "-", "-w", "\n%{http_code}", url],
            capture_output=True, timeout=105)
    except Exception as e:
        return None, 0, "curl_exc:%s" % str(e)[:80]
    if p.returncode != 0:
        return None, 0, "curl_rc%d:%s" % (p.returncode, p.stderr.decode()[:80])
    out = p.stdout.decode("utf-8", "ignore")
    if "\n" not in out:
        return None, 0, "curl_empty_output"
    body, code = out.rsplit("\n", 1)
    try:
        code = int(code.strip())
    except ValueError:
        return None, 0, "curl_bad_code:%s" % code[:20]
    if code == 0 or not body:
        return None, code, "curl_no_body"
    time.sleep(PACE)
    return body, code, None


def gem_versions(name):
    h, code, err = curl_get("%s/gems/%s" % (DIFFEND, name))
    if err is not None:
        return None, "conn:%s" % err
    if code != 200 or not h:
        return None, code
    vers, seen = [], set()
    pat = r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>.*?([A-Z][a-z]+ \d+, \d+ [\d:]+)"
    for m in re.finditer(pat % re.escape(name), h, re.S):
        for v in m.group(1).split("/"):
            if v not in seen:
                seen.add(v)
                vers.append((v, m.group(3).strip()))

    def vkey(v):
        return tuple(int(x) for x in re.findall(r"\d+", v))
    vers.sort(key=lambda vt: vkey(vt[0]))
    return (vers if vers else None), code


def mechanisms(name, version):
    h, code, err = curl_get("%s/gems/%s/%s" % (DIFFEND, name, version))
    if err is not None or code != 200 or not h:
        return [], "diff_fetch_%s" % (err or code)
    if name not in h:
        return [], "not_a_diff_page"
    text = html.unescape(re.sub(r"<[^>]+>", " ", h))
    found = []
    for label, rx in MECH_PATTERNS:
        m = rx.search(text)
        if m:
            if label == "go-import":
                gm = re.search(r'go-import"\s+content="([^\s"]+)\s+([a-z]+)\s', text, re.I)
                vcs = gm.group(2).lower() if gm else "unknown"
                found.append("go-import:vcs=%s" % vcs)
            else:
                found.append(label)
    return found, None


def diffend_wave(ts):
    if not ts:
        return None
    m = re.match(r"([A-Z][a-z]+) (\d+), (\d{4})", ts)
    if not m:
        return None
    month, day, year = m.groups()
    if (year, month, day) == ("2026", "July", "7"):
        return "july-7"
    return "%s-%s-%s" % (year.lower(), month.lower(), day)


def unverified_rows():
    """(todo_names list, carry dict name -> {jfrog_versions, xray_id})."""
    todo, carry = [], {}
    with open(MAIN) as f:
        for line in f:
            rec = json.loads(line)
            if isinstance(rec.get("http_status"), str):
                name = rec["name"]
                todo.append(name)
                carry[name] = {"jfrog_versions": rec.get("jfrog_versions") or [],
                               "xray_id": rec.get("xray_id")}
    return todo, carry


def done_resweep_names():
    done = set()
    if os.path.exists(RESWEEP):
        for line in open(RESWEEP):
            try:
                done.add(json.loads(line)["name"])
            except Exception:
                pass
    return done


def gem_versions_resilient(name):
    last = None
    for attempt in range(MAX_ATTEMPTS):
        vers, st = gem_versions(name)
        if vers:
            return vers, st
        if isinstance(st, int):
            return None, st  # real HTTP answer (200/no-versions or 404 etc.)
        last = st
        log("conn-close on %s (attempt %d/%d): %s" %
            (name, attempt + 1, MAX_ATTEMPTS, str(st)[:60]))
        if attempt < MAX_ATTEMPTS - 1:
            time.sleep(BACKOFFS[attempt])
    return "UNCONFIRMED", last


def main():
    todo_all, carry = unverified_rows()
    done = done_resweep_names()
    todo = [n for n in todo_all if n not in done]
    log("lane-j-resweep start: %d unverified total, %d done, %d todo "
        "(pace=%.1fs, attempts=%d)" % (len(todo_all), len(done), len(todo),
                                       PACE, MAX_ATTEMPTS))
    out = open(RESWEEP, "a")
    consec_close = 0
    found = absent = unconfirmed = 0
    for i, name in enumerate(todo):
        res = gem_versions_resilient(name)
        grams = name_grammars(name)
        jv = carry[name]["jfrog_versions"]
        xr = carry[name]["xray_id"]
        if res[0] == "UNCONFIRMED":
            consec_close += 1
            unconfirmed += 1
            # STAYS UNVERIFIED — never classify as absent without an HTTP answer
            rec = {"name": name, "in_diffend": None,
                   "http_status": "unverified",
                   "jfrog_versions": jv, "xray_id": xr,
                   "versions": [], "first_publish": None, "diffend_wave": None,
                   "mechanism_notes": [], "name_grammars": grams,
                   "retry_error": str(res[1])[:120], "resweep_pass": True,
                   "fetch_client": "curl"}
            log("%d/%d %s -> UNVERIFIED (%s)" %
                (i + 1, len(todo), name, str(res[1])[:50]))
        else:
            vers, st = res
            consec_close = 0
            if not vers:
                absent += 1
                rec = {"name": name, "in_diffend": False, "http_status": st,
                       "jfrog_versions": jv, "xray_id": xr,
                       "versions": [], "first_publish": None,
                       "diffend_wave": None,
                       "mechanism_notes": [], "name_grammars": grams,
                       "resweep_pass": True, "fetch_client": "curl"}
                log("%d/%d %s -> absent (%s)" % (i + 1, len(todo), name, st))
            else:
                found += 1
                mechs, err = mechanisms(name, vers[0][0])
                checked_version = vers[0][0]
                if err is None and (not mechs or mechs == ["empty-summary"]) \
                        and len(vers) > 1:
                    mechs2, err2 = mechanisms(name, vers[-1][0])
                    if err2 is None and mechs2:
                        mechs, err = mechs2, err2
                        checked_version = vers[-1][0]
                fp = vers[0][1]
                rec = {"name": name, "in_diffend": True, "http_status": 200,
                       "jfrog_versions": jv, "xray_id": xr,
                       "versions": [{"version": v, "ts": ts} for v, ts in vers],
                       "first_publish": fp, "diffend_wave": diffend_wave(fp),
                       "mechanism_version_checked": checked_version,
                       "mechanism_notes": mechs, "name_grammars": grams,
                       "resweep_pass": True, "fetch_client": "curl"}
                if err:
                    rec["diff_error"] = err
                log("%d/%d %s -> IN_DIFFEND (%d vers, wave=%s, mechs=%s)" %
                    (i + 1, len(todo), name, len(vers),
                     rec["diffend_wave"], mechs))
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if (i + 1) % COOLDOWN_EVERY == 0 and i + 1 < len(todo):
            log("cooldown %ds at %d/%d (found=%d absent=%d unconfirmed=%d)" %
                (COOLDOWN_SECS, i + 1, len(todo), found, absent, unconfirmed))
            time.sleep(COOLDOWN_SECS)
        if consec_close >= FAIL_COOLDOWN_AT:
            log("fail-cooldown %ds after %d consecutive conn failures" %
                (FAIL_COOLDOWN, consec_close))
            time.sleep(FAIL_COOLDOWN)
            consec_close = 0
    out.close()
    log("lane-j-resweep sweep complete: found=%d absent=%d unconfirmed=%d "
        "of %d attempted" % (found, absent, unconfirmed, len(todo)))
    merge(found, absent, unconfirmed)


def merge(found, absent, unconfirmed):
    """Rebuild MAIN: all previously-verified rows + resweep rows for the 167.
    Writes atomically; validates JSON and row count before replacing."""
    resweep_rows = {}
    with open(RESWEEP) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            resweep_rows[rec["name"]] = line
    kept, replaced, names = [], 0, set()
    with open(MAIN) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            names.add(rec["name"])
            if rec["name"] in resweep_rows:
                kept.append(resweep_rows[rec["name"]])
                replaced += 1
            else:
                kept.append(line)
    tmp = MAIN + ".new"
    with open(tmp, "w") as f:
        f.write("\n".join(kept) + "\n")
    # validate: same name set, valid JSON, row count
    n2, names2 = 0, set()
    with open(tmp) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            names2.add(json.loads(line)["name"])
            n2 += 1
    assert names == names2, "name set changed during merge"
    assert n2 == len(kept) == 264, "row count mismatch: %d" % n2
    os.replace(tmp, MAIN)
    log("merge: replaced %d/264 rows in raw/diffend_sweep_results_july7.jsonl; "
        "row count %d validated" % (replaced, n2))


if __name__ == "__main__":
    main()
