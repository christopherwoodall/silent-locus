#!/usr/bin/env python3
"""AIID scanner: weekly-snapshot diff for incidentdatabase.ai (AIID).

Full-site scope, operator-ordered 2026-10-29: ingest ALL AIID
incidents. This module is the SCANNER half only. It watches the
public weekly snapshot listing and reports what changed since the
last run. The ingest half (downloading and parsing a new snapshot
archive) is a separate worker; it feeds parsed incident id->hash
maps back through scan()'s optional snapshot_incidents argument
(see below). This module never downloads a snapshot archive itself:
the archives are ~121 MB, far over the 2 MB per-response cap shared
by the lane scanners, and a truncated archive would corrupt a diff.

Allowed surface (HARDCODED, frozenset in source; not config-soft;
no --url override; no discovery):
    https://incidentdatabase.ai/research/snapshots/
That listing page only. NEVER the login-gated incidents list page,
never any login, session, cookie, or auth header, never POST.
Passive GET only. Redirects are NOT chased: a 3xx response or a
final-URL mismatch is a degraded state, recorded via report_error,
never a hit, and state is left untouched.

What it reports (grade SECONDARY throughout: AIID entries are a
curated database citing press and other reports, not first-hand
observations by this scanner):
    aiid.snapshot.new       a snapshot entry (date) never seen in
                            state. MEDIUM.
    aiid.snapshot.changed   a previously seen snapshot date whose
                            download URL changed. MEDIUM.
    aiid.incident.new       an incident id present in a supplied
                            snapshot_incidents map but absent from
                            state.incidents. MEDIUM.
    aiid.incident.changed   an incident id present in both, with a
                            different row hash. LOW (a hash change
                            says the record changed, not how).
A snapshot entry that disappears from the listing is NOT a hit: it
is logged via report_error only (listings get reorganised; a
disappearance is not evidence an incident was removed).

No personal names in any output. Hits and state carry incident /
report IDs and URLs only. No submitter names, no editor names, no
titles, no descriptions. parse_snapshot_rows() drops every column
except the id and a hash of the remaining row, and it drops
name-like columns (submitter, editor, author, reporter, ...) from
the hash input as well, so a name change alone never fires a
changed hit and no name ever enters state.

State (scripts/scanners/state/aiid_state.json): snapshot entries
{"date|kind": {url, anchor_hash}} (schema_version 2; kind is
"tarball" for a .tar.* archive, "excel" for a .xlsx export, else
the file extension kind — see _snapshot_kind), incidents
{id: row_hash}, plus bookkeeping (schema_version, updated_at,
consecutive_gaps, last_seen_snapshot_date). IDs and hashes only,
never titles or row content. Version-stamped: a state file with
any other schema_version is quarantined, never reinterpreted, and
the run re-baselines with ZERO hits. Writes go through a unique
tmp name + atomic rename (no shared tmp name; cf. AGENTS.md
last-writer-wins lessons). A degraded fetch on a fresh baseline
(no state file, or a quarantined corrupt state) persists
NOTHING: no blank baseline is written, so the next successful
run still re-baselines with zero hits instead of reporting every
historical snapshot date as new (see scan()).

since_hours is accepted for contract compliance but does not
filter: newness is determined by the state diff, not a time
window (the listing exposes no per-incident event clock the
scanner can trust). A weekly cron passes --since-hours 168.

Disabled by default: a live scan refuses to run unless
scripts/swarm-infra-config.json carries "aiid": {"enabled": true}.
No aiid block exists in that file today, so the module is inert
until the operator adds one. Enabling aiid alone enables ONLY
this module's hardcoded listing GET: the login-gated list page,
login, sessions, and POST are not in this code at all, so no flag
combination can make this module run them. --dry-run performs
ZERO network calls, reads no config, and touches no state (and
no error log).

Usage:
    aiid.py [--dry-run] [--since-hours 168] [--json]
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
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit, report_error, redact_secrets,
)

LANE = "aiid"
GRADE = "SECONDARY"

# Hardcoded allowed surface. One URL. Not config-soft.
SNAPSHOTS_URL = "https://incidentdatabase.ai/research/snapshots/"
ALLOWED = frozenset({SNAPSHOTS_URL})

# Fetch contract (mirrors surfacewatch S2).
REQUEST_SPACING = 2.0      # seconds (single request per run; kept for parity)
TIMEOUT = 30               # seconds per request
MAX_RETRIES = 1            # max 1 retry (2 attempts total, transport only)
MAX_BODY = 2_000_000       # streaming cap for the listing page (2 MB)
CHUNK = 64 * 1024

STATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "state")
STATE_PATH = os.path.join(STATE_DIR, "aiid_state.json")
# v2: snapshot state keys changed from bare date to "date|kind"
# (F1). A v1 file fails the version check in _load_state and is
# quarantined + re-baselined, never misread as v2 keys.
STATE_VERSION = 2

# Columns that must never influence output or state (personal names).
_NAME_LIKE_COLUMNS = {
    "submitter", "submitted_by", "editor", "edited_by", "author",
    "authors", "reporter", "reported_by", "creator", "created_by",
    "owner", "user", "username", "name", "contact", "email",
}

_DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
_HREF_RE = re.compile(
    r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_SNAPSHOT_HREF_RE = re.compile(
    r"snapshot|incidentdatabase|\.tar\.bz2|\.tar\.gz|\.zip|\.json|\.csv|\.xlsx",
    re.IGNORECASE)


def _snapshot_kind(url: str) -> str:
    """Kind slot for a snapshot download URL (F1).

    The tarball and the Excel export for the same Monday are
    different products and must not share one state slot.
    """
    base = url.split("?", 1)[0].split("#", 1)[0].lower()
    if base.endswith(".xlsx"):
        return "excel"
    if base.endswith((".tar.bz2", ".tar.gz", ".tgz")):
        return "tarball"
    if base.endswith(".zip"):
        return "archive"
    if base.endswith(".json"):
        return "json"
    if base.endswith(".csv"):
        return "csv"
    return "file"


def _entry_key(date: str, kind: str) -> str:
    """State/diff key for one (date, kind) snapshot entry.

    parse_snapshot_listing returns tuple keys; scan() converts
    them with this helper because JSON state cannot hold tuple
    keys (json.dumps raises TypeError on tuple keys).
    """
    return f"{date}|{kind}"


def _split_entry_key(key: str) -> tuple:
    """Inverse of _entry_key; a bare date yields kind ""."""
    date, sep, kind = key.partition("|")
    return date, kind if sep else ""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Redirect handler that refuses to chase (mirrors surfacewatch)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _make_opener() -> urllib.request.OpenerDirector:
    # Explicit handler list: no HTTPCookieProcessor (no CookieJar),
    # no auth handlers. ProxyHandler() with no args honors the
    # environment proxy settings (same as surfacewatch/jina).
    return urllib.request.build_opener(
        urllib.request.ProxyHandler(),
        urllib.request.UnknownHandler(),
        urllib.request.HTTPHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        _NoRedirect(),
        urllib.request.HTTPErrorProcessor(),
    )


_OPENER = _make_opener()


def _scrub(obj):
    if isinstance(obj, str):
        return redact_secrets(obj)[1]
    if isinstance(obj, dict):
        return {k: _scrub(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_scrub(v) for v in obj]
    return obj


def _report(error_type: str, message: str, context: dict | None = None):
    ctx = {}
    if context:
        for k, v in context.items():
            ctx[str(k)] = redact_secrets(str(v))[1]
    report_error("aiid", error_type, redact_secrets(str(message))[1], ctx)


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _row_hash(row: dict) -> str:
    """Hash of a snapshot row with id and name-like columns removed.

    Only the hash is ever stored; row content (titles, text, names)
    never leaves this function.
    """
    clean = {k: v for k, v in row.items()
             if k not in _NAME_LIKE_COLUMNS
             and k.lower() not in _NAME_LIKE_COLUMNS
             and "id" not in k.lower()}
    canon = json.dumps(clean, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, default=str)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _incident_id(row: dict):
    """Incident/report id from a parsed row, or None.

    Accepts common column spellings; returns the id as a string.
    """
    for key in ("incident_id", "incidentId", "id", "report_id",
                "report_number", "incident_number"):
        v = row.get(key)
        if v is not None and str(v).strip() != "":
            return str(v).strip()
    return None


def parse_snapshot_rows(payload: bytes, content_type: str = "") -> dict:
    """Parse snapshot payload bytes into {incident_id: row_hash}.

    Supports JSON (list of objects, or {"incidents": [...]} / 
    {"data": [...]}), JSONL, and CSV with a header row. Returns {}
    on unparseable input (caller logs it as degraded, never a hit).
    Pure function: no network, no state, no names in output.
    """
    text = payload.decode("utf-8", "replace").strip()
    if not text:
        return {}
    out = {}
    # JSON / JSONL
    if text.startswith(("[", "{")):
        try:
            doc = json.loads(text)
        except ValueError:
            # Fall through to JSONL attempt below.
            doc = None
        if isinstance(doc, dict):
            for key in ("incidents", "data", "reports", "results"):
                if isinstance(doc.get(key), list):
                    doc = doc[key]
                    break
            else:
                return {}
        if isinstance(doc, list):
            for row in doc:
                if isinstance(row, dict):
                    iid = _incident_id(row)
                    if iid:
                        out[iid] = _row_hash(row)
            return out
        # JSONL: one object per line.
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict):
                iid = _incident_id(row)
                if iid:
                    out[iid] = _row_hash(row)
        return out
    # CSV: first line is the header; id column by name, else col 0.
    import csv
    import io
    try:
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            return {}
        for row in reader:
            row = {k: v for k, v in row.items() if k is not None}
            iid = _incident_id(row)
            if iid:
                out[iid] = _row_hash(row)
    except Exception:
        return {}
    return out


def parse_snapshot_listing(body: bytes) -> dict:
    """Parse the snapshots listing page into {(date, kind): url}.

    Keyed by (date, kind), NOT by date alone (F1): the live page
    lists both backup-20261026101519.tar.bz2 (tarball) and
    AIID_Excel_Export-20261026.xlsx (excel) under 2026-10-26, and
    a date-only key collapsed them to the Excel URL alone.
    HTML: anchor hrefs that look like snapshot downloads, with a
    YYYY-MM-DD date taken from the anchor text, the href, or the
    nearest preceding text on the same line. JSON listing: objects
    with a date + url/download field. Returns {} when nothing
    parseable is found (caller treats that as degraded, never a
    baseline). Pure function: no network, no state.
    """
    text = body.decode("utf-8", "replace")
    stripped = text.strip()
    if stripped.startswith(("{", "[")):
        try:
            doc = json.loads(stripped)
        except ValueError:
            doc = None
        if isinstance(doc, list):
            entries = doc
        elif isinstance(doc, dict):
            entries = None
            for key in ("snapshots", "data", "results", "exports"):
                if isinstance(doc.get(key), list):
                    entries = doc[key]
                    break
            if entries is None:
                return {}
        else:
            return {}
        out = {}
        for row in entries:
            if not isinstance(row, dict):
                continue
            url = None
            for key in ("url", "download_url", "href", "link", "file"):
                if isinstance(row.get(key), str) and row[key].strip():
                    url = row[key].strip()
                    break
            date = None
            for key in ("date", "snapshot_date", "created", "published"):
                if isinstance(row.get(key), str):
                    m = _DATE_RE.search(row[key])
                    if m:
                        date = m.group(1)
                        break
            if url and date:
                if not url.startswith("http"):
                    url = urllib.parse.urljoin(SNAPSHOTS_URL, url)
                out[(date, _snapshot_kind(url))] = url
        return out
    # HTML path.
    import urllib.parse
    out = {}
    for m in _HREF_RE.finditer(text):
        href, inner = m.group(1).strip(), m.group(2)
        if not _SNAPSHOT_HREF_RE.search(href):
            continue
        label = _TAG_RE.sub(" ", inner).strip()
        date_m = _DATE_RE.search(label) or _DATE_RE.search(href)
        if not date_m:
            # Nearest date on the same line before the anchor.
            line_start = text.rfind("\n", 0, m.start()) + 1
            date_m = _DATE_RE.search(text[line_start:m.start()])
        if not date_m:
            continue
        url = href
        if not url.startswith("http"):
            url = urllib.parse.urljoin(SNAPSHOTS_URL, url)
        out[(date_m.group(1), _snapshot_kind(url))] = url
    return out


def diff_snapshots(old: dict, new: dict) -> tuple:
    """Diff snapshot-entry maps {entry_key: {url, ...}}.

    entry_key is the "date|kind" state key (see _entry_key); the
    function itself is key-agnostic. Returns (new_keys,
    changed_keys, vanished_keys). A tarball-URL change now fires
    independently of the Excel URL for the same date (F1). Pure.
    """
    new_keys = sorted(k for k in new if k not in old)
    changed_keys = sorted(
        k for k in new if k in old
        and new[k].get("url") != old[k].get("url"))
    vanished_keys = sorted(k for k in old if k not in new)
    return new_keys, changed_keys, vanished_keys


def diff_incidents(old: dict, new: dict) -> tuple:
    """Diff incident maps {id: row_hash}.

    Returns (new_ids, changed_ids). Pure.
    """
    new_ids = sorted(i for i in new if i not in old)
    changed_ids = sorted(i for i in new if i in old and new[i] != old[i])
    return new_ids, changed_ids


def _blank_state() -> dict:
    return {"schema_version": STATE_VERSION, "updated_at": utcnow_iso(),
            "snapshots": {}, "incidents": {},
            "consecutive_gaps": 0, "last_seen_snapshot_date": None}


def _load_state():
    """Returns (state, fresh_baseline).

    fresh_baseline is True when no state existed or the load failed
    (quarantined). In both cases the run re-baselines with ZERO hits.
    """
    if not os.path.exists(STATE_PATH):
        return _blank_state(), True
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
        if (not isinstance(state, dict)
                or state.get("schema_version") != STATE_VERSION
                or not isinstance(state.get("snapshots"), dict)
                or not isinstance(state.get("incidents"), dict)):
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
        _report("state_corrupt",
                f"state load failed ({type(e).__name__}); quarantined, "
                f"re-baselining with zero hits",
                {"quarantined_as": qname})
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


def _fetch_listing() -> tuple:
    """One GET of the hardcoded snapshots listing page.

    Returns (body|None, note). note: ok, http_429, http_error_<code>,
    redirect_not_chased, final_url_mismatch, unexpected_content_type,
    capped_2MB, transport_<ExcName>. Transport errors get max 1
    retry; HTTP statuses and 429 are not retried. No cookies, no
    auth, no POST, no redirect chase.
    """
    req = urllib.request.Request(SNAPSHOTS_URL, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/json,*/*;q=0.8",
    })
    attempts = 0
    while True:
        attempts += 1
        try:
            resp = _OPENER.open(req, timeout=TIMEOUT)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return None, "http_429"
            if 300 <= e.code < 400:
                return None, "redirect_not_chased"
            return None, f"http_error_{e.code}"
        except Exception as e:
            if attempts <= MAX_RETRIES:
                time.sleep(REQUEST_SPACING)
                continue
            return None, f"transport_{type(e).__name__}"
        try:
            if resp.status == 429:
                return None, "http_429"
            if resp.status != 200:
                if 300 <= resp.status < 400:
                    return None, "redirect_not_chased"
                return None, f"http_error_{resp.status}"
            if resp.geturl() != SNAPSHOTS_URL:
                return None, "final_url_mismatch"
            ctype = resp.headers.get_content_type()
            if ctype not in ("text/html", "application/json",
                             "text/plain"):
                return None, f"unexpected_content_type_{ctype}"
            chunks, total = [], 0
            capped = False
            while True:
                c = resp.read(CHUNK)
                if not c:
                    break
                total += len(c)
                if total > MAX_BODY:
                    capped = True
                    break
                chunks.append(c)
            body = b"".join(chunks)
            return body, ("capped_2MB" if capped else "ok")
        finally:
            try:
                resp.close()
            except Exception:
                pass


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False,
         snapshot_incidents: dict | None = None):
    """Diff the AIID weekly snapshot listing against stored state.

    Returns hit dicts (grade SECONDARY, IDs + URLs only, no names).

    since_hours is accepted for contract compliance but does not
    filter: newness comes from the state diff, not a time window.
    snapshot_incidents is an optional {incident_id: row_hash} map
    supplied by the ingest worker after it downloads and parses a
    new snapshot archive (this module never downloads archives
    itself); when supplied, incident-level new/changed hits are
    emitted and state.incidents is updated. When None (the cron
    default), only listing-level snapshot hits are emitted.
    --dry-run performs ZERO network calls, reads no config, and
    touches no state and no error log.
    """
    if seen_ids is None:
        seen_ids = set()
    observed_at = utcnow_iso()

    if dry_run:
        print("[dry-run] aiid: GET " + SNAPSHOTS_URL +
              " (passive GET only, no redirects, no cookies, no auth, "
              "no POST; login-gated list page never touched)",
              file=sys.stderr)
        print(f"[dry-run] aiid: state {STATE_PATH} (read on live run, "
              f"created on first live run; untouched by dry-run)",
              file=sys.stderr)
        print("[dry-run] aiid: hits would be aiid.snapshot.new / "
              "aiid.snapshot.changed (listing diff) and, only when an "
              "ingest worker supplies snapshot_incidents, "
              "aiid.incident.new / aiid.incident.changed",
              file=sys.stderr)
        return []

    try:
        cfg = load_config()
    except Exception:
        # Missing/unreadable config == disabled (fail closed).
        cfg = {}
    if not (cfg.get("aiid") or {}).get("enabled", False):
        print("[aiid] disabled (config 'aiid'.enabled is not true); "
              "refusing live scan", file=sys.stderr)
        return []

    state, silent = _load_state()
    if silent:
        print("[aiid] (re)baselining: recording listing, zero hits "
              "this run", file=sys.stderr)

    body, note = _fetch_listing()
    if note == "http_429":
        _report("rate_limited_429",
                "snapshots listing returned 429; hard stop for this run",
                {"url": SNAPSHOTS_URL, "http_status": 429})
        return []
    if body is None or note not in ("ok", "capped_2MB"):
        # Degraded fetch: never a hit, never a re-baseline, state
        # listing untouched. F2: on a fresh baseline (silent) do
        # NOT persist at all — saving a blank baseline would make
        # the next successful run report every historical snapshot
        # date (200+ back to 2021) as new. Only an existing state
        # gets its gap counter incremented and saved; a fresh run
        # stays fresh (no state file is created) and re-baselines
        # on the next successful run. This also covers a corrupt-
        # state quarantine followed by a degraded fetch, since
        # _load_state returns silent=True for quarantined state.
        if not silent:
            state["consecutive_gaps"] = int(
                state.get("consecutive_gaps", 0)) + 1
            _save_state(state)
        _report("fetch_gap",
                f"snapshots listing degraded ({note}); not a hit, "
                f"state listing untouched"
                + ("; fresh baseline not persisted" if silent else ""),
                {"url": SNAPSHOTS_URL, "note": note,
                 "consecutive_gaps": state["consecutive_gaps"]})
        return []

    entries = parse_snapshot_listing(body)
    if not entries:
        # Same F2 rule as above: zero-entry parse on a fresh
        # baseline persists nothing.
        if not silent:
            state["consecutive_gaps"] = int(
                state.get("consecutive_gaps", 0)) + 1
            _save_state(state)
        _report("fetch_gap",
                "snapshots listing parsed to zero entries; not a hit, "
                "state listing untouched"
                + ("; fresh baseline not persisted" if silent else ""),
                {"url": SNAPSHOTS_URL,
                 "consecutive_gaps": state["consecutive_gaps"]})
        return []
    state["consecutive_gaps"] = 0

    # F1: (date, kind) tuple keys from the parser become "date|kind"
    # state keys here (JSON cannot hold tuple keys). The tarball
    # and Excel entries for one Monday are now separate entries.
    new_entries = {_entry_key(d, k): {"url": u,
                                      "anchor_hash": _sha256(
                                          f"{d}|{k}|{u}".encode("utf-8"))}
                   for (d, k), u in entries.items()}
    old_entries = state.get("snapshots", {})
    new_keys, changed_keys, vanished_keys = diff_snapshots(
        old_entries, new_entries)
    if vanished_keys:
        _report("listing_entry_vanished",
                "snapshot entries vanished from listing (logged only, "
                "never a hit)",
                {"url": SNAPSHOTS_URL, "entries": ",".join(vanished_keys)})

    hits = []

    def _mk_hit(indicators, confidence, summary, source_url, extra):
        return _scrub(make_hit(
            lane=LANE,
            source_url=source_url,
            indicators_matched=indicators,
            confidence=confidence,
            summary=summary,
            provenance=_scrub({
                "method": "passive GET of public weekly snapshot "
                          "listing; no login, no session, no cookies, "
                          "no auth, no POST; redirects not chased; "
                          "login-gated incidents list page never touched",
                "listing_url": SNAPSHOTS_URL,
                "retrieved_at": observed_at,
                "grade_basis": "AIID is a curated database citing "
                               "press and other reports, not a "
                               "first-hand observation",
            }),
            observed_at=observed_at,
            extra=extra,
            grade=GRADE,
        ))

    if not silent:
        for ekey in new_keys:
            date, kind = _split_entry_key(ekey)
            key = redact_secrets(f"aiid:snapshot:{ekey}:new")[1]
            if is_new(seen_ids, key):
                hits.append(_mk_hit(
                    ["aiid.snapshot.new"], "MEDIUM",
                    f"[aiid] new weekly snapshot {date} ({kind})",
                    new_entries[ekey]["url"],
                    {"snapshot_date": date,
                     "snapshot_kind": kind,
                     "snapshot_url": new_entries[ekey]["url"]}))
                mark_seen(seen_ids, key)
        for ekey in changed_keys:
            date, kind = _split_entry_key(ekey)
            key = redact_secrets(f"aiid:snapshot:{ekey}:changed")[1]
            if is_new(seen_ids, key):
                hits.append(_mk_hit(
                    ["aiid.snapshot.changed"], "MEDIUM",
                    f"[aiid] snapshot {date} ({kind}) download URL changed",
                    new_entries[ekey]["url"],
                    {"snapshot_date": date,
                     "snapshot_kind": kind,
                     "snapshot_url": new_entries[ekey]["url"],
                     "previous_url": old_entries[ekey].get("url")}))
                mark_seen(seen_ids, key)
        if snapshot_incidents is not None:
            old_inc = state.get("incidents", {})
            new_ids, changed_ids = diff_incidents(old_inc,
                                                  snapshot_incidents)
            for iid in new_ids:
                key = redact_secrets(f"aiid:incident:{iid}:new")[1]
                if is_new(seen_ids, key):
                    # source_url stays the listing page: this module
                    # does not assert a per-incident page URL shape.
                    hits.append(_mk_hit(
                        ["aiid.incident.new"], "MEDIUM",
                        f"[aiid] new incident {iid}",
                        SNAPSHOTS_URL,
                        {"incident_id": iid}))
                    mark_seen(seen_ids, key)
            for iid in changed_ids:
                key = redact_secrets(f"aiid:incident:{iid}:changed")[1]
                if is_new(seen_ids, key):
                    hits.append(_mk_hit(
                        ["aiid.incident.changed"], "LOW",
                        f"[aiid] incident {iid} record changed",
                        SNAPSHOTS_URL,
                        {"incident_id": iid}))
                    mark_seen(seen_ids, key)
            state["incidents"] = dict(snapshot_incidents)

    state["snapshots"] = new_entries
    if new_entries:
        # Date part only: with "date|kind" keys, max() alone would
        # also compare kinds; take the max date explicitly.
        state["last_seen_snapshot_date"] = max(
            _split_entry_key(k)[0] for k in new_entries)
    _save_state(state)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("AIID weekly-snapshot diff (public listing only; "
                      "no login, no list page, no POST)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
