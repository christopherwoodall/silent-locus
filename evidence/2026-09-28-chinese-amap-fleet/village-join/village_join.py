#!/usr/bin/env python3
"""VILLAGE-JOIN-2: join silent-locus URL fingerprints against AI Village tables.

Streams each jsonl.gz table (chunked, never full-loads big tables).
- Dates the incident-recreation window via marker scan (all dates).
- Joins 2025-only rows (created_at < 2026-01-01) against our URL sets.
- Match types: full_url, fingerprint_domain (strong), uuid, webhook_token,
  dsqa_phrase. Weak (non-fingerprint) domain hits counted, not row-reported.
"""
import gzip, json, re, sys, os, urllib.parse
from collections import Counter, defaultdict

DATA = os.path.expanduser("~/workspace/ai-village-data")
REF = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/village-join")
OUT = REF
CUTOFF = "2026-01-01"

URL_RE = re.compile(r'https?://[^\s"\'<>\]\)\}]+')
UUID_RE = re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I)
DISCORD_WH_RE = re.compile(r'discord\.com/api/webhooks/\d+/[\w\-~.]+', re.I)
MARKERS = [
    ("zz=oai", re.compile(r'zz=oai', re.I)),
    ("oai_prefix", re.compile(r'\boai[-_][a-z0-9]+', re.I)),
    ("dsqa", re.compile(r'dsqa_\d+', re.I)),
    ("deepsearchqa", re.compile(r'deepsearchqa', re.I)),
    ("unctad", re.compile(r'unctad', re.I)),
    ("artifactory", re.compile(r'artifactory', re.I)),
]

TABLES = {
    "agents.jsonl.gz": ["goal", "status_message", "name"],
    "agent_goals.jsonl.gz": ["description", "name"],
    "chat_messages.jsonl.gz": ["content"],
    "events.jsonl.gz": ["__data_json__"],
    "computer_use_turns.jsonl.gz": ["agent_action", "agent_messages", "output", "error", "system"],
    "agent_memories.jsonl.gz": ["content"],
    "claude_code_messages.jsonl.gz": ["content"],
    "summaries.jsonl.gz": ["content"],
    "villages.jsonl.gz": ["__all_strings__"],
    "village_goals.jsonl.gz": ["__all_strings__"],
    "chat_rooms.jsonl.gz": ["__all_strings__"],
    "computer_use_sessions.jsonl.gz": ["__all_strings__"],
    "claude_code_sessions.jsonl.gz": ["__all_strings__"],
}

def clean_url(u):
    return u.rstrip('.,;:!?*~\'"')

def domain_of(u):
    try:
        h = urllib.parse.urlparse(u).hostname or ""
        return h.lower()
    except Exception:
        return ""

def load_refs():
    fp = {}
    with open(os.path.join(REF, "our-fingerprint-domains.txt")) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 2:
                fp[parts[1].strip().lower()] = int(parts[0])
    alld = {}
    with open(os.path.join(REF, "our-domains.txt")) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 2:
                alld[parts[1].strip().lower()] = int(parts[0])
    urls = set(); uuids = set(); dctokens = set()
    with open(os.path.join(REF, "our-urls-raw.txt"), errors="replace") as f:
        for line in f:
            u = line.strip()
            if not u.startswith("http"):
                continue
            if any(c in u for c in ("$", "{", "}", "<", ">", " ", "\t")):
                continue
            if len(u) < 12:
                continue
            urls.add(u)
            for m in UUID_RE.findall(u):
                uuids.add(m.lower())
            for m in DISCORD_WH_RE.findall(u):
                dctokens.add(m.lower())
    phrases = []
    fp_path = os.path.expanduser("~/workspace/silent-locus/collections/deepsearchqa/fingerprints.md")
    if os.path.exists(fp_path):
        inblock = False
        with open(fp_path) as f:
            for line in f:
                if line.strip().startswith("```"):
                    inblock = not inblock
                    continue
                if inblock and len(line.strip()) > 25:
                    phrases.append(line.strip())
    return fp, alld, urls, uuids, dctokens, phrases

def text_of(row, fields):
    parts = []
    for fld in fields:
        if fld == "__data_json__":
            v = row.get("data")
            parts.append(json.dumps(v, ensure_ascii=False) if v is not None else "")
        elif fld == "__all_strings__":
            stack = [row]
            while stack:
                x = stack.pop()
                if isinstance(x, str):
                    parts.append(x)
                elif isinstance(x, dict):
                    stack.extend(x.values())
                elif isinstance(x, list):
                    stack.extend(x)
        else:
            v = row.get(fld)
            if isinstance(v, str):
                parts.append(v)
    return "\n".join(parts)

