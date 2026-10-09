#!/usr/bin/env bash
# GRAMMAR HUNT — urlquery htmx lane probe sweep.
# One probe per CLI call, 7s pacing between probes, 3 retries with backoff.
# Usage: ./run_probes.sh
set -u
CLI=~/workspace/skills/urlquery/bin/uq_htmx.py
OUT=~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw
LOG=$OUT/probe_run.log
mkdir -p "$OUT"

probes=(
  "nonce:?nonce="
  "tag:?tag="
  "task:?task="
  "batch:?batch="
  "run:?run="
  "step:?step="
  "worker:?worker="
  "agent:?agent="
  "label:?label="
  "job:?job="
  "session:?session="
  "token:?token="
  "v:?v="
  "id:?id="
  "x:?x="
  "prefix-agent-:agent-"
  "prefix-worker-:worker-"
  "prefix-step-:step-"
  "prefix-wave-:wave-"
)

: > "$LOG"
for entry in "${probes[@]}"; do
  name="${entry%%:*}"
  q="${entry#*:}"
  dest="$OUT/htmx-params-${name}.json"
  echo "=== [$name] query='$q' $(date -u +%FT%TZ)" | tee -a "$LOG"
  ok=0
  for attempt in 1 2 3; do
    if "$CLI" search --query "$q" --limit 60 > "$dest.tmp" 2>>"$LOG"; then
      if python3 -c "import json;d=json.load(open('$dest.tmp'));assert d.get('reports')" 2>/dev/null; then
        mv "$dest.tmp" "$dest"
        n=$(python3 -c "import json;print(len(json.load(open('$dest'))['reports']))")
        echo "  attempt $attempt OK: $n reports" | tee -a "$LOG"
        ok=1; break
      else
        echo "  attempt $attempt: empty/invalid result" | tee -a "$LOG"
      fi
    else
      echo "  attempt $attempt: CLI failed" | tee -a "$LOG"
    fi
    sleep $((20 * attempt))
  done
  [ $ok -eq 0 ] && echo "  FAILED after 3 attempts" | tee -a "$LOG" && rm -f "$dest.tmp"
  sleep 7
done
echo "DONE $(date -u +%FT%TZ)" | tee -a "$LOG"
