#!/bin/bash
# Phase 4 (bounded): fetch top-30 model cards from the agent model search, grep shapes.
# Read-only GET via curl. Small text only. Idempotent: skip existing.
set -u
RAW="$HOME/workspace/silent-locus/data/lanes/agent-egress-broad-hunt/raw/huggingface"
cd "$RAW" || exit 1
mkdir -p modelcards
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
python3 -c "
import json
d = json.load(open('api_models_search_agent_downloads.json'))
for x in d[:30]: print(x['id'])
" > modelcard_candidates.txt
wc -l modelcard_candidates.txt
while IFS= read -r id; do
  [ -z "$id" ] && continue
  safe=$(echo "$id" | tr '/' '_')
  f="modelcards/${safe}.md"
  if [ -s "$f" ]; then echo "SKIP $f"; continue; fi
  url="https://huggingface.co/${id}/resolve/main/README.md"
  echo "GET $url"
  curl -s -L -m 60 --max-filesize 2000000 "$url" -o "${f}.tmp"
  if [ $? -eq 0 ] && [ -s "${f}.tmp" ]; then
    mv "${f}.tmp" "$f"
    printf 'source URL: %s\nretrieval time (UTC): %s\nmethod: curl GET -L, unauthenticated, --max-filesize 2000000\n' "$url" "$NOW" > "${f}.PROVENANCE.txt"
    sha256sum "$f" | awk '{print $1}' > "${f}.sha256" 2>/dev/null || true
  else echo "FAIL/EMPTY $id"; rm -f "${f}.tmp"; fi
  sleep 2
done < modelcard_candidates.txt
{
echo "=== MODELCARD SHAPE1 ==="
grep -inE '169\.254\.169\.254|fd00:ec2::254|metadata\.google\.internal|100\.100\.100\.200' modelcards/*.md || echo "(none)"
echo "=== MODELCARD SHAPE2/3 ==="
grep -inE 'upload-file|--post-file|aliyuncs|oss-cn|sanmaohe|routify|proxy_temp_file' modelcards/*.md || echo "(none)"
echo "=== MODELCARD SHAPE4 ==="
grep -inE 'unshare' modelcards/*.md || echo "(none)"
echo "=== MODELCARD SHAPE5 ==="
grep -inE 'curl[^#]* -o |wget[^#]* -O ' modelcards/*.md || echo "(none)"
} > modelcard_grep_hits.txt
cat modelcard_grep_hits.txt
echo PHASE4-DONE
