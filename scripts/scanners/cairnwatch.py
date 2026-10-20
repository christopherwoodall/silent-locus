#!/usr/bin/env python3
"""Lane 12 — cairnwatch: passive watch over 4 counsel-cleared Cairn panels.

Polls GET /projects on four hardcoded Cairn panel hosts and diffs the
project list run-over-run. For project ids never seen before it also
fetches GET /projects/{id} once, to record worker/heartbeat
projections. Passive GET only. No POST, no login, no interaction, no
cookies, no auth headers. Redirects are NOT chased.

Allowlist (HARDCODED frozenset; not config-soft; no --hosts override;
no auto-discovery):
    185.242.245.159:8000, 31.56.206.187:8000,
    31.57.47.29:8000,    31.59.92.155:8000
Counsel verdict 2026-10-19: these 4 hosts are MALICIOUS panels. That
verdict is an UPSTREAM assertion recorded in provenance below; it is
never this module's own finding and the word "malicious" never appears
in indicator names. Evidence:
data/lanes/cairn-panels/working/PHASE2-FINAL-REPORT.md.

Detection rules (diff by project id; grade PRIMARY for all -- direct
observation):
    cairn.project.created          new project id at list level. HIGH.
    cairn.project.status_changed   status enum from->to on a known id.
                                   MEDIUM.
    cairn.worker.first_observed     worker id(s) seen on a new project
                                   id (detail fetch). MEDIUM. Worker and
                                   creator strings recorded verbatim in
                                   the hit; never pivoted, enriched, or
                                   attributed.
    cairn.worker.heartbeat_resumed  worker timestamp advanced after a
                                   stale gap (see heartbeat semantics).
                                   MEDIUM.
    cairn.worker.heartbeat_stale    status=active at list level while
                                   the last-known worker timestamp is
                                   older than the staleness threshold.
                                   MEDIUM. Fires once per stale episode.
    cairn.host.dark                 host unreachable for
                                   DARK_ALERT_N=3 consecutive runs. LOW.
                                   (One dark run cannot distinguish
                                   takedown from a timeout; see
                                   FALSE-POSITIVES-cairnwatch.md.)

Heartbeat semantics (transition only -- NEVER alert on advancing
timestamps):
  The Cairn API names the field "last_heartbeat_at". It appears as
  project.reason.last_heartbeat_at (detail level; usually null at list
  level) and per-intent last_heartbeat_at (detail level only). Because
  /projects/{id} is fetched ONLY for unseen ids (passive-budget rule),
  heartbeat data is refreshed later only when the list-level payload
  itself carries a reason.last_heartbeat_at dict. With list-level-only
  data, "resume" cannot fire; "stale-while-active" can, from the
  frozen first-sight timestamp. This limitation is documented, not
  worked around: chasing freshness would violate the passive budget.
  Staleness threshold: >= 2x poll interval + clock-skew margin.
  Poll interval = 24h (daily orchestrator run); skew margin = 2h;
  threshold = 50h.

OPSEC / shared USER_AGENT tradeoff:
  This module sends _common.USER_AGENT on every request (the same
  string as every other lane scanner). A fixed UA is fingerprintable:
  the panels' operators can log it and recognize our polling pattern.
  That is a known, standing tradeoff (uniform fleet-wide UA keeps our
  own telemetry attributable and avoids per-lane fingerprint sprawl).
  Do NOT rotate or randomize the UA silently -- any change is an OPSEC
  decision for the operator, not a code tweak.

State (state/cairnwatch/state.json): projections + hashes ONLY.
Per project: {host, project_id, first_seen, status_enum, detail_hash,
credential_presence, last_heartbeat_at, stale_alerted}. Never titles,
never detail bytes, never page content. detail_hash is the canonical
JSON hash (sort_keys, compact separators) of the parsed detail payload
-- the hash, not the content. last_heartbeat_at/stale_alerted and the
per-host dark counters are operational bookkeeping required by the
heartbeat and dark-run rules above. State is version-stamped
(schema_version); a corrupt load is quarantined to
state.json.corrupt-<ts> and the module re-baselines with ZERO hits.
Writes go through a unique tmp name + atomic rename (no shared tmp
name; cf. AGENTS.md last-writer-wins lessons).

redact_secrets() (from _common) applies to all four scanner-emitted
paths: hits, error-log context, summaries/dedup keys, state values.
normalize() is used for DETECTION ONLY in the credential sweep at all
layers; decoded variants are discarded immediately and only a
layer-agnostic verdict (count per pattern class) is recorded. Error
context carries identifiers only (host, project id, byte length,
content hash, pattern-class counts) -- never response content.

since_hours is accepted for contract compliance but does not filter:
newness is determined by state diff, not a time window (the panels
expose no reliable per-project event clock).

Usage:
    cairnwatch.py [--dry-run] [--since-hours 24] [--json]

Disabled by default: needs "cairnwatch": {"enabled": true} in
scripts/swarm-infra-config.json AND the orchestrator LANES entry
(which ships False). --dry-run performs ZERO network calls and
touches no state.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402
from _common import (  # noqa: E402
    USER_AGENT, make_hit, utcnow_iso, is_new, mark_seen,
    parse_args, emit, report_error, normalize, redact_secrets,
    attach_ip_classification, load_config,
)

LANE = "cairnwatch"

# --- Hardcoded allowlist (counsel constraint 1). Frozenset in source.
# Not config-soft. No --hosts override. No auto-discovery. -------------
ALLOWLIST = frozenset({
    "185.242.245.159:8000",
    "31.56.206.187:8000",
    "31.57.47.29:8000",
    "31.59.92.155:8000",
})

# --- Transport policy (mirror of lantern3-detail.py) -----------------
REQUEST_SPACING = 2.0      # >=2s between hosts (and between requests)
TIMEOUT = 30               # seconds per request
MAX_BYTES = 2 * 1024 * 1024       # 2MB streaming cap per response
RUN_BYTE_BUDGET = 10 * 1024 * 1024  # ~10MB per-run budget, abort on exceed
MAX_ATTEMPTS = 2           # 1 initial + max 1 retry, then host is "dark"
RETRY_SLEEP = 2.0

# --- Detection policy ----------------------------------------------
DARK_ALERT_N = 3           # consecutive dark runs before a dark alert
POLL_INTERVAL_HOURS = 24   # daily orchestrator cadence
CLOCK_SKEW_MARGIN_HOURS = 2
# Staleness threshold: >= 2x poll interval + clock-skew margin.
STALE_THRESHOLD_HOURS = 2 * POLL_INTERVAL_HOURS + CLOCK_SKEW_MARGIN_HOURS

STATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state", "cairnwatch")
STATE_PATH = os.path.join(STATE_DIR, "state.json")
STATE_SCHEMA_VERSION = 1

# Counsel MALICIOUS verdict (2026-10-19) on the 4 allowlist hosts.
# UPSTREAM assertion -- provenance only, never an indicator name.
PROVENANCE_VERDICT = (
    "Counsel verdict 2026-10-19: the 4 allowlist hosts are MALICIOUS "
    "Cairn panels (UPSTREAM assertion, not this module's finding; "
    "evidence data/lanes/cairn-panels/working/PHASE2-FINAL-REPORT.md)"
)


# ---------------------------------------------------------------------------
# Transport: streaming GET, no redirect chase, no cookies, no auth.
# ---------------------------------------------------------------------------
class _Redirected(Exception):
    """Raised instead of following a redirect (redirects are not chased)."""

    def __init__(self, code, newurl):
        super().__init__(f"HTTP {code} -> {newurl}")
        self.code = code
        self.newurl = newurl


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise _Redirected(code, newurl)


# Default opener handlers + our no-redirect policy. No CookieJar, no
# auth handlers: only a User-Agent header is sent.
_OPENER = urllib.request.build_opener(_NoRedirect())


def _get_capped(url: str, budget: dict) -> tuple:
    """One streaming GET. Returns (status, body, note).

    note is one of: ok, capped_2MB, run_budget_exceeded,
    redirect_not_chased, final_url_mismatch,
    unexpected_content_type_<t>, http_error_<code>,
    transport_<ExcName>.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    try:
        resp = _OPENER.open(req, timeout=TIMEOUT)
    except _Redirected as e:
        return e.code, b"", "redirect_not_chased"
    except urllib.error.HTTPError as e:
        return e.code, b"", f"http_error_{e.code}"
    except Exception as e:
        return -1, b"", f"transport_{type(e).__name__}"
    try:
        if resp.geturl() != url:
            return resp.status, b"", "final_url_mismatch"
        ctype = resp.headers.get_content_type()
        if ctype != "application/json":
            return resp.status, b"", f"unexpected_content_type_{ctype}"
        chunks, total = [], 0
        while True:
            c = resp.read(65536)
            if not c:
                break
            total += len(c)
            if total > MAX_BYTES:
                keep = c[:MAX_BYTES - (total - len(c))]
                chunks.append(keep)
                budget["used"] += MAX_BYTES
                return resp.status, b"".join(chunks), "capped_2MB"
            chunks.append(c)
            if budget["used"] + total > RUN_BYTE_BUDGET:
                budget["used"] += total
                return resp.status, b"".join(chunks), "run_budget_exceeded"
        budget["used"] += total
        return resp.status, b"".join(chunks), "ok"
    finally:
        try:
            resp.close()
        except Exception:
            pass


