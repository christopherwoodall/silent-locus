"""Lane 8 — Database URL mining (lane id: db-url-mining).

Mines OUR OWN collected data (Factum corpus records, the canonical URL
inventory, and hunt lane artifacts) for web surfaces that look ripe for
agent repurposing — the same move the Amap fleet pulled on urlquery.net
(remote code runner) and webhook.site (exfil).

Unlike the other swarm-infra scanners (SECONDARY evidence: other people's
artifacts), this lane analyzes our own database, so hits carry
grade "PRIMARY".

Scoring criteria per domain (target_score = count met, 1-6):
  1. programmability — domain matches a known programmable surface pattern
     (shortener, pastebin, webhook tester, proxy/markdown reader, QR API,
     file host, pubsub, agent venue) in config `target_surfaces`.
  2. low_auth — the matched surface is flagged `no_auth: true` (no login
     needed to create/store content).
  3. persistence — matched surface flagged `persistent: true` (stored
     content stays addressable via a stable URL).
  4. observability — matched surface flagged `public_read: true` (a third
     party can read the stored content).
  5. traffic — domain mention count in our corpus >=
     config `dbmining.min_traffic_count` (agent activity blends in).
  6. prior_agent_contact — domain is in config `agent_contact_surfaces`
     (already observed repurposed by agents) OR appears in records tagged
     with an agent-tradecraft lane marker.

"New" for the daily cron: a domain first seen in the since_hours window,
or an existing domain whose mention count spiked (window count >=
spike_ratio * previous-window count, with a minimum count floor).
scan(full=True) runs the initial baseline sweep over everything.

Read-only against the database. The only write is the scanner's own
state file (scripts/scanners/state/dbmining_state.json).

Contract: scan(since_hours=24, seen_ids=None, dry_run=False) -> list[dict]
"""
from __future__ import annotations

import datetime
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import load_config, utcnow_iso, is_new, mark_seen  # noqa: E402

LANE = "db-url-mining"
GRADE = "PRIMARY"

REPO = os.path.expanduser("~/workspace/silent-locus")
STATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state", "dbmining_state.json"
)

URL_RE = re.compile(r'https?://[^\s<>"\'\]\)\},;]+', re.IGNORECASE)

DEFAULT_CFG = {
    "min_traffic_count": 30,
    "min_spike_count": 5,
    "spike_ratio": 2.0,
    "min_target_score": 2,
    "max_hits": 20,
    "agent_tradecraft_lane_markers": [
        "amap",
        "webhook-deaddrop",
        "pastebin-k4be",
        "agent-convo-venue",
        "chinese",
        "rogue-agent",
        "urlquery-marker",
    ],
    "exclude_hosts": [
        "localhost",
        "127.0.0.1",
        "example.com",
        "example.org",
        "example.net",
    ],
}

