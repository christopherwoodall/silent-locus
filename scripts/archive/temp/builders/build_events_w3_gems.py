#!/usr/bin/env python3
"""Build events.jsonl + rollup.jsonl for data/2025-03-04-rubygems-goimport-campaign.

Worker W3, 2026-09-29. Usage: python3 temp/build_events_w3_gems.py <repo_root>

Inputs (all under data/2025-03-04-rubygems-goimport-campaign/raw/):
  gem-graph-nodes.jsonl   - 2830 IOC graph nodes (2026-09-28 schema backfill)
  gem-ioc-log.jsonl       - 1262 download/extraction/diffend_harvest log records
  gem-ioc-hits.jsonl      - 2341 raw IOC-hit lines (mine_gems.py)
  gem-iocs-2026-09-27.jsonl - 334 campaign IOCs (wiki_ioc_pivot.py)
  gem-june18-wayback.jsonl  - 16 June-18 gem Wayback metadata rows
  gem-pins-batch1..4.txt + gem-pins-diffend.txt - pinned malicious versions
  gemstuffer-jfrog-2026-09-27.csv - 3025-row JFrog GemStuffer inventory
  *.pre-bulk              - EXCLUDED: earlier snapshots (verified pre-bulk node
                            ids are a strict subset of the current set)
  gem-graph-edges.jsonl   - EXCLUDED: edges are relationships, not events; no
                            registry kind covers them; joins live in support
                            indexes per schema/README.md

Grain: one record per node / log line / hit / IOC / wayback row / pin / CSV row.
Kinds (all existing registry): graph_node, download, extraction,
diffend_harvest, corpus_hit, wiki_ioc_pivot, wayback_capture, campaign_specimen.
Rollup: per-day graph aggregates (kind=campaign_day_rollup, NEW - triage note).

Fingerprint identity strings (documented in PROVENANCE.md):
  nodes:    sha256("gem-graph-node:<node.id>")
  ioc-log:  sha256("gem-ioc-log:<kind>:<name>@<version>:<ts>")
  hits:     sha256("gem-ioc-hit:<gem>@<version>:<family>:<line_no>:<matched_string>")
  iocs:     sha256("gem-ioc:<ioc>:<source_link>")
  wayback:  sha256("gem-wayback:<gem>@<version>")
  pins:     sha256("gem-pin:<name>==<version>")
  jfrog:    sha256("gemstuffer-jfrog:<Package>")
  rollup:   sha256("gem-day-rollup:<YYYY-MM-DD>")
"""
import json, sys, hashlib, csv, os
from datetime import datetime, timezone
from collections import Counter, defaultdict

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2025-03-04-rubygems-goimport-campaign")
RAW = os.path.join(D, "raw")
SLUG = "2025-03-04-rubygems-goimport-campaign"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
HUNT_TS = "2026-09-27T00:00:00Z"

def fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def lines(p):
    with open(p, encoding="utf-8") as fh:
        return [l for l in fh if l.strip()]

out = []
counts = {}

# --- 1. graph nodes (reuse backfilled rows, re-key event + fingerprint) ---
raw_nodes = [json.loads(l) for l in lines(os.path.join(RAW, "gem-graph-nodes.jsonl"))]
counts["nodes_in"] = len(raw_nodes)
for r in raw_nodes:
    nid = r["labels"]["node.id"]
    r["event"] = {"dataset": SLUG, "created": CREATED}
    r["fingerprint"] = fp(f"gem-graph-node:{nid}")
    out.append(r)
counts["nodes_out"] = len(raw_nodes)

# --- 2. ioc log (reuse backfilled rows) ---
raw_log = [json.loads(l) for l in lines(os.path.join(RAW, "gem-ioc-log.jsonl"))]
counts["ioclog_in"] = len(raw_log)
for r in raw_log:
    lb = r["labels"]
    ts = r.get("retrieved_at") or lb.get("extracted.at") or lb.get("published.at") or ""
    if r["record_kind"] == "download" and "timestamp_source" not in lb:
        lb["timestamp_source"] = "retrieved_at"
    r["event"] = {"dataset": SLUG, "created": CREATED}
    r["fingerprint"] = fp(f"gem-ioc-log:{r['record_kind']}:{lb.get('gem.name')}"
                           f"@{lb.get('gem.version')}:{ts}")
    out.append(r)
counts["ioclog_out"] = len(raw_log)

