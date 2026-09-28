#!/usr/bin/env python3
"""LANE J — July-7 wave Diffend sweep.

Candidate set: the 263 names whose JFrog XRAY id is in the 1079xxx batch
(range JFrog's newly-identified July material clusters in). For each name:
  Phase 1: GET https://my.diffend.io/gems/<name> -> versions + publish timestamps.
  Phase 2: GET /gems/<name>/<version> (first version; latest too if the first
           yields nothing) -> mechanism markers.

Read-only. Gentle pacing (~1 req/3s). Diffend closes connections mid-fetch,
so every fetch retries with backoff. Checkpointed to the JSONL; restarts
resume via done_names(). Progress appended to progress.log for durability.

Record provenance note: CSV (research.jfrog.com/gemstuffer.csv, 2026-09-27)
carries no per-row dates; the Diffend pages are the independent source of
publish timestamps here. Wave is verified FROM the Diffend timestamp, not
assumed from the Xray id.
"""
import csv
import html
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import http.client

DIFFEND = "https://my.diffend.io"
UA = "rubygems-july7-research/1.0 (read-only inventory sweep; no install)"
PACE = 3.0
MAX_RETRIES = 2  # first pass: fail fast on hostile connections; --retry-failed later

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(PROJ, "data/july7-wave")
OUT = os.path.join(OUTDIR, "diffend_sweep_results_july7.jsonl")
LOG = os.path.join(OUTDIR, "progress.log")

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
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    line = "%s %s" % (ts, msg)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def get(url):
    """Fetch with retries/backoff; returns (text_or_None, status_or_error)."""
    last = None
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read().decode("utf-8", "ignore")
            time.sleep(PACE)
            return data, r.status
        except urllib.error.HTTPError as e:
            time.sleep(PACE)
            return None, e.code
        except Exception as e:
            last = str(type(e).__name__) + ": " + str(e)
            time.sleep(PACE * (2 ** attempt))
    time.sleep(PACE)
    return None, "fetch_failed:" + (last or "unknown")[:80]


def gem_versions(name):
    h, st = get("%s/gems/%s" % (DIFFEND, name))
    if h is None or st != 200:
        return None, st
    vers = []
    seen = set()
    pat = r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>.*?([A-Z][a-z]+ \d+, \d+ [\d:]+)"
    for m in re.finditer(pat % re.escape(name), h, re.S):
        vpath = m.group(1)
        for v in vpath.split("/"):
            if v not in seen:
                seen.add(v)
                vers.append((v, m.group(3).strip()))
    def vkey(v):
        return tuple(int(x) for x in re.findall(r"\d+", v))
    vers.sort(key=lambda vt: vkey(vt[0]))
    return vers, 200


def mechanisms(name, version):
    h, st = get("%s/gems/%s/%s" % (DIFFEND, name, version))
    if h is None or st != 200:
        return [], "diff_fetch_%s" % st
    # Diffend serves a generic stub when the version route has no diff
    if name not in h:
        return [], "not_a_diff_page"
    text = html.unescape(re.sub(r"<[^>]+>", " ", h))
    found = []
    vcs = None
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


def done_names():
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                done.add(json.loads(line)["name"])
            except Exception:
                pass
    return done


def diffend_wave(ts):
    """Classify wave strictly from the Diffend publish timestamp string."""
    if not ts:
        return None
    m = re.match(r"([A-Z][a-z]+) (\d+), (\d{4})", ts)
    if not m:
        return None
    month, day, year = m.groups()
    if (year, month, day) == ("2026", "July", "7"):
        return "july-7"
    return "%s-%s-%s" % (year.lower(), month.lower(), day)


# Named July-wave gems from the JFrog blog that fall outside the XRAY-1079xxx
# batch (verified July-wave examples must be swept regardless of batch id)
EXTRA_CANDIDATES = ["attacker-xss-admin-1"]


def load_candidates():
    cands = []
    csv_path = os.path.join(PROJ, "data/gemstuffer-jfrog-2026-09-27.csv")
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            name = row["Package"].strip()
            xray = row["Xray ID"].strip()
            if re.match(r"XRAY-1079\d{3}$", xray) or name in EXTRA_CANDIDATES:
                cands.append({"name": name,
                              "versions": [v for v in row["Versions"].split(";") if v],
                              "xray_id": xray})
    return cands


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    if "--retry-failed" in sys.argv:
        # drop connection-failure records so the resume pass re-attempts them:
        # phase-1 fetch failures AND phase-2 diff-fetch failures
        kept, dropped = [], 0
        if os.path.exists(OUT):
            for line in open(OUT):
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                st = str(rec.get("http_status", ""))
                derr = str(rec.get("diff_error", ""))
                if st.startswith("fetch_failed") or derr.startswith(
                        "diff_fetch_fetch_failed"):
                    dropped += 1
                else:
                    kept.append(line)
        with open(OUT, "w") as f:
            f.writelines(kept)
        log("retry-failed pass: dropped %d failed-fetch records, %d kept" %
            (dropped, len(kept)))
    cands = load_candidates()
    done = done_names()
    todo = [c for c in cands if c["name"] not in done]
    log("lane-j start: %d candidates, %d done, %d todo" % (len(cands), len(done), len(todo)))
    out = open(OUT, "a")
    for i, cand in enumerate(todo):
        name = cand["name"]
        vers, st = gem_versions(name)
        if not vers:
            rec = {"name": name, "in_diffend": False, "http_status": st,
                   "jfrog_versions": cand["versions"], "xray_id": cand["xray_id"],
                   "versions": [], "first_publish": None, "diffend_wave": None,
                   "mechanism_notes": [], "name_grammars": name_grammars(name)}
            out.write(json.dumps(rec) + "\n")
            out.flush()
            log("miss %d/%d %s (status=%s)" % (i + 1, len(todo), name, st))
            continue
        mechs, err = mechanisms(name, vers[0][0])
        checked_version = vers[0][0]
        # payload may live in a later version: re-check latest if first is bare
        if err is None and (not mechs or mechs == ["empty-summary"]) and len(vers) > 1:
            mechs2, err2 = mechanisms(name, vers[-1][0])
            if err2 is None and mechs2:
                mechs, err = mechs2, err2
                checked_version = vers[-1][0]
        fp = vers[0][1]
        rec = {"name": name, "in_diffend": True, "http_status": 200,
               "jfrog_versions": cand["versions"], "xray_id": cand["xray_id"],
               "versions": [{"version": v, "ts": ts} for v, ts in vers],
               "first_publish": fp, "diffend_wave": diffend_wave(fp),
               "mechanism_version_checked": checked_version,
               "mechanism_notes": mechs, "name_grammars": name_grammars(name)}
        if err:
            rec["diff_error"] = err
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if (i + 1) % 20 == 0 or i == len(todo) - 1:
            log("hit %d/%d %s (%d vers, wave=%s, mechs=%s)" %
                (i + 1, len(todo), name, len(vers), rec["diffend_wave"], mechs))
    out.close()
    log("lane-j sweep complete")


if __name__ == "__main__":
    main()
