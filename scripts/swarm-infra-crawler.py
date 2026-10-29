#!/usr/bin/env python3
"""
Swarm Infrastructure Crawler v2 — webhook.site creator-IP monitor.

Focused exclusively on webhook.site creator-IP records (per redirect).
The swarmcha.se report's Tencent attribution came from creator IPs:
when you view a webhook.site inbox, the token metadata exposes the
IP and user agent of whoever created it.

CRITICAL DISTINCTION:
  - Creator IP: who created the inbox (from token metadata).
    This is what we extract. This is the operator infrastructure signal.
  - Poster IP: who sent requests TO the inbox (from /requests endpoint).
    This is NOT what we extract here. Posters may use residential proxies.

Pipeline:
  1. Harvest webhook.site inbox URLs from urlquery (tag grammar + Amap watches)
  2. For each NEW inbox, GET token metadata -> extract creator IP + UA
  3. Classify creator IP (4 tiers via ip_classifier)
  4. Check factum for existing records (dedup)
  5. Write factum bundle v2 JSON (directly submittable via
     `factum add --input`)
  6. Creator-IP pivot mode (--module creator-pivot): broad webhook.site
     harvest from urlquery -> extract creator IP per inbox -> invert to
     creator-IP -> inboxes -> report watchlist-IP clusters (INFERENCE).
     Commissioned 2026-10-15: "The creator ip should scrape or search
     for inboxes."

Passive only: GET requests to public APIs. No POSTs (except the one-time
API structure verification, documented separately). No intrusive scanning.

Usage:
  swarm-infra-crawler.py [--dry-run] [--module MODULE] [--since-days N]
                         [--pivot-days N]

Modules: harvest, creator (default both), creator-pivot (discovery mode).

State:
  ~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/swarm-infra-crawler-state.json

Output:
  ~/workspace/silent-locus/data/lanes/swarm-infra-watch/crawl-<timestamp>.json
  ~/workspace/silent-locus/data/lanes/swarm-infra-watch/crawl-<timestamp>.bundle.json
  (bundle v2 — submit via `factum add --input <bundle>`; no separate
  lane-ingest worker needed)
"""

import argparse
import datetime
import ipaddress
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

# Import classifier from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ip_classifier import classify_ip, load_cache

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE = os.path.expanduser("~/workspace")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "swarm-infra-config.json")
STATE_PATH = os.path.join(
    WORKSPACE,
    "goals/urlquery-agent-activity-hunt/hidden_files/"
    "swarm-infra-crawler-state.json",
)
ASN_CACHE_PATH = os.path.join(
    WORKSPACE,
    "goals/urlquery-agent-activity-hunt/hidden_files/"
    "swarm-infra-asn-cache.json",
)
OUTPUT_DIR = os.path.join(
    WORKSPACE, "silent-locus/data/lanes/swarm-infra-watch")
UQ_HTMX = os.path.join(WORKSPACE, "skills/urlquery/bin/uq_htmx.py")

# Rate limits
DELAY_UQ = 3          # urlquery htmx: site throttles aggressive use
DELAY_WEBHOOKSITE = 2  # webhook.site: polite spacing

# urlquery search transport failures for this run (searches that failed
# all retry attempts; they must NOT be counted as zero results)
SEARCH_FAILURES = []

# Factum lane tag
LANE_TAG = "swarm-infra-watch"

# ---------------------------------------------------------------------------
# Detection rules with false-positive analysis
# ---------------------------------------------------------------------------
RULES = {
    "creator-ip": {
        "description": (
            "webhook.site inbox creator IP extracted from token metadata. "
            "The creator IP indicates who set up the exfil infrastructure, "
            "distinct from poster IPs (who sent requests to the inbox)."
        ),
        "fp_sources": [
            "Legitimate users creating webhook.site inboxes for testing.",
            "Researchers creating inboxes to study the fleet.",
            "Unrelated automation using webhook.site for legitimate webhooks.",
        ],
        "mitigations": [
            "Only process inboxes found via fleet-indicator searches "
            "(tag grammar, Amap tradecraft), not all webhook.site inboxes.",
            "Classification tiers separate signal (tiers 1-2) from noise.",
            "Creator UA checked: python-requests/2.32.5 is a fleet marker.",
        ],
        "corroboration_for_medium": (
            "Inbox found via fleet-indicator search AND "
            "creator IP in tier 1-2"
        ),
    },
    "creator-pivot": {
        "description": (
            "Creator-IP pivot cluster: a watchlist creator IP created "
            "multiple webhook.site inboxes. Discovery method, not a "
            "classification field — inverts broad inbox enumeration into "
            "creator-IP -> inbox maps. Commissioned 2026-10-15."
        ),
        "fp_sources": [
            "Researchers/probers creating inboxes: they share no watchlist "
            "IP, so they stay in the run log and never become findings.",
            "A1 semantics caveat: the token-metadata 'ip' field is ASSUMED "
            "to be the creator IP (one-time test-token verification "
            "2026-10-14; two-IP control experiment still outstanding).",
            "Shared egress (NAT/VPN) could put unrelated inboxes behind one "
            "IP — UA consistency and fleet-indicator context corroborate.",
        ],
        "mitigations": [
            "Clusters reported ONLY for watchlist IPs (known_swarm_ips "
            "exact matches, known_swarm_cidrs, watchlist_cidrs).",
            "Cluster graded INFERENCE; per-inbox extraction stays OBSERVED.",
            "Creator UA consistency (python-requests/2.32.5 fleet marker) "
            "feeds the HIGH/MEDIUM call.",
        ],
        "corroboration_for_high": (
            "Watchlist creator IP AND >=2 inboxes, OR consistent fleet UA "
            "across the cluster"
        ),
    },
    "tag-grammar": {
        "description": (
            "New urlquery submissions containing fleet tag grammar "
            "(uqscan=, uqframe=). Feeder for inbox harvesting."
        ),
        "fp_sources": [
            "Copycat researchers tagging submissions similarly.",
        ],
        "mitigations": [
            "Bare 'uq=' excluded (too generic).",
            "Used as inbox harvester, not standalone finding.",
        ],
    },
    "amap-targeting": {
        "description": (
            "New urlquery submissions with Amap URLs + fleet tradecraft. "
            "Feeder for inbox harvesting."
        ),
        "fp_sources": [
            "Legitimate researchers scanning Amap.",
            "Normal urlquery submissions of Amap URLs.",
        ],
        "mitigations": [
            "Require >=2 fleet markers (not just Amap URL).",
            "Used as inbox harvester, not standalone finding.",
        ],
    },
}


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def load_state():
    default = {
        "last_run_utc": None,
        "seen_report_ids": [],
        "seen_inbox_uuids": [],
        "processed_creators": {},  # uuid -> {ip, tier, factum_record_id}
        "pivot_seen_uuids": [],  # uuids already extracted in pivot mode
        "pivot_clusters": {},  # creator ip -> {inboxes, updated_utc}
        "run_count": 0,
    }
    if not os.path.exists(STATE_PATH):
        return default
    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
        for k, v in default.items():
            if k not in state:
                state[k] = v
        return state
    except (json.JSONDecodeError, OSError):
        return default