# --- 3. ioc hits (raw -> schema; byte-identical dup lines deduped) ---
raw_hits = lines(os.path.join(RAW, "gem-ioc-hits.jsonl"))
counts["hits_in"] = len(raw_hits)
uniq_hits = sorted(set(raw_hits))
counts["hits_deduped"] = len(raw_hits) - len(uniq_hits)
for l in uniq_hits:
    h = json.loads(l)
    ident = (f"gem-ioc-hit:{h['gem']}@{h['version']}:{h['fingerprint']}:"
             f"{h.get('line_no')}:{h.get('matched_string')}")
    labels = {
        "gem.name": h["gem"],
        "gem.version": h["version"],
        "hit.file": h.get("file"),
        "hit.ioc_family": h["fingerprint"],
        "hit.line_no": h.get("line_no"),
        "hit.scan_truncated": h.get("scan_truncated"),
        "timestamp_source": "lane:2026-09-27 (mine_gems.py hunt; per-hit scan timestamps absent from raw)",
    }
    out.append({
        "@timestamp": HUNT_TS,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "corpus_hit",
        "fingerprint": fp(ident),
        "labels": labels,
        "matched_string": h.get("matched_string"),
        "confidence": h.get("confidence"),
        "note": h.get("note"),
        "source_url": f"https://my.diffend.io/gems/{h['gem']}/{h['version']}",
        "description": (f"IOC hit [{h['fingerprint']}] in {h['gem']}=={h['version']} "
                        f"({h.get('file')}, line {h.get('line_no')})"),
    })
counts["hits_out"] = len(uniq_hits)

# --- 4. campaign IOC snapshot (wiki_ioc_pivot.py) ---
raw_iocs = [json.loads(l) for l in lines(os.path.join(RAW, "gem-iocs-2026-09-27.jsonl"))]
counts["iocs_in"] = len(raw_iocs)
for r in raw_iocs:
    fs = r.get("first_seen", "")
    ts = f"{fs}T00:00:00Z" if len(fs) == 10 else HUNT_TS
    labels = {
        "ioc.type": r.get("type"),
        "ioc.first_seen": r.get("first_seen"),
        "ioc.last_seen": r.get("last_seen"),
        "ioc.report_count": r.get("report_count"),
        "ioc.status": r.get("status"),
        "ioc.context": (r.get("context") or "")[:500],
        "timestamp_source": "labels:ioc.first_seen" if len(fs) == 10 else
            "lane:2026-09-27 (IOC snapshot; unparsable first_seen)",
    }
    out.append({
        "@timestamp": ts,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "wiki_ioc_pivot",
        "fingerprint": fp(f"gem-ioc:{r['ioc']}:{r.get('source_link')}"),
        "labels": labels,
        "matched_string": r["ioc"],
        "source_url": r.get("source_link"),
        "description": (f"Campaign IOC [{r.get('type')}] {r['ioc'][:120]}: "
                        f"{r.get('report_count')} gem version(s), {r.get('first_seen')}->{r.get('last_seen')}"),
    })
counts["iocs_out"] = len(raw_iocs)

# --- 5. june-18 wayback rows ---
raw_wb = [json.loads(l) for l in lines(os.path.join(RAW, "gem-june18-wayback.jsonl"))]
counts["wayback_in"] = len(raw_wb)
for r in raw_wb:
    labels = {
        "gem.name": r["gem"],
        "gem.version": r["version"],
        "gem.wave": r.get("wave"),
        "gem.published_at": r.get("published_at"),
        "gem.total_downloads": r.get("total_downloads"),
        "gem.external_links": r.get("external_links") or [],
        "gem.date_source": r.get("date_source"),
        "timestamp_source": "labels:published_at",
    }
    out.append({
        "@timestamp": r["published_at"],
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "wayback_capture",
        "fingerprint": fp(f"gem-wayback:{r['gem']}@{r['version']}"),
        "labels": labels,
        "source_url": f"https://my.diffend.io/gems/{r['gem']}/{r['version']}",
        "description": r.get("description") or f"Wayback metadata for June-18 gem {r['gem']}=={r['version']}",
    })
counts["wayback_out"] = len(raw_wb)

# --- 6. pinned malicious versions (dedupe across the 5 pin files).
#     7 lines in gem-pins-batch4.txt are bare gem names (no ==version):
#     kept as name-only pins with gem.version=null and identity "gem-pin:<name>". ---
pin_sources = defaultdict(list)
for fn in ["gem-pins-batch1.txt", "gem-pins-batch2.txt", "gem-pins-batch3.txt",
           "gem-pins-diffend.txt", "gem-pins-batch4.txt"]:
    for l in lines(os.path.join(RAW, fn)):
        s = l.strip()
        if s and not s.startswith("#"):
            if fn not in pin_sources[s]:
                pin_sources[s].append(fn)
