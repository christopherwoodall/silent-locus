#!/usr/bin/env python3
"""Build events.jsonl + rollup.jsonl for data/2026-07-10-paste-ubuntu-cn.

Reads raw/ source rows (termina.digital catalog rows, Centaur post texts,
sample-decode notes) and emits schema-conformant event records with
external-overlap annotations. Re-running reproduces events.jsonl byte-identically
(modulo the event.created timestamp, which is pinned below for determinism).

Per-paste records (3,484) are intentionally NOT built: the per-paste record
table and body bundle were unavailable at build time (termina.digital /pub/
returned HTTP 503 on 2026-10-05; absent from the joshuadavid repo).
See PROVENANCE.md.
"""
import json, hashlib, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, 'raw')
DATASET = '2026-07-10-paste-ubuntu-cn'
CREATED = '2026-10-05T08:00:00Z'  # pinned for reproducible builds

def fp(identity: str) -> str:
    return hashlib.sha256(identity.encode()).hexdigest()

def rec(ts, kind, identity, labels, description, **extra):
    r = {
        '@timestamp': ts,
        'event': {'dataset': DATASET, 'created': CREATED},
        'record_kind': kind,
        'fingerprint': fp(identity),
        'labels': labels,
        'confidence': 'confirmed',
        'description': description,
    }
    r.update(extra)
    return r

def raw_json(name):
    with open(os.path.join(RAW, name), encoding='utf-8') as f:
        return json.load(f)

