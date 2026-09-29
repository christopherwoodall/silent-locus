#!/usr/bin/env python3
"""verify.py — idempotent verification of both finished mp4s.
Writes animation/work/verify.json; exits 0 only if everything passes."""
import json, os, subprocess, sys

ANIM = "/home/hatch/workspace/silent-locus/animation"
FILES = {
    "vertical": (f"{ANIM}/swarm-locus-v1-vertical.mp4", 1080, 1920),
    "landscape": (f"{ANIM}/swarm-locus-v1-landscape.mp4", 1920, 1080),
}

def probe(path, *args):
    r = subprocess.run(["ffprobe", "-v", "error", *args, path],
                       capture_output=True, text=True)
    return r.stdout.strip()

results, ok = {}, True
for cut, (path, W, H) in FILES.items():
    info = {"path": path, "exists": os.path.exists(path)}
    if not info["exists"]:
        info["pass"] = False; ok = False; results[cut] = info; continue
    info["size_mb"] = round(os.path.getsize(path) / 1e6, 1)
    info["duration"] = float(probe(path, "-show_entries", "format=duration",
                                   "-of", "csv=p=0") or 0)
    info["vcodec"] = probe(path, "-select_streams", "v:0", "-show_entries",
                           "stream=codec_name", "-of", "csv=p=0")
    info["acodec"] = probe(path, "-select_streams", "a:0", "-show_entries",
                           "stream=codec_name", "-of", "csv=p=0")
    wh = probe(path, "-select_streams", "v:0", "-show_entries",
               "stream=width,height", "-of", "csv=p=0").split(",")
    try:
        info["width"], info["height"] = int(wh[0]), int(wh[1])
        fps = probe(path, "-select_streams", "v:0", "-show_entries",
                    "stream=r_frame_rate", "-of", "csv=p=0")
        n, d = fps.split("/"); info["fps"] = round(int(n) / int(d), 2)
    except (ValueError, IndexError):
        info["width"] = info["height"] = info["fps"] = 0
    checks = [
        abs(info["duration"] - 68.0) < 1.0,
        info["vcodec"] == "h264", info["acodec"] == "aac",
        info["width"] == W and info["height"] == H,
        abs(info["fps"] - 24.0) < 0.1,
        info["size_mb"] < 100,
    ]
    info["pass"] = all(checks)
    ok = ok and info["pass"]
    results[cut] = info

json.dump(results, open(f"{ANIM}/work/verify.json", "w"), indent=1)
print(json.dumps(results, indent=1))
sys.exit(0 if ok else 1)
