#!/usr/bin/env python3
"""Cryptologist lane scanner — read-only, no network.
Scans summary, homepage_uri, source_code_uri, runtime_dependencies, name
(plus dashboard_rules/haiku_reason as context) for payload shapes.
Recomputes all counts; writes tallies to JSON next to this script.
"""
import csv, re, json, collections, urllib.parse, base64, hashlib, sys
from pathlib import Path

CSV = Path.home() / "workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path(__file__).parent

rows = list(csv.DictReader(CSV.open(newline='', encoding='utf-8')))
print(f"rows={len(rows)} cols={list(rows[0].keys())}")
print("sha256:", hashlib.sha256(CSV.read_bytes()).hexdigest())

TARGET_COLS = ["name", "summary", "homepage_uri", "source_code_uri", "runtime_dependencies"]
CTX_COLS = ["dashboard_rules", "haiku_reason", "haiku_category"]

URL_RE = re.compile(r"https?://[^\s\"'<>,\]]+")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HEX_RE = re.compile(r"\b[0-9a-fA-F]{16,}\b")
B64_RE = re.compile(r"\b[A-Za-z0-9+/]{32,}={0,2}\b")
VCS = ["hg", "fossil", "git", "bzr", "svn", "mercurial", "darcs"]
DEADDROP = ["webhook.site", "oast", "requestbin", "ntfy", "pipedream", "beeceptor",
            "hookbin", "webhook", "ngrok", "trycloudflare", "localtunnel", "jina",
            "r.jina.ai", "s3.amazonaws", "storage.googleapis", "blob.core.windows",
            "pastebin", "gist.github", "discord", "telegram", "t.me"]
SCRIPT = ["<script", "javascript:", "onerror", "onload", "{{", "{%", "${", "eval(",
          "go-import", "import-path", "content=\"", "meta name", "<meta",
          "curl ", "wget ", "http-equiv", "document.cookie", "alert(",
          "fetch(", "XMLHttpRequest", "exec(", "system(", "os.system",
          "subprocess", "base64", "fromCharCode", "unescape", "atob("]

hosts = collections.Counter(); schemes = collections.Counter()
dep_names = collections.Counter(); authors = collections.Counter()
dash_rules = collections.Counter(); haiku_cat = collections.Counter()
hits = collections.defaultdict(list)  # shape -> list of (name, col, value)

def record(shape, row, col, val):
    hits[shape].append({"name": row["name"], "col": col, "value": val[:300]})

for r in rows:
    authors[r["authors_declared"]] += 1
    dash_rules[r["dashboard_rules"]] += 1
    haiku_cat[r["haiku_category"]] += 1
    for col in TARGET_COLS:
        v = (r.get(col) or "")
        low = v.lower()
        for u in URL_RE.findall(v):
            p = urllib.parse.urlparse(u.rstrip(")."))
            hosts[p.hostname or "?"] += 1
            schemes[p.scheme] += 1
        for m in IP_RE.findall(v):
            record("ip_literal", r, col, m)
        if "go-import" in low: record("go-import", r, col, v)
        if "import-path" in low or "import path" in low: record("import-path", r, col, v)
        for vc in VCS:
            # VCS value as standalone token / scheme (e.g. hg://, vcs=hg) — bare "git" in github.com URLs excluded
            if re.search(rf"(?:^|[\s=:\"'/]){vc}(?:$|[\s\"'/:])", low) and "github.com" not in low:
                record(f"vcs:{vc}", r, col, v)
        for d in DEADDROP:
            if d in low: record(f"deadrop/host:{d}", r, col, v)
        for s in SCRIPT:
            if s in low: record(f"script-like:{s}", r, col, v)
        # hex / b64 blobs (exclude plain words; require mixed/digit content for b64)
        for m in HEX_RE.findall(v):
            record("hex_blob>=16", r, col, m)
        for m in B64_RE.findall(v):
            if re.search(r"[0-9+/]", m) and re.search(r"[A-Z]", m):
                record("b64_candidate>=32", r, col, m)
    # runtime_dependencies: parse names
    deps = (r.get("runtime_dependencies") or "").strip()
    if deps and deps != "0":
        for d in re.split(r"[;,]", deps):
            d = d.strip()
            if d: dep_names[d] += 1
    # context columns: dashboard rule mentions only
    for col in CTX_COLS:
        v = (r.get(col) or "")
        if "oob url" in v.lower() or "probe name" in v.lower():
            record(f"context:{col}", r, col, v[:200])

