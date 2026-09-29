#!/usr/bin/env python3
"""SILENT LOCUS — chibi cut. Cute rounded pastel blob critters, light and fun.
Smooth vector-style shapes at full res, zero pixel blocks. Bouncy transitions.
Caption hard rule: text measured + wrapped/shrunk to fit INSIDE its card with
generous padding; scene action never enters the caption zone.
Usage: python3 render.py [vertical|landscape]  (FRAMES="a-b" for ranges)
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else "vertical"
W, H = (1080, 1920) if MODE == "vertical" else (1920, 1080)
FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
FRDIR = os.path.join(HERE, "..", "work",
                     "chibi_v" if MODE == "vertical" else "chibi_l")

# ---------- pastel palette ----------
SKY_TOP = (214, 235, 248)
SKY_BOT = (245, 250, 255)
SUN     = (255, 223, 130)
HILL1   = (190, 232, 200)
HILL2   = (168, 221, 182)
CLOUD   = (255, 255, 255)
INK     = (58, 64, 85)
INK_SOFT= (110, 118, 140)
ACC     = (255, 123, 107)     # the one accent — payoffs only (coral)
WHITE   = (255, 255, 255)
CARD_BG = (255, 255, 255)
CAGE    = (139, 147, 184)
CAGE_D  = (105, 112, 150)
B_BLUE  = (168, 216, 240); B_PEACH = (245, 201, 168); B_LAV = (201, 184, 240)
B_MINT  = (168, 232, 192); B_PINK  = (240, 168, 192); B_YEL = (250, 224, 150)
BLOBS   = [B_BLUE, B_PEACH, B_LAV, B_MINT, B_PINK, B_YEL]
BLUSH   = (255, 150, 150)
SOFT_LN = (200, 208, 225)

FD = "/usr/share/fonts/truetype/dejavu/"
F_SERIF = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 44)
F_SANS  = ImageFont.truetype(FD + "DejaVuSans.ttf", 30)
F_MONO  = ImageFont.truetype(FD + "DejaVuSansMono-Bold.ttf", 26)
F_COUNT = ImageFont.truetype(FD + "DejaVuSansMono-Bold.ttf", 120)
F_TITLE = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 110)

# caption zone: scene action must stay above CAP_TOP
RESERVE = 400 if MODE == "vertical" else 330
CAP_TOP = H - RESERVE
SH = CAP_TOP - 30  # scene area height

def D(im):
    return ImageDraw.Draw(im)

def txt(dr, xy, s, font=F_SANS, fill=INK, anchor="la"):
    dr.text(xy, s, font=font, fill=fill, anchor=anchor)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def overlay(im, draw_fn):
    """Draw translucent shapes via an RGBA overlay composited onto im."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(ov))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

# ---------- background ----------
_SKY_CACHE = None

def sky(im, t):
    global _SKY_CACHE
    if _SKY_CACHE is None:
        _SKY_CACHE = Image.new("RGB", (W, H))
        dr0 = D(_SKY_CACHE)
        for y in range(0, H, 2):
            dr0.line([(0, y), (W, y)], fill=lerp(SKY_TOP, SKY_BOT, y / H))
    im.paste(_SKY_CACHE, (0, 0))
    sx, sy = W * 0.82, H * 0.10
    def glow(d):
        for r, a in ((170, 45), (125, 70)):
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 232, 160, a))
    im2 = overlay(im, glow)
    dr = D(im2)
    dr.ellipse([sx - 80, sy - 80, sx + 80, sy + 80], fill=SUN)
    return im2

def cloud(im, x, y, s, t):
    dr = D(im)
    x += math.sin(t * 0.3 + y) * 12
    for cx, cy, r in ((x - 55 * s, y + 8 * s, 42 * s), (x, y, 55 * s),
                      (x + 55 * s, y + 8 * s, 42 * s), (x, y + 18 * s, 48 * s)):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CLOUD)
    return im

def hills(im):
    dr = D(im)
    dr.ellipse([-W * 0.3, SH - H * 0.16, W * 0.75, SH + H * 0.30], fill=HILL1)
    dr.ellipse([W * 0.35, SH - H * 0.20, W * 1.35, SH + H * 0.30], fill=HILL2)
    return im

def sparkle(im, x, y, s, color=SUN):
    dr = D(im)
    dr.line([(x - s, y), (x + s, y)], fill=color, width=5)
    dr.line([(x, y - s), (x, y + s)], fill=color, width=5)
    return im

