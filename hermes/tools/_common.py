"""Shared helpers for the Hermes hunt-profile scanners.

Standalone port. No silent-locus import. No factum.db. No repo state.

Each scanner module follows the same contract:

    scan(since_hours=24, seen_ids=None, dry_run=False) -> list[dict]

Each hit dict carries: lane, observed_at, source_url,
indicators_matched, grade, provenance, confidence
("HIGH" / "MEDIUM" / "LOW").

Terms, defined on first use:
- PRIMARY: a grade. It means we observed the bytes ourselves.
- SECONDARY: a grade. It means the bytes came from someone else.
  Example: another person's scan record, or a third-party report.
- Provenance triple: three files for one capture. The data file,
  a .PROVENANCE.txt file, and a .sha256 file. The triple proves
  what was seen, where it came from, and that it did not change.

Paths resolve from this file, not from the working directory:
- config: tools/config.json (next to this file)
- captures: hermes/workspace/raw/
- state: hermes/workspace/state/

Rules:
- Read-only, passive scans only. GET only. No POST. No login.
  No new session. No new account. No paid upgrade and no
  account creation; keyed APIs use only operator-supplied keys
  and consume operator plan quota.
- No secret value lives in code or config. Config holds only
  env-var names, in the form "${NAME}". Use resolve_env() to read
  the value at run time. Never print it. Never write it to a file.
- Scope is agents and agent infrastructure only. Never pursue
  human or operator identity.
- Redaction applies to emitted summaries and displayed text
  only. Capture files keep full observed values. State files
  may contain public titles. Credential material never belongs
  in emitted text or in state files.
"""
from __future__ import annotations

import copy
import hashlib
import ipaddress
import json
import os
import re
import sys
import time

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.dirname(TOOLS_DIR)
CONFIG_PATH = os.path.join(TOOLS_DIR, "config.json")
WORKSPACE_DIR = os.path.join(PROFILE_DIR, "workspace")
RAW_DIR = os.path.join(WORKSPACE_DIR, "raw")
STATE_DIR = os.path.join(WORKSPACE_DIR, "state")
ERROR_LOG_PATH = os.path.join(STATE_DIR, "error-log.jsonl")
USER_AGENT = "hermes-hunt-scanner/1.0"

GRADE = "SECONDARY"