counts["pins_in"] = sum(1 for fn in
    ["gem-pins-batch1.txt", "gem-pins-batch2.txt", "gem-pins-batch3.txt",
     "gem-pins-batch4.txt", "gem-pins-diffend.txt"]
    for l in lines(os.path.join(RAW, fn)) if l.strip() and not l.strip().startswith("#"))
for pin in sorted(pin_sources):
    if "==" in pin:
        name, ver = pin.split("==", 1)
        ident = f"gem-pin:{pin}"
        src = f"https://my.diffend.io/gems/{name}/{ver}"
        desc = f"Pinned malicious gem version {pin} (go-import campaign)"
    else:
        name, ver = pin, None
        ident = f"gem-pin:{pin}"
        src = f"https://my.diffend.io/gems/{name}"
        desc = f"Pinned malicious gem {pin} (go-import campaign; version unpinned)"
    labels = {
        "gem.name": name,
        "gem.version": ver,
        "pin.sources": sorted(pin_sources[pin]),
        "timestamp_source": "lane:2026-09-27 (pin files; per-pin discovery timestamps absent from raw)",
    }
    out.append({
        "@timestamp": HUNT_TS,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "campaign_specimen",
        "fingerprint": fp(ident),
        "labels": labels,
        "source_url": src,
        "description": desc,
    })
counts["pins_out"] = len(pin_sources)

# --- 7. JFrog GemStuffer inventory ---
with open(os.path.join(RAW, "gemstuffer-jfrog-2026-09-27.csv"), encoding="utf-8") as fh:
    jrows = list(csv.DictReader(fh))
counts["jfrog_in"] = len(jrows)
for r in jrows:
    versions = [v for v in (r["Versions"] or "").split(";") if v]
    labels = {
        "gem.name": r["Package"],
        "gem.versions": versions,
        "gem.xray_id": r.get("Xray ID"),
        "timestamp_source": "dataset:csv_retrieval_date (gemstuffer-jfrog-2026-09-27.csv saved 2026-09-27)",
    }
    out.append({
        "@timestamp": HUNT_TS,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "campaign_specimen",
        "fingerprint": fp(f"gemstuffer-jfrog:{r['Package']}"),
        "labels": labels,
        "source_url": "https://research.jfrog.com/gemstuffer.csv",
        "description": f"JFrog GemStuffer inventory: {r['Package']} ({';'.join(versions)})",
    })
counts["jfrog_out"] = len(jrows)

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as fh:
    for r in out:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

# --- rollup: per-day graph aggregates ---
by_day = defaultdict(list)
for r in raw_nodes:
    by_day[(r.get("@timestamp") or "")[:10]].append(r)
IOCS = ["council-domain", "go-import", "go-import-repo", "go-import-vcs",
        "r-jina-proxy", "probe-name", "zz-token"]
rollup = []
for day in sorted(by_day):
    ns = by_day[day]
    subs = Counter(n["labels"].get("node.subtype") for n in ns)
    pkgs = {n["labels"].get("node.package") for n in ns
            if n["labels"].get("node.subtype") == "diffend-harvest"}
    stamps = sorted(n.get("@timestamp") for n in ns if n.get("@timestamp"))
    labels = {
        "day": day,
        "rollup.nodes": len(ns),
        "rollup.campaign_gems": subs.get("diffend-harvest", 0),
        "rollup.distinct_packages": len(pkgs),
        "rollup.first_seen": stamps[0] if stamps else None,
        "rollup.last_seen": stamps[-1] if stamps else None,
        "timestamp_source": "derived:graph_node @timestamp (min/max)",
    }
    for fam in IOCS:
        labels[f"rollup.ioc_{fam.replace('-', '_')}"] = subs.get(fam, 0)
    rollup.append({
        "@timestamp": f"{day}T00:00:00Z",
        "event": {"dataset": f"{SLUG}-rollup", "created": CREATED},
        "record_kind": "campaign_day_rollup",
        "fingerprint": fp(f"gem-day-rollup:{day}"),
        "labels": labels,
        "description": (f"{day}: {len(ns)} graph nodes, {subs.get('diffend-harvest', 0)} campaign gems "
                        f"({len(pkgs)} packages)"),
    })
with open(os.path.join(D, "rollup.jsonl"), "w", encoding="utf-8") as fh:
    for r in rollup:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

print("in/out:", counts)
print(f"events: {len(out)}, rollup: {len(rollup)}")
