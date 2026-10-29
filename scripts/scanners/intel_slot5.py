#!/usr/bin/env python3
"""Lane — slot-5 intel watch: new posts on swarmcha.se and norforge.com.

Automates the slot-5 manual flow: fetch the two intel sites' index
pages through the r.jina.ai reader (plain GET, polite rate), inventory
their posts, compare against a baseline state file, and emit
NEW-POST findings.

Sources:
  - https://swarmcha.se/posts   (Rowan Howard-Jones / swarmcha.se)
  - https://norforge.com/blog   (NorForge engineering blog)

Contract: scan(since_hours=24, seen_ids=None, dry_run=False) -> hits.
Hits carry the _common contract fields; grade SECONDARY (third-party
intel), confidence MEDIUM (public intel source, first-Party-checked
by the analyst lane on ingest).

State: scripts/scanners/state/intel_slot5.json maps
    {source_id: {slug: {"title":..., "date":..., "first_seen":...}}}
First run seeds the baseline and emits no hits (no novelty baseline
exists yet).

Politeness: 10 s spacing between index fetches (jina free tier),
60/120 s backoff on 429, then the source is skipped — never marked
seen, never baseline-updated, so the next run retries it.

Direct-fetch fallback (A67, 2026-10-24): when the jina reader fails
or returns truncated output for a source, scan() retries that source
with a plain GET of the index URL itself and inventories the direct
HTML the same way (slug keys). Titles from direct HTML are tag soup,
so a direct-only inventory NEVER seeds a fresh source's baseline —
it only diffs against an existing one. A direct fetch that also fails
or parses empty keeps the old baseline, same as before.

Adversarial review (2026-10-23, self-review before commit):
  - Empty/failed index fetch with a non-empty baseline -> skip the
    source with a note and report_error; NEVER treat "could not read
    the index" as "all posts deleted" (that direction would flood).
  - Zero posts parsed from a 200 response -> same skip path (jina
    sometimes returns an interstitial/error page as 200).
  - Truncation guard: _looks_truncated() skips partially-loaded
    reader output (unbalanced brackets in tail, missing jina
    header) instead of seeding/diffing against it. A truncated seed
    would manufacture false NEW-POST hits on the next full run; a
    skipped cycle is retried on the next run.
  - Flood guard: if a source shows more than MAX_NEW_POSTS new
    slugs in one run, emit ONE summary hit (inventory reshuffle /
    URL-scheme change) and mark them seen instead of N lead hits.
  - Slug keys are per-source; a title edit never re-fires (keyed on
    slug only).
  - Titles are attacker-influenced page text: truncated to 200 chars
    and passed through redact_secrets before entering a hit summary.
  - State file corrupt/non-dict -> treated as absent: re-seed
    silently, no hits (no alert flood on a broken baseline).
  - Jina content may be cached/stale: noted in provenance; "new"
    means new to our inventory, not necessarily published today.

Usage:
    intel_slot5.py [--dry-run] [--since-hours 24] [--json]
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
    USER_AGENT, make_hit, utcnow_iso, is_new, mark_seen, parse_args,
    emit, redact_secrets, report_error,
)

LANE = "intel-slot5"
STATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state", "intel_slot5.json")
JINA_BASE = "https://r.jina.ai/"
REQUEST_SPACING = 10   # seconds between index fetches (jina free-tier politeness)
RETRY_SLEEPS = (60, 120)
TIMEOUT = 60
MAX_TEXT = 500_000
MAX_NEW_POSTS = 8      # flood guard: above this, one summary hit
TITLE_LEN = 200

# (source_id, label, index_url, post-slug regex on absolute URLs)
SOURCES = [
    ("swarmcha", "swarmcha.se", "https://swarmcha.se/posts",
     re.compile(r"https://swarmcha\.se/posts/([A-Za-z0-9][A-Za-z0-9_-]*)")),
    ("norforge", "norforge.com", "https://norforge.com/blog",
     re.compile(r"https://norforge\.com/blog/([a-z0-9_-]{2,})(?:[?#]|$)")),
]

_MD_LINK_RE = re.compile(r"\[([^\]]{0,400})\]\((https?://[^)\s]{1,300})\)")
_URL_RE = re.compile(r"https?://[^\s)<>\"]{1,300}")
# swarmcha list items: "*   2026-10-14[Title](url)"; norforge: "OCT 2026"
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})|([A-Z]{3}\s+\d{4})")
_IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_MD_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_BULLET_RE = re.compile(r"^[\s*#>\-*+\d.()]+")
_TRAILING_PUNCT = ".,;:!?"


def _looks_truncated(text: str) -> bool:
    """Heuristic: did the reader return a partially-loaded page?

    Jina warns 'page maybe not yet fully loaded' and truncates
    mid-construct. Seeding or diffing against a truncated page would
    manufacture false NEW-POST hits on the next full run. Two
    cheap signals: (1) unbalanced markdown brackets in the tail
    (cut inside a link/image), (2) missing jina header block.
    Conservative: a false positive here costs one skipped cycle
    (retried next run); a false negative manufactures fake leads.
    """
    if "URL Source:" not in text[:800]:
        return True
    tail = text[-600:]
    return tail.count("[") > tail.count("]")


def _fetch_index(index_url: str, label: str) -> str | None:
    """GET the index page through the jina reader. None on failure."""
    url = JINA_BASE + index_url
    last = ""
    for attempt, sleep_s in enumerate([0] + list(RETRY_SLEEPS)):
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
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                raw = resp.read(MAX_TEXT + 1)
                return raw[:MAX_TEXT].decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 429:
                continue
            print(f"[intel_slot5] {label}: {last} (definitive)",
                  file=sys.stderr)
            return None
        except Exception as e:  # noqa: BLE001 -- transient, retried
            last = f"{type(e).__name__}: {e}"
            print(f"[intel_slot5] {label}: {last}", file=sys.stderr)
    print(f"[intel_slot5] {label}: giving up ({last})", file=sys.stderr)
    return None


def _fetch_direct(index_url: str, label: str) -> str | None:
    """Plain GET of the index URL itself (A67 fallback).

    Used only when the jina reader path failed or truncated. One
    attempt, no backoff: the next run retries jina first anyway.
    Returns None on any failure. Callers must NOT apply the jina
    truncation heuristic to this output (no jina header in direct
    HTML); emptiness is judged by parsed slug count instead.
    """
    req = urllib.request.Request(index_url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,text/plain",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read(MAX_TEXT + 1)
            return raw[:MAX_TEXT].decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 -- fallback, caller logs
        print(f"[intel_slot5] {label}: direct fetch failed: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return None


def _nearby_title(text: str, pos: int) -> str:
    """Title from the ~500 chars before the URL occurrence.

    Prefers the last '##' heading (norforge cards), else the last
    '[' link-text opener (swarmcha list items). Line-based
    extraction failed: norforge's index renders as one long line,
    so every card inherited the first card's title.
    """
    window = text[max(0, pos - 500):pos]
    window = _IMAGE_MD_RE.sub("", window)  # kill ![alt](src) cards first
    # the URL occurrence sits after its link opener: drop a trailing "]("
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
    """Parse {slug: {"title":..., "date":...}} from jina markdown.

    URL-occurrence scanning (not flat [text](url) matching) so nested
    image-links still parse. Date: nearest YYYY-MM-DD or MON YYYY
    within 80 chars before the URL; empty string when absent.
    Duplicated slugs keep the first occurrence.
    """
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
        summary=f"[intel_slot5] NEW POST on {label}: {title!r} "
                f"({date or 'undated'}) — {post_url}",
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
    """Inventory the two intel indexes; report slugs not in baseline."""
    if seen_ids is None:
        seen_ids = set()
    scanned_at = utcnow_iso()

    if dry_run:
        print("[dry-run] intel_slot5 plan:", file=sys.stderr)
        for _sid, label, index_url, _re in SOURCES:
            print(f"  WOULD GET: {JINA_BASE}{index_url}  ({label})",
                  file=sys.stderr)
        print(f"  state: {STATE_PATH} (no writes in dry-run)",
              file=sys.stderr)
        return []

    state = _load_state()
    hits = []
    dirty = False
    for source_id, label, index_url, slug_re in SOURCES:
        fresh = source_id not in state
        baseline = state.setdefault(source_id, {})
        text = _fetch_index(index_url, label)
        via_direct = False
        if text is None or _looks_truncated(text):
            # Jina path degraded (both sources failed 3 straight
            # slot-5 runs, 2026-10-24): fall back to a plain GET of
            # the index itself. The jina truncation heuristic does
            # not apply to direct HTML (no jina header), so a direct
            # inventory is accepted on slug count alone; empty still
            # means skip, never "all gone".
            reason = ("fetch_failed" if text is None
                      else "possibly_truncated")
            print(f"[intel_slot5] {label}: jina {reason}, trying "
                  f"direct fetch", file=sys.stderr)
            direct = _fetch_direct(index_url, label)
            direct_inv = _inventory(direct, slug_re) \
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
        inv = _inventory(text, slug_re)
        if not inv:
            # 200 with zero parseable posts: degraded, not "all gone".
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
            # Direct HTML titles are tag soup and the inventory is
            # unvalidated against the reader: never seed a baseline
            # from a fallback-only read. Keep the source unseeded;
            # the next run retries jina first.
            print(f"[intel_slot5] {label}: direct-only inventory, "
                  f"not seeding baseline", file=sys.stderr)
            report_error("intel_slot5", "direct_fallback_no_seed",
                         f"{label}: fresh source, direct-only "
                         f"inventory not seeded",
                         {"index_url": index_url})
            state.pop(source_id, None)
            continue
        if fresh:
            # First sighting: this inventory IS the novelty baseline.
            # Seed silently — everything is "new" only because we
            # never looked before.
            for slug in inv:
                mark_seen(seen_ids, f"intel_slot5:{source_id}:{slug}")
            print(f"[intel_slot5] {label}: baseline seeded "
                  f"({len(inv)} posts, 0 hits)", file=sys.stderr)
            continue
        if not new_slugs:
            continue
        if len(new_slugs) > MAX_NEW_POSTS:
            # Flood guard: inventory reshuffle, not N leads.
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
        # polite spacing between source fetches
        time.sleep(REQUEST_SPACING)
    if dirty:
        _save_state(state)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Slot-5 intel watch: new posts on swarmcha.se / "
                      "norforge.com")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