# ---------------------------------------------------------------------------
# STANDING RULE (BigSexyWarlock69): Every IP stored anywhere — factum records,
# state files, run logs — MUST be classified for cloud/known-host status.
# ALWAYS use ip_record() to build an IP field. NEVER store a bare IP string
# without its classification tier. Cloud/known-host is a priority indicator.
# ---------------------------------------------------------------------------
def ip_record(ip, config, role):
    """
    Build a standardized classified IP record.

    This is the ONLY sanctioned way to store an IP in crawler output.
    Every IP field in every factum record, state entry, and log line
    must be an ip_record() dict, never a bare string.

    Args:
        ip: the IP address string (v4 or v6)
        config: crawler config dict (known_swarm_ips, cloud_asns, etc.)
        role: semantic role of this IP — "creator", "poster", "source", etc.

    Returns:
        {
            "ip": str,
            "role": str,
            "tier": int (1-4),
            "tier_label": str (KNOWN_SWARM/CLOUD_SERVICE/RESIDENTIAL_VPN_HOSTING/UNKNOWN),
            "tier_detail": str (why this classification),
            "asn": str|None,
            "org": str|None,
            "country": str|None,
            "city": str|None,
            "swarm_linked": bool,
        }
    """
    c = classify_ip(ip, config, ASN_CACHE_PATH)
    return {
        "ip": ip,
        "role": role,
        "tier": c["tier"],
        "tier_label": c["label"],
        "tier_detail": c["detail"],
        "asn": c["asn"],
        "org": c["org"],
        "country": c["country"],
        "city": c["city"],
        "swarm_linked": c["swarm_linked"],
    }


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.rename(tmp, STATE_PATH)


# ---------------------------------------------------------------------------
# urlquery harvesting (feeder modules)
# ---------------------------------------------------------------------------

def uq_htmx_search(query, limit=24, _failures=None):
    """Search urlquery via htmx endpoint. Returns list of reports.

    Transport failures (non-zero exit, bad JSON) are retried up to 3x
    with backoff, then recorded in _failures so a failed search is never
    silently counted as zero results. 2026-10-15: prior runs masked
    rc=1 chunked-read failures as zeros.
    """
    if _failures is None:
        _failures = SEARCH_FAILURES
    last_err = ""
    for attempt in range(3):
        result = subprocess.run(
            [sys.executable, UQ_HTMX, "search", "--query", query,
             "--limit", str(limit)],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout).get("reports", [])
            except json.JSONDecodeError as e:
                last_err = f"json decode: {e}"
        else:
            last_err = f"rc={result.returncode}: {result.stderr[:200]}"
        time.sleep(8)
    print(f"  [warn] uq_htmx search FAILED after 3 attempts: {query} "
          f"({last_err})", file=sys.stderr)
    _failures.append({"query": query, "error": last_err})
    return []


def extract_inbox_uuids(text):
    """Extract webhook.site inbox UUIDs from text.

    Matches the path form (webhook.site/<uuid>), the token-API form
    (webhook.site/token/<uuid>), and the page forms
    (webhook.site/#<uuid>, webhook.site/#!/<uuid>).
    """
    pattern = (r"webhook\.site/(?:token/|#?!?/?)?"
               r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-"
               r"[a-f0-9]{4}-[a-f0-9]{12})")
    return list(set(re.findall(pattern, text, re.IGNORECASE)))


