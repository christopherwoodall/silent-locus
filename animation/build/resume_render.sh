#!/bin/bash
# resume_render.sh — resumable, crash-safe renderer for the silent-locus chibi cuts.
#
# Durability contract (Christopher's requirement: survive VM restarts):
#   - Lock-guarded (flock): two copies can never render at once.
#   - Renders only missing frames: render.py skips existing PNGs and writes
#     atomically (tmp + rename), so a frame is never rendered twice and a
#     killed run can't leave a partial PNG.
#   - Progress manifest work/render_progress.json is recount-from-disk ground
#     truth, updated on every invocation.
#   - When both cuts are complete it runs the idempotent encode + verify, then
#     touches work/pipeline_done so the cron worker can retire this job.
# Fully self-contained: absolute paths, no session state.
set -u
ANIM="/home/hatch/workspace/silent-locus/animation"
BUILD="$ANIM/build"
WORK="$ANIM/work"
LOCK="$WORK/render.lock"
PROGRESS="$WORK/render_progress.json"
LOG="$WORK/render.log"
DONE="$WORK/pipeline_done"

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }

TOTAL="$(python3 "$BUILD/render.py" vertical --total-frames)"
log "resume_render start (total_frames=$TOTAL)"

exec 9>"$LOCK"
if ! flock -n 9; then
  log "lock held by another render; exiting"
  exit 0
fi

count_frames() { # $1 = v|l
  ls "$WORK/chibi_$1"/f*.png 2>/dev/null | wc -l
}

update_progress() {
  local v l
  v="$(count_frames v)"; l="$(count_frames l)"
  python3 - "$PROGRESS" "$v" "$l" "$TOTAL" <<'EOF'
import json, sys
p, v, l, t = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
json.dump({"vertical": {"done": v, "total": t},
           "landscape": {"done": l, "total": t}}, open(p, "w"), indent=1)
EOF
  log "progress vertical=$v/$TOTAL landscape=$l/$TOTAL"
}

update_progress

for spec in "vertical:v" "landscape:l"; do
  cut="${spec%%:*}"; tag="${spec##*:}"
  # drop any partial tmp writes from a killed run (they're never counted)
  rm -f "$WORK/chibi_$tag"/f*.png.tmp
  have="$(count_frames "$tag")"
  if [ "$have" -lt "$TOTAL" ]; then
    log "rendering $cut (have $have/$TOTAL)"
    if python3 "$BUILD/render.py" "$cut" >>"$LOG" 2>&1; then
      log "$cut render pass finished"
    else
      log "$cut render pass exited nonzero (resumable; will continue next run)"
    fi
    update_progress
  else
    log "$cut already complete ($have/$TOTAL)"
  fi
done

v="$(count_frames v)"; l="$(count_frames l)"
if [ "$v" -ge "$TOTAL" ] && [ "$l" -ge "$TOTAL" ]; then
  log "both cuts complete; running idempotent encode"
  if bash "$BUILD/encode.sh" >>"$LOG" 2>&1; then
    log "encode ok; verifying"
    if python3 "$BUILD/verify.py" >>"$LOG" 2>&1; then
      log "verify PASS; pipeline done"
      touch "$DONE"
    else
      log "verify FAILED; leaving for next run / manual inspection"
    fi
  else
    log "encode FAILED"
  fi
  update_progress
else
  log "incomplete: vertical=$v/$TOTAL landscape=$l/$TOTAL"
fi
log "resume_render end"
