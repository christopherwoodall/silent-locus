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


# --- 7. SSE resume cursor (Last-Event-ID) -------------------------------------
with tempfile.TemporaryDirectory() as tmp:
    eid_file = os.path.join(tmp, 'state', 'recentchange.last_event_id')
    p = process.Processor(out_root=tmp, heartbeat_interval=0,
                          event_id_file=eid_file)
    p.handle_line('id: 12345')
    check('id: line captured as cursor (not an event)',
          p.last_event_id == '12345' and p.counts['events'] == 0)
    p.handle_line('data: {"a": 1}')
    p.close()
    with open(eid_file, encoding='utf-8') as fh:
        check('cursor checkpointed to event-id file on close',
              fh.read().strip() == '12345')

with tempfile.TemporaryDirectory() as tmp:
    eid_file = os.path.join(tmp, 'no-cursor.last_event_id')
    p = process.Processor(out_root=tmp, heartbeat_interval=0,
                          event_id_file=eid_file)
    p.handle_line('data: {"a": 1}')
    p.close()
    check('no cursor seen -> no event-id file written',
          not os.path.exists(eid_file))


# --- 8. Wiki derivation prefers `database`; page-delete event typing ---------
rc_db = {'meta': {'uri': 'x', 'dt': '2026-10-06T02:15:00Z',
                  'domain': 'www.wikidata.org',
                  'stream': 'mediawiki.revision-create'},
         'database': 'wikidatawiki',
         'page_title': 'Q42', 'rev_id': 5,
         'performer': {'user_text': '~2026-40000-01'}}
n4 = process.normalize(rc_db)
check('database beats domain derivation', n4['wiki'] == 'wikidatawiki', n4)

pd = {'meta': {'uri': 'x', 'dt': '2026-10-06T02:15:00Z',
               'domain': 'meta.wikimedia.org',
               'stream': 'mediawiki.page-delete'},
      'database': 'metawiki', 'page_title': 'Web2Cit/data/com/arcgis/templates.json',
      'page_namespace': 4, 'rev_id': 30732700,
      'performer': {'user_text': 'Pppery'}}
n5 = process.normalize(pd)
check('page-delete typed correctly (not revision-create)',
      n5['event_type'] == 'page-delete' and n5['wiki'] == 'metawiki', n5)
check('page-delete performer user', n5['user'] == 'Pppery', n5)


print('\nALL TESTS PASSED')