def module_harvest_inboxes(state, config, since_days=7):
    """
    Harvest webhook.site inbox URLs from urlquery via fleet-indicator
    searches. Returns list of {uuid, source_report, source_url, rule}.
    """
    print("[1/3] Harvesting webhook.site inboxes from urlquery...")
    since = (datetime.datetime.now(datetime.timezone.utc) -
             datetime.timedelta(days=since_days)).strftime("%Y-%m-%d")
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    date_filter = f"date:[{since} TO {today}]"

    searches = []
    # Tag grammar searches (feeder)
    for tag in config["tag_patterns"]:
        # 2026-10-17: urlquery redesigned the site; bare tag text no longer
        # matches tag values. Fleet tags are exact tokens like uqscan=<val>,
        # so pivot via the tags: field with a wildcard for the value suffix.
        searches.append((f"tags:{tag}* {date_filter}", "tag-grammar"))
    # Amap targeting searches (feeder)
    for domain in config["amap_domains"]:
        searches.append(
            (f"url.domain:{domain} {date_filter}", "amap-targeting"))
    # Direct webhook.site search in Amap context
    searches.append(
        (f"webhook.site amap {date_filter}", "amap-targeting"))

    found = {}  # uuid -> {source_report, source_url, rule}
    for query, rule in searches:
        reports = uq_htmx_search(query, limit=24)
        time.sleep(DELAY_UQ)
        for r in reports:
            rid = r.get("report_id", "")
            url = r.get("url", "")
            for uuid in extract_inbox_uuids(url):
                if uuid not in found:
                    found[uuid] = {
                        "uuid": uuid,
                        "source_report": rid,
                        "source_url": url[:500],
                        "rule": rule,
                    }
            # Also check if the report itself IS a webhook.site URL
            # (inbox submitted directly to urlquery)
            if "webhook.site" in url:
                for uuid in extract_inbox_uuids(url):
                    if uuid not in found:
                        found[uuid] = {
                            "uuid": uuid,
                            "source_report": rid,
                            "source_url": url[:500],
                            "rule": "direct-submission",
                        }

    # Filter to new UUIDs only
    new = {u: v for u, v in found.items()
           if u not in state["seen_inbox_uuids"]}
    print(f"  -> {len(searches)} searches, {len(found)} total inboxes, "
          f"{len(new)} new")
    return list(new.values()), len(searches)


# ---------------------------------------------------------------------------
# Creator IP extraction (core module)
# ---------------------------------------------------------------------------

def extract_creator(uuid):
    """
    Extract creator IP and UA from webhook.site token metadata.

    Method (verified 2026-10-14 via test token):
      GET https://webhook.site/token/<uuid>
      Header: Accept: application/json
      Response fields: "ip" (creator IP), "user_agent" (creator UA)

    This is DISTINCT from poster IPs (from /requests endpoint).

    SEMANTICS CAVEAT (adversarial review A1):
      The `ip` field is ASSUMED to be the creator IP based on:
      - Test token created 2026-10-14: field contained our egress IP
      - Open-source webhook.site Token model documents `ip` as
        "IP address of the creator" (second-hand, not pinned)
      - swarmcha.se researchers used this field for their 18-IP attribution
      REQUIRED VALIDATION (not yet done): two-IP control experiment —
      create token from IP-A, read metadata from IP-B, confirm field
      still shows IP-A (not IP-B). If the field follows the VIEWER,
      this entire method is invalid and all records need retraction.
      See ADVERSARIAL-REVIEW.md A1.

    Returns dict with creator_ip, creator_ua, created_at, or error info.
    """
    url = f"https://webhook.site/token/{uuid}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "swarm-infra-crawler/1.0 (research)",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"uuid": uuid, "status": "gone",
                    "http_code": 404,
                    "note": "Inbox not found (404) — deleted or never existed"}
        if e.code == 410:
            return {"uuid": uuid, "status": "gone",
                    "http_code": 410,
                    "note": "Inbox gone (410) — expired by platform"}
        return {"uuid": uuid, "status": "transient_error",
                "http_code": e.code,
                "note": f"HTTP {e.code} — will retry next run"}
    except Exception as e:
        return {"uuid": uuid, "status": "transient_error",
                "note": f"Fetch failed: {e} — will retry next run"}

    # Check for API error response
    if isinstance(data, dict) and data.get("success") is False:
        return {"uuid": uuid, "status": "gone",
                "note": data.get("error", {}).get("message", "not found")}

    creator_ip = data.get("ip")
    creator_ua = data.get("user_agent")
    if not creator_ip:
        return {"uuid": uuid, "status": "no_ip_field",
                "note": "Token metadata lacks 'ip' field",
                "raw_keys": list(data.keys())[:20]}

    return {
        "uuid": uuid,
        "status": "extracted",
        "creator_ip": creator_ip,
        "creator_ua": creator_ua,
        "created_at": data.get("created_at"),
    }


