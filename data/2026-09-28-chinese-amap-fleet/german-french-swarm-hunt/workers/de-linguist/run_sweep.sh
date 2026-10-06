#!/bin/bash
# de-linguist OPEN-query sweep, 2026-10-05
# Polite pacing: 65s between queries, max ~8 per session.
# A 429 is marked OPEN, never zero.
OUT=~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/de-linguist/raw
mkdir -p "$OUT"
LOG="$OUT/sweep_$(date -u +%Y%m%dT%H%M%SZ).log"
exec > >(tee -a "$LOG") 2>&1
run() {
  local slug="$1" q="$2" lim="$3"
  echo "=== $(date -u +%FT%TZ) QUERY: $q ==="
  ~/workspace/skills/urlquery/bin/uq_htmx.py search --query "$q" --limit "$lim" > "$OUT/$slug.json" 2>"$OUT/$slug.err"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "QUERY FAILED rc=$rc (see $slug.err)"
    head -c 500 "$OUT/$slug.err"
    echo
  else
    python3 - "$OUT/$slug.json" <<'EOF'
import json,sys
d=json.load(open(sys.argv[1]))
rs=d.get("reports",[])
print(f"hits={len(rs)}")
for r in rs[:6]:
    print(" ", r.get("date"), r.get("report_id"), r.get("url","")[:110])
EOF
  fi
  echo "=== done $(date -u +%FT%TZ) ==="
}
P=65
run q1_httpbun_aufgabe    "httpbun aufgabe" 24; sleep $P
run q2_httpbun_agent      "httpbun agent" 24; sleep $P
run q3_claude_httpbun     "claude httpbun" 24; sleep $P
run q4_uqscan_berlin      "uqscan berlin" 24; sleep $P
run q5_subpoinavi_berlin  "sub_poi_navi berlin" 24; sleep $P
run q6_linkvertise_ts     "url.domain:linkvertise.com" 60; sleep $P
run q7_deepl_ts           "url.domain:deepl.com" 24; sleep $P
run q8_httpbun_ergebnis   "httpbun ergebnis" 24
echo "SWEEP COMPLETE $(date -u +%FT%TZ)"