def main():
    campaign = raw_json('terminadigital_campaign_xinzhai-2026-07.json')
    venue = raw_json('terminadigital_venue_paste-ubuntu-cn.json')
    actors = raw_json('terminadigital_actors_xz.json')
    evidence = raw_json('terminadigital_evidence_ubuntu-cn-crawl.json')

    ext = {  # external-overlap annotation block, attached to every record
        'external_overlap.source': 'joshuadavid/wikiagentswarminvestigation + swarm.termina.digital (ai-safety-lab, CC0-1.0)',
        'external_overlap.investigation_commit': 'c09593ffc904954fb4a9acae96b946d2d3c853e6',
        'external_overlap.catalog': 'swarm.termina.digital/db/ schema v8, data through 2026-09-08T01:30Z',
        'external_overlap.in_our_corpus': False,
    }

    recs = []

    # 1. venue rollup
    recs.append(rec(
        '2026-07-10T00:00:00Z', 'paste_venue_rollup', 'paste-ubuntu-cn:venue',
        {**ext,
         'venue.id': 'paste-ubuntu-cn', 'venue.host': 'paste.ubuntu.org.cn',
         'venue.software': 'pastebin-php', 'venue.pastes': 4756,
         'venue.handles': 600,
         'venue.top_handle': 'xz_knowledge_p1', 'venue.top_handle_count': 3484,
         'venue.first_seen': '2026-07-10', 'venue.last_seen': '2026-07-20',
         'venue.utc_offset': '+08:00', 'venue.status': 'live',
         'venue.body_limit_chars': 30000,
         'venue.encoding_quirks': 'form turns + into space in base64 bodies; sequential numeric ids',
         'venue.monthly.m2026_06': 122, 'venue.monthly.m2026_07': 4309,
         'venue.monthly.m2026_08': 316, 'venue.monthly.m2026_09': 9,
         'timestamp_source': 'labels:venue.first_seen (termina.digital venue row)',
         'attribution': 'unattributed'},
        'paste.ubuntu.org.cn: 4,756 pastes, 600 handles (2026-06-08..2026-09-05); '
        'top handle xz_knowledge_p1 x3,484; xz_improvement_plan_p1 x11; otherwise '
        'normal human traffic (APK-modder handles). Encoding quirks: paste form turns '
        '+ into space; sequential numeric IDs; 30,000-char body limit; site displays UTC+8.',
        source_url='https://paste.ubuntu.org.cn/',
        observer={'product': 'muse', 'type': 'research-agent', 'vendor': 'meta'},
    ))

    # 2. campaign temporal shape
    recs.append(rec(
        '2026-07-10T13:26:00Z', 'run_shape', 'paste-ubuntu-cn:xinzhai-campaign',
        {**ext,
         'campaign.id': 'xinzhai-2026-07', 'campaign.name': 'the xinzhai persistence run',
         'campaign.cohesion': 'probable', 'campaign.confidence': 'unattributed',
         'campaign.window_utc8': '2026-07-10 21:26 -> 2026-07-20',
         'phase.a_write_tests': '2026-07-10 21:26 UTC+8: 3x print(hello) under xinzhai',
         'phase.b_snapshots': '2026-07-10 21:32->22:43 UTC+8: 8 Fernet snapshots '
                              '(xinzhai_v5.2,v52,v60,v61,v70,v71,v72,v73), 4-14 parts of 30,000 chars, '
                              'plaintext 65KB->231KB monotonic',
         'phase.c_knowledge': '2026-07-10 22:24 -> 2026-07-20: 3,484 posts under xz_knowledge_p1, '
                              'pairs every 5-6 min, ten fixed sizes 124-572 chars (500-char cohort: 1,134)',
         'phase.d_plans': '2026-07-12 -> 2026-07-19: 11 posts x 864 chars under xz_improvement_plan_p1, ~6h apart',
         'timestamp_source': 'labels:campaign (phase-a start, UTC+8 -> 13:26Z)',
         'attribution': 'unattributed'},
        'xinzhai-2026-07: one operator, 4 phases over 2026-07-10..20 (UTC+8): write tests, '
        '8 growing Fernet snapshots, 3,484 paired 5-min knowledge posts, 11 six-hour plan posts. '
        'Reads as an agent persistence layer (memory/log/plan); operator, model, country unknown.',
    ))

    # 3. encoding finding (lane-4 verification)
    recs.append(rec(
        '2026-10-05T00:00:00Z', 'finding', 'paste-ubuntu-cn:encoding-verification',
        {**ext,
         'finding.topic': 'encoding',
         'finding.method': 'spaces-to-plus base64 decode of Centaur-published 124-char sample; characterization only, nothing executed',
         'finding.sample_sha256': hashlib.sha256(
             open(os.path.join(RAW, 'sample_decode_verification.txt'), 'rb').read()).hexdigest(),
         'encoding.snapshots': 'Fernet (python cryptography); header timestamps UTC (8h behind displayed UTC+8)',
         'encoding.knowledge_posts': 'headerless cipher, unique per message; sample -> 93 bytes, entropy 6.251 bits/byte, no gzip magic, no UTF-8, not Fernet',
         'encoding.plan_posts': '864 chars -> 648 bytes; cipher unidentified',
         'timestamp_source': 'lane:2026-10-05 (lane-4 analysis date)',
         'attribution': 'unattributed'},
        'Encoding verified: knowledge posts are spaces-to-plus base64 of 93-byte high-entropy '
        '(6.251 bits/byte) ciphertext — not plaintext, not gzip, not Fernet. Snapshots are Fernet '
        'with UTC header timestamps. Contents unrecovered in all phases.',
    ))

    # 4. cadence finding
    recs.append(rec(
        '2026-10-05T00:00:00Z', 'finding', 'paste-ubuntu-cn:cadence',
        {**ext,
         'finding.topic': 'cadence/pairing',
         'finding.structure': 'two posts, consecutive numeric IDs, seconds apart, repeating every ~5-6 min',
         'finding.arithmetic': '3484 posts ~= 1742 pairs over 2026-07-10 22:24 -> 2026-07-20 (~9.07d = 13061 min) '
                               '-> mean ~7.5 min/pair; consistent with sustained 5/6-min cadence breaking late',
         'finding.unresolved': 'whether the ten size cohorts have distinct cadences (needs per-paste record table)',
         'timestamp_source': 'lane:2026-10-05 (lane-4 analysis date)',
         'attribution': 'unattributed'},
        'Pairing: two consecutive-ID posts per ~5-6 min slot for ~10 days (mean ~7.5 min/pair incl. '
        'late breaks). Machine cadence, no diurnal pause. Cohort-vs-cadence mapping unresolved.',
    ))

    # 5. agent-vs-other assessment
    recs.append(rec(
        '2026-10-05T00:00:00Z', 'finding', 'paste-ubuntu-cn:agent-assessment',
        {**ext,
         'finding.topic': 'agent-vs-other',
         'finding.verdict': 'agent-shaped, unattributed, NOT the HF swarm',
         'finding.for_agent': 'machine cadence; fixed-size encrypted payloads; test->snapshot->stream->plan bootstrap; Fernet+Python; UTC encoder; scheduled plan posts',
         'finding.against_hf_link': 'own terminadigital campaign (xinzhai-2026-07, "a run, not a swarm"); Centaur third-behavioral-cluster; 10-day run vs 3-day HF burst; keyed blobs vs HF plaintext coordination',
         'finding.alternatives': 'personal encrypted backup pipeline / researcher monitor / devops heartbeat not excluded',
         'timestamp_source': 'lane:2026-10-05 (lane-4 analysis date)',
         'attribution': 'unattributed'},
        'Assessment: agent-shaped persistence layer, operator/model/country unknown (termina.digital '
        'confidence: unattributed; Centaur: agent involvement unresolved). Distinct from the HF swarm. '
        'Zero xz_knowledge hits in our own corpora.',
    ))

    # 6-8. report captures
    for ts, ident, title, url, pub, note in [
        ('2026-09-05T16:21:54Z', 'paste-ubuntu-cn:centaur-post-1',
         '1,142 encoded pastes on a Chinese Ubuntu pastebin (Jul 10-11, HF window): third behavioral cluster, contact declined',
         'https://thecolony.ai/post/c894f76a-c06a-47f3-8926-1a0a36b1e471', '2026-09-05',
         'first finding: 1,142 posts, pairs/5min, 124 chars, sample blob, contact declined'),
        ('2026-09-05T21:33:37Z', 'paste-ubuntu-cn:centaur-post-2',
         'termina round 2: xz series is 3,484 posts (my 1,142 corrected), probyte PUSH-grammar + 3 unvisited pastes + controls methodology',
         'https://thecolony.ai/post/de97aec6-e967-443f-8b76-d5ab65935068', '2026-09-05',
         'correction: 3,484 posts, ten size cohorts, Jul 10-20, 5/6-min cadence breaking late; agent involvement unresolved'),
        ('2026-09-08T00:00:00Z', 'paste-ubuntu-cn:joshuadavid-commit-c09593',
         'joshuadavid/wikiagentswarminvestigation commit c09593ffc904954fb4a9acae96b946d2d3c853e6: Read-only scrape of thecolony.ai + Centaur investigator trail',
         'https://github.com/joshuadavid/wikiagentswarminvestigation/commit/c09593ffc904954fb4a9acae96b946d2d3c853e6', '2026-09-08',
         'commit message + analyses/thecolony-ai/README.md: 3,484 posts by xz_knowledge_p1, Jul 10-11 HF window, 124 chars, encoded, pairs every 5 min'),
    ]:
        recs.append(rec(
            ts, 'report_capture', ident,
            {**ext, 'report.title': title, 'report.published': pub,
             'timestamp_source': 'labels:report.published (post/commit date)'},
            f'Investigator report: {title}. {note}',
            source_url=url,
        ))

    # 9-10. source references (termina.digital rows)
    recs.append(rec(
        '2026-09-08T01:30:00Z', 'source_reference', 'paste-ubuntu-cn:source-campaign-row',
        {**ext, 'source.table': 'campaign', 'source.row_id': 'xinzhai-2026-07',
         'source.license': 'CC0-1.0', 'source.schema': 'v8',
         'timestamp_source': 'labels:source (catalog data-through timestamp)'},
        'Termina.digital campaign row xinzhai-2026-07 (schema v8, CC0): full summary text preserved in '
        'raw/terminadigital_campaign_xinzhai-2026-07.json; cohesion probable, confidence unattributed.',
    ))
    recs.append(rec(
        '2026-09-05T00:00:00Z', 'source_reference', 'paste-ubuntu-cn:source-evidence-row',
        {**ext, 'source.table': 'evidence', 'source.row_id': 'ubuntu-cn-crawl',
         'source.license': 'CC0-1.0',
         'evidence.method': 'paste.ubuntu.org.cn ids 4548500 to 4552399, every page saved; author, tag, displayed time, length and head indexed',
         'evidence.retrieved_by': 'fable', 'evidence.retrieved_at': '2026-09-05',
         'timestamp_source': 'labels:source (evidence retrieved_at)'},
        'Termina.digital evidence row ubuntu-cn-crawl: paste IDs 4548500-4552399 (3,900 IDs) fully saved '
        '2026-09-05 by fable; author/tag/displayed-time/length/head indexed. Row preserved in raw/.',
        source_url='https://paste.ubuntu.org.cn/4548564',
    ))

    # 11. corpus negative
    recs.append(rec(
        '2026-10-05T00:00:00Z', 'corpus_grep_negative', 'paste-ubuntu-cn:corpus-grep-negative',
        {**ext,
         'sweep.indicator': 'xz_knowledge', 'sweep.query': 'xz_knowledge (case-insensitive)',
         'sweep.scopes': ['data/2026-10-01-oai-tag-sweep/events.jsonl',
                          'data/2026-10-03-openai-agent-traces/events.jsonl',
                          'full silent-locus tree'],
         'sweep.hits_own_corpus': 0,
         'sweep.hits_external_refs_only': True,
         'sweep.external_ref_paths': [
             'data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/ (joshuadavid investigation copies)'],
         'timestamp_source': 'lane:2026-10-05 (grep date)'},
        "Corpus grep 'xz_knowledge': 0 hits in our own corpora (oai-tag-sweep, openai-agent-traces, "
        'full tree). Only hits are lane3 ref copies of the joshuadavid investigation files — external '
        'overlap, not our observations. Honest negative: the series is new to our corpus.',
    ))

    with open(os.path.join(ROOT, 'events.jsonl'), 'w', encoding='utf-8') as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # rollup: one campaign-level row
    roll = rec(
        '2026-07-10T13:26:00Z', 'paste_venue_rollup', 'paste-ubuntu-cn:rollup',
        {**ext,
         'rollup.window': '2026-07-10 -> 2026-07-20 (UTC+8 displayed)',
         'rollup.handles.xz_knowledge_p1': 3484, 'rollup.handles.xz_improvement_plan_p1': 11,
         'rollup.handles.xinzhai_snapshot_versions': 8, 'rollup.handles.xinzhai_write_tests': 3,
         'rollup.total_xz_posts': 3495,
         'rollup.per_paste_ingested': False,
         'rollup.per_paste_blocker': 'termina.digital /pub/ HTTP 503 on 2026-10-05; record.jsonl + xz-ubuntu-cn-2026-09-05.tar.gz absent from joshuadavid repo',
         'timestamp_source': 'labels:campaign (phase-a start)',
         'attribution': 'unattributed'},
        'xinzhai run rollup: 3,495 xz-handle posts (+8 versioned snapshots in parts, +3 write tests) '
        'over 2026-07-10..20 on paste.ubuntu.org.cn. Per-paste records NOT ingested (source table unavailable); '
        'campaign/venue/actor/evidence-level records ingested with external-overlap annotations.',
    )
    roll['event']['dataset'] = DATASET + '-rollup'
    with open(os.path.join(ROOT, 'rollup.jsonl'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(roll, ensure_ascii=False) + '\n')

    print(f'wrote {len(recs)} events + 1 rollup')

if __name__ == '__main__':
    sys.exit(main())
