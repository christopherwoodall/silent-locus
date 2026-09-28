#!/bin/bash
# lane12 supervisor v3: relaunches sweep workers when backends recover.
# Window: 2026-09-28 ~17:35 UTC -> 2026-09-30 12:00 UTC, checks every 10 min.
# Installed after v2 died in a runtime restart drain (~2026-09-28 11:54 UTC).
# Workers: sweep3/4/pattern_sweep need index.commoncrawl.org; wb_sweep needs web.archive.org/cdx.
# All workers are resumable (durable state in this dir) and self-terminate.
# Probes carry a nonce (cache-busting on liveness checks is mandatory).
# Note: egress-proxy quirk — curl may report HTTP 000 with "Empty reply from
#   server" even on a live backend; probes demand real JSON/body matches.
BASE="$HOME/workspace/muse-home/projects/swarmtraces-hf-corpus/hidden_files/lane12"
LOG="$BASE/supervisor.log"
END_TS=$(date -d '2026-09-30 12:00 UTC' +%s)

cc_up() {
  curl -s -m 25 "https://index.commoncrawl.org/CC-MAIN-2026-21-index?url=commoncrawl.org&output=json&limit=1&x=$(date +%s)" \
    | grep -q '"url"'
}
wb_up() {
  out=$(curl -s -m 25 "https://web.archive.org/cdx/search/cdx?url=rubygems.org%2Fgems%2Frails&output=json&limit=1&x=$(date +%s)")
  echo "$out" | grep -q '^\['
}
alive() { pgrep -f "[l]ane12/$1.py" >/dev/null; }
launch() {  # $1 script, $2 log — full path in argv so alive() matches
  nohup python3 "$BASE/$1" >> "$BASE/$2" 2>&1 &
  echo "$(date -u +%FT%TZ) supervisor v3: launched $1 (backend recovered)" >> "$LOG"
}
log() { echo "$(date -u +%FT%TZ) supervisor v3: $1" >> "$LOG"; }

# Completion markers (workers print DONE on natural completion, then exit).
wb_done()      { grep -q '^DONE wayback sweep' "$BASE"/wb_sweep*.log 2>/dev/null; }
sweep3_done()  { grep -q '^DONE all crawls' "$BASE"/sweep3*.log 2>/dev/null; }
sweep4_done()  { grep -q '^DONE sweep4' "$BASE"/sweep4*.log 2>/dev/null; }
pattern_done() { grep -q '^DONE \[jina-url\]' "$BASE"/pattern_sweep*.log 2>/dev/null; }
all_done() { wb_done && sweep3_done && sweep4_done && pattern_done; }

log "start (window ends 2026-09-30 12:00 UTC)"
while [ "$(date +%s)" -lt "$END_TS" ]; do
  if ! wb_done && ! alive wb_sweep; then
    if wb_up; then launch wb_sweep.py wb_sweep-v3.log; else
      log "wayback still down"; fi
  fi
  if cc_up; then
    ! sweep3_done  && ! alive sweep3  && launch sweep3.py sweep3-v3.log
    ! sweep4_done  && ! alive sweep4  && launch sweep4.py sweep4-v3.log
    ! pattern_done && ! alive pattern_sweep && launch pattern_sweep.py pattern_sweep-v3.log
  else
    log "CC index still down"
  fi
  if all_done; then log "all workers complete; exiting"; break; fi
  sleep 600
done
log "window ended"
