#!/bin/bash
# encode.sh — idempotent encode of both cuts.
# Skips a cut whose mp4 already exists and verifies (duration ~68s, H.264 + AAC).
set -u
ANIM="/home/hatch/workspace/silent-locus/animation"
WORK="$ANIM/work"
AUD="$WORK/final_audio.m4a"

ok_mp4() { # $1 = path -> 0 if valid
  [ -f "$1" ] || return 1
  dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1" 2>/dev/null)"
  [ -z "$dur" ] && return 1
  python3 -c "import sys; sys.exit(0 if abs(float('$dur')-68.0) < 1.0 else 1)" || return 1
  v="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$1")"
  a="$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$1")"
  [ "$v" = "h264" ] && [ "$a" = "aac" ]
}

enc() { # $1=cut(v|l) $2=WxH $3=out
  local tag="$1" res="$2" out="$3"
  if ok_mp4 "$out"; then echo "skip $out (already valid)"; return 0; fi
  echo "encoding $out"
  ffmpeg -y -v error -framerate 24 -i "$WORK/chibi_$tag/f%05d.png" -i "$AUD" \
    -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium \
    -c:a aac -b:a 160k -ar 48000 -ac 2 -movflags +faststart \
    -t 68 "$out" && ok_mp4 "$out"
}

enc v 1080x1920 "$ANIM/swarm-locus-v1-vertical.mp4" || exit 1
enc l 1920x1080 "$ANIM/swarm-locus-v1-landscape.mp4" || exit 1
echo "encode done"
