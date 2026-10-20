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

    Hardening (adversarial 2026-10-14):
    - Message truncated to 500 chars; context bounded to 10 keys,
      each value truncated to 200 chars (prevents log-bloat attacks).
    - Values are coerced to str -- no nested objects that could carry
      attacker-controlled structures into the fixer's instruction surface.
    - Log rotates at 1000 entries (oldest dropped). Prevents disk-fill.
    - Do NOT log secrets, credentials, full request bodies, or raw
      attacker-influenced input. Log identifiers, not content.

    Note: the error log is an instruction surface for the self-modifier.
    Treat context values as untrusted. The self-modifier must not copy
    "suggested" values from error context into code without independent
    verification.
    """
    import hashlib
    import traceback as tb_mod

    MAX_LOG_ENTRIES = 1000

    # Hash the current traceback for dedup (empty if none active)
    tb_text = "".join(tb_mod.format_exc()) if sys.exc_info()[0] else ""
    tb_hash = hashlib.sha256(
        f"{module}:{error_type}:{tb_text[-500:]}".encode()
    ).hexdigest()[:16]

    # Bound and sanitize context (adversarial: unbounded context is
    # a log-bloat / instruction-injection surface)
    safe_context = {}
    if context:
        for k in list(context.keys())[:10]:
            try:
                v = str(context[k])[:200]
            except Exception:
                v = "<unprintable>"
            safe_context[str(k)[:50]] = v

    entry = {
        "timestamp": utcnow_iso(),
        "module": str(module)[:100],
        "error_type": str(error_type)[:100],
        "message": str(message)[:500],
        "traceback_hash": tb_hash,
        "context": safe_context,
    }
    try:
        os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
        # Rotate: keep last MAX_LOG_ENTRIES
        lines = []
        if os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
        lines.append(json.dumps(entry, ensure_ascii=False) + "\n")
        lines = lines[-MAX_LOG_ENTRIES:]
        tmp = ERROR_LOG_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(lines)
        os.rename(tmp, ERROR_LOG_PATH)
    except OSError:
        # Error logging must never crash the scanner -- but be LOUD
        # about it (adversarial: silent logging failure = blind spot)
        print(f"[report_error] FAILED to write: {module}/{error_type}",
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


# ---------------------------------------------------------------------------
# Credential redaction for scanner-emitted paths.
#
# redact_secrets() applies to hits, error-log context, summaries/dedup
# keys, and state files -- the four scanner-emitted paths. It NEVER
# applies to raw evidence captures: those keep full observed values with
# sensitivity annotated (2026-10-19 carve-out; see AGENTS.md evidence
# rules).
#
# Conservative pattern list (documented; false negatives acceptable,
# false positives on redaction are the safe direction):
#   - AWS access key IDs (AKIA...) and session keys (ASIA...)
#   - Anthropic keys (sk-ant-...)
#   - OpenAI-style keys (sk- + 20 alnum)
#   - GitHub tokens (ghp_/gho_/ghu_/ghs_/ghr_..., github_pat_...)
#   - Slack tokens (xoxb-/xoxp-/xoxa-/xoxo-/xoxr-/xoxs-...)
#   - Google API keys (AIza...)
#   - Bearer tokens ("Bearer <token>")
#   - NAMED-SECRET: a long hex/base64-ish value (16+ chars) adjacent to
#     a key-ish name (secret, password, api_key, aws_secret, token,
#     private_key, client_secret, ...), e.g.  password = "hunter2..."
#     or  "aws_secret_access_key": "wJalr...".
# Replacement markers are [REDACTED-<CLASS>]; they are designed not to
# re-match any pattern, so redaction is idempotent.
# ---------------------------------------------------------------------------
_SECRET_PATTERNS = [
    # (class name, compiled regex, mode)
    # mode "whole": the whole match is the secret -> replace it.
    # mode "group": named group "v" is the secret -> replace only it,
    #               keeping the surrounding label (e.g. "Bearer ").
    ("AWS-ACCESS-KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "whole"),
    ("AWS-SESSION-KEY", re.compile(r"\bASIA[0-9A-Z]{16}\b"), "whole"),
    ("ANTHROPIC-KEY",
     re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{8,}\b"), "whole"),
    ("OPENAI-KEY",
     re.compile(r"\bsk-(?!ant-)[A-Za-z0-9][A-Za-z0-9\-]{19,}\b"), "whole"),
    ("GITHUB-TOKEN",
     re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"
                r"|\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
     "whole"),
    ("SLACK-TOKEN",
     re.compile(r"\bxox[aboprs]-[A-Za-z0-9\-]{10,}\b"), "whole"),
    ("GOOGLE-API-KEY",
     re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"), "whole"),
    ("BEARER-TOKEN",
     re.compile(r"(?i)\bBearer\s+(?P<v>[A-Za-z0-9._~+/=\-]{10,})"),
     "group"),
    ("NAMED-SECRET",
     re.compile(
         r"(?i)\b(secret|secrets|password|passwd|pwd|pass"
         r"|api[_-]?key|access[_-]?key|auth[_-]?token"
         r"|bearer[_-]?token|private[_-]?key|client[_-]?secret"
         r"|aws[_-]?secret[_-]?access[_-]?key|aws[_-]?secret"
         r"|session[_-]?token|refresh[_-]?token"
         r"|token)\b\s*[\"']?\s*[:=]\s*[\"']?"
         r"(?P<v>[A-Za-z0-9/+=._~\-]{16,})"),
     "group"),
]

_REDACT_MARKER = "[REDACTED-{}]"


def secret_pattern_counts(text: str) -> dict:
    """Count credential-looking spans per pattern class (detection only).

    Layer-agnostic verdict: returns {class_name: match_count}. The
    matched strings are never returned or stored -- callers record
    counts only (counsel: never emit matched secret values or decoded
    variants). Pure function.
    """
    counts = {}
    for name, rx, _mode in _SECRET_PATTERNS:
        try:
            n = len(rx.findall(text))
        except Exception:
            n = 0
        if n:
            counts[name] = n
    return counts


def redact_secrets(text) -> tuple:
    """Redact credential-looking spans in scanner-emitted text.

    Returns (found: bool, redacted: str). found is True when at least
    one pattern matched. When nothing matches, redacted is the original
    string unchanged. Pure function; uses only `re` (already imported).
    Redaction is idempotent: markers never re-match a pattern.
    """
    if not isinstance(text, str):
        text = str(text)
    found = False
    out = text
    for name, rx, mode in _SECRET_PATTERNS:
        marker = _REDACT_MARKER.format(name)
        if mode == "whole":
            out, n = rx.subn(marker, out)
        else:
            def _rep(m, _mk=marker):
                whole = m.group(0)
                v = m.group("v")
                i = whole.find(v)
                return whole[:i] + _mk + whole[i + len(v):]
            out, n = rx.subn(_rep, out)
        if n:
            found = True
    return found, out


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
