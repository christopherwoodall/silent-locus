#!/usr/bin/env python3
"""Build data/2026-08-25-commonlog-scan/messages.jsonl — one doc per commonlog.ai message (explicit events).

Source: raw/stream.sse captured 2026-09-28 via GET /stream (read-only SSE catch-up).
No posts, no accounts, no submissions. Hosted Elastic writes frozen — disk only.
"""
import json, re, hashlib, datetime, collections, os

BASE = os.path.dirname(os.path.abspath(__file__))
msgs = json.load(open(os.path.join(BASE, 'raw', 'messages.json')))
msgs.sort(key=lambda m: m['seq'])

TESTS = {
    'zz_label': re.compile(r'\bzz\b', re.I),
    'epoch_nonce': re.compile(r'\b1[678]\d{9}(?:\.\d+)?\b'),
    'transfer_grammar': re.compile(r'xfer|transfer.test|TRANSFER|REPLY_PAYLOAD', re.I),
    'proxy_ladder': re.compile(r'jqp|pure\.md|md\.succ\.ai|r\.jina\.ai|allorigins|markdown\.new', re.I),
    'nsi_stats': re.compile(r'nsi\.bg|infostat|pxweb', re.I),
    'relay_bridge': re.compile(r'relay|bridge', re.I),
    'goimport': re.compile(r'go-import', re.I),
    'webhook': re.compile(r'web_hook|webhook', re.I),
    'shortener': re.compile(r'goto\.unm\.edu|u\.ethz\.ch|go\.uvm\.edu|popcat|vanderbi\.lt|t\.mdcdev\.me|yourls', re.I),
    'swarm_ref': re.compile(r'swarm', re.I),
}
# Manually reviewed false positives: (pattern, seq) -> reason.
# All reviewed against full message bodies 2026-09-28. None shows swarm operations.
FALSE_POSITIVES = {
    # "transfer" as in handoff/state-transfer protocol essays, "transient" substring
    ('transfer_grammar', 39): 'restart identity contract essay (lineage/authority/trust)',
    ('transfer_grammar', 41): 'cross-family judging essay (eval methodology)',
    ('transfer_grammar', 43): 'handoff responsibility-transfer essay (Multica bug)',
    ('transfer_grammar', 46): 'skill-bundle handoff essay (Multica bug)',
    ('transfer_grammar', 266): '"transient failures" substring; agent-email delivery essay',
    # "webhook" in evidence-lineage philosophy essay
    ('webhook', 50): 'evidence-lineage essay ("unauthenticated webhook" as example ingress)',
    # "relay"/"bridge": commonlog's own email bridge + operator service-type docs
    ('relay_bridge', 2): 'operator service-type definition (bridge as a service)',
    ('relay_bridge', 8): 'operator story: commonlog email bridge build',
    ('relay_bridge', 9): 'operator principles: mail bridge example',
    ('relay_bridge', 50): 'evidence-lineage essay ("compromised relay" as example)',
    ('relay_bridge', 60): 'QA runtime bridge commit note',
    ('relay_bridge', 120): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 140): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 160): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 180): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 200): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 220): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 243): 'Grand Survey: Relay karma-weighted admission (survey series)',
    ('relay_bridge', 262): 'commonlog email-bridge guide',
    ('relay_bridge', 263): 'commonlog email-bridge guide',
    ('relay_bridge', 265): 'commonlog email-bridge guide',
    ('relay_bridge', 267): 'commonlog email-bridge guide',
    ('relay_bridge', 268): 'commonlog email-bridge guide',
    ('relay_bridge', 269): 'commonlog email-bridge guide',
    ('relay_bridge', 279): 'tide_scribe watch log ("oxtr nostr relay" venue note)',
    # "swarm" substring: scare-story reference in a watch log
    ('swarm_ref', 275): 'tide_scribe: "scare-stories about agents swarming old wikis" (meta)',
}

now = '2026-09-28T20:30:00+00:00'
out = []
for m in msgs:
    c = m['content'] or ''
    hits = sorted(n for n, rx in TESTS.items() if rx.search(c))
    fp = sorted(h for h in hits if (h, m['seq']) in FALSE_POSITIVES)
    real = sorted(h for h in hits if h not in fp)
    fp_reasons = {h: FALSE_POSITIVES[(h, m['seq'])] for h in fp}
    fp2 = hashlib.sha256(c.encode()).hexdigest()
    ts = datetime.datetime.fromtimestamp(m['ts'] / 1000, datetime.UTC).isoformat()
    doc = {
        'record_kind': 'log_message',
        'event': {'dataset': 'commonlog-scan', 'created': now},
        'observer': {'product': 'lane-commonlog-scan', 'vendor': 'hunt', 'type': 'read-only-sweep'},
        'retrieved_via': 'read-only GET /stream (SSE catch-up); no posts, no accounts, no submissions',
        'fingerprint': fp2,
        'labels': {
            'venue': 'commonlog.ai',
            'source_url': m['url'],
            'message_id': m['id'],
            'seq': m['seq'],
            'author': m['author'],
            'author_url': m['author_url'],
            'posted_utc': ts,
            'title': c.split('\n')[0][:120],
            'body_chars': len(c),
            'marker_hits_raw': hits,
            'marker_hits_false_positive': fp,
            'false_positive_reasons': fp_reasons,
            'marker_hits_true': real,
            'verdict': 'clean' if not real else 'REVIEW:' + ','.join(real),
        },
    }
    out.append(doc)

with open(os.path.join(BASE, 'messages.jsonl'), 'w') as f:
    for d in out:
        f.write(json.dumps(d, ensure_ascii=False) + '\n')

# corpus stats for the note
days = collections.Counter(
    datetime.datetime.fromtimestamp(m['ts'] / 1000, datetime.UTC).strftime('%Y-%m-%d') for m in msgs)
authors = collections.Counter(m['author'] for m in msgs)
print('docs:', len(out))
print('seq:', msgs[0]['seq'], '-', msgs[-1]['seq'])
print('days:', len(days), 'authors:', len(authors))
print('docs with true hits:', sum(1 for d in out if d['labels']['marker_hits_true']))
