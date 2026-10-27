#!/usr/bin/env python3
"""Slot-5 intel watch (Hermes port): new posts on swarmcha.se
and norforge.com.

Automates the manual flow: fetch the two intel sites' index
pages through the r.jina.ai reader (plain GET, polite rate),
inventory their posts, compare against a baseline state file,
and emit New to inventory findings.

Sources:
- https://swarmcha.se/posts
- https://norforge.com/blog

Contract: scan(since_hours=24, seen_ids=None, dry_run=False).
Hits carry the _common contract fields. Grade SECONDARY
(third-party intel). Confidence MEDIUM.

State: hermes/workspace/state/intel_slot5.json, mapping
{source_id: {slug: {title, date, first_seen}}}.
First run seeds the baseline and emits no hits.

Politeness: 10 s spacing between index fetches (jina free
tier), 60/120 s backoff on 429, then the source is skipped.
Never mark a failed source seen, never update its baseline,
so the next run retries it.

Direct-fetch fallback: when the jina reader fails or returns
truncated output, retry with a plain GET of the index URL and
inventory the direct HTML the same way (slug keys). A
direct-only inventory NEVER seeds a fresh source's baseline.
It only diffs against an existing one.

Safety rules kept from the source:
- Empty or failed fetch with a non-empty baseline: skip the
  source. Never read "could not read the index" as "all posts
  deleted".
- Zero posts parsed from a 200 response: same skip path.
- Truncation guard: skip partially loaded reader output.
- Flood guard: more than MAX_NEW_POSTS new slugs in one run
  emits ONE summary hit, not N lead hits.
- Slug keys are per-source. A title edit never re-fires.
- Titles are page text: cut to 200 chars, passed through
  redact_secrets before entering a hit summary.

Port changes vs the source: sources and timings come from
tools/config.json (slug regexes compiled at run time);
state under hermes/workspace/state/; no silent-locus paths.

Usage: intel_slot5.py [--dry-run] [--since-hours 24] [--json]
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso, is_new, mark_seen,
    parse_args, emit, redact_secrets, report_error, STATE_DIR,
    scanner_enabled,
)

LANE = "intel-slot5"
STATE_PATH = os.path.join(STATE_DIR, "intel_slot5.json")
JINA_BASE = "https://r.jina.ai/"
MAX_TEXT = 500_000
TITLE_LEN = 200

_URL_RE = re.compile(r"https?://[^\s)<>\"]{1,300}")
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})|([A-Z]{3}\s+\d{4})")
_IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_MD_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_BULLET_RE = re.compile(r"^[\s*#>\-*+\d.()]+")
_TRAILING_PUNCT = ".,;:!?"
_ANCHOR_RE = re.compile(
    r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S | re.I)


def _sources(block: dict) -> list:
    out = []
    for s in block.get("sources", []):
        try:
            out.append((s["source_id"], s["label"], s["index_url"],
                        re.compile(s["slug_regex"])))
        except (KeyError, re.error) as e:
            print(f"[intel_slot5] bad source entry {s}: {e}",
                  file=sys.stderr)
    return out


def _looks_truncated(text: str) -> bool:
    if "URL Source:" not in text[:800]:
        return True
    tail = text[-600:]
    return tail.count("[") > tail.count("]")


def _fetch_index(index_url: str, label: str, timeout: int,
                 retry_sleeps: list) -> str | None:
    url = JINA_BASE + index_url
    last = ""
    for attempt, sleep_s in enumerate([0] + list(retry_sleeps)):
        if sleep_s:
            print(f"[intel_slot5] {label}: 429/backoff, retry in "
                  f"{sleep_s}s (attempt {attempt + 1})", file=sys.stderr)
            time.sleep(sleep_s)
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/plain",
            "X-Return-Format": "text",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read(MAX_TEXT + 1)
                return raw[:MAX_TEXT].decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 429:
                continue
            print(f"[intel_slot5] {label}: {last} (definitive)",
                  file=sys.stderr)
            return None
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            print(f"[intel_slot5] {label}: {last}", file=sys.stderr)
    print(f"[intel_slot5] {label}: giving up ({last})", file=sys.stderr)
    return None


def _fetch_direct(index_url: str, label: str, timeout: int) -> str | None:
    req = urllib.request.Request(index_url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,text/plain",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(MAX_TEXT + 1)
            return raw[:MAX_TEXT].decode("utf-8", "replace")
    except Exception as e:
        print(f"[intel_slot5] {label}: direct fetch failed: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return None


def _absolutize_relative_hrefs(text: str, index_url: str) -> str:
    m = re.match(r"(https?://[^/]+)", index_url)
    if not m:
        return text
    base = m.group(1)
    return re.sub(r'href=(["\'])/',
                  lambda hm: f'href={hm.group(1)}{base}/', text)


def _nearby_title(text: str, pos: int) -> str:
    window = text[max(0, pos - 500):pos]
    window = _IMAGE_MD_RE.sub("", window)
    window = re.sub(r"\]\(\s*$", "", window.rstrip())
    idx = window.rfind("##")
    if idx != -1:
        cand = window[idx + 2:]
    else:
        idx = window.rfind("[")
        cand = window[idx + 1:] if idx != -1 else window[-160:]
    cand = _LINK_MD_RE.sub(r"\1", cand)
    cand = _BULLET_RE.sub("", cand).replace("##", " ")
    return re.sub(r"\s+", " ", cand).strip()[:TITLE_LEN]


def _inventory(text: str, slug_re) -> dict:
    out = {}
    for m in _URL_RE.finditer(text):
        url = m.group(0).rstrip(_TRAILING_PUNCT)
        sm = slug_re.match(url)
        if not sm:
            continue
        slug = sm.group(1)
        if slug in out:
            continue
        before = text[max(0, m.start() - 80):m.start()]
        dm = _DATE_RE.search(before)
        out[slug] = {
            "title": _nearby_title(text, m.start()),
            "date": dm.group(0) if dm else "",
        }
    return out


def _inventory_html(text: str, slug_re) -> dict:
    out = {}
    for m in _ANCHOR_RE.finditer(text):
        url = m.group(1).rstrip(_TRAILING_PUNCT)
        sm = slug_re.match(url)
        if not sm:
            continue
        slug = sm.group(1)
        if slug in out:
            continue
        title = re.sub(r"<[^>]*>", " ", m.group(2))
        title = re.sub(r"\s+", " ", title).strip()[:TITLE_LEN]
        before = text[max(0, m.start() - 200):m.start()]
        dm = _DATE_RE.search(before)
        out[slug] = {
            "title": title,
            "date": dm.group(0) if dm else "",
        }
    return out


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


def _new_post_hit(source_id: str, label: str, index_url: str, slug: str,
                  info: dict, scanned_at: str) -> dict:
    post_url = f"{index_url.rstrip('/')}/{slug}"
    _, title = redact_secrets(info.get("title", ""))
    date = info.get("date", "")
    return make_hit(
        lane=LANE,
        source_url=post_url,
        indicators_matched=["new-post", source_id],
        confidence="MEDIUM",
        summary=f"[intel_slot5] New to inventory on {label}: "
                f"{title!r} ({date or 'undated'}) — {post_url}",
        provenance={
            "method": "r.jina.ai reader GET of index page (plain GET, "
                      "polite rate)",
            "index_url": index_url,
            "post_url": post_url,
            "slug": slug,
            "retrieved_at": scanned_at,
            "caveat": "reader content may be cached; 'new' means new "
                      "to our inventory",
        },
        extra={
            "source_id": source_id,
            "slug": slug,
            "post_date": date,
            "first_seen": scanned_at,
        },
    )


def scan(since_hours: float = 24, seen_ids=None,
         dry_run: bool = False) -> list:
    if not dry_run and not scanner_enabled("intel_slot5"):
        print("[intel_slot5] live scan refused: intel_slot5.enabled "
              "is not true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    if seen_ids is None:
        seen_ids = set()
    scanned_at = utcnow_iso()
    block = load_config().get("scanners", {}).get("intel_slot5", {})
    sources = _sources(block)
    spacing = float(block.get("rate_limit_seconds", 10))
    timeout = int(block.get("timeout", 60))
    retry_sleeps = block.get("retry_sleeps", [60, 120])
    max_new = int(block.get("max_new_posts", 8))

    if dry_run:
        print("[dry-run] intel_slot5 plan:", file=sys.stderr)
        for _sid, label, index_url, _re in sources:
            print(f"  WOULD GET: {JINA_BASE}{index_url}  ({label})",
                  file=sys.stderr)
        print(f"  state: {STATE_PATH} (no writes in dry-run)",
              file=sys.stderr)
        return []

    state = _load_state()
    hits = []
    dirty = False
    for source_id, label, index_url, slug_re in sources:
        fresh = source_id not in state
        baseline = state.setdefault(source_id, {})
        text = _fetch_index(index_url, label, timeout, retry_sleeps)
        via_direct = False
        if text is None or _looks_truncated(text):
            reason = ("fetch_failed" if text is None
                      else "possibly_truncated")
            print(f"[intel_slot5] {label}: jina {reason}, trying "
                  f"direct fetch", file=sys.stderr)
            direct = _fetch_direct(index_url, label, timeout)
            if direct is not None:
                direct = _absolutize_relative_hrefs(direct, index_url)
            direct_inv = _inventory_html(direct, slug_re) \
                if direct is not None else {}
            if direct_inv:
                text, via_direct = direct, True
            else:
                report_error("intel_slot5",
                             f"index_{reason}_direct_failed",
                             f"{label}: jina {reason} and direct "
                             f"fallback unusable, baseline kept",
                             {"index_url": index_url})
                continue
        inv = _inventory_html(text, slug_re) if via_direct \
            else _inventory(text, slug_re)
        if not inv:
            report_error("intel_slot5", "index_parse_empty",
                         f"{label}: parsed 0 posts, baseline kept",
                         {"index_url": index_url})
            continue
        new_slugs = [s for s in inv if s not in baseline]
        for slug in inv:
            if slug not in baseline:
                baseline[slug] = {
                    "title": inv[slug]["title"],
                    "date": inv[slug]["date"],
                    "first_seen": scanned_at,
                }
                dirty = True
        print(f"[intel_slot5] {label}: {len(inv)} posts, "
              f"{len(new_slugs)} new", file=sys.stderr)
        if fresh and via_direct:
            print(f"[intel_slot5] {label}: direct-only inventory, "
                  f"not seeding baseline", file=sys.stderr)
            report_error("intel_slot5", "direct_fallback_no_seed",
                         f"{label}: fresh source, direct-only "
                         f"inventory not seeded",
                         {"index_url": index_url})
            state.pop(source_id, None)
            continue
        if fresh:
            for slug in inv:
                mark_seen(seen_ids, f"intel_slot5:{source_id}:{slug}")
            print(f"[intel_slot5] {label}: baseline seeded "
                  f"({len(inv)} posts, 0 hits)", file=sys.stderr)
            continue
        if not new_slugs:
            continue
        if len(new_slugs) > max_new:
            for slug in new_slugs:
                mark_seen(seen_ids, f"intel_slot5:{source_id}:{slug}")
            hits.append(make_hit(
                lane=LANE,
                source_url=index_url,
                indicators_matched=["inventory-reshuffle", source_id],
                confidence="LOW",
                summary=f"[intel_slot5] {label}: {len(new_slugs)} new "
                        f"slugs at once (reshuffle/scheme change?) — "
                        f"suppressed as one summary hit",
                provenance={
                    "method": "r.jina.ai reader GET of index page",
                    "index_url": index_url,
                    "new_slugs": sorted(new_slugs)[:20],
                    "retrieved_at": scanned_at,
                },
                extra={"source_id": source_id,
                       "suppressed": sorted(new_slugs)},
            ))
            continue
        for slug in new_slugs:
            key = f"intel_slot5:{source_id}:{slug}"
            if is_new(seen_ids, key):
                mark_seen(seen_ids, key)
                hits.append(_new_post_hit(
                    source_id, label, index_url, slug, inv[slug],
                    scanned_at))
        time.sleep(spacing)
    if dirty:
        _save_state(state)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Slot-5 intel watch (Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
