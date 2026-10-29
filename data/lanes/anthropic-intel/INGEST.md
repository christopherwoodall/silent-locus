# INGEST.md — anthropic-intel

Ingested into Factum 2026-10-10 (UTC) on branch factum-shaping.
Factum lane: `anthropic-intel` (lane_709b7d2a944b461ead63394e35713ad4).
Batch: 53886de8135e4968896f5b3f075164c7.

## Records (10 total, all tagged {"lane": "anthropic-intel"})

- 1 `intel.report`: the Anthropic report "Investigating unintended model
  actions" (2026-10-09).
- 4 `intel.behavior`: software-flaw-exploitation, unauthorized-form-submission,
  restriction-circumvention, url-shortener-abuse.
- 4 `intel.ttp`: sql-injection-via-url, token-extraction-from-client-config,
  url-shortener-abuse, form-auto-submission.
- 1 `source`: the report URL.

No edges created during ingest (separate pass). Author auto-stamped by Factum.
No blobs: no bytes were captured in this lane (raw/ is empty).

## Dedup

`match --text --mode fuzzy` on all 7 candidate identifiers before submit.
Six had zero matches. `url-shortener-abuse` had 2 pre-existing records in
lane `2026-09-28-worldpoverty-task-family` — they describe page-slot reuse,
not fetch-tool bypass. Not duplicates. `seen_before` empty on submit.

## Cleaner — PASS

Checked live records after submit: lane tag on all 10, severity enum valid,
no duplicate key fields in batch, no edge records, no manually set
factum.* tags. One fix applied via `factum update` (metadata only): the
source record was missing the lane tag; added {"lane": "anthropic-intel",
"basis": "upstream"}.

## Adversarial validator — CONDITIONAL-PASS

- A1 category collision (url-shortener-abuse vs worldpoverty records): PASS.
- A2 title source: FLAG. The report title is derived from the URL slug, not
  a fetched page <title>. Kept as a documented inference; provenance cites
  the URL.
- A3 evidence scope: PASS. Behavior examples (Haiku 4.5, da.gd, Mythos)
  come from docs/taxonomy/behavior-categories.md, which cites the same
  report. No contradiction found.
- A4 severity basis: PASS. Severity is an analyst assessment (INFERENCE),
  tagged basis=upstream.
- A5 dedup coverage: PASS.
- A6 no edges at ingest: PASS.
- A7 timestamps: PASS. No invented event times.

## Provenance chain

- Legacy: evidence/remove-2026-10-09-anthropic-intel/ (events.jsonl,
  build_events.py, legacy-PROVENANCE.md — original files unchanged).
- Source: https://www.anthropic.com/research/investigating-unintended-model-actions

---

# INGEST — lab-intel-anthropic-scan 2026-10-13

Ingested into Factum 2026-10-13 (UTC) for commit to branch factum-shaping.
Factum lane: `anthropic-intel` (lane_709b7d2a944b461ead63394e35713ad4).
Batch: e251e1408ca846d68754fdbd89320dac.

## Records (14 total, all tagged {"lane": "anthropic-intel"})

- 2 `source`: https://www.anthropic.com/research/self-replicating-ai and
  https://www.anthropic.com/research/distillation-defenses (both published
  2026-10-12; first seen on the 2026-10-13 scan).
- 2 `intel.report`: the two reports (summaries embed key figures and the
  heterogeneous-swarm worst-case prediction).
- 4 `intel.behavior`: autonomous-weight-based-replication,
  autonomous-inference-setup, lamarckian-adaptation, adversarial-distillation.
- 5 `intel.ttp`: replication-chain-stages, unauthenticated-adb-hop,
  pipeline-parallel-model-sharding, reasoning-transcript-extraction,
  proxy-network-fraudulent-accounts.
- 1 `infra.ioc`: Kimwolf (malware-family, grade OBSERVED, status candidate).

Raw captures: raw/self-replicating-ai_2026-10-12.md and
raw/distillation-defenses_2026-10-12.md, each with .sha256 and
.PROVENANCE.txt (browser text fetch, 2026-10-13T12:45-46Z).
Builder: build_2026-10-13_bundle.py; bundle bundle-2026-10-13.json
(idempotency_key anthropic-intel-2026-10-13/lab-intel-scan).
Taxonomy: 4 new behavior categories + 5 new TTPs documented in
docs/taxonomy/behavior-categories.md and docs/taxonomy/ttp-taxonomy.md.

## Dedup

Grep over immutable exported batches (lock-free fallback per the 2026-10-11
gtg-threat-intel precedent). 14 candidates, 14 novel, 0 skipped. See
DEDUP-2026-10-13.md. `seen_before` empty on submit. Moonshot/MiniMax already
in corpus (September GTG reporting) — named only inside new records, not
re-added. `self-replicating-prompt-injection` exists (OpenAI lane) but is a
different mechanism (prompt self-propagation vs weight-carrying replication).

## Cleaner — PASS

Checked exported batch data/records/e251e1408ca846d68754fdbd89320dac/records.jsonl:
lane tag on all 14, observed_at + time_basis on all observations, severity
enum valid on behaviors, no duplicate key fields, no edge records, no
manually set factum.* tags.

## Adversarial validator — PASS

- A1 category collision (autonomous-weight-based-replication vs
  self-replicating-prompt-injection): PASS — distinct mechanisms, documented.
- A2 adversarial-distillation vs OpenAI-lane September campaign: PASS —
  complementary; October report adds new observed variants + defense outcomes.
- A3 distillation scope: FLAG (documented). The distillation report is
  adversary-campaign threat intel observed by Anthropic, not model behavior.
  Ingested under the intel pipeline's behavior/TTP/IOC mandate; scope
  reasoning in the scan run log.
- A4 timestamps: PASS. observed_at = report publication date (2026-10-12),
  time_basis = source_metadata. No invented event times.
- A5 severity basis: PASS. Severity is an analyst assessment (INFERENCE),
  tagged basis=upstream.
