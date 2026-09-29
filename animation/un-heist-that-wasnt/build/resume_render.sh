#!/bin/bash
# un-heist resume_render.sh — resumable, crash-safe renderer (vertical only).
# Lock-guarded, skips existing frames, atomic writes, recount-from-disk progress.
set -u
PROJ="/home/hatch/workspace/silent-locus/animation/un-heist-that-wasnt"
BUILD="$PROJ/build"; WORK="$PROJ/work"
LOCK="$WORK/render.lock"; PROGRESS="$WORK/render_progress.json"; LOG="$WORK/render.log"

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }

TOTAL="$(python3 "$BUILD/render_un.py" --total-frames)"
log "resume_render start (total_frames=$TOTAL)"

exec 9>"$LOCK"
if ! flock -n 9; then log "lock held; exiting"; exit 0; fi

have() { ls "$WORK/frames_v"/f*.png 2>/dev/null | wc -l; }
update() {
  python3 - "$PROGRESS" "$(have)" "$TOTAL" <<'EOF'
import json, sys
p, v, t = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
json.dump({"vertical": {"done": v, "total": t}}, open(p, "w"), indent=1)
EOF
  log "progress vertical=$(have)/$TOTAL"
}
update
rm -f "$WORK/frames_v"/f*.png.tmp
if [ "$(have)" -lt "$TOTAL" ]; then
  log "rendering vertical"
  if python3 "$BUILD/render_un.py" >>"$LOG" 2>&1; then log "render pass finished";
  else log "render pass exited nonzero (resumable)"; fi
  update
else
  log "already complete"
fi
if [ "$(have)" -ge "$TOTAL" ]; then
  log "frames complete; encoding"
  if bash "$BUILD/encode.sh" >>"$LOG" 2>&1; then
    log "encode ok; verifying"
    if python3 "$BUILD/verify.py" >>"$LOG" 2>&1; then
      log "verify PASS; pipeline done"; touch "$WORK/pipeline_done"
    else log "verify FAILED"; fi
  else log "encode FAILED"; fi
  update
else
  log "incomplete: $(have)/$TOTAL"
fi
log "resume_render end"
