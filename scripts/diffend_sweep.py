#!/usr/bin/env python3
"""HUNT LANE 20 — Diffend sweep for the 1,284 missing campaign gems.

Phase 1: GET https://my.diffend.io/gems/<name> per name -> in_diffend, versions, first publish ts.
Phase 2: for found gems, GET /gems/<name>/<first_version> and scan content for mechanism markers.

Read-only, ~1 req/s, no auth. Checkpointed so restarts resume.
"""
import html
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

DIFFEND = "https://my.diffend.io"
UA = "rubygems-goimport-research/1.0 (read-only inventory sweep; no install)"
PACE = 1.0

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = json.load(open(os.path.join(PROJ, "data/osv/ghsa_gemstuffer_classified.json")))["gs_not_in_corpus"]
OUT = os.path.join(PROJ, "data/osv/diffend_sweep_results.jsonl")

MECH_PATTERNS = [
    # (label, regex) — go-import VCS value extracted separately
    ("go-import", re.compile(r"go-import", re.I)),
    ("jina-laundered", re.compile(r"[rs]\.jina\.ai", re.I)),
    ("webhook-deaddrop", re.compile(r"web_hooks?|A000|ZZEND|southpxdatapp", re.I)),
    ("xss-exfil", re.compile(
        r"oast\.online|webhook\.site|<script|onerror=|alert\s*\(|"
        r"javascript:|expression\(|<style", re.I)),
    ("ssti-probe", re.compile(r"\$\{7\*7\}|\{\{\s*7\*7|\*\{|constructor", re.I)),
    ("county-json", re.compile(r"county\.json", re.I)),
    ("empty-summary", re.compile(r"summary:\s*x\b", re.I)),
]

# name-grammar families (pattern-based hunt, not exact phrase)
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
]


def name_grammars(name):
    return [label for label, rx in GRAMMAR_PATTERNS if rx.search(name)]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read().decode("utf-8", "ignore")
        time.sleep(PACE)
        return data, r.status
    except urllib.error.HTTPError as e:
        time.sleep(PACE)
        return None, e.code
    except Exception as e:
        time.sleep(2)
        return None, str(e)


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
    # Diffend serves a generic stub page when the version route has no diff
    # (title lacks the gem name) — treat as error, not as empty mechanism set
    if name not in h:
        return [], "not_a_diff_page"
    text = html.unescape(re.sub(r"<[^>]+>", " ", h))
    found = []
    for label, rx in MECH_PATTERNS:
        m = rx.search(text)
        if m:
            if label == "go-import":
                # extract the VCS value family: content="<importpath> <vcs> <url>"
                vcs = "unknown"
                gm = re.search(r'go-import"\s+content="([^\s"]+)\s+([a-z]+)\s', text, re.I)
                if gm:
                    vcs = gm.group(2).lower()
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


def main():
    done = done_names()
    todo = [n for n in NAMES if n not in done]
    print("total %d, done %d, todo %d" % (len(NAMES), len(done), len(todo)), flush=True)
    out = open(OUT, "a")
    for i, name in enumerate(todo):
        vers, st = gem_versions(name)
        if not vers:
            out.write(json.dumps({"name": name, "in_diffend": False,
                                  "http_status": st, "versions": [],
                                  "first_publish": None, "mechanism_notes": [],
                                  "name_grammars": name_grammars(name)}) + "\n")
            out.flush()
            if i % 50 == 0:
                print("%d/%d ... %s -> miss" % (i, len(todo), name), flush=True)
            continue
        mechs, err = mechanisms(name, vers[0][0])
        # if the earliest version is an empty carrier but later versions exist,
        # check the latest version too — payload may have been added later
        if err is None and mechs == ["empty-summary"] and len(vers) > 1:
            mechs2, err2 = mechanisms(name, vers[-1][0])
            if err2 is None and mechs2:
                mechs = mechs2
                err = None
        rec = {"name": name, "in_diffend": True, "http_status": 200,
               "versions": [{"version": v, "ts": ts} for v, ts in vers],
               "first_publish": vers[0][1], "mechanism_notes": mechs,
               "name_grammars": name_grammars(name)}
        if err:
            rec["diff_error"] = err
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if i % 25 == 0 or i == len(todo) - 1:
            print("%d/%d ... %s -> %d versions, mechs=%s" % (i, len(todo), name, len(vers), mechs), flush=True)
    out.close()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
