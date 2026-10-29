#!/usr/bin/env python3
"""Lane 9 — Jina AI reader scanner: text-extraction proxy for target surfaces.

Fetches target URLs through the Jina AI reader (https://r.jina.ai/<url>)
and scans the clean extracted text for IOC patterns:

  - webhook.site inbox UUIDs (dead-drop endpoints)
  - ntfy.sh topic names (pub/sub dead drops)
  - Tag grammars: uqscan=, uqframe=, uqtag=, uq=, zz= (fleet markers)
  - Base64 payload runs >=40 chars (program-packing tradecraft)
  - Agent infrastructure terms from the word list

r.jina.ai is used throughout this hunt as a text-extraction proxy
(173 hits in the URL inventory) and as a laundering hop in several
investigations. This module makes that usage systematic: a watchlist
of target URLs, fetched on schedule, with NEW IOCs reported.

Rate limits: the Jina free tier is rate-limited. This module spaces
requests 10 s apart and backs off on HTTP 429 with 60/120 s retries.
If the tier blocks us, targets are skipped (not marked seen) so the
next run retries them.

Jina returns live text with no capture timestamp, so --since-hours
does not filter by time here. "New" means IOCs not previously seen
for that target URL (content-hash dedup via seen_ids).

Passive only. GET requests through the reader proxy. No POST, no
interaction, no logins.

This module watches OUR targets through jina. The reverse direction —
how OTHER agents use jina, reconstructed from third-party records of
r.jina.ai/<url> fetches — is documented in
docs/jina-activity-methodology.md and wired as phase-1 queries in
swarm-infra-config.json (urlscan `relay-jina-reader`, wayback
`r.jina.ai` domain target, urlquery `r.jina.ai/` family).

IP-classification note (standing rule): Jina reader output carries no
IP addresses (it is extracted page text), so jina hits record no IPs
and attach no ip_classification. If an IP field is ever added to
these hits, it must be classified via
_common.attach_ip_classification before this module ships.

Usage:
    jina.py [--dry-run] [--since-hours 24] [--json]

Targets come from ~/workspace/silent-locus/scripts/swarm-infra-config.json
("jina" block).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit, normalize, report_error,
)

LANE = "jina"
JINA_BASE = "https://r.jina.ai/"
REQUEST_SPACING = 10  # seconds between requests (free-tier politeness)
RETRY_SLEEPS = (60, 120)  # backoff on 429 / transport failures
MAX_TEXT = 200_000  # cap fetched text at 200 KB

# IOC patterns scanned in extracted text
WEBHOOK_UUID_RE = re.compile(
    r"webhook\.site/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)
NTFY_TOPIC_RE = re.compile(r"ntfy\.sh/([a-zA-Z0-9_-]{3,64})")
TAG_GRAMMAR_RES = [
    re.compile(r"uqscan=([a-zA-Z0-9_-]+)"),
    re.compile(r"uqframe=([a-zA-Z0-9_-]+)"),
    re.compile(r"uqtag=([a-zA-Z0-9_-]+)"),
    re.compile(r"[?&]uq=([a-zA-Z0-9_-]+)"),
    re.compile(r"zz=([a-zA-Z0-9_-]+)"),
]
B64_RUN_RE = re.compile(r"[A-Za-z0-9+/=]{40,}")


def _fetch_via_jina(target_url: str, label: str) -> tuple[int, str | None]:
    """GET https://r.jina.ai/<url>. Returns (status, text)."""
    jina_url = JINA_BASE + target_url
    req = urllib.request.Request(jina_url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/plain",
        "X-Return-Format": "text",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read(MAX_TEXT + 1)
            text = raw[:MAX_TEXT].decode("utf-8", "replace")
            return resp.status, text
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"[jina] {label}: HTTP 429 rate-limited",
                  file=sys.stderr)
        else:
            print(f"[jina] {label}: HTTP {e.code}", file=sys.stderr)
        return e.code, None
    except Exception as e:
        print(f"[jina] {label}: {type(e).__name__}: {e}",
              file=sys.stderr)
        return -1, None


def _fetch_with_retry(target_url: str, label: str) -> str | None:
    for attempt, sleep_s in enumerate([0] + list(RETRY_SLEEPS)):
        if sleep_s:
            print(f"[jina] {label}: retrying in {sleep_s}s "
                  f"(attempt {attempt + 1})", file=sys.stderr)
            time.sleep(sleep_s)
        status, text = _fetch_via_jina(target_url, label)
        if status == 200 and text is not None:
            return text
        if status == 429:
            continue  # retry on rate limit
        if status in (401, 403, 404):
            # Definitive: not a retryable failure
            return None
    print(f"[jina] {label}: giving up after "
          f"{1 + len(RETRY_SLEEPS)} attempts", file=sys.stderr)
    return None


