# PROVENANCE — swarmtraces-verification (2026-09-27)

**Dataset:** `2026-09-27-swarmtraces-verification` — measured structural
audit of the SwarmTraces corpus (`redacted.jsonl.gz`, 189,579 records),
from `notes/verification-2026-09-27.md`. All figures re-measured from the
corpus bytes, not from memory of earlier passes.

**Retrieval/observation date:** 2026-09-27. `@timestamp` = note date;
`labels.timestamp_source=note:publication_date`. `confidence: confirmed`
(the note states all claims re-verified against source data).

**Method:** uniform 7-field record audit (id/cite/kind/parent_id/time_utc/
tags/text): per-kind counts and ID-gap check; field nullability and text
length stats; redaction-marker occurrence counts; parentage topology
(parent_id targets); cite-token distribution and reuse analysis.

**What landed** (`events.jsonl`, 5 records): one `finding` each for
record counts (payload 91,037 / recovered_text 75,534 / response 23,008;
IDs R0000001–R0189579, zero gaps), field stats (time_utc null on 189,579/
189,579; parent_id null on all payloads), redaction markers (e.g. 116,646
destination redactions, 100,215 numbered encoded blobs), parentage topology
(61,124 parents → payload, 1 → recovered_text, 0 dangling), and cite-token
semantics (163,849 distinct tokens; 19,036 reused; template/cluster key).

**Dedup note:** these are corpus-audit measurements; existing aggregate
collections (`2026-09-28-gem83-reconciliation`, `2026-09-29-overlap-analysis`)
analyze cross-corpus overlaps, not the SwarmTraces corpus structure itself.

**Fingerprint identities:** `swarmtraces-verification|<audit-slug>`.
