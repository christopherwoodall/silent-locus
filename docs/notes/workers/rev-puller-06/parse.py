#!/usr/bin/env python3
"""Parse one MediaWiki revisions API response.

Reads the raw JSON at argv[1], emits one JSON line per revision to stdout.
Writes markers to stderr:
  REVCOUNT <n>         number of revision lines emitted for this page
  RVCONTINUE <token>   continuation token (empty if exhausted)
  MISSING <title>      page missing/invalid
  APIERROR <code>:...  API-level error (caller retries on maxlag)
  PARSEERROR ...       unparseable response
URL encoding / HTTP are done by the curl driver; this script is JSON-only.
"""
import json
import sys


def main():
    path, rank, title = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"PARSEERROR {e}", file=sys.stderr)
        sys.exit(10)

    err = d.get("error")
    if err:
        print(f"APIERROR {err.get('code')}:{err.get('info', '')}", file=sys.stderr)
        sys.exit(11)

    pages = d.get("query", {}).get("pages", [])
    n = 0
    try:
        for p in pages:
            if p.get("missing") or p.get("invalid"):
                print(f"MISSING {p.get('title', title)}", file=sys.stderr)
                continue
            for r in p.get("revisions", []):
                rec = {
                    "rank": int(rank),
                    "article": title,
                    "revid": r.get("revid"),
                    "parentid": r.get("parentid"),
                    "user": r.get("user"),
                    "timestamp": r.get("timestamp"),
                    "comment": r.get("comment"),
                    "tags": r.get("tags") or [],
                    "size": r.get("size"),
                }
                print(json.dumps(rec, ensure_ascii=False))
                n += 1
    except BrokenPipeError:
        pass  # downstream closed the pipe (e.g. head); counted lines stand
    print(f"REVCOUNT {n}", file=sys.stderr)
    cont = d.get("continue", {}).get("rvcontinue", "")
    print(f"RVCONTINUE {cont}", file=sys.stderr)


main()
