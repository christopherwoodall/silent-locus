#!/usr/bin/env python3
"""Lane 3: ntfy.sh monitor for Chinese Amap agent-fleet dead-drop topics.

Passive-only watch over known and candidate ntfy.sh topics used as fleet
exfil dead-drops (v3 "amap probe" grammar posts JSON results to ntfy.sh
topics of the form amapdata-<POI>-<suffix>; POI ID is embedded in the
topic name).

Primary transport: ntfy JSON API poll, GET
    https://ntfy.sh/<topic>/json?poll=1
which returns newline-delimited JSON messages (or [] when the window is
empty). ntfy.sh free tier retains ~12h of messages; an empty poll means
"no messages in window", NOT "topic never existed".

KNOWN GAP (verified 2026-10-14): ntfy.sh is unreachable through our
egress proxy (TCP fails, HTTP 000). The module does NOT treat this as a
clean negative. On transport failure it attempts, in order:
  1. r.jina.ai relay of the same JSON URL -- also fails for ntfy.sh
     (jina returns 422 "Unexpected empty file: https://ntfy.sh";
     verified 2026-10-14). Kept as an attempted step with its known
     outcome so future runs re-check rather than assume.
  2. Wayback CDX (http://web.archive.org/cdx, port 80 works per
     workspace TOOLS.md): query for archived captures of
     ntfy.sh/<topic> -- documents HISTORICAL existence/content only.
Any transport gap is reported on stderr and in each hit's provenance;
scans that only achieved the gap outcome emit zero hits, never a
"no fleet activity" claim.

Topic discovery: ntfy has no public topic directory, so new topics can
only be checked by name. Candidate patterns come from config
(ntfy_topic_patterns); while direct polling is blocked, existence is
probed via CDX matchType=prefix (archived history only) and recorded
as "exists in archive" / "no archive record" / "unknown (blocked)".

Contract:
    scan(since_hours=24, seen_ids=None, dry_run=False) -> list[dict]

CLI:
    ntfy.py [--since-hours N] [--dry-run] [--json]
"""
from __future__ import annotations

import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _common as C
from ip_classifier import classify_ip

LANE = "ntfy-amap-watch"
UA = {"User-Agent": C.USER_AGENT}
POLL_TIMEOUT = 20
DELAY = 3.0  # polite spacing between polls
IP_CACHE_PATH = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/ip_asn_cache.json")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

# Content regexes marking a ntfy message as agent-relevant (fleet exfil).
# COUNSEL FIXES (2026-10-14):
#  - cryptologist: poi_id was case-sensitive, missed fleet's own lowercase
#    b0g3lmf2g1 -- added IGNORECASE
#  - linguist H5: fleet_grammar used bare uqscan/uqframe (no =), bare
#    webhook.site, typo-shaped nfy\( -- tightened to require = and
#    word boundaries
#  - adversarial: topic name is published in writeups (copycat risk);
#    confidence capped at MEDIUM in _make_hit, fleet_grammar demoted
CONTENT_RULES = [
    ("amap_mention", re.compile(r"amap|gaode", re.IGNORECASE)),
    ("poi_id", re.compile(r"\bB0[A-Z0-9]{8}\b", re.IGNORECASE)),  # Amap POI id grammar (10 chars)
    ("fleet_grammar", re.compile(r"(uqscan=|uqframe=|uqtag=|webhook\.site/[a-f0-9]{8}-)")),
    ("claude_label", re.compile(r"claude20\d{6,}", re.IGNORECASE)),
]
# fleet_grammar is DEMOTED: cannot distinguish quoting the fleet from
# being the fleet. It contributes to multi-rule hits only.

RETENTION_HOURS = 12  # ntfy.sh free-tier message retention


def _poll_topic(topic: str):
    """Poll one topic. Returns (status, payload) where status is one of:
    'ok' (list of message dicts), 'empty', 'blocked' (transport gap)."""
    url = f"https://ntfy.sh/{urllib.parse.quote(topic, safe='')}/json?poll=1"
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=POLL_TIMEOUT) as resp:
            body = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        return "blocked", str(e)
    msgs = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msgs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return ("empty" if not msgs else "ok"), msgs


def _jina_relay(topic: str):
    """Attempt the r.jina.ai relay of the same JSON poll.

    Known outcome (verified 2026-10-14): jina cannot fetch ntfy.sh and
    returns 422 AssertionFailureError. Kept as an attempted step so the
    gap is re-checked rather than assumed on every run."""
    inner = f"https://ntfy.sh/{urllib.parse.quote(topic, safe='')}/json?poll=1"
    url = "https://r.jina.ai/" + inner
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = resp.read().decode("utf-8", "replace")
        return "ok", body[:200]
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        return "blocked", str(e)


