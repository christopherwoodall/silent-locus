#!/usr/bin/env python3
"""
SILENT LOCUS audio: bright, playful chibi underscore + narration mix.

Replaces the dark cinematic drone (build_audio.sh) with a warm major-key
music bed that fits the cute/playful chibi art style:
  - warm major-key pad (soft sine stack C3/G3/C4/E4/G4, slow attack)
  - cheerful pentatonic plucks (C5 D5 E5 G5 A5 C6), sparse 0-16s,
    playful 16-40s "adventure" stretch, calmer 40-60s, resolving 60-68s
  - very soft shaker (bandpassed noise, gentle tremolo), 14-62s

Narration (animation/work/narration_clean.wav) is LOCKED and stays full and
forward in the mix; the bed sits ~-18 dB under it (volume=0.126), with a
limiter at 0.95 and AAC 160k 48kHz encode to animation/work/final_audio.m4a.

Bed: 68.0s, 48kHz, stereo, 16-bit WAV at animation/work/bed_chibi.wav.

Usage:
    python3 animation/build/build_audio_chibi.py
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
WORK = HERE.parent.parent / "work"
SR = 48000
DUR = 68.0
N = int(SR * DUR)

# ---------------------------------------------------------------- frequencies
C3, G3 = 130.81, 196.00
C4, E4, G4 = 261.63, 329.63, 392.00
PENTA = {  # cheerful pentatonic ladder
    "C5": 523.25, "D5": 587.33, "E5": 659.26,
    "G5": 783.99, "A5": 880.00, "C6": 1046.50,
}
MOTIF = ["C5", "D5", "E5", "G5", "A5", "G5", "E5", "D5"]
RESOLVE = ["E5", "G5", "A5", "C6"]

rng = np.random.default_rng(0xC41B1)  # fixed seed: reproducible bed


def fade_env(n, attack, release):
    """Linear-ish smooth envelope: attack up, release down."""
    env = np.ones(n)
    a = max(1, int(attack * SR))
    r = max(1, int(release * SR))
    t = np.linspace(0, 1, a)
    env[:a] = t * t * (3 - 2 * t)          # smoothstep in
    t = np.linspace(0, 1, r)
    env[-r:] = (1 - t) * (1 - t) * (3 - 2 * (1 - t))  # smoothstep out
    return env


def stereo_pad():
    """Warm major-key pad: soft sine stack, slow attack, full-length."""
    t = np.arange(N) / SR
    parts = [
        (C3, 0.050), (G3, 0.045), (C4, 0.040),
        (E4, 0.035), (G4, 0.020),
    ]
    L = np.zeros(N)
    R = np.zeros(N)
    for f, g in parts:
        # gentle 2nd harmonic for warmth, tiny L/R detune for width
        for sig, det in ((L, -0.12), (R, +0.12)):
            sig += g * (np.sin(2 * np.pi * (f + det) * t)
                        + 0.18 * np.sin(2 * np.pi * 2 * (f + det) * t))
    env = fade_env(N, attack=5.0, release=4.0)  # in 0-5s, out 64-68s
    return L * env, R * env


def add_pluck(L, R, t0, freq, gain, pan):
    """Cheerful pluck: sine + soft harmonics, exponential decay, no click."""
    dlen = int(1.4 * SR)  # decay tail (overlaps next pluck a little)
    start = int(t0 * SR)
    if start >= N:
        return
    end = min(N, start + dlen)
    tt = np.arange(end - start) / SR
    decay = np.exp(-tt / 0.38)                     # ~0.38s time constant
    atk = np.minimum(1.0, tt / 0.006)              # 6ms click-free attack
    wave = (np.sin(2 * np.pi * freq * tt)
            + 0.30 * np.sin(2 * np.pi * 2 * freq * tt) * np.exp(-tt / 0.18)
            + 0.10 * np.sin(2 * np.pi * 3 * freq * tt) * np.exp(-tt / 0.10))
    wave *= gain * decay * atk
    # equal-power pan
    gl = np.cos((pan + 1) * np.pi / 4)
    gr = np.sin((pan + 1) * np.pi / 4)
    L[start:end] += wave * gl
    R[start:end] += wave * gr


def plucks(L, R):
    """Pentatonic pluck timeline across the four story stretches."""
    # (t_start, t_end, spacing, gain)
    stretches = [
        (1.0, 16.0, 2.0, 0.110),   # 0-16s: sparse, waking up
        (16.0, 40.0, 0.5, 0.190),  # 16-40s: playful adventure
        (40.0, 60.0, 1.0, 0.140),  # 40-60s: calmer, curious
    ]
    for t0, t1, step, gain in stretches:
        n = int((t1 - t0) / step)
        for i in range(n):
            t = t0 + i * step + rng.uniform(-0.010, 0.010)
            note = MOTIF[i % len(MOTIF)]
            g = gain * rng.uniform(0.9, 1.1)
            pan = 0.18 if i % 2 == 0 else -0.18  # gentle L/R bounce
            add_pluck(L, R, t, PENTA[note], g, pan)
    # 60-68s: resolving phrase over the end sting, then silence into fade
    for i, note in enumerate(RESOLVE):
        add_pluck(L, R, 60.5 + i * 1.1, PENTA[note], 0.150, 0.0)
    add_pluck(L, R, 64.2, PENTA["C6"], 0.130, 0.0)   # final landing note


def shaker(L, R):
    """Very soft shaker: bandpassed noise, gentle tremolo, 14-62s only."""
    t = np.arange(N) / SR
    noise = rng.standard_normal(N)
    # crude bandpass around ~7kHz: highpass via diff of a smoothed version
    k = int(SR / 9000)
    smooth = np.convolve(noise, np.ones(k) / k, mode="same")
    hp = noise - smooth
    trem = 0.55 + 0.45 * np.sin(2 * np.pi * 4.0 * t) ** 2  # gentle 4Hz wobble
    s = hp * trem * 0.016
    gate = np.zeros(N)
    g0, g1 = int(14 * SR), int(62 * SR)
    gate[g0:g1] = 1.0
    a = int(3 * SR)
    gate[g0:g0 + a] = np.linspace(0, 1, a)
    gate[g1 - a:g1] = np.linspace(1, 0, a)
    s *= gate
    L += s
    R += s


def main():
    L, R = stereo_pad()
    plucks(L, R)
    shaker(L, R)

    stereo = np.stack([L, R], axis=1)
    peak = np.max(np.abs(stereo))
    stereo *= 0.42 / max(peak, 1e-9)          # bed peak ~0.42 pre-mix
    # global safety fades (pad already fades, this guarantees clean edges)
    f = int(0.5 * SR)
    stereo[:f] *= np.linspace(0, 1, f)[:, None]
    f2 = int(3.0 * SR)
    stereo[-f2:] *= np.linspace(1, 0, f2)[:, None]

    bed_path = WORK / "bed_chibi.wav"
    pcm = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
    import wave
    with wave.open(str(bed_path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"bed written: {bed_path} ({N / SR:.1f}s, peak 0.42)")

    # --- mix: narration full + forward, bed tucked ~-18 dB under it ---
    nar = WORK / "narration_clean.wav"
    out = WORK / "final_audio.m4a"
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", str(nar), "-i", str(bed_path),
        "-filter_complex",
        "[0]aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo[nar];"
        "[1]volume=0.126[bed];"
        "[nar][bed]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
        "alimiter=limit=0.95[a]",
        "-map", "[a]", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    print(f"mix written: {out}")

    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(out)],
        capture_output=True, text=True, check=True)
    print(f"final duration: {r.stdout.strip()}s")


if __name__ == "__main__":
    sys.exit(main())
