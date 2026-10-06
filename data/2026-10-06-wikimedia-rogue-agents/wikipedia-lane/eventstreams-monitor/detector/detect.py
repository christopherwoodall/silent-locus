#!/usr/bin/env python3
"""EventStreams detection engine — Wikimedia rogue-agent monitor (offline build).

BUILD-ONLY: this script must NOT be run against live data / live EventStreams.
It evaluates hand-written JSONL fixtures (see tests/fixtures/) against the
data-driven rules in rules.yaml and emits alerts as JSONL.

Usage:
    python3 detect.py [options] [FILE|-]
      FILE: path to a JSONL event batch; '-' or omitted reads stdin.
    Options:
      --rules PATH        rules.yaml location (default: alongside this script)
      --state-file PATH   JSON state file for stateful (burst) rules
      --in-memory         do not persist burst state (default behavior)
      --pretty            pretty-print alert JSON

Alert schema (one JSON object per line on stdout):
    {"ts": <event ts>, "rule": <rule name>, "severity": <sev>,
     "wiki": ..., "user": ..., "title": ...,
     "evidence": {...}, "provenance": {"finding": ..., "source_file": ..., "grade": ...}}

Exit codes: 0 = success (alerts or not); 2 = malformed input (bad JSON line /
missing required fields) with a clear stderr message.

Input event schema (normalized; see README.md for the full mapping):
    {"ts": "2026-06-25T20:28:27Z", "wiki": "meta.wikimedia.org",
     "user": "~2026-36867-71", "title": "Web2Cit/data/com/arcgis/geocode/templates.json",
     "namespace": 0, "comment": "...", "tags": ["mw-reverted"],
     "content": "<added text>", "is_new": true}

The normalizer also accepts raw EventStreams `revision-create` event shapes
(mapping meta.dt→ts, page_title→title, rev_content→content, etc.).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))

URL_RE = re.compile(r"https?://([^/\s\"'<>]+)", re.IGNORECASE)

# --------------------------------------------------------------------------- #
# Event normalization
# --------------------------------------------------------------------------- #

REQUIRED_FIELDS = ("ts", "wiki", "user", "title")


def parse_ts(ts):
    """Parse an ISO-8601 timestamp to an aware datetime. Raises ValueError."""
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    s = str(ts).strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def normalize_event(raw):
    """Map a fixture event OR a raw EventStreams revision-create event to the
    normalized schema. Raises ValueError on malformed events."""
    if not isinstance(raw, dict):
        raise ValueError(f"event is not a JSON object: {type(raw).__name__}")

    meta = raw.get("meta") or {}
    # Detect raw EventStreams shape (has meta.uri / meta.dt) vs fixture shape.
    is_es = isinstance(meta, dict) and ("uri" in meta or "dt" in meta)

    ev = {
        "ts": raw.get("ts", meta.get("dt")),
        "wiki": raw.get("wiki"),
        "user": raw.get("user", raw.get("user_text")),
        "title": raw.get("title", raw.get("page_title")),
        "namespace": raw.get("namespace", raw.get("page_namespace", 0)),
        "comment": raw.get("comment", "") or "",
        "tags": raw.get("tags", []),
        "content": raw.get("content", raw.get("rev_content", "") or ""),
        "is_new": bool(raw.get("is_new", raw.get("rev_parent_id") == 0)),
    }
    # tags may arrive as a comma-separated string (MediaWiki API style).
    if isinstance(ev["tags"], str):
        ev["tags"] = [t for t in ev["tags"].split(",") if t]
    ev["tags"] = list(ev["tags"] or [])

    missing = [f for f in REQUIRED_FIELDS if not ev.get(f)]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
    try:
        ev["_dt"] = parse_ts(ev["ts"])
    except (ValueError, TypeError) as exc:
        raise ValueError(f"bad timestamp {ev['ts']!r}: {exc}")
    # Normalize comment/content to str.
    ev["comment"] = str(ev["comment"])
    ev["content"] = str(ev["content"])
    return ev


# --------------------------------------------------------------------------- #
# State (burst rules only)
# --------------------------------------------------------------------------- #

def load_state(path):
    """State file format (JSON object):
        {"<rule-name>": [{"ts": iso, "wiki": w, "user": u, "title": t}, ...], ...}
    Each list holds recent candidate events for that burst rule, pruned to the
    rule's window on every run. Created if missing; corrupt state is a hard error.
    """
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path) as fh:
            state = json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"cannot load state file {path!r}: {exc}")
    if not isinstance(state, dict):
        raise ValueError(f"state file {path!r} is not a JSON object")
    return state


def save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(state, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)


# --------------------------------------------------------------------------- #
# Web2Cit title → domain derivation
# --------------------------------------------------------------------------- #

def web2cit_domain_from_title(title):
    """Reverse the title's full DNS path per Web2Cit/Docs/Storage (observed in
    the 2026-10-06 census, followups/web2cit-namespace/catalog.tsv):
      Web2Cit/data/ar/com/pagina12/www/templates.json -> www.pagina12.com.ar
      Web2Cit/data/com/go/abcnews/templates.json     -> abcnews.go.com
      Web2Cit/data/com/arcgis/services/templates.json -> services.arcgis.com
      Web2Cit/data/com/arcgis/templates.json          -> arcgis.com
    Returns the domain or None if the title does not start with Web2Cit/data/.
    Suffix-aware allowlist matching (domain_allowed) means host variants like
    www.pagina12.com.ar are covered by the pagina12.com.ar census entry."""
    prefix = "Web2Cit/data/"
    if not title.startswith(prefix):
        return None
    parts = title[len(prefix):].split("/")
    if len(parts) < 3:  # need at least tld + domain + file leaf
        return None
    labels = parts[:-1]  # drop the file leaf (templates.json / tests.json / ...)
    if not all(re.fullmatch(r"[A-Za-z0-9-]+", lab) for lab in labels):
        return None
    return ".".join(reversed(labels)).lower()


def domain_allowed(domain, allowlist):
    """Allowlist hit if the domain or any parent suffix is listed
    (www.example.com is covered by example.com)."""
    d = domain.lower().rstrip(".")
    while d:
        if d in allowlist:
            return True
        if "." not in d:
            break
        d = d.split(".", 1)[1]
    return False


def load_allowlist(path):
    domains = set()
    with open(path) as fh:
        for line in fh:
            line = line.strip().lower()
            if not line or line.startswith("#"):
                continue
            domains.add(line)
    return domains


# --------------------------------------------------------------------------- #
# Rule evaluators
# --------------------------------------------------------------------------- #

class RuleContext:
    """Per-rule mutable state handed to the evaluator each batch."""

    def __init__(self, rule, rules_dir, state, state_file):
        self.rule = rule
        self.params = rule.get("params", {}) or {}
        self.events = []  # (dt, event) for the current batch + persisted state
        # Rehydrate persisted burst state.
        for item in state.get(rule["name"], []):
            try:
                dt = parse_ts(item["ts"])
            except (ValueError, TypeError, KeyError):
                continue  # skip corrupt entries, don't die on state
            self.events.append((dt, {
                "ts": item["ts"], "wiki": item.get("wiki", ""),
                "user": item.get("user", ""), "title": item.get("title", ""),
            }))
        # Lazily loaded by the allowlist rule.
        self._allowlist = None
        self._rules_dir = rules_dir

    @property
    def allowlist(self):
        if self._allowlist is None:
            p = self.params.get("allowlist_file")
            if not p:
                raise ValueError("rule %r: missing params.allowlist_file" % self.rule["name"])
            full = p if os.path.isabs(p) else os.path.join(self._rules_dir, p)
            self._allowlist = load_allowlist(full)
        return self._allowlist


def make_alert(rule, event, evidence):
    prov = rule.get("provenance", {}) or {}
    return {
        "ts": event["ts"],
        "rule": rule["name"],
        "severity": rule.get("severity", "info"),
        "wiki": event["wiki"],
        "user": event["user"],
        "title": event["title"],
        "evidence": evidence,
        "provenance": {
            "finding": prov.get("incident_finding", ""),
            "source_file": prov.get("source_file", ""),
            "grade": prov.get("claim_grade", ""),
        },
    }


def _burst_window_hits(ctx, predicate, n, window):
    """Generic sliding-window burst evaluator. Returns (fired_dt, hits)."""
    window = timedelta(minutes=window)
    now = ctx.events[-1][0] if ctx.events else None
    # Group by wiki; evaluate per wiki.
    by_wiki = {}
    for dt, ev in ctx.events:
        if predicate(ev):
            by_wiki.setdefault(ev["wiki"], []).append((dt, ev))
    for wiki, items in by_wiki.items():
        items.sort(key=lambda x: x[0])
        # Prune to events within the window of the latest candidate.
        latest = items[-1][0]
        inwin = [(dt, ev) for dt, ev in items if latest - dt <= window]
        if len(inwin) >= n:
            return wiki, inwin
    return None, []


def eval_temp_account_burst(ctx):
    p = ctx.params
    n = p.get("n", 5)
    window = p.get("window_minutes", 10)
    temp_re = re.compile(p.get("temp_account_regex", r"~20\d{2}-\d+-\d+"))
    pred = lambda ev: bool(temp_re.search(ev.get("user", "")))
    wiki, hits = _burst_window_hits(ctx, pred, n, window)
    if wiki:
        return [make_alert(ctx.rule, hits[-1][1], {
            "window_minutes": window,
            "temp_account_events_in_window": len(hits),
            "distinct_users": sorted({h[1]["user"] for h in hits}),
            "titles": [h[1]["title"] for h in hits[-n:]],
        })]
    return []


def eval_sandbox_edit_burst(ctx):
    p = ctx.params
    n = p.get("n", 3)
    window = p.get("window_minutes", 15)
    temp_re = re.compile(p.get("temp_account_regex", r"~20\d{2}-\d+-\d+"))
    sb_re = re.compile(p.get("sandbox_title_regex", r"(?i)(^|:|/)Sandbox"))
    pred = lambda ev: bool(temp_re.search(ev.get("user", ""))) and bool(sb_re.search(ev.get("title", "")))
    wiki, hits = _burst_window_hits(ctx, pred, n, window)
    if wiki:
        return [make_alert(ctx.rule, hits[-1][1], {
            "window_minutes": window,
            "sandbox_events_in_window": len(hits),
            "distinct_users": sorted({h[1]["user"] for h in hits}),
            "titles": [h[1]["title"] for h in hits[-n:]],
        })]
    return []


def eval_title_prefix(ctx, events):
    prefixes = ctx.params.get("title_prefixes", [])
    alerts = []
    for ev in events:
        for pre in prefixes:
            if ev["title"].startswith(pre):
                alerts.append(make_alert(ctx.rule, ev, {
                    "matched_prefix": pre,
                    "comment": ev["comment"],
                    "tags": ev["tags"],
                }))
                break
    return alerts


def eval_web2cit_target_allowlist(ctx, events):
    prefixes = ctx.params.get("title_prefixes", ["Web2Cit/data/"])
    check_title = ctx.params.get("check_title_domain", True)
    check_content = ctx.params.get("check_content_urls", True)
    allow = ctx.allowlist
    alerts = []
    for ev in events:
        if not any(ev["title"].startswith(pre) for pre in prefixes):
            continue
        bad = []
        if check_title:
            dom = web2cit_domain_from_title(ev["title"])
            if dom and not domain_allowed(dom, allow):
                bad.append({"source": "title", "domain": dom})
        if check_content:
            for m in URL_RE.finditer(ev["content"]):
                host = m.group(1).split(":")[0].lower()
                if not domain_allowed(host, allow):
                    bad.append({"source": "content_url", "domain": host, "url": m.group(0)[:200]})
        if bad:
            # Dedupe by domain, keep first observation each.
            seen, uniq = set(), []
            for b in bad:
                if b["domain"] not in seen:
                    seen.add(b["domain"])
                    uniq.append(b)
            alerts.append(make_alert(ctx.rule, ev, {
                "non_allowlisted_domains": uniq,
                "allowlist_size": len(allow),
            }))
    return alerts


def eval_content_pattern(ctx, events):
    patterns = ctx.params.get("patterns", [])
    fields = ctx.params.get("scan_fields", ["comment", "content"])
    flags = 0 if ctx.params.get("case_sensitive", False) else re.IGNORECASE
    compiled = []
    for spec in patterns:
        try:
            compiled.append((spec, re.compile(spec["pattern"], flags)))
        except re.error as exc:
            raise ValueError(f"rule {ctx.rule['name']!r}: bad regex {spec.get('pattern')!r}: {exc}")
    alerts = []
    for ev in events:
        hits = []
        for spec, rx in compiled:
            for field in fields:
                text = ev.get(field) or ""
                m = rx.search(text)
                if m:
                    hits.append({"pattern_label": spec.get("label", spec["pattern"]),
                                 "field": field,
                                 "match": m.group(0)[:120],
                                 "note": spec.get("note", "")})
                    break  # one hit per pattern per event is enough
        if hits:
            alerts.append(make_alert(ctx.rule, ev, {"pattern_hits": hits}))
    return alerts


def eval_comment_shape(ctx, events):
    p = ctx.params
    prefixes = p.get("title_prefixes", [])
    empty_ok = p.get("flag_empty_comment", True)
    machine_res = [re.compile(x, re.IGNORECASE) for x in p.get("machine_comment_patterns", [])]
    sus_tags = set(p.get("suspicious_tags", []))
    alerts = []
    for ev in events:
        if not any(ev["title"].startswith(pre) for pre in prefixes):
            continue  # scoped to config trees; article edits must NOT fire
        reasons = []
        if empty_ok and not ev["comment"].strip():
            reasons.append({"signal": "empty_comment",
                            "note": "config-tree edit with no edit summary"})
        for rx in machine_res:
            if rx.search(ev["comment"].strip()):
                reasons.append({"signal": "machine_shaped_comment",
                                "comment": ev["comment"][:120],
                                "pattern": rx.pattern})
                break
        tagged = sorted(sus_tags.intersection(ev["tags"]))
        if tagged:
            reasons.append({"signal": "suspicious_tags", "tags": tagged})
        if reasons:
            alerts.append(make_alert(ctx.rule, ev, {"signals": reasons}))
    return alerts


EVALUATORS = {
    "temp_account_burst": lambda ctx, events: eval_temp_account_burst(ctx),
    "sandbox_edit_burst": lambda ctx, events: eval_sandbox_edit_burst(ctx),
    "title_prefix": eval_title_prefix,
    "web2cit_target_allowlist": eval_web2cit_target_allowlist,
    "content_pattern": eval_content_pattern,
    "comment_shape": eval_comment_shape,
}


# --------------------------------------------------------------------------- #
# Batch driver
# --------------------------------------------------------------------------- #

def run_batch(events, rules, rules_dir, state, state_file, out):
    """Evaluate all rules over one batch. Returns alert count."""
    count = 0
    for rule in rules:
        rtype = rule.get("type")
        if rtype not in EVALUATORS:
            raise ValueError(f"rule {rule.get('name')!r}: unknown type {rtype!r}")
        ctx = RuleContext(rule, rules_dir, state, state_file)
        # Feed current batch into burst windows.
        if rtype in ("temp_account_burst", "sandbox_edit_burst"):
            for ev in events:
                ctx.events.append((ev["_dt"], ev))
            alerts = EVALUATORS[rtype](ctx, events)
            # Persist pruned window for next batch.
            if state_file is not None:
                window = timedelta(minutes=ctx.params.get("window_minutes", 10))
                latest = max(dt for dt, _ in ctx.events) if ctx.events else None
                kept = []
                if latest:
                    for dt, ev in ctx.events:
                        if latest - dt <= window:
                            kept.append({"ts": ev["ts"], "wiki": ev["wiki"],
                                         "user": ev["user"], "title": ev["title"]})
                state[rule["name"]] = kept
        else:
            alerts = EVALUATORS[rtype](ctx, events)
        for a in alerts:
            out.write(json.dumps(a, ensure_ascii=False) + "\n")
            count += 1
    return count


def main(argv=None):
    ap = argparse.ArgumentParser(description="Wikimedia rogue-agent EventStreams detector (offline)")
    ap.add_argument("input", nargs="?", default="-", help="JSONL event batch file ('-' = stdin)")
    ap.add_argument("--rules", default=os.path.join(HERE, "rules.yaml"))
    ap.add_argument("--state-file", default=None,
                    help="JSON state file for burst rules (default: in-memory only)")
    ap.add_argument("--in-memory", action="store_true", default=True,
                    help="do not persist burst state (default)")
    ap.add_argument("--persist", action="store_true",
                    help="persist burst state to --state-file (requires --state-file)")
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args(argv)

    try:
        import yaml
    except ImportError:
        print("detect.py: PyYAML is required (python3 -c 'import yaml')", file=sys.stderr)
        return 3

    try:
        with open(args.rules) as fh:
            rules_doc = yaml.safe_load(fh)
        rules = rules_doc.get("rules", [])
        if not isinstance(rules, list) or not rules:
            raise ValueError("rules.yaml contains no rules")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"detect.py: cannot load rules: {exc}", file=sys.stderr)
        return 2

    if args.input == "-":
        fh = sys.stdin
    else:
        try:
            fh = open(args.input)
        except OSError as exc:
            print(f"detect.py: cannot open input: {exc}", file=sys.stderr)
            return 2

    events = []
    try:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {lineno}: invalid JSON: {exc}")
            try:
                events.append(normalize_event(raw))
            except ValueError as exc:
                raise ValueError(f"line {lineno}: {exc}")
    except ValueError as exc:
        print(f"detect.py: malformed input: {exc}", file=sys.stderr)
        return 2
    finally:
        if fh is not sys.stdin:
            fh.close()

    # Burst state defaults to in-memory; an explicit --state-file persists it.
    state_file = args.state_file if (args.persist or args.state_file) else None
    try:
        state = load_state(state_file)
    except ValueError as exc:
        print(f"detect.py: {exc}", file=sys.stderr)
        return 2

    rules_dir = os.path.dirname(os.path.abspath(args.rules))
    try:
        if args.pretty:
            import io
            buf = io.StringIO()
            n = run_batch(events, rules, rules_dir, state, state_file, buf)
            for line in buf.getvalue().splitlines():
                print(json.dumps(json.loads(line), indent=2, ensure_ascii=False))
        else:
            n = run_batch(events, rules, rules_dir, state, state_file, sys.stdout)
    except ValueError as exc:
        print(f"detect.py: rule evaluation error: {exc}", file=sys.stderr)
        return 2

    if state_file:
        try:
            save_state(state_file, state)
        except OSError as exc:
            print(f"detect.py: cannot write state file: {exc}", file=sys.stderr)
            return 2

    print(f"detect.py: {len(events)} events, {n} alerts", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