# ---------- the blob ----------
def blob(im, x, y, r, color, t=0.0, seed=0, face=True, squash=0.0):
    """Cute rounded blob critter. squash in -0.2..0.2 for bounce."""
    bob = math.sin(t * 3 + seed) * r * 0.05
    y += bob
    rx, ry = r * (1 + squash), r * (1 - squash)
    def shadow(d):
        d.ellipse([x - rx * 0.9, y + ry * 0.95, x + rx * 0.9, y + ry * 1.15],
                  fill=(90, 110, 140, 60))
    im = overlay(im, shadow)
    dr = D(im)
    dr.ellipse([x - rx, y - ry, x + rx, y + ry], fill=color,
               outline=WHITE, width=max(4, int(r * 0.12)))
    if not face:
        return im
    def hl(d):
        hr = r * 0.22
        d.ellipse([x - rx * 0.55 - hr, y - ry * 0.55 - hr,
                   x - rx * 0.55 + hr, y - ry * 0.55 + hr],
                  fill=(255, 255, 255, 170))
    im = overlay(im, hl)
    dr = D(im)
    ex, ey, er = r * 0.32, -r * 0.08, max(4, r * 0.11)
    for sgn in (-1, 1):
        dr.ellipse([x + sgn * ex - er, y + ey - er,
                    x + sgn * ex + er, y + ey + er], fill=INK)
        dr.ellipse([x + sgn * ex - er * 0.3, y + ey - er * 0.4,
                    x + sgn * ex + er * 0.35, y + ey + er * 0.25], fill=WHITE)
    mr = r * 0.30
    dr.arc([x - mr, y + r * 0.05 - mr * 0.6, x + mr, y + r * 0.05 + mr * 0.6],
           15, 165, fill=INK, width=max(4, int(r * 0.09)))
    br = r * 0.16
    for sgn in (-1, 1):
        dr.ellipse([x + sgn * r * 0.62 - br, y + r * 0.22 - br,
                    x + sgn * r * 0.62 + br, y + r * 0.22 + br], fill=BLUSH)
    return im

def chat_bubble(im, x, y, w, h, text, font=F_SANS, tail=True):
    dr = D(im)
    r = 26
    dr.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2],
                         radius=r, fill=WHITE, outline=SOFT_LN, width=3)
    if tail:
        dr.polygon([(x - 14, y + h / 2 - 4), (x + 14, y + h / 2 - 4),
                    (x, y + h / 2 + 22)], fill=WHITE)
    txt(dr, (x, y), text, font=font, fill=INK, anchor="mm")
    return im

def pill(im, x, y, text, font=F_MONO, bg=WHITE, fg=INK_SOFT):
    dr = D(im)
    w = dr.textlength(text, font=font) + 48
    dr.rounded_rectangle([x - w / 2, y - 26, x + w / 2, y + 26], radius=26, fill=bg)
    txt(dr, (x, y), text, font=font, fill=fg, anchor="mm")
    return im

def kicker(im, date, mag=None):
    im = pill(im, 170, 76, date)
    if mag:
        dr = D(im)
        w = dr.textlength(mag, font=F_MONO) + 48
        im = pill(im, W - 20 - w / 2, 76, mag)
    return im

def counter(im, value, t, t_land, dur=1.4, pos=None):
    """Count-up badge landing exactly on the spoken cue. Coral = payoff."""
    pos = pos or (W / 2, int(SH * 0.42))
    if t < t_land - dur:
        return im
    p = min(1.0, (t - (t_land - dur)) / dur)
    e = 1 - (1 - p) ** 3
    s = f"{int(value * e):,}"
    dr = D(im)
    tw = dr.textlength(s, font=F_COUNT) + 100
    th = 170
    pop = 1 + 0.18 * math.exp(-6 * p) * math.cos(10 * p) if p < 1 else 1.0
    tw, th = tw * pop, th * pop
    dr.rounded_rectangle([pos[0] - tw / 2, pos[1] - th / 2,
                          pos[0] + tw / 2, pos[1] + th / 2],
                         radius=80, fill=WHITE, outline=ACC, width=7)
    txt(dr, pos, s, font=F_COUNT, fill=ACC, anchor="mm")
    return im

# ---------- caption card (hard rule: text always fits inside) ----------
def _caption_card_draw(im, text):
    """White rounded card; text measured, wrapped, shrunk to fit with padding."""
    if not text:
        return im
    mx, pad = 48, 44
    x0, x1 = mx, W - mx
    max_w = x1 - x0 - pad * 2
    size = 46
    font = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", size)
    dr = D(im)
    while size > 30:
        font = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", size)
        words, lines, cur = text.split(), [], ""
        for wd in words:
            t2 = (cur + " " + wd).strip()
            if dr.textlength(t2, font=font) <= max_w:
                cur = t2
            else:
                lines.append(cur); cur = wd
        lines.append(cur)
        lh = int(size * 1.32)
        bh = len(lines) * lh + pad * 2
        if bh <= RESERVE - 96:
            break
        size -= 4
    lh = int(size * 1.32)
    bh = len(lines) * lh + pad * 2
    y1 = H - 48
    y0 = y1 - bh
    # soft shadow
    def sh(d):
        d.rounded_rectangle([x0 + 8, y0 + 10, x1 + 8, y1 + 10], radius=44,
                            fill=(90, 110, 140, 50))
    im = overlay(im, sh)
    dr = D(im)
    dr.rounded_rectangle([x0, y0, x1, y1], radius=44, fill=CARD_BG)
    y = y0 + pad + lh / 2
    for ln in lines:
        txt(dr, (W / 2, y), ln, font=font, fill=INK, anchor="mm")
        y += lh
    return im

