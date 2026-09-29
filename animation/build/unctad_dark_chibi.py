#!/usr/bin/env python3
"""Dark-chibi X-post summary card for the UNCTAD incident findings.
1600x900, all vector/PIL, crisp text. Run: python3 unctad_dark_chibi.py"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "work", "unctad_dark_chibi.png")

# ---------- dark chibi palette ----------
BG      = (11, 17, 33)
CARD    = (23, 31, 54)
CARD_LN = (52, 64, 100)
TXT     = (240, 244, 252)
SOFT    = (148, 163, 196)
ACC     = (255, 123, 107)    # coral — verdict/punchline
MINT    = (126, 231, 172)    # "real"
GOLD    = (255, 209, 130)
INK     = (30, 34, 50)
WHITE   = (255, 255, 255)
BLUSH   = (255, 150, 150)
BLOBS   = [(168, 216, 240), (245, 201, 168), (201, 184, 240),
           (168, 232, 192), (240, 168, 192), (250, 224, 150)]

FD = "/usr/share/fonts/truetype/dejavu/"
def F(path, size):
    return ImageFont.truetype(FD + path, size)

def overlay(im, fn):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(ov))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def txt_w(dr, s, font):
    return dr.textlength(s, font=font)

def wrap(dr, s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if txt_w(dr, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def blob(im, x, y, r, color, seed=0, glow=True):
    if glow:
        def g(d):
            for gr, a in ((int(r * 2.4), 26), (int(r * 1.8), 45)):
                d.ellipse([x - gr, y - gr, x + gr, y + gr],
                          fill=color + (a,))
        im = overlay(im, g)
    def shadow(d):
        d.ellipse([x - r * 0.9, y + r * 0.95, x + r * 0.9, y + r * 1.15],
                  fill=(0, 0, 0, 70))
    im = overlay(im, shadow)
    dr = ImageDraw.Draw(im)
    dr.ellipse([x - r, y - r, x + r, y + r], fill=color,
               outline=WHITE, width=max(3, int(r * 0.1)))
    def hl(d):
        hr = r * 0.22
        d.ellipse([x - r * 0.55 - hr, y - r * 0.55 - hr,
                   x - r * 0.55 + hr, y - r * 0.55 + hr],
                  fill=(255, 255, 255, 170))
    im = overlay(im, hl)
    dr = ImageDraw.Draw(im)
    ex, ey, er = r * 0.32, -r * 0.08, max(3, r * 0.11)
    for sgn in (-1, 1):
        dr.ellipse([x + sgn * ex - er, y + ey - er,
                    x + sgn * ex + er, y + ey + er], fill=INK)
        dr.ellipse([x + sgn * ex - er * 0.3, y + ey - er * 0.4,
                    x + sgn * ex + er * 0.35, y + ey + er * 0.25], fill=WHITE)
    mr = r * 0.30
    dr.arc([x - mr, y + r * 0.05 - mr * 0.6, x + mr, y + r * 0.05 + mr * 0.6],
           15, 165, fill=INK, width=max(3, int(r * 0.09)))
    br = r * 0.16
    for sgn in (-1, 1):
        dr.ellipse([x + sgn * r * 0.62 - br, y + r * 0.22 - br,
                    x + sgn * r * 0.62 + br, y + r * 0.22 + br], fill=BLUSH)
    return im

def card(im, x0, y0, x1, y1, radius=28):
    def sh(d):
        d.rounded_rectangle([x0 + 5, y0 + 8, x1 + 5, y1 + 8], radius=radius,
                            fill=(0, 0, 0, 60))
    im = overlay(im, sh)
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=CARD,
                        outline=CARD_LN, width=2)
    return im

def arrow(dr, x, y0, y1, color=(130, 150, 195), width=10):
    dr.line([(x, y0), (x, y1)], fill=color, width=width)
    s = 20
    dr.polygon([(x - s, y1 - s - 6), (x + s, y1 - s - 6), (x, y1 + 10)],
               fill=color)

def cloud_shape(d, x, y, s, fill):
    for ox, oy, r in ((-58, 8, 40), (0, -6, 52), (58, 8, 40), (0, 16, 44)):
        d.ellipse([x + (ox - r) * s, y + (oy - r) * s,
                   x + (ox + r) * s, y + (oy + r) * s], fill=fill)

# ================= build =================
random.seed(7)
im = Image.new("RGB", (W, H), BG)
dr = ImageDraw.Draw(im)

def ambience(d):
    for _ in range(80):
        x, y = random.uniform(0, W), random.uniform(0, H)
        r = random.uniform(1, 2.6)
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=(170, 190, 235, random.randint(35, 110)))
    for (cx, cy, cr, col, a) in ((W * 0.5, 120, 420, (90, 110, 220), 26),
                                 (W * 0.12, 780, 330, (255, 123, 107), 16),
                                 (W * 0.9, 760, 330, (110, 220, 190), 14)):
        for rr, aa in ((cr, a), (int(cr * 0.66), a + 10)):
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                      fill=col + (aa,))
im = overlay(im, ambience)
dr = ImageDraw.Draw(im)

# ---------- header (bar placed from measured text bbox) ----------
title = "What we actually saw: the UNCTAD incident"
f_title = F("DejaVuSerif-Bold.ttf", 58)
tw = txt_w(dr, title, f_title)
assert tw <= W - 160, f"title overflow: {tw}"
ty = 44
dr.text((W / 2, ty), title, font=f_title, fill=TXT, anchor="ma")
tb = dr.textbbox((W / 2, ty), title, font=f_title, anchor="ma")
bar_y = tb[3] + 10
dr.rounded_rectangle([W / 2 - 150, bar_y, W / 2 + 150, bar_y + 8],
                     radius=4, fill=ACC)

sub = "Our independent trace of the Apr\u2013Jun 2026 UNCTADstat scans"
f_sub = F("DejaVuSans.ttf", 27)
sw = txt_w(dr, sub, f_sub)
assert sw <= W - 160, f"subtitle overflow: {sw}"
sy = bar_y + 8 + 16
dr.text((W / 2, sy), sub, font=f_sub, fill=SOFT, anchor="ma")
sb = dr.textbbox((W / 2, sy), sub, font=f_sub, anchor="ma")

# ---------- main row ----------
T0 = sb[3] + 22
T1 = 780
assert T1 - T0 >= 560, f"row too short: {T1 - T0}"

# ----- left card: our trace -----
L0, L1 = 48, 566
im = card(im, L0, T0, L1, T1)
dr = ImageDraw.Draw(im)
f_kick = F("DejaVuSansMono-Bold.ttf", 23)
dr.text((L0 + 32, T0 + 24), "OUR TRACE", font=f_kick, fill=ACC)

f_num = F("DejaVuSansMono-Bold.ttf", 76)
dr.text((L0 + 32, T0 + 84), "~3,653", font=f_num, fill=TXT)

f_lab = F("DejaVuSans.ttf", 26)
dr.text((L0 + 32, T0 + 182), "UNCTADstat accesses", font=f_lab, fill=SOFT)
dr.text((L0 + 32, T0 + 214), "via third-party relays", font=f_lab, fill=SOFT)

f_date = F("DejaVuSansMono-Bold.ttf", 23)
ds = "Apr 21 \u2192 Jun 21, 2026"
dw = txt_w(dr, ds, f_date) + 44
dy = T0 + 256
assert L0 + 32 + dw <= L1 - 32, "date pill overflow"
dr.rounded_rectangle([L0 + 32, dy, L0 + 32 + dw, dy + 42], radius=21,
                     fill=(38, 48, 80))
dr.text((L0 + 32 + 22, dy + 21), ds, font=f_date, fill=GOLD, anchor="lm")

f_ch = F("DejaVuSansMono.ttf", 20)
f_chb = F("DejaVuSansMono-Bold.ttf", 22)
relays = [("httpbin base64 bridges", "3,215"),
          ("httpbun base64 bridges", "216"),
          ("r.jina.ai reader relay", "194"),
          ("api.allorigins.win proxy", "4"),
          ("dagd relay", "24")]
cy = dy + 42 + 20
dr.text((L0 + 32, cy), "RELAY BREAKDOWN", font=f_kick, fill=SOFT)
cy += 32
for name, cnt in relays:
    chh = 32
    assert cy + chh <= T1 - 16, f"chips overflow card at {name}"
    assert txt_w(dr, name, f_ch) <= (L1 - 32) - (L0 + 52) - 90, \
        f"chip label overflow: {name}"
    dr.rounded_rectangle([L0 + 32, cy, L1 - 32, cy + chh], radius=16,
                        fill=(32, 42, 70))
    dr.text((L0 + 52, cy + chh / 2), name, font=f_ch, fill=TXT, anchor="lm")
    dr.text((L1 - 52, cy + chh / 2), cnt, font=f_chb, fill=GOLD, anchor="rm")
    cy += chh + 8

# ----- center: the trick -----
C0, C1 = 606, 994
cx = (C0 + C1) / 2
dr.text((cx, T0 + 24), "THE TRICK", font=f_kick, fill=ACC, anchor="ma")
f_trick = F("DejaVuSansMono.ttf", 21)
tsub = "the GET\u2192POST bridge"
assert txt_w(dr, tsub, f_trick) <= C1 - C0 - 40
dr.text((cx, T0 + 52), tsub, font=f_trick, fill=SOFT, anchor="ma")

im = blob(im, cx, T0 + 124, 44, BLOBS[0], seed=1)
dr = ImageDraw.Draw(im)
f_cap = F("DejaVuSansMono.ttf", 20)
dr.text((cx, T0 + 188), "agent", font=f_cap, fill=SOFT, anchor="ma")
arrow(dr, cx, T0 + 204, T0 + 240)

cloud_cy = T0 + 288
im = overlay(im, lambda d: cloud_shape(d, cx, cloud_cy, 0.82,
                                      (190, 205, 235, 46)))
dr = ImageDraw.Draw(im)
cloud_shape(dr, cx, cloud_cy, 0.75, (196, 210, 238))
dr.text((cx, cloud_cy + 98), "trusted relay", font=f_cap, fill=SOFT,
        anchor="ma")
arrow(dr, cx, cloud_cy + 116, cloud_cy + 148)

bx, by, bw, bh = cx - 85, cloud_cy + 156, 170, 96
assert by + bh + 30 <= T1, "building overflow"
dr.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16,
                     fill=(42, 55, 88), outline=(80, 96, 140), width=3)
for r_ in range(3):
    for c_ in range(3):
        wx = bx + 22 + c_ * 42
        wy = by + 14 + r_ * 27
        lit = (r_ + c_) % 2 == 0
        dr.rounded_rectangle([wx, wy, wx + 26, wy + 17], radius=4,
                            fill=GOLD if lit else (30, 38, 62))
dr.line([(cx, by), (cx, by - 30)], fill=(150, 165, 200), width=5)
dr.rounded_rectangle([cx, by - 30, cx + 42, by - 8], radius=4,
                     fill=(140, 180, 240))
lbl = "UNCTADstat API"
assert txt_w(dr, lbl, f_cap) <= C1 - C0 - 40
dr.text((cx, by + bh + 24), lbl, font=f_cap, fill=SOFT, anchor="ma")

# ----- right card: verdict -----
R0, R1 = 1034, 1552
im = card(im, R0, T0, R1, T1)
dr = ImageDraw.Draw(im)
dr.text((R0 + 32, T0 + 24), "THE VERDICT", font=f_kick, fill=ACC)

f_v = F("DejaVuSans-Bold.ttf", 32)
y = T0 + 82
l1a, l1b = "Filter-evasion: ", "REAL"
assert txt_w(dr, l1a + l1b, f_v) <= R1 - R0 - 64, "verdict line 1 overflow"
dr.text((R0 + 32, y), l1a, font=f_v, fill=TXT)
dr.text((R0 + 32 + txt_w(dr, l1a, f_v), y), l1b, font=f_v, fill=MINT)
y += 50
l2a, l2b = "Exploitation: ", "ZERO"
assert txt_w(dr, l1a + l1b, f_v) <= R1 - R0 - 64, "verdict line 2 overflow"
dr.text((R0 + 32, y), l2a, font=f_v, fill=TXT)
dr.text((R0 + 32 + txt_w(dr, l2a, f_v), y), l2b, font=f_v, fill=ACC)

f_z = F("DejaVuSans.ttf", 27)
zeros = ["0 double-encoded paths",
         "0 SQL injections",
         "0 XSS-game hosts"]
y += 56
for z in zeros:
    zl = "\u2022  " + z
    assert txt_w(dr, zl, f_z) <= R1 - R0 - 84, f"zero-line overflow: {z}"
    dr.text((R0 + 52, y), zl, font=f_z, fill=TXT)
    y += 40

note = ("Every query was a legitimate public-data pull. "
        "The \u201csecret key\u201d is the API\u2019s documented auth parameter.")
f_note = F("DejaVuSans.ttf", 25)
nlines = wrap(dr, note, f_note, R1 - R0 - 64)
nlh = int(25 * 1.35)
y += 8
for i, ln in enumerate(nlines):
    dr.text((R0 + 32, y + i * nlh), ln, font=f_note, fill=SOFT)
y += len(nlines) * nlh

attr_h = "ATTRIBUTION"
y += 18
dr.text((R0 + 32, y), attr_h, font=f_kick, fill=SOFT)
y += 32
attr = ("\u201cHighly likely\u201d OpenAI \u2014 45/54 Azure IPs overlap "
        "DseWiki editors.")
f_attr = F("DejaVuSans.ttf", 23)
alines = wrap(dr, attr, f_attr, R1 - R0 - 64)
alh = int(23 * 1.35)
assert y + len(alines) * alh <= T1 - 16, "attribution overflow"
for i, ln in enumerate(alines):
    dr.text((R0 + 32, y + i * alh), ln, font=f_attr, fill=SOFT)

# ---------- footer punchline ----------
foot = "Fancy curl with commitment issues \u2014 not a third exploit."
try:
    f_foot = F("DejaVuSerif-BoldItalic.ttf", 36)
except OSError:
    f_foot = F("DejaVuSerif-Bold.ttf", 36)
fw = txt_w(dr, foot, f_foot)
assert fw <= W - 340, f"footer overflow: {fw}"
fy = 832
assert fy + 40 < H - 10, "footer too low"
dr.text((W / 2, fy), foot, font=f_foot, fill=ACC, anchor="ma")
im = blob(im, W / 2 - fw / 2 - 72, fy - 4, 25, BLOBS[3], seed=2)
im = blob(im, W / 2 + fw / 2 + 72, fy - 4, 25, BLOBS[4], seed=5)

# corner peekers
im = blob(im, 40, H - 34, 28, BLOBS[1], seed=9)
im = blob(im, W - 40, 44, 24, BLOBS[2], seed=4)

im.save(OUT)
print("saved", OUT, im.size)
