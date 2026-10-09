#!/bin/bash
# Pull all files of one P1 dataset via curl (Hub resolve URLs), write PROVENANCE.md.
DS="$1"; SLUG="$2"
DIR="$HOME/workspace/silent-locus/data/hf-trajectories/raw/$SLUG"
cd "$DIR" || exit 1
UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 - <<'EOF' "$DS" "$SLUG"
import json, sys
ds, slug = sys.argv[1], sys.argv[2]
d = json.load(open(f"/home/hatch/workspace/silent-locus/data/hf-trajectories/raw/{slug}/api_card.json"))
files = [s['rfilename'] for s in d.get('siblings', [])]
open(f"/home/hatch/workspace/silent-locus/data/hf-trajectories/raw/{slug}/filelist.txt","w").write("\n".join(files))
print(f"{ds}: {len(files)} files")
EOF
cat filelist.txt | xargs -P 8 -I{} sh -c '
  f="{}"; mkdir -p "$(dirname "$f")"
  curl -sL --retry 3 --retry-delay 5 -o "$f" "https://huggingface.co/datasets/'"$DS"'/resolve/main/$f"
  if [ ! -s "$f" ]; then echo "EMPTY: $f" >&2; fi
'
sha256sum $(cat filelist.txt | grep -v '^$') > SHA256SUMS.txt 2>/dev/null
{
  echo "# Provenance: $DS"
  echo "retrieved: $UTC"
  echo "method: curl -sL https://huggingface.co/datasets/$DS/resolve/main/<file> (file list from https://huggingface.co/api/datasets/$DS)"
  echo "files: $(wc -l < filelist.txt)"
  echo "bytes: $(du -sb . | cut -f1)"
  echo ""
  echo "sha256 per file in SHA256SUMS.txt"
} > PROVENANCE.md
echo "DONE $SLUG: $(du -sh . | cut -f1)"
