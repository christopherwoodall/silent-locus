#!/usr/bin/env python3
"""Pattern-sweep all recovered paste bodies; save sweep_bodies.json."""
import re, json, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "2026-05-27-paste-archive" / "bodies"

PATTERNS = {
    "zz": re.compile(r"(?<![a-z])zz(?![a-z])"),
    "oai": re.compile(r"(?<![a-z])oai(?![a-z])"),
    "epoch_nonce": re.compile(r"\b\d{10}\b"),
    "try_zz": re.compile(r"try[a-z]*\d*zz|zz\d{4,}", re.I),
    "proxy_wrapper": re.compile(r"(jqp\.vercel\.app|md\.succ\.ai|r\.jina\.ai|s\.jina\.ai|allorigins|proxymule|cors|markdown\.new|da\.gd|is\.gd|shorturl|bit\.ly|tinyurl)", re.I),
    "laundering_chain": re.compile(r"jina\.ai|allorigins|workers\.dev|markdown\.new", re.I),
    "go_import": re.compile(r"go-import", re.I),
    "web_hook": re.compile(r"web_hooks?|webhook", re.I),
    "chunk_marker": re.compile(r"A000|ZZEND|southpxdatapp", re.I),
    "gmail": re.compile(r"[\w.+-]+@gmail\.com"),
    "nsi_table": re.compile(r"nsi\.bg", re.I),
    "LINKANNA": re.compile(r"LINKANNA|LINKTARGETANNA|LINKANNATARGET"),
    "ReplyLink": re.compile(r"ReplyLink\d"),
    "CLICK_TARGET": re.compile(r"CLICK TARGET DATA|DIFFLINK|ENCODED"),
    "stat_ref": re.compile(r"Statistical reference"),
    "canary_x": None,
    "roi_et": re.compile(r"Roi Et", re.I),
    "premier_league": re.compile(r"premier league|arsenal|liverpool", re.I),
    "thai": re.compile(r"[\u0e00-\u0e7f]"),
}

results = []
for host in ("k4be.pl", "anna.fyi"):
    d = BASE / host
    for f in sorted(d.glob("*.txt")):
        body = f.read_text(errors="replace")
        pid = f.stem
        hits = {}
        for name, rx in PATTERNS.items():
            if name == "canary_x":
                hits[name] = 0 if not body.strip() else (1 if body.strip() in ("x", "X") else 0)
                continue
            hits[name] = len(rx.findall(body))
        res = {
            "id": pid,
            "host": host,
            "sha256": hashlib.sha256(body.encode()).hexdigest(),
            "bytes": len(body.encode()),
            "lines": body.count("\n") + 1,
            "hits": {k: v for k, v in hits.items() if v},
            "first80": body[:80].replace("\n", "\\n"),
        }
        # structure classification
        if host == "k4be.pl":
            if body.strip() in ("x", "X"):
                res["structure"] = "canary_x"
            elif re.search(r"Roi Et data segment", body, re.I):
                res["structure"] = "roi_et_segment"
            else:
                res["structure"] = "other"
        else:
            if hits["stat_ref"] and hits["LINKANNA"]:
                res["structure"] = "stat_ref_nsi"
            elif hits["LINKANNA"]:
                res["structure"] = "nsi_link_ref"
            elif re.search(r"<a href|&lt;a href|\[http|Link: \[", body):
                res["structure"] = "link_render_probe"
            else:
                res["structure"] = "other"
        results.append(res)

out = {
    "dataset": "2026-05-27-paste-archive",
    "bodies_swept": len(results),
    "pattern_battery": sorted(PATTERNS.keys()),
    "results": results,
}
path = ROOT / "data" / "2026-05-27-paste-archive" / "sweep_bodies.json"
path.write_text(json.dumps(out, indent=1))
print(f"swept {len(results)} bodies -> {path}")
# summary rollup
from collections import Counter
print(Counter(r["structure"] for r in results))
agg = {}
for r in results:
    for k, v in r["hits"].items():
        agg[k] = agg.get(k, 0) + v
print(json.dumps(agg, indent=1))
