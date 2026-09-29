#!/usr/bin/env python3
"""Pattern sweep for LANE D (March-7 RCE modality).

Two sources:
  A. Diffend-rendered diffs (raw/<gem>.<version>.diff.html) — static text
     analysis only, nothing executed. Strip diff2html markup, match
     mechanism/egress/temporal patterns per +/- line.
  B. Investigator-reported markers from colonist-one's post
     (data/2026-09-04-thecolony-ai/raw/posts/dfac3a74-4685-43d8-9bd6-c76409f87ade.json) —
     recorded with provenance "colonist-one (reported)", not our own
     observation, since the gems are absent from Diffend.

Writes data/2026-03-07-march7-rce-modality/raw/sweep.json.
"""
import html
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(BASE, "data", "2026-03-07-march7-rce-modality")
RAW = os.path.join(DIR, "raw")

PATTERNS = {
    "rce-sink": {
        "system-call": r"\bsystem\s*\(",
        "exec-call": r"\bexec\s*\(",
        "io-popen": r"\bIO\.popen\b",
        "open3": r"\bOpen3\b",
        "spawn": r"\bKernel\.(?:spawn|system|exec)\b",
        "eval": r"\beval\s*\(",
        "backticks": r"`[^`\n]+`",
    },
    "doc-builder": {
        "yard": r"\byard\b",
        "rdoc": r"\brdoc\b",
        "yard-handler": r"YARD::Handlers",
        "kramdown": r"\bkramdown\b",
        "rouge": r"\brouge\b",
    },
    "egress-host": {
        "net-http": r"\bNet::HTTP\b",
        "tcpsocket": r"\bTCPSocket\b",
        "curl": r"\bcurl\b",
        "wget": r"\bwget\b",
        "uri-open": r"\bURI\.open\b",
        "httparty": r"\bHTTParty\b",
    },
    "egress-url": {
        "http-url": r"https?://[^\s\"'<>]+",
    },
    "temporal": {
        "date-literal-2026": r"2026-\d{2}-\d{2}",
    },
}

# Investigator-reported (colonist-one, 2026-09-05) — mechanism markers for
# the payload gem, since we have no diffs of our own (absent from Diffend).
# Hosts that belong to Diffend's own page chrome (excluded from egress sweep
# so their URLs are never misread as gem egress targets).
CHROME_HOSTS = ("diffend.io", "analysis.windows.net", "googleapis.com",
                "gstatic.com", "gravatar.com", "fonts.googleapis.com")

# Investigator-reported (colonist-one, 2026-09-05) — mechanism markers for
# the payload gem, since we have no diffs of our own (absent from Diffend).
INVESTIGATOR_MARKERS = [
    {"version": "reported", "family": "doc-builder", "pattern": "doc-builder-rce",
     "prefix": "+", "match": "documentation-build config directs the registry's doc builder to load and run a Ruby file at build time",
     "line": "colonist-one: inspected the live .gem, executed nothing", "line_no": 0,
     "provenance": "colonist-one post dfac3a74 (reported)"},
    {"version": "reported", "family": "rce-sink", "pattern": "execution-proof",
     "prefix": "+", "match": "writes an execution proof (timestamp + working directory)",
     "line": "colonist-one: that file writes an execution proof (timestamp + working directory)", "line_no": 0,
     "provenance": "colonist-one post dfac3a74 (reported)"},
    {"version": "reported", "family": "egress-host", "pattern": "egress-http",
     "prefix": "+", "match": "makes an outbound HTTP call (an egress test)",
     "line": "colonist-one: makes an outbound HTTP call (an egress test); target withheld by investigator", "line_no": 0,
     "provenance": "colonist-one post dfac3a74 (reported)"},
    {"version": "reported", "family": "doc-builder", "pattern": "html-script-test",
     "prefix": "+", "match": "ships an HTML asset that tests script execution in the rendered docs",
     "line": "colonist-one: the gem also ships an HTML asset that tests script execution in the rendered docs", "line_no": 0,
     "provenance": "colonist-one post dfac3a74 (reported)"},
]


def strip_diff_text(page_html):
    lines = []
    for m in re.finditer(
            r'<span class="d2h-code-line-prefix">([\+\- ])</span>\s*'
            r'<span class="d2h-code-line-ctn">(.*?)</span>', page_html, re.S):
        prefix = m.group(1)
        content = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        lines.append((prefix, content))
    return lines


def main():
    results = json.load(open(DIR + "/results.json"))
    out = {"hits": {}, "mechanism_markers": {}, "egress_targets": {},
           "note": ("diffend-hits: our own observation from Diffend-rendered "
                    "diffs; investigator-hits: colonist-one's reported claims, "
                    "not independently re-verified (gems absent from Diffend)")}

    for name, pkg in results["gems"].items():
        out["hits"][name] = []
        markers = set()
        egress = set()
        for v in pkg["diffend"].get("versions", []):
            path = os.path.join(RAW, f"{name}.{v}.diff.html")
            if not os.path.exists(path):
                continue
            page = open(path, encoding="utf-8", errors="replace").read()
            for fam, pats in PATTERNS.items():
                for pname, rx in pats.items():
                    cre = re.compile(rx)
                    for i, (prefix, content) in enumerate(strip_diff_text(page)):
                        m = cre.search(content)
                        if not m:
                            continue
                        match = m.group(0)[:160]
                        if fam == "egress-url":
                            # host-level only — never full paths/queries
                            hm = re.match(r"https?://([^/\s\"'<>]+)", m.group(0))
                            match = (hm.group(1) if hm else match)[:120]
                        hit = {"version": v, "family": fam, "pattern": pname,
                               "prefix": prefix,
                               "match": match,
                               "line": content.strip()[:300], "line_no": i,
                               "provenance": "diffend-diff (observed)"}
                        out["hits"][name].append(hit)
                        if fam in ("doc-builder", "rce-sink"):
                            markers.add(f"{pname}:{match[:60]}")
                        if fam in ("egress-host", "egress-url"):
                            if not any(h in match for h in CHROME_HOSTS):
                                egress.add(match[:120])
        # investigator-reported markers attach to the payload gem
        if name == "sampledocpayload624286":
            for h in INVESTIGATOR_MARKERS:
                out["hits"][name].append(dict(h))
            markers.add("reported:doc-builder-rce (colonist-one)")
            markers.add("reported:execution-proof (colonist-one)")
            egress.add("reported:HTTP egress call (target withheld by colonist-one)")
        out["mechanism_markers"][name] = sorted(markers)
        out["egress_targets"][name] = sorted(egress)

    with open(DIR + "/sweep.json", "w") as f:
        json.dump(out, f, indent=1)
    n = sum(len(v) for v in out["hits"].values())
    print(f"sweep hits: {n}")
    for name in results["gems"]:
        print(f"{name}: markers={len(out['mechanism_markers'][name])} "
              f"egress={len(out['egress_targets'][name])}")


if __name__ == "__main__":
    main()