def _get_with_retry(url: str, budget: dict) -> tuple:
    """One retry on transport errors only. HTTP statuses are not retried."""
    last = (-1, b"", "no_attempt")
    for attempt in range(MAX_ATTEMPTS):
        if attempt:
            time.sleep(RETRY_SLEEP)
        status, body, note = _get_capped(url, budget)
        if note.startswith("transport_"):
            last = (status, body, note)
            continue
        return status, body, note
    return last


# ---------------------------------------------------------------------------
# Payload validation: content-type + JSON shape before any diffing.
# ---------------------------------------------------------------------------
def _parse_projects(body: bytes):
    """Validate list-level /projects shape. Returns (rows, note)."""
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception:
        return None, "json_parse_failed"
    # A 200 with {"detail": "Not Found"} is degraded, not a hit.
    if isinstance(data, dict):
        return None, "api_detail_envelope"
    if not isinstance(data, list):
        return None, "unexpected_shape_not_list"
    for p in data:
        if (not isinstance(p, dict)
                or not isinstance(p.get("id"), str)
                or not isinstance(p.get("status"), str)):
            return None, "unexpected_shape_row"
    return data, "ok"


def _parse_detail(body: bytes):
    """Validate /projects/{id} shape. Returns (detail_dict, note)."""
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception:
        return None, "json_parse_failed"
    if not isinstance(data, dict):
        return None, "unexpected_shape_not_dict"
    proj = data.get("project")
    if not isinstance(proj, dict) or not isinstance(proj.get("id"), str):
        return None, "unexpected_shape_no_project"
    return data, "ok"


