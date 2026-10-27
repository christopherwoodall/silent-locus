#!/bin/bash
# Recovery for called_home__comment (filtered set): Algolia caps offset
# pagination at 1000 hits per query ("you can only fetch the 1000 hits
# for this query"), so the single-query capture held only 1000/1384.
# Fix: split the date range in two disjoint halves, each fully paged.
# Half A: 2025-11-01 <= created_at_i < 2026-05-01 (680 hits, 2 pages)
# Half B: created_at_i >= 2026-05-01 (704 hits, 2 pages)
# 680 + 704 = 1384 = the single-query nbHits. This script REPLACES the
# earlier incomplete called_home__comment.json (1000 hits) with the full
# 1384-hit capture. The supersession is recorded in COVERAGE.md.
set -u
OUT="$(cd "$(dirname "$0")" && pwd)"
TMP="$OUT/.tmp-recover"
mkdir -p "$TMP"
HPP=500
BASE="https://hn.algolia.com/api/v1/search?query=called%20home&tags=comment&hitsPerPage=${HPP}"

fetch_page() { # $1=url $2=outfile
  local code
  code=$(curl -sS -o "$2" -w "%{http_code}" "$1") || { echo "CURL FAIL $1"; exit 1; }
  [ "$code" = "200" ] || { echo "HTTP $code $1"; exit 1; }
  sleep 1.2
}

fetch_page "${BASE}&numericFilters=created_at_i%3E%3D1761955200%2Ccreated_at_i%3C1777593600&page=0" "$TMP/A0.json"
fetch_page "${BASE}&numericFilters=created_at_i%3E%3D1761955200%2Ccreated_at_i%3C1777593600&page=1" "$TMP/A1.json"
fetch_page "${BASE}&numericFilters=created_at_i%3E%3D1777593600&page=0" "$TMP/B0.json"
fetch_page "${BASE}&numericFilters=created_at_i%3E%3D1777593600&page=1" "$TMP/B1.json"

python3 - "$TMP" "$OUT/called_home__comment.json" <<'EOF'
import json, sys
tmp, out = sys.argv[1], sys.argv[2]
pages = [json.load(open(f"{tmp}/{n}.json")) for n in ("A0", "A1", "B0", "B1")]
ids = [h["objectID"] for p in pages for h in p["hits"]]
assert len(ids) == 1384, f"expected 1384 hits, got {len(ids)}"
assert len(set(ids)) == 1384, "duplicate objectIDs across halves"
for p in pages:
    assert p["nbHits"] in (680, 704), p["nbHits"]
print("OK: 4 pages, 1384 unique hits")
with open(out, "w") as fh:
    fh.write("[")
    for i, n in enumerate(("A0", "A1", "B0", "B1")):
        if i: fh.write(",")
        fh.write(open(f"{tmp}/{n}.json").read())
    fh.write("]")
EOF

retrieved=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > "$OUT/called_home__comment.json.PROVENANCE.txt" <<EOF
Source: HN Algolia public API, https://hn.algolia.com/api/v1/search
Query term: called home
Tag: comment
Date filter: created_at_i >= 1761955200 (2025-11-01 00:00:00 UTC)
Method note: Algolia caps offset pagination at 1000 hits per query, so the
single-query capture held only 1000 of 1384 hits. This file replaces it with
a date-split capture of the same set, in two disjoint halves:
  Half A: created_at_i >= 1761955200 AND created_at_i < 1777593600
          (2025-11-01 .. 2026-05-01), nbHits 680, pages 0-1
  Half B: created_at_i >= 1777593600 (2026-05-01 .. retrieval),
          nbHits 704, pages 0-1
  Half totals: 680 + 704 = 1384 = single-query nbHits. All 1384 objectIDs unique.
Pages in file: 4 (A0, A1, B0, B1), hitsPerPage=500, raw page bytes preserved.
Retrieval time (UTC): ${retrieved}
Method: curl, no key, no login, no account. Polite pace: >=1.2s between calls.
Collector: HN Collector C, agent-egress-hunt lane.
Supersedes: the earlier single-query called_home__comment.json (1000/1384 hits),
replaced because it was incomplete; the full set is this file.
EOF
(cd "$OUT" && sha256sum "called_home__comment.json" > "called_home__comment.json.sha256")
rm -rf "$TMP"
echo "RECOVERY DONE"
