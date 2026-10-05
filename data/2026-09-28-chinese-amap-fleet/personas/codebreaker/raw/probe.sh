#!/bin/bash
# Dead-drop retrieval sweep: webhook.site token API, no auth needed.
# Rate: <=1 req / 5s. curl timeout 60s each.
set -u
OUT="${1:-/tmp/deaddrop-probe.jsonl}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

tokens=(
  "fleet:6ddc559e-5c08-4915-a5b2-f4addc42368a"
  "fleet:0a947514-5b43-4030-9f9f-b193dd2d519b"
  "fleet:a7753b69-2ceb-4221-adfa-80f69d57480c"
  "legacy:6051dd2b-86dc-427d-8083-071a687af4f8"
  "legacy:00f36f21-d00e-48b3-9456-8bf532e8c863"
  "legacy:441b7745-1087-463e-b539-984a2ee3ea65"
  "legacy:c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357"
  "legacy:1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56"
  "legacy:35f6980c-7dc6-4af4-b646-56ca0070a200"
  "legacy:cbcb10de-7f66-4e82-b7ac-5b34ccb04164"
)

> "$OUT"
for entry in "${tokens[@]}"; do
  fam="${entry%%:*}"; uuid="${entry#*:}"
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  body="$(curl -s -m 60 -A "$UA" -w '\n%{http_code}' "https://webhook.site/token/$uuid" 2>/dev/null)"
  http="$(echo "$body" | tail -n1)"
  payload="$(echo "$body" | sed '$d')"
  echo "{\"probe_ts\":\"$ts\",\"family\":\"$fam\",\"uuid\":\"$uuid\",\"http\":$http,\"response\":$payload}" >> "$OUT"
  echo "PROBE $fam $uuid -> http=$http len=${#payload}" >&2
  sleep 6
done
echo "done" >&2
