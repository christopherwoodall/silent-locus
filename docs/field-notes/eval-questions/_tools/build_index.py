#!/usr/bin/env python3
"""Build EVAL_QUESTIONS.md index from the enriched per-eval files. stdlib only."""
import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from enrich import EVALS, SOURCE_URL, domain_of

ROOT = os.path.expanduser('~/workspace/silent-locus/collections/eval-questions')

def load(ev):
    with open(f'{ROOT}/{ev}/questions-enriched.jsonl', encoding='utf-8') as f:
        return [json.loads(l) for l in f]

def main():
    data = {ev: load(ev) for ev in EVALS}
    total = sum(len(v) for v in data.values())
    assert total == 10201, total

    corp_topics = Counter()
    corp_domains = Counter()
    markers = Counter()
    for ev in EVALS:
        for r in data[ev]:
            corp_topics[r['topic']] += 1
            for s in r['expected_sources']:
                d = s['domain_or_url']
                if not d:
                    markers[s['why']] += 1
                elif d.startswith('selfhosted:'):
                    corp_domains[d] += 1
                else:
                    corp_domains[domain_of(d)] += 1

    L = []
    A = L.append
    A('# EVAL Questions — Unified Corpus (W3 enrichment)')
    A('')
    A(f'**Records:** {total} across 11 evals (DeepSearchQA banked separately, untouched). '
      'Enriched 2026-10-05 by `_tools/enrich.py` (stdlib only).')
    A('')
    A('## Corpus totals')
    A('')
    A('| eval | questions | license |')
    A('|---|---|---|')
    for ev in EVALS:
        A(f"| {ev} | {len(data[ev])} | {data[ev][0]['license']} |")
    A('')
    A('### Topic distribution (top 15, corpus-wide)')
    A('')
    for t, c in corp_topics.most_common(15):
        A(f'- {t}: {c}')
    A('')
    A('### Expected-source domains (top 20, corpus-wide)')
    A('')
    A('(Marker entries with empty `domain_or_url` and `selfhosted:*` env tags excluded '
      'from domain counts; marker totals below.)')
    A('')
    for d, c in corp_domains.most_common(20):
        A(f'- {d}: {c}')
    A('')
    A('### Empty-source markers (why the list is empty)')
    A('')
    for w, c in markers.most_common():
        A(f'- `{w}`: {c}')
    A('')
    A('---')

    random.seed(7)
    for ev in EVALS:
        recs = data[ev]
        A('')
        A(f'## {ev}')
        A('')
        A(f'- **Questions:** {len(recs)}')
        A(f'- **License:** {recs[0]["license"]}')
        A(f'- **Source:** {SOURCE_URL[ev]}')
        A(f'- **Retrieved:** {recs[0]["retrieved"]}')
        A('')
        A('**Topic distribution (top 10):**')
        A('')
        for t, c in Counter(r['topic'] for r in recs).most_common(10):
            A(f'- {t}: {c}')
        A('')
        A('**Most common expected-source domains (top 15):**')
        A('')
        dc = Counter()
        mk = Counter()
        for r in recs:
            for s in r['expected_sources']:
                d = s['domain_or_url']
                if not d:
                    mk[s['why']] += 1
                elif d.startswith('selfhosted:'):
                    dc[d] += 1
                else:
                    dc[domain_of(d)] += 1
        for d, c in dc.most_common(15):
            A(f'- {d}: {c}')
        if mk:
            A('')
            A('**Markers:** ' + ', '.join(f'`{w}`: {c}' for w, c in mk.most_common()))
        A('')
        A('**Examples:**')
        A('')
        for r in random.sample(recs, 3):
            A(f'- Q ({r["question_id"]}, topic={r["topic"]}): '
              f'{r["question"][:220]}')
            A(f'  sources: {", ".join(s["domain_or_url"] or "[" + s["why"] + "]" for s in r["expected_sources"])}')
            for fp in r['fingerprint_phrases']:
                A(f'  fp: "{fp}"')
        A('')

    A('---')
    A('')
    A('## Method notes')
    A('')
    A('### Topic assignment')
    A('- **Metadata first:** openai-simpleqa (`metadata.topic`), sealqa (`topic`), '
      'mind2web (`subdomain`→`domain`), tau-bench (`airline`/`retail` kept as-is), '
      'webvoyager (`web_name`, the site itself), webwalkerqa (`info.domain` as fallback). '
      'Metadata values normalized to a canonical label set '
      '(sports, politics, science, history, geography, tech, finance, health, '
      'entertainment, gov-policy, food, travel, shopping, education, other).')
    A('- **Keyword-rule fallback** for google-facts-grounding, google-frames '
      '(its `reasoning_types` is a reasoning category, not a topic), assistantbench, '
      'webarena (its `sites` are environments), webwalkerqa, openai-mle-bench '
      '(classified on the competition slug; `tech` fallback — all 82 are ML competitions), '
      'and mind2web records whose metadata is `Other`/`General`. '
      'Rules are ordered regex lists (politics → gov-policy → health → finance → science → '
      'history → geography → sports → entertainment → tech → food → travel → shopping); '
      'first match wins, else `other`. Which rule fired is not recorded per question. '
      'CJK questions (433 webwalkerqa + 2 simpleqa) use a separate ordered Chinese '
      'substring rule list covering the same labels plus `education`.')
    A('')
    A('### expected_sources')
    A('- `why="metadata"`: simpleqa (`metadata.urls`), sealqa (parquet `urls` column, '
      'decoded with `_tools/pqdec.py`), frames (`wiki_links`), mind2web (`website`, '
      'TLD-normalized: `aa`→`aa.com`, `sports.yahoo`→`sports.yahoo.com`, `nyc`→`nyc.gov`, '
      'known-TLD values kept), webvoyager (`web` site URL), webwalkerqa (`root_url` + '
      '`info.source_website`). Distinct article URLs kept (up to 3) even on one domain.')
    A('- `why="named-in-question"`: domains/URLs regex-extracted from the question text.')
    A('- `why="prior"`: conservative priors on QA evals only — en.wikipedia.org for '
      'wh-/how-many-style questions with no other source; official-site domains for a '
      'small brand map (apple, tesla, nasa, cdc, white house, …) when the brand is named; '
      'kaggle.com for mle-bench (agent traces hit competition pages per repo notes).')
    A('- `why="selfhosted"`: webarena tasks run against six self-hosted environments '
      '(shopping, shopping_admin, gitlab, map, reddit, wikipedia) — limited live-web '
      'trace value, flagged explicitly.')
    A('- Empty-list markers (single entry, `domain_or_url=""`): tau-bench '
      '`synthetic-policy-no-live-web` (165); facts-grounding '
      '`context-provided-no-web-needed` (553 — the grounding doc ships with the question); '
      'assistantbench `no-metadata-no-prior` (50 — gold_url/difficulty null in this release).')
    A('')
    A('### fingerprint_phrases')
    A('- Corpus-wide n-gram document frequency over word 4..8-grams across all 10,201 '
      'questions (1,089,394 unique n-grams). Per question, candidates scored by '
      '(df asc, length desc); up to 3 non-overlapping picked, relaxed to 2 with overlap '
      'if needed; guaranteed ≥1.')
    A('- Filters: no stopword-leading n-grams; ≤50% weak tokens; ≥1 content token '
      '(≥2 for 6+-grams); digit-bearing tokens dropped except 4-digit years; URL/email '
      'spans stripped before tokenizing (chopped URL tokens make bad verbatim phrases); '
      'CJK text tokenized per-character and treated as content (433 webwalkerqa + '
      '2 simpleqa questions), rejoined without spaces for verbatim search.')
    A('- Rationale: agents execute eval questions rather than pasting them, so probes '
      'target distinctive instruction fragments and named-entity + verb combos '
      '(e.g. "how many episodes of X aired") suitable for verbatim search on '
      'urlquery.net / urlscan / Google. High-df boilerplate (tau-bench instruction '
      'templates, mle-bench Kaggle boilerplate, webarena task templates) is '
      'automatically penalized by df.')
    A('')
    A('### Outputs')
    A('- `all-questions.jsonl`: unified corpus, one JSON object per line, schema '
      '`{"eval","eval_org","question_id","question","topic","expected_sources":'
      '[{"domain_or_url","why"}],"fingerprint_phrases":[...],"license","retrieved"}`.')
    A('- `<eval-slug>/questions-enriched.jsonl`: per-eval enriched copies (provenance).')
    A('- Raw sources and `questions.jsonl` were read, never modified. Scripts: '
      '`_tools/enrich.py`, `_tools/build_index.py`.')

    with open(f'{ROOT}/EVAL_QUESTIONS.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print(f'wrote EVAL_QUESTIONS.md ({len(L)} lines)')
    print('corpus topics top15:', corp_topics.most_common(15))
    print('corpus domains top20:', corp_domains.most_common(20))
    print('markers:', dict(markers))

if __name__ == '__main__':
    main()