def _extract_iocs(text: str, config: dict) -> dict:
    """Scan extracted text for IOC patterns. Returns {kind: [values]}."""
    iocs: dict[str, list] = {}

    # webhook.site inbox UUIDs
    uuids = sorted(set(WEBHOOK_UUID_RE.findall(text)))
    if uuids:
        iocs["webhook_uuids"] = uuids

    # ntfy.sh topics (pattern matches + config watchlist)
    topics = sorted(set(NTFY_TOPIC_RE.findall(text)))
    watchlist = config.get("ntfy_topics", [])
    for t in watchlist:
        if t in text and t not in topics:
            topics.append(t)
    if topics:
        iocs["ntfy_topics"] = sorted(topics)

    # Tag grammars (fleet markers)
    tags = []
    for rx in TAG_GRAMMAR_RES:
        tags.extend(rx.findall(text))
    # Also check config tag_patterns literally
    for pat in config.get("tag_patterns", []):
        if pat in text:
            tags.append(pat)
    if tags:
        iocs["tag_grammars"] = sorted(set(tags))

    # Base64 payload runs (use _common.normalize for decode variants)
    b64_hits = []
    for variant in normalize(text[:50_000]):  # cap for perf
        for m in set(B64_RUN_RE.findall(variant)):
            if len(m) >= 40:
                b64_hits.append(m[:80])  # truncate for hit record
    if b64_hits:
        iocs["b64_runs"] = sorted(set(b64_hits))[:20]  # cap at 20

    return iocs


def _ioc_fingerprint(target_url: str, iocs: dict) -> str:
    """Content hash of extracted IOCs for dedup."""
    canonical = json.dumps(iocs, sort_keys=True)
    digest = hashlib.sha256(
        f"{target_url}|{canonical}".encode()).hexdigest()[:32]
    return f"jina:{digest}"


def scan_target(target: dict, seen_ids, collected_at: str,
                dry_run: bool, config: dict) -> list:
    url = target["url"]
    label = target.get("label", url)
    hits = []

    if dry_run:
        print(f"[dry-run] jina target: {label} (url={url!r})",
              file=sys.stderr)
        return hits

    text = _fetch_with_retry(url, label)
    if text is None:
        # Failed fetch: do NOT mark seen, next run retries
        report_error("jina", "fetch_failed",
                     f"target {label!r} returned no text",
                     {"url": url[:200]})
        return hits

    iocs = _extract_iocs(text, config)
    if not iocs:
        print(f"[jina] {label}: no IOCs in {len(text)} chars",
              file=sys.stderr)
        return hits

    key = _ioc_fingerprint(url, iocs)
    if not is_new(seen_ids, key):
        print(f"[jina] {label}: IOCs unchanged since last run",
              file=sys.stderr)
        return hits

    # Flatten IOC kinds for indicators_matched
    indicators = []
    for kind, vals in iocs.items():
        indicators.extend(f"{kind}:{v}" for v in vals[:10])

    # Confidence: webhook UUIDs and tag grammars are HIGH (direct
    # fleet markers); ntfy topics MEDIUM; b64 runs LOW without context
    if iocs.get("webhook_uuids") or iocs.get("tag_grammars"):
        confidence = "HIGH"
    elif iocs.get("ntfy_topics"):
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    hits.append(make_hit(
        lane=LANE,
        source_url=f"https://r.jina.ai/{url}",
        indicators_matched=indicators[:30],
        confidence=confidence,
        summary=f"[jina] {label} — {len(indicators)} IOCs in reader text",
        provenance={
            "method": "Jina AI reader (r.jina.ai) text extraction",
            "target_url": url,
            "text_chars": len(text),
            "retrieved_at": collected_at,
        },
        extra={
            "target_label": label,
            "ioc_kinds": sorted(iocs.keys()),
            "webhook_uuids": iocs.get("webhook_uuids", []),
            "ntfy_topics": iocs.get("ntfy_topics", []),
            "tag_grammars": iocs.get("tag_grammars", []),
        },
        grade="PRIMARY",
    ))
    mark_seen(seen_ids, key)
    print(f"[jina] {label}: NEW IOCs ({confidence})", file=sys.stderr)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Fetch targets via Jina reader, report NEW IOCs. Returns hit dicts.

    Note: since_hours is accepted for contract compliance but Jina
    returns live text with no timestamps; newness is determined by
    content-hash dedup, not time window.
    """
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    targets = cfg.get("jina", {}).get("targets", [])
    collected_at = utcnow_iso()

    if not targets:
        print("[jina] no targets in config 'jina' block", file=sys.stderr)
        return []

    hits = []
    for i, t in enumerate(targets):
        try:
            hits.extend(scan_target(t, seen_ids, collected_at, dry_run,
                                    cfg))
        except Exception as e:
            report_error("jina", "target_failed",
                         f"{t.get('label', t.get('url'))}: {e}",
                         {"url": str(t.get("url"))[:200]})
            print(f"[jina] target {t.get('label')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
        if not dry_run and i < len(targets) - 1:
            time.sleep(REQUEST_SPACING)  # free-tier politeness
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Lane 9 — Jina AI reader scanner (IOC extraction)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
