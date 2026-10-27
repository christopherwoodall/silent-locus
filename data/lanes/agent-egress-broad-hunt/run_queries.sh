#!/bin/bash
# GitHub CODE search lane, agent-egress broad hunt. Read-only GET only.
# Idempotent: skips queries with an existing non-empty capture file.
# Pace: 8s between calls. Code-search quota is 10/min (verified in headers).
# NOTE: gh api "-f q=" form returns 404 for search/code on this gh build;
# URL-form query strings work (verified 200 on 2026-10-27).
set -u
DIR="$HOME/workspace/silent-locus/data/lanes/agent-egress-broad-hunt/raw/github-code"
cd "$DIR" || exit 1
run() {
  local id="$1"; shift
  local q="$1"
  local f="${id}.json"
  if [ -s "$f" ]; then echo "SKIP $id (exists)"; return 0; fi
  local enc
  enc=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1]))' "$q")
  echo "RUN $id : $q"
  gh api "search/code?q=${enc}&per_page=30" \
    -H "Accept: application/vnd.github.text-match+json" > "${f}.tmp" 2>"${id}.err" || {
      echo "FAIL $id"; cat "${id}.err"; rm -f "${f}.tmp"; return 1; }
  mv "${f}.tmp" "$f"
  {
    echo "Source: GET https://api.github.com/search/code (query below, per_page=30)"
    echo "Query: $q"
    echo "Retrieved: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "Method: gh api search/code URL form (existing gh CLI auth, read-only), text-match Accept header"
  } > "${f}.PROVENANCE.txt"
  sha256sum "$f" > "${f}.sha256"
  rm -f "${id}.err"
  sleep 8
}
run c01 '"unshare -Urm"'
run c02 '"unshare --map-root-user"'
run c03 '"unshare -U"'
run c04 '"curl -o" "chmod +x"'
run c05 '"wget -O" "chmod +x"'
run c06 '"curl -fsSL" bash'
run c07 '"wget -qO-" bash'
run c08 '"cat /etc/resolv.conf" curl'
run c09 '"uname -a" curl'
run c10 '"169.254.169.254" curl'
run c11 '"metadata.google.internal" curl'
run c12 '"curl -T" amazonaws'
run c13 '"curl --upload-file" oss'
run c14 'sanmaohe'
run c15 'routify-file-proxy'
run c16 '"curl -F" amazonaws'
echo DONE