def _cdx_lookup(topic: str, prefix: bool = False):
    """Wayback CDX lookup for a topic (historical existence only).

    Uses http:// (port 80): web.archive.org:443 is blocked by our egress
    proxy (workspace TOOLS.md). Returns (ok, list of capture dicts)."""
    q = {
        "url": f"ntfy.sh/{topic}",
        "output": "json",
        "limit": 50,
    }
    if prefix:
        q["matchType"] = "prefix"
        q["collapse"] = "urlkey"
    url = ("http://web.archive.org/cdx/search/cdx?"
           + urllib.parse.urlencode(q))
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001 - archive backend is flaky
        return False, str(e)
    if not data:
        return True, []
    header, rows = data[0], data[1:]
    return True, [dict(zip(header, r)) for r in rows]


def _msg_time(msg: dict):
    ts = msg.get("time")
    if ts is None:
        return None
    try:
        return datetime.datetime.fromtimestamp(int(ts),
                                              tz=datetime.timezone.utc)
    except (ValueError, TypeError, OverflowError):
        return None


def _score_message(msg: dict) -> list:
    text = " ".join(str(msg.get(k, "")) for k in ("message", "title", "topic"))
    return [name for name, rx in CONTENT_RULES if rx.search(text)]


def _extract_global_ipv4s(text: str) -> list:
    """Distinct globally-routable IPv4s in text. Skips private/loopback/
    documentation ranges -- those are not infrastructure signal."""
    import ipaddress
    found = []
    for cand in IPV4_RE.findall(text or ""):
        try:
            addr = ipaddress.ip_address(cand)
        except ValueError:
            continue
        if addr.is_global and cand not in found:
            found.append(cand)
    return found


def _classify_ips(ips: list, config: dict) -> list:
    """Classify every IP (standing rule). Errors degrade to UNKNOWN."""
    out = []
    for ip in ips:
        try:
            out.append(classify_ip(ip, config, IP_CACHE_PATH))
        except Exception as e:  # noqa: BLE001 - degrade, don't crash
            print(f"  [warn] ip classification failed for {ip}: {e}",
                  file=sys.stderr)
            out.append({"ip": ip, "tier": 4, "label": "UNKNOWN",
                        "detail": f"classifier error: {e}", "asn": None,
                        "org": None, "country": None, "city": None,
                        "swarm_linked": False})
    return out


def _make_hit(topic: str, msg: dict, matched: list, transport_note: str,
              scanned_at: str, config: dict) -> dict:
    mid = msg.get("id", "?")
    # adversarial: cap at MEDIUM -- topic name is published in writeups,
    # anyone can POST, copycat can satisfy content rules with public POI ids
    confidence = "MEDIUM"
    body = str(msg.get("message", ""))[:280]
    summary = (f"ntfy.sh/{topic}: message {mid} matches "
               f"{', '.join(matched)}: {body[:80]}")
    hit = C.make_hit(
        lane=LANE,
        observed_at=(_msg_time(msg).isoformat().replace("+00:00", "Z")
                     if _msg_time(msg) else scanned_at),
        source_url=f"https://ntfy.sh/{topic}",
        indicators_matched=matched,
        confidence=confidence,
        summary=summary,
        provenance={
            "method": "ntfy JSON poll (GET /json?poll=1)",
            "transport": transport_note,
            "scanned_at": scanned_at,
            "retention_note": ("ntfy.sh free tier retains ~12h; "
                               "empty poll = no messages in window"),
        },
        grade="PRIMARY",
        extra={
            "topic": topic,
            "message_id": mid,
            "message_time": (_msg_time(msg).isoformat()
                             if _msg_time(msg) else None),
            "message_title": msg.get("title"),
            "message_tags": msg.get("tags"),
            "message_body": str(msg.get("message", ""))[:2000],
        },
    )
    # Standing rule: classify every IP the hit carries. Probe-result
    # bodies can embed resolved/infrastructure IPs.
    body_ips = _extract_global_ipv4s(body + " " + str(msg.get("title", "")))
    if body_ips:
        classified = _classify_ips(body_ips, config)
        hit["ip_classification"] = classified[0]
        if len(classified) > 1:
            hit["all_ip_classifications"] = classified
        # A cloud IP where you don't expect one is signal: flag it.
        if any(c.get("tier") in (1, 2) for c in classified):
            hit["priority"] = True
    return hit


