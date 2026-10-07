# Common schema proposal — Transluce findings × our corpus

## The three shapes in play

| | Transluce `/api/findings` | Our `events.jsonl` | Raw captures (urlquery / arquivo.pt) |
|---|---|---|---|
| Grain | One **finding** = analyst synthesis over many observations | One **observation** = single record (report, commit, capture) | One **artifact** = fetched bytes |
| Envelope | id, created_at, updated_at, submitter, submitter_id, sensitive, form_version | @timestamp, event{ dataset, created }, record_kind, fingerprint | retrieval timestamp, source URL, method, sha256 |
| Content | data{ summary, description, evidence_links[], data_zip, untapped_source, cyberattack[], government, ai_company } | labels{...per-kind fields...}, description, confidence | raw bytes + provenance note |
| Identity | server-assigned id | fingerprint (sha256 of canonical form) | sha256 of bytes |

## Verdict: yes — two grains, one envelope

The shapes are complementary, not competing. Transluce's is the **finding** layer;
ours is the **observation** layer. A common schema keeps both and links them:

```
FINDING
  id                  # uuid or server id
  summary             # ≤280 chars (Transluce's constraint is good)
  description         # long-form, uncertainties stated
  observed_at         # when the activity happened (range allowed)
  recorded_at         # when the finding was written
  source              # which hunt/corpus produced it
  submitter           # who (analyst or agent id)
  classifications     # cyberattack[] (XSS, SQLi, bot-bypass, SSRF, ...),
                      # government (national/state/none/unsure),
                      # ai_company (openai/anthropic/xai/unknown/...),
                      # eval (deepsearchqa, exploitgym, unknown, ...)
  evidence            # list of { kind: link|file|observation_ref,
                      #           url | fingerprint, sha256, retrieved_at }
  untapped_source     # bool — more left to find?
  confidence          # observed | inferred | upstream (our grading)
  sensitivity_note    # annotate, never redact

OBSERVATION
  fingerprint         # sha256 of canonical record (dedup key)
  observed_at         # event time (with timestamp_source noted)
  record_kind         # urlquery_report | arquivo_capture | hf_commit | wiki_rev | ...
  labels              # per-kind fields (submitted_url, commit.sha, ...)
  source_url          # where it was fetched from
  sha256 / size_bytes # of the raw bytes
  retrieved_at / retrieved_via
  description
```

## Field mapping (what translates cleanly)

| Transluce field | Common-schema home |
|---|---|
| summary / description | FINDING.summary / description (unchanged) |
| evidence_links[] | FINDING.evidence[] with kind=link |
| data_zip | FINDING.evidence[] with kind=file (+sha256) |
| cyberattack[] | FINDING.classifications.attack[] |
| government / ai_company | FINDING.classifications.government / .ai_company |
| untapped_source | FINDING.untapped_source |
| id / created_at / submitter | FINDING.id / recorded_at / submitter |

| Our field | Common-schema home |
|---|---|
| fingerprint | OBSERVATION.fingerprint; referenced from FINDING.evidence[].fingerprint |
| labels.* | OBSERVATION.labels (per-kind, namespaced: `urlquery.report_id`, not bare `report.id`) |
| confidence | FINDING.confidence (observed/inferred/upstream) |
| @timestamp / event.dataset | OBSERVATION.observed_at / source |

## Gaps the common schema must add (neither has today)

1. **eval linkage** — which benchmark was RUN vs which was TARGETED (our incident
   ledger keeps these separate; Transluce's schema has no eval field at all).
2. **Shape tags** — the detection shapes (tag-grammar, burst, sweep, dead-drop)
   as first-class labels, so findings are queryable by shape not just by text.
3. **Cross-corpus refs** — a finding's evidence should cite observation
   fingerprints across corpora (their urlquery report ↔ our cached capture).

## Practical note

Transluce's schema is v3 and filterable on `untapped_source`, `cyberattack`,
`government`, `ai_company` — a shared schema should keep those exact enums where
they exist and only ADD the eval/shape fields, so both sides can adopt it without
breaking their current queries. The `data_zip` (200MB) convention already matches
our "cache raw bytes with provenance" rule.
