#!/usr/bin/env python3
"""Telegraph watch (Hermes port): content/view deltas on watched
telegra.ph pages.

CDX is blind on telegra.ph, so this module polls the PUBLIC
Telegraph API directly:

    GET https://api.telegra.ph/getPage/<path>?return_content=true

No account creation, no auth: getPage/getViews are public
read-only endpoints. Passive GET only.

Watched pages come from tools/config.json ("telegraph" block):
- Research-Links-05-26 (corpus evidence link)
- Test-Link-88990-05-18 (fleet marker term)

Tracks per page: content hash (sha256 of canonical content
JSON), title, views. Emits on:
- content edit (hash change) -> LOW hit
- page deleted (2 consecutive misses) -> LOW hit
First sighting seeds the baseline silently. View counts are
recorded and carried on hits as context, but view creep alone
never alerts (views only move up on a public page).

Contract: scan(since_hours=24, seen_ids=None, dry_run=False).
Grade SECONDARY (third-party surface), confidence LOW.

State: hermes/workspace/state/telegraph.json.

Safety rules kept from the source:
- Path injection: paths are validated against
  ^[A-Za-z0-9._-]{1,64}$ and URL-quoted before use.
- API ok:false -> PAGE_NOT_FOUND counts a miss. Only the 2nd
  CONSECUTIVE miss fires DELETED.
- ok:true with content missing -> degraded, skip comparison.
- Empty content [] -> a real edit (page wiped), LOW hit.
- Views decrease -> never alerts.
- Oversized page (>1 MB) -> skip hash comparison this run.
- 429/5xx/transport -> skip page, keep baseline, report_error.
- State corrupt/non-dict -> re-seed silently, no hits.
- Titles are page text: cut and passed through
  redact_secrets before entering a hit summary. Author names
  are never stored, never summarized, and never emitted: only
  the title and the content hash are kept.

Port changes vs the source: watched pages and timings from
tools/config.json; state under hermes/workspace/state/;
no silent-locus paths.

Usage: telegraph.py [--dry-run] [--since-hours 24] [--json]
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
    USER_AGENT, load_config, make_hit, utcnow_iso, is_new, mark_seen,
    parse_args, emit, redact_secrets, report_error, STATE_DIR,
    scanner_enabled,
)

LANE = "telegraph"
STATE_PATH = os.path.join(STATE_DIR, "telegraph.json")
API_BASE = "https://api.telegra.ph"
PATH_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
TITLE_LEN = 200


def _api_get_page(path: str, timeout: int, max_body: int
                  ) -> tuple[str, dict | None]:
    """GET getPage. Status: ok | not_found | api_error |
    transport_error | oversized | bad_path."""
    if not PATH_RE.match(path):
        return "bad_path", None
    url = (f"{API_BASE}/getPage/{urllib.parse.quote(path, safe='')}"
           "?return_content=true")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(max_body + 1)
    except urllib.error.HTTPError:
        return "transport_error", None
    except Exception:
        return "transport_error", None
    if len(raw) > max_body:
        return "oversized", None
    try:
        data = json.loads(raw.decode("utf-8", "replace"))
    except (json.JSONDecodeError, ValueError):
        return "api_error", None
    if not isinstance(data, dict):
        return "api_error", None
    if not data.get("ok"):
        err = str(data.get("error", ""))
        if "NOT_FOUND" in err.upper() or "PAGE" in err.upper():
            return "not_found", None
        return "api_error", None
    result = data.get("result")
    if not isinstance(result, dict):
        return "api_error", None
    return "ok", result


def _content_hash(content) -> str | None:
    """sha256 of canonical content JSON. None when content is
    absent (degraded). Distinct from [] (page wiped), which
    hashes."""
    if content is None:
        return None
    canon = json.dumps(content, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _load_state() -> dict:
    try:
        with open(STATE_PATH) as f:
            state = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    return state if isinstance(state, dict) else {}


def _save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
    os.replace(tmp, STATE_PATH)


def _edit_hit(path: str, why: str, prev: dict, result: dict,
              scanned_at: str) -> dict:
    page_url = f"https://telegra.ph/{path}"
    _, title = redact_secrets(str(result.get("title", ""))[:TITLE_LEN])
    return make_hit(
        lane=LANE,
        source_url=page_url,
        indicators_matched=["telegraph-edit", path],
        confidence="LOW",
        summary=f"[telegraph] EDIT on telegra.ph/{path}: {title!r} "
                f"— content changed since "
                f"{prev.get('last_seen', '?')} — {page_url}",
        provenance={
            "method": "public api.telegra.ph getPage (no auth), "
                      "content-hash diff",
            "page_url": page_url,
            "why_watched": why,
            "prev_content_hash": (prev.get("content_hash") or "")[:16],
            "prev_views": prev.get("views"),
            "retrieved_at": scanned_at,
        },
        extra={
            "path": path,
            "title": title,
            "views": result.get("views"),
            "why_watched": why,
        },
    )


def _deleted_hit(path: str, why: str, prev: dict,
                 scanned_at: str) -> dict:
    page_url = f"https://telegra.ph/{path}"
    return make_hit(
        lane=LANE,
        source_url=page_url,
        indicators_matched=["telegraph-deleted", path],
        confidence="LOW",
        summary=f"[telegraph] DELETED: telegra.ph/{path} returned "
                f"PAGE_NOT_FOUND on 2 consecutive checks (last seen "
                f"{prev.get('last_seen', '?')}) — {page_url}",
        provenance={
            "method": "public api.telegra.ph getPage (no auth)",
            "page_url": page_url,
            "why_watched": why,
            "retrieved_at": scanned_at,
        },
        extra={"path": path, "why_watched": why},
    )


def scan(since_hours: float = 24, seen_ids=None,
         dry_run: bool = False) -> list:
    if not dry_run and not scanner_enabled("telegraph"):
        print("[telegraph] live scan refused: telegraph.enabled "
              "is not true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    if seen_ids is None:
        seen_ids = set()
    scanned_at = utcnow_iso()
    block = load_config().get("scanners", {}).get("telegraph", {})
    watched = [(w.get("path", ""), w.get("why", ""))
               for w in block.get("watched", [])]
    spacing = float(block.get("rate_limit_seconds", 3))
    timeout = int(block.get("timeout", 30))
    max_body = int(block.get("max_body", 1_000_000))

    if dry_run:
        print("[dry-run] telegraph plan:", file=sys.stderr)
        for path, why in watched:
            print(f"  WOULD GET: {API_BASE}/getPage/{path}"
                  f"?return_content=true  ({why[:60]})", file=sys.stderr)
        print(f"  state: {STATE_PATH} (no writes in dry-run)",
              file=sys.stderr)
        return []

    state = _load_state()
    hits = []
    dirty = False
    for path, why in watched:
        status, result = _api_get_page(path, timeout, max_body)
        if status in ("transport_error", "api_error", "bad_path"):
            report_error("telegraph", f"getpage_{status}",
                         f"{path}: {status}, baseline kept",
                         {"path": path})
            print(f"[telegraph] {path}: {status}, baseline kept",
                  file=sys.stderr)
            continue
        if status == "oversized":
            print(f"[telegraph] {path}: oversized, hash check skipped",
                  file=sys.stderr)
            report_error("telegraph", "getpage_oversized",
                         f"{path}: >1MB, hash check skipped",
                         {"path": path})
            continue
        prev = state.get(path)
        if status == "not_found":
            if prev is None:
                state[path] = {"missing": True, "miss_count": 1,
                               "first_seen": scanned_at,
                               "last_seen": scanned_at,
                               "why": why}
                dirty = True
                continue
            misses = int(prev.get("miss_count", 0)) + 1
            prev["miss_count"] = misses
            prev["last_seen"] = scanned_at
            dirty = True
            print(f"[telegraph] {path}: not found "
                  f"(miss {misses})", file=sys.stderr)
            if misses >= 2 and not prev.get("missing"):
                key = f"telegraph:deleted:{path}"
                if is_new(seen_ids, key):
                    mark_seen(seen_ids, key)
                    hits.append(_deleted_hit(path, why, prev,
                                             scanned_at))
                prev["missing"] = True
            continue
        content = result.get("content")
        chash = _content_hash(content)
        views = result.get("views")
        if prev is None or prev.get("missing"):
            state[path] = {
                "title": str(result.get("title", ""))[:TITLE_LEN],
                "content_hash": chash,
                "views": views,
                "miss_count": 0,
                "first_seen": scanned_at,
                "last_seen": scanned_at,
                "why": why,
            }
            dirty = True
            print(f"[telegraph] {path}: baseline seeded",
                  file=sys.stderr)
            continue
        prev["miss_count"] = 0
        prev["last_seen"] = scanned_at
        prev.pop("author_name", None)
        if isinstance(views, int):
            prev["views"] = views
        dirty = True
        if chash is None:
            print(f"[telegraph] {path}: ok but content absent, "
                  f"hash kept", file=sys.stderr)
            continue
        if chash != prev.get("content_hash"):
            key = f"telegraph:edit:{path}:{chash[:16]}"
            print(f"[telegraph] {path}: CONTENT CHANGED",
                  file=sys.stderr)
            if is_new(seen_ids, key):
                mark_seen(seen_ids, key)
                hits.append(_edit_hit(path, why, prev, result,
                                      scanned_at))
            prev["content_hash"] = chash
            prev["title"] = str(result.get("title", ""))[:TITLE_LEN]
            prev.pop("author_name", None)
        else:
            print(f"[telegraph] {path}: unchanged "
                  f"(views={views})", file=sys.stderr)
        time.sleep(spacing)
    if dirty:
        _save_state(state)
    hits.sort(key=lambda h: h["summary"])
    return hits


def main():
    args = parse_args("Telegraph watch (Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
