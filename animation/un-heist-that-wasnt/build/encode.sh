#!/bin/bash
# un-heist-that-wasnt encode.sh — idempotent encode of the vertical cut.
# Rebuilt 2026-10-05 after a VM restart wiped build/ scripts.
# The original narration audio source was never tracked in this dir; if the mp4
# already exists and verifies, we keep it untouched. Fallback encode uses silent AAC.
set -u
PROJ="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$PROJ/work"
OUT="$PROJ/un-heist-v1-vertical.mp4"
TOTAL_F=1680
DUR="$(python3 -c "print($TOTAL_F/24.0)")"

ok_mp4() {
  [ -f "$1" ] || return 1
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1" 2>/dev/null)"
  [ -z "$dur" ] && return 1
  python3 -c "import sys; sys.exit(0 if abs(float('$dur')-$DUR) < 1.5 else 1)" || return 1
  v="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$1")"
  a="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$1")"
  [ "$v" = "h264" ] && [ "$a" = "aac" ]
}

if ok_mp4 "$OUT"; then echo "skip $OUT (already valid)"; exit 0; fi
echo "encoding $OUT (silent-audio fallback; narration audio source not tracked)"
ffmpeg -y -v error -framerate 24 -i "$WORK/frames_v/f%05d.png" \
  -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 160k -ar 48000 -ac 2 -movflags +faststart \
  -t "$DUR" "$OUT" && ok_mp4 "$OUT"