def _canonical_hash(obj) -> str:
    """Canonical JSON hash (sort_keys, compact separators)."""
    canon = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Heartbeat extraction. The API names the field "last_heartbeat_at"
# (project.reason.last_heartbeat_at and per-intent last_heartbeat_at).
# ---------------------------------------------------------------------------
def _parse_ts(ts: str):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _extract_heartbeat(detail: dict):
    """Returns (latest_heartbeat_iso|None, workers[], creators[]).

    Worker/creator strings are returned verbatim (never pivoted or
    enriched downstream).
    """
    workers, creators, stamps = [], [], []
    proj = detail.get("project") or {}
    reason = proj.get("reason")
    if isinstance(reason, dict):
        ts = reason.get("last_heartbeat_at")
        if isinstance(ts, str):
            stamps.append(ts)
        w = reason.get("worker")
        if isinstance(w, str):
            workers.append(w)
    intents = detail.get("intents") or []
    if isinstance(intents, list):
        for intent in intents:
            if not isinstance(intent, dict):
                continue
            ts = intent.get("last_heartbeat_at")
            if isinstance(ts, str):
                stamps.append(ts)
            w = intent.get("worker")
            c = intent.get("creator")
            if isinstance(w, str):
                workers.append(w)
            if isinstance(c, str):
                creators.append(c)
    latest = None
    for ts in stamps:
        try:
            dt = _parse_ts(ts)
        except Exception:
            continue
        if latest is None or dt > latest:
            latest = dt
    latest_iso = (latest.isoformat().replace("+00:00", "Z")
                  if latest is not None else None)
    return latest_iso, sorted(set(workers)), sorted(set(creators))


