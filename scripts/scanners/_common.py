"""Shared helpers for the swarm-infra evidence-lane scanners.

Each scanner module follows the same contract:

    scan(since_hours=24, seen_ids=None, dry_run=False) -> list[dict]

Each hit dict carries: lane, observed_at, source_url, indicators_matched,
grade ("PRIMARY" for our direct observations, "SECONDARY" for others'
artifacts), provenance, confidence ("HIGH"/"MEDIUM"/"LOW").

Standing rule (BigSexyWarlock69): every IP recorded on a hit gets
classified via attach_ip_classification() -- cloud/known-host status
is a priority indicator.
"""
from __future__ import annotations

import base64
import binascii
import datetime
import json
import os
import re
import sys
import time
import urllib.parse

# ip_classifier.py lives in scripts/ (parent of scanners/).
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from ip_classifier import classify_ip  # noqa: E402

CONFIG_PATH = os.path.expanduser(
    "~/workspace/silent-locus/scripts/swarm-infra-config.json"
)
IP_CACHE_PATH = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/ip_asn_cache.json"
)
ERROR_LOG_PATH = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/error-log.jsonl"
)
USER_AGENT = "silent-locus-lane-scanner/1.0 (+hunt: chinese-amap-fleet)"

GRADE = "SECONDARY"


def report_error(module: str, error_type: str, message: str,
                 context: dict | None = None) -> None:
    """Structured error reporting for the self-modifier swarm.

    Appends a JSONL entry to state/error-log.jsonl. Entries are deduped
    by the self-modifier agent using traceback_hash. Call this wherever
    a scanner catches an exception or encounters a degraded state --
    a silent failure is worse than a logged one.

    Do NOT log secrets, credentials, or full request bodies here.
    Keep messages to error type + affected input identifier.
    """
    import hashlib
    import traceback as tb_mod

    # Hash the current traceback for dedup (empty if none active)
    tb_text = "".join(tb_mod.format_exc()) if sys.exc_info()[0] else ""
    tb_hash = hashlib.sha256(
        f"{module}:{error_type}:{tb_text[-500:]}".encode()
    ).hexdigest()[:16]

    entry = {
        "timestamp": utcnow_iso(),
        "module": module,
        "error_type": error_type,
        "message": str(message)[:500],
        "traceback_hash": tb_hash,
        "context": context or {},
    }
    try:
        os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
        with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        # Error logging must never crash the scanner
        print(f"[report_error] failed to write: {module}/{error_type}",
              file=sys.stderr)


def utcnow_iso() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def make_hit(
    *,
    lane: str,
    source_url: str,
    indicators_matched: list,
    confidence: str,
    summary: str,
    provenance: dict,
    observed_at: str | None = None,
    extra: dict | None = None,
    grade: str | None = None,
) -> dict:
    hit = {
        "lane": lane,
        "observed_at": observed_at or utcnow_iso(),
        "source_url": source_url,
        "indicators_matched": list(indicators_matched),
        "grade": grade or GRADE,
        "provenance": provenance,
        "confidence": confidence,
        "summary": summary,
    }
    if extra:
        hit.update(extra)
    return hit


def dedup_key(base: str) -> str:
    return base


def is_new(seen_ids, key: str) -> bool:
    if seen_ids is None:
        return True
    return key not in seen_ids


def mark_seen(seen_ids, key: str) -> None:
    if seen_ids is not None:
        seen_ids.add(key)


def attach_ip_classification(hit: dict, ip: str | None, config: dict) -> dict:
    """Standing rule (BigSexyWarlock69): every recorded IP gets classified.

    Attaches the classify_ip() result dict inline as hit["ip_classification"]
    and sets hit["priority"] = True for tier 1 (KNOWN_SWARM) and tier 2
    (CLOUD_SERVICE). No-op when ip is empty. A cloud IP in an unexpected
    place is signal: this function never filters, only flags.
    """
    if not ip:
        return hit
    try:
        cls = classify_ip(ip, config, IP_CACHE_PATH)
    except Exception as e:
        print(f"[ip_classify] {ip}: {type(e).__name__}: {e}",
              file=sys.stderr)
        return hit
    hit["ip_classification"] = cls
    if cls.get("tier") in (1, 2):
        hit["priority"] = True
    return hit


def normalize(text: str) -> list[str]:
    """Decode-then-score helper (cryptologist 2026-10-14).

    The fleet's tradecraft IS base64 program-packing; detectors that only
    inspect the wrapping never see the contents. This returns multiple
    decoded variants of the input so scanners can match indicators at
    every encoding layer.

    Returns [original, url-decoded, url-decoded-x2, base64-decoded...].
    Base64 candidates: runs of >=40 base64 chars (fleet payload minimum).
    Failures degrade to fewer variants, never crash.
    """
    variants = [text]
    # URL decode (once and twice -- double-encoding is common evasion)
    try:
        once = urllib.parse.unquote(text)
        if once != text:
            variants.append(once)
            twice = urllib.parse.unquote(once)
            if twice != once:
                variants.append(twice)
    except Exception:
        pass
    # Base64 decode: find long base64 runs, decode each
    try:
        for m in set(re.findall(r"[A-Za-z0-9+/=]{40,}", text)):
            # pad to multiple of 4
            padded = m + "=" * (-len(m) % 4)
            try:
                decoded = base64.b64decode(padded, validate=False).decode(
                    "utf-8", "replace")
                if decoded != m and len(decoded) >= 10:
                    variants.append(decoded)
            except (binascii.Error, ValueError):
                continue
    except Exception:
        pass
    # dedupe preserving order
    seen, out = set(), []
    for v in variants:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def parse_args(description: str):
    import argparse

    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--dry-run", action="store_true",
                    help="Query one page per pattern, print results, write nothing.")
    ap.add_argument("--since-hours", type=float, default=24,
                    help="Look-back window in hours (default: 24).")
    ap.add_argument("--json", action="store_true",
                    help="Print hits as JSON array.")
    return ap.parse_args()


def emit(hits: list, as_json: bool, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] would return {len(hits)} hits")
    if as_json or dry_run:
        print(json.dumps(hits, indent=2, ensure_ascii=False))
    else:
        for h in hits:
            print(f"[{h['confidence']}] {h['summary']}")
            print(f"    {h['source_url']}")
        print(f"\n{len(hits)} hits")
