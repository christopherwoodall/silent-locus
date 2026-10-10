#!/usr/bin/env bash
# recheck_deaddrops.sh — probe webhook.site inboxes for ghost-hunter DEAD-DROP GRAVEYARD.
# Run when egress is back. Writes raw probe results to raw/deaddrop-probe-<ts>.jsonl.
# DO NOT run faster than 1 req/5s against webhook.site (see sleep below).
set -u
cd "$(dirname "$0")"
mkdir -p raw
OUT="raw/deaddrop-probe-$(date -u +%Y%m%dT%H%M%SZ).jsonl"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

INBOXES="
6ddc559e-5c08-4915-a5b2-f4addc42368a
0a947514-5b43-4030-9f9f-b193dd2d519b
a7753b69-2ceb-4221-adfa-80f69d57480c
6051dd2b-86dc-427d-8083-071a687af4f8
00f36f21-d00e-48b3-9456-8bf532e8c863
441b7745-1087-463e-b539-984a2ee3ea65
c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357
1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56
35f6980c-7dc6-4af4-b646-56ca0070a200
"

echo "probing $(echo "$INBOXES" | grep -c .) inboxes -> $OUT"
for uuid in $INBOXES; do
  ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  # 1) JSON token endpoint (frontend data source)
  body="$(curl -s -m 25 -A "$UA" "https://webhook.site/token/$uuid" || echo CURL_FAIL)"
  code="$(curl -s -m 25 -o /dev/null -w '%{http_code}' -A "$UA" "https://webhook.site/token/$uuid" || echo 000)"
  # 2) HTML page (expiry marker check)
  page="$(curl -s -m 25 -A "$UA" "https://webhook.site/$uuid" | head -c 3000 || echo CURL_FAIL)"
  printf '%s\n' "{\"probed_at\":\"$ts\",\"uuid\":\"$uuid\",\"token_http\":$code,\"token_body\":$(printf '%s' "$body" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),\"page_head\":$(printf '%s' "$page" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}" >> "$OUT"
  echo "$uuid -> token HTTP $code"
  sleep 6
done
echo "done. summarizing newest request timestamps:"
python3 - "$OUT" <<'EOF'
import json, sys
for line in open(sys.argv[1]):
    d = json.loads(line)
    body = d.get("token_body") or ""
    newest = "n/a"
    try:
        j = json.loads(body)
        reqs = j.get("requests") or []
        ts = [r.get("created_at") for r in reqs if isinstance(r, dict) and r.get("created_at")]
        if ts: newest = max(ts)
        print(f"{d['uuid'][:8]}… token_http={d['token_http']} requests={len(reqs)} newest={newest}")
    except Exception:
        marker = "EXPIRED?" if ("expired" in body.lower() or "does not exist" in body.lower()) else "?"
        print(f"{d['uuid'][:8]}… token_http={d['token_http']} newest={marker}")
EOF