def utcnow_iso() -> str:
    import datetime
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def load_config() -> dict:
    """Read tools/config.json. Path is relative to this file."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def scanner_config(name: str) -> dict:
    """One scanner block from config.json. Empty dict when absent."""
    cfg = load_config()
    block = cfg.get("scanners", {}).get(name, {})
    return block if isinstance(block, dict) else {}


def scanner_enabled(name: str) -> bool:
    """True only when the scanner block says enabled:true.

    All scanners ship disabled. Enabling one needs the operator's
    word. This check happens before any network call.
    """
    return scanner_config(name).get("enabled", False) is True


def resolve_env(value):
    """Resolve a "${NAME}" env-var name to its value.

    Returns None when the value is absent, when it is not a
    "${NAME}" reference, or when the env var is unset. Callers
    must treat None as "no key, skip the call". Never log the
    returned value.
    """
    if not isinstance(value, str):
        return None
    m = re.fullmatch(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", value.strip())
    if not m:
        return None
    return os.environ.get(m.group(1))


def report_error(module: str, error_type: str, message: str,
                 context: dict | None = None) -> None:
    """Append one bounded JSONL entry to state/error-log.jsonl.

    Message is cut to 500 chars. Context is cut to 10 keys, each
    value cut to 200 chars. The log holds 1000 entries at most.
    Do not log secrets, full request bodies, or raw input.
    A logging failure never crashes the scanner.
    """
    import traceback as tb_mod

    tb_text = "".join(tb_mod.format_exc()) if sys.exc_info()[0] else ""
    tb_hash = hashlib.sha256(
        f"{module}:{error_type}:{tb_text[-500:]}".encode()
    ).hexdigest()[:16]
    safe_context = {}
    if context:
        for k in list(context.keys())[:10]:
            try:
                v = str(context[k])[:200]
            except Exception:
                v = "<unprintable>"
            _, v = redact_secrets(v)
            safe_context[str(k)[:50]] = v
    _, safe_message = redact_secrets(str(message)[:500])
    entry = {
        "timestamp": utcnow_iso(),
        "module": str(module)[:100],
        "error_type": str(error_type)[:100],
        "message": safe_message,
        "traceback_hash": tb_hash,
        "context": safe_context,
    }
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        lines = []
        if os.path.exists(ERROR_LOG_PATH):
            with open(ERROR_LOG_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
        lines.append(json.dumps(entry, ensure_ascii=False) + "\n")
        lines = lines[-1000:]
        tmp = ERROR_LOG_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.writelines(lines)
        os.rename(tmp, ERROR_LOG_PATH)
    except OSError:
        print(f"[report_error] FAILED to write: {module}/{error_type}",
              file=sys.stderr)


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


def classify_ip(ip: str, config: dict) -> dict:
    """Classify one IP against the profile config.

    Tier 1: exact match on known_swarm_ips (operator-supplied
    watchlist). An exact match is a watch flag only, never
    attribution: it sets swarm_linked_candidate, never a bare
    swarm-linked claim. Any attribution use needs a provenance
    record and Counsel clearance.
    Tier 2: match on a watchlist CIDR (cloud range, watch only).
    Tier 4: unknown / ordinary internet.
    This port has no live ASN lookup. A tier-2 flag is a watch
    flag, never attribution. ASN-based tiers from the source
    classifier are not reproduced here.
    """
    out = {"ip": ip, "tier": 4, "label": "UNKNOWN", "detail": "",
           "asn": None, "org": None, "country": None, "city": None,
           "swarm_linked_candidate": False}
    if not ip:
        return out
    try:
        block = config.get("ip_classification", {})
        if ip in (block.get("known_swarm_ips") or []):
            out.update({"tier": 1, "label": "KNOWN_SWARM",
                        "detail": "exact match on known fleet IP "
                                  "list — watch flag only, not "
                                  "attribution; Counsel clearance "
                                  "required before any attribution use",
                        "swarm_linked_candidate": True})
            return out
        addr = ipaddress.ip_address(ip)
        for cidr in block.get("watchlist_cidrs") or []:
            try:
                if addr in ipaddress.ip_network(cidr, strict=False):
                    out.update({"tier": 2, "label": "CLOUD_SERVICE",
                                "detail": f"inside watchlist {cidr}"})
                    return out
            except ValueError:
                continue
    except ValueError:
        out["detail"] = "not a valid IP literal"
    return out


def attach_ip_classification(hit: dict, ip: str | None,
                             config: dict) -> dict:
    """Standing rule: every recorded IP gets classified.

    Sets hit["priority"] = True for tier 1 and tier 2. Never
    filters. A cloud IP in an odd place is signal, not proof.
    """
    if not ip:
        return hit
    try:
        cls = classify_ip(ip, config)
    except Exception as e:
        print(f"[ip_classify] {ip}: {type(e).__name__}: {e}",
              file=sys.stderr)
        return hit
    hit["ip_classification"] = cls
    if cls.get("tier") in (1, 2):
        hit["priority"] = True
    return hit


# --- Credential redaction for scanner-emitted text only. ---
# Raw evidence captures keep full observed values. Redaction
# applies only to hit summaries, error context, and state text.
_SECRET_PATTERNS = [
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
    """Count credential-like spans per class. Values never returned."""
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
    """Redact credential-like spans. Returns (found, redacted)."""
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


def write_capture(scanner: str, stem: str, payload: bytes,
                  source_url: str, method: str,
                  subdir: str | None = None) -> str | None:
    """Write a provenance triple into workspace/raw/<scanner>/.

    Files: <stem>.json, <stem>.PROVENANCE.txt, <stem>.sha256.
    All three files are written via tmp+rename. After the
    writes, the data file is re-read and its sha256 is verified
    against the digest before the path is returned. A failed
    verification returns None. Returns the data-file path, or
    None on failure. Never raises. This is the single capture
    implementation; callers must use it, not a second writer.
    """
    try:
        safe = re.sub(r"[^A-Za-z0-9_.\-]", "_", stem)
        outdir = os.path.join(RAW_DIR, scanner)
        if subdir:
            outdir = os.path.join(outdir, subdir)
        os.makedirs(outdir, exist_ok=True)
        base = os.path.join(outdir, safe)
        digest = hashlib.sha256(payload).hexdigest()
        tmp = base + ".json.tmp"
        with open(tmp, "wb") as fh:
            fh.write(payload)
        os.rename(tmp, base + ".json")
        tmp = base + ".sha256.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(digest + "\n")
        os.rename(tmp, base + ".sha256")
        tmp = base + ".PROVENANCE.txt.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(f"source URL: {source_url}\n")
            fh.write(f"retrieval time: {utcnow_iso()}\n")
            fh.write(f"method: {method}\n")
            fh.write(f"sha256: {digest}\n")
        os.rename(tmp, base + ".PROVENANCE.txt")
        with open(base + ".json", "rb") as fh:
            actual = hashlib.sha256(fh.read()).hexdigest()
        if actual != digest:
            report_error(scanner, "capture_verify_failed",
                         "re-read sha256 does not match digest")
            return None
        return base + ".json"
    except OSError as e:
        report_error(scanner, "capture_failed", str(e))
        return None


def parse_args(description: str):
    import argparse

    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the scan plan only; zero network "
                         "calls, zero writes.")
    ap.add_argument("--since-hours", type=float, default=24,
                    help="Look-back window in hours (default: 24).")
    ap.add_argument("--json", action="store_true",
                    help="Print hits as JSON array.")
    return ap.parse_args()


def _redact_hit_for_display(hit: dict) -> dict:
    """Return a display copy with credential-like spans redacted.

    Redacts summary strings and URL-bearing fields only.
    Capture files are untouched: this copy is for display.
    """
    shown = copy.deepcopy(hit)

    def _walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and (
                        k == "summary" or "url" in k.lower()):
                    _, node[k] = redact_secrets(v)
                else:
                    _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(shown)
    return shown


def emit(hits: list, as_json: bool, dry_run: bool) -> None:
    shown = [_redact_hit_for_display(h) for h in hits]
    if dry_run:
        print(f"[dry-run] would return {len(shown)} hits")
    if as_json or dry_run:
        print(json.dumps(shown, indent=2, ensure_ascii=False))
    else:
        for h in shown:
            print(f"[{h['confidence']}] {h['summary']}")
            print(f"    {h['source_url']}")
        print(f"\n{len(shown)} hits")


def sleep_guarded(seconds: float) -> None:
    """Sleep, but never below zero. Rate-limit spacing helper."""
    if seconds and seconds > 0:
        time.sleep(seconds)
