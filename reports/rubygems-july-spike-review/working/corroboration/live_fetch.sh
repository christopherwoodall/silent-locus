#!/bin/bash
# Corroboration lane live spot-checks, READ-ONLY GET only. Saves full bytes + provenance + sha256.
OUT=~/workspace/silent-locus/data/lanes/rubygems-july-spike-review/raw/corroboration
mkdir -p "$OUT"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
RG="mini-sharp-hub ultra-fast-box mega-max-tool mini-fast-rb piko-max-gem piko-lite-mod hyper-lite-tool micro-pure-box piko-fast-kit ultra-clean-mod test-apex-gem xss-test-gem test-ssti-0 jrjackson shirobai sportdb-parser edoxen apex-blk-test-final test_gem_kangaroo apex-black-test-012"
for n in $RG; do
  f="$OUT/rubygems-api-$n.json"
  code=$(curl -sS -L --max-time 60 -o "$f" -w "%{http_code}" "https://rubygems.org/api/v1/gems/$n.json" 2>"$f.curlerr" || echo "CURL_FAIL")
  printf 'source_url: https://rubygems.org/api/v1/gems/%s.json\nretrieved_utc: %s\nmethod: curl -L GET, unauthenticated, read-only\nhttp_code_or_curl: %s\n' "$n" "$TS" "$code" > "$f.PROVENANCE.txt"
  sha256sum "$f" | awk '{print $1}' > "$f.sha256"
  echo "rubygems $n -> $code"
done
DF="mini-sharp-hub ultra-fast-box piko-max-gem micro-pure-box test-apex-gem xss-test-gem test-ssti-0 jrjackson shirobai sportdb-parser"
for n in $DF; do
  f="$OUT/diffend-$n.html"
  code=$(curl -sS -L --max-time 60 -o "$f" -w "%{http_code}" "https://my.diffend.io/gems/$n" 2>"$f.curlerr" || echo "CURL_FAIL")
  printf 'source_url: https://my.diffend.io/gems/%s\nretrieved_utc: %s\nmethod: curl -L GET, unauthenticated, read-only\nhttp_code_or_curl: %s\n' "$n" "$TS" "$code" > "$f.PROVENANCE.txt"
  sha256sum "$f" | awk '{print $1}' > "$f.sha256"
  echo "diffend $n -> $code"
done
echo "done $TS"
