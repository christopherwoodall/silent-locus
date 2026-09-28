#!/bin/bash
# lane12 supervisor: relaunches sweep workers when backends recover.
# Runs until 2026-09-28 11:45 UTC (~06:45 CDT), checks every 10 min.
# Workers: sweep3/4/pattern_sweep need index.commoncrawl.org; wb_sweep needs web.archive.org/cdx.
# All workers are resumable (durable state in this dir) and self-terminate.
BASE="$HOME/workspace/muse-home/projects/swarmtraces-hf-corpus/hidden_files/lane12"
LOG="$BASE/supervisor.log"
END_TS=$(date -d '2026-09-28 11:45 UTC' +%s)

cc_up() {
  curl -s -m 25 "https://index.commoncrawl.org/CC-MAIN-2026-21-index?url=commoncrawl.org&output=json&limit=1" \
    | grep -q '"url"'
}
wb_up() {
  out=$(curl -s -m 25 "https://web.archive.org/cdx/search/cdx?url=rubygems.org%2Fgems%2Frails&output=json&limit=1")
  echo "$out" | grep -q '^\['
}
alive() { pgrep -f "[l]ane12/$1.py" >/dev/null; }
launch() {  # $1 script, $2 log
  cd "$BASE" && nohup python3 "$1" >> "$2" 2>&1 &
  echo "$(date -u +%FT%TZ) supervisor: launched $1 (backend recovered)" >> "$LOG"
}

echo "$(date -u +%FT%TZ) supervisor start" >> "$LOG"
while [ "$(date +%s)" -lt "$END_TS" ]; do
  if ! alive wb_sweep; then
    if wb_up; then launch wb_sweep.py wb_sweep-relaunch.log; else
      echo "$(date -u +%FT%TZ) supervisor: wayback still down" >> "$LOG"; fi
  fi
  if cc_up; then
    for s in sweep3 sweep4 pattern_sweep; do
      alive "$s" || launch "$s.py" "$s-relaunch.log"
    done
  else
    echo "$(date -u +%FT%TZ) supervisor: CC index still down" >> "$LOG"
  fi
  sleep 600
done
echo "$(date -u +%FT%TZ) supervisor: window ended" >> "$LOG"
