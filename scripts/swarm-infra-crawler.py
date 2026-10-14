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
  5. Write factum-ready JSONL for the lane-ingest worker

Passive only: GET requests to public APIs. No POSTs (except the one-time
API structure verification, documented separately). No intrusive scanning.

Usage:
  swarm-infra-crawler.py [--dry-run] [--module MODULE] [--since-days N]

State:
  ~/workspace/goals/urlquery-agent-activity-hunt/hidden_files/swarm-infra-crawler-state.json

Output:
  ~/workspace/silent-locus/data/lanes/swarm-infra-watch/crawl-<timestamp>.json
  (factum-ready; the lane-ingest worker handles submission)
"""

import argparse
import datetime
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

def uq_htmx_search(query, limit=24):
    """Search urlquery via htmx endpoint. Returns list of reports."""
    result = subprocess.run(
        [sys.executable, UQ_HTMX, "search", "--query", query,
         "--limit", str(limit)],
        capture_output=True, text=True, timeout=300,
    )
    if result.returncode != 0:
        print(f"  [warn] uq_htmx failed: {result.stderr[:200]}",
              file=sys.stderr)
        return []
    try:
        return json.loads(result.stdout).get("reports", [])
    except json.JSONDecodeError:
        return []


def extract_inbox_uuids(text):
    """Extract webhook.site inbox UUIDs from text."""
    pattern = (r"webhook\.site/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-"
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
        searches.append((f"{tag} {date_filter}", "tag-grammar"))
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
# Factum output
# ---------------------------------------------------------------------------

def build_factum_records(findings):
    """
    Build factum-ready records from findings.
    Only MEDIUM+ confidence creator-IP extractions become records.
    LOW findings stay in the run log for analyst review.
    """
    records = []
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
        records.append({
            "type": "observation",
            "lane": LANE_TAG,
            "grade": "OBSERVED",
            "observed_at": f["extracted_at"],
            "summary": (
                f"webhook.site inbox creator IP: {cip['ip']} "
                f"({cip['tier_label']})"
            ),
            "data": {
                "inbox_uuid": f["uuid"],
                "inbox_url": f["inbox_url"],
                # Classified IP record — tier always present (standing rule)
                "creator_ip": cip,
                # Flat copies for query convenience (backward compat)
                "creator_ip_str": cip["ip"],
                "creator_ip_tier": cip["tier"],
                "creator_ip_tier_label": cip["tier_label"],
                "creator_ua": f["creator_ua"],
                "classification_tier": f["classification_tier"],
                "classification_label": f["classification_label"],
                "classification_detail": f["classification_detail"],
                "swarm_linked": f["swarm_linked"],
                "has_fleet_ua": f["has_fleet_ua"],
                "inbox_created_at": f.get("created_at"),
                "source_report": f["source_report"],
                "source_url": f["source_url"],
                "harvest_rule": f["harvest_rule"],
                "signals": f["signals"],
                "confidence": f["confidence"],
            },
            "provenance": {
                "method": (
                    "GET https://webhook.site/token/<uuid> with "
                    "Accept: application/json; 'ip' field from token metadata"
                ),
                "extraction_verified": "2026-10-14 via test token",
                "creator_vs_poster": (
                    "Creator IP (token metadata 'ip' field), NOT poster IPs "
                    "(/requests endpoint per-request source IPs)"
                ),
            },
        })
    return records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(dry_run=False, since_days=7, modules=None):
    config = load_config()
    state = load_state()
    run_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"Swarm infra crawler v2 run at {run_utc}")
    print(f"State: {state['run_count']} prior runs, "
          f"{len(state['seen_inbox_uuids'])} seen inboxes")

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

    # Module 3: Build factum records
    print("[3/3] Building factum records...")
    factum_records = build_factum_records(all_findings)

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

    print(f"\nResults (denominators logged for silent-run interpretation):")
    print(f"  urlquery searches run: {search_count}")
    print(f"  Inboxes harvested: {len(inboxes)} "
          f"({len(state['seen_inbox_uuids'])} total seen)")
    print(f"  Creator IPs extracted: {len(extracted)}")
    print(f"    Tier 1 (KNOWN_SWARM): {len(tier1)}")
    print(f"    Tier 2 (CLOUD_SERVICE): {len(tier2)}")
    print(f"  Inboxes gone (404/410): {len(gone)}")
    print(f"  Transient failures (will retry): {len(transient)}")
    print(f"  Factum records (MEDIUM+): {len(factum_records)}")
    if not inboxes and not extracted:
        print(f"  NOTE: Zero new inboxes. This is expected if the fleet "
              f"is dormant OR has moved off webhook.site. "
              f"Distinguish via urlquery tag-grammar hits.")

    # Write output
    if not dry_run:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        run_id = run_utc.replace(":", "").replace("-", "")[:15]
        out_path = os.path.join(OUTPUT_DIR, f"crawl-{run_id}.json")
        output = {
            "run_utc": run_utc,
            "crawler_version": "2.0",
            "findings": all_findings,
            "factum_records": factum_records,
            "summary": {
                "urlquery_searches": search_count,
                "inboxes_harvested": len(inboxes),
                "total_seen_inboxes": len(state["seen_inbox_uuids"]),
                "extracted": len(extracted),
                "tier1": len(tier1),
                "tier2": len(tier2),
                "gone": len(gone),
                "transient_failures": len(transient),
                "factum_records": len(factum_records),
            },
        }
        tmp = out_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(output, f, indent=1)
        os.rename(tmp, out_path)
        print(f"Output: {out_path}")

        state["last_run_utc"] = run_utc
        state["run_count"] += 1
        save_state(state)
    else:
        print("[dry-run] No state changes.")

    return all_findings, factum_records


def main():
    parser = argparse.ArgumentParser(
        description="Swarm infra crawler v2 (webhook.site creator-IP)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--module", choices=["harvest", "creator"],
                        action="append", dest="modules")
    parser.add_argument("--since-days", type=int, default=7)
    args = parser.parse_args()
    run(dry_run=args.dry_run, since_days=args.since_days,
        modules=args.modules)


if __name__ == "__main__":
    main()