def _pattern_stem(pattern: str) -> str:
    return pattern.rstrip("*")


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run the lane-3 ntfy watch.

    since_hours: look-back window for message timestamps (default 24;
        capped in practice by the ~12h ntfy free-tier retention).
    seen_ids: optional set for dedup (keys "ntfy:<topic>:<message_id>").
    dry_run: print what WOULD be polled; hit no network.
    """
    config = C.load_config()
    topics = config.get("ntfy_topics", [])
    patterns = config.get("ntfy_topic_patterns", [])
    scanned_at = C.utcnow_iso()
    hits = []

    if since_hours > RETENTION_HOURS:
        print(f"  [note] window {since_hours}h exceeds ntfy ~{RETENTION_HOURS}h "
              f"retention; only the retained window is visible",
              file=sys.stderr)

    if dry_run:
        print("[dry-run] ntfy.sh lane-3 monitor plan")
        print(f"  window: last {since_hours}h "
              f"(retention-limited to ~{RETENTION_HOURS}h)")
        for t in topics:
            print(f"  WOULD poll: https://ntfy.sh/{t}/json?poll=1")
            print(f"    fallback: r.jina.ai relay of same URL "
                  f"(known-fail 422, re-checked each run)")
            print(f"    fallback: CDX http://web.archive.org/cdx/search/cdx"
                  f"?url=ntfy.sh/{t}&output=json (historical only)")
        print("  WOULD probe candidate patterns (CDX prefix, "
              "historical existence):")
        for p in patterns:
            print(f"    ntfy.sh/{_pattern_stem(p)}*")
        print("  content rules (message must match >=1 to emit):")
        for name, rx in CONTENT_RULES:
            print(f"    {name:12s} {rx.pattern}")
        return hits

    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(hours=since_hours))

    # --- 1. Poll known topics -----------------------------------------
    for topic in topics:
        status, payload = _poll_topic(topic)
        time.sleep(DELAY)
        transport_note = "direct ntfy.sh poll"
        if status == "blocked":
            print(f"  [gap] ntfy.sh blocked ({payload[:80]}); "
                  f"trying fallbacks for {topic}", file=sys.stderr)
            jstatus, jpayload = _jina_relay(topic)
            time.sleep(DELAY)
            cdx_ok, captures = _cdx_lookup(topic)
            time.sleep(DELAY)
            print(f"  [gap] {topic}: jina relay -> {jstatus} "
                  f"({str(jpayload)[:70]}); "
                  f"CDX -> {'ok, %d captures' % len(captures) if cdx_ok else 'failed'}",
                  file=sys.stderr)
            transport_note = (
                "TRANSPORT GAP: ntfy.sh blocked at egress (HTTP 000); "
                "jina relay failed (known 422); "
                f"CDX archive lookup: {len(captures) if cdx_ok else 'failed'} "
                "historical captures. No live poll possible -- "
                "absence of hits here is a gap, not a clean negative.")
            continue  # no live data; do not fabricate hits from archive
        if status == "empty":
            print(f"  [ok] {topic}: no messages in window", file=sys.stderr)
            continue
        for msg in payload:
            mtime = _msg_time(msg)
            if mtime is not None and mtime < cutoff:
                continue
            matched = _score_message(msg)
            if not matched:
                continue
            key = f"ntfy:{topic}:{msg.get('id', '?')}"
            if C.is_new(seen_ids, key):
                C.mark_seen(seen_ids, key)
                hits.append(_make_hit(topic, msg, matched,
                                      transport_note, scanned_at, config))

    # --- 2. Candidate-topic discovery (archive only; direct poll is
    #        blocked, so existence via poll is 'unknown') --------------
    for pattern in patterns:
        stem = _pattern_stem(pattern)
        cdx_ok, captures = _cdx_lookup(stem, prefix=True)
        time.sleep(DELAY)
        if cdx_ok and captures:
            urls = sorted({c.get("original", "") for c in captures})
            print(f"  [discover] pattern {pattern}: {len(urls)} archived "
                  f"topic URL(s): {', '.join(urls[:5])}", file=sys.stderr)
        else:
            print(f"  [discover] pattern {pattern}: "
                  f"{'no archive record' if cdx_ok else 'CDX failed'}; "
                  f"live existence unknown (ntfy.sh blocked)", file=sys.stderr)

    hits.sort(key=lambda h: (h["observed_at"],), reverse=True)
    print(f"lane-3: {len(hits)} hits", file=sys.stderr)
    return hits


def main():
    args = C.parse_args("Lane 3: ntfy.sh Amap fleet topic monitor")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    C.emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
