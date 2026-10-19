#!/usr/bin/env python3
"""Harbor inventory builder: all unique hosts -> host-inventory.jsonl."""
import json, os
from collections import Counter

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/cairn-panels")
SR = os.path.join(BASE, "raw/search-results")
HR = os.path.join(BASE, "raw/hosts")

def load(name):
    out = []
    with open(os.path.join(SR, name)) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out

sets = {
    "cairn": load("cairn-banners.jsonl"),
    "strix": load("strix-banners.jsonl"),
    "hermes": load("hermes-dashboard-banners.jsonl"),
    "hermes-chinese": load("hermes-chinese-login-banners.jsonl"),
    "hermes-product": load("hermes-product-banners.jsonl"),
    "cairn-login": load("cairn-login-banners.jsonl"),
}
PRODUCT_COVERAGE_NOTE = ("partial: Shodan deep-pagination cutoff at ~4,200 banners "
                         "(total reported 5,499); ~1,300 banners unreachable; per-country split "
                         "fetch failed when API credits exhausted")

pulled = {fn[:-5] for fn in os.listdir(HR) if fn.endswith(".json") and not fn.endswith(".PROVENANCE.txt") and not fn.endswith(".sha256")}
pulled = {p for p in pulled if os.path.exists(os.path.join(HR, p + ".json"))}

def full_ports(ip):
    try:
        d = json.load(open(os.path.join(HR, ip + ".json")))
        return sorted(d.get("ports") or [])
    except Exception:
        return None

hosts = {}  # ip -> merged banner info
for harness, banners in sets.items():
    for m in banners:
        ip = m["ip_str"]
        h = hosts.setdefault(ip, {"harnesses": set(), "banners": []})
        h["harnesses"].add(harness)
        h["banners"].append(m)

TS = None
import datetime
inv_lines = []
def ipkey(x):
    try:
        return (0, tuple(int(o) for o in x.split(".")))
    except ValueError:
        return (1, x)
for ip in sorted(hosts, key=ipkey):
    h = hosts[ip]
    ms = h["banners"]
    loc = ms[0].get("location") or {}
    ports_banner = sorted({m["port"] for m in ms})
    titles = sorted({((m.get("http") or {}).get("title") or "") for m in ms})
    timestamps = sorted({m.get("timestamp") for m in ms if m.get("timestamp")})
    tags = sorted({t for m in ms for t in (m.get("tags") or [])})
    harness_list = sorted(h["harnesses"])

    # panel status
    if "cairn" in h["harnesses"] or "cairn-login" in h["harnesses"]:
        status = "login_gated" if any("login" in t.lower() for t in titles) else "open_dashboard"
    elif "strix" in h["harnesses"]:
        status = "open_dashboard"  # title/favicon visible to scanners; viewer is token-gated by design
    elif any(x.startswith("hermes") for x in h["harnesses"]):
        if any(t == "Hermes Agent - Dashboard" for t in titles):
            status = "open_dashboard"
        elif any(k in t for t in titles for k in ("Sign in", "登录", "Login", "401", "Вход", "로그인", "验证")):
            status = "login_gated"
        else:
            status = "unknown"
    else:
        status = "unknown"

    notes = []
    if ip in pulled:
        notes.append("full host record pulled: raw/hosts/%s.json" % ip)
        fp = full_ports(ip)
        ports = fp if fp else ports_banner
        d = json.load(open(os.path.join(HR, ip + ".json")))
        for s in d.get("data", []):
            prod = (s.get("product") or "")
            pl = prod.lower()
            if "cobalt strike" in pl:
                notes.append("CO-LOCATION: Cobalt Strike C2 on port %s (Shodan product fingerprint)" % s.get("port"))
            if "openclaw" in pl:
                notes.append("CO-LOCATION: OpenClaw on port %s (Shodan product fingerprint)" % s.get("port"))
            if any(k in pl for k in ("frp", "ngrok", "chisel", "gost", "nps", "metasploit", "teamserver", "sliver")):
                notes.append("CO-LOCATION: %s on port %s (Shodan product fingerprint)" % (prod, s.get("port")))
        htags = d.get("tags") or []
        if "c2" in htags:
            notes.append("Shodan tags this host: c2")
    else:
        ports = ports_banner
        notes.append("banner-level only (no full host pull; Shodan API credit budget)")

    if ip == "47.97.206.32":
        notes.append("Sextant flag: Cairn-Login (uvicorn) on 8000 + Cobalt Strike C2 on 50050, Aliyun CN")
    if (loc.get("country_code")) == "IR":
        notes.append("sanctioned-geo hosting (IR)")
    def collapse(x):
        if x.startswith("hermes"): return "hermes"
        if x.startswith("cairn"): return "cairn"
        return x
    collapsed = {collapse(x) for x in harness_list}
    if len(collapsed) > 1:
        notes.append("CROSS-HARNESS: matched queries for " + ",".join(sorted(collapsed)))
    if "hermes-product" in h["harnesses"]:
        notes.append("from product-query banner set (" + PRODUCT_COVERAGE_NOTE + ")")

    entry = {
        "ip": ip,
        "harness": "hermes" if any(x.startswith("hermes") for x in harness_list) else harness_list[0],
        "harness_queries_matched": harness_list,
        "ports": ports,
        "org": ms[0].get("org"),
        "asn": ms[0].get("asn"),
        "isp": ms[0].get("isp"),
        "country": loc.get("country_code"),
        "city": loc.get("city"),
        "hostnames": ms[0].get("hostnames", []),
        "panel_status": status,
        "titles_seen": titles,
        "shodan_tags": tags,
        "first_seen_utc": timestamps[0] if timestamps else None,
        "banner_count": len(ms),
        "full_record_pulled": ip in pulled,
        "notes": notes,
    }
    inv_lines.append(entry)

with open(os.path.join(BASE, "working/host-inventory.jsonl"), "w") as f:
    for e in inv_lines:
        f.write(json.dumps(e) + "\n")

print(f"inventory lines: {len(inv_lines)}")
print("by harness:", Counter(e["harness"] for e in inv_lines))
print("by status:", Counter(e["panel_status"] for e in inv_lines))
print("by country:", Counter(e["country"] for e in inv_lines).most_common(12))
print("by asn:", Counter(e["asn"] for e in inv_lines).most_common(12))
print("full pulled:", sum(1 for e in inv_lines if e["full_record_pulled"]))
print("multi-harness hosts:", [e["ip"] for e in inv_lines if len(e["harness_queries_matched"]) > 1])