# Built-in programmable-surface patterns (config `target_surfaces` extends /
# overrides these). Regex matched against the lowercased host.
DEFAULT_SURFACES = [
    {"pattern": r"^urlquery\.net$", "category": "security-scanner/code-runner",
     "no_auth": True, "persistent": True, "public_read": True,
     "notes": "Amap fleet repurposed as remote code runner"},
    {"pattern": r"^webhook\.site$", "category": "webhook-tester",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Amap fleet exfil endpoint; inboxes public by URL"},
    {"pattern": r"^da\.gd$", "category": "shortener",
     "no_auth": True, "persistent": True, "public_read": True,
     "notes": "Anthropic/Claude operator-confirmed shortener tradecraft"},
    {"pattern": r"^(tinyurl\.com|bit\.ly|is\.gd|t\.ly|shorturl\.at|rebrand\.ly)$",
     "category": "shortener", "no_auth": True, "persistent": True,
     "public_read": True, "notes": "Public shortener, anonymous create"},
    {"pattern": r"^r\.jina\.ai$", "category": "proxy/markdown-reader",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Jina reader laundering marker in OAI tradecraft"},
    {"pattern": r"^(pure\.md|markdown\.new)$", "category": "proxy/markdown-reader",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Markdown-render proxy of arbitrary URLs"},
    {"pattern": r"^(api\.cors\.lol|cors\.lol|corsmirror\.com|allorigins\.hexlet\.app|cors\.bwa\.workers\.dev)$",
     "category": "cors-proxy", "no_auth": True, "persistent": False,
     "public_read": True, "notes": "Open CORS proxy: fetch arbitrary URL server-side"},
    {"pattern": r"^jqp\.vercel\.app$", "category": "relay/proxy",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Relay wrapper seen in intermediary-relay sweep"},
    {"pattern": r"^md\.succ\.ai$", "category": "relay/proxy",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Relay target seen in corpus"},
    {"pattern": r"^(pastebin\.com|paste\.rs|ix\.io|0x0\.st|termbin\.com|paste\.ee|hastebin\.com|privatebin\.net)$",
     "category": "pastebin", "no_auth": True, "persistent": True,
     "public_read": True, "notes": "Anonymous paste, public read"},
    {"pattern": r"^(paste\.linuxiarz\.pl|pastebin\.k4be\.pl)$", "category": "pastebin",
     "no_auth": True, "persistent": True, "public_read": True,
     "notes": "Pastebins already in hunt corpus"},
    {"pattern": r"^(ntfy\.sh)$", "category": "pubsub",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Anonymous pub/sub topic, public read by topic name"},
    {"pattern": r"^(api\.qrserver\.com|quickchart\.io)$", "category": "qr-api",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "QR/image API reflects arbitrary input into output"},
    {"pattern": r"^(transfer\.sh|file\.io|catbox\.moe|uguu\.se)$", "category": "file-host",
     "no_auth": True, "persistent": True, "public_read": True,
     "notes": "Anonymous file host, stable URL"},
    {"pattern": r"^(beeceptor\.com|pipedream\.net|webhook-test\.com)$",
     "category": "webhook-tester", "no_auth": True, "persistent": False,
     "public_read": True, "notes": "Free webhook receiver / request inspector"},
    {"pattern": r"^(swarm\.termina\.digital|tantive\.space|thecolony\.ai)$",
     "category": "agent-venue", "no_auth": True, "persistent": True,
     "public_read": True, "notes": "Agent conversation venues in hunt corpus"},
    {"pattern": r"^(goto\.unm\.edu|u\.ethz\.ch|go\.uvm\.edu)$", "category": "shortener",
     "no_auth": False, "persistent": True, "public_read": True,
     "notes": "University shorteners; creation needs campus login but links are public"},
    {"pattern": r"^t\.mdcdev\.me$", "category": "shortener",
     "no_auth": True, "persistent": True, "public_read": True,
     "notes": "Shortener seen in university sweep data"},
    {"pattern": r"^url\.popcat\.xyz$", "category": "shortener",
     "no_auth": True, "persistent": True, "public_read": True,
     "notes": "Shortener seen in yourls resweep raw data"},
    {"pattern": r"^(jsonhero\.io)$", "category": "json-viewer/proxy",
     "no_auth": True, "persistent": False, "public_read": True,
     "notes": "Fetches and renders arbitrary JSON URLs"},
]

# Surfaces already observed repurposed by agents (prior agent contact).
DEFAULT_AGENT_CONTACT = [
    {"domain": "urlquery.net", "provenance": "Amap fleet remote-code-runner (PRIMARY, 2026-09-28-chinese-amap-fleet)"},
    {"domain": "webhook.site", "provenance": "Amap fleet exfil dead-drop (SECONDARY swarmcha.se, PRIMARY fleet evidence)"},
    {"domain": "da.gd", "provenance": "Anthropic/Claude operator-confirmed shortener tradecraft (PRIMARY)"},
    {"domain": "r.jina.ai", "provenance": "Jina laundering marker in OAI working hypothesis (PRIMARY)"},
]


def _cfg():
    cfg = load_config()
    db = dict(DEFAULT_CFG)
    db.update(cfg.get("dbmining", {}))
    surfaces = list(DEFAULT_SURFACES)
    surfaces.extend(cfg.get("target_surfaces", []))
    contact = {c["domain"]: c["provenance"] for c in DEFAULT_AGENT_CONTACT}
    for c in cfg.get("agent_contact_surfaces", []):
        contact[c["domain"]] = c.get("provenance", "config-listed")
    return db, surfaces, contact


def _iter_sources():
    """Yield (url, source_name, observed_at_iso_or_None, lane_tag_string)."""
    # 1. Factum corpus records (direct data/records grep is authoritative).
    rec_glob = os.path.join(REPO, "data", "records", "*", "records.jsonl")
    for path in sorted(glob.glob(rec_glob)):
        try:
            fh = open(path, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                ts = None
                lanes = ""
                try:
                    d = json.loads(line)
                    ts = d.get("@timestamp")
                    tags = d.get("tags") or {}
                    lanes = str(tags.get("lane", ""))
                except Exception:
                    pass
                for u in URL_RE.findall(line):
                    yield u.rstrip(".,;:!?"), "factum:data/records", ts, lanes
    # 2. Canonical URL inventory.
    inv = os.path.join(REPO, "lists", "urls", "urls.jsonl")
    if os.path.exists(inv):
        with open(inv, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    u = d.get("url")
                except Exception:
                    continue
                if u:
                    yield u, "lists/urls/urls.jsonl", None, ""
    # 3. Legacy Transluce URL inventory (read-only).
    leg = os.path.join(REPO, "evidence", "transluce-api", "url-inventory.jsonl")
    if os.path.exists(leg):
        with open(leg, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                for u in URL_RE.findall(line):
                    yield u.rstrip(".,;:!?"), "evidence/transluce-api/url-inventory.jsonl", None, ""
    # 4. Hunt lane inventory artifacts.
    for rel in [
        "data/lanes/2026-09-28-yourls-resweep/events.jsonl",
        "data/lanes/urlquery-marker-sweep/events.jsonl",
    ]:
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                for u in URL_RE.findall(line):
                    yield u.rstrip(".,;:!?"), rel, None, ""


def _parse_ts(ts):
    if not ts:
        return None
    try:
        return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def collect_domains():
    """Aggregate URL mentions per domain.

    Returns dict domain -> {
        count, first_seen (datetime|None), last_seen, sources Counter,
        lanes set, example_urls list, ts_list [datetimes]
    }.
    """
    db, surfaces, contact = _cfg()
    compiled = [(re.compile(s["pattern"], re.IGNORECASE), s) for s in surfaces]
    exclude = {h.lower() for h in db["exclude_hosts"]}
    aggs = {}

    def agg_for(host):
        if host not in aggs:
            aggs[host] = {
                "count": 0, "first_seen": None, "last_seen": None,
                "sources": Counter(), "lanes": set(), "example_urls": [],
                "ts": [],
            }
        return aggs[host]

    for url, source, ts_raw, lane in _iter_sources():
        try:
            host = urlparse(url).hostname
        except Exception:
            continue
        if not host:
            continue
        host = host.lower().rstrip(".")
        if host in exclude or "@" in host:
            continue
        a = agg_for(host)
        a["count"] += 1
        a["sources"][source] += 1
        if lane:
            a["lanes"].add(lane)
        if len(a["example_urls"]) < 5 and url not in a["example_urls"]:
            a["example_urls"].append(url)
        dt = _parse_ts(ts_raw)
        if dt:
            a["ts"].append(dt)
            if a["first_seen"] is None or dt < a["first_seen"]:
                a["first_seen"] = dt
            if a["last_seen"] is None or dt > a["last_seen"]:
                a["last_seen"] = dt
    return aggs, compiled, db, contact


def score_domain(host, a, compiled, db, contact):
    """Return (criteria_list, categories, notes)."""
    criteria = []
    categories = []
    notes = []
    matched_flags = {"no_auth": False, "persistent": False, "public_read": False}
    for rx, s in compiled:
        if rx.search(host):
            categories.append(s["category"])
            for flag in matched_flags:
                if s.get(flag):
                    matched_flags[flag] = True
            if s.get("notes"):
                notes.append(s["notes"])
    categories = sorted(set(categories))
    if categories:
        criteria.append("programmability")
    if matched_flags["no_auth"]:
        criteria.append("low_auth")
    if matched_flags["persistent"]:
        criteria.append("persistence")
    if matched_flags["public_read"]:
        criteria.append("observability")
    if a["count"] >= db["min_traffic_count"]:
        criteria.append("traffic")
    prior = None
    if host in contact:
        prior = contact[host]
    else:
        for lane in a["lanes"]:
            ll = lane.lower()
            if any(m in ll for m in db["agent_tradecraft_lane_markers"]):
                prior = f"appears in agent-tradecraft lane tag '{lane}'"
                break
    if prior:
        criteria.append("prior_agent_contact")
        notes.append(f"prior agent contact: {prior}")
    return criteria, categories, notes


def _spike(counts_now, counts_prev, db):
    return (
        counts_now >= db["min_spike_count"]
        and counts_prev >= 0
        and counts_now >= db["spike_ratio"] * max(counts_prev, 1)
        and (counts_prev == 0 or counts_now > counts_prev)
    )


def _make_hit(host, a, criteria, categories, notes, reason):
    # COUNSEL FIX (adversarial 2026-10-14): target_score DEMOTED to
    # annotation. The 6 criteria are not discriminative of future agent
    # adoption -- criteria 1-4 restate the hardcoded pattern list,
    # criterion 5 counts our own corpus mentions, criterion 6 is circular.
    # The score describes "how programmable is this surface", NOT
    # "how likely are agents to use it". Ranking is by reason + activity.
    return {
        "lane": LANE,
        "domain": host,
        "url": a["example_urls"][0] if a["example_urls"] else f"https://{host}/",
        "criteria": criteria,
        "categories": categories,
        "target_score": len(criteria),  # annotation only, not predictive
        "grade": GRADE,
        "reason": reason,  # "new" | "spike" | "baseline"
        "confidence": "LOW",  # hypothesis feeder, not a detection
        "provenance": {
            "sources": dict(a["sources"]),
            "occurrences": a["count"],
            "first_seen": a["first_seen"].isoformat() if a["first_seen"] else None,
            "last_seen": a["last_seen"].isoformat() if a["last_seen"] else None,
            "lanes": sorted(a["lanes"]),
        },
        "evidence": {
            "example_urls": a["example_urls"][:5],
            "notes": notes,
        },
        "observed_at": utcnow_iso(),
    }


def scan(since_hours=24, seen_ids=None, dry_run=False, full=False):
    """Run the lane-8 database URL-mining scan.

    full=True: baseline sweep — every scored domain with
        target_score >= min_target_score, ranked desc, capped at max_hits.
    full=False: only domains first seen within since_hours, or with an
        activity spike in the window vs the previous equal window.
    seen_ids: optional set for dedup ("dbmining:<domain>" keys).
    """
    aggs, compiled, db, contact = collect_domains()
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(hours=since_hours)
    prev_cutoff = cutoff - datetime.timedelta(hours=since_hours)

    hits = []
    for host in sorted(aggs):
        a = aggs[host]
        criteria, categories, notes = score_domain(host, a, compiled, db, contact)
        if len(criteria) < db["min_target_score"]:
            continue
        if full:
            key = f"dbmining:{host}"
            if is_new(seen_ids, key):
                mark_seen(seen_ids, key)
                hits.append(_make_hit(host, a, criteria, categories, notes, "baseline"))
            continue
        # incremental: new or spike
        reason = None
        if a["first_seen"] and a["first_seen"] >= cutoff:
            reason = "new"
        else:
            now_n = sum(1 for t in a["ts"] if t >= cutoff)
            prev_n = sum(1 for t in a["ts"] if prev_cutoff <= t < cutoff)
            if _spike(now_n, prev_n, db):
                reason = "spike"
        if reason:
            key = f"dbmining:{host}:{reason}"
            if is_new(seen_ids, key):
                mark_seen(seen_ids, key)
                hits.append(_make_hit(host, a, criteria, categories, notes, reason))

    # Rank by reason (new/spike first) then activity, NOT by target_score
    # (adversarial: score is annotation, not predictive).
    reason_rank = {"new": 0, "spike": 1, "baseline": 2}
    hits.sort(key=lambda h: (reason_rank.get(h["reason"], 3),
                             -h["provenance"]["occurrences"]))
    hits = hits[: db["max_hits"]]

    if not dry_run:
        os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
        state = {
            "last_run": utcnow_iso(),
            "full": full,
            "since_hours": since_hours,
            "domains_scored": len(aggs),
            "hits_emitted": len(hits),
        }
        tmp = STATE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2)
        os.replace(tmp, STATE_PATH)
    return hits


def main():
    import argparse

    ap = argparse.ArgumentParser(description="Lane 8: database URL mining")
    ap.add_argument("--dry-run", action="store_true",
                    help="Score and print hits; write no state.")
    ap.add_argument("--since-hours", type=float, default=24,
                    help="Look-back window in hours (default: 24).")
    ap.add_argument("--full", action="store_true",
                    help="Baseline sweep over all data.")
    ap.add_argument("--json", action="store_true",
                    help="Print hits as JSON array.")
    args = ap.parse_args()
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run, full=args.full)
    if args.dry_run:
        print(f"[dry-run] would return {len(hits)} hits", file=sys.stderr)
    if args.json or args.dry_run:
        print(json.dumps(hits, indent=2, ensure_ascii=False))
    else:
        for h in hits:
            print(f"[score {h['target_score']}] {h['domain']} "
                  f"({h['provenance']['occurrences']} mentions) "
                  f"[{', '.join(h['criteria'])}] <{h['reason']}>")
            print(f"    {h['url']}")
        print(f"\n{len(hits)} hits")


if __name__ == "__main__":
    main()
