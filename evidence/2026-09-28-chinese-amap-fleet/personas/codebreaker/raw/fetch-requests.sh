#!/bin/bash
# Fetch request lists for alive tokens. Rate: <=1 req / 5s.
set -u
OUT="${1:-/tmp/deaddrop-reqs.jsonl}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
tokens=(
  "fleet:6ddc559e-5c08-4915-a5b2-f4addc42368a"
  "fleet:0a947514-5b43-4030-9f9f-b193dd2d519b"
  "fleet:a7753b69-2ceb-4221-adfa-80f69d57480c"
  "legacy:cbcb10de-7f66-4e82-b7ac-5b34ccb04164"
)
> "$OUT"
for entry in "${tokens[@]}"; do
  fam="${entry%%:*}"; uuid="${entry#*:}"
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  body="$(curl -s -m 60 -A "$UA" -w '\n%{http_code}' "https://webhook.site/token/$uuid/requests?per_page=100&sorting=newest" 2>/dev/null)"
  http="$(echo "$body" | tail -n1)"
  payload="$(echo "$body" | sed '$d' | tr -d '\n')"
  echo "{\"probe_ts\":\"$ts\",\"family\":\"$fam\",\"uuid\":\"$uuid\",\"http\":$http,\"response\":$payload}" >> "$OUT"
  echo "REQ $fam ${uuid:0:8} -> http=$http len=${#payload}" >&2
  sleep 6
done
echo "done" >&2
