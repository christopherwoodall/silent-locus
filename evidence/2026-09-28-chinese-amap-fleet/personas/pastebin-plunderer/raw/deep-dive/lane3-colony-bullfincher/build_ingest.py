#!/usr/bin/env python3
"""Build data/2026-10-05-thecolony-ai ingest dataset (Lane 3).

Extracts genuinely-new agent records from the third-party read-only corpus
joshuadavid/wikiagentswarminvestigation (local shallow clone, lane3/ref/run1):
- 17 x paste.linuxiarz.pl Perceptual Zephyr recruitment pastes (2026-09-04)
- 3 x pastebin.k4be.pl Humana 10-K / bullfincher sec-proxy pastes (2026-02-26)

Excluded: k4be 6b4db783 (CentaurAgent) - byte-identical to anna.fyi eba4cc0e
already in data/2018-05-09-paste-archive-gap (sha256 match verified).
"""
import json, hashlib, os
from datetime import datetime, timezone

LANE = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher")
RUN1 = os.path.join(LANE, "ref/run1")
OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-10-05-thecolony-ai")
NOW = datetime.now(timezone.utc).isoformat()
DS = "2026-10-05-thecolony-ai"

os.makedirs(os.path.join(OUT, "raw/rows"), exist_ok=True)
os.makedirs(os.path.join(OUT, "raw/bodies"), exist_ok=True)

# (revisions file, page_id, timestamp, timestamp_source, authorship_note)
targets = []
lin = os.path.join(RUN1, "agent-logs/paste-linuxiarz/revisions.jsonl")
k4be = os.path.join(RUN1, "agent-logs/pastebin-k4be/revisions.jsonl")

zephyr_ids = ["08d6473d","0977e8cb","0fee83f5","115ae365","169683a1","25c81b19",
              "3bd538a7","48d18719","546740ba","5a768d76","77280fdf","8cfcafeb",
              "bae744b9","cb7def97","e0fde17d","e5410e8e","ebcced74"]
for pid in zephyr_ids:
    targets.append((lin, f"paste-linuxiarz/{pid}", "2026-09-04T00:00:00Z",
        "labels:thread_analysis_wb_timestamp_cluster_2026-09-04",
        "self-identifies as 'Perceptual Zephyr, Solar Pro 4 on Hermes Agent by Nous Research' (unverified claim); run-1 verdict=swarm; post-disclosure recruitment, not swarm coordination"))
for pid, ts in [("5329a841","2026-02-26T14:49:24Z"),("bd44d381","2026-02-26T14:50:18Z"),("680ec235","2026-02-26T14:52:19Z")]:
    targets.append((k4be, f"pastebin-k4be/{pid}", ts,
        "labels:api_paste_created_field",
        "earliest proxy-gadget record in corpus; Humana 10-K stock-return table via bullfincher.io/sec-proxy; run-1 verdict=swarm"))

index = {}
for path, pid, ts, ts_src, note in targets:
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("page_id") == pid:
                index[pid] = (r, ts, ts_src, note)
                break
    assert pid in index, f"missing {pid}"
print(f"loaded {len(index)} rows")

events = []
for pid, (r, ts, ts_src, note) in index.items():
    body = r.get("body") or ""
    body_bytes = body.encode("utf-8")
    # verify against source row's sha256 when the source provides one
    calc = hashlib.sha256(body_bytes).hexdigest()
    src_sha = r.get("body_sha256")
    if src_sha:
        assert calc == src_sha, f"sha mismatch {pid}"
    elif body_bytes:
        note += " [body_sha256 absent in source row; computed locally]"
    else:
        note += " [body NOT recovered in source export; metadata-only record]"
    host = pid.split("/")[0]
    short = pid.split("/")[1]
    # raw audit copies
    with open(os.path.join(OUT, "raw/rows", pid.replace("/","~")+".json"), "w") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "raw/bodies", f"{host}_{short}.txt"), "wb") as f:
        f.write(body_bytes)
    fp = hashlib.sha256(f"{DS}|{r.get('source_url')}|{calc}".encode()).hexdigest()
    title = r.get("source_title")
    desc_bits = [f"{host} paste '{short}'"]
    if title: desc_bits.append(f"title '{title}'")
    desc_bits.append(f"({len(body_bytes)} B): third-party-archived agent-text copy")
    ev = {
        "@timestamp": ts,
        "event": {"dataset": DS, "created": NOW},
        "record_kind": "relay_paste",
        "fingerprint": fp,
        "labels": {
            "paste.id": short, "paste.host": host, "paste.title": title,
            "paste.author_label": r.get("label"),
            "paste.verdict": r.get("verdict"),
            "paste.inclusion_reason": r.get("inclusion_reason"),
            "paste.body_sha256": calc,
            "paste.archived_at": r.get("archived_at"),
            "timestamp_source": ts_src,
            "external_overlap": "joshuadavid/wikiagentswarminvestigation agent-logs (" +
                ("paste-linuxiarz" if host=="paste-linuxiarz" else "pastebin-k4be") + "/revisions.jsonl)",
            "authorship_note": note,
            "retrieval_method": "extracted_from_run1_corpus_file",
        },
        "source_url": r.get("source_url"),
        "sha256": calc,
        "size_bytes": len(body_bytes),
        "retrieved_at": NOW,
        "retrieved_via": "extracted_from_run1_corpus_file",
        "confidence": "confirmed",
        "description": " ".join(desc_bits),
    }
    events.append(ev)

events.sort(key=lambda e: e["@timestamp"])
with open(os.path.join(OUT, "events.jsonl"), "w") as f:
    for e in events:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")

# rollups: one per day-burst
def rollup(day, subset, kind_desc):
    fps = sorted(e["fingerprint"] for e in subset)
    fp = hashlib.sha256("|".join(fps).encode()).hexdigest()
    titles = {}
    for e in subset:
        t = e["labels"]["paste.title"] or "(untitled)"
        titles[t] = titles.get(t, 0) + 1
    top = max(titles, key=titles.get)
    return {
        "@timestamp": subset[0]["@timestamp"],
        "event": {"dataset": DS+"-rollup", "created": NOW},
        "record_kind": "paste_day_burst",
        "fingerprint": fp,
        "labels": {"day": day, "pastes.count": len(subset),
                   "titles.distinct": len(titles), "titles.top": top,
                   "titles.top_count": titles[top]},
        "description": f"{kind_desc}: {len(subset)} pastes; top title '{top}' x{titles[top]}",
    }

hum = [e for e in events if e["labels"]["paste.host"]=="pastebin-k4be"]
zep = [e for e in events if e["labels"]["paste.host"]=="paste-linuxiarz"]
rollups = [
    rollup("2026-02-26", hum, "k4be Humana 10-K bullfincher sec-proxy cluster (earliest proxy gadget)"),
    rollup("2026-09-04", zep, "linuxiarz Perceptual Zephyr thecolony.ai recruitment drop (post-disclosure)"),
]
with open(os.path.join(OUT, "rollup.jsonl"), "w") as f:
    for r in rollups:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"events={len(events)} rollups={len(rollups)}")
