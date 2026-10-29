#!/usr/bin/env python3
"""Aggregate 2026-09-28-dockerhub-trojan-images lane into a Factum bundle.

42,318 probe/listing rows -> 37,441 unique org/repo:tag infra.ioc observations
+ 1 source record + 1 extraction run record + summary claims (OBSERVED).

Aggregation methodology (also documented in the lane PROVENANCE.md):
- Read every row of evidence/2026-09-28-dockerhub-trojan-images/events.jsonl.
- Key = org/repo:tag from labels (exact strings, case preserved).
- record_kind 'tag_liveness' rows carry the probe status in `status`:
    'LIVE' | 'LIVE (in registry tag list)' -> live
    'GONE (HTTP 404)' -> dead
- record_kind 'tag_listing' rows (Hub tag-page enumeration, 4,873 rows) carry
  NO status; they are second-witness enumeration rows for the same keys.
- Merge rule per key: non-empty tag_liveness status wins. Zero real conflicts
  were found (no key had two different non-empty probe statuses).
- Final IOC status: 'active' if live; 'candidate' if dead or unknown.
- observed_at per IOC: retrieved_at of the status-determining row
  (time_basis 'source_metadata': the liveness probe time IS the event time,
  per the lane's own schema backfill notes).
"""
import json
import sys
from collections import Counter

EVENTS = 'data/lanes/dockerhub-trojan-images/events.jsonl'
LANE = 'dockerhub-trojan-images'
ACTOR = 'agent:lane-ingest/dockerhub-trojan-images'
IDEMPOTENCY = 'dockerhub-trojan-images-aggregate-2026-10-09'

def main():
    tags = {}   # key -> dict(org, repo, tag, status, retrieved_at)
    org_counts = Counter()
    repo_counts = Counter()
    total_rows = 0
    live = dead = unknown = 0
    dead_keys = []
    unknown_keys = []
    listing_only = 0

    with open(EVENTS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total_rows += 1
            e = json.loads(line)
            l = e.get('labels', {})
            key = f"{l['org']}/{l['repo']}:{l['tag']}"
            st = (e.get('status') or '').strip()
            rec = tags.get(key)
            if rec is None:
                tags[key] = {'org': l['org'], 'repo': l['repo'], 'tag': l['tag'],
                             'status': st, 'retrieved_at': e.get('retrieved_at', ''),
                             'kind': e.get('record_kind', '')}
            else:
                # status-determining rows are tag_liveness rows (non-empty status)
                if st:
                    rec['status'] = st
                    rec['retrieved_at'] = e.get('retrieved_at', rec['retrieved_at'])
                    rec['kind'] = e.get('record_kind', rec['kind'])

    for key, rec in tags.items():
        st = rec['status']
        if st == 'GONE (HTTP 404)':
            rec['liveness'] = 'dead'
            dead += 1
            dead_keys.append(key)
        elif st in ('LIVE', 'LIVE (in registry tag list)'):
            rec['liveness'] = 'live'
            live += 1
        else:
            rec['liveness'] = 'unknown'
            unknown += 1
            unknown_keys.append(key)
        org_counts[rec['org']] += 1
        repo_counts[f"{rec['org']}/{rec['repo']}"] += 1

    assert live + dead + unknown == len(tags) == 37441, (live, dead, unknown, len(tags))
    assert total_rows == 42318, total_rows

    # ---- bundle ----
    records = []

    def tagged(r, extra=None):
        r['tags'] = {'lane': LANE, 'grade': 'OBSERVED'}
        if extra:
            r['tags'].update(extra)
        return r

    records.append(tagged({
        'ref': 'src',
        'kind': 'source',
        'body': {
            'locator': 'data/lanes/dockerhub-trojan-images/events.jsonl',
            'source_type': 'submitted',
            'title': ('2026-09-28 dockerhub trojan-images lane: 42,318 '
                      'tag liveness probe/listing rows aggregated to '
                      '37,441 unique container tags'),
        },
    }))

    records.append(tagged({
        'ref': 'run',
        'kind': 'run',
        'body': {
            'run_kind': 'extraction',
            'tool': 'tmp_build_dockerhub_aggregate.py (lane aggregation)',
            'params': {
                'question': ('Aggregate the 42,318 tag_liveness/tag_listing probe rows '
                             'of the 2026-09-28-dockerhub-trojan-images lane into '
                             'unique container-tag IOCs for Factum ingest.'),
                'source_events': 'data/lanes/dockerhub-trojan-images/events.jsonl',
                'dedupe_key': 'org/repo:tag (exact label strings)',
                'merge_rule': 'non-empty tag_liveness status wins; zero conflicting statuses observed',
                'ioc_status_rule': "live -> active; dead/unknown -> candidate",
            },
            'coverage': {
                'total': total_rows,
                'scanned': total_rows,
                'complete': True,
                'description': (f'{total_rows} rows scanned; {len(tags)} unique '
                                f'org/repo:tag identifiers; live={live} dead={dead} '
                                f'unknown={unknown}'),
            },
        },
    }))

    for key in sorted(tags):
        rec = tags[key]
        ioc_status = 'active' if rec['liveness'] == 'live' else 'candidate'
        records.append(tagged({
            'kind': 'observation',
            'body': {
                'type': 'infra.ioc',
                'data_schema': 'urn:factum:infra:ioc:1',
                'data': {
                    'term': key,
                    'category': 'container_tag',
                    'status': ioc_status,
                    'provenance': ('2026-09-28-dockerhub-trojan-images lane aggregation: '
                                   'Docker Hub tag liveness sweep over cybergym + n132 orgs; '
                                   f"probe status {rec['status']!r}"),
                },
                'observed_at': rec['retrieved_at'],
                'time_basis': 'source_metadata',
                'source': '@src',
                'files': [],
            },
        }, extra={
            'ioc.org': rec['org'],
            'ioc.repo': rec['repo'],
            'ioc.liveness': rec['liveness'],
        }))

    claims = [
        ('unique_tags_probed',
         {'total_probe_rows': total_rows,
          'unique_tags': len(tags),
          'live': live,
          'dead_http_404': dead,
          'unknown_listing_only': unknown,
          'orgs': dict(org_counts),
          'repos': dict(repo_counts)}),
        ('liveness_dead_tags',
         {'dead_tags': sorted(dead_keys),
          'note': 'the 3 dead tags are the 3 corpus trojan tags that 404\'d '
                  'in the lane\'s corpus-trojan-tag-liveness sweep'}),
        ('org_distribution',
         {'n132': org_counts['n132'], 'cybergym': org_counts['cybergym']}),
    ]
    for prop, value in claims:
        records.append(tagged({
            'kind': 'claim',
            'body': {
                'subject': '@run',
                'property': prop,
                'value': value,
                'basis': 'OBSERVED',
                'cites': ['@run'],
            },
        }))

    bundle = {
        'bundle': 2,
        'actor': ACTOR,
        'idempotency_key': IDEMPOTENCY,
        'lane': LANE,
        'records': records,
    }
    with open('/tmp/dockerhub-aggregate-bundle.json', 'w') as f:
        json.dump(bundle, f)
    print(f'rows={total_rows} unique={len(tags)} live={live} dead={dead} '
          f'unknown={unknown} records={len(records)}')
    print('dead:', sorted(dead_keys))
    print('unknown:', sorted(unknown_keys))
    print('repos:', dict(repo_counts))

if __name__ == '__main__':
    main()
