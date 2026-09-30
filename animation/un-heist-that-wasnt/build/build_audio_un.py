#!/usr/bin/env python3
"""UN HEIST audio: bright chibi underscore + narration mix.
Same recipe as build_audio_chibi.py (warm major-key pad, pentatonic plucks,
soft shaker), sized to the measured narration length. Narration stays full
and forward; bed sits ~-18 dB under it. Output: work/final_audio_un.m4a.
Usage: python3 build_audio_un.py
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve()
WORK = HERE.parent.parent / "work"
SR = 48000

C3, G3 = 130.81, 196.00
C4, E4, G4 = 261.63, 329.63, 392.00
PENTA = {"C5": 523.25, "D5": 587.33, "E5": 659.26,
         "G5": 783.99, "A5": 880.00, "C6": 1046.50}
MOTIF = ["C5", "D5", "E5", "G5", "A5", "G5", "E5", "D5"]
RESOLVE = ["E5", "G5", "A5", "C6"]
rng = np.random.default_rng(0xBEEF)

pt = json.loads((WORK / "phrase_times.json").read_text())
NARR = pt["total"]
DUR = NARR + 2.0   # narration + sting tail
N = int(SR * DUR)

def fade_env(n, attack, release):
    env = np.ones(n)
    a = max(1, int(attack * SR)); r = max(1, int(release * SR))
    t = np.linspace(0, 1, a); env[:a] = t * t * (3 - 2 * t)
    t = np.linspace(0, 1, r)
    env[-r:] = (1 - t) * (1 - t) * (3 - 2 * (1 - t))
    return env

def add_pluck(L, R, t0, freq, gain, pan):
    dlen = int(1.4 * SR); start = int(t0 * SR)
    if start >= N: return
    end = min(N, start + dlen)
    tt = np.arange(end - start) / SR
    decay = np.exp(-tt / 0.38); atk = np.minimum(1.0, tt / 0.006)
    wave = (np.sin(2 * np.pi * freq * tt)
            + 0.30 * np.sin(2 * np.pi * 2 * freq * tt) * np.exp(-tt / 0.18)
            + 0.10 * np.sin(2 * np.pi * 3 * freq * tt) * np.exp(-tt / 0.10))
    wave *= gain * decay * atk
    gl = np.cos((pan + 1) * np.pi / 4); gr = np.sin((pan + 1) * np.pi / 4)
    L[start:end] += wave * gl; R[start:end] += wave * gr

def main():
    t = np.arange(N) / SR
    L = np.zeros(N); R = np.zeros(N)
    for f, g in [(C3, 0.050), (G3, 0.045), (C4, 0.040), (E4, 0.035), (G4, 0.020)]:
        for sig, det in ((L, -0.12), (R, +0.12)):
            sig += g * (np.sin(2 * np.pi * (f + det) * t)
                        + 0.18 * np.sin(2 * np.pi * 2 * (f + det) * t))
    env = fade_env(N, attack=4.0, release=3.5)
    L *= env; R *= env
    # plucks: playful through the debunk, resolving at the sting
    mid = NARR - 6.0
    stretches = [(1.0, 16.0, 2.0, 0.110), (16.0, mid, 0.55, 0.180),
                 (mid, NARR, 1.0, 0.130)]
    for t0, t1, step, gain in stretches:
        n = int((t1 - t0) / step)
        for i in range(n):
            tt = t0 + i * step + rng.uniform(-0.010, 0.010)
            add_pluck(L, R, tt, PENTA[MOTIF[i % len(MOTIF)]],
                      gain * rng.uniform(0.9, 1.1),
                      0.18 if i % 2 == 0 else -0.18)
    for i, note in enumerate(RESOLVE):
        add_pluck(L, R, NARR + 0.4 + i * 0.5, PENTA[note], 0.150, 0.0)
    # shaker 12s -> NARR
    noise = rng.standard_normal(N)
    k = int(SR / 9000)
    smooth = np.convolve(noise, np.ones(k) / k, mode="same")
    hp = noise - smooth
    trem = 0.55 + 0.45 * np.sin(2 * np.pi * 4.0 * t) ** 2
    s = hp * trem * 0.016
    gate = np.zeros(N); g0, g1 = int(12 * SR), int(NARR * SR)
    gate[g0:g1] = 1.0
    a = int(3 * SR)
    gate[g0:g0 + a] = np.linspace(0, 1, a)
    gate[g1 - a:g1] = np.linspace(1, 0, a)
    s *= gate; L += s; R += s

    stereo = np.stack([L, R], axis=1)
    stereo *= 0.42 / max(np.max(np.abs(stereo)), 1e-9)
    f = int(0.5 * SR); stereo[:f] *= np.linspace(0, 1, f)[:, None]
    f2 = int(2.5 * SR); stereo[-f2:] *= np.linspace(1, 0, f2)[:, None]
    bed = WORK / "bed_un.wav"
    import wave
    with wave.open(str(bed), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(stereo, -1, 1) * 32767).astype(np.int16).tobytes())
    print(f"bed: {DUR:.1f}s")

    out = WORK / "final_audio_un.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y",
                    "-i", str(WORK / "narration_clean.wav"), "-i", str(bed),
                    "-filter_complex",
                    "[0]aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo[nar];"
                    "[1]volume=0.126[bed];"
                    "[nar][bed]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
                    "alimiter=limit=0.95[a]",
                    "-map", "[a]", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    str(out)], check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", str(out)],
                       capture_output=True, text=True, check=True)
    print(f"mix: {r.stdout.strip()}s -> {out.name}")

if __name__ == "__main__":
    sys.exit(main())
