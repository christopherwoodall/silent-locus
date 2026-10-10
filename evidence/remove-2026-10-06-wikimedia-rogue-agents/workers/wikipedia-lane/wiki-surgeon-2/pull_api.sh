#!/bin/bash
# wiki-surgeon-2 independent API verification pull
# curl-only (VM python HTTP stacks break on egress proxy), 6s pacing per methodology
set -u
OUTDIR="$HOME/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/workers/wikipedia-lane/wiki-surgeon-2/api_raw"
mkdir -p "$OUTDIR"
# wiki => revids (covering all 9 wikis present in the CSV; includes 3 of the 5 "missing" meta oldids)
declare -A Q=(
  ["en.wikipedia.org"]="1353490694|1356419247"
  ["test.wikipedia.org"]="741406|744268"
  ["test2.wikipedia.org"]="612931|613856"
  ["www.mediawiki.org"]="8370989"
  ["commons.wikimedia.org"]="1213513506|1238390511"
  ["simple.wikipedia.org"]="10891416"
  ["incubator.wikimedia.org"]="7226107|7226111"
  ["meta.wikimedia.org"]="30732655|30732691|30732696|30732700"
  ["bg.wikipedia.org"]="12923296"
)
LOG="$OUTDIR/pull.log"
: > "$LOG"
for host in "${!Q[@]}"; do
  revids_enc=$(printf '%s' "${Q[$host]}" | sed 's/|/%7C/g')
  url="https://${host}/w/api.php?action=query&prop=revisions&revids=${revids_enc}&rvprop=ids%7Ctimestamp%7Cuser%7Ccomment%7Ctags%7Ccontent&rvslots=main&format=json&formatversion=2&origin=*"
  code=$(curl -s -o "$OUTDIR/${host}.json" -w '%{http_code}' --max-time 60 "$url")
  echo "$(date -u +%FT%TZ) host=$host revids=${Q[$host]} http=$code bytes=$(stat -c%s "$OUTDIR/${host}.json")" | tee -a "$LOG"
  sleep 6
done
echo "done"
