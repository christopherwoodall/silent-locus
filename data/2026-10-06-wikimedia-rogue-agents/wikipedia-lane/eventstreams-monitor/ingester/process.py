#!/usr/bin/env python3
# =============================================================================
# process.py — EventStreams SSE line processor (stdin only, NO network)
#
# TRANSPORT CONSTRAINT (this VM): Python HTTP stacks (httpx/urllib) break on
# the egress proxy; curl works. The persistent SSE connection MUST be owned by
# curl (`curl -N -s <stream-url>`), which pipes raw stream bytes into this
# script via stdin. This module never opens a socket, never imports anything
# that does on import, and is safe to unit-test offline.
#
# Input : raw EventStreams SSE text on stdin (`data: {...}` lines; comment
#         lines like `:heartbeat` and blank lines are ignored).
# Output: one JSON line per accepted event, appended to per-hour UTC files:
#           <out-dir>/raw/YYYY-MM-DD/HH.jsonl
#         The hour is derived from the EVENT's own timestamp (epoch `timestamp`
#         or ISO `meta.dt`), not wall clock — replay-safe.
# Diagnostics go to stderr (never mixed into the JSONL evidence files).
#
# SSE resume: `id:` lines are captured as the resume cursor and checkpointed
# to --event-id-file (on every heartbeat and on close); ingest.sh sends the
# cursor back as `Last-Event-ID` on reconnect (DESIGN.md §7).
#
# Supported event schemas (best-effort normalization):
#   - recentchange  (stream.wikimedia.org/v2/stream/recentchange):
#       {wiki, title, type, timestamp(epoch), user, comment, ...}
#   - revision-create (stream.wikimedia.org/v2/stream/revision-create):
#       {meta:{domain, dt}, page_title, page_namespace, rev_id,
#        performer:{user_text}, ...}
# Raw event bytes are stored verbatim (no redaction, no field dropping).
# =============================================================================

import json
import os
import re
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# SSE parsing
# ---------------------------------------------------------------------------

def parse_sse_line(line):
    """Parse one raw SSE text line.

    Returns the decoded event dict for `data: {...}` lines, or None for
    heartbeat comments (`:heartbeat`), blank lines, and malformed payloads
    (the caller counts those as errors, not events).
    """
    if not line:
        return None
    s = line.strip()
    if not s:
        return None
    if s.startswith(':'):
        return None                      # SSE comment / :heartbeat
    if not s.startswith('data:'):
        return None                      # id:, event:, retry: lines — not events
    payload = s[5:].strip()
    if not payload:
        return None
    try:
        ev = json.loads(payload)
    except json.JSONDecodeError:
        return None
    return ev if isinstance(ev, dict) else None


# ---------------------------------------------------------------------------
# Schema normalization (recentchange + revision-create)
# ---------------------------------------------------------------------------

def _meta_dt_to_epoch(dt):
    """Parse ISO-8601 `meta.dt` to epoch seconds; None on failure."""
    if not dt or not isinstance(dt, str):
        return None
    try:
        s = dt.replace('Z', '+00:00') if dt.endswith('Z') else dt
        return datetime.fromisoformat(s).timestamp()
    except ValueError:
        return None


def normalize(ev):
    """Best-effort canonical accessor for both schemas.

    Returns {'wiki', 'title', 'user', 'event_type', 'timestamp'} where
    timestamp is epoch seconds (float) or None if unrecoverable.
    """
    # recentchange shape
    if 'wiki' in ev:
        return {
            'wiki': ev.get('wiki'),
            'title': ev.get('title'),
            'user': ev.get('user'),
            'event_type': ev.get('type'),
            'timestamp': ev.get('timestamp'),
        }
    # revision-create / page-delete shape
    meta = ev.get('meta') or {}
    # Prefer the canonical dbname when present: domain derivation misfires for
    # e.g. www.wikidata.org ('wwwiki' instead of 'wikidatawiki').
    wiki = ev.get('database')
    if not wiki:
        domain = meta.get('domain', '')
        if isinstance(domain, str) and domain:
            # e.g. en.wikipedia.org -> enwiki
            if domain.endswith('.wikipedia.org'):
                wiki = domain[:-len('.wikipedia.org')] + 'wiki'
            elif domain == 'commons.wikimedia.org':
                wiki = 'commonswiki'
            elif domain.endswith('.wikimedia.org'):
                # meta.wikimedia.org -> metawiki (canonical dbname = stem + 'wiki')
                wiki = domain[:-len('.wikimedia.org')] + 'wiki'
    performer = ev.get('performer') or {}
    stream = meta.get('stream') or ''
    if 'rev_id' in ev:
        # page-delete events also carry rev_id (head rev at delete) — tell
        # them apart from revision-create via the stream name.
        event_type = 'page-delete' if 'page-delete' in stream else 'revision-create'
    else:
        event_type = ev.get('type')
    return {
        'wiki': wiki,
        'title': ev.get('page_title') or ev.get('title'),
        'user': performer.get('user_text') or ev.get('user'),
        'event_type': event_type,
        'timestamp': ev.get('timestamp') or _meta_dt_to_epoch(meta.get('dt')),
    }


