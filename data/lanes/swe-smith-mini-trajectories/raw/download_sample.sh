#!/bin/bash
# Download the sampled shards for the SWE-smith-mini trajectory lane.
# Idempotent: skips files already present with a verified sha256.
# Resumes partial downloads with curl -C -. Stops if disk < 10 GiB.
set -u
RAW="$HOME/workspace/silent-locus/data/lanes/swe-smith-mini-trajectories/raw"
REV="750b2c11239fd5e32f97e6cfb9bf80fb9a9a2983"
BASE="https://huggingface.co/datasets/Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k/resolve/${REV}/data"
KEEP="01 02 03 04 05 06 07 08 09 10 11 12 14 15 16 17 19 20 21 24 25 27 28 29 30 31 32 33 34 35 36 37 38 39 41 42 43 44 46"
LOG="$RAW/download.log"
cd "$RAW" || exit 1

log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }

for s in $KEEP; do
  fn="train-000${s}-of-00047.parquet"
  url="${BASE}/${fn}"
  # idempotent skip
  if [ -f "$fn" ] && [ -f "$fn.sha256" ]; then
    if sha256sum -c "$fn.sha256" >/dev/null 2>&1; then
      log "SKIP $fn (already present, sha256 ok)"
      continue
    else
      log "RETRY $fn (sha256 mismatch, re-downloading)"
      rm -f "$fn"
    fi
  fi
  # disk guard: stop under 10 GiB free
  free_kb=$(df -k /home/hatch | tail -1 | awk '{print $4}')
  if [ "$free_kb" -lt 10485760 ]; then
    log "STOP: free space ${free_kb}kB < 10 GiB"
    exit 2
  fi
  log "GET $fn"
  echo "$url" > "$fn.SOURCE_URL.txt"
  t0=$(date -u +%FT%TZ)
  ok=0
  for attempt in $(seq 1 10); do
    if curl -L -C - --retry 2 --retry-delay 15 --retry-all-errors \
            --speed-limit 50000 --speed-time 120 --connect-timeout 60 \
            -o "$fn" "$url"; then
      ok=1; break
    fi
    log "RETRY $fn attempt $attempt failed (curl exit $?)"
    sleep 20
  done
  if [ "$ok" = "1" ]; then
    t1=$(date -u +%FT%TZ)
    sha256sum "$fn" > "$fn.sha256"
    cat > "$fn.PROVENANCE.txt" <<EOF
Provenance for: $fn
Dataset: Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k
Dataset revision (git sha): $REV
Source URL: $url
Retrieval time (UTC): $t0 .. $t1
Method: curl -L -C - --retry 3 -o (single-threaded; huggingface_hub is broken on this VM)
License: mit (verified verbatim from HF API cardData.license and README frontmatter; see LICENSE.note)
EOF
    rows=$(python3 -c "import pyarrow.parquet as pq; print(pq.read_metadata('$fn').num_rows)" 2>/dev/null || echo "?")
    log "OK $fn rows=$rows sha=$(cut -c1-16 "$fn.sha256")"
  else
    log "FAIL $fn (curl exit $?)"
  fi
done
log "ALL DONE"
