#!/bin/bash
# urlscan anonymous search API, read-only GET only. No login, no key.
# Idempotent: skips files that already exist with nonzero size.
set -u
OUT="$(dirname "$0")"
cd "$OUT" || exit 1
UA="Muse-hunt-lane/1.0 (read-only research; contact via repo)"
fetch() {
  local name="$1"; local q="$2"
  local file="urlscan_${name}.json"
  if [ -s "$file" ]; then echo "SKIP $file exists"; return 0; fi
  local url="https://urlscan.io/api/v1/search/?q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$q")&size=100"
  echo "GET $q"
  curl -sS -m 120 -A "$UA" "$url" -o "$file.tmp"
  local rc=$?
  if [ $rc -ne 0 ]; then echo "FAIL $name rc=$rc"; rm -f "$file.tmp"; return 1; fi
  mv "$file.tmp" "$file"
  {
    echo "source URL: $url"
    echo "retrieval time (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "method: curl GET, anonymous, no login, no API key"
    echo "query (verbatim): $q"
  } > "$file.PROVENANCE.txt"
  sha256sum "$file" > "$file.sha256"
  sleep 6
}
fetch metadata_169 "169.254.169.254"
fetch metadata_google "metadata.google.internal"
fetch metadata_100 "100.100.100.200"
fetch sanmaohe "sanmaohe"
fetch routify_file_proxy "routify-file-proxy"
fetch aliyuncs "aliyuncs.com"
fetch domain_aliyuncs "domain:aliyuncs.com"
fetch proxy_temp_file "proxy_temp_file"
fetch unshare "unshare"
fetch gcs "storage.googleapis.com"
fetch azure_blob "blob.core.windows.net"
fetch r2 "r2.dev"
fetch probe_payload "PROBE_PAYLOAD"
fetch s3 "s3.amazonaws.com"
fetch oss_cn "oss-cn-beijing.aliyuncs.com"
echo DONE