# ---------------------------------------------------------------------------
# Credential sweep: normalize() for DETECTION ONLY. Decoded variants are
# discarded; only the layer-agnostic verdict (count per pattern class)
# is returned and recorded. Matched strings are never stored.
# ---------------------------------------------------------------------------
def _credential_sweep_counts(text: str) -> dict:
    counts: dict = {}
    for variant in normalize(text):
        for cls, n in C.secret_pattern_counts(variant).items():
            counts[cls] = counts.get(cls, 0) + n
    return counts


# ---------------------------------------------------------------------------
# Redaction of scanner-emitted strings (hits, dedup keys, state values).
# ---------------------------------------------------------------------------
def _scrub(obj):
    if isinstance(obj, str):
        return redact_secrets(obj)[1]
    if isinstance(obj, dict):
        return {k: _scrub(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_scrub(v) for v in obj]
    return obj


def _scrub_context(ctx: dict) -> dict:
    """Identifiers-only context, redacted for defense in depth."""
    return {str(k)[:50]: redact_secrets(v)[1] for k, v in ctx.items()}


# ---------------------------------------------------------------------------
# State: projections + hashes only. Version-stamped. Corrupt load ->
# quarantine + re-baseline with ZERO hits. Unique tmp + atomic rename.
# ---------------------------------------------------------------------------
def _blank_state() -> dict:
    return {
        "schema_version": STATE_SCHEMA_VERSION,
        "updated_at": utcnow_iso(),
        "hosts": {},
        "projects": {},
    }


def _load_state():
    """Returns (state, fresh_baseline).

    fresh_baseline is True when no state existed (first run) or the
    load failed (quarantined). In both cases the run re-baselines with
    ZERO hits.
    """
    if not os.path.exists(STATE_PATH):
        return _blank_state(), True
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
        if (not isinstance(state, dict)
                or state.get("schema_version") != STATE_SCHEMA_VERSION
                or not isinstance(state.get("projects"), dict)
                or not isinstance(state.get("hosts"), dict)):
            raise ValueError("schema mismatch")
        return state, False
    except Exception as e:
        ts = utcnow_iso().replace(":", "").replace("-", "")
        qpath = STATE_PATH + f".corrupt-{ts}"
        try:
            os.rename(STATE_PATH, qpath)
            qname = os.path.basename(qpath)
        except OSError:
            qname = "<rename-failed>"
        report_error(
            "cairnwatch", "state_corrupt",
            f"state load failed ({type(e).__name__}); quarantined, "
            f"re-baselining with zero hits",
            _scrub_context({"quarantined_as": qname}),
        )
        return _blank_state(), True


def _save_state(state: dict) -> None:
    state["updated_at"] = utcnow_iso()
    scrubbed = _scrub(state)
    os.makedirs(STATE_DIR, exist_ok=True)
    # Unique tmp name per write (pid + uuid): no two writers share a
    # tmp path. Atomic rename.
    tmp = STATE_PATH + f".tmp.{os.getpid()}.{uuid.uuid4().hex[:8]}"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(scrubbed, f, indent=1, sort_keys=True,
                  ensure_ascii=False)
    os.rename(tmp, STATE_PATH)


# ---------------------------------------------------------------------------
# Per-host scan.
# ---------------------------------------------------------------------------
def _scan_host(host: str, state: dict, seen_ids, budget: dict,
               observed_at: str, silent: bool, config: dict):
    """Scan one host. Returns (hits, abort_run)."""
    hits = []
    ip = host.split(":")[0]
    hstate = state["hosts"].setdefault(host, {
        "consecutive_dark": 0,
        "dark_alerted": False,
        "last_outcome": None,
    })
    url = f"http://{host}/projects"
    status, body, note = _get_with_retry(url, budget)

    def _base_provenance():
        return {
            "method": ("passive GET /projects (+ /projects/{id} for "
                       "unseen ids only); 2s spacing, 30s timeout, "
                       "2MB cap, ~10MB run budget, no redirects, "
                       "no cookies, no auth"),
            "host": host,
            "endpoint": "/projects",
            "panel_verdict": PROVENANCE_VERDICT,
            "retrieved_at": observed_at,
        }

    def _mk_hit(indicators, confidence, summary, source_url, extra):
        hit = make_hit(
            lane=LANE,
            source_url=source_url,
            indicators_matched=indicators,
            confidence=confidence,
            summary=summary,
            provenance=_base_provenance(),
            observed_at=observed_at,
            extra=extra,
            grade="PRIMARY",
        )
        hit = attach_ip_classification(hit, ip, config)
        return _scrub(hit)

    if note == "run_budget_exceeded":
        report_error("cairnwatch", "byte_budget_exceeded",
                     f"run byte budget exceeded at {host}; aborting run",
                     _scrub_context({"host": host,
                                     "budget_bytes": RUN_BYTE_BUDGET}))
        return hits, True

    # --- Dark: transport failure after 1 retry -------------------------
    if note.startswith("transport_") or status == -1:
        hstate["consecutive_dark"] = hstate.get("consecutive_dark", 0) + 1
        hstate["last_outcome"] = "dark"
        report_error(
            "cairnwatch", "host_dark",
            f"{host} unreachable after 1 retry ({note})",
            _scrub_context({
                "host": host,
                "consecutive_dark": hstate["consecutive_dark"],
                "note": note,
            }),
        )
        if (hstate["consecutive_dark"] >= DARK_ALERT_N
                and not hstate.get("dark_alerted") and not silent):
            hstate["dark_alerted"] = True
            key = redact_secrets(
                f"cairnwatch:{host}:dark:{hstate['consecutive_dark']}")[1]
            if is_new(seen_ids, key):
                hits.append(_mk_hit(
                    ["cairn.host.dark"], "LOW",
                    f"[cairnwatch] {host}: dark for "
                    f"{hstate['consecutive_dark']} consecutive runs "
                    f"(timeout vs takedown indistinguishable)",
                    url,
                    {"host": host,
                     "consecutive_dark": hstate["consecutive_dark"]},
                ))
                mark_seen(seen_ids, key)
        return hits, False

    # --- 429: hard stop for this host for the run (not "dark") ---------
    if status == 429:
        hstate["last_outcome"] = "rate_limited_429"
        report_error("cairnwatch", "rate_limited_429",
                     f"{host} returned 429; hard stop for this host "
                     f"this run",
                     _scrub_context({"host": host, "endpoint": "/projects",
                                     "http_status": 429}))
        return hits, False

    # --- Degraded: 3xx/redirect, content-type, shape, HTTP errors ------
    # A 200 with HTML or {"detail": "Not Found"} lands here via the
    # content-type / shape checks. Degraded is never a hit.
    if note != "ok":
        hstate["last_outcome"] = f"degraded:{note}"
        report_error(
            "cairnwatch", "degraded_response",
            f"{host}/projects degraded ({note}); not a hit",
            _scrub_context({
                "host": host,
                "endpoint": "/projects",
                "http_status": status,
                "note": note,
                "bytes": len(body),
                "content_sha256": hashlib.sha256(body).hexdigest()[:16],
            }),
        )
        return hits, False

    projects, shape = _parse_projects(body)
    if shape != "ok":
        hstate["last_outcome"] = f"degraded:{shape}"
        report_error(
            "cairnwatch", "degraded_response",
            f"{host}/projects invalid payload ({shape}); not a hit",
            _scrub_context({
                "host": host,
                "endpoint": "/projects",
                "http_status": status,
                "shape_note": shape,
                "bytes": len(body),
                "content_sha256": hashlib.sha256(body).hexdigest()[:16],
            }),
        )
        return hits, False

    # --- OK: reset dark counters, diff by project id -------------------
    hstate["consecutive_dark"] = 0
    hstate["dark_alerted"] = False
    hstate["last_outcome"] = "ok"
    host_stop = False  # set on detail 429 / budget abort

    list_text = body.decode("utf-8", "replace")
    list_sweep = _credential_sweep_counts(list_text)

    for p in projects:
        pid = p["id"]
        status_enum = p["status"]
        pkey = f"{host}|{pid}"
        prev = state["projects"].get(pkey)

        # List-level reason.last_heartbeat_at, when the API serves it
        # (usually null at list level; detail is authoritative).
        row_hb = None
        reason = p.get("reason")
        if isinstance(reason, dict):
            rhb = reason.get("last_heartbeat_at")
            if isinstance(rhb, str):
                row_hb = rhb

        if prev is None:
            # --- New project id ------------------------------------
            hb_iso, workers, creators = None, [], []
            detail_hash = _canonical_hash({"unavailable": True})
            d_sweep: dict = {}
            cred_present = False
            if not host_stop:
                durl = f"http://{host}/projects/{pid}"
                d_status, d_body, d_note = _get_with_retry(durl, budget)
                if d_note == "run_budget_exceeded":
                    host_stop = True
                elif d_status == 429:
                    host_stop = True
                    report_error(
                        "cairnwatch", "rate_limited_429",
                        f"{host} returned 429 on detail fetch; hard "
                        f"stop for this host this run",
                        _scrub_context({"host": host,
                                        "project_id": pid,
                                        "http_status": 429}))
                else:
                    (hb_iso, workers, creators, detail_hash,
                     d_sweep) = _finish_detail(d_status, d_body, d_note,
                                              host, pid)
                    cred_present = any(d_sweep.values())
            else:
                d_sweep = {}
            state["projects"][pkey] = {
                "host": host,
                "project_id": pid,
                "first_seen": observed_at,
                "status_enum": status_enum,
                "detail_hash": detail_hash,
                "credential_presence": bool(cred_present),
                "last_heartbeat_at": hb_iso or row_hb,
                "stale_alerted": False,
            }
            if not silent:
                key = redact_secrets(f"cairnwatch:{host}:{pid}:created")[1]
                if is_new(seen_ids, key):
                    indicators = ["cairn.project.created"]
                    if workers:
                        indicators.append("cairn.worker.first_observed")
                    hits.append(_mk_hit(
                        indicators, "HIGH",
                        f"[cairnwatch] {host}: new project {pid} "
                        f"(status {status_enum})",
                        f"http://{host}/projects/{pid}",
                        {
                            "host": host,
                            "project_id": pid,
                            "status": status_enum,
                            # Worker/creator strings verbatim; never
                            # pivoted, enriched, or attributed.
                            "workers_first_seen": workers,
                            "creators_first_seen": creators,
                            "last_heartbeat_at": hb_iso or row_hb,
                            # Credential sweep: counts per pattern
                            # class only; never matched values.
                            "credential_sweep": d_sweep,
                            "list_credential_sweep": list_sweep,
                        },
                    ))
                    mark_seen(seen_ids, key)
            continue

        # --- Known project: status transition ------------------------
        if prev.get("status_enum") != status_enum:
            old_status = prev.get("status_enum")
            prev["status_enum"] = status_enum
            if not silent:
                key = redact_secrets(
                    f"cairnwatch:{host}:{pid}:status:"
                    f"{old_status}->{status_enum}")[1]
                if is_new(seen_ids, key):
                    hits.append(_mk_hit(
                        ["cairn.project.status_changed"], "MEDIUM",
                        f"[cairnwatch] {host}: project {pid} status "
                        f"{old_status} -> {status_enum}",
                        url,
                        {
                            "host": host,
                            "project_id": pid,
                            "status_from": old_status,
                            "status_to": status_enum,
                        },
                    ))
                    mark_seen(seen_ids, key)

        # --- Heartbeat transitions (never bare advancing) ------------
        # Refresh from list-level reason when the API serves it.
        if row_hb and row_hb != prev.get("last_heartbeat_at"):
            prev["last_heartbeat_at"] = row_hb
        hb_iso = prev.get("last_heartbeat_at")
        hb_age_h = None
        if hb_iso:
            try:
                now = datetime.datetime.now(datetime.timezone.utc)
                hb_age_h = (now - _parse_ts(hb_iso)).total_seconds() / 3600.0
            except Exception:
                hb_age_h = None  # unparseable timestamp: no assessment
        if (status_enum == "active" and hb_age_h is not None
                and not silent):
            if (hb_age_h > STALE_THRESHOLD_HOURS
                    and not prev.get("stale_alerted")):
                prev["stale_alerted"] = True
                key = redact_secrets(
                    f"cairnwatch:{host}:{pid}:heartbeat_stale")[1]
                if is_new(seen_ids, key):
                    hits.append(_mk_hit(
                        ["cairn.worker.heartbeat_stale"], "MEDIUM",
                        f"[cairnwatch] {host}: project {pid} status "
                        f"active but worker timestamp older than "
                        f"{STALE_THRESHOLD_HOURS}h",
                        url,
                        {
                            "host": host,
                            "project_id": pid,
                            "last_heartbeat_at": hb_iso,
                            "heartbeat_age_hours": round(hb_age_h, 1),
                            "stale_threshold_hours":
                                STALE_THRESHOLD_HOURS,
                        },
                    ))
                    mark_seen(seen_ids, key)
            elif (hb_age_h <= STALE_THRESHOLD_HOURS
                    and prev.get("stale_alerted")):
                prev["stale_alerted"] = False
                key = redact_secrets(
                    f"cairnwatch:{host}:{pid}:heartbeat_resumed")[1]
                if is_new(seen_ids, key):
                    hits.append(_mk_hit(
                        ["cairn.worker.heartbeat_resumed"], "MEDIUM",
                        f"[cairnwatch] {host}: project {pid} worker "
                        f"timestamp advanced after stale gap",
                        url,
                        {
                            "host": host,
                            "project_id": pid,
                            "last_heartbeat_at": hb_iso,
                            "heartbeat_age_hours": round(hb_age_h, 1),
                        },
                    ))
                    mark_seen(seen_ids, key)

    return hits, False


def _finish_detail(status: int, body: bytes, note: str,
                   host: str, pid: str):
    """Shared tail of a detail fetch: validate, extract, hash, sweep."""
    text = body.decode("utf-8", "replace")
    sweep = _credential_sweep_counts(text)
    ctx = {
        "host": host,
        "project_id": pid,
        "http_status": status,
        "note": note,
        "bytes": len(body),
        "content_sha256": hashlib.sha256(body).hexdigest()[:16],
        "secret_class_counts": sweep,
    }
    if note != "ok" or status != 200:
        etype = ("detail_transport_failed" if note.startswith("transport_")
                 else "detail_degraded")
        report_error("cairnwatch", etype,
                     f"{host}/projects/{pid}: {note}",
                     _scrub_context(ctx))
        return None, [], [], _canonical_hash({"unavailable": True}), sweep
    detail, shape = _parse_detail(body)
    if shape != "ok":
        report_error("cairnwatch", "detail_degraded",
                     f"{host}/projects/{pid}: {shape}",
                     _scrub_context(ctx))
        return None, [], [], _canonical_hash({"unavailable": True}), sweep
    hb_iso, workers, creators = _extract_heartbeat(detail)
    return hb_iso, workers, creators, _canonical_hash(detail), sweep


# ---------------------------------------------------------------------------
# scan() contract.
# ---------------------------------------------------------------------------
def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Poll the 4 allowlist panels, diff by project id. Returns hit dicts.

    since_hours is accepted for contract compliance but does not
    filter: newness comes from the state diff, not a time window.
    --dry-run performs ZERO network calls and touches no state.
    """
    if seen_ids is None:
        seen_ids = set()

    cfg = load_config()
    if not cfg.get("cairnwatch", {}).get("enabled", False):
        print("[cairnwatch] disabled (config 'cairnwatch'.enabled is "
              "false); skipping", file=sys.stderr)
        return []

    if dry_run:
        for host in sorted(ALLOWLIST):
            print(f"[dry-run] cairnwatch GET http://{host}/projects "
                  f"(+ GET /projects/{{id}} for unseen ids only)",
                  file=sys.stderr)
        return []

    state, silent = _load_state()
    if silent:
        print("[cairnwatch] (re)baselining: recording projections, "
              "zero hits this run", file=sys.stderr)

    observed_at = utcnow_iso()
    budget = {"used": 0}
    hits = []
    hosts = sorted(ALLOWLIST)
    for i, host in enumerate(hosts):
        if i:
            time.sleep(REQUEST_SPACING)  # >=2s per-host spacing
        try:
            host_hits, abort = _scan_host(host, state, seen_ids, budget,
                                          observed_at, silent, cfg)
        except Exception as e:
            # Defense-in-depth: redact the message too (no active leak path
            # today — parsers never pass body text — but exception .str()
            # is attacker-adjacent). Mirrors surfacewatch._report.
            _, safe_msg = redact_secrets(f"{host}: {type(e).__name__}: {e}")
            report_error("cairnwatch", "host_scan_failed", safe_msg,
                         _scrub_context({"host": host}))
            print(f"[cairnwatch] {host} failed: {type(e).__name__}",
                  file=sys.stderr)
            continue
        hits.extend(host_hits)
        if abort:
            print("[cairnwatch] run byte budget exceeded; aborting",
                  file=sys.stderr)
            break

    _save_state(state)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Lane 12 — Cairn panel watch (4 counsel-cleared "
                      "panels, passive GET)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