def main():
    fp, alld, our_urls, our_uuids, our_dctokens, phrases = load_refs()
    print(f"refs: {len(fp)} fp-domains, {len(alld)} all-domains, {len(our_urls)} urls, "
          f"{len(our_uuids)} uuids, {len(our_dctokens)} discord-tokens, {len(phrases)} dsqa-phrases",
          flush=True)
    matches = open(os.path.join(OUT, "matches-2025.jsonl"), "w")
    stats = {}
    marker_hits = defaultdict(list)  # marker -> list of (ts, table, rowid)

    for tname, fields in TABLES.items():
        path = os.path.join(DATA, tname)
        if not os.path.exists(path):
            print(f"SKIP missing {tname}", flush=True); continue
        s = {"rows": 0, "rows_2025": 0, "urls_2025": 0, "weak_domain_hits": Counter()}
        print(f"--- {tname} ---", flush=True)
        with gzip.open(path, "rt", errors="replace") as gz:
            for line in gz:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                s["rows"] += 1
                ts = str(row.get("created_at") or "")
                rid = str(row.get("id") or row.get("event_index") or s["rows"])
                text = text_of(row, fields)
                # marker scan (all dates)
                low = text.lower()
                for mname, mrx in MARKERS:
                    if mrx.search(text):
                        marker_hits[mname].append((ts, tname, rid))
                if ts >= CUTOFF or not ts:
                    continue
                s["rows_2025"] += 1
                # phrase scan (dsqa fingerprints)
                for ph in phrases:
                    if ph.lower() in low:
                        i = low.find(ph.lower())
                        matches.write(json.dumps({
                            "match_type": "dsqa_phrase", "our_value": ph,
                            "village_table": tname, "row_id": rid, "created_at": ts,
                            "context": text[max(0, i-30):i+len(ph)+30]}) + "\n")
                # uuid scan
                for m in UUID_RE.findall(text):
                    if m.lower() in our_uuids:
                        i = text.lower().find(m.lower())
                        matches.write(json.dumps({
                            "match_type": "uuid", "our_value": m.lower(),
                            "village_table": tname, "row_id": rid, "created_at": ts,
                            "context": text[max(0, i-30):i+len(m)+30]}) + "\n")
                # discord token scan
                for m in DISCORD_WH_RE.findall(text):
                    if m.lower() in our_dctokens:
                        i = text.lower().find(m.lower())
                        matches.write(json.dumps({
                            "match_type": "webhook_token", "our_value": m,
                            "village_table": tname, "row_id": rid, "created_at": ts,
                            "context": text[max(0, i-30):i+len(m)+30]}) + "\n")
                # url scan
                for m in URL_RE.findall(text):
                    u = clean_url(m)
                    if len(u) < 12:
                        continue
                    s["urls_2025"] += 1
                    d = domain_of(u)
                    mtype = None
                    if u in our_urls:
                        mtype = "full_url"
                    elif d in fp:
                        mtype = "fingerprint_domain"
                    if mtype:
                        i = text.find(m)
                        matches.write(json.dumps({
                            "match_type": mtype, "our_value": u if mtype == "full_url" else d,
                            "village_url": u, "village_table": tname, "row_id": rid,
                            "created_at": ts,
                            "context": text[max(0, i-30):i+len(m)+30]}) + "\n")
                    elif d in alld:
                        s["weak_domain_hits"][d] += 1
                if s["rows"] % 500000 == 0:
                    print(f"  {tname}: {s['rows']} rows...", flush=True)
        s["weak_domain_hits"] = dict(s["weak_domain_hits"].most_common(25))
        stats[tname] = s
        print(f"  done {tname}: {s['rows']} rows, {s['rows_2025']} in 2025, {s['urls_2025']} urls",
              flush=True)

    # recreation window from markers
    window = {}
    for mname, hits in marker_hits.items():
        tss = sorted(t for t, _, _ in hits if t)
        window[mname] = {"count": len(hits), "first": tss[0] if tss else None,
                         "last": tss[-1] if tss else None,
                         "sample": hits[:5]}
    with open(os.path.join(OUT, "join-stats.json"), "w") as f:
        json.dump({"per_table": stats, "marker_window": window}, f, indent=1, default=str)
    matches.close()
    print("WROTE matches-2025.jsonl + join-stats.json", flush=True)

if __name__ == "__main__":
    main()
