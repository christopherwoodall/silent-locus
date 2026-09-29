#!/usr/bin/env python3
"""YOURLS re-sweep fetcher (2026-09-28, lane yourls-resweep).

Read-only: plain GETs of public stats/preview/info pages only.
Polite pacing (3s between requests), single retry, 30s timeout.
No logins, no form submissions, no API-write endpoints, no link creation.
Saves raw HTML under data/yourls-resweep-2026-09-28/evidence/ with a
provenance header prepended.
"""
import os, time, subprocess
from datetime import datetime, timezone

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUTDIR = os.path.join(BASE, "data", "yourls-resweep-2026-09-28", "evidence")
LOG = os.path.join(BASE, "data", "yourls-resweep-2026-09-28", "progress.log")
os.makedirs(OUTDIR, exist_ok=True)

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

TARGETS = [
    ("unm_7t6-o",      "https://goto.unm.edu/7t6-o+"),
    ("unm_discvr",      "https://goto.unm.edu/discvr+"),
    ("unm_reso",        "https://goto.unm.edu/reso+"),
    ("unm_urphy21",     "https://goto.unm.edu/urphy21+"),
    ("unm_vbudg",       "https://goto.unm.edu/vbudg+"),
    ("eth_nB1nv",       "https://u.ethz.ch/nB1nv+?jqpaccess=1"),
    ("uvm_-4s0q",       "https://go.uvm.edu/-4s0q+"),
    ("uvm_tgmtq",       "https://go.uvm.edu/tgmtq+"),
    ("uvm_xc26",        "https://go.uvm.edu/xc26+"),
    ("popcat_5vtSk2RG2f", "https://url.popcat.xyz/5vtSk2RG2f/info"),
    ("popcat_IRZTIxDlZ",  "https://url.popcat.xyz/IRZTIxDlZ/info"),
    ("tmdc_frontpage",  "https://t.mdcdev.me/"),
    ("tmdc_robots",     "https://t.mdcdev.me/robots.txt"),
    ("tmdc_sitemap",    "https://t.mdcdev.me/sitemap.xml"),
    ("tmdc_squarespacefreeemail934785", "https://t.mdcdev.me/squarespacefreeemail934785+"),
    ("tmdc_evegelendiyarbakrescort772509", "https://t.mdcdev.me/evegelendiyarbakrescort772509+"),
    ("tmdc_mattressstoresaroundmyarea909270", "https://t.mdcdev.me/mattressstoresaroundmyarea909270+"),
    ("uoft_maagentxyz99999", "https://uoft.me/maagentxyz99999+"),
]

def log(msg):
    line = "[%s] %s\n" % (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), msg)
    with open(LOG, "a") as f:
        f.write(line)
    print(line, end="")

def fetch(name, url):
    out = os.path.join(OUTDIR, "%s_resweep_2026-09-28.html" % name)
    for attempt in (1, 2):
        try:
            r = subprocess.run(
                ["curl", "-sS", "-L", "--compressed", "--max-time", "45",
                 "--retry", "1", "-A", UA, "-o", out + ".body", "-w",
                 "%{http_code} %{size_download}", url],
                capture_output=True, text=True, timeout=60)
            meta = r.stdout.strip().split()
            status, size = (meta + ["?", "?"])[:2]
            body = b""
            if os.path.exists(out + ".body"):
                with open(out + ".body", "rb") as f:
                    body = f.read()
                os.remove(out + ".body")
            header = ("SOURCE: %s\nRETRIEVED: %s via read-only GET (attempt %d)\n"
                      "HTTP_STATUS: %s\nBYTES: %d\nCURL_STDERR: %s\n\n"
                      % (url, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         attempt, status, len(body), r.stderr.strip()[:200]))
            with open(out, "wb") as f:
                f.write(header.encode("utf-8") + body)
            ok = status.startswith("2") and len(body) > 500
            log("FETCH %s %s -> %s (http %s, %d bytes)" % ("ok" if ok else "thin", name, url, status, len(body)))
            if ok:
                return True
        except Exception as e:
            log("FETCH fail %s attempt %d: %r" % (name, attempt, e))
        time.sleep(5)
    return False

def main():
    log("fetch start: %d targets, 3s pacing" % len(TARGETS))
    ok = 0
    for name, url in TARGETS:
        if fetch(name, url):
            ok += 1
        time.sleep(3)
    log("fetch done: %d/%d ok" % (ok, len(TARGETS)))

if __name__ == "__main__":
    main()
