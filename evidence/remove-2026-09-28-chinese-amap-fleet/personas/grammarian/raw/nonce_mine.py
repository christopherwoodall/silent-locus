#!/usr/bin/env python3
"""Mine local urlquery corpora for nonce/tag VALUE encodings in submitted URLs.

Offline: walks every JSON under ~/workspace/silent-locus/data that carries
urlquery reports, extracts (param_name x value_encoding) pairs, aggregates
distinct reports / time span / burst shape / target family.

Excluded (known): uq labels <word><YYYYMMDD>[letter] and 19-digit ?x= values.
"""
import json, re, sys, os
from urllib.parse import urlparse, parse_qsl, unquote
from collections import defaultdict
from datetime import datetime

ROOT = os.path.expanduser("~/workspace/silent-locus/data")
OUTDIR = os.path.expanduser(
    "~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw")

UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                     r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
HEX_RE = re.compile(r"^[0-9a-fA-F]+$")
DIG_RE = re.compile(r"^\d+$")
UQ_LABEL_RE = re.compile(
    r"^[a-zA-Z]+(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[a-zA-Z]?$")
DATE_EMBED_RE = re.compile(r"(19|20)\d{2}-?\d{2}-?\d{2}")
B64_RE = re.compile(r"^[A-Za-z0-9+/=_-]{20,}$")
EPOCH10_RE = re.compile(r"^1[4-9]\d{8}$")
EPOCH13_RE = re.compile(r"^1[4-9]\d{11}$")


def classify(v):
    v = v.strip()
    if not v:
        return "empty"
    if DIG_RE.match(v):
        if len(v) == 19:
            return "digits19"          # known uq
        if EPOCH10_RE.match(v):
            return "epoch10"
        if EPOCH13_RE.match(v):
            return "epoch13"
        if len(v) >= 12:
            return f"digits{len(v)}"
        if len(v) <= 4:
            return "counter"
        return "digits_small"
    if UUID_RE.match(v):
        return "uuid"
    if HEX_RE.match(v):
        n = len(v)
        if n == 16:
            return "hex16"
        if n == 32:
            return "hex32"
        if n == 64:
            return "hex64"
        if n >= 8:
            return f"hex{n}"
        return "hex_small"
    if UQ_LABEL_RE.match(v):
        return "uq_label"              # known uq
    if DATE_EMBED_RE.search(v):
        return "date_embed"
    if B64_RE.match(v) and re.search(r"[0-9]", v) and re.search(r"[A-Za-z]", v) \
            and not re.match(r"^[a-zA-Z]+$", v) and len(v) >= 20:
        return "base64ish"
    if re.match(r"^[a-zA-Z]+$", v) and len(v) >= 12:
        return "longword"
    if len(v) <= 8 and re.match(r"^[\w-]+$", v):
        return "short_token"
    return "other"


def iter_reports(path):
    try:
        with open(path, errors="replace") as f:
            d = json.load(f)
    except Exception:
        return
    reps = []
    if isinstance(d, dict):
        reps = d.get("reports") or d.get("results") or []
    elif isinstance(d, list):
        reps = d
    for r in reps:
        if not isinstance(r, dict):
            continue
        url = r.get("url")
        if isinstance(url, dict):
            u = url.get("addr") or ""
            sch = url.get("schema") or "http"
            if u and "://" not in u:
                u = f"{sch}://{u}"
        else:
            u = url or ""
        if not u:
            continue
        yield r.get("report_id"), u, r.get("date") or r.get("timestamp")


agg = defaultdict(lambda: {"reports": set(), "dates": [],
                            "vals": [], "domains": defaultdict(int)})

n_files = n_reports = n_params = 0
for dirpath, _, files in os.walk(ROOT):
    # skip our own persona raw dir to avoid double counting
    if "personas/grammarian" in dirpath:
        continue
    for fn in files:
        if not fn.endswith(".json"):
            continue
        p = os.path.join(dirpath, fn)
        n_files += 1
        for rid, url, date in iter_reports(p):
            n_reports += 1
            try:
                pr = urlparse(url)
                domain = (pr.hostname or "").lower()
                qs = parse_qsl(pr.query, keep_blank_values=True)
            except Exception:
                continue
            # classify param NAMES too (some labels ride as names)
            for name, val in qs:
                n_params += 1
                v = unquote(val)
                enc = classify(v)
                nenc = classify(unquote(name))
                key = (name.lower(), enc)
                a = agg[key]
                if rid:
                    a["reports"].add(rid)
                a["dates"].append(date)
                if len(a["vals"]) < 8:
                    a["vals"].append(v[:120])
                a["domains"][domain] += 1
                if nenc in ("uq_label", "date_embed", "uuid", "hex32",
                            "epoch10", "epoch13", "digits19"):
                    key2 = ("<NAME>:" + name.lower(), nenc)
                    a2 = agg[key2]
                    if rid:
                        a2["reports"].add(rid)
                    a2["dates"].append(date)
                    if len(a2["vals"]) < 8:
                        a2["vals"].append(v[:120])
                    a2["domains"][domain] += 1

print(f"files={n_files} reports={n_reports} params={n_params} pairs={len(agg)}",
      file=sys.stderr)

def dts(ds):
    ds = sorted(d for d in ds if d)
    return (ds[0], ds[-1]) if ds else (None, None)

rows = []
for (param, enc), a in agg.items():
    if enc in ("other", "empty", "short_token", "counter", "digits_small",
               "hex_small", "longword"):
        continue
    if enc == "uq_label" and not param.startswith("<NAME>"):
        # uq labels are known regardless of param; keep values only in detail
        pass
    lo, hi = dts(a["dates"])
    rows.append({
        "param": param,
        "encoding": enc,
        "distinct_reports": len(a["reports"]),
        "first": lo, "last": hi,
        "top_domains": sorted(a["domains"].items(),
                              key=lambda kv: -kv[1])[:5],
        "sample_values": a["vals"][:5],
    })
rows.sort(key=lambda r: -r["distinct_reports"])

out = {"meta": {"files": n_files, "reports_scanned": n_reports,
                "params_scanned": n_params, "generated": datetime.utcnow()
                .isoformat() + "Z"},
       "pairs": rows}
os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, "nonce-01-local-mine.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"wrote nonce-01-local-mine.json with {len(rows)} pairs")
# print top 60 for the verdict pass
for r in rows[:60]:
    print(f"{r['distinct_reports']:6d}  {r['param'][:40]:42s} {r['encoding']:12s} "
          f"{str(r['first'])[:10]}..{str(r['last'])[:10]} "
          f"{','.join(d for d, _ in r['top_domains'][:2])[:60]}")
