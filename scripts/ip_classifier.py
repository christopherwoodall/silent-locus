#!/usr/bin/env python3
"""
IP classification module for swarm infrastructure monitoring.

Tiers:
  1. KNOWN_SWARM — matches known fleet IPs or CIDRs (highest signal)
  2. CLOUD_SERVICE — ASN belongs to a cloud provider (flag which cloud)
  3. RESIDENTIAL_VPN_HOSTING — ISP ranges, VPN providers, bulletproof hosting
  4. UNKNOWN — couldn't classify

ASN lookups use ipinfo.io with a persistent local cache to avoid
hammering the API. Cache lives alongside the crawler state.

Usage:
    from ip_classifier import classify_ip
    result = classify_ip("43.162.198.97", config, cache_path)
    # -> {"tier": 1, "label": "KNOWN_SWARM", "detail": "exact IP match", ...}
"""

import ipaddress
import json
import os
import time
import urllib.request


def load_cache(cache_path):
    """Load ASN cache. Returns {} if missing/corrupt."""
    if os.path.exists(cache_path):
        try:
            with open(cache_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_cache(cache, cache_path):
    """Write ASN cache atomically."""
    tmp = cache_path + ".tmp"
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(tmp, "w") as f:
        json.dump(cache, f, indent=1)
    os.rename(tmp, cache_path)


def asn_lookup(ip, cache, cache_path):
    """
    Look up ASN/org/country for an IP via ipinfo.io.
    Uses cache; only hits API on miss. Returns dict or None.
    Rate: 1 req per miss, 1s delay between API calls.
    """
    if ip in cache:
        return cache[ip]
    url = f"https://ipinfo.io/{ip}/json"
    req = urllib.request.Request(url, headers={
        "User-Agent": "swarm-infra-crawler/1.0 (research)",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
        result = {
            "asn": None,
            "org": data.get("org", ""),
            "country": data.get("country", ""),
            "city": data.get("city", ""),
            "region": data.get("region", ""),
        }
        # ipinfo org format: "AS7922 Comcast Cable Communications, LLC"
        org = result["org"]
        if org.startswith("AS"):
            parts = org.split(" ", 1)
            result["asn"] = parts[0]
            result["org_name"] = parts[1] if len(parts) > 1 else ""
        else:
            result["org_name"] = org
        cache[ip] = result
        save_cache(cache, cache_path)
        time.sleep(1)  # Polite delay between API calls
        return result
    except Exception:
        return None


def ip_in_cidrs(ip, cidrs):
    """Check if IP is within any of the given CIDR ranges."""
    try:
        addr = ipaddress.ip_address(ip)
        for cidr in cidrs:
            try:
                if addr in ipaddress.ip_network(cidr, strict=False):
                    return cidr
            except ValueError:
                continue
    except ValueError:
        pass
    return None


def classify_ip(ip, config, cache_path):
    """
    Classify an IP into tiers 1-4.

    Returns:
        {
            "tier": int (1-4),
            "label": str,
            "detail": str (why this classification),
            "asn": str or None,
            "org": str or None,
            "country": str or None,
            "city": str or None,
            "swarm_linked": bool (for cloud tier: is this ASN swarm-linked?),
        }
    """
    result = {
        "ip": ip,
        "tier": 4,
        "label": "UNKNOWN",
        "detail": "Could not classify",
        "asn": None,
        "org": None,
        "country": None,
        "city": None,
        "swarm_linked": False,
    }

    # --- Tier 1: Known swarm infrastructure ---
    if ip in config.get("known_swarm_ips", []):
        result.update({
            "tier": 1, "label": "KNOWN_SWARM",
            "detail": "Exact match against published fleet IP list",
            "swarm_linked": True,
        })
        return result

    matched_cidr = ip_in_cidrs(ip, config.get("known_swarm_cidrs", []))
    if matched_cidr:
        result.update({
            "tier": 1, "label": "KNOWN_SWARM",
            "detail": f"Within known swarm CIDR {matched_cidr}",
            "swarm_linked": True,
        })
        return result

    # --- Tier 1b: Watchlist CIDR (demoted from tier 1 per adversarial B1) ---
    # 43.162.0.0/16 is 65k addresses; "~half fleet inferred" is not enough
    # for KNOWN_SWARM. These get tier 2 with a watchlist note.
    watchlist_cidr = ip_in_cidrs(ip, config.get("watchlist_cidrs", []))
    watchlist_hit = bool(watchlist_cidr)

    # --- ASN lookup for tiers 2-3 ---
    cache = load_cache(cache_path)
    info = asn_lookup(ip, cache, cache_path)
    if info:
        result["asn"] = info.get("asn")
        result["org"] = info.get("org_name") or info.get("org")
        result["country"] = info.get("country")
        result["city"] = info.get("city")

    asn = result["asn"]
    cloud_asns = config.get("cloud_asns", {})
    residential_asns = config.get("residential_asns", {})

    # --- Tier 2: Cloud service ---
    if asn and asn in cloud_asns:
        cloud_info = cloud_asns[asn]
        detail = f"{cloud_info['provider']} ({cloud_info['region']})"
        if watchlist_hit:
            detail += f"; within watchlist CIDR {watchlist_cidr}"
        result.update({
            "tier": 2, "label": "CLOUD_SERVICE",
            "detail": detail,
            "swarm_linked": cloud_info.get("swarm_linked", False),
        })
        return result

    # Watchlist CIDR without cloud ASN match — still tier 2, lower confidence
    if watchlist_hit:
        result.update({
            "tier": 2, "label": "CLOUD_SERVICE",
            "detail": (f"Within watchlist CIDR {watchlist_cidr} "
                       f"(demoted from tier 1 per adversarial review)"),
            "swarm_linked": False,
        })
        return result

    # --- Tier 3: Residential / VPN / Hosting ---
    if asn and asn in residential_asns:
        res_info = residential_asns[asn]
        result.update({
            "tier": 3, "label": "RESIDENTIAL_VPN_HOSTING",
            "detail": f"{res_info['provider']} ({res_info['type']})",
        })
        return result

    # Heuristic tier 3: org name patterns for hosting/VPN
    org_lower = (result["org"] or "").lower()
    hosting_keywords = [
        "hosting", "vps", "dedicated", "datacenter", "colo",
        "vpn", "proxy", "m247", "datacamp", "cdn77",
    ]
    if any(kw in org_lower for kw in hosting_keywords):
        result.update({
            "tier": 3, "label": "RESIDENTIAL_VPN_HOSTING",
            "detail": f"Hosting/VPN keyword in org: {result['org']}",
        })
        return result

    isp_keywords = [
        "comcast", "charter", "spectrum", "verizon", "at&t",
        "telekomunikasi", "telecom", "cable", "broadband",
        "isp", "internet service",
    ]
    if any(kw in org_lower for kw in isp_keywords):
        result.update({
            "tier": 3, "label": "RESIDENTIAL_VPN_HOSTING",
            "detail": f"Residential ISP: {result['org']}",
        })
        return result

    # --- Tier 4: Unknown ---
    if info:
        result["detail"] = (
            f"ASN {asn} ({result['org']}) not in known lists"
            if asn else f"Org '{result['org']}' not classifiable"
        )
    return result