def event_hour_path(ts, out_root):
    """Map epoch timestamp to the rotation path raw/YYYY-MM-DD/HH.jsonl (UTC).

    `ts` None/unparseable -> current UTC hour (live stream shouldn't hit this;
    replay of schema-drifted events might).
    """
    if ts is None:
        dt = datetime.now(timezone.utc)
    else:
        try:
            dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
        except (ValueError, TypeError, OverflowError, OSError):
            dt = datetime.now(timezone.utc)
    return os.path.join(
        out_root, 'raw', dt.strftime('%Y-%m-%d'), dt.strftime('%H') + '.jsonl'
    )


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def make_filter(wikis, title_pattern):
    """Build a predicate; None args mean 'accept everything'."""
    title_re = re.compile(title_pattern) if title_pattern else None
    wiki_set = set(wikis) if wikis else None

    def accept(norm):
        if wiki_set is not None and norm.get('wiki') not in wiki_set:
            return False
        if title_re is not None and not title_re.search(norm.get('title') or ''):
            return False
        return True

    return accept


# ---------------------------------------------------------------------------
# Stream processor
# ---------------------------------------------------------------------------

class Processor:
    def __init__(self, out_root, accept=None, heartbeat_interval=1000,
                 log=sys.stderr, event_id_file=None):
        self.out_root = out_root
        self.accept = accept or (lambda norm: True)
        self.heartbeat_interval = heartbeat_interval
        self.log = log
        # SSE resume cursor: path of the file holding the last seen `id:` line.
        # ingest.sh reads it and sends it back as `Last-Event-ID` on reconnect.
        self.event_id_file = event_id_file
        self.last_event_id = None
        self.counts = {'events': 0, 'accepted': 0, 'filtered': 0,
                       'malformed': 0}
        self._current_path = None
        self._current_fh = None

    def _emit(self, msg):
        print(msg, file=self.log, flush=True)

    def _write_event_id(self):
        """Persist the SSE resume cursor. Best-effort: warn, never raise."""
        if not self.event_id_file or not self.last_event_id:
            return
        try:
            parent = os.path.dirname(self.event_id_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            tmp = self.event_id_file + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as fh:
                fh.write(self.last_event_id + '\n')
            os.replace(tmp, self.event_id_file)
        except OSError as exc:
            self._emit('warn: could not write event-id file: %s' % exc)

    def _fh_for(self, path):
        if path != self._current_path:
            if self._current_fh:
                self._current_fh.close()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self._current_fh = open(path, 'a', encoding='utf-8')
            self._current_path = path
        return self._current_fh

    def handle_line(self, line):
        """Process one raw SSE line. Returns True if an event was stored."""
        s = line.strip()
        if s.startswith('id:'):
            # SSE event id — the resume cursor (DESIGN.md §7). Not an event.
            val = s[3:].strip()
            if val:
                self.last_event_id = val
            return False
        ev = parse_sse_line(line)
        if ev is None:
            # Distinguish malformed data: payloads from `data:` lines only.
            if s.startswith('data:') and s[5:].strip():
                self.counts['malformed'] += 1
                self._emit('warn: malformed data line skipped')
            return False
        self.counts['events'] += 1
        norm = normalize(ev)
        if not self.accept(norm):
            self.counts['filtered'] += 1
            return False
        fh = self._fh_for(event_hour_path(norm.get('timestamp'),
                                          self.out_root))
        fh.write(json.dumps(ev, ensure_ascii=False) + '\n')
        self.counts['accepted'] += 1
        n = self.counts['events']
        if self.heartbeat_interval and n % self.heartbeat_interval == 0:
            self._write_event_id()   # checkpoint the resume cursor
            self._emit('heartbeat: events=%d accepted=%d filtered=%d '
                       'malformed=%d current_file=%s'
                       % (n, self.counts['accepted'], self.counts['filtered'],
                          self.counts['malformed'], self._current_path))
        return True

    def close(self):
        """Flush and close the current hour file. Idempotent."""
        self._write_event_id()        # final cursor checkpoint
        if self._current_fh:
            self._current_fh.flush()
            self._current_fh.close()
            self._current_fh = None
            self._current_path = None

    def run(self, stream):
        """Consume an iterable of raw text lines until exhaustion."""
        try:
            for line in stream:
                self.handle_line(line)
        finally:
            self.close()


# ---------------------------------------------------------------------------
# CLI (thin wrapper; all logic lives above and is import-testable)
# ---------------------------------------------------------------------------

def _parse_args(argv):
    import argparse
    p = argparse.ArgumentParser(description='EventStreams SSE stdin processor')
    p.add_argument('--out-dir', default='.',
                   help='root under which raw/YYYY-MM-DD/HH.jsonl is written')
    p.add_argument('--wikis', default='',
                   help='comma-separated wiki filter, e.g. enwiki,metawiki '
                        '(empty = all wikis)')
    p.add_argument('--title-regex', default='',
                   help='regex filter applied to the page title '
                        '(empty = all titles)')
    p.add_argument('--heartbeat', type=int, default=1000,
                   help='log a heartbeat line to stderr every N events')
    p.add_argument('--event-id-file', default=None,
                   help='persist the last seen SSE event id here (resume '
                        'cursor; ingest.sh sends it back as Last-Event-ID)')
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    accept = make_filter([w for w in args.wikis.split(',') if w] or None,
                         args.title_regex or None)
    proc = Processor(out_root=args.out_dir, accept=accept,
                     heartbeat_interval=args.heartbeat,
                     event_id_file=args.event_id_file)
    proc.run(sys.stdin)


if __name__ == '__main__':
    main()
