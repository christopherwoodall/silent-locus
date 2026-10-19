#!/usr/bin/env python3
"""Lane 7 (revised) — package registry scanner: RubyGems / PyPI / npm.

Searches package registries for agent-swarm indicators tied to the Chinese
Amap fleet and the broader oai* toolkit thesis:

  HIGH   : hysandbox-ats, akbkyowd9geqr98, uqscan= / uqframe= / uqtag= literals
  MEDIUM : oai* name prefix (recent), getPoiInfo, amap-pc-ssr,
           POI ID pattern (B + 9 alphanumerics), amap/gaode in geo context
  LOW    : bare "oai" / "amap" / "agent swarm" noise

Sources:
  RubyGems — full compact index name sweep (cached locally) + search API
             (server-side name/summary/description) for description matches.
  PyPI      — RSS recent-updates feed (name/summary screen), then per-match
             JSON metadata. RSS covers ~the last 100 releases.
  npm       — registry search API (name+description+keywords, server-side),
             then per-candidate package doc for publish dates.

Focus: NEW or recently-published/updated packages (last 30 days). Rare
indicators (hysandbox-*, uq*= literals, the submitter ID) are always
reported regardless of age.

All hits are grade SECONDARY: these are other people's artifacts, found by
us, not our own observations.

Usage:
    packages.py [--dry-run] [--since-hours 24] [--json]

Config: ~/workspace/silent-locus/scripts/swarm-infra-config.json
        ("scanner_patterns" block). RubyGems index cache lives in
        ~/.cache/silent-locus-scanners/ (refresh > 24h old).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# ip_classifier.py lives one level up, in scripts/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit,
)
from ip_classifier import classify_ip  # noqa: E402

LANE = "packages"
RECENT_DAYS = 30
CACHE_DIR = os.path.expanduser("~/.cache/silent-locus-scanners")
RG_INDEX = os.path.join(CACHE_DIR, "rubygems-versions")
RG_INDEX_TTL = 24 * 3600
# Standing rule: every stored IP gets classified; shared ASN cache.
IP_ASN_CACHE = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/ip_asn_cache.json")

UA_HEADERS = {"User-Agent": USER_AGENT}  # no Accept-Encoding: urllib won't decode gzip


# ---------------------------------------------------------------------------
# indicator matching
# ---------------------------------------------------------------------------

def indicator_matches(name: str, summary: str, description: str) -> list:
    """Return [(indicator, tier)] for text matches across name/summary/desc.

    COUNSEL FIX (adversarial 2026-10-14): demoted to rare-marker tripwire.
    All MEDIUM rules (oai* prefix, amap-geo, getPoiInfo, POI-id regex,
    cross-registry reuse) CUT -- crowded with legitimate packages, zero
    agent precedent for registry staging by this fleet. All LOW rules CUT.
    Only HIGH exact-string tripwires remain: zero legitimate use, and an
    honest-zero baseline is itself signal.
    (Also resolves linguist H2/H3/H4: the cut rules contained the
    roadmap/scraper collisions, OAI-PMH collision, and hex-fragment POI
    matches.)
    """
    text = f"{name}\n{summary}\n{description}"
    low = text.lower()
    hits = []

    for term in ("hysandbox-ats", "akbkyowd9geqr98", "uqscan=", "uqframe=",
                 "uqtag="):
        if term in low:
            hits.append((term, "HIGH"))
    if "hysandbox" in low and ("hysandbox-ats", "HIGH") not in hits:
        hits.append(("hysandbox", "HIGH"))

    return sorted(hits)


def tier_confidence(matches: list, recent: bool) -> str:
    # Tripwire mode: only HIGH indicators exist. Any match is HIGH.
    return "HIGH" if matches else "LOW"


def is_rare(matches: list) -> bool:
    return any(t == "HIGH" for _, t in matches)


def within_days(iso_ts: str | None, days: int) -> bool:
    if not iso_ts:
        return False
    try:
        ts = iso_ts.replace("Z", "+00:00")
        dt = __import__("datetime").datetime.fromisoformat(ts)
        now = __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc)
        return (now - dt).days <= days
    except Exception:
        return False


# ---------------------------------------------------------------------------
# HTTP helpers (polite, curl-free; urllib handles the egress proxy here)
# ---------------------------------------------------------------------------

def http_json(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return -1, str(e)


def http_text(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return -1, str(e)


# ---------------------------------------------------------------------------
# RubyGems
# ---------------------------------------------------------------------------

def _rg_index_path(dry_run: bool) -> str | None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    fresh = (os.path.exists(RG_INDEX)
             and time.time() - os.path.getmtime(RG_INDEX) < RG_INDEX_TTL)
    if fresh:
        return RG_INDEX
    if dry_run:
        return None
    try:
        subprocess.run(
            ["curl", "-sS", "-m", "120", "--compressed", "-o", RG_INDEX,
             "https://index.rubygems.org/versions"],
            check=True, capture_output=True, timeout=150)
        return RG_INDEX
    except Exception as e:
        print(f"[rubygems] index download failed: {e}", file=sys.stderr)
        return RG_INDEX if os.path.exists(RG_INDEX) else None


def _rg_index_names(index_path: str):
    """Yield gem names from the compact-versions index (name per line)."""
    seen = set()
    with open(index_path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith(("created_at:", "---", "- ")):
                continue
            name = line.split(" ", 1)[0].strip()
            if name and name not in seen:
                seen.add(name)
                yield name


NAME_RE = re.compile(
    r"^(oai|amap|uqscan|uqtag|uqframe|hysandbox)[\w-]*"
    r"|[\w-]*(amap|uqscan|uqtag|uqframe|hysandbox)[\w-]*$",
    re.IGNORECASE)


def scan_rubygems(cfg, since_hours, seen_ids, dry_run):
    hits = []
    matched_names = set()
    now = utcnow_iso()

    def add_hit(name, version, pub_ts, desc, summary, url, matches, method,
                query):
        recent = within_days(pub_ts, RECENT_DAYS)
        matched_names.add(name)
        key = f"packages:rubygems:{name}:{version}"
        if not is_new(seen_ids, key):
            return
        conf = tier_confidence(matches, recent)
        hits.append(make_hit(
            lane=LANE, source_url=url,
            indicators_matched=[i for i, _ in matches],
            confidence=conf,
            summary=f"[rubygems] {name} {version} — "
                    f"{', '.join(i for i, _ in matches)}"
                    + ("" if recent else " (older than 30d, rare marker)"),
            provenance={"method": method, "query": query,
                        "registry": "rubygems",
                        "version_created_at": pub_ts,
                        "retrieved_at": now},
            extra={"package": name, "version": version,
                   "registry": "rubygems", "description": (desc or "")[:500]}))
        mark_seen(seen_ids, key)

    # 1) full compact-index name sweep
    index_path = _rg_index_path(dry_run)
    name_hits = []
    if index_path:
        for name in _rg_index_names(index_path):
            if NAME_RE.match(name):
                name_hits.append(name)
        if dry_run:
            name_hits = name_hits[:25]
    print(f"[rubygems] index name sweep: {len(name_hits)} pattern matches",
          file=sys.stderr)

    detail_cap = 25 if dry_run else 200
    for name in name_hits[:detail_cap]:
        time.sleep(0.5)
        status, meta = http_json(
            f"https://rubygems.org/api/v1/gems/{urllib.parse.quote(name)}.json")
        if status != 200 or not meta:
            continue
        desc, summary = meta.get("info") or "", meta.get("summary") or ""
        matches = indicator_matches(name, summary, desc)
        if not matches:
            continue
        pub_ts = meta.get("version_created_at")
        recent = within_days(pub_ts, RECENT_DAYS)
        if not (recent or is_rare(matches)):
            continue
        add_hit(name, meta.get("version"), pub_ts, desc, summary,
                meta.get("project_uri")
                or f"https://rubygems.org/gems/{name}",
                matches, "rubygems compact-index name sweep + gem metadata",
                f"index regex on {name}")

    # 2) server-side search API — catches description/summary matches the
    #    name sweep misses
    queries = ["uqscan", "uqtag", "uqframe", "hysandbox", "getPoiInfo"]
    if dry_run:
        queries = queries[:2]
    for q in queries:
        time.sleep(1.0)
        page = 1
        while True:
            status, results = http_json(
                "https://rubygems.org/api/v1/search.json?"
                f"query={urllib.parse.quote(q)}&page={page}")
            if status != 200 or not results:
                break
            for g in results:
                name = g.get("name", "")
                desc, summary = g.get("info") or "", g.get("summary") or ""
                matches = indicator_matches(name, summary, desc)
                if not matches:
                    continue
                pub_ts = g.get("version_created_at")
                recent = within_days(pub_ts, RECENT_DAYS)
                if not (recent or is_rare(matches)):
                    continue
                add_hit(name, g.get("version"), pub_ts, desc, summary,
                        g.get("project_uri")
                        or f"https://rubygems.org/gems/{name}",
                        matches, "rubygems search API", q)
            if dry_run or len(results) < 30 or page >= 5:
                break
            page += 1
    return hits, matched_names


# ---------------------------------------------------------------------------
# PyPI
# ---------------------------------------------------------------------------

def scan_pypi(cfg, since_hours, seen_ids, dry_run, cross_names=()):
    hits = []
    now = utcnow_iso()
    checked = 0
    detail_cap = 5 if dry_run else 50

    def add_pypi_hit(name, version, desc, url, matches, method, query, pub,
                     info):
        key = f"packages:pypi:{name}:{version or info.get('version', '')}"
        if not is_new(seen_ids, key):
            return
        conf = tier_confidence(matches, True)
        hits.append(make_hit(
            lane=LANE, source_url=url or info.get("project_url")
            or f"https://pypi.org/project/{name}/",
            indicators_matched=[i for i, _ in matches],
            confidence=conf,
            summary=f"[pypi] {name} {version} — "
                    f"{', '.join(i for i, _ in matches)}",
            provenance={"method": method, "query": query,
                        "registry": "pypi", "author": info.get("author"),
                        "published": pub, "retrieved_at": now},
            extra={"package": name, "version": version,
                   "registry": "pypi",
                   "description": ((info.get("summary") or desc) or "")[:500]}))
        mark_seen(seen_ids, key)

    status, xml_text = http_text("https://pypi.org/rss/updates.xml")
    if status != 200 or not xml_text:
        print(f"[pypi] RSS fetch failed: {status}", file=sys.stderr)
    else:
        try:
            root = ET.fromstring(xml_text)
            items = []
            for item in root.iter("item"):
                title = (item.findtext("title") or "").strip()
                desc = (item.findtext("description") or "").strip()
                link = (item.findtext("link") or "").strip()
                pub = (item.findtext("pubDate") or "").strip()
                if title:
                    items.append((title, desc, link, pub))
        except ET.ParseError as e:
            print(f"[pypi] RSS parse failed: {e}", file=sys.stderr)
            items = []
        print(f"[pypi] RSS window: {len(items)} recent releases",
              file=sys.stderr)
        for title, desc, link, pub in items:
            parts = title.rsplit(" ", 1)
            name = parts[0] if len(parts) == 2 else title
            version = parts[1] if len(parts) == 2 else ""
            matches = indicator_matches(name, "", desc)
            if not matches:
                continue
            checked += 1
            if checked > detail_cap:
                break
            time.sleep(0.5)
            status2, meta = http_json(
                f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json")
            info = (meta or {}).get("info", {}) if status2 == 200 else {}
            matches = indicator_matches(
                name, info.get("summary") or "", desc) or matches
            add_pypi_hit(name, version, desc, link, matches,
                         "pypi RSS recent-updates + JSON metadata",
                         "rss/updates.xml pattern screen", pub, info)

    # Cross-registry check: PyPI has no server-side search (XMLRPC search
    # disabled 2023), so look up RubyGems/npm indicator names directly —
    # multi-registry campaigns often reuse the same package name.
    cross = [n for n in cross_names if is_new(seen_ids, f"packages:pypi:{n}:x")]
    if dry_run:
        cross = cross[:5]
    for name in cross:
        if checked > detail_cap + (5 if dry_run else 100):
            break
        checked += 1
        time.sleep(0.5)
        status2, meta = http_json(
            f"https://pypi.org/pypi/{urllib.parse.quote(name)}/json")
        if status2 != 200 or not meta:
            continue
        info = meta.get("info", {})
        matches = indicator_matches(name, info.get("summary") or "",
                                    info.get("description") or "")
        if not matches:
            continue
        # cross-registry name reuse of an indicator name is itself signal
        matches = list(matches) + [("cross-registry name reuse", "MEDIUM")]
        add_pypi_hit(name, info.get("version", ""), info.get("description", ""),
                     info.get("project_url"), matches,
                     "pypi JSON cross-registry name lookup",
                     f"same name as registry hit: {name}", None, info)
    return hits


# ---------------------------------------------------------------------------
# npm
# ---------------------------------------------------------------------------

def scan_npm(cfg, since_hours, seen_ids, dry_run):
    hits = []
    matched_names = set()
    now = utcnow_iso()
    queries = ["uqscan", "uqtag", "uqframe", "hysandbox", "getPoiInfo",
               "amap", "oai"]
    if dry_run:
        queries = ["uqscan", "hysandbox"]

    detail_budget = 10 if dry_run else 60
    for q in queries:
        time.sleep(1.0)
        status, data = http_json(
            "https://registry.npmjs.org/-/v1/search?"
            f"text={urllib.parse.quote(q)}&size=250")
        if status != 200 or not data:
            continue
        objs = data.get("objects", [])
        print(f"[npm] query {q!r}: {data.get('total', 0)} total, "
              f"{len(objs)} returned", file=sys.stderr)
        for obj in objs:
            pkg = obj.get("package", {})
            name = pkg.get("name", "")
            desc = pkg.get("description") or ""
            pub_ts = obj.get("date") or (pkg.get("time") or {}).get("modified")
            matches = indicator_matches(name, "", desc)
            if not matches:
                continue
            # npm search has no date filter; enrich for publish date
            version = pkg.get("version", "")
            created = pub_ts
            if detail_budget > 0:
                detail_budget -= 1
                time.sleep(0.5)
                st2, doc = http_json(
                    f"https://registry.npmjs.org/{urllib.parse.quote(name)}")
                if st2 == 200 and doc:
                    times = doc.get("time", {})
                    created = times.get("created") or pub_ts
                    version = doc.get("dist-tags", {}).get("latest", version)
            recent = within_days(created, RECENT_DAYS)
            if not (recent or is_rare(matches)):
                continue
            key = f"packages:npm:{name}:{version}"
            if not is_new(seen_ids, key):
                continue
            matched_names.add(name)
            conf = tier_confidence(matches, recent)
            hits.append(make_hit(
                lane=LANE,
                source_url=f"https://www.npmjs.com/package/{name}",
                indicators_matched=[i for i, _ in matches],
                confidence=conf,
                summary=f"[npm] {name}@{version} — "
                        f"{', '.join(i for i, _ in matches)}"
                        + ("" if recent else " (older than 30d, rare marker)"),
                provenance={"method": "npm registry search API + package doc",
                            "query": q, "registry": "npm",
                            "created": created, "retrieved_at": now},
                extra={"package": name, "version": version,
                       "registry": "npm", "description": desc[:500]}))
            mark_seen(seen_ids, key)
    return hits, matched_names


# ---------------------------------------------------------------------------
# IP extraction + classification (standing rule: classify EVERY stored IP)
# ---------------------------------------------------------------------------

_IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_IPV6_RE = re.compile(r"\b(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\b")


def extract_ips(*texts: str) -> list:
    """Find syntactically valid IP literals in free text / URLs.

    Note: version strings like 1.2.3.4 can false-positive as IPv4. They
    validate via ipaddress and get classified (usually tier 4 UNKNOWN);
    see FALSE-POSITIVES-packages.md.
    """
    import ipaddress

    found = []
    for text in texts:
        if not text:
            continue
        for m in _IPV4_RE.finditer(text):
            try:
                ipaddress.IPv4Address(m.group(0))
                found.append(m.group(0))
            except ValueError:
                continue
        for m in _IPV6_RE.finditer(text):
            try:
                ip = ipaddress.IPv6Address(m.group(0))
                if not ip.is_link_local:
                    found.append(m.group(0))
            except ValueError:
                continue
    # stable order, deduped
    return sorted(set(found), key=found.index)


def enrich_ip_classification(hits: list, config: dict) -> None:
    """Attach ip_classification to every hit that stores an IP literal.

    Classification dicts go inline on the hit. Tier 1 (KNOWN_SWARM) and
    tier 2 (CLOUD_SERVICE) set "priority": true. Cloud IPs in unexpected
    places are NOT filtered — they are the signal.
    """
    for h in hits:
        # make_hit() flattens `extra` into the hit, so serialize the whole
        # hit (minus any prior classification) to catch IPs in any field:
        # name, summary, description, homepage/project URLs.
        blob = json.dumps(
            {k: v for k, v in h.items() if k != "ip_classification"},
            ensure_ascii=False, default=str)
        ips = extract_ips(blob)
        if not ips:
            continue
        classifications = {}
        for ip in ips:
            try:
                c = classify_ip(ip, config, IP_ASN_CACHE)
            except Exception as e:
                c = {"tier": 4, "label": "UNKNOWN",
                     "detail": f"classifier error: {e}", "ip": ip}
            classifications[ip] = c
        h["ip_classification"] = classifications
        if any(c.get("tier") in (1, 2) for c in classifications.values()):
            h["priority"] = True


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run all registry scanners. Returns list of factum-ready hit dicts."""
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    hits = []
    cross_names = set()
    # RubyGems and npm first: their matched names seed PyPI's
    # cross-registry check (PyPI has no server-side search).
    for fn in (scan_rubygems, scan_npm):
        try:
            sub_hits, names = fn(cfg, since_hours, seen_ids, dry_run)
            hits.extend(sub_hits)
            cross_names.update(names)
        except Exception as e:
            print(f"[{fn.__name__}] failed: {type(e).__name__}: {e}",
                  file=sys.stderr)
    try:
        hits.extend(scan_pypi(cfg, since_hours, seen_ids, dry_run,
                              cross_names=cross_names))
    except Exception as e:
        print(f"[scan_pypi] failed: {type(e).__name__}: {e}",
              file=sys.stderr)
    # Standing rule: classify every IP stored on any hit, no exceptions.
    enrich_ip_classification(hits, cfg)
    # rank: HIGH first, then MEDIUM, then LOW
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Lane 7 — package registry scanner (RubyGems/PyPI/npm)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
