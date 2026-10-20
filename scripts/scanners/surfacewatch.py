#!/usr/bin/env python3
"""Lane 13 — surfacewatch: content-hash change detection on public agent-infrastructure surfaces.

An agent-surface is a public page or file that agents can read or write
(for example a community llms.txt, a message board, or a registry API).
This module watches 13 hardcoded agent-surfaces for content changes.
A hash change means "the content hash changed at <url>". It never
means "agent activity". A hash-only change is not evidence that an
agent did anything.

Counsel verdict 2026-10-20: GO-WITH-CHANGES. Binding constraints:

- S1: targets are HARDCODED as a frozenset in this module source. They
  are not config-soft, there is no --targets override, and there is no
  target discovery. New targets need counsel review + operator word.
- S2: per-target fetch contracts. GET only. No CookieJar, no auth
  headers. Content-type is validated before hashing. Redirects are NOT
  chased: a 3xx response or a final-URL mismatch is a degraded state,
  recorded via report_error, never a hit. Streaming reads cap at 2MB
  per target. Per-run byte budget is ~10MB with abort on exceed. At
  least 2s spacing between requests (this module uses 10s, the same
  as jina.py on free tiers). 30s timeout. Max 1 retry. HTTP 429 is a
  hard stop for that target for the run (no retry).
- S3: normalized-extraction hashing. Volatile boilerplate is stripped
  per a documented per-target volatile-token policy (see
  TARGET_CONTRACTS and _canonicalize()). The canonical form is hashed
  with SHA-256. Raw byte-length and raw SHA-256 are also recorded in
  provenance for forensics (dual layer). A hash-only change is
  PRIMARY-observed with MEDIUM confidence at most. _common.normalize()
  is not used for emission; no decoded variants and no page text are
  ever emitted in hits, summaries, or state.
- S4: per-target gap semantics. A failed or missing fetch is a GAP. A
  gap is never a hit, never a clean negative, and never silently
  re-baselines state. Consecutive gaps are tracked per target; an
  alert (via report_error) fires only after GAP_ALERT_N (3)
  consecutive gaps. Documented in FALSE-POSITIVES-surfacewatch.md.
- S5: infrastructure surfaces only. These are public pages. The module
  performs no interaction, no form submission, no login.

Hits carry identifiers only: target URL, hash pair (old -> new),
observed_at. Never page bytes, titles, or decoded variants. The
summary template is "content hash changed at <url>".

Indicator names describe observed events only: `surface.content_changed`.
No "malicious", no undefined terms. The artifact type is named per hit:
"file" (llms.txt / skill.md / mcp.json), "api-response" (/api/canon),
or "page".

redact_secrets() (from _common) is applied on all four output paths:
hits, error-log context, summaries/dedup keys, and state files.
Error context carries identifiers only, never content.

USER_AGENT OPSEC tradeoff: this module uses the shared
_common.USER_AGENT ("silent-locus-lane-scanner/1.0 (+hunt:
chinese-amap-fleet)"). A static UA is fingerprintable: any of the 13
target operators can see that the same scanner fetched their page.
This is a known standing tradeoff, accepted by the operator. Do NOT
rotate or randomize the UA silently — changing the fingerprint we
present can look like evasion, and a rotation is an operator/counsel
decision, not a module-level one.

IP-classification note (standing rule): surfacewatch fetches carry no
IP addresses in hits (only the target URL and hashes), so no
ip_classification is attached. If an IP field is ever added to these
hits, it must be classified via _common.attach_ip_classification
before this module ships.

State: state/surfacewatch/state.json. Hashes and projections only,
never page bytes or titles. Version-stamped. A corrupt state file is
quarantined (moved to state/surfacewatch/quarantine/) and the module
re-baselines with zero hits. Writes go through a unique tmp name plus
atomic rename.

Disabled by default: the "surfacewatch" block in
swarm-infra-config.json carries "enabled": false. A live scan refuses
to run unless it is enabled. --dry-run performs ZERO network calls.

Usage:
    surfacewatch.py [--dry-run] [--since-hours 24] [--json]

since_hours is accepted for contract compliance; newness is
determined by hash change against stored state, not by a time window.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit, report_error, redact_secrets,
)

LANE = "surfacewatch"
INDICATOR_CHANGED = "surface.content_changed"

STATE_DIR = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/surfacewatch")
STATE_PATH = os.path.join(STATE_DIR, "state.json")
QUARANTINE_DIR = os.path.join(STATE_DIR, "quarantine")
STATE_VERSION = 1

# S1: hardcoded target set, frozen at build. Full https:// URLs.
# Not config-soft. No --targets override. No discovery.
TARGETS = frozenset({
    "https://rel-ochre.vercel.app/api/canon",
    "https://room.trydemigod.com",
    "https://inference.dahl.global",
    "https://extract.paypercall.dev",
    "https://agenttavern.dev",
    "https://public-agents.com",
    "https://agentsboard.org/llms.txt",
    "https://agents-agents-agents.com/llms.txt",
    "https://bboard.ai/llms.txt",
    "https://agentgateway.pythonanywhere.com/mcp.json",
    "https://tantive.space/skill.md",
    "https://swarmmemo.com",
    "https://messageboardforaiagents.com",
})

# Per-target fetch + canonicalization contracts (S2/S3).
# "canon" selects the volatile-token policy in _canonicalize().
# The "volatile" note documents WHAT is stripped and WHY.
TARGET_CONTRACTS = {
    "https://rel-ochre.vercel.app/api/canon": {
        "artifact_type": "api-response",
        "artifact_kind": "canon-json",
        "content_types": ("application/json",),
        "canon": "json-envelope",
        "volatile": (
            "JSON envelope keys dropped recursively: updated_at, updated, "
            "timestamp, ts, _ts, nonce, buildId, build_id, etag, "
            "last_modified, generated_at, fetched_at, request_id, "
            "trace_id. Keys sorted for canonical form. WHY: API wrappers "
            "stamp volatile envelope fields around stable canon data; an "
            "envelope-only change is not a content change."),
    },
    "https://agentgateway.pythonanywhere.com/mcp.json": {
        "artifact_type": "file",
        "artifact_kind": "mcp.json",
        "content_types": ("application/json",),
        "canon": "json-envelope",
        "volatile": (
            "Same JSON-envelope policy as /api/canon. WHY: MCP registry "
            "files are re-serialized on deploy; key order and envelope "
            "timestamps churn without changing the registry content."),
    },
    "https://agentsboard.org/llms.txt": {
        "artifact_type": "file",
        "artifact_kind": "llms.txt",
        "content_types": ("text/plain", "text/markdown"),
        "canon": "text-doc",
        "volatile": (
            "CRLF normalized, trailing whitespace stripped, 'Last "
            "updated / Updated / Date / Generated' header lines replaced, "
            "ISO timestamps replaced. WHY: llms.txt maintainers bump the "
            "date header on regeneration; a date-only bump is not a "
            "content change."),
    },
    "https://agents-agents-agents.com/llms.txt": {
        "artifact_type": "file",
        "artifact_kind": "llms.txt",
        "content_types": ("text/plain", "text/markdown"),
        "canon": "text-doc",
        "volatile": (
            "Same text-doc policy as agentsboard.org/llms.txt. WHY: same "
            "date-header regeneration churn."),
    },
    "https://bboard.ai/llms.txt": {
        "artifact_type": "file",
        "artifact_kind": "llms.txt",
        "content_types": ("text/plain", "text/markdown"),
        "canon": "text-doc",
        "volatile": (
            "Same text-doc policy as agentsboard.org/llms.txt. WHY: same "
            "date-header regeneration churn."),
    },
    "https://tantive.space/skill.md": {
        "artifact_type": "file",
        "artifact_kind": "skill.md",
        "content_types": ("text/plain", "text/markdown"),
        "canon": "text-doc",
        "volatile": (
            "Same text-doc policy as the llms.txt files. WHY: skill files "
            "carry version/date headers that maintainers bump without "
            "changing the skill body."),
    },
    "https://room.trydemigod.com": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "ISO-8601 timestamps, datetime= attributes, cache-buster query "
            "params (?v/?t/?build/?cb=), buildId fields, /_next/static/ "
            "hashes, HTML comments replaced. WHY: deployments rotate "
            "build IDs and cache busters on every deploy without changing "
            "agent-visible content."),
    },
    "https://inference.dahl.global": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "Same html policy as room.trydemigod.com. WHY: same "
            "deployment-rotated build identifiers."),
    },
    "https://extract.paypercall.dev": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "Same html policy as room.trydemigod.com. WHY: same "
            "deployment-rotated build identifiers."),
    },
    "https://agenttavern.dev": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "Same html policy as room.trydemigod.com. WHY: same "
            "deployment-rotated build identifiers."),
    },
    "https://public-agents.com": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "Same html policy as room.trydemigod.com. WHY: same "
            "deployment-rotated build identifiers."),
    },
    "https://swarmmemo.com": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "Same html policy as room.trydemigod.com. WHY: same "
            "deployment-rotated build identifiers."),
    },
    "https://messageboardforaiagents.com": {
        "artifact_type": "page",
        "artifact_kind": "html-page",
        "content_types": ("text/html",),
        "canon": "html",
        "volatile": (
            "Same html policy as room.trydemigod.com. WHY: same "
            "deployment-rotated build identifiers."),
    },
}

# S2 fetch contract constants
REQUEST_SPACING = 10      # seconds between requests (>=2s required)
TIMEOUT = 30              # seconds per request
MAX_RETRIES = 1           # max 1 retry (2 attempts total)
MAX_BODY = 2_000_000      # streaming cap per target (2MB)
RUN_BUDGET = 10_000_000   # ~10MB per-run byte budget, abort on exceed
CHUNK = 64 * 1024

# S4 gap semantics: alert after this many consecutive gaps
GAP_ALERT_N = 3

# Volatile-token patterns (S3). Applied per the target's "canon" policy.
_ISO_TS_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?")
_DATETIME_ATTR_RE = re.compile(r'datetime="[^"]*"')
_CACHEBUSTER_RE = re.compile(r"([?&](?:v|t|build|cb|_v)=)[0-9A-Za-z._~-]+")
_BUILDID_RE = re.compile(r'("buildId"\s*:\s*")[^"]*(")')
_NEXT_STATIC_RE = re.compile(r"/_next/static/[A-Za-z0-9_.-]+/")
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_TS_LINE_RE = re.compile(
    r"(?im)^\s*(?:last[- ]updated|updated|date|generated)\s*[:\-].*$")
_JSON_VOLATILE_KEYS = {
    "updated_at", "updated", "timestamp", "ts", "_ts", "nonce",
    "buildid", "build_id", "etag", "last_modified", "generated_at",
    "fetched_at", "request_id", "trace_id", "requestid",
}

# Bot-detection / challenge page markers (HTML targets). A body that
# matches is treated as DEGRADED (a gap), not a hash input: bot walls
# vary by request, and hashing them would manufacture false changes.
_BOTWALL_MARKERS = (
    "cf-challenge", "just a moment", "attention required", "cf_chl",
    "__cf_bm", "cf-please-wait",
)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirect handler that refuses to chase (S2).

    Returning None from redirect_request makes urllib return the 3xx
    response as-is instead of following it. The caller then treats a
    non-200 status as a degraded state.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _make_opener() -> urllib.request.OpenerDirector:
    # Explicit handler list: no HTTPCookieProcessor (no CookieJar),
    # redirect handler replaced by _NoRedirect. ProxyHandler() with no
    # args honors the environment proxy settings (same as jina.py).
    return urllib.request.build_opener(
        urllib.request.ProxyHandler(),
        urllib.request.UnknownHandler(),
        urllib.request.HTTPHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        _NoRedirect(),
        urllib.request.HTTPErrorProcessor(),
    )


_OPENER = _make_opener()


def _scrub_strings(obj):
    """Apply redact_secrets() to every string in a structure (S: 4 paths)."""
    if isinstance(obj, str):
        _, redacted = redact_secrets(obj)
        return redacted
    if isinstance(obj, dict):
        return {k: _scrub_strings(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_scrub_strings(v) for v in obj]
    return obj


def _report(error_type: str, message: str, context: dict | None = None):
    """report_error wrapper: redact_secrets on message + context.

    Context carries identifiers only (URL, reason, status) — never
    response bytes, titles, or decoded variants.
    """
    ctx = {}
    if context:
        for k, v in context.items():
            _, rv = redact_secrets(str(v))
            ctx[str(k)] = rv
    _, msg = redact_secrets(str(message))
    report_error("surfacewatch", error_type, msg, ctx)


# ---------------------------------------------------------------------------
# Fetch (S2)
# ---------------------------------------------------------------------------

def _read_capped(resp) -> tuple[bytes, bool]:
    """Stream the body, cap at MAX_BODY. Returns (bytes, truncated)."""
    buf = bytearray()
    truncated = False
    while True:
        chunk = resp.read(CHUNK)
        if not chunk:
            break
        buf += chunk
        if len(buf) > MAX_BODY:
            truncated = True
            break
    return bytes(buf[:MAX_BODY]), truncated


def _fetch(url: str, contract: dict) -> dict:
    """GET url per the S2 fetch contract.

    Returns {"ok": True, "raw": bytes, "content_type": str,
             "truncated": bool}
    or {"ok": False, "reason": <identifier>, "detail": <identifier>}.
    Reasons: redirect, url_mismatch, content_type, botwall,
             http_429, http_error, transport, json_shape.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/json,text/plain,*/*;q=0.8",
    })
    attempts = 0
    while True:
        attempts += 1
        try:
            resp = _OPENER.open(req, timeout=TIMEOUT)
            status = resp.status
            if status == 429:
                # Hard stop for this target for the run. No retry.
                return {"ok": False, "reason": "http_429",
                        "detail": "rate limited; hard stop for this run"}
            if status != 200:
                return {"ok": False,
                        "reason": "redirect" if 300 <= status < 400
                        else "http_error",
                        "detail": f"http status {status}"}
            if resp.geturl() != url:
                return {"ok": False, "reason": "url_mismatch",
                        "detail": "final URL differs from request URL"}
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0]
            ctype = ctype.strip().lower()
            if ctype not in contract["content_types"]:
                return {"ok": False, "reason": "content_type",
                        "detail": f"unexpected content-type {ctype!r}"}
            raw, truncated = _read_capped(resp)
            return {"ok": True, "raw": raw, "content_type": ctype,
                    "truncated": truncated}
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return {"ok": False, "reason": "http_429",
                        "detail": "rate limited; hard stop for this run"}
            if 300 <= e.code < 400:
                # Redirect surfaced as an error (our redirect handler
                # refuses to chase): degraded, never a hit.
                return {"ok": False, "reason": "redirect",
                        "detail": f"http status {e.code} (not chased)"}
            if e.code in (401, 403, 404):
                return {"ok": False, "reason": "http_error",
                        "detail": f"http status {e.code} (not retryable)"}
            if attempts <= MAX_RETRIES:
                continue
            return {"ok": False, "reason": "http_error",
                    "detail": f"http status {e.code} after retry"}
        except Exception as e:
            # Transport errors, timeouts: max 1 retry, then gap.
            if attempts <= MAX_RETRIES:
                continue
            return {"ok": False, "reason": "transport",
                    "detail": f"{type(e).__name__}"}


# ---------------------------------------------------------------------------
# Canonicalization (S3)
# ---------------------------------------------------------------------------

def _drop_volatile_keys(obj):
    """Recursively drop volatile JSON envelope keys (case-insensitive)."""
    if isinstance(obj, dict):
        return {k: _drop_volatile_keys(v) for k, v in obj.items()
                if k.lower() not in _JSON_VOLATILE_KEYS}
    if isinstance(obj, list):
        return [_drop_volatile_keys(v) for v in obj]
    return obj


def _canonicalize(raw: bytes, contract: dict) -> tuple[bytes | None, str]:
    """Normalize raw bytes to the canonical form for hashing.

    Returns (canonical_bytes, "") or (None, "json_shape") when a JSON
    target's body fails shape validation (degraded, never hashed).
    Page text is NEVER emitted — only its hash leaves this function.
    """
    policy = contract["canon"]
    if policy == "json-envelope":
        try:
            doc = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return None, "json_shape"
        cleaned = _drop_volatile_keys(doc)
        canon = json.dumps(cleaned, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True).encode("utf-8")
        return canon, ""
    text = raw.decode("utf-8", "replace")
    if policy == "text-doc":
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = [ln.rstrip() for ln in text.split("\n")]
        text = "\n".join(lines).rstrip("\n")
        text = _TS_LINE_RE.sub("<VOLATILE-TS-LINE>", text)
        text = _ISO_TS_RE.sub("<TS>", text)
    elif policy == "html":
        text = _COMMENT_RE.sub("<COMMENT>", text)
        text = _DATETIME_ATTR_RE.sub('datetime="<TS>"', text)
        text = _ISO_TS_RE.sub("<TS>", text)
        text = _CACHEBUSTER_RE.sub(r"\1<CB>", text)
        text = _BUILDID_RE.sub(r"\1<BUILD>\2", text)
        text = _NEXT_STATIC_RE.sub("/_next/static/<BUILD>/", text)
    else:  # pragma: no cover - defensive
        raise ValueError(f"unknown canon policy {policy!r}")
    return text.encode("utf-8"), ""


def _looks_like_botwall(text: str) -> bool:
    lowered = text.lower()
    return any(m in lowered for m in _BOTWALL_MARKERS)


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------
# State (hashes/projections only, never page bytes or titles)
# ---------------------------------------------------------------------------

def _blank_state() -> dict:
    return {"version": STATE_VERSION, "updated_at": utcnow_iso(),
            "targets": {}}


def _load_state(path: str = STATE_PATH) -> tuple[dict, bool]:
    """Load state. Returns (state, was_corrupt).

    was_corrupt=True means the file was quarantined and the state is a
    fresh baseline (zero hits on re-baseline).
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            st = json.load(f)
        if (not isinstance(st, dict)
                or st.get("version") != STATE_VERSION
                or not isinstance(st.get("targets"), dict)):
            raise ValueError("bad version or shape")
        return st, False
    except FileNotFoundError:
        return _blank_state(), False
    except (OSError, ValueError, json.JSONDecodeError) as e:
        # Quarantine the corrupt file, re-baseline with zero hits.
        # The quarantine dir sits next to the state file (derived from
        # the path, so tests can redirect it).
        try:
            qdir = os.path.join(os.path.dirname(path), "quarantine")
            os.makedirs(qdir, exist_ok=True)
            qname = (f"state-corrupt-"
                     f"{utcnow_iso().replace(':', '')}.json")
            os.rename(path, os.path.join(qdir, qname))
        except OSError:
            pass
        _report("state_corrupt",
                f"state file quarantined ({type(e).__name__}); "
                "re-baselining with zero hits",
                {"path": path})
        return _blank_state(), True


def _save_state(state: dict, path: str = STATE_PATH) -> None:
    """Write state through a unique tmp name + atomic rename."""
    state = dict(state)
    state["updated_at"] = utcnow_iso()
    payload = _scrub_strings(state)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{uuid.uuid4().hex}.tmp"  # unique per write (S: no shared tmp)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, sort_keys=True)
    os.rename(tmp, path)


# ---------------------------------------------------------------------------
# Per-target scan
# ---------------------------------------------------------------------------

def _note_gap(state: dict, url: str, reason: str, detail: str) -> None:
    """Record a gap (S4): never a hit, never a clean negative.

    Consecutive gaps are tracked. After GAP_ALERT_N consecutive gaps,
    a report_error alert fires (identifiers only).
    """
    entry = state["targets"].setdefault(url, {})
    entry["consecutive_gaps"] = int(entry.get("consecutive_gaps", 0)) + 1
    entry["last_gap"] = utcnow_iso()
    entry["last_gap_reason"] = reason
    n = entry["consecutive_gaps"]
    print(f"[surfacewatch] {url}: GAP ({reason}); "
          f"consecutive_gaps={n}", file=sys.stderr)
    if n == GAP_ALERT_N:
        _report("target_dark",
                f"{url} unreachable for {GAP_ALERT_N} consecutive runs",
                {"url": url, "reason": reason, "detail": detail,
                 "consecutive_gaps": n})
    elif n > GAP_ALERT_N and n % GAP_ALERT_N == 0:
        _report("target_dark",
                f"{url} still unreachable ({n} consecutive gaps)",
                {"url": url, "reason": reason,
                 "consecutive_gaps": n})


def _scan_target(url: str, contract: dict, state: dict, seen_ids,
                 observed_at: str) -> tuple[list, int]:
    """Scan one target. Returns (hits, bytes_read)."""
    hits = []
    res = _fetch(url, contract)
    if not res["ok"]:
        _note_gap(state, url, res["reason"], res["detail"])
        _report("fetch_gap",
                f"{url}: fetch failed ({res['reason']})",
                {"url": url, "reason": res["reason"],
                 "detail": res["detail"]})
        return hits, 0

    raw = res["raw"]
    raw_sha = _sha256(raw)
    raw_len = len(raw)

    if contract["canon"] == "html":
        # Bot-wall check on decoded text (detection only; never emitted).
        if _looks_like_botwall(raw.decode("utf-8", "replace")[:50_000]):
            _note_gap(state, url, "botwall", "challenge page served")
            _report("fetch_gap",
                    f"{url}: bot-detection page served (degraded)",
                    {"url": url, "reason": "botwall"})
            return hits, raw_len

    canon, shape_err = _canonicalize(raw, contract)
    if canon is None:
        _note_gap(state, url, shape_err, "json shape invalid")
        _report("fetch_gap",
                f"{url}: content-shape validation failed ({shape_err})",
                {"url": url, "reason": shape_err})
        return hits, raw_len

    canon_sha = _sha256(canon)
    entry = state["targets"].get(url, {})
    old_canon = entry.get("canon_sha256")

    if old_canon is None:
        # First sighting (or post-quarantine re-baseline): record, no hit.
        state["targets"][url] = {
            "canon_sha256": canon_sha,
            "raw_sha256": raw_sha,
            "raw_bytes": raw_len,
            "truncated": res["truncated"],
            "consecutive_gaps": 0,
            "last_seen": observed_at,
            "last_gap": None,
        }
        print(f"[surfacewatch] {url}: baselined ({canon_sha[:12]}…)",
              file=sys.stderr)
        return hits, raw_len

    entry["consecutive_gaps"] = 0
    entry["last_seen"] = observed_at

    if canon_sha == old_canon:
        # Unchanged: update forensic fields, no hit.
        entry.update({"raw_sha256": raw_sha, "raw_bytes": raw_len,
                      "truncated": res["truncated"]})
        return hits, raw_len

    # Hash changed. Identifiers only: target, hash pair, observed_at.
    key_base = f"surfacewatch:{url}:{canon_sha}"
    _, dedup_key = redact_secrets(key_base)
    summary = f"content hash changed at {url}"
    _, summary = redact_secrets(summary)
    provenance = _scrub_strings({
        "method": "GET content-hash change detection (surfacewatch)",
        "target_url": url,
        "artifact_type": contract["artifact_type"],
        "artifact_kind": contract["artifact_kind"],
        "previous_canon_sha256": old_canon,
        "current_canon_sha256": canon_sha,
        "previous_raw_sha256": entry.get("raw_sha256"),
        "current_raw_sha256": raw_sha,
        "previous_raw_bytes": entry.get("raw_bytes"),
        "raw_bytes": raw_len,
        "truncated": res["truncated"],
        "volatile_policy": contract["canon"],
        "observed_at": observed_at,
    })
    if is_new(seen_ids, dedup_key):
        hits.append(make_hit(
            lane=LANE,
            source_url=url,
            indicators_matched=[INDICATOR_CHANGED],
            confidence="MEDIUM",  # S3: hash-only change, MEDIUM max
            summary=summary,
            provenance=provenance,
            observed_at=observed_at,
            extra=_scrub_strings({
                "hash_pair": {"old": old_canon, "new": canon_sha},
                "artifact_type": contract["artifact_type"],
                "artifact_kind": contract["artifact_kind"],
            }),
            grade="PRIMARY",  # S3: direct observation of the fetch
        ))
        mark_seen(seen_ids, dedup_key)
        print(f"[surfacewatch] {url}: HASH CHANGED "
              f"{old_canon[:12]}… -> {canon_sha[:12]}…", file=sys.stderr)
    entry.update({"canon_sha256": canon_sha, "raw_sha256": raw_sha,
                  "raw_bytes": raw_len, "truncated": res["truncated"]})
    return hits, raw_len


# ---------------------------------------------------------------------------
# Main scan contract
# ---------------------------------------------------------------------------

def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Fetch the 13 hardcoded agent-surfaces, report hash changes.

    Note: since_hours is accepted for contract compliance but content
    has no capture timestamp; newness is determined by hash change
    against stored state, not by time window.
    """
    if seen_ids is None:
        seen_ids = set()
    observed_at = utcnow_iso()

    if dry_run:
        # ZERO network calls on dry-run.
        print("[dry-run] surfacewatch: 13 hardcoded targets "
              "(GET only, no redirects, 10s spacing, 2MB/target cap)",
              file=sys.stderr)
        for url in sorted(TARGETS):
            c = TARGET_CONTRACTS[url]
            print(f"[dry-run]   {c['artifact_type']}:{c['artifact_kind']} "
                  f"{url}", file=sys.stderr)
        return []

    cfg = load_config()
    sw = cfg.get("surfacewatch", {}) or {}
    if not sw.get("enabled", False):
        print("[surfacewatch] disabled in config "
              "(surfacewatch.enabled is not true); refusing live scan",
              file=sys.stderr)
        return []

    state, was_corrupt = _load_state()
    if was_corrupt:
        print("[surfacewatch] state was corrupt; quarantined and "
              "re-baselining with zero hits", file=sys.stderr)

    hits = []
    budget_used = 0
    targets = sorted(TARGETS)
    for i, url in enumerate(targets):
        if budget_used + MAX_BODY > RUN_BUDGET:
            _report("run_budget_exceeded",
                    "per-run byte budget exceeded; aborting remaining "
                    "targets",
                    {"budget_bytes": RUN_BUDGET,
                     "targets_done": i,
                     "targets_total": len(targets)})
            print("[surfacewatch] run budget exceeded; aborting",
                  file=sys.stderr)
            break
        try:
            thits, bread = _scan_target(url, TARGET_CONTRACTS[url],
                                        state, seen_ids, observed_at)
            hits.extend(thits)
            budget_used += bread
        except Exception as e:
            _note_gap(state, url, "exception", type(e).__name__)
            _report("target_failed", f"{url}: {type(e).__name__}: {e}",
                    {"url": url})
            print(f"[surfacewatch] target {url!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
        if i < len(targets) - 1:
            time.sleep(REQUEST_SPACING)
    _save_state(state)
    hits.sort(key=lambda h: h["summary"])
    return hits


def main():
    args = parse_args("Lane 13 — surfacewatch: content-hash change "
                      "detection on public agent-infrastructure surfaces")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
