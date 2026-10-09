# Common schema — Transluce findings × our observation corpus

## TL;DR
Transluce sends us findings (conclusions an analyst draws from many observations).
Our corpus holds observations (single records: reports, captures, commits).
The two layers fit together: we keep both layers and we link each finding to the records it uses.

## Term definitions
- **finding**: a conclusion an analyst draws from many observations.
- **observation**: one record of one event.
- **artifact**: the raw bytes we fetched.
- **fingerprint**: a sha256 hash of the canonical form of a record. It is the dedup key.
- **envelope**: the set of fields that describe a record (who, when, where it came from).

## The two shapes in play

| | Transluce `/api/findings` | Our `events.jsonl` | Raw captures (urlquery / arquivo.pt) |
|---|---|---|---|
| Grain | One finding = an analyst conclusion over many observations | One observation = one record (report, commit, capture) | One artifact = fetched bytes |
| Envelope | id, created_at, updated_at, submitter, submitter_id, sensitive, form_version | @timestamp, event{ dataset, created }, record_kind, fingerprint | retrieval time, source URL, method, sha256 |
| Content | data{ summary, description, evidence_links[], data_zip, untapped_source, cyberattack[], government, ai_company } | labels{...per-kind fields...}, description, confidence | raw bytes + provenance note |
| Identity | server-assigned id | fingerprint (sha256 of canonical form) | sha256 of bytes |

## Verdict: two grains, one envelope

The shapes complete each other. They do not compete.
Transluce gives the **finding** layer. We give the **observation** layer.
A common schema keeps both layers and links them:

```
FINDING
  id                  # uuid or server id
  summary             # ≤280 chars (Transluce uses this limit; we keep it)
  description         # long text; state what is uncertain
  observed_at         # when the activity happened (a range is allowed)
  recorded_at         # when the analyst wrote the finding
  source              # which hunt or corpus made it
  submitter           # who wrote it (analyst name or agent id)
  classifications     # cyberattack[] (XSS, SQLi, bot-bypass, SSRF, ...),
                      # government (national / state / none / unsure),
                      # ai_company (openai / anthropic / xai / unknown / ...),
                      # eval (deepsearchqa, exploitgym, unknown, ...)
  evidence            # list of { kind: link|file|observation_ref,
                      #           url | fingerprint, sha256, retrieved_at }
  untapped_source     # true/false — is there more to find here?
  confidence          # observed | inferred | upstream (our grade)
  sensitivity_note    # describe the risk; never remove data

OBSERVATION
  fingerprint         # sha256 of canonical record (dedup key)
  observed_at         # time of the event (note the time source)
  record_kind         # urlquery_report | arquivo_capture | hf_commit | wiki_rev | ...
  labels              # per-kind fields (submitted_url, commit.sha, ...)
  source_url          # where we fetched it
  sha256 / size_bytes # of the raw bytes
  retrieved_at / retrieved_via
  description
```

## Field mapping (what translates cleanly)

| Transluce field | Common-schema home |
|---|---|
| summary / description | FINDING.summary / description (no change) |
| evidence_links[] | FINDING.evidence[] with kind=link |
| data_zip | FINDING.evidence[] with kind=file (+sha256) |
| cyberattack[] | FINDING.classifications.attack[] |
| government / ai_company | FINDING.classifications.government / .ai_company |
| untapped_source | FINDING.untapped_source |
| id / created_at / submitter | FINDING.id / recorded_at / submitter |

| Our field | Common-schema home |
|---|---|
| fingerprint | OBSERVATION.fingerprint; FINDING.evidence[].fingerprint points to it |
| labels.* | OBSERVATION.labels (per-kind, namespaced: `urlquery.report_id`, not bare `report.id`) |
| confidence | FINDING.confidence (observed / inferred / upstream) |
| @timestamp / event.dataset | OBSERVATION.observed_at / source |

## Gaps the common schema must add (neither side has these today)

1. **eval linkage** — which benchmark ran, and which benchmark was the target.
   Our incident ledger keeps these separate.
   Transluce has no eval field at all.
2. **Shape tags** — the detection shapes (tag-grammar, burst, sweep, dead-drop) as labels.
   Then we can search findings by shape, not only by text.
3. **Cross-corpus refs** — one finding must cite observation fingerprints across corpora.
   Example: their urlquery report next to our cached capture of the same page.

## Practical note

Transluce uses schema v3.
It filters on `untapped_source`, `cyberattack`, `government`, `ai_company`.
A shared schema must keep those exact enums.
It must only ADD the eval and shape fields.
Then both sides can adopt it and keep their current queries.
The `data_zip` (200MB) rule already matches our rule: cache raw bytes with provenance.
