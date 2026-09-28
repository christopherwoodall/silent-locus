#!/usr/bin/env python3
"""Pattern sweep over Diffend-rendered diffs for the March-7 RCE modality.

Reads data/march7-rce-modality/raw/<name>.<version>.diff.html, strips
diff2html markup to plain +/- lines, and matches mechanism/egress/date
patterns. Writes data/march7-rce-modality/sweep.json.

Read-only static text analysis; nothing is executed.
"""
import html
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(BASE, "data", "march7-rce-modality")
RAW = os.path.join(DIR, "raw")

PATTERNS = {
    # family -> {pattern_name: regex}
    "rce-sink": {
        "system-call": r"`system\s*\(",
        "exec-call": r"\bexec\s*\(",
        "backtick": r"`[^`\n]+`",
        "io-popen": r"\bIO\.popen\b",
        "open3": r"\bOpen3\b",
        "spawn": r"\bKernel\.(?:spawn|system|exec)\b",
        "eval": r"\beval\s*\(",
    },
    "doc-builder": {
        "yard": r"\byard\b",
        "rdoc": r"\brdoc\b",
        "kramdown": r"\bkramdown\b",
        "rouge": r"\brouge\b",
        "yard-handler": r"YARD::Handlers",
    },
    "egress-host": {
        "net-http": r"\bNet::HTTP\b",
        "tcpsocket": r"\bTCPSocket\b",
        "socket": r"\bSocket\b",
        "curl": r"\bcurl\b",
        "wget": r"\bwget\b",
        "httparty": r"\bHTTParty\b",
        "uri-open": r"\bURI\.open\b",
    },
    "egress-url": {
        "http-url": r"https?://[^\s\"'<>]+",
    },
    "toolkit": {
        "jina": r"r\.jina\.ai",
        "httpbun": r"httpbun",
        "countapi": r"countapi",
        "jqp": r"jqp\.vercel",
        "serveo": r"serveo",
        "pinggy": r"pinggy",
        "zz-marker": r"\bzz\b",
        "epoch-nonce": r"\b17\d{8}\b",
    },
    "temporal": {
        "march-2026": r"2026-0?3",
        "date-literal": r"2026-\d{2}-\d{2}",
    },
}


def strip_diff_text(page_html):
    lines = []
    for m in re.finditer(
            r'<span class="d2h-code-line-prefix">([\+\- ])</span>'
            r'<span class="d2h-code-line-ctn">(.*?)</span>', page_html, re.S):
        prefix = m.group(1)
        content = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        lines.append((prefix, content))
    return lines


def file_of_line(lines, idx):
    """Best-effort: walk back to nearest d2h-file-name is heavy; use
    the diff header context instead (kept simple)."""
    return ""


def main():
    results = json.load(open(DIR + "/results.json"))
    out = {"hits": {}, "mechanism_markers": {}, "egress_targets": {}}
    file_ctx = {}
    for name, pkg in results.items():
        out["hits"][name] = []
        markers = set()
        egress = set()
        for v in pkg.get("versions", []):
            path = os.path.join(RAW, f"{name}.{v}.diff.html")
            if not os.path.exists(path):
                continue
            page = open(path, encoding="utf-8", errors="replace").read()
            lines = strip_diff_text(page)
            for fam, pats in PATTERNS.items():
                for pname, rx in pats.items():
                    cre = re.compile(rx)
                    for i, (prefix, content) in enumerate(lines):
                        m = cre.search(content)
                        if not m:
                            continue
                        hit = {
                            "version": v,
                            "family": fam,
                            "pattern": pname,
                            "prefix": prefix,
                            "match": m.group(0)[:160],
                            "line": content.strip()[:300],
                            "line_no": i,
                        }
                        out["hits"][name].append(hit)
                        if fam in ("doc-builder", "rce-sink"):
                            markers.add(f"{pname}:{m.group(0)[:60]}")
                        if fam in ("egress-host", "egress-url"):
                            egress.add(m.group(0)[:120])
            # version-scoped
            out["mechanism_markers"].setdefault(f"{name}:{v}", []).append("")
        out["mechanism_markers"][name] = sorted(markers)
        out["egress_targets"][name] = sorted(egress)
    with open(DIR + "/sweep.json", "w") as f:
        json.dump(out, f, indent=1)
    n_hits = sum(len(v) for v in out["hits"].values())
    print(f"sweep hits: {n_hits}")
    for name in results:
        print(name, "markers:", len(out["mechanism_markers"][name]),
              "egress:", len(out["egress_targets"][name]))
        for e in out["egress_targets"][name][:10]:
            print("   egress:", e)


if __name__ == "__main__":
    main()
