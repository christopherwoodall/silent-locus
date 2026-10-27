#!/bin/bash
# HF lane: API searches (id/name match only) + topical enumeration for README grep phase.
# Read-only GET via curl. Polite: sleep between calls. Idempotent: skip existing files.
set -u
RAW="$HOME/workspace/silent-locus/data/lanes/agent-egress-broad-hunt/raw/huggingface"
cd "$RAW" || exit 1
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
urlenc() { python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1"; }

search_kind() { # $1=kind $2=term
  _kind="$1"; _term="$2"
  _f="api_${_kind}_search_$(echo "$_term" | tr -c 'a-zA-Z0-9' '_').json"
  if [ -s "$_f" ]; then echo "SKIP $_f"; return; fi
  _q=$(urlenc "$_term")
  _url="https://huggingface.co/api/${_kind}?search=${_q}&limit=100"
  echo "GET $_url"
  curl -s -m 90 "$_url" -o "${_f}.tmp" && mv "${_f}.tmp" "$_f" || echo "FAIL $_url"
  printf 'source URL: %s\nretrieval time (UTC): %s\nmethod: curl GET, unauthenticated, -m 90\n' "$_url" "$NOW" > "${_f}.PROVENANCE.txt"
  sha256sum "$_f" | awk '{print $1}' > "${_f}.sha256" 2>/dev/null || true
  sleep 3
}

SHAPE_TERMS="169.254 metadata.google.internal 100.100.100.200 fd00:ec2 sanmaohe routify proxy_temp_file aliyuncs unshare cloud-metadata"
for t in $SHAPE_TERMS; do search_kind datasets "$t"; done
for t in $SHAPE_TERMS; do search_kind models "$t"; done
for t in $SHAPE_TERMS; do search_kind spaces "$t"; done

TOPICAL="trajectory agent-traces computer-use web-agent OSWorld WebArena SWE-agent agent-benchmark browser-agent tool-use"
for t in $TOPICAL; do search_kind datasets "$t"; done

# Downloads-sorted topical lists (most-downloaded first) for README prioritisation
for t in trajectory agent-traces computer-use web-agent; do
  f="api_datasets_search_${t}_downloads.json"
  if [ ! -s "$f" ]; then
    q=$(urlenc "$t")
    url="https://huggingface.co/api/datasets?search=${q}&limit=100&sort=downloads"
    echo "GET $url"
    curl -s -m 90 "$url" -o "$f.tmp" && mv "$f.tmp" "$f" || echo "FAIL $url"
    printf 'source URL: %s\nretrieval time (UTC): %s\nmethod: curl GET, unauthenticated, -m 90\n' "$url" "$NOW" > "$f.PROVENANCE.txt"
    sha256sum "$f" | awk '{print $1}' > "$f.sha256" 2>/dev/null || true
    sleep 3
  fi
done
echo DONE