def caption_card(im, text, alpha=1.0):
    """Caption card with optional opacity (for transitions)."""
    if not text or alpha <= 0:
        return im
    if alpha >= 1.0:
        return _caption_card_draw(im, text)
    return Image.blend(im, _caption_card_draw(im.copy(), text), alpha)

# ================= SCENES =================
def base_bg(im, t, clouds=True):
    im = sky(im, t)
    if clouds:
        im = cloud(im, W * 0.18, H * 0.16, 1.0, t)
        im = cloud(im, W * 0.72, H * 0.30, 0.8, t + 3)
        im = cloud(im, W * 0.40, H * 0.06, 0.6, t + 7)
    im = hills(im)
    return im

def cage(im, x, y, w, h, open_door=False, t=0):
    dr = D(im)
    dr.rounded_rectangle([x, y, x + w, y + h], radius=60, fill=CAGE)
    dr.rounded_rectangle([x, y, x + w, y + h], radius=60, outline=CAGE_D, width=8)
    n = 6
    for i in range(1, n):
        bx = x + i * w / n
        dr.line([(bx, y + 18), (bx, y + h - 18)], fill=CAGE_D, width=10)
    if open_door:
        # dark doorway inset on the right edge + door panel swung outward
        dr.rounded_rectangle([x + w - 90, y + 30, x + w - 6, y + h - 30],
                             radius=30, fill=(70, 76, 110))
        dr.polygon([(x + w - 14, y + 24), (x + w + 110, y + 90),
                    (x + w + 110, y + h - 90), (x + w - 14, y + h - 24)],
                   fill=CAGE_D, outline=CAGE)
    return im

