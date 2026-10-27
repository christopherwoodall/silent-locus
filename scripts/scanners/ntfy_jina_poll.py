#!/usr/bin/env python3
"""Standalone ntfy dead-drop poll via the r.jina.ai relay.

Polls the configured ntfy.sh topic(s) through the working jina route
(verified 2026-10-17):
    https://r.jina.ai/https://ntfy.sh/<topic>/json?since=all

Direct ntfy.sh access is blocked at egress; ?poll=1 fails through jina
(422 long-poll). ?since=all returns the retained (~12h) window
immediately as newline-delimited JSON.

This is the recurring-poll script for the dead-drop watch (BigSexyWarlock69
2026-10-22: "setup the reoccurring route poll"). It is intentionally
narrow: poll known topics, score against the lane's content rules,
report hits. Full lane logic (CDX discovery, orchestrator wiring)
lives in ntfy.py.

State: tracks seen message IDs in
    scripts/scanners/state/ntfy_jina_poll_seen.json
so recurring runs only report NEW messages.

Usage:
    ntfy_jina_poll.py [--json] [--dry-run]
Exit codes: 0 = clean (no new hits), 1 = hits found, 2 = transport error.
"""

from __future__ import annotations

import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import ntfy as NTFY  # content rules + scoring + hit builder

STATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state",
    "ntfy_jina_poll_seen.json")
TIMEOUT = 45


def _load_seen() -> tuple:
    """Return (seen_set, load_ok). load_ok is False when the state file
    was missing or unparseable (e.g. a transient overlay read failure),
    in which case the caller must not let _save_seen shrink the state."""
    try:
        with open(STATE_PATH) as f:
            return set(json.load(f)), True
    except (OSError, json.JSONDecodeError):
        return set(), False


def _save_seen(seen: set, allow_empty: bool = False) -> None:
    """Persist the seen set.

    Safety rules (A36): (1) write the current on-disk state to a .bak
    before every overwrite; (2) refuse to persist an empty set over a
    previously non-empty state unless allow_empty is True, i.e. the poll
    both loaded the prior state OK and enumerated every topic
    successfully with zero new messages. A transient read failure must
    never silently destroy the dedup state."""
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    prev_len = 0
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH) as f:
                prev_len = len(json.load(f))
            # last-good backup before every overwrite
            bak = STATE_PATH + ".bak"
            with open(STATE_PATH, "rb") as sf, open(bak, "wb") as df:
                df.write(sf.read())
        except (OSError, json.JSONDecodeError):
            pass
    if prev_len > 0 and len(seen) == 0 and not allow_empty:
        # Silent-wipe guard: keep the prior state on disk.
        return
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(sorted(seen), f)
    os.rename(tmp, STATE_PATH)


def _fetch_via_jina(topic: str, retries: int = 2):
    """GET the topic's retained messages through jina. Returns
    (ok, list_of_msgs) or (False, error_string). Retries transient
    connection drops (jina occasionally resets)."""
    inner = ("https://ntfy.sh/"
             + urllib.parse.quote(topic, safe='') + "/json?since=all")
    url = "https://r.jina.ai/" + inner
    last_err = ""
    for attempt in range(retries + 1):
        req = urllib.request.Request(url,
                                     headers={"User-Agent": C.USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                body = resp.read().decode("utf-8", "replace")
            break
        except Exception as e:  # noqa: BLE001 -- retry, then exit 2
            last_err = str(e)
            if attempt < retries:
                import time
                time.sleep(5)
    else:
        return False, last_err
    msgs = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msgs.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return True, msgs


def poll(dry_run: bool = False):
    """Poll all configured topics. Returns (hits, notes)."""
    config = C.load_config()
    topics = config.get("ntfy_topics", [])
    scanned_at = C.utcnow_iso()
    hits, notes = [], []

    if dry_run:
        print("[dry-run] ntfy jina poll plan")
        for t in topics:
            print(f"  WOULD GET: https://r.jina.ai/https://ntfy.sh/{t}"
                  f"/json?since=all")
        print(f"  state: {STATE_PATH}")
        print(f"  content rules: {[n for n, _ in NTFY.CONTENT_RULES]}")
        return hits, notes

    seen, loaded_ok = _load_seen()
    all_topics_ok = True
    for topic in topics:
        ok, payload = _fetch_via_jina(topic)
        if not ok:
            all_topics_ok = False
            notes.append(f"{topic}: TRANSPORT ERROR: {payload[:120]}")
            continue
        # Drop stream markers ("open" events carry no content; the topic
        # name itself matches content rules, so scoring it is noise).
        real = [m for m in payload if m.get("event") != "open"]
        if not real:
            notes.append(f"{topic}: empty (no messages in ~12h window)")
            continue
        notes.append(f"{topic}: {len(real)} message(s) in window")
        for msg in real:
            mid = str(msg.get("id", "?"))
            key = f"ntfy-jina:{topic}:{mid}"
            # Known fleet topic: any real message here is signal by
            # itself. Content rules classify, they don't gate.
            matched = NTFY._score_message(msg) or ["known_fleet_topic"]
            if key in seen:
                continue
            seen.add(key)
            hits.append(NTFY._make_hit(
                topic, msg, matched,
                "r.jina.ai relay (?since=all), recurring poll",
                scanned_at, config))
    _save_seen(seen, allow_empty=(loaded_ok and all_topics_ok))
    return hits, notes


def main() -> int:
    args = C.parse_args("ntfy jina recurring poll")
    hits, notes = poll(dry_run=args.dry_run)
    for n in notes:
        print(f"  {n}", file=sys.stderr)
    if args.json:
        print(json.dumps(
            [{"topic": h["extra"]["topic"],
              "message_id": h["extra"]["message_id"],
              "matched": h["indicators_matched"],
              "summary": h["summary"]} for h in hits], indent=2))
    else:
        for h in hits:
            print(f"HIT: {h['summary']}")
    if any("TRANSPORT ERROR" in n for n in notes):
        return 2
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
