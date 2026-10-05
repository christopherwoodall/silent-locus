#!/usr/bin/env python3
"""THE UN HEIST THAT WASN'T — vertical chibi debunk, 1080x1920.
Reuses the chibi primitives from ../../build/render.py (same cute look),
with a dithered sky (kills the gradient banding seen in the last cut).
Caption hard rule: measured + wrapped/shrunk to fit INSIDE the card.
Usage: python3 render_un.py   (FRAMES="a-b" for ranges, --total-frames)
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "build"))
import render as R

W, H, FPS = 1080, 1920, 24
FRDIR = os.path.join(HERE, "..", "work", "frames_v")

# ---------- dithered sky (banding fix) ----------
_SKY2 = None
def sky2(im, t):
    global _SKY2
    if _SKY2 is None:
        _SKY2 = Image.new("RGB", (W, H))
        dr0 = R.D(_SKY2)
        for y in range(0, H, 2):
            dr0.line([(0, y), (W, y)],
                     fill=R.lerp(R.SKY_TOP, R.SKY_BOT, y / H))
        rng = np.random.default_rng(0xBEEF)
        arr = np.asarray(_SKY2).astype(np.int16)
        arr += rng.integers(-2, 3, arr.shape, dtype=np.int16)
        _SKY2 = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    im.paste(_SKY2, (0, 0))
    sx, sy = W * 0.82, H * 0.10
    def glow(d):
        for r, a in ((170, 45), (125, 70)):
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 232, 160, a))
    im2 = R.overlay(im, glow)
    dr = R.D(im2)
    dr.ellipse([sx - 80, sy - 80, sx + 80, sy + 80], fill=R.SUN)
    return im2

R.sky = sky2  # base_bg() picks this up

# ---------- text fitting ----------
def fit_lines(dr, text, max_w, start=64, min_s=30, path=None):
    path = path or (R.FD + "DejaVuSerif-Bold.ttf")
    size = start
    while size > min_s:
        font = ImageFont.truetype(path, size)
        words, lines, cur = text.split(), [], ""
        for wd in words:
            t2 = (cur + " " + wd).strip()
            if dr.textlength(t2, font=font) <= max_w:
                cur = t2
            else:
                lines.append(cur); cur = wd
        lines.append(cur)
        if all(dr.textlength(l, font=font) <= max_w for l in lines):
            return font, lines, size
        size -= 4
    font = ImageFont.truetype(path, min_s)
    return font, [text], min_s

NEWS_RED = (205, 70, 70)

# ================= SCENES =================
def sc_headline(im, t, d):
    im = R.base_bg(im, t)
    dr = R.D(im)
    # newsprint card
    x0, x1 = 80, W - 80
    y0, y1 = int(R.SH * 0.16), int(R.SH * 0.66)
    def sh(dd):
        dd.rounded_rectangle([x0 + 8, y0 + 12, x1 + 8, y1 + 12], radius=36,
                             fill=(90, 110, 140, 55))
    im = R.overlay(im, sh); dr = R.D(im)
    dr.rounded_rectangle([x0, y0, x1, y1], radius=36, fill=(250, 247, 240),
                         outline=R.SOFT_LN, width=4)
    im = R.pill(im, W / 2, y0 + 62, "BREAKING", bg=NEWS_RED, fg=R.WHITE)
    font, lines, _ = fit_lines(dr, "AI agents hack UN website — 16,000 times",
                               x1 - x0 - 110, start=72)
    y = y0 + 170
    for ln in lines:
        R.txt(dr, (W / 2, y), ln, font=font, fill=R.INK, anchor="mm")
        y += int(font.size * 1.28)
    R.txt(dr, (W / 2, y1 - 70), "every outlet · Sep 28, 2026", font=R.F_MONO,
          fill=R.INK_SOFT, anchor="mm")
    # shocked blobs
    for i, c in enumerate((R.B_PINK, R.B_BLUE)):
        bx = W * (0.24 + i * 0.52)
        im = R.blob(im, bx, y1 + 150 + math.sin(t * 3 + i) * 14, 62, c, t,
                    seed=200 + i)
        R.txt(R.D(im), (bx, y1 + 40), "!", font=R.F_TITLE, fill=NEWS_RED,
              anchor="mm")
    return R.kicker(im, "2026-09-28", "the headlines")

def sc_chain(im, t, d):
    im = R.base_bg(im, t)
    dr = R.D(im)
    nodes = [("X post", "Clash Report · Sep 28"),
             ("WSJ", "Sep 27"),
             ("one blog post", "swarmcha.se · Sep 26")]
    y = int(R.SH * 0.16)
    for i, (title, sub) in enumerate(nodes):
        on = t > i * 0.5
        if not on:
            continue
        w2 = 560 if i < 2 else 640
        col = R.WHITE if i < 2 else (255, 243, 224)
        dr.rounded_rectangle([W / 2 - w2 / 2, y, W / 2 + w2 / 2, y + 150],
                             radius=36, fill=col, outline=R.SOFT_LN, width=4)
        R.txt(dr, (W / 2, y + 58), title, font=R.F_SERIF, fill=R.INK, anchor="mm")
        R.txt(dr, (W / 2, y + 108), sub, font=R.F_MONO, fill=R.INK_SOFT,
              anchor="mm")
        if i < 2:
            R.txt(dr, (W / 2, y + 196), "▼", font=R.F_SANS, fill=R.INK_SOFT,
                  anchor="mm")
        y += 240
    # the number, deflating
    p = min(1.0, max(0.0, (t - 1.2) / 1.0))
    if p > 0:
        ny = int(R.SH * 0.80)
        R.txt(dr, (W / 2, ny), "16,500", font=R.F_COUNT, fill=R.INK, anchor="mm")
        lw = dr.textlength("16,500", font=R.F_COUNT)
        dr.line([(W / 2 - lw / 2, ny), (W / 2 + lw / 2 * p, ny)],
                fill=NEWS_RED, width=12)
        if p >= 1:
            R.txt(dr, (W / 2, ny + 110), "scan sessions · mostly failures",
                  font=R.F_MONO, fill=R.INK_SOFT, anchor="mm")
    im = R.blob(im, W * 0.85, R.SH * 0.52, 58, R.B_YEL, t, seed=210)
    mgx, mgy = W * 0.85 + 70, R.SH * 0.52 - 50
    dr = R.D(im)
    dr.ellipse([mgx - 52, mgy - 52, mgx + 52, mgy + 52], outline=R.CAGE_D,
               width=12)
    dr.line([(mgx + 38, mgy + 38), (mgx + 96, mgy + 96)], fill=R.CAGE_D, width=14)
    return R.kicker(im, "the source chain", "one blog post")

def sc_trace(im, t, d):
    im = R.base_bg(im, t, clouds=False)
    dr = R.D(im)
    im = R.pill(im, W / 2, 110, "our trace · Apr 21 → Jun 21 · ~3,653 relayed")
    rows = [("httpbin", 3215), ("httpbun", 216), ("r.jina.ai", 194),
            ("dagd", 24), ("allorigins", 4)]
    y = int(R.SH * 0.21)
    for i, (label, v) in enumerate(rows):
        if t < 0.3 + i * 0.25:
            continue
        p = min(1.0, (t - 0.3 - i * 0.25) / 0.5)
        bw = int((W - 420) * (v / 3215) * p)
        R.txt(dr, (90, y + 24), label, font=R.F_MONO, fill=R.INK,
              anchor="lm")
        dr.rounded_rectangle([330, y, 330 + max(bw, 10), y + 48], radius=24,
                             fill=R.BLOBS[i % 6])
        R.txt(dr, (W - 90, y + 24), f"{v:,}", font=R.F_MONO, fill=R.INK,
              anchor="rm")
        y += 82
    # flow: agent -> cloud -> UN building
    fy = int(R.SH * 0.70)
    R.txt(dr, (W / 2, fy - 170), "the GET→POST bridge", font=R.F_SERIF,
          fill=R.INK, anchor="mm")
    im = R.blob(im, 170, fy, 64, R.B_BLUE, t, seed=220)
    im = R.cloud(im, W / 2, fy - 10, 1.1, t)
    dr = R.D(im)
    bx, by = W - 170, fy
    dr.rounded_rectangle([bx - 110, by - 90, bx + 110, by + 70], radius=30,
                         fill=(235, 200, 160))
    dr.ellipse([bx - 120, by - 118, bx + 120, by - 62], fill=(245, 215, 175))
    for ci in range(3):
        cx2 = bx - 56 + ci * 56
        dr.rectangle([cx2 - 20, by - 60, cx2 + 20, by + 10], fill=(200, 170, 130))
    for ax, ex in ((262, 408), (672, 762)):
        q = (t * 1.2) % 1.0
        dr.line([(ax, fy), (ex, fy)], fill=R.INK_SOFT, width=8)
        dr.polygon([(ex, fy - 16), (ex, fy + 16), (ex + 26, fy)],
                   fill=R.INK_SOFT)
        px = ax + (ex - ax) * q
        dr.ellipse([px - 12, fy - 12, px + 12, fy + 12], fill=R.ACC)
    for lx, lab in ((170, "agent"), (W / 2, "trusted relay"),
                    (bx, "UNCTADstat API")):
        R.txt(dr, (lx, fy + 122), lab, font=R.F_MONO, fill=R.INK,
              anchor="mm")
    return im

def sc_trick(im, t, d):
    im = R.base_bg(im, t, clouds=False)
    dr = R.D(im)
    R.txt(dr, (W / 2, int(R.SH * 0.12)), "the trick, simply",
          font=R.F_SERIF, fill=R.INK, anchor="mm")
    fy = int(R.SH * 0.40)
    # agent with a question mark
    im = R.blob(im, 170, fy, 70, R.B_PEACH, t, seed=230)
    im = R.chat_bubble(im, 170, fy - 195, 150, 100, "?")
    # relay cloud
    im = R.cloud(im, W / 2, fy, 1.2, t)
    # server building
    dr = R.D(im)
    bx, by = W - 170, fy
    dr.rounded_rectangle([bx - 110, by - 90, bx + 110, by + 70], radius=30,
                         fill=(235, 200, 160))
    dr.ellipse([bx - 120, by - 118, bx + 120, by - 62], fill=(245, 215, 175))
    for ci in range(3):
        cx2 = bx - 56 + ci * 56
        dr.rectangle([cx2 - 20, by - 60, cx2 + 20, by + 10], fill=(200, 170, 130))
    # envelope traveling agent -> cloud -> server (never overlapping ends)
    q = (t * 0.45) % 1.0
    if q < 0.5:
        x = 262 + (408 - 262) * (q * 2)
    else:
        x = 672 + (762 - 672) * ((q - 0.5) * 2)
    y = fy - 40 * math.sin(q * math.pi)
    ew, eh = 92, 64
    dr.rounded_rectangle([x - ew / 2, y - eh / 2, x + ew / 2, y + eh / 2],
                         radius=12, fill=R.WHITE, outline=R.INK_SOFT, width=4)
    dr.line([(x - ew / 2, y - eh / 2), (x, y + 6),
             (x + ew / 2, y - eh / 2)], fill=R.INK_SOFT, width=4)
    for lx, lab in ((170, "agent"), (W / 2, "trusted relay"), (bx, "server")):
        R.txt(dr, (lx, fy + 122), lab, font=R.F_MONO, fill=R.INK,
              anchor="mm")
    R.txt(dr, (W / 2, int(R.SH * 0.60)), "blocked GET → smuggled in as a form POST",
          font=R.F_MONO, fill=NEWS_RED, anchor="mm")
    R.txt(dr, (W / 2, int(R.SH * 0.68)), "evasive? yes.   a hack? no.",
          font=R.F_SERIF, fill=R.INK, anchor="mm")
    return R.kicker(im, "how it worked", "GET→POST bridge")

def sc_key(im, t, d):
    im = R.base_bg(im, t)
    dr = R.D(im)
    kx, ky = W / 2, int(R.SH * 0.36)
    wig = math.sin(t * 2) * 8
    kr = 110
    dr.ellipse([kx - kr + wig, ky - kr, kx + kr + wig, ky + kr],
               outline=R.SUN, width=34)
    dr.line([(kx + kr * 0.7 + wig, ky + kr * 0.7),
             (kx + kr * 0.7 + wig, ky + kr * 2.4)], fill=R.SUN, width=34)
    dr.line([(kx + kr * 0.7 + wig, ky + kr * 1.5),
             (kx + kr * 0.7 + 70 + wig, ky + kr * 1.5)], fill=R.SUN, width=26)
    dr.line([(kx + kr * 0.7 + wig, ky + kr * 2.0),
             (kx + kr * 0.7 + 70 + wig, ky + kr * 2.0)], fill=R.SUN, width=26)
    im = R.blob(im, W * 0.20, ky + 260, 58, R.B_LAV, t, seed=240)
    im = R.blob(im, W * 0.80, ky + 260, 58, R.B_MINT, t, seed=241)
    # PUBLIC stamp
    if t > 0.5:
        p = min(1.0, (t - 0.5) / 0.3)
        s = 1 + 0.6 * (1 - p)
        fnt = ImageFont.truetype(R.FD + "DejaVuSansMono-Bold.ttf",
                                 int(64 * s))
        dr = R.D(im)
        R.txt(dr, (W / 2, ky - 260), "NOT STOLEN", font=fnt, fill=NEWS_RED,
              anchor="mm")
        tw = dr.textlength("NOT STOLEN", font=fnt)
        dr.rectangle([W / 2 - tw / 2 - 24, ky - 260 - 52,
                      W / 2 + tw / 2 + 24, ky - 260 + 52],
                     outline=NEWS_RED, width=6)
    font, lines, _ = fit_lines(dr, "433468f8…d2bd4 — the site's own public key",
                               W - 220, start=44,
                               path=R.FD + "DejaVuSansMono-Bold.ttf")
    y = int(R.SH * 0.66)
    for ln in lines:
        R.txt(dr, (W / 2, y), ln, font=font, fill=R.INK_SOFT, anchor="mm")
        y += int(font.size * 1.3)
    return R.kicker(im, "the “secret key”", "public by design")

def sc_zeros(im, t, d):
    im = R.base_bg(im, t)
    dr = R.D(im)
    rows = [("SQL injections", "0"), ("non-public data taken", "0"),
            ("service disrupted", "0")]
    y = int(R.SH * 0.22)
    for i, (label, z) in enumerate(rows):
        if t < 0.3 + i * 0.5:
            continue
        p = min(1.0, (t - 0.3 - i * 0.5) / 0.4)
        pop = 1 + 0.5 * (1 - p)
        dr.rounded_rectangle([120, y, W - 120, y + 150], radius=36,
                             fill=R.WHITE, outline=R.SOFT_LN, width=4)
        R.txt(dr, (200, y + 75), z,
              font=ImageFont.truetype(R.FD + "DejaVuSansMono-Bold.ttf",
                                      int(96 * pop)),
              fill=R.ACC, anchor="mm")
        R.txt(dr, (340, y + 75), label, font=R.F_SERIF, fill=R.INK, anchor="lm")
        y += 190
    im = R.blob(im, W * 0.82, int(R.SH * 0.80), 60, R.B_YEL, t, seed=250)
    fn_font = ImageFont.truetype(R.FD + "DejaVuSansMono.ttf", 30)
    R.txt(R.D(im), (W / 2, int(R.SH * 0.635)),
          "primary report: 55 double-encoded probes (May 4–Jun 19)",
          font=fn_font, fill=R.INK, anchor="mm")
    R.txt(R.D(im), (W / 2, int(R.SH * 0.675)), "— none in our local trace",
          font=fn_font, fill=R.INK, anchor="mm")
    return R.kicker(im, "exploitation check", "zero, zero, zero")

def sc_attrib(im, t, d):
    im = R.base_bg(im, t)
    dr = R.D(im)
    im = R.blob(im, W / 2, int(R.SH * 0.34), 84, R.B_BLUE, t, seed=260)
    mgx, mgy = W / 2 + 96, int(R.SH * 0.34) - 60 + math.sin(t * 2) * 12
    dr = R.D(im)
    dr.ellipse([mgx - 64, mgy - 64, mgx + 64, mgy + 64], outline=R.CAGE_D,
               width=14)
    dr.line([(mgx + 46, mgy + 46), (mgx + 116, mgy + 116)], fill=R.CAGE_D,
            width=16)
    im = R.pill(im, W / 2, int(R.SH * 0.56), "“highly likely” OpenAI",
                bg=R.B_YEL, fg=R.INK)
    if t > 0.8:
        im = R.pill(im, W / 2, int(R.SH * 0.64), "≠ proven", bg=R.WHITE,
                    fg=R.INK_SOFT)
    if t > 1.6:
        R.txt(R.D(im), (W / 2, int(R.SH * 0.74)),
              "45 of 54 Azure IPs overlap wiki editors",
              font=R.F_MONO, fill=R.INK_SOFT, anchor="mm")
    return R.kicker(im, "attribution", "likely ≠ proven")

# ================= STING =================
def sting_frame():
    im = Image.new("RGB", (W, H), (255, 251, 240))
    dr = R.D(im)
    segs = [("Fancy curl with", R.INK), ("commitment issues", R.INK),
            ("—", R.INK_SOFT), ("not a third exploit.", R.ACC)]
    y = H / 2 - 90
    for s, col in segs:
        font, lines, _ = fit_lines(dr, s, W - 200, start=72)
        for ln in lines:
            R.txt(dr, (W / 2, y), ln, font=font, fill=col, anchor="mm")
            y += int(font.size * 1.3)
        y += 18
    for i, c in enumerate(R.BLOBS[:5]):
        im = R.blob(im, W * (0.14 + i * 0.18), H - 260, 52, c, 0, seed=270 + i)
    return im

# ================= DRIVER =================
TR = 0.6
TOTAL = 60.0
PHRASE_STARTS = []   # filled from work/phrase_times.json
CAPTIONS = [
    "On September 28th, the headlines screamed: AI agents hacked a UN website — sixteen thousand times.",
    "Follow it back to the source: one blog post. Sixteen thousand counts scan sessions — mostly failures. Not hacks.",
    "In our own data: about 3,600 relayed UN data requests, April to June.",
    "The trick: a GET-to-POST bridge. Questions stuffed into web forms, served through trusted relays.",
    "The “secret key” is the site's own public subscription key — every visitor sends the same one.",
    "Zero SQL injections. Zero stolen data. The UN says nothing was disrupted.",
    "Was it OpenAI's agents? Highly likely — but not proven.",
]
SCENES = [sc_headline, sc_chain, sc_trace, sc_trick, sc_key, sc_zeros,
          sc_attrib]

def load_schedule():
    import json
    global TOTAL, PHRASE_STARTS
    pt = os.path.join(HERE, "..", "work", "phrase_times.json")
    with open(pt) as f:
        data = json.load(f)
    starts = [p["start"] for p in data["phrases"]]
    # audio total + 1s tail, sting covers the rest
    aud = os.path.join(HERE, "..", "work", "final_audio_un.m4a")
    if os.path.exists(aud):
        import subprocess
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", aud],
                           capture_output=True, text=True)
        total = float(r.stdout.strip()) + 1.0
    else:
        total = data["total"] + 5.0
    TOTAL = math.ceil(total)
    PHRASE_STARTS = [max(0.0, s - TR) for s in starts]

def build_sched():
    sched = []
    for fn, st, cap in zip(SCENES, PHRASE_STARTS[:7], CAPTIONS):
        sched.append((fn, st, cap))
    sched.append((None, PHRASE_STARTS[7], ""))
    return sched

def ease_io(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)

def ease_out_back(p):
    c1, c3 = 1.70158, 2.70158
    p = max(0.0, min(1.0, p))
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2

def scene_frame(fn, g, start, dur):
    im = Image.new("RGB", (W, H), R.SKY_BOT)
    return fn(im, g - start, dur)

def render_frame(g, SCHED):
    i = 0
    for k in range(len(SCHED)):
        if g >= SCHED[k][1]:
            i = k
    fn, start, cap = SCHED[i]
    end = SCHED[i + 1][1] if i + 1 < len(SCHED) else TOTAL
    if fn is None:
        return sting_frame()
    if i > 0 and g < start + TR:
        p = (g - start) / TR
        pfn, pstart, pcap = SCHED[i - 1]
        pa = sting_frame() if pfn is None else \
            R.caption_card(scene_frame(pfn, g, pstart, start - pstart),
                           pcap, alpha=1 - ease_io(p))
        b = R.caption_card(scene_frame(fn, g - TR, start, end - start), cap,
                           alpha=ease_io(p))
        e = ease_out_back(p)
        im = pa
        if i % 2 == 1:
            im.paste(b, (int((1 - e) * W), 0))
        else:
            im.paste(b, (0, int((1 - e) * H)))
        return im
    return R.caption_card(scene_frame(fn, g, start, end - start), cap)

if __name__ == "__main__":
    load_schedule()
    SCHED = build_sched()
    total_f = int(TOTAL * FPS)
    if "--total-frames" in sys.argv:
        print(total_f)
        sys.exit(0)
    fr = os.environ.get("FRAMES", "")
    a, b = (int(x) for x in fr.split("-")) if fr else (0, total_f)
    os.makedirs(FRDIR, exist_ok=True)
    skipped = 0
    for f in range(a, min(b, total_f)):
        fp = os.path.join(FRDIR, "f%05d.png" % f)
        if os.path.exists(fp):
            skipped += 1
            continue
        im = render_frame(f / FPS, SCHED)
        tmp = fp + ".tmp"
        im.save(tmp, format="PNG")
        os.rename(tmp, fp)
        if f % 120 == 0:
            print("frame %d/%d" % (f, total_f), flush=True)
    print("done skipped=%d" % skipped, flush=True)
