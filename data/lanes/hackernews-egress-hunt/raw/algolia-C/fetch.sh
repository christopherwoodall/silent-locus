#!/bin/bash
# HN Collector C — Algolia capture script (collect only, no triage).
# Usage: bash fetch.sh
# Writes one JSON file per term per tag: a JSON array of raw page-response
# objects, byte-preserved per page (concatenated, not re-serialized).
# Each capture gets a .PROVENANCE.txt and a .sha256 beside it.
set -u
OUT="$(cd "$(dirname "$0")" && pwd)"
TMP="$OUT/.tmp-pages"
mkdir -p "$TMP"
ERRLOG="$OUT/fetch-errors.log"
: > "$ERRLOG"
EPOCH_FROM=1761955200   # 2025-11-01 00:00:00 UTC
HPP=500
CAP=2000

urlenc() { python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"; }

# fetch_set <term> <tag> <filter> <suffix>
# filter: "ge" (created_at_i>=EPOCH_FROM, new-hit set) or "lt" (pre-Nov context)
fetch_set() {
  local term="$1" tag="$2" filt="$3" suffix="$4"
  local slug
  slug=$(echo "$term" | tr ' ' '_' | tr -cd 'A-Za-z0-9_')
  local enc
  enc=$(urlenc "$term")
  local nf
  if [ "$filt" = "ge" ]; then nf="created_at_i%3E%3D${EPOCH_FROM}"; else nf="created_at_i%3C${EPOCH_FROM}"; fi
  local base="https://hn.algolia.com/api/v1/search?query=${enc}&tags=${tag}&numericFilters=${nf}&hitsPerPage=${HPP}"
  local stem="${slug}__${tag}${suffix}"
  local retrieved
  retrieved=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  # Page 0 first, to learn nbPages/nbHits.
  local code
  code=$(curl -sS -o "$TMP/${stem}__p0.json" -w "%{http_code}" "${base}&page=0") || {
    echo "ERROR ${stem} curl failed page 0" >> "$ERRLOG"; return 1; }
  if [ "$code" != "200" ]; then
    echo "ERROR ${stem} HTTP ${code} page 0" >> "$ERRLOG"; return 1; fi
  local nbhits nbpages
  nbhits=$(python3 -c "import json;print(json.load(open('$TMP/${stem}__p0.json')).get('nbHits'))")
  nbpages=$(python3 -c "import json;print(json.load(open('$TMP/${stem}__p0.json')).get('nbPages'))")
  echo "${stem}: nbHits=${nbhits} nbPages=${nbpages}"
  if [ "$nbhits" -gt "$CAP" ]; then
    echo "CAPPED ${stem} nbHits=${nbhits} exceeds cap ${CAP}; pages NOT fetched beyond probe" >> "$ERRLOG"
    rm -f "$TMP/${stem}__p0.json"
    echo "${stem} CAPPED at ${nbhits} (cap ${CAP}); no capture file written" >> "$OUT/cap-notes.txt"
    return 0
  fi
  local p
  for p in $(seq 1 $((nbpages - 1))); do
    sleep 1.2
    code=$(curl -sS -o "$TMP/${stem}__p${p}.json" -w "%{http_code}" "${base}&page=${p}") || {
      echo "ERROR ${stem} curl failed page ${p}" >> "$ERRLOG"; return 1; }
    if [ "$code" != "200" ]; then
      echo "ERROR ${stem} HTTP ${code} page ${p}" >> "$ERRLOG"; return 1; fi
  done
  # Assemble: JSON array of raw page objects, bytes preserved per page.
  {
    printf '['
    local first=1
    for p in $(seq 0 $((nbpages - 1))); do
      if [ "$first" = 1 ]; then first=0; else printf ','; fi
      cat "$TMP/${stem}__p${p}.json"
    done
    printf ']'
  } > "$OUT/${stem}.json"
  rm -f "$TMP/${stem}__p"*.json
  # Provenance triple.
  cat > "$OUT/${stem}.json.PROVENANCE.txt" <<EOF
Source: HN Algolia public API, https://hn.algolia.com/api/v1/search
Query term: ${term}
Tag: ${tag}
Date filter: ${filt} (created_at_i ${filt} ${EPOCH_FROM}; 2025-11-01 00:00:00 UTC boundary)
Base query URL: ${base}
Pages fetched: ${nbpages} (page=0..$((nbpages - 1))), hitsPerPage=${HPP}
nbHits reported by API: ${nbhits}
Retrieval time (UTC): ${retrieved}
Method: curl, no key, no login, no account. Polite pace: >=1.2s between calls.
Collector: HN Collector C, agent-egress-hunt lane. Raw API bytes preserved per page.
EOF
  (cd "$OUT" && sha256sum "${stem}.json" > "${stem}.json.sha256")
  sleep 1.2
}

TERMS=("model fetched" "hallucinated URL" "signed URL" "called home" "agent exfiltration" "model exfiltrated")

# New-hit set: 2025-11-01 onward, fully paged.
for term in "${TERMS[@]}"; do
  for tag in story comment; do
    fetch_set "$term" "$tag" "ge" ""
  done
done

# Pre-Nov-2025 context set: fully paged where under cap; capped queries recorded only.
for term in "${TERMS[@]}"; do
  for tag in story comment; do
    fetch_set "$term" "$tag" "lt" "__pre20251101"
  done
done

rmdir "$TMP" 2>/dev/null || true
echo "DONE. See fetch-errors.log and cap-notes.txt (if present)."
