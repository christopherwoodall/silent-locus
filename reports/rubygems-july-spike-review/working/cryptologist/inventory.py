#!/usr/bin/env python3
"""Second pass: distinct-row inventories + explicit zero-checks. Read-only, no network."""
import csv, re, json, collections, urllib.parse
from pathlib import Path
CSV = Path.home() / "workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path(__file__).parent
rows = list(csv.DictReader(CSV.open(newline='', encoding='utf-8')))
TARGET = ["name", "summary", "homepage_uri", "source_code_uri", "runtime_dependencies"]
ALL = list(rows[0].keys())

def rows_with(pred, cols=TARGET):
    return [r["name"] for r in rows if any(pred(r.get(c) or "") for c in cols)]

def rows_with_anycol(pred):
    return [r["name"] for r in rows if any(pred(r.get(c) or "") for c in ALL)]

# zero checks across target cols AND all cols
terms = ["go-import", "go import", "import-path", "r.jina.ai", "jina.ai", "wandsworth",
         "lambeth", "southwark", "ntfy", "requestbin", "pipedream", "beeceptor",
         "hookbin", "ngrok", "trycloudflare", "localtunnel", "s3.amazonaws",
         "storage.googleapis", "blob.core.windows", "pastebin", "discord.gg",
         "hg://", "fossil", "bzr://", "svn://", "mercurial", "darcs",
         "curl ", "wget ", "eval(", "os.system", "subprocess", "document.cookie"]
zero = {}
for t in terms:
    zero[t] = {"target_cols_rows": len(rows_with(lambda v, t=t: t in v.lower())),
               "all_cols_rows": len(rows_with_anycol(lambda v, t=t: t in v.lower()))}
print("ZERO-CHECKS (row counts containing term):")
for k, v in zero.items(): print(f"  {k}: target={v['target_cols_rows']} all={v['all_cols_rows']}")

# empty / value stats per target col
for c in TARGET:
    vals = collections.Counter(r.get(c) or "" for r in rows)
    print(f"\n{c}: empty={vals['']} distinct={len(vals)} top={vals.most_common(5)}")
print("\nruntime_dependencies distinct values:", sorted(collections.Counter(r['runtime_dependencies'] for r in rows).items()))

# OAST / webhook inventories
oast_rows, oast_hosts, oast_paths = set(), collections.Counter(), collections.Counter()
wh_rows, wh_uuids, wh_paths = set(), collections.Counter(), collections.Counter()
for r in rows:
    for c in ("homepage_uri", "source_code_uri", "summary"):
        v = r.get(c) or ""
        for u in re.findall(r"https?://[^\s\"'<>,\]]+", v):
            p = urllib.parse.urlparse(u.rstrip(")."))
            h = p.hostname or ""
            if "oast" in h:
                oast_rows.add(r["name"]); oast_hosts[h] += 1; oast_paths[p.path] += 1
            if h == "webhook.site":
                wh_rows.add(r["name"])
                parts = [x for x in p.path.split("/") if x]
                if parts: wh_uuids[parts[0]] += 1
                wh_paths["/".join(parts[1:]) if len(parts) > 1 else "(bare)"] += 1
print(f"\nOAST distinct rows={len(oast_rows)} hosts={dict(oast_hosts)} paths={dict(oast_paths)}")
print(f"WEBHOOK distinct rows={len(wh_rows)} uuids={dict(wh_uuids)} paths={dict(wh_paths)}")

# IP / metadata rows
ip_rows = {}
for r in rows:
    for c in ("homepage_uri", "source_code_uri"):
        v = r.get(c) or ""
        if re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", v) or "metadata." in v or "instance-data" in v or "ip-10-0-0-1" in v:
            ip_rows.setdefault(r["name"], []).append((c, v))
print(f"\nIP/metadata distinct rows={len(ip_rows)}")
for k, v in sorted(ip_rows.items()): print(f"  {k}: {v}")

