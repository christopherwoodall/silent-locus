#!/usr/bin/env bash
# SILENT LOCUS audio: dark cinematic underscore + narration mix.
# Bed is SUBTLE: -18 to -22 dB under narration. Never masks words.
set -e
cd "$(dirname "$0")/../work"
FF="ffmpeg -v error -y"

# --- bed segment 1: 0-16s, low drone, gentle fade in ---
$FF -f lavfi -i "sine=frequency=55:duration=16" \
    -f lavfi -i "sine=frequency=82.4:duration=16" \
    -f lavfi -i "anoisesrc=d=16:c=pink:r=48000" \
    -filter_complex "[0]volume=0.30[a];[1]volume=0.20[b];[2]lowpass=f=220,volume=0.08[c];[a][b][c]amix=3,afade=t=in:st=0:d=2.5[s1]" \
    -map "[s1]" bed1.wav

# --- bed segment 2: 16-40s, drone + 60BPM pulse + noise riser into the heist (16-20s) ---
$FF -f lavfi -i "sine=frequency=55:duration=24" \
    -f lavfi -i "sine=frequency=82.4:duration=24" \
    -f lavfi -i "anoisesrc=d=24:c=pink:r=48000" \
    -f lavfi -i "anoisesrc=d=4:c=white:r=48000" \
    -filter_complex "[0]volume=0.30[a];[1]volume=0.20[b];[a][b]amix=2,tremolo=f=1:d=0.55[p];[2]lowpass=f=240,volume=0.08[n];[3]bandpass=f=2400,afade=t=in:st=0:d=3.8:curve=cbr,volume=0.22[r];[p][n][r]amix=3[s2]" \
    -map "[s2]" bed2.wav

# --- bed segment 3: 40-60s, darker drone, pulse eases off ---
$FF -f lavfi -i "sine=frequency=55:duration=20" \
    -f lavfi -i "sine=frequency=65.4:duration=20" \
    -f lavfi -i "anoisesrc=d=20:c=pink:r=48000" \
    -filter_complex "[0]volume=0.30[a];[1]volume=0.18[b];[2]lowpass=f=200,volume=0.08[c];[a][b][c]amix=3[s3]" \
    -map "[s3]" bed3.wav

# --- bed segment 4: 60-68s, somber resolve under end card + sting, fade out ---
$FF -f lavfi -i "sine=frequency=55:duration=8" \
    -f lavfi -i "sine=frequency=110:duration=8" \
    -filter_complex "[0]volume=0.28[a];[1]volume=0.10[b];[a][b]amix=2,afade=t=out:st=5:d=3[s4]" \
    -map "[s4]" bed4.wav

printf "file 'bed1.wav'\nfile 'bed2.wav'\nfile 'bed3.wav'\nfile 'bed4.wav'\n" > bedlist.txt
$FF -f concat -safe 0 -i bedlist.txt -c:a pcm_s16le bed_raw.wav
$FF -i bed_raw.wav -af "volume=0.5" bed.wav

# --- final mix: narration full, bed at ~-18dB under it ---
$FF -i narration_clean.wav -i bed.wav \
    -filter_complex "[1]volume=0.14[bed];[0][bed]amix=inputs=2:duration=longest:dropout_transition=0,alimiter=limit=0.95[a]" \
    -map "[a]" -c:a aac -b:a 160k -ar 48000 final_audio.m4a

echo "audio done:"; ffprobe -v error -show_entries format=duration -of csv=p=0 final_audio.m4a
