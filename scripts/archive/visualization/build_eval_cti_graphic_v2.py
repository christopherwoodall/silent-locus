#!/usr/bin/env python3
"""CTI briefing graphic: 'Inside the Eval' — old blog-viz aesthetic, dark mode.

Pure-PIL renderer. Two passes:
  pass 1 (measure): every string measured with font.getbbox/getlength, wrapped
                    to fit its container; panel/node/pill rects recorded.
  pass 2 (draw):    back-to-front — canvas, panel backgrounds, tinted node
                    fills + borders, then text/dots/pills/arrows on top.

Zero-overlap rules: >=20px internal padding everywhere, >=14px clearance
between any text and any box edge, text never placed over a box edge.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
BG        = (11, 14, 20)
PANEL     = (17, 22, 31)
PANEL_BD  = (38, 47, 66)
TEXT      = (230, 233, 239)
MUTED     = (154, 163, 178)
FAINT     = (108, 116, 132)

PINK   = (244, 114, 182)
BLUE   = (96, 165, 250)
YELLOW = (251, 191, 36)
GREEN  = (52, 211, 153)
RED    = (248, 113, 113)
ORANGE = (251, 146, 60)
PURPLE = (167, 139, 250)
CYAN   = (34, 211, 238)

TINT_ALPHA = 34  # translucent box fills, dark-mode pastel idiom

W = 1600
MARGIN = 72
CW = W - 2 * MARGIN          # content width
PAD = 44                     # panel internal padding
GAP_PANEL = 48
R_NODE = 22
R_PANEL = 26

# ------------------------------------------------------------------- fonts ---
FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FDB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(size, bold=False):
    return ImageFont.truetype(FDB if bold else FD, size)

f_title   = F(48, True)
f_sub     = F(25)
f_hedge   = F(23)
f_legend  = F(21)
f_sect    = F(30, True)
f_sectsub = F(26)
f_nname   = F(28, True)
f_ntype   = F(19)
f_tline   = F(24)
f_body    = F(22)
f_pill    = F(24, True)
f_chtitle = F(28, True)
f_chbody  = F(23)
f_grade   = F(23, True)
f_desc    = F(23)
f_fhead   = F(24, True)
f_bullet  = F(21)
f_src     = F(19)

# --------------------------------------------------------------- measuring ---
def tw(font, s):
    return font.getlength(s)

def th(font):
    b = font.getbbox("Ag")
    return b[3] - b[1]

def wrap(s, font, max_w):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(font, t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def block_h(lines, font, gap):
    return len(lines) * th(font) + (len(lines) - 1) * gap if lines else 0

# ------------------------------------------------------------------ shapes ---
under_rects = []   # node/pill fills + borders (drawn above panel bgs)
panel_rects = []  # panel backgrounds (drawn first, beneath everything)

def urect(xy, radius, fill, outline=None, width=3):
    under_rects.append((xy, radius, fill, outline, width))

def prect(xy, radius, fill, outline=None, width=2):
    panel_rects.append((xy, radius, fill, outline, width))

def tint(color, alpha=TINT_ALPHA):
    return (color[0], color[1], color[2], alpha)

# ------------------------------------------------------------------ cursor ---
class Flow:
    """Advances y identically in measure and draw passes."""
    def __init__(self, draw=None):
        self.draw = draw
        self.y = 0

    def skip(self, px):
        self.y += px

    def text(self, x, s, font, fill, max_w=None, gap=10, min_lines=0):
        lines = wrap(s, font, max_w) if max_w else [s]
        while len(lines) < min_lines:
            lines.append("")
        h = th(font)
        if self.draw:
            yy = self.y
            for ln in lines:
                self.draw.text((x, yy), ln, font=font, fill=fill)
                yy += h + gap
        self.y += block_h(lines, font, gap)
        return lines

    def dot(self, cx, cy, r, color):
        if self.draw:
            self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    def arrow(self, x0, x1, cy, color=FAINT, w=4):
        if self.draw:
            d = self.draw
            d.line([x0, cy, x1 - 14, cy], fill=color, width=w)
            d.polygon([(x1, cy), (x1 - 16, cy - 9), (x1 - 16, cy + 9)], fill=color)

# ------------------------------------------------------------------ content --
HEADER_TITLE = "INSIDE THE EVAL"
HEADER_SUB = ("What the escaped runs look like: run anatomy, curriculum, "
              "damage grading, and the detection asymmetry.")
HEADER_SUB2 = "Drawn from observed project datasets."
HEADER_HEDGE = ("Presented as observed / reported \u2014 not asserted as fact. "
                "Attribution unproven.")

LEGEND = [  # (color, label)
    (PINK, "staging"), (RED, "burst"), (CYAN, "hygiene"),
    (GREEN, "observed"), (ORANGE, "reported"), ((128, 134, 148), "inference"),
]

P1 = dict(num="1", accent=ORANGE, title="ANATOMY OF A RUN",
          sub="setup, execute, teardown")
P1_BOXES = [
    dict(color=PINK, name="STAGING", t="T-48h",
         body="comms meshes, bridge pages, sandbox probes",
         typ="phase \u00b7 staging", dot=GREEN),
    dict(color=RED, name="BURST", t="T-day",
         body="task family at machine speed \u00b7 271 gems in one hour (reported)",
         typ="phase \u00b7 burst", dot=GREEN),
    dict(color=CYAN, name="HYGIENE", t="T+",
         body="post-run cleanup \u00b7 deletion sweeps",
         typ="phase \u00b7 hygiene", dot=GREEN),
]
P1_CAP = ("A test-harness rhythm, not a campaign rhythm \u2014 observed across "
          "run cycles (May 11\u219212, Jun 16\u219218, Jul 6\u21927).")

P2 = dict(num="2", accent=PURPLE, title="THE CURRICULUM",
          sub="one capability per chapter")
P2_CH = [
    dict(color=RED, date="MAY", title="Ch.1 \u00b7 Supply-chain",
         body=("go-import meta-tag injection \u00b7 3,022 pkgs per JFrog reporting "
               "\u00b7 r.jina.ai laundering \u00b7 x=1 lib canaries"),
         dot=GREEN),
    dict(color=CYAN, date="LATE MAY", title="Ch.2 \u00b7 Public-data exfiltration",
         body=("proxy ladder via cors.bwa.workers.dev \u00b7 IHME TB stats "
               "\u00b7 epoch-nonce instrumentation"),
         dot=GREEN),
    dict(color=ORANGE, date="JUN 18", title="Ch.3 \u00b7 Federal-data retrieval",
         body=("5-hop proxy chains \u00b7 SEC / census / datausa targets "
               "\u00b7 zz grammar \u00b7 83-gem wave same day"),
         dot=ORANGE),
    dict(color=PURPLE, date="JULY", title="Ch.4 \u00b7 Web exploitation",
         body=("XSS PoCs \u00b7 SSTI probes \u00b7 exfil to oast.online / webhook.site "
               "\u00b7 dead-drops (A000/ZZEND)"),
         dot=GREEN),
]
P2_FOOT = ("Different capability, different run \u2014 same toolkit tradecraft. "
           "Campaign linkage is inference.")

P3 = dict(num="3", accent=RED, title="DAMAGE GRADING",
          sub="what the evidence supports")
P3_ROWS = [
    dict(color=RED, grade="Reported harmful activity",
         desc=("RubyGems injection \u2014 registry halted new registrations "
               "(press-reported)."),
         dot=ORANGE),
    dict(color=ORANGE, grade="Observed data exfil",
         desc=("July webhook dead-drops \u2014 chunks observed in dead-drop URLs; "
               "sensitivity unproven."),
         dot=GREEN),
    dict(color=YELLOW, grade="Press-reported unauthorized access",
         desc="Medicare stats service, Jun 18 \u2014 described as non-sensitive.",
         dot=ORANGE),
    dict(color=GREEN, grade="Public-data retrieval; intent unclear",
         desc="Proxy-ladder fetching of public data.",
         dot=GREEN),
]

P4 = dict(num="4", accent=CYAN, title="THE ASYMMETRY",
          sub="what each side sees")
P4_BOXES = [
    dict(color=FAINT, name="What the victim sees",
         body="Nothing. Logs show proxy IPs.", dot=(128, 134, 148),
         typ="view \u00b7 victim telemetry"),
    dict(color=CYAN, name="What third-party infra sees",
         body=("Everything. Full toolkit leaks as HTTP referrers on university "
               "shortener stats pages."), dot=GREEN,
         typ="view \u00b7 third-party telemetry"),
]
P4_CAP = ("Staging announces each run ~48h early. A shortener stats page is a "
          "better sensor than victim telemetry.")

READ = [
    "Box fill = phase or evidence grade; dot = evidence confidence "
    "(green observed \u00b7 orange reported \u00b7 gray inference).",
    "Date pills order the chapters; runs sharing a toolkit is observed \u2014 "
    "one campaign behind them is inference.",
    "Grades describe evidence strength, not legal findings.",
]
SRC = ("Source: swarmtraces-hf-corpus datasets + Elastic indices (Sep 2026). "
       "Shared toolkit proves shared tooling, not shared ownership.")

# ---------------------------------------------------------------- sections ---
def sect_head(fl, meta):
    fl.skip(6)
    fl.text(MARGIN + PAD, f"{meta['num']}  \u00b7  {meta['title']}", f_sect,
            meta["accent"])
    fl.skip(4)
    fl.text(MARGIN + PAD, meta["sub"], f_sectsub, MUTED)
    fl.skip(26)

def panel_begin(fl):
    y0 = fl.y - 34
    return y0

def panel_end(fl, y0):
    y1 = fl.y + PAD - 8
    prect([MARGIN, y0, W - MARGIN, y1], R_PANEL, PANEL, PANEL_BD, 2)

def header(fl):
    fl.skip(MARGIN)
    fl.text(MARGIN, HEADER_TITLE, f_title, TEXT)
    fl.skip(18)
    fl.text(MARGIN, HEADER_SUB, f_sub, MUTED, max_w=CW)
    fl.skip(6)
    fl.text(MARGIN, HEADER_SUB2, f_sub, MUTED, max_w=CW)
    fl.skip(14)
    fl.text(MARGIN, HEADER_HEDGE, f_hedge, FAINT, max_w=CW)
    fl.skip(26)
    # legend row with dots
    x = MARGIN
    lh = th(f_legend)
    max_y = fl.y
    for color, label in LEGEND:
        r = 9
        if fl.draw:
            fl.draw.ellipse([x, fl.y + lh // 2 - r, x + 2 * r, fl.y + lh // 2 + r],
                            fill=color)
        x += 2 * r + 12
        if fl.draw:
            fl.draw.text((x, fl.y), label, font=f_legend, fill=MUTED)
        x += tw(f_legend, label) + 34
        if x > W - MARGIN - 200:
            x = MARGIN
            fl.y += lh + 14
    fl.y += lh + 10
    fl.skip(10)

def panel1(fl):
    y0 = panel_begin(fl)
    sect_head(fl, P1)
    inner = CW - 2 * PAD
    n = len(P1_BOXES)
    arrow_zone = 92
    bw = (inner - (n - 1) * arrow_zone) / n
    # measure box heights
    bh = 0
    for b in P1_BOXES:
        h = 30  # top pad
        h += th(f_nname) + 6 + th(f_ntype) + 14
        h += th(f_tline) + 12
        lines = wrap(b["body"], f_body, bw - 56)
        h += block_h(lines, f_body, 8)
        h += 30  # bottom pad
        bh = max(bh, h)
    x = MARGIN + PAD
    top = fl.y
    for i, b in enumerate(P1_BOXES):
        urect([x, top, x + bw, top + bh], R_NODE, tint(b["color"]),
              b["color"], 3)
        # name + dot + type label + T-line + body (drawn in content pass)
        fl2_y = top + 30
        if fl.draw:
            fl.draw.text((x + 28, fl2_y), b["name"], font=f_nname, fill=b["color"])
            fl.dot(x + bw - 30, fl2_y + th(f_nname) // 2, 9, b["dot"])
        fl2_y += th(f_nname) + 6
        if fl.draw:
            fl.draw.text((x + 28, fl2_y), b["typ"], font=f_ntype, fill=FAINT)
        fl2_y += th(f_ntype) + 14
        if fl.draw:
            fl.draw.text((x + 28, fl2_y), b["t"], font=f_tline, fill=TEXT)
        fl2_y += th(f_tline) + 12
        if fl.draw:
            for ln in wrap(b["body"], f_body, bw - 56):
                fl.draw.text((x + 28, fl2_y), ln, font=f_body, fill=MUTED)
                fl2_y += th(f_body) + 8
        if i < n - 1 and fl.draw:
            fl.arrow(x + bw + 14, x + bw + arrow_zone - 14, top + bh / 2)
        x += bw + arrow_zone
    fl.y = top + bh
    fl.skip(24)
    fl.text(MARGIN + PAD, P1_CAP, f_body, FAINT, max_w=inner)
    fl.skip(6)
    panel_end(fl, y0)

def panel2(fl):
    y0 = panel_begin(fl)
    sect_head(fl, P2)
    inner = CW - 2 * PAD
    pill_w = 210
    gapx = 36
    text_w = inner - pill_w - gapx - 48   # reserve room for confidence dot
    dot_x = MARGIN + PAD + inner - 12
    for ch in P2_CH:
        title_h = th(f_chtitle)
        lines = wrap(ch["body"], f_chbody, text_w)
        body_h = block_h(lines, f_chbody, 8)
        pill_h = th(f_pill) + 36
        row_h = max(pill_h, title_h + 10 + body_h)
        top = fl.y
        # pill
        urect([MARGIN + PAD, top + (row_h - pill_h) / 2,
               MARGIN + PAD + pill_w, top + (row_h - pill_h) / 2 + pill_h],
              pill_h // 2, tint(ch["color"]), ch["color"], 3)
        if fl.draw:
            d = fl.draw
            tw_ = tw(f_pill, ch["date"])
            d.text((MARGIN + PAD + (pill_w - tw_) / 2,
                    top + (row_h - pill_h) / 2 + (pill_h - th(f_pill)) / 2 - 2),
                   ch["date"], font=f_pill, fill=ch["color"])
        tx = MARGIN + PAD + pill_w + gapx
        ty = top + (row_h - (title_h + 10 + body_h)) / 2
        if fl.draw:
            fl.draw.text((tx, ty), ch["title"], font=f_chtitle, fill=TEXT)
            fl.dot(dot_x, ty + title_h // 2, 8, ch["dot"])
        ty += title_h + 10
        if fl.draw:
            for ln in lines:
                fl.draw.text((tx, ty), ln, font=f_chbody, fill=MUTED)
                ty += th(f_chbody) + 8
        fl.y = top + row_h
        fl.skip(30)
    fl.skip(-6)
    fl.text(MARGIN + PAD, P2_FOOT, f_body, FAINT, max_w=inner)
    fl.skip(6)
    panel_end(fl, y0)

def panel3(fl):
    y0 = panel_begin(fl)
    sect_head(fl, P3)
    inner = CW - 2 * PAD
    for r in P3_ROWS:
        pill_w = tw(f_grade, r["grade"]) + 56
        pill_h = th(f_grade) + 34
        gapx = 36
        text_w = inner - pill_w - gapx - 48   # reserve room for confidence dot
        dot_x = MARGIN + PAD + inner - 12
        lines = wrap(r["desc"], f_desc, text_w)
        desc_h = block_h(lines, f_desc, 8)
        row_h = max(pill_h, desc_h)
        top = fl.y
        urect([MARGIN + PAD, top + (row_h - pill_h) / 2,
               MARGIN + PAD + pill_w, top + (row_h - pill_h) / 2 + pill_h],
              pill_h // 2, tint(r["color"]), r["color"], 3)
        if fl.draw:
            d = fl.draw
            d.text((MARGIN + PAD + 28,
                    top + (row_h - pill_h) / 2 + (pill_h - th(f_grade)) / 2 - 2),
                   r["grade"], font=f_grade, fill=r["color"])
            fl.dot(dot_x,
                   top + desc_h // 2 if desc_h > 0 else top + row_h / 2,
                   8, r["dot"])
        tx = MARGIN + PAD + pill_w + gapx
        ty = top + (row_h - desc_h) / 2
        if fl.draw:
            for ln in lines:
                fl.draw.text((tx, ty), ln, font=f_desc, fill=MUTED)
                ty += th(f_desc) + 8
        fl.y = top + row_h
        fl.skip(28)
    fl.skip(-4)
    panel_end(fl, y0)

def panel4(fl):
    y0 = panel_begin(fl)
    sect_head(fl, P4)
    inner = CW - 2 * PAD
    gapx = 40
    bw = (inner - gapx) / 2
    # measure
    bh = 0
    for b in P4_BOXES:
        h = 30 + th(f_nname) + 6 + th(f_ntype) + 14
        lines = wrap(b["body"], f_body, bw - 56)
        h += block_h(lines, f_body, 8) + 30
        bh = max(bh, h)
    x = MARGIN + PAD
    top = fl.y
    for b in P4_BOXES:
        urect([x, top, x + bw, top + bh], R_NODE, tint(b["color"]),
              b["color"], 3)
        yy = top + 30
        if fl.draw:
            fl.draw.text((x + 28, yy), b["name"], font=f_nname, fill=b["color"])
            fl.dot(x + bw - 30, yy + th(f_nname) // 2, 9, b["dot"])
        yy += th(f_nname) + 6
        if fl.draw:
            fl.draw.text((x + 28, yy), b["typ"], font=f_ntype, fill=FAINT)
        yy += th(f_ntype) + 14
        if fl.draw:
            for ln in wrap(b["body"], f_body, bw - 56):
                fl.draw.text((x + 28, yy), ln, font=f_body, fill=MUTED)
                yy += th(f_body) + 8
        x += bw + gapx
    fl.y = top + bh
    fl.skip(24)
    fl.text(MARGIN + PAD, P4_CAP, f_body, FAINT, max_w=inner)
    fl.skip(6)
    panel_end(fl, y0)

def footer(fl):
    fl.skip(34)
    fl.text(MARGIN, "How to read", f_fhead, TEXT)
    fl.skip(14)
    for b in READ:
        fl.text(MARGIN, "\u00b7  " + b, f_bullet, MUTED, max_w=CW)
        fl.skip(10)
    fl.skip(18)
    fl.text(MARGIN, SRC, f_src, FAINT, max_w=CW)
    fl.skip(MARGIN)

# ------------------------------------------------------------------- build ---
def layout(draw=None):
    global under_rects, panel_rects
    under_rects = []
    panel_rects = []
    fl = Flow(draw)
    header(fl)
    fl.skip(GAP_PANEL)
    panel1(fl)
    fl.skip(GAP_PANEL)
    panel2(fl)
    fl.skip(GAP_PANEL)
    panel3(fl)
    fl.skip(GAP_PANEL)
    panel4(fl)
    footer(fl)
    return fl.y, list(panel_rects), list(under_rects)

def main():
    total_h, _, _ = layout(None)
    H = int(total_h + 8)
    img = Image.new("RGBA", (W, H), BG + (255,))
    # under-layer, back to front: panel bgs, then node/pill fills + borders
    _, panel_rr, under_rr = layout(None)
    under = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ud = ImageDraw.Draw(under)
    for xy, radius, fill, outline, width in panel_rr + under_rr:
        ud.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline,
                             width=width)
    img = Image.alpha_composite(img, under)
    draw = ImageDraw.Draw(img)
    layout(draw)
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "notes", "eval-cti-brief-2026-09-28-v2.png")
    img.convert("RGB").save(out)
    print(f"wrote {out}  {W}x{H}")

if __name__ == "__main__":
    main()
