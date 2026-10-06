#!/usr/bin/env python3
"""un-heist-that-wasnt verify.py — idempotent verification of the finished mp4.
Rebuilt 2026-10-05 after a VM restart wiped build/ scripts (mp4 intact)."""
import json, os, subprocess, sys

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_MP4 = f"{PROJ}/un-heist-v1-vertical.mp4"
REL_MP4 = "animation/un-heist-that-wasnt/un-heist-v1-vertical.mp4"
TOTAL_F = 1680
EXP_DUR = TOTAL_F / 24.0

def probe(*args):
    r = subprocess.run(["ffprobe", "-v", "error", *args, PATH_MP4],
                       capture_output=True, text=True)
    return r.stdout.strip()

info = {"path": REL_MP4, "exists": os.path.exists(PATH_MP4)}
ok = info["exists"]
if ok:
    info["size_mb"] = round(os.path.getsize(PATH_MP4) / 1e6, 1)
    info["duration"] = float(probe("-show_entries", "format=duration",
                                  "-of", "csv=p=0") or 0)
    info["vcodec"] = probe("-select_streams", "v:0", "-show_entries",
                           "stream=codec_name", "-of", "csv=p=0")
    info["acodec"] = probe("-select_streams", "a:0", "-show_entries",
                           "stream=codec_name", "-of", "csv=p=0")
    wh = probe("-select_streams", "v:0", "-show_entries", "stream=width,height",
               "-of", "csv=p=0").split(",")
    try:
        info["width"], info["height"] = int(wh[0]), int(wh[1])
        fps = probe("-select_streams", "v:0", "-show_entries",
                    "stream=r_frame_rate", "-of", "csv=p=0")
        n, d = fps.split("/"); info["fps"] = round(int(n) / int(d), 2)
    except (ValueError, IndexError):
        info["width"] = info["height"] = info["fps"] = 0
    checks = [
        abs(info["duration"] - EXP_DUR) < 1.5,
        info["vcodec"] == "h264", info["acodec"] == "aac",
        info["width"] == 1080, info["height"] == 1920,
        abs(info["fps"] - 24) < 0.1,
    ]
    info["expected_duration"] = round(EXP_DUR, 2)
    info["pass"] = all(checks)
    ok = info["pass"]
else:
    info["pass"] = False

json.dump(info, open(f"{PROJ}/work/verify.json", "w"), indent=1)
print(json.dumps(info, indent=1))
sys.exit(0 if ok else 1)