def module_creator_ips(inboxes, state, config):
    """
    Extract creator IPs for new inboxes and classify them.
    Returns list of finding dicts.
    """
    print(f"[2/3] Extracting creator IPs for {len(inboxes)} inboxes...")
    findings = []
    cache = load_cache(ASN_CACHE_PATH)

    for i, inbox in enumerate(inboxes):
        uuid = inbox["uuid"]
        result = extract_creator(uuid)
        time.sleep(DELAY_WEBHOOKSITE)

        if result["status"] != "extracted":
            findings.append({
                "rule": "creator-ip",
                "uuid": uuid,
                "source_report": inbox["source_report"],
                "source_url": inbox["source_url"],
                "status": result["status"],
                "http_code": result.get("http_code"),
                "note": result.get("note", ""),
                "confidence": "N/A",
                "grade": "OBSERVED",
            })
            # Only mark definitively-gone inboxes as seen.
            # Transient failures are NOT marked — they retry next run.
            # (Adversarial review C1: a 429/500 blip must not permanently
            # burn an inbox from the watch.)
            if result["status"] == "gone":
                if uuid not in state["seen_inbox_uuids"]:
                    state["seen_inbox_uuids"].append(uuid)
            continue

        creator_ip = result["creator_ip"]
        # Classify via the sanctioned ip_record() helper (standing rule:
        # every stored IP must carry its classification tier).
        creator = ip_record(creator_ip, config, role="creator")

        # Check for fleet UA marker
        ua = result.get("creator_ua", "")
        has_fleet_ua = "python-requests/2.32.5" in (ua or "")

        # Confidence scoring
        tier = creator["tier"]
        signals = [f"tier-{tier}"]
        if has_fleet_ua:
            signals.append("fleet-ua")
        if tier <= 2:
            confidence = "HIGH" if (tier == 1 or has_fleet_ua) else "MEDIUM"
        elif tier == 3:
            confidence = "LOW"
        else:
            confidence = "LOW"

        findings.append({
            "rule": "creator-ip",
            "uuid": uuid,
            "inbox_url": f"https://webhook.site/#{uuid}",
            "source_report": inbox["source_report"],
            "source_url": inbox["source_url"],
            "harvest_rule": inbox["rule"],
            "status": "extracted",
            "creator_ip": creator,  # Full classified IP record (standing rule)
            "creator_ua": ua,
            "classification_tier": tier,  # Flat copy for backward compat
            "classification_label": creator["tier_label"],
            "classification_detail": creator["tier_detail"],
            "swarm_linked": creator["swarm_linked"],
            "has_fleet_ua": has_fleet_ua,
            "created_at": result.get("created_at"),
            "extracted_at": datetime.datetime.now(
                datetime.timezone.utc).isoformat(),
            "signals": signals,
            "confidence": confidence,
            "grade": "OBSERVED",  # We directly observed the creator IP via API
            "lane": LANE_TAG,
        })

        # Mark as seen
        if uuid not in state["seen_inbox_uuids"]:
            state["seen_inbox_uuids"].append(uuid)
        state["processed_creators"][uuid] = {
            "ip": creator,  # Full classified record (standing rule)
            "extracted_at": findings[-1]["extracted_at"],
        }

        print(f"  [{i+1}/{len(inboxes)}] {uuid[:8]}... "
              f"-> {creator_ip} (tier {tier}: "
              f"{creator['tier_label']})", file=sys.stderr)

    # Cap seen lists
    state["seen_inbox_uuids"] = state["seen_inbox_uuids"][-5000:]
    return findings


# ---------------------------------------------------------------------------
# Creator-IP pivot (discovery mode)
#
# Commissioned 2026-10-15 (BigSexyWarlock69): "The creator ip should scrape
# or search for inboxes." Given a webhook.site creator IP (for example a
# Tencent Cloud IP that created one fleet inbox), find EVERY other inbox
# that IP created — mapping the operator's full infrastructure, not just
# the inboxes the watch happened to harvest.
#
# Method (inversion): inbox UUIDs are unguessable and webhook.site has no
# search-by-creator-IP endpoint, so the pivot enumerates candidate inboxes
# from urlquery's submitted-URL index (broad `webhook.site` search,
# paginated), extracts the creator IP per inbox via the public token-
# metadata endpoint, then inverts the map: creator-IP -> [inboxes].
#
# Reporting rule: clusters are reported ONLY for watchlist IPs (config
# known_swarm_ips exact matches, plus known_swarm_cidrs and
# watchlist_cidrs). All other creator IPs stay in the run log as negative
# evidence — broad extraction is a discovery method, not a dragnet.
#
# Grading: per-inbox extraction is OBSERVED (direct API read). The cluster
# itself — "same creator IP => same operator infrastructure" — is an
# INFERENCE. The A1 semantics caveat from extract_creator applies
# unchanged: the token-metadata `ip` field is ASSUMED to be the creator IP
# (one-time test-token verification 2026-10-14; two-IP control experiment
# still outstanding). If A1 falls, pivot clusters fall with it.
#
# Passive only: GET requests to public APIs. No POSTs.
# ---------------------------------------------------------------------------

PIVOT_PAGE_SIZE = 48
PIVOT_MAX_PAGES = 8
PIVOT_MAX_INBOXES = 400  # per-run extraction cap (politeness bound)


def ip_on_watchlist(ip, config):
    """True if ip is an exact known-swarm IP or inside a watchlist CIDR."""
    if ip in config.get("known_swarm_ips", []):
        return True
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for cidr in (config.get("known_swarm_cidrs", [])
                 + config.get("watchlist_cidrs", [])):
        try:
            if addr in ipaddress.ip_network(cidr, strict=False):
                return True
        except ValueError:
            continue
    return False