# XSS / SSTI in summary (target) and authors (context)
xss = [r["name"] for r in rows if re.search(r"<(script|img|svg)|onerror|onload", (r["summary"] or ""), re.I)]
ssti_sum = [r["name"] for r in rows if re.search(r"\{\{|\$\{|<%=|<%25", (r["summary"] or ""))]
ssti_auth = [r["name"] for r in rows if re.search(r"\{\{|\$\{|<%=|<%25|<script|<img", (r["authors_declared"] or ""))]
xss_auth = [r["name"] for r in rows if re.search(r"<(script|img)", (r["authors_declared"] or ""), re.I)]
print(f"\nXSS-in-summary rows={len(xss)}: {xss}")
print(f"SSTI-in-summary rows={len(ssti_sum)}: {ssti_sum}")
print(f"payload-in-authors rows={len(set(ssti_auth+xss_auth))}: {sorted(set(ssti_auth+xss_auth))}")

# dashboard oob/probe counts (row-level, dashboard_rules col)
oob = [r["name"] for r in rows if "oob url" in (r["dashboard_rules"] or "").lower()]
probe = [r["name"] for r in rows if "probe name" in (r["dashboard_rules"] or "").lower()]
both = [r["name"] for r in rows if "oob url" in (r["dashboard_rules"] or "").lower() and "probe name" in (r["dashboard_rules"] or "").lower()]
print(f"\ndashboard 'oob url' rows={len(oob)}  'probe name' rows={len(probe)}  both={len(both)}")

# name patterns: ssrf-*-hex, webhook-*, test-*, apex-*
for pat, rx in [("ssrf-*", r"^ssrf-"), ("webhook-*", r"^webhook-"), ("apex_*", r"^apex"),
                ("hex-suffix -[0-9a-f]{8}$", r"-[0-9a-f]{8}$"), ("epoch-like -1[67][0-9]{8}$", r"-1[67]\d{8}$"),
                ("a*100 name", r"^a{50,}")]:
    lst = [r["name"] for r in rows if re.search(rx, r["name"])]
    print(f"name {pat}: {len(lst)}")

# credential-shaped: masked — column + name + which keyword class only, no values
cred_classes = {"api_key_word": re.compile(r"api[_-]?key", re.I), "token_word": re.compile(r"token", re.I),
                "secret_word": re.compile(r"secret", re.I), "sk_prefix": re.compile(r"sk-[A-Za-z0-9]", re.I),
                "ghp": re.compile(r"ghp_", re.I), "akia": re.compile(r"AKIA", re.I)}
cred = []
for r in rows:
    for c in TARGET:
        v = r.get(c) or ""
        for cls, rx in cred_classes.items():
            if rx.search(v): cred.append({"name": r["name"], "col": c, "class": cls})
print(f"\ncredential-shaped (masked, name+col+class only): {cred}")

# http vs https payload rows
http_rows = [r["name"] for r in rows if any((r.get(c) or "").startswith("http://") for c in ("homepage_uri", "source_code_uri"))]
print(f"\nhttp:// (not https) homepage/source rows={len(http_rows)}: {http_rows}")

inv = {"zero_checks": zero, "oast_rows": sorted(oast_rows), "oast_hosts": dict(oast_hosts),
       "oast_paths": dict(oast_paths), "webhook_rows": sorted(wh_rows), "webhook_uuids": dict(wh_uuids),
       "webhook_paths": dict(wh_paths), "ip_rows": {k: v for k, v in sorted(ip_rows.items())},
       "xss_summary_rows": xss, "ssti_summary_rows": ssti_sum, "payload_authors_rows": sorted(set(ssti_auth+xss_auth)),
       "dashboard_oob_rows": oob, "dashboard_probe_rows": probe, "dashboard_both_rows": both,
       "credential_shaped_masked": cred, "http_rows": http_rows}
(OUT / "inventory.json").write_text(json.dumps(inv, indent=1))
print("\nwrote inventory.json")
