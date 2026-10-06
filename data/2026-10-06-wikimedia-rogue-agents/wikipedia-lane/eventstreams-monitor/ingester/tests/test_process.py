#!/usr/bin/env python3
# =============================================================================
# Offline fixture tests for the EventStreams ingester. NO NETWORK.
# Run:  python3 tests/test_process.py
# Exit code 0 = all pass, nonzero = failure (first failing assertion printed).
# =============================================================================

import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INGESTER = os.path.dirname(HERE)
sys.path.insert(0, INGESTER)
import process  # noqa: E402  (import-safe: no network on import by design)

FIX = os.path.join(HERE, 'fixtures')


def fixture_lines(name):
    with open(os.path.join(FIX, name), encoding='utf-8') as f:
        return f.read().splitlines()


def check(name, cond, detail=''):
    if not cond:
        print('FAIL: %s %s' % (name, detail))
        sys.exit(1)
    print('ok:   %s' % name)


# --- 1. SSE line parsing -----------------------------------------------------
check('heartbeat comment skipped',
      process.parse_sse_line(':heartbeat') is None)
check('blank line skipped',
      process.parse_sse_line('   ') is None)
check('id:/event: lines skipped',
      process.parse_sse_line('event: message') is None)
check('malformed json -> None (not exception)',
      process.parse_sse_line('data: {not json') is None)
check('non-dict payload -> None',
      process.parse_sse_line('data: [1,2,3]') is None)
check('valid data line parses',
      process.parse_sse_line('data: {"a": 1}') == {'a': 1})


# --- 2. Schema normalization -------------------------------------------------
rc_lines = [l for l in fixture_lines('recentchange-edit.sse')
            if l.startswith('data:')]
rc_ev = process.parse_sse_line(rc_lines[0])
n = process.normalize(rc_ev)
check('recentchange wiki', n['wiki'] == 'enwiki', n)
check('recentchange title', n['title'] == 'User:~2026-28355-02/sandbox', n)
check('recentchange user', n['user'] == '~2026-28355-02', n)
check('recentchange epoch', n['timestamp'] == 1791251970, n)

def data_lines(name):
    return [l for l in fixture_lines(name) if l.startswith('data:')]


rev_ev = process.parse_sse_line(data_lines('revision-create.sse')[0])
n2 = process.normalize(rev_ev)
check('revision-create wiki derived from meta.domain',
      n2['wiki'] == 'metawiki', n2)
check('revision-create title', n2['title'] == 'Web2Cit/data/ArcGIS.json', n2)
check('revision-create user', n2['user'] == '~2026-36867-71', n2)
check('revision-create epoch from meta.dt',
      abs(n2['timestamp'] - 1791252900) < 1, n2)

lu_ev = process.parse_sse_line(data_lines('newusers-log.sse')[0])
n3 = process.normalize(lu_ev)
check('newusers log type preserved', n3['event_type'] == 'log', n3)
check('newusers epoch', n3['timestamp'] == 1791252005, n3)


# --- 3. Rotation: events land in the right UTC hour files --------------------
with tempfile.TemporaryDirectory() as tmp:
    p = process.Processor(out_root=tmp, heartbeat_interval=0)
    for name in ('recentchange-edit.sse', 'newusers-log.sse',
                 'revision-create.sse'):
        for line in fixture_lines(name):
            p.handle_line(line)
    p.close()

    f01 = os.path.join(tmp, 'raw', '2026-10-06', '01.jsonl')
    f02 = os.path.join(tmp, 'raw', '2026-10-06', '02.jsonl')
    check('hour-01 file exists', os.path.isfile(f01))
    check('hour-02 file exists', os.path.isfile(f02))

    ev01 = [json.loads(l) for l in open(f01, encoding='utf-8')]
    ev02 = [json.loads(l) for l in open(f02, encoding='utf-8')]
    check('hour-01 holds both 01:59 events', len(ev01) == 2,
          'got %d' % len(ev01))
    check('hour-02 holds log + revision-create', len(ev02) == 2,
          'got %d' % len(ev02))
    check('raw event stored verbatim',
          ev01[0].get('title') == 'User:~2026-28355-02/sandbox'
          and '$schema' in ev01[0])

    c = p.counts
    check('counts: events=4 accepted=4 malformed=1',
          c['events'] == 4 and c['accepted'] == 4
          and c['malformed'] == 1 and c['filtered'] == 0, c)


# --- 4. Wiki + title filtering ------------------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    accept = process.make_filter(['metawiki'], 'Web2Cit')
    p = process.Processor(out_root=tmp, accept=accept, heartbeat_interval=0)
    for name in ('recentchange-edit.sse', 'newusers-log.sse',
                 'revision-create.sse'):
        for line in fixture_lines(name):
            p.handle_line(line)
    p.close()
    got = []
    for root, _, files in os.walk(os.path.join(tmp, 'raw')):
        for fn in files:
            for l in open(os.path.join(root, fn), encoding='utf-8'):
                got.append(json.loads(l))
    check('wiki+title filter keeps only revision-create',
          len(got) == 1 and got[0].get('rev_id') == 30732701, got)
    check('filtered count', p.counts['filtered'] == 3, p.counts)


# --- 5. Empty filters = accept everything ------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    p = process.Processor(out_root=tmp,
                          accept=process.make_filter(None, None),
                          heartbeat_interval=0)
    n_lines = sum(p.handle_line(l) for l in fixture_lines('revision-create.sse'))
    p.close()
    check('no filters accepts revision-create', n_lines == 1)


# --- 6. Close is idempotent; run() consumes a stream --------------------------
with tempfile.TemporaryDirectory() as tmp:
    p = process.Processor(out_root=tmp, heartbeat_interval=0)
    p.run(iter(fixture_lines('newusers-log.sse')))
    p.close()
    p.close()  # must not raise
    check('run()+double-close ok', True)


print('\nALL TESTS PASSED')