def module_pivot_harvest(state, config, since_days=90):
    """
    Broad harvest of webhook.site inbox URLs from urlquery's
    submitted-URL index. Paginated; dedups against pivot_seen_uuids.
    Returns (list of {uuid, source_report, source_url, rule}, pages).
    """
    print("[pivot] Harvesting webhook.site inboxes (broad, paginated)...")
    since = (datetime.datetime.now(datetime.timezone.utc) -
             datetime.timedelta(days=since_days)).strftime("%Y-%m-%d")
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    query = f"webhook.site date:[{since} TO {today}]"

    found = {}
    pages = 0
    for page in range(PIVOT_MAX_PAGES):
        offset = page * PIVOT_PAGE_SIZE
        result = subprocess.run(
            [sys.executable, UQ_HTMX, "search", "--query", query,
             "--limit", str(PIVOT_PAGE_SIZE), "--offset", str(offset)],
            capture_output=True, text=True, timeout=300,
        )
        pages += 1
        if result.returncode != 0:
            print(f"  [warn] uq_htmx page {page} failed: "
                  f"{result.stderr[:200]}", file=sys.stderr)
            break
        try:
            reports = json.loads(result.stdout).get("reports", [])
        except json.JSONDecodeError:
            print(f"  [warn] uq_htmx page {page}: bad JSON",
                  file=sys.stderr)
            break
        if not reports:
            break
        for r in reports:
            url = r.get("url", "")
            for uuid in extract_inbox_uuids(url):
                if uuid not in found:
                    found[uuid] = {
                        "uuid": uuid,
                        "source_report": r.get("report_id", ""),
                        "source_url": url[:500],
                        "rule": "pivot-broad",
                    }
        time.sleep(DELAY_UQ)
        if len(reports) < PIVOT_PAGE_SIZE:
            break

    new = {u: v for u, v in found.items()
           if u not in state["pivot_seen_uuids"]}
    print(f"  -> {pages} pages, {len(found)} total inboxes, "
          f"{len(new)} new (pivot)")
    return list(new.values()), pages


def module_creator_pivot(state, config, since_days=90):
    """
    Creator-IP pivot: harvest inboxes broadly, extract creator IPs,
    invert to creator-IP -> inboxes, report watchlist-IP clusters.
    Returns (findings, pivot_map, summary).
    pivot_map: {ip: {classified, watchlist, inbox_count, inbox_uuids,
    creator_uas}} — the full inversion, kept in the run log as evidence
    (non-watchlist IPs included = negative evidence).
    """
    print("[pivot] Running creator-IP pivot...")
    inboxes, pages = module_pivot_harvest(state, config,
                                          since_days=since_days)
    inboxes = inboxes[:PIVOT_MAX_INBOXES]

    by_ip = {}  # ip -> {inboxes: [...], uas: set, created: [...]}
    extracted = 0
    gone = 0
    for i, inbox in enumerate(inboxes):
        uuid = inbox["uuid"]
        result = extract_creator(uuid)
        time.sleep(DELAY_WEBHOOKSITE)
        if uuid not in state["pivot_seen_uuids"]:
            state["pivot_seen_uuids"].append(uuid)
        if result["status"] == "gone":
            gone += 1
            continue
        if result["status"] != "extracted":
            continue
        extracted += 1
        ip = result["creator_ip"]
        entry = by_ip.setdefault(ip, {"inboxes": [], "uas": set(),
                                      "created": []})
        entry["inboxes"].append({
            "uuid": uuid,
            "source_report": inbox["source_report"],
            "source_url": inbox["source_url"],
        })
        if result.get("creator_ua"):
            entry["uas"].add(result["creator_ua"])
        if result.get("created_at"):
            entry["created"].append(result["created_at"])
        print(f"  [pivot {i+1}/{len(inboxes)}] {uuid[:8]}... -> {ip}",
              file=sys.stderr)
    state["pivot_seen_uuids"] = state["pivot_seen_uuids"][-20000:]

    # Report only watchlist-IP clusters; diff against known clusters so
    # repeat runs emit findings only for NEW inboxes in a cluster.
    findings = []
    run_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clusters = state.setdefault("pivot_clusters", {})
    for ip, entry in sorted(by_ip.items()):
        if not ip_on_watchlist(ip, config):
            continue
        prior = clusters.get(ip, {}).get("inboxes", [])
        new_uuids = [b["uuid"] for b in entry["inboxes"]
                     if b["uuid"] not in prior]
        merged = list(dict.fromkeys(
            prior + [b["uuid"] for b in entry["inboxes"]]))
        clusters[ip] = {"inboxes": merged, "updated_utc": run_utc}
        if not new_uuids:
            continue
        creator = ip_record(ip, config, role="creator")
        uas = sorted(entry["uas"])
        created = sorted(entry["created"])
        has_fleet_ua = any("python-requests/2.32.5" in u for u in uas)
        tier = creator["tier"]
        confidence = ("HIGH" if (tier == 1 or len(new_uuids) >= 2
                                 or has_fleet_ua) else "MEDIUM")
        findings.append({
            "rule": "creator-pivot",
            "creator_ip": creator,
            "inbox_uuids": new_uuids,
            "inbox_count_new": len(new_uuids),
            "inbox_count_total": len(merged),
            "inbox_urls": [f"https://webhook.site/#{u}"
                           for u in new_uuids],
            "creator_uas": uas,
            "created_at_range": ([created[0], created[-1]]
                                 if created else []),
            "source_inboxes": [
                {"uuid": b["uuid"], "source_report": b["source_report"],
                 "source_url": b["source_url"]}
                for b in entry["inboxes"] if b["uuid"] in new_uuids],
            "has_fleet_ua": has_fleet_ua,
            "watchlist_match": ("known_swarm_ip"
                                if ip in config.get("known_swarm_ips", [])
                                else "watchlist_cidr"),
            "confidence": confidence,
            "grade": "INFERENCE",
            "lane": LANE_TAG,
            "extracted_at": run_utc,
            "pivot_note": (
                "Cluster = same creator IP across inboxes => same operator "
                "infrastructure (inference). Per-inbox extraction is a "
                "direct token-metadata read (observed); A1 semantics "
                "caveat applies."
            ),
        })
        print(f"  [pivot] CLUSTER {ip} (tier {tier}): "
              f"{len(new_uuids)} new / {len(merged)} total inboxes",
              file=sys.stderr)

    # Serialize the full inversion for the run log (sets -> lists).
    # Standing rule: IPs ride as ip_record() dicts, never bare strings.
    pivot_map = {}
    for ip, entry in by_ip.items():
        pivot_map[ip] = {
            "classified": ip_record(ip, config, role="creator"),
            "watchlist": ip_on_watchlist(ip, config),
            "inbox_count": len(entry["inboxes"]),
            "inbox_uuids": [b["uuid"] for b in entry["inboxes"]],
            "creator_uas": sorted(entry["uas"]),
        }

    summary = {
        "pages": pages,
        "inboxes_harvested": len(inboxes),
        "extracted": extracted,
        "gone": gone,
        "distinct_creator_ips": len(by_ip),
        "watchlist_clusters_reported": len(findings),
    }
    print(f"[pivot] {extracted} extracted / {len(by_ip)} distinct "
          f"creator IPs / {len(findings)} watchlist clusters")
    return findings, pivot_map, summary