print("\n== hosts =="); print(json.dumps(dict(hosts), indent=1))
print("\n== schemes =="); print(json.dumps(dict(schemes), indent=1))
print("\n== runtime_dependencies distinct ==", len(dep_names), dict(dep_names))
print("\n== authors =="); print(json.dumps(dict(authors), indent=1))
print("\n== dashboard_rules =="); print(json.dumps(dict(dash_rules), indent=1))
print("\n== haiku_category =="); print(json.dumps(dict(haiku_cat), indent=1))
print("\n== HIT SHAPES ==")
for shape, lst in sorted(hits.items()):
    print(f"{shape}: {len(lst)} rows-hits")
    for h in lst[:20]:
        print(f"   {h['name']} [{h['col']}] {h['value']!r}")
    if len(lst) > 20: print(f"   ... +{len(lst)-20} more")

# distinct URL full shapes (host+path pattern): homepage/source templates
url_shapes = collections.Counter()
for r in rows:
    for col in ("homepage_uri", "source_code_uri"):
        u = (r.get(col) or "")
        p = urllib.parse.urlparse(u)
        shape = f"{p.hostname}{re.sub(r'[^/]+$', '<name>', p.path) if p.path else ''}"
        url_shapes[shape] += 1
print("\n== url host+path shapes =="); print(json.dumps(dict(url_shapes), indent=1))

# summary templates
sum_shapes = collections.Counter()
for r in rows:
    s = (r.get("summary") or "")
    s2 = re.sub(r"based on \S+", "based on <X>", s)
    sum_shapes[s2] += 1
print("\n== summary templates =="); print(json.dumps(dict(sum_shapes), indent=1))

# name shapes: token patterns
name_pat = collections.Counter()
for r in rows:
    n = r["name"]
    pat = re.sub(r"[a-z]+", "w", n)
    name_pat[pat] += 1
print("\n== name token patterns (top 30) ==")
for k, v in name_pat.most_common(30): print(f"  {v:4d}  {k}")

# credential-shaped values: count only, never print values
cred_re = re.compile(r"(?:api[_-]?key|token|secret|password|passwd|aws_|sk-[A-Za-z0-9]|ghp_|github_pat_|AKIA[0-9A-Z]{16})", re.I)
cred_count = 0
for r in rows:
    for col in TARGET_COLS:
        if cred_re.search(r.get(col) or ""): cred_count += 1
print(f"\ncredential-shaped field hits (count only): {cred_count}")

# distinct summary "based on X" values = dependency-like mentions inside summaries
based = collections.Counter()
for r in rows:
    m = re.search(r"based on (\S+)", r.get("summary") or "")
    if m: based[m.group(1).rstrip(",.")] += 1
print(f"\nsummary 'based on X' distinct={len(based)} total={sum(based.values())}")
print(json.dumps(dict(based.most_common(50)), indent=1))

result = {
    "rows": len(rows),
    "sha256": hashlib.sha256(CSV.read_bytes()).hexdigest(),
    "hosts": dict(hosts), "schemes": dict(schemes),
    "dep_names": dict(dep_names),
    "authors": dict(authors), "dashboard_rules": dict(dash_rules),
    "haiku_category": dict(haiku_cat),
    "hit_shapes": {k: len(v) for k, v in hits.items()},
    "hit_examples": {k: v[:10] for k, v in hits.items()},
    "url_shapes": dict(url_shapes), "summary_templates": dict(sum_shapes),
    "based_on_distinct": len(based), "based_on_total": sum(based.values()),
    "based_on": dict(based),
    "credential_shaped_field_hits": cred_count,
}
(OUT / "tallies.json").write_text(json.dumps(result, indent=1))
print("\nwrote tallies.json")
