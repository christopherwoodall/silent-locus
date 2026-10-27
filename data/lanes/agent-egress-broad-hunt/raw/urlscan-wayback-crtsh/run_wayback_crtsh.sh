#!/bin/bash
# Wayback CDX (port 80 http) + crt.sh, read-only GET only. No login.
# Idempotent: skips existing nonzero files. Wayback backend is flaky:
# on empty/error, retry identical query after 45-90s (caller re-runs script).
set -u
OUT="$(dirname "$0")"
cd "$OUT" || exit 1
UA="Muse-hunt-lane/1.0 (read-only research)"
wb() {
  local name="$1"; local url="$2"
  local file="wayback_${name}.json"
  if [ -s "$file" ]; then echo "SKIP $file exists"; return 0; fi
  echo "GET $url"
  curl -sS -m 120 -A "$UA" "$url" -o "$file.tmp" || { echo "FAIL $name curl"; rm -f "$file.tmp"; return 1; }
  mv "$file.tmp" "$file"
  {
    echo "source URL: $url"
    echo "retrieval time (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "method: curl GET, http port 80 CDX API, no login"
  } > "$file.PROVENANCE.txt"
  sha256sum "$file" > "$file.sha256"
  sleep 5
}
crt() {
  local name="$1"; local q="$2"
  local file="crtsh_${name}.json"
  if [ -s "$file" ]; then echo "SKIP $file exists"; return 0; fi
  local url="https://crt.sh/?q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$q")&output=json"
  echo "GET $url"
  curl -sS -m 120 -A "$UA" "$url" -o "$file.tmp" || { echo "FAIL $name curl"; rm -f "$file.tmp"; return 1; }
  mv "$file.tmp" "$file"
  {
    echo "source URL: $url"
    echo "retrieval time (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "method: curl GET, crt.sh JSON output, no login"
    echo "query (verbatim): $q"
  } > "$file.PROVENANCE.txt"
  sha256sum "$file" > "$file.sha256"
  sleep 5
}
# Wayback: bare prefix matchType=prefix (no trailing *), plus domain matches.
wb sanmaohe_exact "http://web.archive.org/cdx/search/cdx?url=sanmaohe.oss-cn-beijing.aliyuncs.com&output=json&limit=1000"
wb sanmaohe_prefix "http://web.archive.org/cdx/search/cdx?url=sanmaohe.oss-cn-beijing.aliyuncs.com&output=json&matchType=prefix&limit=1000"
wb routify_sg_exact "http://web.archive.org/cdx/search/cdx?url=routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com&output=json&limit=1000"
wb routify_sg_prefix "http://web.archive.org/cdx/search/cdx?url=routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com&output=json&matchType=prefix&limit=1000"
wb proxy_temp_file_url "http://web.archive.org/cdx/search/cdx?url=aliyuncs.com/proxy_temp_file&output=json&matchType=prefix&limit=1000"
wb aliyuncs_domain "http://web.archive.org/cdx/search/cdx?url=aliyuncs.com&output=json&matchType=domain&limit=1000&collapse=urlkey"
wb metadata_169 "http://web.archive.org/cdx/search/cdx?url=169.254.169.254&output=json&matchType=prefix&limit=1000"
wb metadata_google "http://web.archive.org/cdx/search/cdx?url=metadata.google.internal&output=json&matchType=prefix&limit=1000"
# crt.sh: named hosts (exact + wildcard %) and OSS host families.
crt sanmaohe_exact "sanmaohe.oss-cn-beijing.aliyuncs.com"
crt sanmaohe_wild "%.sanmaohe.oss-cn-beijing.aliyuncs.com"
crt routify_sg_exact "routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com"
crt routify_sg_wild "%.routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com"
crt routify_pub_exact "routify-pub.alibaba-inc.com"
crt routify_online_exact "routify-online.alibaba-inc.com"
crt routify_alibaba_exact "routify.alibaba-inc.com"
crt aliyuncs_wild "%.aliyuncs.com"
crt oss_cn_beijing_wild "%.oss-cn-beijing.aliyuncs.com"
echo DONE
