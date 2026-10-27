#!/usr/bin/env python3
"""Provenance sidecars + SHA256SUMS for the cross-surface pivot raw dir.
Rule: raw captures keep full bytes. Notes carry path shape only.
Each capture file gets .PROVENANCE.txt (source pattern, method, time)
and .sha256. The dir gets SHA256SUMS over capture files only.
Idempotent: rewrites sidecars from file mtime, same content each run."""
import hashlib, os, time

BASE = os.path.dirname(os.path.abspath(__file__))
SOURCES = {
    "uq-": "urlquery public API search via skills/urlquery/bin/uq.py (authenticated API search; query term in file name).",
    "uq-detail-": "urlquery public API report detail via skills/urlquery/bin/uq.py.",
    "urlscan-": "urlscan.io public anonymous search API, metadata only (no login, no detail fetch).",
    "crtsh-": "crt.sh public certificate search, JSON output, expired excluded.",
    "gh-issues-": "GitHub search/issues API via gh api, read-only GET, 5 results per query.",
    "gh-issuespr-": "GitHub search/issues API via gh api, read-only GET, pull-request qualifier, 5 results.",
    "gh-code-": "GitHub search/code API via gh api, read-only GET, 5 results per query.",
    "pivot-summary": "Working summary derived from the capture files in this dir. Query strings stripped to host plus path.",
    "github-summary": "Working summary derived from the capture files in this dir.",
    "factum-summary": "Working summary derived from read-only Factum match queries. Values truncated to 160 chars.",
}
SKIP_SUFFIXES = (".PROVENANCE.txt", ".sha256", ".py")
SKIP_NAMES = {"SHA256SUMS", "PROGRESS.md"}

def source_for(name):
    for prefix, text in SOURCES.items():
        if name.startswith(prefix):
            return text
    return "Working file for this lane."

def main():
    files = sorted(f for f in os.listdir(BASE)
                   if os.path.isfile(os.path.join(BASE, f))
                   and not f.endswith(SKIP_SUFFIXES) and f not in SKIP_NAMES)
    lines = []
    for name in files:
        path = os.path.join(BASE, name)
        data = open(path, "rb").read()
        sha = hashlib.sha256(data).hexdigest()
        with open(path + ".sha256", "w") as fh:
            fh.write(sha + "  " + name + "\n")
        mtime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(os.path.getmtime(path)))
        with open(path + ".PROVENANCE.txt", "w") as fh:
            fh.write("Source: " + source_for(name) + "\n")
            fh.write("Retrieved: " + mtime + " (file time, UTC)\n")
            fh.write("Method: read-only API search; no login beyond existing gh auth; no POST.\n")
            fh.write("SHA256: " + sha + "\n")
        lines.append(sha + "  " + name + "\n")
    with open(os.path.join(BASE, "SHA256SUMS"), "w") as fh:
        fh.writelines(lines)
    print(f"sidecars written for {len(files)} files")

if __name__ == "__main__":
    main()
