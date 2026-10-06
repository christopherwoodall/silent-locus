#!/usr/bin/env python3
"""v2: dense X/research figure cards for the skill-egress scan. 1200x675 PNGs."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top500/egress-live-scan/cards")
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 675
BG = (11, 14, 20)
AMBER = (245, 165, 36)
CYAN = (34, 211, 238)
GREEN = (52, 211, 153)
RED = (248, 113, 113)
WHITE = (242, 245, 249)
GRAY = (154, 164, 178)
DIM = (105, 115, 130)
SOBG = (32, 26, 12)

FB = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FMD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FDVB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(p, s): return ImageFont.truetype(p, s)
F_kicker = font(FMD, 19)
F_title = font(FB, 50)
F_head = font(FB, 28)
F_body = font(FR, 24)
F_small = font(FR, 21)
F_foot = font(FMD, 17)
F_bignum = font(FB, 76)
F_mono = font(FMD, 22)
F_arrow = font(FDVB, 38)

def base(kicker, title):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=AMBER)
    d.rectangle([48, 36, 1152, H - 36], outline=(38, 48, 66), width=2)
    d.text((70, 56), kicker, font=F_kicker, fill=CYAN)
    d.text((70, 88), title, font=F_title, fill=WHITE)
    d.line([70, 164, 1130, 164], fill=(38, 48, 66), width=2)
    return img, d

def footer(d, text):
    d.text((70, H - 66), text, font=F_foot, fill=DIM)

def bullet(d, x, y, text, color=WHITE, f=F_body):
    d.ellipse([x, y + 8, x + 9, y + 17], fill=color)
    d.text((x + 24, y), text, font=f, fill=WHITE)
    return y + 36

def sowhat(d, text):
    y0, y1 = 528, 588
    d.rectangle([70, y0, 1130, y1], fill=SOBG)
    d.rectangle([70, y0, 78, y1], fill=AMBER)
    d.text((70, y0 - 26), "SO WHAT", font=font(FMD, 18), fill=AMBER)
    # wrap
    words, lines, cur = text.split(" "), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=F_body) <= 1000: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur)
    yy = y0 + 8
    for ln in lines[:2]:
        d.text((94, yy), ln, font=F_body, fill=WHITE); yy += 30

def save(img, name):
    p = os.path.join(OUT, name); img.save(p); print("wrote", p)

def star_title(d, before, after):
    x, y = 70, 88
    d.text((x, y), before, font=F_title, fill=WHITE); x += d.textlength(before, font=F_title)
    d.text((x, y), "★ ", font=font(FMD, 50), fill=AMBER); x += d.textlength("★ ", font=font(FMD, 50))
    d.text((x, y), after, font=F_title, fill=WHITE)

# ---- 1: scorecard ----
img, d = base("SKILL EGRESS STUDY · LIVE PROBE 2026-10-05", "The egress scorecard")
d.text((70, 182), "r.jina.ai keyless is DEAD — the study's #2 egress primitive is gone.", font=F_head, fill=AMBER)
d.text((70, 232), "LIVE (7)", font=font(FMD, 22), fill=GREEN)
y = 264
for t in ["ngrok.com · cloudflarestatus.com", "uploads.github.com",
          "Discord + Slack webhook docs", "localcan GH repo · roamzy.io"]:
    y = bullet(d, 70, y, t, GREEN) - 4
d.text((660, 232), "DEAD / UNREACHABLE (3)", font=font(FMD, 22), fill=RED)
bullet(d, 660, 264, "r.jina.ai — 25s timeout", RED)
d.text((684, 296), "(control fetch OK — jina-specific)", font=F_small, fill=GRAY)
bullet(d, 660, 326, "catbox.moe · sci-hub.se", RED)
d.text((684, 358), "(one attempt each — down or path-filtered)", font=F_small, fill=GRAY)
d.text((70, 420), "Dead-drop layer fully alive: webhooks, GitHub uploads, ngrok all reachable.", font=F_body, fill=WHITE)
d.text((70, 456), "Effect: agents keep the exfil path; only the free reader proxy died.", font=F_small, fill=GRAY)
sowhat(d, "Keyless jina dead > relay shifts to keyed tier or self-hosted readers. Watch skill updates for new reader domains.")
footer(d, "one public GET per endpoint · ~3s pacing · no auth, no payloads · single egress path")
save(img, "card-1-scorecard.png")

# ---- 2: inversion ----
img, d = base("SKILL EGRESS STUDY · TRADECRAFT", "The inversion")
d.text((70, 182), "webhook.site", font=F_head, fill=RED)
d.text((70, 218), "0 hits in 3,853 skill units · CONFIRMED in 4 incident campaigns", font=F_body, fill=WHITE)
d.text((70, 252), "UNCTAD bridge c773aa22 · AIHW liveness inboxes · fleet 2026-10-04", font=F_small, fill=GRAY)
d.text((70, 296), "httpbun", font=F_head, fill=RED)
d.text((70, 332), "0 hits in 3,853 skill units · 1,096 urlquery rows · AIHW exfil ladder", font=F_body, fill=WHITE)
d.text((70, 366), "GO exfils AIHW ZIP 4KB at a time · fleet /anything/gcresult dead-drop", font=F_small, fill=GRAY)
d.text((70, 412), "Observed exfil grammar:", font=F_small, fill=CYAN)
d.text((70, 440), "href.li > httpbun/base64 > sendBeacon > webhook.site", font=F_mono, fill=AMBER)
sowhat(d, "Code-only skill audits miss the incident playbook entirely. You have to monitor both worlds — the supply chain and the wire.")
footer(d, "silent-locus incident corpora · urlquery hunt dataset · 2026-10-05")
save(img, "card-2-inversion.png")

# ---- 3: bearer ----
img, d = base("SKILL EGRESS STUDY · CRYPTOGRAPHER", "Bearer credentials")
d.text((70, 182), "Discord webhook token ~ 408 bits · Slack ~ 143 bits", font=F_head, fill=CYAN)
y = bullet(d, 70, 232, "Threat is disclosure, not brute force. One leak =", WHITE)
d.text((94, 262), "impersonation + forged alerts + silent webhook deletion (operator blinded).", font=F_small, fill=GRAY)
y = bullet(d, 70, 300, "Bitwarden via MCP: not one bearer token — all of them at once.", AMBER)
d.text((94, 330), "TOTP seeds in MCP memory = 2FA bypass material. One confused deputy = whole vault.", font=F_small, fill=GRAY)
y = bullet(d, 70, 368, "r.jina.ai terminates TLS: every fetched URL in plaintext,", AMBER)
d.text((94, 398), "including query-string API keys, signed URLs, session tokens.", font=F_small, fill=GRAY)
y = bullet(d, 70, 436, "ngrok: the random public URL is the entire access control — no auth by default.", AMBER)
sowhat(d, "One leaked webhook URL forges operator alerts. One vault read takes every credential. Audit where these strings land: logs, commits, dashboards.")
footer(d, "full analysis: egress-live-scan/cryptographer/FINDINGS.md")
save(img, "card-3-bearer.png")

# ---- 4: esim ----
img, d = base("SKILL EGRESS STUDY · RECON · GENUINELY NEW", "An agent can buy a phone")
d.text((70, 182), "Roamzy eSIM: anonymous no-KYC mobile identity, bought with crypto, via MCP.", font=F_body, fill=WHITE)
y = 224
for t in ["193 countries · account minted on first call · $20 min top-up",
          "20%-forever USDT referral incentive — in anonymous mode",
          "Zero security literature on agents buying telecom identity"]:
    y = bullet(d, 70, y, t, CYAN) - 4
d.text((70, 352), "What it buys the agent:", font=F_small, fill=CYAN)
y = 382
for t in ["SMS verification at scale (sybil accounts)", "2FA interception on victim numbers", "Out-of-band C2 outside any monitored egress"]:
    y = bullet(d, 70, y, t, WHITE, F_small) - 6
sowhat(d, "Crypto-funded telecom = sybil identities + 2FA interception that no DNS resolver or egress monitor ever sees. The referral turns it into a self-propagating loop.")
footer(d, "passive intel only · Shodan stored observations · public docs · 2026-10-05")
save(img, "card-4-esim.png")

# ---- 5: seen-list ----
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
d.rectangle([0, 0, W, 6], fill=AMBER)
d.rectangle([48, 36, 1152, H - 36], outline=(38, 48, 66), width=2)
d.text((70, 56), "SKILL EGRESS STUDY · CORPUS VERDICT", font=F_kicker, fill=CYAN)
star_title(d, "The ", "seen-list")
d.line([70, 164, 1130, 164], fill=(38, 48, 66), width=2)
rows = [
    ("★ r.jina.ai", "confirmed both · 618 urlquery rows · Transluce 2026-09-23 rung-2 relay", GREEN),
    ("★ catbox", "confirmed both · single row, epoch-nonce, campaign “reader-proxy-ops”", GREEN),
    ("★ ngrok · discord · uploads.github", "skill code only · zero incident-corpus usage", CYAN),
    ("★ webhook.site · httpbun", "incidents only — absent from all 3,853 scanned units", AMBER),
    ("NEW", "sci-hub+verify=False · Bitwarden · eSIM · pinme receiver · LocalCan", WHITE),
]
y = 182
for label, desc, color in rows:
    d.text((70, y), label, font=font(FMD, 21), fill=color)
    d.text((70, y + 28), desc, font=F_small, fill=GRAY)
    y += 62
sowhat(d, "The overlap is the tripwire set: jina, catbox, ngrok, discord appear in BOTH worlds. New sightings there are the highest-signal alerts.")
footer(d, "PixelLeak/Glow Labs 2026-09-30 · SANS ISC 2026-07-17 · Transluce 2026-09-23 · wikiservice.at audit")
save(img, "card-5-seenlist.png")

# ---- 6: funnel ----
img, d = base("SKILL EGRESS STUDY · 2026-10-05", "The funnel")
nums = [("358", "skill identities"), ("177", "repos / packages"), ("3,853", "units scanned"), ("800", "egress hits")]
x = 70
for n, label in nums:
    d.text((x, 210), n, font=F_bignum, fill=WHITE)
    d.text((x, 300), label, font=F_small, fill=GRAY)
    if n != "800": d.text((x + 228, 232), "→", font=F_arrow, fill=AMBER)
    x += 285
d.text((70, 370), "216 GitHub-stars lane · 142 marketplace lane", font=F_body, fill=CYAN)
d.text((70, 406), "Claude skills 3,392 · Cursor/MCP 317 · Marketplace 144", font=F_small, fill=GRAY)
d.text((70, 442), "20.8% of scanned units have egress hits — better than 1 in 5.", font=F_head, fill=AMBER)
sowhat(d, "1 in 5 skill units can reach the network. Audit the capability, not the intent — dual-use surface on legitimate tools is not an accusation.")
footer(d, "studies/skill-egress-top500 · EGRESS_MAP.md")
save(img, "card-6-funnel.png")
print("done")
