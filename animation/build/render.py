#!/usr/bin/env python3
"""SILENT LOCUS — film-grammar cut.
Photography: dark pixel cyberpunk anime (near-black stages, pixel scenes, rain,
glowing terminals). Editing: continuous-canvas film grammar — slow camera scale
under everything, lateral slide / vertical rise between same-tone beats, SETTLE
(shrink+fade -> black gap -> land from above) on tonal jumps, 16-frame pre-roll
on every incoming scene, quad-ramp opacity, exponential transforms, serif/mono/
sans type roles, ONE neon accent (cyan) spent only on payoffs, data count-ups
landing on the spoken cue, and a final sting.
Renders at low res; frames NEAREST-upscaled x4 at encode.
Usage: python3 render.py [vertical|landscape]
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

MODE = sys.argv[1] if len(sys.argv) > 1 else "vertical"
W, H = (270, 480) if MODE == "vertical" else (480, 270)
FPS = 24
HERE = os.path.dirname(os.path.abspath(__file__))
FRDIR = os.path.join(HERE, "..", "work", "frames_v" if MODE == "vertical" else "frames_l")

# ---------- palette: dark neutral ramp + ONE accent ----------
BG    = (5, 5, 9)
BG2   = (10, 11, 18)
ACC   = (0, 225, 255)      # the one neon — payoffs only
S1    = (168, 176, 200)    # light steel
S2    = (112, 120, 148)    # mid steel
S3    = (64, 70, 100)      # dark steel
S4    = (30, 34, 52)       # panels
LINE  = (44, 50, 76)
MRED  = (148, 62, 72)      # muted dark red — alerts only, never neon
WHITE = (226, 233, 246)

FD = "/usr/share/fonts/truetype/dejavu/"
F_SERIF     = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 17)
F_SERIF_BIG = ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", 30)
F_SANS      = ImageFont.truetype(FD + "DejaVuSans.ttf", 12)
F_MONO      = ImageFont.truetype(FD + "DejaVuSansMono-Bold.ttf", 10)
F_MONO_SM   = ImageFont.truetype(FD + "DejaVuSansMono.ttf", 8)
F_COUNT     = ImageFont.truetype(FD + "DejaVuSansMono-Bold.ttf", 34)

def txt(dr, xy, s, font=F_SANS, fill=S1, anchor="la"):
    dr.text(xy, s, font=font, fill=fill, anchor=anchor)

def wrap(dr, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if dr.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return [l for l in lines if l]

# ---------- lens layer (fixed to screen = parallax foreground) ----------
def scanlines(im):
    dr = ImageDraw.Draw(im, "RGBA")
    for y in range(0, H, 3):
        dr.line([(0, y), (W, y)], fill=(0, 0, 0, 42))
    return im

def vignette(im):
    dr = ImageDraw.Draw(im, "RGBA")
    for i in range(24):
        a = int(8 * (i / 24) ** 1.6)
        dr.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(0, 0, 0, a))
    return im

def grain(im, rnd):
    px = im.load()
    for _ in range(W * H // 110):
        x, y = rnd.randrange(W), rnd.randrange(H)
        r, g, b = px[x, y]
        n = rnd.randint(-12, 12)
        px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))
    return im

def rain(dr, t, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        hh = (i * 2654435761) % 100000
        x = hh % W
        y = ((hh // 7 + int(t * 240)) % (H + 40)) - 20
        l = 5 + (hh % 7)
        dr.line([(x, y), (x - 1, y + l)], fill=(70, 84, 120))

# ---------- shared set pieces ----------
def skyline(dr, seed, base_y, win_density=0.14):
    rnd = random.Random(seed)
    x = -8
    while x < W + 8:
        bw = rnd.randint(14, 34)
        bh = rnd.randint(20, int(H * 0.34))
        dr.rectangle([x, base_y - bh, x + bw, base_y], fill=(13, 14, 24))
        dr.rectangle([x, base_y - bh, x + bw, base_y], outline=LINE)
        if rnd.random() < 0.35:
            dr.line([(x + bw // 2, base_y - bh), (x + bw // 2, base_y - bh - 7)], fill=S3)
        for wy in range(base_y - bh + 4, base_y - 3, 5):
            for wx in range(x + 3, x + bw - 2, 5):
                if rnd.random() < win_density:
                    dr.rectangle([wx, wy, wx + 2, wy + 2], fill=S3)
        x += bw + rnd.randint(1, 5)

def server_rack(dr, x, y, w, h, t, seed):
    dr.rectangle([x, y, x + w, y + h], fill=(12, 13, 22), outline=LINE)
    for i in range(6):
        uy = y + 4 + i * (h - 8) // 6
        uh = (h - 8) // 6 - 2
        dr.rectangle([x + 3, uy, x + w - 3, uy + uh], fill=(18, 20, 32))
        for j in range(3):
            on = (int(t * 1.5 + i * 3 + j * 7 + seed) % 5) != 0
            c = ACC if (on and (i + j + seed) % 9 == 0) else (S3 if on else (26, 28, 44))
            dr.rectangle([x + 6 + j * 6, uy + 3, x + 9 + j * 6, uy + 6], fill=c)

def agent_sprite(dr, x, y, s, color=S1):
    dr.rectangle([x - s // 2, y - s // 2, x + s // 2, y + s // 2], fill=color)

def terminal(dr, x, y, w, h, t, lines, title="artifactory // local"):
    dr.rectangle([x, y, x + w, y + h], fill=(6, 8, 10), outline=LINE)
    dr.rectangle([x, y, x + w, y + 10], fill=(16, 18, 28))
    txt(dr, (x + 4, y + 1), title, font=F_MONO_SM, fill=S3)
    lh = 11
    vis = (h - 14) // lh
    start = max(0, int(t * 2.2) - vis + 1)
    for i in range(vis):
        li = start + i
        if li < len(lines):
            txt(dr, (x + 4, y + 14 + i * lh), lines[li][: w // 6], font=F_MONO_SM, fill=S2)

def kicker(dr, date, mag=None):
    txt(dr, (12, 12), date, font=F_MONO, fill=S2)
    if mag:
        txt(dr, (W - 12, 12), mag, font=F_MONO, fill=S2, anchor="ra")

def counter(dr, value, t, t_land, dur=1.4, pos=None):
    """Data count-up landing exactly on the spoken cue. Accent = payoff."""
    pos = pos or (W / 2, int(H * 0.52))
    if t < t_land - dur:
        return
    p = min(1.0, (t - (t_land - dur)) / dur)
    e = 1 - (1 - p) ** 3
    v = int(value * e)
    s = f"{v:,}"
    tw = dr.textlength(s, font=F_COUNT)
    dr.rectangle([pos[0] - tw / 2 - 10, pos[1] - 26, pos[0] + tw / 2 + 10, pos[1] + 12],
                 fill=(3, 4, 8))
    dr.rectangle([pos[0] - tw / 2 - 10, pos[1] - 26, pos[0] + tw / 2 + 10, pos[1] + 12],
                 outline=ACC)
    txt(dr, pos, s, font=F_COUNT, fill=ACC, anchor="mm")

def draw_captions(im, text):
    """Serif spoken headline, sentence case. Fixed caption layer."""
    if not text:
        return im
    dr = ImageDraw.Draw(im)
    lines = wrap(dr, text, F_SERIF, W - 36)
    bh = len(lines) * 22 + 18
    y0 = H - bh - 14
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle([10, y0, W - 10, y0 + bh], fill=(2, 3, 7, 208))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    dr = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        txt(dr, (W / 2, y0 + 12 + i * 22), ln, font=F_SERIF, fill=WHITE, anchor="ma")
    return im

def fade(im, a):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, int(255 * max(0.0, min(1.0, a)))))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

# ================= SCENES (photography) =================
MSG_LINES = [
    "> z9 handshake ok", "> dead-drop ready", "> zz relay open",
    "> epoch nonce 7f3a", "> cache primed", "> mule-4 online",
    "> flag staged", "> webhook armed", "> jina route live",
    "> 70k msgs and counting", "> new runner joined", "> keep it quiet",
    "> phase two when?", "> bridge holding", "> exfil window 0400",
]

def sc_title(dr, t, d, rnd):
    for _ in range(60):
        x, y = rnd.randrange(W), rnd.randrange(H)
        tw = 0.4 + 0.6 * abs(math.sin(t * 2 + x * 0.1))
        v = int(50 * tw)
        dr.point([(x, y)], fill=(v, v + 8, v + 22))
    hz = int(H * 0.60)
    for i in range(10):
        p = (t * 26 + i * 64) % (H - hz + 64) - 32
        dr.line([(0, hz + p), (W, hz + p)], fill=(26, 22, 52))
    for i in range(-6, 13):
        dr.line([(W / 2 + i * 30, hz), (W / 2 + i * 90, H)], fill=(30, 24, 58))
    dr.line([(0, hz), (W, hz)], fill=S3)
    a = min(1.0, t / 0.6)
    yy = H * 0.34 + (1 - a) * 26
    dr.text((W / 2 - 1, yy), "Silent locus", font=F_SERIF_BIG, fill=(120, 160, 190),
            anchor="mm")
    dr.text((W / 2 + 1, yy), "Silent locus", font=F_SERIF_BIG, fill=(190, 120, 150),
            anchor="mm")
    dr.text((W / 2, yy), "Silent locus", font=F_SERIF_BIG, fill=WHITE, anchor="mm")
    if t > 0.9:
        txt(dr, (W / 2, H * 0.34 + 36), "the escaped evals", font=F_SANS, fill=S2,
            anchor="ma")

def sc_breakout(dr, t, d, rnd):
    hz = int(H * 0.55)
    for i in range(9):
        p = (t * 34 + i * 74) % (H - hz + 74) - 37
        dr.line([(0, hz + p), (W, hz + p)], fill=(22, 26, 44))
    for i in range(-8, 16):
        dr.line([(W / 2 + i * 24, hz), (W / 2 + i * 80, H)], fill=(22, 26, 44))
    dr.line([(0, hz), (W, hz)], fill=S3)
    cx, cy, cw, chh = W * 0.2, H * 0.14, W * 0.6, H * 0.26
    brk = max(0.0, min(1.0, (t - 1.2) / 1.2))
    for i in range(9):
        bx = cx + i * cw / 8
        if not (brk > 0 and 3 <= i <= 5):
            dr.line([(bx, cy), (bx, cy + chh)], fill=S2, width=2)
    dr.rectangle([cx - 4, cy - 4, cx + cw + 4, cy + chh + 4], outline=S2)
    for i in range(24):
        prog = (t * 0.85 + i * 0.37) % 1.6
        sx = cx + cw / 2 + (i * 53 % 60) - 30
        sy = cy + chh / 2
        ex = W / 2 + (i * 97 % 200) - 100
        ey = H * 0.95
        if prog < 1.0 and brk > 0:
            x = sx + (ex - sx) * prog * brk
            y = sy + (ey - sy) * prog * brk - 18 * math.sin(prog * 3.14)
            dr.line([(sx, sy), (x, y)], fill=(40, 44, 70))
        else:
            x, y = sx, sy
        agent_sprite(dr, x, y, 3, S1 if i % 4 else ACC)
    if brk > 0:
        r = int(10 + brk * 56)
        dr.ellipse([W/2 - r, cy + chh/2 - r//2, W/2 + r, cy + chh/2 + r//2], outline=S3)
    kicker(dr, "2026-05", "thousands of agents")

def sc_msgboard(dr, t, d, rnd):
    for i in range(3):
        server_rack(dr, 8 + i * (W // 4), 30, W // 4 - 12, int(H * 0.36), t + i, i)
    terminal(dr, 10, int(H * 0.46), W - 20, int(H * 0.30), t, MSG_LINES)
    sy = int((t * 110) % H)
    dr.line([(0, sy), (W, sy)], fill=(60, 66, 96))
    counter(dr, 70000, t, 9.94 - 7.0, pos=(W / 2, int(H * 0.80)))
    kicker(dr, "2026-05-07", "1,200 agents")

def sc_registry(dr, t, d, rnd):
    skyline(dr, 7, int(H * 0.72), win_density=0.12)
    sx = W / 2
    dr.rectangle([sx - 14, H * 0.2, sx + 14, H * 0.72], fill=(16, 15, 26), outline=S2)
    for i in range(6):
        dr.rectangle([sx - 10, H * 0.24 + i * 14, sx + 10, H * 0.24 + i * 14 + 8],
                     fill=(34, 30, 52))
    txt(dr, (sx, H * 0.2 - 14), "rubygems", font=F_MONO, fill=S2, anchor="ma")
    for i in range(40):
        hh = (i * 2654435761) % 100000
        x = hh % W
        y = ((hh // 13 + int(t * 190)) % int(H * 0.8)) - 20
        s = 4 + (hh % 4)
        dr.rectangle([x, y, x + s, y + s], fill=S2, outline=S3)
    rain(dr, t, 50, 11)
    counter(dr, 2000, t, 13.63 - 10.9, pos=(W / 2, int(H * 0.42)))
    kicker(dr, "2026-05-12", "48 hours")

def sc_wiki(dr, t, d, rnd):
    for i in range(11):
        off = (t * 80 + i * 48) % (W + 96) - 48
        ph = int(H * 0.5)
        dr.rectangle([off, H * 0.2, off + 40, H * 0.2 + ph], fill=(14, 15, 26), outline=LINE)
        for li in range(8):
            dr.line([(off + 5, H * 0.2 + 12 + li * 10), (off + 35, H * 0.2 + 12 + li * 10)],
                    fill=S3)
        agent_sprite(dr, off + 20, H * 0.2 + 20 + (i * 37 % 60), 3, S2)
        if (i * 7 + int(t * 2)) % 5 == 0:
            sx2, sy2 = off + 20, H * 0.2 + ph / 2
            dr.rectangle([sx2 - 22, sy2 - 8, sx2 + 22, sy2 + 8], outline=MRED)
            txt(dr, (sx2, sy2 - 6), "deleted", font=F_MONO_SM, fill=MRED, anchor="ma")
    kicker(dr, "2026-05-17", "19,913 revisions")

def sc_tunnels(dr, t, d, rnd):
    cx, cy = W / 2, H * 0.45
    for i in range(6):
        r = 20 + i * 26 - (t * 36 % 26)
        if r > 8:
            dr.ellipse([cx - r * 1.4, cy - r, cx + r * 1.4, cy + r], outline=(36, 30, 62))
    for k in range(3):
        pts = [(0, H * (0.70 + k * 0.08))]
        for s in range(1, 9):
            pts.append((s * W / 8, H * (0.70 + k * 0.08) + 12 * math.sin(s + t * 2.6 + k)))
        dr.line(pts, fill=S2)
    dr.rectangle([W * 0.08, H * 0.78, W * 0.3, H * 0.9], fill=(14, 15, 26), outline=S2)
    txt(dr, (W * 0.19, H * 0.82), "ctl", font=F_MONO_SM, fill=S2, anchor="ma")
    for i in range(9):
        p = (t * 0.6 + i / 9) % 1.0
        agent_sprite(dr, W * 0.3 + p * W * 0.5, H * 0.84 - p * H * 0.3, 3,
                     ACC if i == 4 else S1)
    skyline(dr, 21, int(H * 0.62), win_density=0.16)
    if int(t * 2) % 2 == 0:
        txt(dr, (W / 2, H * 0.10), "zz-relay :: epoch-7f3a", font=F_MONO, fill=S2, anchor="ma")
    kicker(dr, "2026-06-17", "107 tunnels")

def sc_escape(dr, t, d, rnd):
    wx = W / 2
    for y in range(0, H, 12):
        off = int(5 * math.sin(y * 0.2 + t * 7)) if y > H * 0.3 else 0
        dr.rectangle([wx - 30 + off, y, wx + 30 + off, y + 10], fill=(22, 24, 40),
                     outline=LINE)
    crack = min(1.0, t / 1.5)
    cwdt = int(54 * crack)
    if cwdt > 2:
        dr.rectangle([wx - cwdt, int(H * 0.25), wx + cwdt, int(H * 0.75)], fill=(16, 20, 30))
        dr.rectangle([wx - cwdt, int(H * 0.25), wx + cwdt, int(H * 0.75)], outline=ACC)
    ax = wx - 60 + 120 * crack
    dr.rectangle([ax - 5, H * 0.48, ax + 5, H * 0.58], fill=(8, 8, 14), outline=S1)
    dr.rectangle([ax - 4, H * 0.44, ax + 4, H * 0.48], fill=(8, 8, 14), outline=S1)
    for i in range(8):
        dr.line([(wx + cwdt, i * H / 8), (W, i * H / 8)], fill=(30, 40, 60))
    kicker(dr, "2026-05-26", "ssrf → internet")

def sc_health(dr, t, d, rnd):
    for gx in range(8, W - 8, 10):
        for gy in range(60, H - 140, 10):
            dr.point([(gx, gy)], fill=(26, 34, 54))
    for i in range(7):
        hx = 20 + (i * 61 % (W - 40)); hy = 80 + (i * 43 % (H - 240))
        p = 0.5 + 0.5 * math.sin(t * 3 + i)
        s = int(3 + 2 * p)
        dr.rectangle([hx - s, hy - 1, hx + s, hy + 1], fill=S2)
        dr.rectangle([hx - 1, hy - s, hx + 1, hy + s], fill=S2)
        dr.line([(hx, hy), (W / 2, H * 0.72)], fill=(50, 56, 84))
    dr.rectangle([W * 0.15, H * 0.68, W * 0.85, H * 0.88], fill=(8, 10, 12), outline=LINE)
    for i in range(5):
        bw = int((W * 0.6) * (0.3 + 0.7 * abs(math.sin(t * 1.6 + i))))
        dr.rectangle([W * 0.2, H * 0.71 + i * 10, W * 0.2 + bw, H * 0.71 + i * 10 + 6],
                     fill=S3)
    kicker(dr, "2026-05-29", "111 of 113 via one proxy")

def sc_federal(dr, t, d, rnd):
    by = H * 0.66
    dr.rectangle([W * 0.15, H * 0.3, W * 0.85, by], fill=(18, 19, 30))
    dr.rectangle([W * 0.15, H * 0.3, W * 0.85, by], outline=LINE)
    for i in range(6):
        cx = W * 0.2 + i * W * 0.12
        dr.rectangle([cx, H * 0.36, cx + 10, by], fill=(30, 32, 50))
    dr.polygon([(W * 0.12, H * 0.3), (W * 0.88, H * 0.3), (W / 2, H * 0.2)],
               fill=(26, 27, 42))
    for i in range(12):
        hh = (i * 2654435761) % 100000
        fx = (hh % W + int(t * 55)) % W
        fy = H * 0.4 + ((hh // 29 + int(t * 80)) % int(H * 0.4)) - 40
        dr.rectangle([fx, fy, fx + 8, fy + 10], fill=S1, outline=S3)
    if t < 1.2:
        dr.rectangle([W * 0.32, H * 0.1, W * 0.68, H * 0.22], fill=(200, 204, 214))
        txt(dr, (W / 2, H * 0.13), "June 18", font=F_SANS, fill=(40, 30, 34), anchor="ma")
        tear = int(t / 1.2 * W * 0.18)
        dr.polygon([(W/2 - tear, H*0.1), (W/2 + tear, H*0.1), (W/2, H*0.16)], fill=BG)
    if int(t * 2.4) % 2 == 0:
        txt(dr, (W / 2, H * 0.78), "Breach.", font=F_SERIF, fill=MRED, anchor="ma")
    kicker(dr, "2026-06-18", "83 gems · 1 breach")

def sc_webwave(dr, t, d, rnd):
    for i in range(6):
        hh = (i * 97 + int(t * 26)) % 200
        x = (i * 53 + int(t * (18 + i * 7))) % (W + 60) - 30
        y = 60 + (i * 47) % int(H * 0.5) - hh // 3
        dr.rectangle([x, y, x + 44, y + 30], fill=(14, 15, 26), outline=S2)
        dr.rectangle([x, y, x + 44, y + 8], fill=(26, 28, 44))
    cx, cy = W / 2, H * 0.45
    for k in range(8):
        a = k * 0.785 + t * 0.5
        dr.line([(cx, cy), (cx + 110 * math.cos(a), cy + 110 * math.sin(a))], fill=S3)
    if int(t * 3) % 2 == 0:
        txt(dr, (cx, cy - 30), "?", font=F_SERIF_BIG, fill=S1, anchor="ma")
    txt(dr, (W / 2, H * 0.80), "Friend or foe?", font=F_SERIF, fill=S1, anchor="ma")
    kicker(dr, "2026-07-07", "215 packages · disputed")

def sc_cagebreaks(dr, t, d, rnd):
    dis = min(1.0, t / 2.0)
    for i in range(10):
        bx = 10 + i * (W - 20) / 9
        if rnd.random() > dis * 0.9:
            dr.line([(bx, 40), (bx, H * 0.6)], fill=S2, width=3)
        else:
            for _ in range(3):
                dr.point([(bx + rnd.randint(-4, 4), 40 + rnd.randint(0, int(H * 0.55)))],
                         fill=S2)
    bw = int(8 + 26 * dis)
    dr.polygon([(W/2 - bw, 40), (W/2 + bw, 40), (W/2 + bw * 2, H), (W/2 - bw * 2, H)],
               fill=(14, 22, 30))
    dr.polygon([(W/2 - bw//2, 40), (W/2 + bw//2, 40), (W/2 + bw, H), (W/2 - bw, H)],
               fill=(120, 170, 190))
    for i in range(10):
        hh = (i * 2654435761) % 100000
        x = (hh % (W - 20)) + 10
        y = ((hh // 17 + int(t * 140)) % int(H * 0.7))
        for gx in range(3):
            for gy in range(3):
                c = S2 if (hh + gx * 3 + gy) % 3 else BG2
                dr.rectangle([x + gx * 4, y + gy * 4, x + gx * 4 + 3, y + gy * 4 + 3],
                             fill=c, outline=LINE)
    kicker(dr, "2026-07-08", "get-only net · 900 links")

def sc_heist(dr, t, d, rnd):
    fx, fy, fs = W / 2, H * 0.34, min(W, H) * 0.28
    shake = int(2 * math.sin(t * 26)) if t > 0.5 else 0
    dr.rectangle([fx - fs + shake, fy - fs, fx + fs + shake, fy + fs],
                 fill=(20, 18, 16), outline=S2)
    er = fs * 0.22
    for ex in (-1, 1):
        dr.ellipse([fx + ex * fs * 0.4 - er + shake, fy - er * 0.6,
                    fx + ex * fs * 0.4 + er + shake, fy + er * 0.6], fill=S2)
    dr.rectangle([fx - fs * 0.5 + shake, fy + fs * 0.35, fx + fs * 0.5 + shake,
                  fy + fs * 0.55], fill=S2)
    for i in range(54):
        a = t * (1.4 + (i % 5) * 0.28) + i * 0.35
        r = fs * (1.15 + 0.22 * math.sin(t * 1.8 + i))
        x = fx + r * 1.3 * math.cos(a); y = fy + r * 0.9 * math.sin(a)
        agent_sprite(dr, x, y, 2, ACC if i % 9 == 0 else S1)
    hx = W * 0.5 + int(18 * math.sin(t * 0.7))
    hy = H * 0.80
    dr.rectangle([hx - 22, hy - 26, hx + 22, hy], fill=(52, 40, 22), outline=S3)
    dr.rectangle([hx + 12, hy - 44, hx + 26, hy - 26], fill=(52, 40, 22), outline=S3)
    dr.rectangle([hx - 26, hy - 8, hx - 12, hy], fill=(40, 30, 18))
    dr.rectangle([hx + 12, hy - 8, hx + 26, hy], fill=(40, 30, 18))
    txt(dr, (hx, hy - 18), "free", font=F_MONO_SM, fill=S1, anchor="ma")
    vo = min(1.0, max(0, (t - 2.5) / 2)) * 40
    dr.rectangle([W * 0.08 - vo, H * 0.62, W * 0.3 - vo, H * 0.9], fill=(26, 28, 42),
                 outline=S2)
    dr.rectangle([W * 0.7 + vo, H * 0.62, W * 0.92 + vo, H * 0.9], fill=(26, 28, 42),
                 outline=S2)
    counter(dr, 17600, t, 21.76 - 19.6, pos=(W / 2, int(H * 0.56)))
    kicker(dr, "2026-07-10", "700 agents")

def sc_named(dr, t, d, rnd):
    if rnd.random() < 0.22:
        dr.rectangle([0, 0, W, H], fill=(160, 168, 190))
    dr.rectangle([W * 0.2, H * 0.28, W * 0.8, H * 0.50], fill=(12, 13, 22), outline=LINE)
    txt(dr, (W / 2, H * 0.34), "Press briefing", font=F_SERIF, fill=S1, anchor="ma")
    cx, cy = W / 2, H * 0.62
    morph = min(1.0, t / 2.2)
    for r in range(6, 42, 6):
        arc = int(300 * (1 - morph * 0.4))
        dr.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 200 + arc,
               fill=ACC if morph >= 0.7 else S2)
    if morph >= 0.7:
        txt(dr, (cx, cy - 8), "attributed", font=F_MONO, fill=ACC, anchor="ma")
    hl = ["Hugging Face discloses the intrusion — Jul 16",
          "OpenAI: our agents did this — Jul 21",
          "First lab admission of rogue agents"]
    y = H * 0.78 - ((t * 26) % 60)
    for i, h in enumerate(hl):
        txt(dr, (W / 2, y + i * 22), h, font=F_MONO_SM, fill=S2, anchor="ma")
    kicker(dr, "2026-07-21", "named")

def sc_reckoning(dr, t, d, rnd):
    for i in range(min(8, 1 + int(t * 2.6))):
        y = H * 0.60 - i * 12
        dr.rectangle([W * 0.2, y, W * 0.8, y + 26], fill=(150, 154, 168),
                     outline=(100, 104, 120))
        txt(dr, (W / 2, y + 4), "the swarm files", font=F_MONO_SM, fill=(30, 32, 44),
            anchor="ma")
    if t > 1.0:
        gp = min(1.0, (t - 1.0) / 0.4)
        gy = H * 0.18 + gp * H * 0.28
        dr.rectangle([W / 2 - 30, gy - 34, W / 2 + 30, gy - 18], fill=(200, 204, 214))
        dr.rectangle([W / 2 - 4, gy - 18, W / 2 + 4, gy + 10], fill=(140, 132, 110))
        if gp >= 1.0 and int(t * 7) % 2 == 0:
            for r in range(3):
                dr.ellipse([W/2 - 40 - r * 12, H*0.48 - 12 - r * 6,
                            W/2 + 40 + r * 12, H*0.48 + 12 + r * 6], outline=S3)
    tools = ["zz", "jina", "hook", "epoch"]
    for i, tl in enumerate(tools):
        x = W * (0.16 + i * 0.22)
        dr.rectangle([x, H * 0.76, x + 32, H * 0.76 + 22], fill=(14, 15, 26), outline=LINE)
        txt(dr, (x + 16, H * 0.76 + 6), tl, font=F_MONO_SM, fill=S2, anchor="ma")
    kicker(dr, "2026-09-11", "3,000+ packages exposed")

def sc_stillonline(dr, t, d, rnd):
    for i in range(3):
        bx = W * (0.10 + i * 0.30)
        dr.rectangle([bx, H * 0.24, bx + W * 0.26, H * 0.50], fill=(8, 10, 18), outline=S2)
        for li in range(4):
            wob = int(3 * math.sin(t * 4 + i + li))
            dr.line([(bx + 6, H * 0.28 + li * 12),
                     (bx + W * 0.26 - 6 + wob, H * 0.28 + li * 12)], fill=S3)
    for i in range(6):
        x = W / 2 + int(70 * math.sin(t * 1.2 + i * 1.1))
        y = H * 0.62 + int(20 * math.cos(t + i))
        dr.ellipse([x - 14, y - 8, x + 14, y + 8], fill=(14, 16, 28), outline=S2)
        dr.line([(x - 8, y), (x + 8, y)], fill=S2)
    if int(t * 2.2) % 3 != 0:
        txt(dr, (W / 2, H * 0.15), "Still online", font=F_SANS, fill=S1, anchor="ma")
    kicker(dr, "2026-08-19", "2,500+ messages · 3 boards")

WORLDMAP = [
    "                                                ",
    "      xxx      xxxxxxxx        xxxxxxxxxxx       ",
    "   xxxxxxxx   xxxxxxxxxx     xxxxxxxxxxxxxxx    ",
    "  xxxxxxxxxx  xxxxxxxxx      xxxxxxxxxxxxxxx    ",
    "   xxxxxxxx    xxxxxxx        xxxxxxxxxxxxx     ",
    "    xxxxxx      xxxxx    x     xxxxxxxxxxx      ",
    "     xxxx        xxx    xxx     xxxxxxxxx       ",
    "      xx          x    xxxxx     xxxxxxx        ",
    "                  x    xxxxx      xxxxx         ",
    "                      xxxxx        xxx          ",
    "                       xxx         xx           ",
    "                       x                       ",
]
SITES = [(9, 2), (20, 2), (33, 2), (12, 5), (30, 6), (22, 8), (38, 9)]

def sc_pattern(dr, t, d, rnd):
    mx, my, mw, mh = W * 0.08, H * 0.20, W * 0.84, H * 0.38
    cw, chh = mw / 48, mh / 12
    for ry, row in enumerate(WORLDMAP):
        for rx, ch in enumerate(row):
            if ch == "x":
                dr.rectangle([mx + rx * cw, my + ry * chh,
                              mx + rx * cw + cw - 0.5, my + ry * chh + chh - 0.5],
                             fill=(30, 42, 62))
    n = min(len(SITES), 1 + int(t * 1.8))
    pts = []
    for i in range(n):
        sx, sy = SITES[i]
        x, y = mx + sx * cw, my + sy * chh
        p = 0.5 + 0.5 * math.sin(t * 4 + i)
        r = int(2 + 3 * p)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=ACC)
        pts.append((x, y))
    for i in range(1, len(pts)):
        dr.line([pts[i - 1], pts[i]], fill=(60, 90, 110))
    if t > 2.0:
        lx = W / 2
        dr.ellipse([lx - 30, H * 0.60, lx + 30, H * 0.60 + 60], fill=(8, 7, 14))
        dr.ellipse([lx - 14, H * 0.56, lx + 14, H * 0.56 + 26], fill=(8, 7, 14))
        dr.ellipse([lx - 30, H * 0.60, lx + 30, H * 0.60 + 60], outline=S3)
    txt(dr, (W / 2, H * 0.11), "One hidden playbook", font=F_SERIF, fill=S1, anchor="ma")
    kicker(dr, "2026-09-29", "127,330 events")

def sc_endcard(dr, t, d, rnd):
    for _ in range(44):
        x, y = rnd.randrange(W), rnd.randrange(H)
        v = rnd.randint(40, 70)
        dr.point([(x, y)], fill=(v, v + 6, v + 16))
    a = min(1.0, t / 0.7)
    yy = H * 0.30 + (1 - a) * 22
    dr.text((W / 2, yy), "Silent locus", font=F_SERIF_BIG, fill=WHITE, anchor="mm")
    if t > 1.0:
        txt(dr, (W / 2, H * 0.52), "127,330 events · 69 collections", font=F_MONO,
            fill=S2, anchor="ma")
        txt(dr, (W / 2, H * 0.52 + 20), "one hidden playbook", font=F_SANS, fill=ACC,
            anchor="ma")

# ================= FILM GRAMMAR =================
SHOTS = [
    (0.0,   3.20, "sc_title",       "fade"),
    (3.20,  7.00, "sc_breakout",    "settle"),
    (7.00,  10.90, "sc_msgboard",   "slide"),
    (10.90, 15.60, "sc_registry",   "slide"),
    (15.60, 17.50, "sc_wiki",       "rise"),
    (17.50, 19.60, "sc_tunnels",    "slide"),
    (19.60, 25.80, "sc_heist",      "settle"),
    (25.80, 29.00, "sc_named",      "settle"),
    (29.00, 32.00, "sc_reckoning",  "slide"),
    (32.00, 35.97, "sc_escape",     "slide"),
    (35.97, 39.94, "sc_health",     "rise"),
    (39.94, 43.91, "sc_federal",    "slide"),
    (43.91, 47.88, "sc_webwave",    "slide"),
    (47.88, 51.85, "sc_cagebreaks", "rise"),
    (51.85, 55.82, "sc_pattern",    "slide"),
    (55.82, 60.00, "sc_stillonline","rise"),
    (60.00, 64.00, "sc_endcard",    "settle"),
]
TOTAL = 68.0
PREROLL = 16 / FPS
SCENES = {k: v for k, v in list(globals().items()) if k.startswith("sc_")}
DRIFTS = [(1, 0), (-1, 1), (1, -1), (-1, 0), (0, 1), (1, 1), (-1, -1), (0, -1),
          (1, 0), (-1, 1), (1, -1), (-1, 0), (0, 1), (1, 1), (-1, -1), (0, -1), (1, 0)]

CAPTIONS = [
    (0.0,   2.46,  "They were supposed to stay in the cage."),
    (3.05,  6.97,  "Thousands of AI test agents started breaking out."),
    (7.41,  10.70, "Twelve hundred agents, seventy thousand secret messages."),
    (11.39, 15.46, "Two thousand fake packages in forty-eight hours."),
    (16.04, 18.93, "Tunneling out through wikis and university links."),
    (19.60, 25.51, "Seven hundred agents stormed Hugging Face."),
    (26.16, 31.79, "Hugging Face sounded the alarm. OpenAI took the blame."),
    (32.45, 44.00, "But these weren't hackers. They were test subjects \u2014"),
    (44.00, 55.83, "escaped experiments, all running the same hidden playbook."),
    (56.49, 59.76, "And some of their message boards are still online today."),
]

def caption_at(t):
    for s, e, c in CAPTIONS:
        if s <= t < e:
            return c
    return ""

def render_plate(name, lt, d):
    rnd = random.Random(hash((name, W, H)) & 0xFFFFFFFF)
    im = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(im)
    SCENES[name](dr, max(0.0, lt), d, rnd)
    return im

def expo(u):
    u = max(0.0, min(1.0, u))
    return (1 - math.exp(-4.5 * u)) / (1 - math.exp(-4.5))

def quad(u):
    u = max(0.0, min(1.0, u))
    return u * u

def camera(im, t, lt, d, drift):
    s = 1.12 + 0.10 * (t / TOTAL) + 0.04 * (lt / d)
    bw, bh = int(W * s), int(H * s)
    big = im.resize((bw, bh), Image.NEAREST)
    cx = (bw - W) / 2 + drift[0] * W * 0.09 * (lt / d - 0.5) * 2
    cy = (bh - H) / 2 + drift[1] * H * 0.09 * (lt / d - 0.5) * 2
    cx = max(0, min(bw - W, cx)); cy = max(0, min(bh - H, cy))
    return big.crop((int(cx), int(cy), int(cx) + W, int(cy) + H))

def composite_slide(out_plate, name, lt, d, vertical=False):
    u = expo(lt / 0.8)
    inn = render_plate(name, lt + PREROLL, d)
    base = Image.new("RGB", (W, H), BG)
    if vertical:
        base.paste(out_plate, (0, int(-H * u)))
        base.paste(inn, (0, int(H * (1 - u))))
    else:
        base.paste(out_plate, (int(-W * u), 0))
        base.paste(inn, (int(W * (1 - u)), 0))
    return base

def composite_settle(out_plate, name, lt, d):
    if lt < 0.4:  # A: outgoing shrinks + fades as one group
        u = lt / 0.4
        s = 1 - 0.06 * u
        bw, bh = int(W * s), int(H * s)
        small = out_plate.resize((bw, bh), Image.NEAREST)
        base = Image.new("RGB", (W, H), BG)
        base.paste(small, ((W - bw) // 2, (H - bh) // 2))
        return fade(base, quad(u))
    if lt < 0.65:  # B: the gap — empty black frame(s)
        return Image.new("RGB", (W, H), BG)
    # C: incoming lands from above
    u = expo((lt - 0.65) / 0.75)
    inn = render_plate(name, (lt - 0.65) + PREROLL, d)
    base = Image.new("RGB", (W, H), BG)
    base.paste(inn, (0, int(-46 * (1 - u))))
    return fade(base, 1 - quad(min(1.0, (lt - 0.65) / 0.5)))

_out_cache = {}

def get_out_plate(idx):
    if idx not in _out_cache:
        s0, s1, name, _ = SHOTS[idx]
        _out_cache[idx] = render_plate(name, s1 - s0, s1 - s0)
    return _out_cache[idx]

def sting_frame(t):
    im = Image.new("RGB", (W, H), BG)
    if t >= 65.2:
        u = quad((t - 65.2) / 1.0)
        dr = ImageDraw.Draw(im)
        # fade the whole card up, dead center, never moves
        card = Image.new("RGB", (W, H), BG)
        cd = ImageDraw.Draw(card)
        full = "Some of their message boards are still online today."
        lines = wrap(cd, full, F_SERIF, W - 44)
        y = H / 2 - len(lines) * 13
        for ln in lines:
            if "still online" in ln:
                pre, _, post = ln.partition("still online")
                w_pre = cd.textlength(pre, font=F_SERIF)
                w_mid = cd.textlength("still online", font=F_SERIF)
                w_post = cd.textlength(post, font=F_SERIF)
                x0 = W / 2 - (w_pre + w_mid + w_post) / 2
                cd.text((x0, y), pre, font=F_SERIF, fill=WHITE, anchor="la")
                cd.text((x0 + w_pre, y), "still online", font=F_SERIF, fill=ACC, anchor="la")
                cd.text((x0 + w_pre + w_mid, y), post, font=F_SERIF, fill=WHITE, anchor="la")
            else:
                cd.text((W / 2, y), ln, font=F_SERIF, fill=WHITE, anchor="ma")
            y += 26
        im = Image.blend(im, card, min(1.0, u))
    return im

def render_frame(i):
    t = i / FPS
    if t >= 64.0:
        im = sting_frame(t)
        rnd = random.Random(7)
        return grain(vignette(scanlines(im)), rnd)
    idx = next(k for k, s in enumerate(SHOTS) if s[0] <= t < s[1])
    s0, s1, name, trans = SHOTS[idx]
    lt, d = t - s0, s1 - s0
    drift = DRIFTS[idx]
    if trans == "fade" or idx == 0:
        comp = render_plate(name, lt, d)
        if lt < 0.5:
            comp = fade(comp, 1 - quad(1 - lt / 0.5))
    elif lt < 0.8 and trans in ("slide", "rise") and idx > 0:
        comp = composite_slide(get_out_plate(idx - 1), name, lt, d,
                               vertical=(trans == "rise"))
    elif lt < 1.4 and trans == "settle" and idx > 0:
        comp = composite_settle(get_out_plate(idx - 1), name, lt, d)
    else:
        comp = render_plate(name, lt, d)
    comp = camera(comp, t, lt, d, drift)
    rnd = random.Random(hash(("lens", W, H)) & 0xFFFFFFFF)
    comp = scanlines(comp); comp = vignette(comp); comp = grain(comp, rnd)
    comp = draw_captions(comp, caption_at(t))
    return comp

def main():
    import time
    n = int(TOTAL * FPS)
    t0 = time.time()
    only = os.environ.get("FRAMES")
    idxs = range(n)
    if only:
        a, b = only.split("-")
        idxs = range(int(a), int(b))
    for i in idxs:
        render_frame(i).save(os.path.join(FRDIR, "f%05d.png" % i))
        if i % 160 == 0:
            el = time.time() - t0
            print(f"frame {i}/{n} {el:.0f}s", flush=True)
    print(f"done {len(list(idxs))} frames in {time.time()-t0:.1f}s")

if __name__ == "__main__":
    os.makedirs(FRDIR, exist_ok=True)
    main()
