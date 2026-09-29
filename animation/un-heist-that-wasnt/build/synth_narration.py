#!/usr/bin/env python3
"""UN Heist: synthesize narration phrase-by-phrase, measure each duration,
assemble with fixed gaps, and emit exact phrase timestamps (no guessed timing).
Usage: python3 synth_narration.py
Writes work/narration_clean.wav and work/phrase_times.json
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent / "work"
PHRASES = (HERE / "narration_script.txt").read_text().strip().split("\n\n")
GAP = 0.45  # seconds of silence between phrases
SR = 48000
VOICE = "avocado_v2:MAI_03"


def run(*a):
    subprocess.run(a, check=True)


def dur(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True,
        check=True)
    return float(r.stdout.strip())


def main():
    chunks = []
    times = []
    t = 0.0
    for i, ph in enumerate(PHRASES):
        mp3 = WORK / f"phrase_{i:02d}.mp3"
        wav = WORK / f"phrase_{i:02d}.wav"
        if not mp3.exists():
            # write phrase via stdin heredoc-equivalent (no shell quoting issues)
            p = subprocess.run(
                ["/opt/hatch/bin/tts", "speak", "--voice", VOICE,
                 "--output", str(mp3), "--text-stdin"],
                input=ph.encode(), capture_output=True)
            if p.returncode != 0:
                print(p.stderr.decode()[-2000:], file=sys.stderr)
                sys.exit(1)
        run("ffmpeg", "-v", "error", "-y", "-i", str(mp3),
            "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(wav))
        d = dur(wav)
        times.append({"phrase": ph, "start": round(t, 3), "dur": round(d, 3)})
        chunks.append(wav)
        t += d + GAP
        print(f"phrase {i}: start={times[-1]['start']:.2f}s dur={d:.2f}s", flush=True)

    total = t - GAP
    print(f"narration total: {total:.2f}s")
    # assemble: concat with silence gaps
    lst = WORK / "concat_list.txt"
    sil = WORK / "gap.wav"
    run("ffmpeg", "-v", "error", "-y", "-f", "lavfi",
        "-i", f"anoisesrc=d={GAP}:c=brown:r={SR}:a=0.0",
        "-t", str(GAP), "-ac", "2", "-c:a", "pcm_s16le", str(sil))
    with open(lst, "w") as f:
        for i, c in enumerate(chunks):
            f.write(f"file '{c}'\n")
            if i < len(chunks) - 1:
                f.write(f"file '{sil}'\n")
    out = WORK / "narration_clean.wav"
    run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
        "-i", str(lst), "-c:a", "pcm_s16le", str(out))
    print(f"wrote {out}: {dur(out):.2f}s")
    (WORK / "phrase_times.json").write_text(
        json.dumps({"gap": GAP, "total": round(total, 3), "phrases": times},
                   indent=1))
    print("wrote phrase_times.json")


if __name__ == "__main__":
    sys.exit(main())
