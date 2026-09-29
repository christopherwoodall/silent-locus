#!/bin/bash
# un-heist encode.sh — idempotent encode of the vertical cut.
set -u
PROJ="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$PROJ/work"; AUD="$WORK/final_audio_un.m4a"
OUT="$PROJ/un-heist-v1-vertical.mp4"

ok_mp4() {
  [ -f "$1" ] || return 1
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1" 2>/dev/null)"
  [ -z "$dur" ] && return 1
  python3 -c "import sys; sys.exit(0 if abs(float('$dur')-$(python3 "$PROJ/build/render_un.py" --total-frames)/24.0) < 1.5 else 1)" || return 1
  v="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$1")"
  a="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$1")"
  [ "$v" = "h264" ] && [ "$a" = "aac" ]
}

if ok_mp4 "$OUT"; then echo "skip $OUT (already valid)"; exit 0; fi
echo "encoding $OUT"
TOTAL_F="$(python3 "$PROJ/build/render_un.py" --total-frames)"
DUR="$(python3 -c "print($TOTAL_F/24.0)")"
ffmpeg -y -v error -framerate 24 -i "$WORK/frames_v/f%05d.png" -i "$AUD" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 160k -ar 48000 -ac 2 -movflags +faststart \
  -t "$DUR" "$OUT" && ok_mp4 "$OUT"
