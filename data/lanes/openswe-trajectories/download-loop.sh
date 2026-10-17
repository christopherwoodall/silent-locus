#!/bin/bash
# Patient whole-file downloader for the Open-SWE-Traces stratified sample.
# Context: the egress Sentinel policy intermittently denies (approval timeout)
# requests to the HF Xet CDN host (us.aws.cdn.hf.co). Approvals DO succeed
# sometimes (two large transfers completed 2026-10-16 ~21:17-21:24 UTC), so
# this loop retries at LOW frequency (20 min spacing) instead of hammering.
# Each attempt is an independent, policy-evaluated HTTPS GET of a whole file.
# Acceptance criteria per file: exact byte size AND parquet magic (PAR1).
# On success it writes <file>.PROVENANCE.txt (5-line format) and moves on.
# Usage: setsid nohup ./download-loop.sh >/tmp/dl_patient.log 2>&1 &
set -u
RAW="$(cd "$(dirname "$0")/raw" && pwd)"
REV="1db674173119d71df45c22007af99e214600711a"
BASE="https://huggingface.co/datasets/nvidia/Open-SWE-Traces/resolve/$REV"
LOG="/tmp/dl_patient.log"

# local_name | repo_path | expected_bytes
FILES=(
  "openhands_qwen35_122b_swe-rebench-v2_train-00000-of-00017.parquet|data/openhands/qwen35_122b/swe-rebench-v2/train-00000-of-00017.parquet|236380400"
  "sweagent_minimax_m25_swe-rebench-v2_train-00000-of-00019.parquet|data/sweagent/minimax_m25/swe-rebench-v2/train-00000-of-00019.parquet|208152116"
)

ts() { date -u +%FT%TZ; }

for entry in "${FILES[@]}"; do
  IFS='|' read -r NAME RPATH TARGET <<< "$entry"
  for i in $(seq 1 8); do
    echo "$(ts) $NAME attempt $i" >> "$LOG"
    curl -sL --connect-timeout 90 --max-time 2400 \
      -o "$RAW/$NAME" "$BASE/$RPATH"
    SZ=$(stat -c%s "$RAW/$NAME" 2>/dev/null || echo 0)
    MAGIC=$(head -c 4 "$RAW/$NAME" 2>/dev/null || echo "NONE")
    echo "$(ts) $NAME attempt $i exit=$? size=$SZ magic=$MAGIC" >> "$LOG"
    if [ "$SZ" -eq "$TARGET" ] && [ "$MAGIC" = "PAR1" ]; then
      SHA=$(sha256sum "$RAW/$NAME" | cut -d' ' -f1)
      MTS=$(stat -c %y "$RAW/$NAME" | cut -d. -f1 | tr ' ' 'T')
      printf 'source_url: %s/%s\nretrieved_at: %sZ\nretrieval_method: https-get\nsha256: %s\ndataset_revision: %s\n' \
        "$BASE" "$RPATH" "$MTS" "$SHA" "$REV" > "$RAW/$NAME.PROVENANCE.txt"
      rm -f "$RAW/$NAME.partial"
      echo "$(ts) $NAME DONE sha256=$SHA" >> "$LOG"
      break
    fi
    rm -f "$RAW/$NAME"
    sleep 1200
  done
done
echo "$(ts) LOOP FINISHED" >> "$LOG"