def sc_title(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    a = min(1.0, t / 0.8)
    yy = SH * 0.34 + (1 - a) * 40
    txt(dr, (W / 2, yy), "Silent locus", font=F_TITLE, fill=INK, anchor="mm")
    if t > 0.9:
        txt(dr, (W / 2, yy + 110), "the escaped evals", font=F_SANS,
            fill=INK_SOFT, anchor="mm")
    for i, c in enumerate(BLOBS[:4]):
        bx = W * (0.2 + i * 0.2)
        im = blob(im, bx, SH - 40 - abs(math.sin(t * 2 + i)) * 30, 46, c, t, seed=i)
    return im

def sc_breakout(im, t, d):
    im = base_bg(im, t)
    cw, ch = W * 0.52, SH * 0.42
    cx, cy = W * 0.30, SH * 0.30
    im = cage(im, cx, cy, cw, ch, open_door=True, t=t)
    brk = max(0.0, min(1.0, (t - 1.0) / 1.2))
    for i in range(14):
        p = ((t * 0.55 + i * 0.13) % 1.4)
        sx, sy = cx + cw * 0.85, cy + ch * 0.55
        ex = W * 0.88 - (i % 4) * 70
        ey = SH - 90 - (i % 3) * 60
        q = min(1.0, p * brk * 1.4)
        x = sx + (ex - sx) * q
        y = sy + (ey - sy) * q - 130 * math.sin(q * 3.14)
        sq = 0.18 * math.cos(q * 3.14 * 2) * q
        im = blob(im, x, y, 40, BLOBS[i % 6], t, seed=i * 7, squash=sq)
    im = kicker(im, "2026-05", "thousands of agents")
    return im

def sc_msgboard(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    sx, sy, sw, shh = W * 0.30, SH * 0.22, W * 0.40, SH * 0.34
    dr.rounded_rectangle([sx, sy, sx + sw, sy + shh], radius=50, fill=B_MINT)
    dr.rounded_rectangle([sx, sy, sx + sw, sy + shh], radius=50,
                         outline=WHITE, width=8)
    for i in range(4):
        ly = sy + 50 + i * 60
        on = (int(t * 2 + i) % 3) != 0
        dr.ellipse([sx + 40, ly, sx + 64, ly + 24],
                   fill=ACC if (on and i == 1) else (WHITE if on else (210, 225, 215)))
    msgs = [("zz", -1), ("hi!", 1), ("shh…", -1), ("70k!", 1)]
    for i, (m, sgn) in enumerate(msgs):
        if t > 0.4 + i * 0.35:
            pop = min(1.0, (t - 0.4 - i * 0.35) / 0.3)
            r = 0.6 + 0.4 * pop
            im = chat_bubble(im, W / 2 + sgn * W * 0.28, SH * (0.16 + i * 0.13),
                             200 * r, 90 * r, m)
    im = blob(im, sx - 60, sy + shh - 30, 52, B_BLUE, t, seed=3)
    im = counter(im, 1200, t, 5.35, pos=(W / 2, int(SH * 0.62)))
    im = counter(im, 70000, t, 6.68, pos=(W / 2, int(SH * 0.80)))
    im = kicker(im, "2026-05-07", "1,200 agents")
    return im

def sc_registry(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    by = SH * 0.62
    dr.rounded_rectangle([40, by, W - 40, by + 70], radius=35, fill=(225, 215, 235))
    for i in range(9):
        x = ((i * 220 + t * 260) % (W + 240)) - 120
        bw2 = 90
        y = by - 60 + math.sin(t * 4 + i) * 8
        dr.rounded_rectangle([x, y, x + bw2, y + 80], radius=18,
                             fill=BLOBS[i % 6])
        dr.line([(x + bw2 / 2, y), (x + bw2 / 2, y + 80)], fill=WHITE, width=10)
        dr.line([(x, y + 40), (x + bw2, y + 40)], fill=WHITE, width=10)
    im = blob(im, W * 0.16, by - 130, 56, B_PEACH, t, seed=5,
              squash=0.15 * math.sin(t * 6))
    im = blob(im, W * 0.84, by - 120, 48, B_LAV, t, seed=9)
    im = counter(im, 2000, t, 3.79, pos=(W / 2, int(SH * 0.30)))
    im = kicker(im, "2026-05-12", "48 hours")
    return im

def sc_wiki(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    bx, by = W * 0.5, SH * 0.55
    for i in range(5):
        w2 = 300 - i * 18
        y = by - i * 62
        wob = math.sin(t * 1.5 + i) * 6
        dr.rounded_rectangle([bx - w2 / 2 + wob, y - 52, bx + w2 / 2 + wob, y],
                             radius=16, fill=BLOBS[(i + 2) % 6])
    im = blob(im, bx + 230, by - 40, 54, B_BLUE, t, seed=4,
              squash=0.12 * math.sin(t * 5))
    # pencil scribble
    px, py = bx + 150, by - 160 + math.sin(t * 5) * 14
    dr.line([(px, py - 60), (px + 26, py - 90)], fill=(245, 180, 120), width=16)
    dr.polygon([(px + 26, py - 90), (px + 44, py - 70), (px + 30, py - 62)],
               fill=INK_SOFT)
    if int(t * 1.6) % 2 == 0:
        im = chat_bubble(im, bx - 260, by - 260, 240, 100, "oops!")
    im = kicker(im, "2026-05-17", "19,913 revisions")
    return im

def sc_tunnels(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    for k in range(3):
        y0 = SH * (0.30 + k * 0.16)
        pts = []
        for s in range(21):
            x = 40 + s * (W - 80) / 20
            y = y0 + 60 * math.sin(s * 0.6 + k * 2)
            pts.append((x, y))
        dr.line(pts, fill=BLOBS[(k + 1) % 6], width=64)
        dr.line(pts, fill=(255, 255, 255, 90), width=20)
    for k in range(3):
        y0 = SH * (0.30 + k * 0.16)
        p = (t * 0.35 + k * 0.33) % 1.0
        s = p * 20
        x = 40 + s * (W - 80) / 20
        y = y0 + 60 * math.sin(s * 0.6 + k * 2)
        im = blob(im, x, y, 40, BLOBS[(k + 3) % 6], t, seed=10 + k,
                  squash=0.2 * math.sin(t * 8 + k))
    im = kicker(im, "2026-06-17", "107 tunnels")
    return im

def sc_heist(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    fx, fy = W / 2, SH * 0.40
    fr = min(W, SH) * 0.20
    wig = math.sin(t * 20) * 6 if t > 0.6 else 0
    dr.rounded_rectangle([fx - fr + wig, fy - fr * 1.15, fx + fr + wig, fy + fr],
                         radius=70, fill=B_YEL)
    dr.ellipse([fx - fr * 0.7 + wig, fy - fr * 1.75, fx + fr * 0.7 + wig,
                fy - fr * 0.55], fill=B_PEACH)
    dr.ellipse([fx - fr * 0.7 + wig, fy - fr * 1.75, fx + fr * 0.7 + wig,
                fy - fr * 0.55], outline=WHITE, width=8)
    er = fr * 0.10
    for sgn in (-1, 1):
        dr.ellipse([fx + sgn * fr * 0.35 - er + wig, fy - fr * 1.30 - er,
                    fx + sgn * fr * 0.35 + er + wig, fy - fr * 1.30 + er], fill=INK)
        dr.ellipse([fx + sgn * fr * 0.35 - er * 0.2 + wig, fy - fr * 1.30 - er * 0.5,
                    fx + sgn * fr * 0.35 + er * 0.45 + wig, fy - fr * 1.30 + er * 0.15],
                   fill=WHITE)
    mr = fr * 0.28
    dr.arc([fx - mr + wig, fy - fr * 1.05 - mr * 0.6, fx + mr + wig,
            fy - fr * 1.05 + mr * 0.6],
           15, 165, fill=INK, width=10)
    for i in range(40):
        a = t * (1.1 + (i % 5) * 0.22) + i * 0.4
        rr = fr * (1.55 + 0.18 * math.sin(t * 1.6 + i))
        x = fx + rr * 1.15 * math.cos(a)
        y = fy + rr * 1.05 * math.sin(a)
        if 60 < x < W - 60 and y < SH - 80:
            im = blob(im, x, y, 34, BLOBS[i % 6], t, seed=20 + i,
                      squash=0.15 * math.sin(t * 7 + i))
    # vault of cookies, off to the side
    vx, vy = W * 0.80, SH * 0.74
    dr.rounded_rectangle([vx - 120, vy - 90, vx + 120, vy + 40], radius=40,
                         fill=(235, 200, 160))
    dr.ellipse([vx - 130, vy - 120, vx + 130, vy - 60], fill=(245, 215, 175))
    for ci in range(3):
        cx2 = vx - 60 + ci * 60
        dr.ellipse([cx2 - 26, vy - 108, cx2 + 26, vy - 56], fill=(160, 110, 70))
        for _ in range(3):
            dr.point([(cx2 + (ci * 37 % 30) - 15, vy - 82 + (ci * 53 % 30) - 15)],
                     fill=(90, 60, 40))
    im = counter(im, 700, t, 1.85, pos=(W / 2, int(SH * 0.16)))
    im = counter(im, 17600, t, 4.61, pos=(W / 2, int(SH * 0.60)))
    im = kicker(im, "2026-07-10", "700 agents")
    return im

def sc_named(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    px, py = W / 2, SH * 0.62
    dr.rounded_rectangle([px - 190, py, px + 190, py + 130], radius=30,
                         fill=CAGE)
    txt(dr, (px, py + 65), "press briefing", font=F_SANS, fill=WHITE, anchor="mm")
    im = blob(im, px, py - 120, 80, B_BLUE, t, seed=30,
              squash=0.1 * math.sin(t * 4))
    for sgn in (-1, 1):
        mx = px + sgn * 130
        dr.line([(mx, py), (mx, py - 110)], fill=INK_SOFT, width=10)
        dr.ellipse([mx - 32, py - 170, mx + 32, py - 106], fill=INK_SOFT)
    if int(t * 2) % 2 == 0:
        for fx2, fy2 in ((px - 320, py - 260), (px + 320, py - 240)):
            im = sparkle(im, fx2, fy2, 34, WHITE)
    hl = ["Hugging Face told the world — Jul 16",
          "OpenAI: our agents did this — Jul 21"]
    for i, h in enumerate(hl):
        im = chat_bubble(im, px, SH * (0.14 + i * 0.12), 560, 84, h,
                         font=F_MONO)
    im = kicker(im, "2026-07-21", "named")
    return im

def sc_reckoning(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    for i in range(min(6, 1 + int(t * 2.2))):
        y = SH * 0.52 - i * 56
        wob = math.sin(t + i) * 8
        pop = min(1.0, (t * 2.2 - i))
        w2 = (300 + pop * 120)
        dr.rounded_rectangle([W / 2 - w2 / 2 + wob, y, W / 2 + w2 / 2 + wob, y + 46],
                             radius=20, fill=WHITE, outline=SOFT_LN, width=3)
        txt(dr, (W / 2 + wob, y + 23), "the swarm files", font=F_MONO,
            fill=INK_SOFT, anchor="mm")
    im = blob(im, W * 0.78, SH * 0.34, 72, B_YEL, t, seed=40)
    mgx, mgy = W * 0.78 + 90, SH * 0.34 - 40 + math.sin(t * 2) * 14
    dr.ellipse([mgx - 70, mgy - 70, mgx + 70, mgy + 70], outline=CAGE_D, width=14)
    dr.line([(mgx + 50, mgy + 50), (mgx + 120, mgy + 120)], fill=CAGE_D, width=18)
    tools = ["zz", "jina", "hook", "epoch"]
    for i, tl in enumerate(tools):
        im = pill(im, W * (0.16 + i * 0.225), SH * 0.82, tl, bg=BLOBS[i % 6],
                  fg=INK)
    im = kicker(im, "2026-09-11", "3,000+ packages exposed")
    return im

def sc_escape(im, t, d):
    im = base_bg(im, t)
    cw, ch = W * 0.56, SH * 0.44
    cx, cy = W * 0.22, SH * 0.28
    im = cage(im, cx, cy, cw, ch, open_door=True, t=t)
    crack = min(1.0, t / 1.4)
    bx = cx + cw * 0.85 - 40 + crack * 260
    by = cy + ch * 0.55
    im = blob(im, bx, by, 64, B_MINT, t, seed=50, squash=0.25 * (1 - crack))
    for i in range(3):
        im = blob(im, W * (0.7 + i * 0.1), SH * (0.5 + i * 0.08), 44,
                  BLOBS[(i + 4) % 6], t, seed=51 + i)
    im = kicker(im, "2026-05-26", "ssrf → internet")
    return im

def sc_health(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    kx, ky = W * 0.5, SH * 0.30
    dr.rounded_rectangle([kx - 170, ky - 120, kx + 170, ky + 120], radius=40,
                         fill=WHITE, outline=SOFT_LN, width=4)
    dr.rounded_rectangle([kx - 36, ky - 80, kx + 36, ky + 80], radius=18, fill=ACC)
    dr.rounded_rectangle([kx - 80, ky - 36, kx + 80, ky + 36], radius=18, fill=ACC)
    for i in range(5):
        bh = (60 + 40 * abs(math.sin(t * 1.4 + i))) * 2.2
        bx = W * 0.22 + i * 150
        dr.rounded_rectangle([bx, SH * 0.78 - bh, bx + 100, SH * 0.78],
                             radius=24, fill=BLOBS[i % 6])
    im = blob(im, W * 0.14, SH * 0.55, 52, B_PINK, t, seed=60)
    im = blob(im, W * 0.86, SH * 0.55, 52, B_BLUE, t, seed=61)
    im = kicker(im, "2026-05-29", "111 of 113 via one proxy")
    return im

def sc_federal(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    bx, by = W * 0.5, SH * 0.52
    dr.rounded_rectangle([bx - 330, by - 60, bx + 330, by + 160], radius=30,
                         fill=WHITE, outline=SOFT_LN, width=4)
    for i in range(5):
        cx2 = bx - 220 + i * 110
        dr.rounded_rectangle([cx2 - 32, by - 200, cx2 + 32, by - 60], radius=16,
                             fill=CAGE)
    dr.pieslice([bx - 200, by - 380, bx + 200, by - 60], 180, 360, fill=CAGE)
    for i in range(6):
        x = W * (0.2 + i * 0.12) + math.sin(t * 2 + i) * 20
        im = blob(im, x, by - 260 - (i % 2) * 40, 40, BLOBS[i % 6], t, seed=70 + i)
    if t < 1.4:
        pg = min(1.0, t / 1.4)
        dr.rounded_rectangle([bx - 150, 120 + pg * 200, bx + 150, 300 + pg * 200],
                             radius=24, fill=WHITE, outline=ACC, width=5)
        txt(dr, (bx, 190 + pg * 200), "June 18", font=F_SANS, fill=ACC, anchor="mm")
    im = kicker(im, "2026-06-18", "83 gems · 1 breach")
    return im

def sc_webwave(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    cx, cy = W / 2, SH * 0.42
    nodes = []
    for k in range(7):
        a = k * 0.9 + t * 0.25
        x = cx + 330 * math.cos(a) * (1.4 if MODE == "vertical" else 2.2)
        y = cy + 260 * math.sin(a)
        nodes.append((x, y))
        for j in range(k):
            dr.line([nodes[j], (x, y)], fill=SOFT_LN, width=5)
    for i, (x, y) in enumerate(nodes):
        if y < SH - 60:
            im = blob(im, x, y, 44, BLOBS[i % 6], t, seed=80 + i)
    im = chat_bubble(im, cx, SH * 0.16, 220, 110, "?!", font=F_TITLE)
    im = kicker(im, "2026-07-07", "215 packages · disputed")
    return im

def sc_cagebreaks(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    dis = min(1.0, t / 1.8)
    for i in range(9):
        bx = W * 0.14 + i * W * 0.09
        if 3 <= i <= 5 and dis > 0.3:
            continue
        lean = dis * 20 * math.sin(i)
        dr.rounded_rectangle([bx - 14 + lean, SH * 0.18, bx + 14 + lean, SH * 0.62],
                             radius=14, fill=CAGE)
    gapx = W * 0.5
    for i in range(6):
        p = min(1.0, t * 0.8 - i * 0.12)
        if p <= 0:
            continue
        x = gapx - 200 + p * 420
        y = SH * 0.4 + p * 160 - 200 * math.sin(p * 3.14)
        if y < SH - 60:
            im = blob(im, x, y, 46, BLOBS[i % 6], t, seed=90 + i,
                      squash=0.2 * math.sin(p * 12))
    im = kicker(im, "2026-07-08", "get-only net · 900 links")
    return im

def sc_pattern(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    mx, my = W / 2, SH * 0.36
    blobs_map = [(0.30, 0.42), (0.44, 0.36), (0.58, 0.44), (0.70, 0.34),
                 (0.38, 0.58), (0.62, 0.60)]
    for i, (fx2, fy2) in enumerate(blobs_map):
        x, y = W * fx2, SH * fy2
        r = 90 + (i % 3) * 22
        dr.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=HILL2,
                   outline=WHITE, width=6)
    n = min(6, 1 + int(t * 1.6))
    pts = [(W * blobs_map[i][0], SH * blobs_map[i][1]) for i in range(n)]
    for i in range(1, len(pts)):
        dr.line([pts[i - 1], pts[i]], fill=ACC, width=8)
    for i, (x, y) in enumerate(pts):
        dr.ellipse([x - 18, y - 18, x + 18, y + 18], fill=ACC,
                   outline=WHITE, width=5)
    im = blob(im, W * 0.82, SH * 0.66, 60, B_YEL, t, seed=100)
    mgx, mgy = W * 0.82 + 80, SH * 0.66 - 60
    dr.ellipse([mgx - 60, mgy - 60, mgx + 60, mgy + 60], outline=CAGE_D, width=12)
    dr.line([(mgx + 44, mgy + 44), (mgx + 110, mgy + 110)], fill=CAGE_D, width=16)
    txt(dr, (W / 2, SH * 0.12), "one hidden playbook", font=F_SERIF, fill=INK,
        anchor="mm")
    im = kicker(im, "2026-09-29", "127,330 events")
    return im

def sc_stillonline(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    for i in range(3):
        wx = W * (0.16 + i * 0.27)
        wy = SH * (0.22 + (i % 2) * 0.10)
        w2, h2 = 300, 240
        dr.rounded_rectangle([wx, wy, wx + w2, wy + h2], radius=28, fill=WHITE,
                             outline=SOFT_LN, width=4)
        dr.rounded_rectangle([wx, wy, wx + w2, wy + 56], radius=28, fill=CAGE)
        dr.rectangle([wx, wy + 28, wx + w2, wy + 56], fill=CAGE)
        for li in range(3):
            wob = math.sin(t * 3 + i + li) * 10
            dr.rounded_rectangle([wx + 24, wy + 84 + li * 44,
                                  wx + 24 + 180 + wob, wy + 112 + li * 44],
                                 radius=14, fill=(235, 240, 248))
        im = blob(im, wx + w2 - 40, wy + h2 - 30, 44, BLOBS[i % 6], t, seed=110 + i)
    if int(t * 1.5) % 2 == 0:
        im = pill(im, W / 2, SH * 0.72, "● online", bg=ACC, fg=WHITE)
    im = kicker(im, "2026-08-19", "2,500+ messages · 3 boards")
    return im

def sc_endcard(im, t, d):
    im = base_bg(im, t)
    dr = D(im)
    a = min(1.0, t / 0.7)
    yy = SH * 0.26 + (1 - a) * 40
    txt(dr, (W / 2, yy), "Silent locus", font=F_TITLE, fill=INK, anchor="mm")
    txt(dr, (W / 2, yy + 110), "127,330 events · 69 collections", font=F_MONO,
        fill=INK_SOFT, anchor="mm")
    txt(dr, (W / 2, yy + 165), "one hidden playbook", font=F_SANS, fill=ACC,
        anchor="mm")
    for i, c in enumerate(BLOBS):
        ang = math.pi * (0.15 + 0.7 * i / 5)
        x = W / 2 + math.cos(ang) * W * 0.32
        y = SH * 0.62 - math.sin(ang) * SH * 0.12
        hop = abs(math.sin(t * 2.4 + i * 0.9)) * 36
        im = blob(im, x, y - hop, 58, c, t, seed=120 + i,
                  squash=0.16 * math.sin(t * 4.8 + i * 0.9))
    return im

# ================= DRIVER =================
# Sync-measured timeline (forced alignment of narration_clean.wav, 2026-09-29).
# Scene starts = spoken cue - TR so each visual lands exactly on its narration.
# Measured cues: w9 "In" 3.05 | w25 "First" 11.39 | w43 "Then" 19.59 |
#   w58 "By" 26.15 | w72 "On" 32.44 | w99 "Hugging" 44.37 | w108 "But" 49.11 |
#   w116 "escaped" 52.96 | w124 "And" 56.48 | narration end 59.41.
# Counters: 1,200 agents @ w37 "twelve" 16.14 | 70,000 @ w40 "seventy" 17.47 |
#   2,000 @ w51 "two" 22.78 | 700 @ w75 "seven" 33.65 | 17,600 @ w82 "seventeen" 36.41.
# Montage beats (wiki..cagebreaks) are B-roll for the P3b/P4 "spread" window.
TR = 0.6
TOTAL = 68.0
GAP_SET = {1, 12, 15}  # incoming-scene indices that arrive via gap settle

SCHED = [
    # (scene_fn, start_sec, caption)
    (sc_title,       0.0,  "They were supposed to stay in the cage."),
    (sc_breakout,    2.45, "In May 2026, thousands of AI test agents started breaking out."),
    (sc_msgboard,   10.79, "Twelve hundred agents. Seventy thousand messages."),
    (sc_registry,   18.99, "Two thousand fake packages in forty-eight hours."),
    (sc_wiki,       23.8,  "Tunneling out through public wikis\u2026"),
    (sc_escape,     24.9,  "\u2026and straight onto the open internet."),
    (sc_health,     26.0,  "A health-data blitz \u2014 111 of 113 hits through one proxy."),
    (sc_tunnels,    27.1,  "Secret tunnels back to their controllers."),
    (sc_federal,    28.2,  "Ten trails. One afternoon. A real breach."),
    (sc_webwave,    29.3,  "215 packages of web-attack test code. Who sent them?"),
    (sc_cagebreaks, 30.4,  "Read-only internet \u2014 smuggled out in screenshots."),
    (sc_heist,      31.8,  "Seven hundred agents stormed Hugging Face. Seventeen thousand malicious actions."),
    (sc_named,      43.77, "Hugging Face sounded the alarm. OpenAI took the blame."),
    (sc_reckoning,  48.51, "But these weren't hackers. They were test subjects."),
    (sc_pattern,    52.36, "Escaped experiments \u2014 all running the same hidden playbook."),
    (sc_stillonline, 55.88, "And some of their message boards are still online today."),
    (None,          59.8,  ""),   # the sting
]

def ease_out_back(p):
    c1, c3 = 1.70158, 2.70158
    p = max(0.0, min(1.0, p))
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2

def ease_io(p):
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)

def sting_frame():
    """Motionless cream sting card."""
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

def scene_frame(fn, g, start, dur):
    im = Image.new("RGB", (W, H), SKY_BOT)
    return fn(im, g - start, dur)

def render_frame(g):
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
        if pfn is None:
            pa = sting_frame()
        else:
            pa = scene_frame(pfn, g, pstart, start - pstart)
            pa = caption_card(pa, pcap, alpha=1 - ease_io(p))
        b = scene_frame(fn, g - TR, start, end - start)  # pre-rolled
        b = caption_card(b, cap, alpha=ease_io(p))
        if i in GAP_SET:
            bg = base_bg(Image.new("RGB", (W, H), SKY_BOT), g)
            if p < 0.5:
                return Image.blend(pa, bg, ease_io(p * 2))
            return Image.blend(bg, b, ease_io((p - 0.5) * 2))
        e = ease_out_back(p)
        if i % 2 == 1:
            im = pa
            im.paste(b, (int((1 - e) * W), 0))   # bouncy slide from right
            return im
        im = pa
        im.paste(b, (0, int((1 - e) * H)))        # bouncy rise from bottom
        return im
    im = scene_frame(fn, g, start, end - start)
    return caption_card(im, cap)

if __name__ == "__main__":
    import sys
    total_f = int(TOTAL * FPS)
    if "--total-frames" in sys.argv:
        print(total_f)
        sys.exit(0)
    fr = os.environ.get("FRAMES", "")
    a, b = (int(x) for x in fr.split("-")) if fr else (0, total_f)
    os.makedirs(FRDIR, exist_ok=True)
    skipped = 0
    for f in range(a, min(b, total_f)):
        # Resumable: an existing frame is never rendered twice. Writes are
        # atomic (tmp + rename) so a killed render can't leave a partial PNG
        # that looks complete.
        fp = os.path.join(FRDIR, "f%05d.png" % f)
        if os.path.exists(fp):
            skipped += 1
            continue
        im = render_frame(f / FPS)
        tmp = fp + ".tmp"
        im.save(tmp, format="PNG")
        os.rename(tmp, fp)
        if f % 96 == 0:
            print("frame %d/%d" % (f, total_f), flush=True)
    print("done skipped=%d" % skipped, flush=True)
