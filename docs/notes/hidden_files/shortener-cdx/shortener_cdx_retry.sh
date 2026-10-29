#!/usr/bin/env bash
# Standing retry: shortener-stats Wayback slice.
#
# The shortener archive lane found Wayback CDX down (503/timeouts). This slice
# (12 shortener stats-page URLs) is UNCLAIMED -- lane12's wb_sweep.py covers
# gem pages only. Poll the CDX backend every 15 min; when it recovers, pull
# archived captures of the 12 stats URLs (May-Jul 2026 priority), explode
# per-row (explicit events only), stage to disk.
#
# Window: until 2026-09-30 12:00 UTC (matches lane12 supervisor window).
# Disk-only: no hosted-Elastic writes (pause in effect). Commits results via git.
set -u
PROJ="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$PROJ" || exit 1
LOG="hidden_files/shortener-cdx/retry.log"
DEADLINE="2026-09-30T12:00:00Z"
mkdir -p hidden_files/shortener-cdx data/university-shorteners/wayback

log() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }

log "shortener-cdx retry started; deadline $DEADLINE"

probe() {
  # cache-busting nonce per standing rule; CDX probe with short timeout
  local nonce; nonce=$(date +%s)
  curl -sS -m 20 -o /dev/null -w "%{http_code}" \
    "https://web.archive.org/cdx/search/cdx?url=example.com&output=json&fl=timestamp&limit=1&x=${nonce}" 2>/dev/null
}

while :; do
  now=$(date -u +%s)
  deadline=$(date -u -d "$DEADLINE" +%s)
  if [ "$now" -ge "$deadline" ]; then
    log "deadline reached with Wayback still down; standing down"
    echo "STOOD-DOWN deadline-reached $(date -u +%FT%TZ)" >> "$LOG"
    exit 0
  fi
  if [ -f "data/university-shorteners/wayback/DONE" ]; then
    log "DONE marker present; exiting"
    exit 0
  fi
  code=$(probe)
  if [ "$code" = "200" ]; then
    log "Wayback CDX reachable (probe 200); running pull_and_explode.py"
    if python3 hidden_files/shortener-cdx/pull_and_explode.py >> "$LOG" 2>&1; then
      log "pull+explode succeeded; committing"
      git add hidden_files/shortener-cdx data/university-shorteners/wayback \
              data/university-shorteners-events >> "$LOG" 2>&1
      git commit -m "Shortener-stats Wayback slice: CDX recovered, captures pulled + exploded per-row (disk-staged, no hosted writes)" \
        >> "$LOG" 2>&1
      git push >> "$LOG" 2>&1 || log "push failed (will retry next watcher run)"
      log "standing retry COMPLETE"
      exit 0
    else
      log "pull_and_explode.py failed; will retry in 15 min"
    fi
  else
    log "Wayback CDX still down (probe=$code); retry in 15 min"
  fi
  sleep 900
done