# ---------------------------------------------------------------------------
# Factum output
# ---------------------------------------------------------------------------

def build_factum_records(findings, run_id=None):
    """
    Build a factum bundle v2 from creator-IP findings.

    Bundle v2 shape (matches orchestrator._build_factum_bundle and the
    factum skill's bundle.json example):
        {
            "bundle": 2,
            "idempotency_key": ...,
            "actor": ...,
            "tags": {...},
            "records": [
                {"ref": ..., "kind": "source"|"observation"|"observable",
                 "body": {...}},
            ],
        }

    Only MEDIUM+ confidence creator-IP extractions become records.
    LOW findings stay in the run log for analyst review.

    NOTE (2026-10-14 fix): the previous version emitted a custom
    {"type": "observation", "lane": ..., "grade": ...} shape that factum
    does not accept. There is no separate "lane-ingest worker" — the
    bundle must be directly submittable via `factum add --input`.

    NOTE (2026-10-14 fix 2): the observation used
    "type": "network.infra", which is not a registered observation type
    (factum add raises "Unknown observation type"). Observations are now
    infra.ioc term records (term=creator IP, category="ip",
    status="candidate"); the full classified extraction stays in the run
    log JSON and the tier rides on the observable's tags.
    """
    if run_id is None:
        run_id = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y%m%dT%H%M%SZ")
    records = []
    n = 0
    for f in findings:
        if f.get("rule") != "creator-ip":
            continue
        if f.get("status") != "extracted":
            continue
        if f.get("confidence") not in ("HIGH", "MEDIUM"):
            continue
        # creator_ip is a full classified ip_record() dict (standing rule:
        # every stored IP carries its classification tier).
        cip = f["creator_ip"]
        sref, oref = f"swc-source-{n}", f"swc-obs-{n}"
        # Source: the webhook.site inbox
        records.append({
            "ref": sref,
            "kind": "source",
            "body": {
                "source_type": "scanner",
                "locator": f"webhook.site inbox {f['uuid']}",
                "title": (
                    f"webhook.site inbox creator-IP extraction "
                    f"({f['uuid'][:8]}…)"
                ),
            },
            "tags": {
                "lane": LANE_TAG,
                "scanner": True,
            },
        })
        # Observation: the creator-IP extraction, as an infra.ioc term
        # record. ("network.infra" is not a registered observation type --
        # factum add rejects the whole bundle. Fixed 2026-10-14.) The full
        # classified extraction (UA, signals, harvest rule, tier detail)
        # stays in the run log JSON; the IOC record carries the term and a
        # classification summary in provenance. Tier also rides on the
        # observable's tags (standing rule: no bare IPs).
        data = {
            "term": cip["ip"],
            "category": "ip",
            "provenance": (
                f"swarm-infra-crawler creator-IP extraction (PRIMARY): "
                f"GET webhook.site/token/{f['uuid']} "
                f"Accept: application/json, 'ip' field of token metadata "
                f"(extraction method verified 2026-10-14 via test token; "
                f"creator IP, not poster IP). "
                f"Tier {cip['tier']} ({cip['tier_label']}); "
                f"creator UA {f['creator_ua']}; "
                f"harvest rule {f['harvest_rule']}; "
                f"signals {','.join(str(s) for s in f['signals'])}; "
                f"swarm_linked={f['swarm_linked']}; "
                f"has_fleet_ua={f['has_fleet_ua']}."
            ),
            "status": "candidate",
        }
        records.append({
            "ref": oref,
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "source": f"@{sref}",
                "observed_at": f["extracted_at"],
                "data": data,
            },
            "tags": {
                "lane": LANE_TAG,
                "scanner": True,
                "grade": "PRIMARY",
                "tier": cip["tier"],
                "tier_label": cip["tier_label"],
            },
        })
        # Observable: inbox URL
        records.append({
            "ref": f"swc-url-{n}",
            "kind": "observable",
            "body": {"type": "url", "value": f["inbox_url"]},
        })
        # Observable: creator IP
        ip = cip["ip"]
        records.append({
            "ref": f"swc-ip-{n}",
            "kind": "observable",
            "body": {
                "type": "ipv4" if "." in ip else "ipv6",
                "value": ip,
            },
            "tags": {
                "tier": cip["tier"],
                "tier_label": cip["tier_label"],
                "asn": cip.get("asn"),
            },
        })
        n += 1

    # Pivot clusters: one observation per watchlist-IP cluster. The
    # cluster ("same creator IP => same operator infrastructure") is
    # graded INFERENCE; the per-inbox extraction it rests on is OBSERVED.
    for f in findings:
        if f.get("rule") != "creator-pivot":
            continue
        if f.get("confidence") not in ("HIGH", "MEDIUM"):
            continue
        cip = f["creator_ip"]
        sref, oref = f"swp-source-{n}", f"swp-obs-{n}"
        uuid_list = ", ".join(f["inbox_uuids"][:20])
        if f["inbox_count_new"] > 20:
            uuid_list += f", ... (+{f['inbox_count_new'] - 20} more)"
        records.append({
            "ref": sref,
            "kind": "source",
            "body": {
                "source_type": "scanner",
                "locator": ("webhook.site creator-IP pivot cluster: "
                            f"{cip['ip']}"),
                "title": (f"creator-IP pivot cluster {cip['ip']}: "
                          f"{f['inbox_count_new']} new / "
                          f"{f['inbox_count_total']} total inboxes"),
            },
            "tags": {
                "lane": LANE_TAG,
                "scanner": True,
            },
        })
        data = {
            "term": cip["ip"],
            "category": "ip",
            "provenance": (
                f"swarm-infra-crawler creator-IP pivot (INFERENCE): broad "
                f"urlquery 'webhook.site' submitted-URL harvest + GET "
                f"webhook.site/token/<uuid> per inbox; 'ip' field identical "
                f"across {f['inbox_count_new']} new / "
                f"{f['inbox_count_total']} total inboxes (UUIDs: "
                f"{uuid_list}). Creator UA set: "
                f"{'; '.join(f['creator_uas']) or 'none'}. created_at "
                f"range: {'..'.join(f['created_at_range']) or 'unknown'}. "
                f"Watchlist match: {f['watchlist_match']}; tier "
                f"{cip['tier']} ({cip['tier_label']}); "
                f"has_fleet_ua={f['has_fleet_ua']}. Cluster = same creator "
                f"IP => same operator infrastructure (inference; per-inbox "
                f"extraction observed). A1 semantics caveat: 'ip' field "
                f"assumed creator IP (one-time test-token verification "
                f"2026-10-14; two-IP control outstanding)."
            ),
            "status": "candidate",
        }
        records.append({
            "ref": oref,
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "source": f"@{sref}",
                "observed_at": f["extracted_at"],
                "data": data,
            },
            "tags": {
                "lane": LANE_TAG,
                "scanner": True,
                "grade": "INFERENCE",
                "tier": cip["tier"],
                "tier_label": cip["tier_label"],
            },
        })
        ip = cip["ip"]
        records.append({
            "ref": f"swp-ip-{n}",
            "kind": "observable",
            "body": {
                "type": "ipv4" if "." in ip else "ipv6",
                "value": ip,
            },
            "tags": {
                "lane": LANE_TAG,
                "tier": cip["tier"],
                "tier_label": cip["tier_label"],
                "asn": cip.get("asn"),
            },
        })
        # Inbox URL observables (capped; full UUID list rides in
        # provenance). tags.lane on every record (lane-edit rule).
        for m, inbox_url in enumerate(f["inbox_urls"][:10]):
            records.append({
                "ref": f"swp-url-{n}-{m}",
                "kind": "observable",
                "body": {"type": "url", "value": inbox_url},
                "tags": {"lane": LANE_TAG, "scanner": True},
            })
        n += 1
    return {
        "bundle": 2,
        "idempotency_key": f"swarm-infra-crawler/{run_id}",
        "actor": "agent:swarm-infra-crawler",
        "tags": {"swarm_infra_crawler": True, "run_id": run_id,
                 "lane": LANE_TAG},
        "records": records,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(dry_run=False, since_days=7, modules=None, pivot_days=90):
    config = load_config()
    state = load_state()
    run_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"Swarm infra crawler v2 run at {run_utc}")
    print(f"State: {state['run_count']} prior runs, "
          f"{len(state['seen_inbox_uuids'])} seen inboxes, "
          f"{len(state['pivot_seen_uuids'])} pivot-seen inboxes")

    if modules is None:
        modules = ["harvest", "creator"]

    all_findings = []

    # Module 1: Harvest inboxes
    search_count = 0
    if "harvest" in modules:
        inboxes, search_count = module_harvest_inboxes(
            state, config, since_days=since_days)
    else:
        inboxes = []

    # Module 2: Extract creator IPs
    if "creator" in modules and inboxes:
        findings = module_creator_ips(inboxes, state, config)
        all_findings.extend(findings)
    elif "creator" in modules:
        print("[2/3] No new inboxes to process.")

    # Module 3: Creator-IP pivot (discovery mode)
    pivot_map = {}
    pivot_summary = {}
    if "creator-pivot" in modules:
        pivot_findings, pivot_map, pivot_summary = module_creator_pivot(
            state, config, since_days=pivot_days)
        all_findings.extend(pivot_findings)

    # Module 3: Build factum bundle (bundle v2, directly submittable
    # via `factum add --input`)
    print("[3/3] Building factum bundle...")
    run_id = run_utc.replace(":", "").replace("-", "")[:15]
    factum_bundle = build_factum_records(all_findings, run_id=run_id)
    n_bundle_records = len(factum_bundle["records"])

    # Summary with denominator logging (adversarial review C2:
    # "fleet leaving webhook.site looks identical to fleet dormant" —
    # log denominators so silent runs are interpretable)
    extracted = [f for f in all_findings
                 if f.get("status") == "extracted"]
    tier1 = [f for f in extracted
             if f.get("classification_tier") == 1]
    tier2 = [f for f in extracted
             if f.get("classification_tier") == 2]
    gone = [f for f in all_findings if f.get("status") == "gone"]
    transient = [f for f in all_findings
                 if f.get("status") == "transient_error"]
    pivot_clusters = [f for f in all_findings
                      if f.get("rule") == "creator-pivot"]

    print(f"\nResults (denominators logged for silent-run interpretation):")
    print(f"  urlquery searches run: {search_count}")
    print(f"  Inboxes harvested: {len(inboxes)} "
          f"({len(state['seen_inbox_uuids'])} total seen)")
    print(f"  Creator IPs extracted: {len(extracted)}")
    print(f"    Tier 1 (KNOWN_SWARM): {len(tier1)}")
    print(f"    Tier 2 (CLOUD_SERVICE): {len(tier2)}")
    print(f"  Inboxes gone (404/410): {len(gone)}")
    print(f"  Transient failures (will retry): {len(transient)}")
    if "creator-pivot" in modules:
        print(f"  Pivot: {pivot_summary.get('inboxes_harvested', 0)} "
              f"inboxes / {pivot_summary.get('extracted', 0)} extracted / "
              f"{pivot_summary.get('distinct_creator_ips', 0)} distinct "
              f"creator IPs / {len(pivot_clusters)} watchlist clusters")
    print(f"  Factum bundle records (MEDIUM+): {n_bundle_records}")
    if not inboxes and not extracted:
        if SEARCH_FAILURES:
            print(f"  WARNING: {len(SEARCH_FAILURES)} urlquery searches "
                  f"failed on transport after retries -- a zero-inbox "
                  f"conclusion is NOT reliable for those searches. "
                  f"Failed: {[f['query'] for f in SEARCH_FAILURES]}")
        else:
            print(f"  NOTE: Zero new inboxes. This is expected if the fleet "
                  f"is dormant OR has moved off webhook.site. "
                  f"Distinguish via urlquery tag-grammar hits.")

    # Write output
    if not dry_run:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, f"crawl-{run_id}.json")
        bundle_path = os.path.join(OUTPUT_DIR, f"crawl-{run_id}.bundle.json")
        output = {
            "run_utc": run_utc,
            "crawler_version": "2.2",
            "modules": modules,
            "findings": all_findings,
            "pivot_map": pivot_map,
            "pivot_summary": pivot_summary,
            "factum_bundle": factum_bundle,
            "summary": {
                "urlquery_searches": search_count,
                "inboxes_harvested": len(inboxes),
                "total_seen_inboxes": len(state["seen_inbox_uuids"]),
                "extracted": len(extracted),
                "tier1": len(tier1),
                "tier2": len(tier2),
                "gone": len(gone),
                "transient_failures": len(transient),
                "urlquery_search_failures": len(SEARCH_FAILURES),
                "urlquery_failed_queries": [f["query"]
                                            for f in SEARCH_FAILURES],
                "pivot_inboxes_harvested":
                    pivot_summary.get("inboxes_harvested", 0),
                "pivot_distinct_creator_ips":
                    pivot_summary.get("distinct_creator_ips", 0),
                "pivot_watchlist_clusters": len(pivot_clusters),
                "factum_bundle_records": n_bundle_records,
            },
        }
        tmp = out_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(output, f, indent=1)
        os.rename(tmp, out_path)
        # Standalone bundle file for `factum add --input`
        btmp = bundle_path + ".tmp"
        with open(btmp, "w") as f:
            json.dump(factum_bundle, f, indent=1)
        os.rename(btmp, bundle_path)
        print(f"Output: {out_path}")
        print(f"Factum bundle: {bundle_path} "
              f"(submit via: factum add --input {bundle_path})")

        state["last_run_utc"] = run_utc
        state["run_count"] += 1
        save_state(state)
    else:
        print("[dry-run] No state changes.")

    return all_findings, factum_bundle


def main():
    parser = argparse.ArgumentParser(
        description="Swarm infra crawler v2 (webhook.site creator-IP)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--module",
                        choices=["harvest", "creator", "creator-pivot"],
                        action="append", dest="modules")
    parser.add_argument("--since-days", type=int, default=7)
    parser.add_argument("--pivot-days", type=int, default=90,
                        help="urlquery window (days) for creator-pivot "
                             "broad harvest")
    args = parser.parse_args()
    run(dry_run=args.dry_run, since_days=args.since_days,
        modules=args.modules, pivot_days=args.pivot_days)


if __name__ == "__main__":
    main()
