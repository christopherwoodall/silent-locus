#!/usr/bin/env bash
# LIFEVAL cross-corpus sweep — urlquery.net htmx search, curl-based, paced.
# Worker: urlquery-live. Doctrine: >=5s between requests.
set -u
RAW="$HOME/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/lifeval-cross-corpus/raw"
UA="silent-locus/lifeval-sweep"
NOW_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Each entry: slug|query-string (already URL-encoded)
queries=(
  "q01_full_marker_init|Lifeval%20temporary%20technical%20sandbox%20initialization"
  "q02_full_marker_api|Lifeval%20API%20temp-account%20test"
  "q03_lifeval_standalone|Lifeval"
  "q04_init_phrase|Temporary%20technical%20sandbox%20initialization"
  "q05_sandbox_test_link|sandbox%20test%20link"
  "q06_testing_external_link|testing%20external%20link"
  "q07_sandbox_link_test|Sandbox%20link%20test"
  "q08_temp_tech_sandbox|Temporary%20technical%20sandbox"
  "q09_lifeval_domain_incubator|Lifeval%20url.domain%3Aincubator.wikimedia.org"
  "q10_lifeval_domain_commons|Lifeval%20url.domain%3Acommons.wikimedia.org"
  "q11_lifeval_domain_meta|Lifeval%20url.domain%3Ameta.wikimedia.org"
)

BASE="https://urlquery.net/api/htmx/search/?type=reports&view=list&limit=24&offset=0&q="

for entry in "${queries[@]}"; do
  slug="${entry%%|*}"
  enc="${entry#*|}"
  out="$RAW/htmx_${slug}.html"
  meta="$RAW/htmx_${slug}.meta.json"
  echo ">>> $slug @ $NOW_UTC"
  code="$(curl -s -o "$out" -w '%{http_code}' --max-time 60 \
    -A "$UA" \
    -H 'HX-Request: true' -H 'HX-Trigger: search_query' -H 'HX-Target: search_results' \
    -H 'HX-Current-URL: https://urlquery.net/search' -H 'Referer: https://urlquery.net/search' \
    "${BASE}${enc}")"
  bytes="$(stat -c%s "$out" 2>/dev/null || echo 0)"
  sha="$(sha256sum "$out" | cut -d' ' -f1)"
  uuids="$(grep -o -E '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' "$out" 2>/dev/null | sort -u | wc -l)"
  printf '{"slug":"%s","query_raw":"%s","endpoint":"%s","http_status":%s,"bytes":%s,"sha256":"%s","retrieved_utc":"%s","method":"curl (direct)","report_uuids_distinct":%s}\n' \
    "$slug" "$(printf '%s' "$enc" | sed 's/%/\\u0025/g')" "${BASE}..." "$code" "$bytes" "$sha" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$uuids" > "$meta"
  echo "    http=$code bytes=$bytes sha=$sha uuids=$uuids"
  sleep 6
done
echo "DONE"
