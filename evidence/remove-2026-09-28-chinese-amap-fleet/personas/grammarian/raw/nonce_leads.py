#!/usr/bin/env python3
"""Pull full submitted URLs for specific (param x encoding) leads from local corpus."""
import json, os, re
from urllib.parse import urlparse, parse_qsl, unquote

ROOT = os.path.expanduser("~/workspace/silent-locus/data")
seen = set()

def iter_reports():
    for dirpath, _, files in os.walk(ROOT):
        if "personas/grammarian" in dirpath:
            continue
        for fn in files:
            if not fn.endswith(".json"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                d = json.load(open(p, errors="replace"))
            except Exception:
                continue
            reps = d.get("reports") if isinstance(d, dict) else d
            if not isinstance(reps, list):
                continue
            for r in reps:
                if not isinstance(r, dict):
                    continue
                url = r.get("url")
                if isinstance(url, dict):
                    u = url.get("addr") or ""
                    if u and "://" not in u:
                        u = "http://" + u
                else:
                    u = url or ""
                rid = r.get("report_id")
                if u and rid and rid not in seen:
                    seen.add(rid)
                    yield rid, u, r.get("date"), p

targets = {
    "A_gucheng": lambda ps, dom: dom in ("httpbin.ceshiren.com", "httpbun.com") and any(n == "q" for n, _ in ps),
    "B_jun21": lambda ps, dom: any(n in ("x", "ov", "retry", "n") and re.fullmatch(r"\d{19}", unquote(v) or "") or (n == "n" and re.fullmatch(r"1[4-9]\d{8}", unquote(v) or "")) for n, v in ps),
    "C_appwrite": lambda ps, dom: dom in ("new.appwrite.io", "webhook.site") and any(n in ("userid", "secret", "expire") for n, _ in ps),
    "D_livecodes": lambda ps, dom: dom == "livecodes.io" and any(n in ("x", "html") for n, _ in ps),
    "E_httpbin_u": lambda ps, dom: dom == "httpbin.org" and any(n == "u" for n, _ in ps),
}

out = {k: [] for k in targets}
for rid, url, date, path in iter_reports():
    try:
        pr = urlparse(url)
        dom = (pr.hostname or "").lower()
        ps = [(n.lower(), v) for n, v in parse_qsl(pr.query, keep_blank_values=True)]
    except Exception:
        continue
    for k, fn in targets.items():
        try:
            if fn(ps, dom) and len(out[k]) < 15:
                out[k].append({"report_id": rid, "date": date, "url": url[:600], "file": os.path.relpath(path, ROOT)})
        except Exception:
            pass

od = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw")
json.dump(out, open(os.path.join(od, "nonce-02-lead-urls.json"), "w"), indent=1)
for k, v in out.items():
    print("=" * 90)
    print(k, len(v))
    for e in v[:8]:
        print(" ", e["date"], e["report_id"][:8], e["url"][:220].replace("\n", " "))
