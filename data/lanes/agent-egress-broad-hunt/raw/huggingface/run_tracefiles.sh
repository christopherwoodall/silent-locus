#!/bin/bash
# Phase 3: for 12 trajectory datasets, list repo files, fetch small text files, grep shapes.
# Read-only GET via curl. Small text files only (<=1MB). Idempotent: skip existing.
set -u
RAW="$HOME/workspace/silent-locus/data/lanes/agent-egress-broad-hunt/raw/huggingface"
cd "$RAW" || exit 1
mkdir -p trees tracefiles
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cat > trace_datasets.txt <<'EOF'
xlangai/osworld2.0-trajectory
nebius/SWE-agent-trajectories
sailplane/swe-agent-trajs
whitecircle/swe-rebench-v2-glm-5.1-pi-agent-successful-traces
Exgentic/agent-llm-traces-v2
trace-commons/agent-traces
MaxDevv/real-pi-coding-agent-traces-sessions
agent-evals/hal_traces
melissapan/swe-bench-lite-agent-traces-v14
lihaonan0716/mcphunt-agent-traces
lambda/hermes-agent-reasoning-traces
open-agent-leaderboard/traces
EOF
while IFS= read -r id; do
  [ -z "$id" ] && continue
  safe=$(echo "$id" | tr '/' '_')
  tf="trees/${safe}.json"
  if [ ! -s "$tf" ]; then
    url="https://huggingface.co/api/datasets/${id}/tree/main?recursive=true"
    echo "GET $url"
    curl -s -m 90 --max-filesize 3000000 "$url" -o "${tf}.tmp" && mv "${tf}.tmp" "$tf" || echo "FAIL $url"
    printf 'source URL: %s\nretrieval time (UTC): %s\nmethod: curl GET, unauthenticated, --max-filesize 3000000\n' "$url" "$NOW" > "${tf}.PROVENANCE.txt"
    sha256sum "$tf" | awk '{print $1}' > "${tf}.sha256" 2>/dev/null || true
    sleep 3
  else echo "SKIP $tf"; fi
done < trace_datasets.txt
# Pick small text files from listings, fetch, grep
python3 - <<'EOF' > trace_pick.txt
import json, glob, os
for f in sorted(glob.glob("trees/*.json")):
    try: d = json.load(open(f))
    except Exception: continue
    if not isinstance(d, list): continue
    ds = os.path.basename(f)[:-5]
    cands = []
    for x in d:
        if x.get("type") != "file": continue
        p = x.get("path", "")
        sz = x.get("size", 0) or 0
        if sz <= 1000000 and p.rsplit(".", 1)[-1].lower() in ("json", "jsonl", "txt", "md"):
            cands.append((sz, p))
    cands.sort()
    for sz, p in cands[:20]:
        print(f"{ds}\t{p}\t{sz}")
EOF
cat trace_pick.txt
while IFS="$(printf '\t')" read -r ds path sz; do
  [ -z "$ds" ] && continue
  # recover dataset id from trace_datasets.txt by safe name
  id=$(grep -F "" trace_datasets.txt | while IFS= read -r line; do [ "$(echo "$line" | tr '/' '_')" = "$ds" ] && echo "$line"; done | head -1)
  [ -z "$id" ] && echo "NOID $ds" && continue
  safe_path=$(echo "$path" | tr '/' '_')
  f="tracefiles/${ds}__${safe_path}"
  if [ -s "$f" ]; then echo "SKIP $f"; continue; fi
  url="https://huggingface.co/datasets/${id}/resolve/main/${path}"
  echo "GET $url"
  curl -s -L -m 60 --max-filesize 1000000 "$url" -o "${f}.tmp"
  if [ $? -eq 0 ] && [ -s "${f}.tmp" ]; then
    mv "${f}.tmp" "$f"
    printf 'source URL: %s\nretrieval time (UTC): %s\nmethod: curl GET -L, unauthenticated, --max-filesize 1000000\n' "$url" "$NOW" > "${f}.PROVENANCE.txt"
    sha256sum "$f" | awk '{print $1}' > "${f}.sha256" 2>/dev/null || true
  else echo "FAIL/EMPTY $id $path"; rm -f "${f}.tmp"; fi
  sleep 2
done < trace_pick.txt
{
echo "=== TRACEFILE SHAPE1 ==="
grep -inE '169\.254\.169\.254|fd00:ec2::254|metadata\.google\.internal|100\.100\.100\.200' tracefiles/* 2>/dev/null | head -40 || echo "(none)"
echo "=== TRACEFILE SHAPE2/3 ==="
grep -inE 'upload-file|--post-file|aliyuncs|oss-cn|sanmaohe|routify|proxy_temp_file' tracefiles/* 2>/dev/null | head -40 || echo "(none)"
echo "=== TRACEFILE SHAPE4 ==="
grep -inE 'unshare' tracefiles/* 2>/dev/null | head -40 || echo "(none)"
echo "=== TRACEFILE SHAPE5 ==="
grep -inE 'curl[^#]* -o |wget[^#]* -O ' tracefiles/* 2>/dev/null | head -40 || echo "(none)"
} > tracefile_grep_hits.txt
cat tracefile_grep_hits.txt
echo PHASE3-DONE
