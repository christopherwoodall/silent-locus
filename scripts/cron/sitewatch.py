#!/usr/bin/env python3
"""Shared library for per-site cron monitors (scripts/cron/sites/*.py).

Each site script is ~20 lines: it defines a SITE dict and calls
sitewatch.main(SITE). All fetching, state handling, and reporting live
here so the per-site scripts stay thin and uniform.

Kinds:
  listing-hash  GET each URL, sha256 the body, compare with state.
  api-poll      GET JSON endpoint, sha256 canonicalized JSON, compare.
  cdx           Wayback CDX new-capture check for a domain (paste archives).
  feed          IOC feed recent-items check (GET-able sources only).

Statuses: NEW (never seen), CHANGED (hash/content differs), UNCHANGED,
NEW_CAPTURES(n), NEW_MATCHES(n), NO_NEW, SKIPPED, ERROR.

Grading: every hit is SECONDARY until independently verified (operator
grading rule). This library never assigns PRIMARY.

Passive GET only. >=5s between requests. 30s timeout.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(BASE_DIR, "state")
USER_AGENT = "silent-locus-sitewatch/1.0 (+hunt: agent-infrastructure)"
REQUEST_SPACING = 5.0
TIMEOUT = 30
CDX_BASE = "http://web.archive.org/cdx/search/cdx"

_last_req = [0.0]


def utcnow_iso() -> str:
    return (datetime.datetime.now(datetime.timezone.utc)
            .replace(microsecond=0).isoformat().replace("+00:00", "Z"))


def _space() -> None:
    dt = time.time() - _last_req[0]
    if dt < REQUEST_SPACING:
        time.sleep(REQUEST_SPACING - dt)
    _last_req[0] = time.time()


def _fetch(url: str) -> tuple:
    """GET url. Returns (http_code:int|None, body:bytes, error:str|None).

    HTTP error statuses (4xx/5xx) are NOT failures here: the code and
    body are returned so callers can treat a code transition as a
    state change. Only transport failures (DNS, timeout, refused)
    return code=None with an error string.
    """
    _space()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read(), None
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        return e.code, body, None
    except Exception as e:  # never crash the caller
        return None, b"", f"{type(e).__name__}: {e}"[:200]


def _state_path(name: str) -> str:
    return os.path.join(STATE_DIR, f"{name}.json")


def _load_state(name: str) -> dict:
    try:
        with open(_state_path(name), "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_state(name: str, state: dict) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = _state_path(name) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.rename(tmp, _state_path(name))  # atomic; no torn state


def _report_error(site_name: str, error_type: str, message: str) -> None:
    try:
        sys.path.insert(0, os.path.join(BASE_DIR, "..", "scanners"))
        import _common
        _common.report_error(f"cron-sites/{site_name}", error_type, message)
    except Exception:
        pass


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_listing_hash(site: dict, state: dict, dry_run: bool,
                       limit: int | None) -> tuple:
    """GET each URL, sha256 body, compare with state. Returns (results, state)."""
    results, urls_state = [], state.setdefault("urls", {})
    urls = site["urls"][:limit] if limit else site["urls"]
    for url in urls:
        if dry_run:
            results.append({"url": url, "status": "WOULD_FETCH"})
            continue
        code, body, err = _fetch(url)
        prev = urls_state.get(url, {})
        if err or code is None:
            # No HTTP response at all (DNS, timeout, refused): transient.
            results.append({"url": url, "status": "ERROR", "detail": err})
            _report_error(site["name"], "fetch_error", f"{url}: {err}")
            continue
        # Any HTTP response (even 404/500) is hashable state: a code
        # transition (200->404) reports CHANGED once, then goes quiet.
        h = _sha256(body)
        old = prev.get("sha256")
        old_code = prev.get("http")
        if old is None:
            status = "NEW"
        elif old != h or old_code != code:
            status = "CHANGED"
        else:
            status = "UNCHANGED"
        detail = None if old_code in (None, code) else f"http {old_code}->{code}"
        results.append({"url": url, "status": status, "http": code,
                        "bytes": len(body), "sha256": h[:16],
                        **({"detail": detail} if detail else {})})
        urls_state[url] = {"sha256": h, "bytes": len(body), "http": code,
                           "checked_at": utcnow_iso()}
    return results, state


def check_api_poll(site: dict, state: dict, dry_run: bool,
                   limit: int | None) -> tuple:
    """GET JSON endpoints, sha256 canonicalized JSON, compare."""
    results, urls_state = [], state.setdefault("urls", {})
    urls = site["urls"][:limit] if limit else site["urls"]
    for url in urls:
        if dry_run:
            results.append({"url": url, "status": "WOULD_FETCH"})
            continue
        code, body, err = _fetch(url)
        prev = urls_state.get(url, {})
        if err or code is None:
            results.append({"url": url, "status": "ERROR", "detail": err})
            _report_error(site["name"], "fetch_error", f"{url}: {err}")
            continue
        try:
            canon = json.dumps(json.loads(body), sort_keys=True,
                               separators=(",", ":"), ensure_ascii=False)
            h = _sha256(canon.encode("utf-8"))
            as_json = True
        except ValueError:
            # Non-JSON body (e.g. an error page): hash raw bytes so a
            # content-type transition still reports CHANGED once.
            h = _sha256(body)
            as_json = False
        old = prev.get("sha256")
        old_code = prev.get("http")
        if old is None:
            status = "NEW"
        elif old != h or old_code != code:
            status = "CHANGED"
        else:
            status = "UNCHANGED"
        detail = None if old_code in (None, code) else f"http {old_code}->{code}"
        if not as_json and detail is None:
            detail = "non-JSON body"
        results.append({"url": url, "status": status, "http": code,
                        "sha256": h[:16],
                        **({"detail": detail} if detail else {})})
        urls_state[url] = {"sha256": h, "http": code,
                           "checked_at": utcnow_iso()}
    return results, state


def check_cdx(site: dict, state: dict, dry_run: bool,
              limit: int | None) -> tuple:
    """Wayback CDX new-capture check per domain. site["urls"] holds domains."""
    results = []
    domains = site["urls"][:limit] if limit else site["urls"]
    if "newest_ts" in state:
        from_ts = state["newest_ts"]
    else:
        # First run: bound catch-up to the last 30 days so a busy
        # domain doesn't take dozens of runs to reach the present.
        from_ts = (datetime.datetime.now(datetime.timezone.utc)
                   - datetime.timedelta(days=30)).strftime("%Y%m%d%H%M%S")
    newest_known = state.get("newest_ts", from_ts)
    newest_seen = newest_known
    for domain in domains:
        q = (f"{CDX_BASE}?url={urllib.parse.quote(domain)}"
             f"&matchType=domain&output=json&fl=timestamp,original,statuscode"
             f"&filter=statuscode:200&collapse=urlkey&limit=200"
             f"&from={from_ts}")
        if dry_run:
            results.append({"domain": domain, "status": "WOULD_QUERY",
                            "cdx_url": q})
            continue
        code, body, err = _fetch(q)
        if err or code != 200:
            results.append({"domain": domain, "status": "ERROR",
                            "detail": err or f"http={code}"})
            _report_error(site["name"], "cdx_error", f"{domain}: {err or code}")
            continue
        try:
            rows = json.loads(body)
            if not isinstance(rows, list):
                raise ValueError("CDX returned non-list")
        except ValueError:
            results.append({"domain": domain, "status": "ERROR",
                            "detail": "CDX body not JSON"})
            continue
        if rows and rows[0][0] == "timestamp":  # header row
            rows = rows[1:]
        fresh = [r for r in rows if r and r[0] > newest_known]
        for r in rows:
            if r and r[0] > newest_seen:
                newest_seen = r[0]
        if fresh:
            results.append({"domain": domain, "status": f"NEW_CAPTURES({len(fresh)})",
                            "examples": [r[1] for r in fresh[:5]]})
        else:
            results.append({"domain": domain, "status": "NO_NEW",
                            "captures_seen": len(rows)})
    state["newest_ts"] = newest_seen
    state["last_check"] = utcnow_iso()
    return results, state


def check_feed(site: dict, state: dict, dry_run: bool,
               limit: int | None) -> tuple:
    """IOC feed check over GET-able sources. site["feed"] describes it.

    Supported feed kinds:
      otx-indicators  GET OTX /api/v1/indicators/{type}/{value}/general
                      (keyless) per indicator; report pulse-count changes.
      delegate      hand off to scripts/scanners/iocfeeds.py when present.
      skipped       no keyless GET surface; exit 0 with SKIPPED.
    """
    feed = site.get("feed", {})
    fkind = feed.get("kind", "skipped")
    if fkind == "skipped":
        return ([{"status": "SKIPPED",
                  "detail": feed.get("reason", "no keyless surface")}], state)
    if fkind == "delegate":
        mod = feed.get("module")
        try:
            sys.path.insert(0, os.path.join(BASE_DIR, "..", "scanners"))
            m = __import__(mod)
            if hasattr(m, "check"):
                return m.check(site, state, dry_run, limit)
            return ([{"status": "SKIPPED",
                      "detail": f"{mod} has no check() entrypoint"}], state)
        except Exception as e:
            return ([{"status": "SKIPPED",
                      "detail": f"module {mod} not present: "
                               f"{type(e).__name__}"}], state)
    if fkind == "otx-indicators":
        # Keyless OTX indicator lookups (verified 2026-10-22). Reports
        # third-party pulse counts per watched indicator; a rising count
        # means someone else filed our infrastructure.
        base = "https://otx.alienvault.com/api/v1/indicators"
        inds = feed.get("indicators", [])
        if limit:
            inds = inds[:limit]
        if dry_run:
            return ([{"indicator": f"{i['type']}:{i['value']}",
                      "status": "WOULD_FETCH"} for i in inds], state)
        seen = state.setdefault("pulse_counts", {})
        results = []
        for ind in inds:
            itype, value = ind["type"], ind["value"]
            key = f"{itype}:{value}"
            url = (f"{base}/{itype}/"
                   f"{urllib.parse.quote(value, safe='')}/general")
            code, body, err = _fetch(url)
            if err or code != 200:
                results.append({"indicator": key, "status": "ERROR",
                                "detail": err or f"http={code}"})
                _report_error(site["name"], "feed_error",
                              f"{key}: {err or code}")
                continue
            try:
                count = int(json.loads(body)
                            .get("pulse_info", {}).get("count", 0))
            except (ValueError, TypeError):
                results.append({"indicator": key, "status": "ERROR",
                                "detail": "bad JSON"})
                continue
            old = seen.get(key)
            if old is None:
                status = f"PULSES({count})"
            elif count != old:
                status = f"CHANGED({old}->{count})"
            else:
                status = "UNCHANGED"
            results.append({"indicator": key, "status": status})
            seen[key] = count
        state["last_check"] = utcnow_iso()
        return results, state
    return ([{"status": "ERROR",
              "detail": f"unknown feed kind {fkind}"}], state)


_CHECKERS = {
    "listing-hash": check_listing_hash,
    "api-poll": check_api_poll,
    "cdx": check_cdx,
    "feed": check_feed,
}


def run_site(site: dict, dry_run: bool = False,
             limit: int | None = None) -> dict:
    """Run one site's check. Returns a result dict (never raises)."""
    name = site["name"]
    kind = site["kind"]
    checker = _CHECKERS.get(kind)
    result = {"site": name, "label": site.get("label", name), "kind": kind,
              "checked_at": utcnow_iso(), "dry_run": dry_run}
    if checker is None:
        result.update({"status": "ERROR",
                       "detail": f"unknown kind {kind}", "results": []})
        return result
    state = _load_state(name)
    try:
        results, new_state = checker(site, state, dry_run, limit)
    except Exception as e:  # belt and suspenders
        _report_error(name, "checker_crash", f"{type(e).__name__}: {e}")
        result.update({"status": "ERROR", "detail": "checker crashed",
                       "results": []})
        return result
    if not dry_run:
        _save_state(name, new_state)
    stats = {}
    for r in results:
        stats[r["status"].split("(")[0]] = stats.get(r["status"].split("(")[0], 0) + 1
    result.update({"results": results, "summary": stats})
    return result


def main(site: dict) -> int:
    ap = argparse.ArgumentParser(description=f"sitewatch: {site.get('label')}")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be fetched; write no state")
    ap.add_argument("--json", action="store_true",
                    help="print result as JSON")
    ap.add_argument("--limit", type=int, default=None,
                    help="check at most N urls/domains")
    args = ap.parse_args()
    res = run_site(site, dry_run=args.dry_run, limit=args.limit)
    if args.json or args.dry_run:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print(f"[{res['label']}] {res.get('summary', res.get('status'))}")
        for r in res.get("results", []):
            target = r.get("url") or r.get("domain") or r.get("indicator", "")
            print(f"  {r.get('status')}: {target}"
                  f"{' — ' + str(r.get('detail', '')) if r.get('detail') else ''}")
    # exit 1 only on hard ERRORs (not on NEW/CHANGED findings)
    bad = any(r.get("status") == "ERROR" for r in res.get("results", []))
    return 1 if bad else 0
