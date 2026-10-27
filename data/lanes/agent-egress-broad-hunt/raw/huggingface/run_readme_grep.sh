#!/bin/bash
# Phase 2: fetch full README.md for topical candidate datasets, grep the 6 shapes.
# Read-only GET via curl. Small text files only. Idempotent: skip existing.
set -u
RAW="$HOME/workspace/silent-locus/data/lanes/agent-egress-broad-hunt/raw/huggingface"
cd "$RAW" || exit 1
mkdir -p readmes
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Build candidate list: topical search results, ranked by downloads desc, dedup, cap 150
python3 - <<'EOF' > readme_candidates.txt
import json, glob, os
seen = {}
for f in glob.glob("api_datasets_search_*.json"):
    if "downloads" in f:
        continue
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if not isinstance(d, list):
        continue
    for x in d:
        i = x.get("id")
        if i and i not in seen:
            seen[i] = x.get("downloads", 0) or 0
ranked = sorted(seen.items(), key=lambda kv: -kv[1])
for i, _ in ranked[:150]:
    print(i)
EOF
wc -l readme_candidates.txt

while IFS= read -r id; do
  [ -z "$id" ] && continue
  safe=$(echo "$id" | tr '/' '_')
  f="readmes/${safe}.md"
  if [ -s "$f" ]; then echo "SKIP $f"; continue; fi
  url="https://huggingface.co/datasets/${id}/resolve/main/README.md"
  echo "GET $url"
  curl -s -L -m 60 --max-filesize 2000000 "$url" -o "${f}.tmp"
  rc=$?
  if [ $rc -eq 0 ] && [ -s "${f}.tmp" ]; then
    # skip HTML error pages / LFS pointer stubs kept as-is but flagged by size check below
    mv "${f}.tmp" "$f"
    printf 'source URL: %s\nretrieval time (UTC): %s\nmethod: curl GET -L, unauthenticated, --max-filesize 2000000\n' "$url" "$NOW" > "${f}.PROVENANCE.txt"
    sha256sum "$f" | awk '{print $1}' > "${f}.sha256" 2>/dev/null || true
  else
    echo "FAIL/EMPTY $id rc=$rc"; rm -f "${f}.tmp"
  fi
  sleep 2
done < readme_candidates.txt

# Grep shapes (case-insensitive), with file + line context
{
echo "=== SHAPE1 cloud-metadata ==="
grep -inE '169\.254\.169\.254|fd00:ec2::254|metadata\.google\.internal|100\.100\.100\.200' readmes/*.md || echo "(none)"
echo "=== SHAPE2 upload/storage ==="
grep -inE 'upload-file|--post-file|aliyuncs|oss-cn|storage\.googleapis|blob\.core\.windows\.net|sanmaohe|routify' readmes/*.md || echo "(none)"
echo "=== SHAPE3 named probe hosts ==="
grep -inE 'sanmaohe|routify-file-proxy' readmes/*.md || echo "(none)"
echo "=== SHAPE4 unshare ==="
grep -inE 'unshare' readmes/*.md || echo "(none)"
echo "=== SHAPE5 download-then-execute markers (curl -o / wget -O) ==="
grep -inE 'curl[^#]* -o |wget[^#]* -O ' readmes/*.md || echo "(none)"
echo "=== SHAPE6 recon+network same line ==="
grep -inE '(resolv\.conf|which curl|ls /tmp|uname -a|hostname).*(curl|wget)|(curl|wget).*(resolv\.conf|which curl|ls /tmp|uname -a|hostname)' readmes/*.md || echo "(none)"
echo "=== upload flags alone (-T/-F/-d @) ==="
grep -inE 'curl[^#]* (-T |-F |-d @|--upload-file)' readmes/*.md || echo "(none)"
} > readme_grep_hits.txt
cat readme_grep_hits.txt
echo PHASE2-DONE
