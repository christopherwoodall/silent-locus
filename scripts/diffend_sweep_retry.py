#!/usr/bin/env python3
"""HUNT LANE 20 — Diffend RETRY pass for the 672 phase-1 fetch failures.

Lane 20 (scripts/diffend_sweep.py) left 672 names UNCONFIRMED: Diffend closed
the connection before serving the gem page ("Remote end closed connection
without response"). Those rows sit in data/osv/diffend_sweep_results.jsonl
with a STRING http_status (vs int for resolved rows).

KEY FIX vs the original: Python urllib's TLS handshake is now being dropped
by Diffend's edge (100% RemoteDisconnected on fresh requests), while curl
succeeds on the same URLs. This script fetches via curl subprocess.

Retries ONLY the 672 names, ~1 req/3s, with backoff on connection-close.
Checkpointed: reruns skip names already in the retry file.

Per name, determine: in Diffend (versions page parsed + publish timestamps,
plus phase-2 mechanism scan like the original) or confirmed absent.

Read-only, no auth.
"""
import html
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diffend_sweep as lane20

PROJ = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
ORIG = os.path.join(PROJ, "data/osv/diffend_sweep_results.jsonl")
RETRY_OUT = os.path.join(PROJ, "data/osv/diffend_sweep_results_retry.jsonl")
LOG = os.path.join(PROJ, "data/osv/diffend_retry.log")

DIFFEND = "https://my.diffend.io"
UA = "rubygems-goimport-research/1.0 (read-only inventory sweep; no install)"
PACE = 3.0

MAX_ATTEMPTS = 3
BACKOFFS = [15, 120]
COOLDOWN_EVERY = 5
COOLDOWN_SECS = 180


def log(msg):
    line = "%s %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def curl_get(url):
    """(body_text|None, http_code|int, err_str|None). Follows redirects."""
    try:
        p = subprocess.run(
            ["curl", "-sSL", "-A", UA, "--max-time", "60",
             "-o", "-", "-w", "\n%{http_code}", url],
            capture_output=True, timeout=75)
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
        return None, "conn:%s" % err          # connection-level failure
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
    for label, rx in lane20.MECH_PATTERNS:
        m = rx.search(text)
        if m:
            if label == "go-import":
                vcs = "unknown"
                gm = re.search(r'go-import"\s+content="([^\s"]+)\s+([a-z]+)\s', text, re.I)
                if gm:
                    vcs = gm.group(2).lower()
                found.append("go-import:vcs=%s" % vcs)
            else:
                found.append(label)
    return found, None


def failure_names():
    fails = []
    for line in open(ORIG):
        r = json.loads(line)
        if isinstance(r.get("http_status"), str):
            fails.append(r["name"])
    return fails


def done_retry_names():
    done = set()
    if os.path.exists(RETRY_OUT):
        for line in open(RETRY_OUT):
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
            return None, st                    # real HTTP answer
        last = st
        log("conn-close on %s (attempt %d/%d): %s" %
            (name, attempt + 1, MAX_ATTEMPTS, str(st)[:60]))
        if attempt < MAX_ATTEMPTS - 1:
            time.sleep(BACKOFFS[attempt])
    return "UNCONFIRMED", last


def main():
    todo_all = failure_names()
    done = done_retry_names()
    todo = [n for n in todo_all if n not in done]
    log("retry pass: %d failures total, %d done, %d todo" %
        (len(todo_all), len(done), len(todo)))

    out = open(RETRY_OUT, "a")
    consec_close = 0
    found = absent = unconfirmed = 0
    for i, name in enumerate(todo):
        res = gem_versions_resilient(name)
        if res[0] == "UNCONFIRMED":
            consec_close += 1
            unconfirmed += 1
            rec = {"name": name, "in_diffend": None, "http_status": "unconfirmed",
                   "versions": [], "first_publish": None, "mechanism_notes": [],
                   "name_grammars": lane20.name_grammars(name),
                   "retry_error": str(res[1])[:120], "retry_pass": True,
                   "fetch_client": "curl"}
            log("%d/%d %s -> UNCONFIRMED (%s)" % (i + 1, len(todo), name, str(res[1])[:50]))
        else:
            vers, st = res
            consec_close = 0
            if not vers:
                absent += 1
                rec = {"name": name, "in_diffend": False, "http_status": st,
                       "versions": [], "first_publish": None, "mechanism_notes": [],
                       "name_grammars": lane20.name_grammars(name), "retry_pass": True,
                       "fetch_client": "curl"}
            else:
                found += 1
                mechs, err = mechanisms(name, vers[0][0])
                if err is None and mechs == ["empty-summary"] and len(vers) > 1:
                    mechs2, err2 = mechanisms(name, vers[-1][0])
                    if err2 is None and mechs2:
                        mechs = mechs2
                        err = None
                rec = {"name": name, "in_diffend": True, "http_status": 200,
                       "versions": [{"version": v, "ts": ts} for v, ts in vers],
                       "first_publish": vers[0][1], "mechanism_notes": mechs,
                       "name_grammars": lane20.name_grammars(name), "retry_pass": True,
                       "fetch_client": "curl"}
                if err:
                    rec["diff_error"] = err
            log("%d/%d %s -> in_diffend=%s mechs=%s" %
                (i + 1, len(todo), name, rec["in_diffend"], rec.get("mechanism_notes")))
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if consec_close >= COOLDOWN_EVERY:
            log("cooldown: %d consecutive conn-closes, sleeping %ds" %
                (consec_close, COOLDOWN_SECS))
            time.sleep(COOLDOWN_SECS)
            consec_close = 0
    out.close()
    log("RETRY DONE: found=%d absent=%d unconfirmed=%d" % (found, absent, unconfirmed))


if __name__ == "__main__":
    main()
