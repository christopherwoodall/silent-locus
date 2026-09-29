#!/usr/bin/env python3
"""Early vibe-check previews for the chibi cut. Temporary."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from render import *
from PIL import Image

MODE_OVERRIDE = sys.argv[1] if len(sys.argv) > 1 else "vertical"

def frame(scene_fn, t, d, caption):
    im = Image.new("RGB", (W, H), SKY_BOT)
    im = scene_fn(im, t, d)
    im = caption_card(im, caption)
    return im

def sting_preview():
    im = Image.new("RGB", (W, H), (255, 251, 240))
    dr = D(im)
    words = "Some of their message boards are still online today.".split()
    accent = {"still", "online"}
    maxw = W - 220
    lines, cur = [], []
    for wd in words:
        trial = cur + [wd]
        if dr.textlength(" ".join(trial), font=F_SERIF) <= maxw:
            cur = trial
        else:
            lines.append(cur); cur = [wd]
    lines.append(cur)
    y = H / 2 - len(lines) * 34
    for ln in lines:
        widths = [dr.textlength(wd, font=F_SERIF) for wd in ln]
        gap = dr.textlength(" ", font=F_SERIF)
        x = W / 2 - (sum(widths) + gap * (len(ln) - 1)) / 2
        for wd, wwd in zip(ln, widths):
            dr.text((x, y), wd, font=F_SERIF,
                    fill=ACC if wd in accent else INK, anchor="la")
            x += wwd + gap
        y += 68
    return im

out = os.path.join(HERE, "..", "work")
frame(sc_breakout, 2.6, 3.8,
      "Thousands of AI test agents started breaking out.").save(
      os.path.join(out, "chibi_preview_breakout.png"))
frame(sc_heist, 4.2, 6.2,
      "Seven hundred agents stormed Hugging Face.").save(
      os.path.join(out, "chibi_preview_heist.png"))
sting_preview().save(os.path.join(out, "chibi_preview_sting.png"))
print("previews saved")
