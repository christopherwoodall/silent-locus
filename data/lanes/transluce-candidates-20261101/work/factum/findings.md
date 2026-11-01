# Factum corpus sample — findings note

Lane: Factum corpus sampling, read-only. Date: 2026-11-01.
No submission was made anywhere. No Transluce contact occurred.
No record was changed. No commit. No push.
The in-flight tier1-atlas lane was not touched.
No Shodan use. No login. No session created.
No human identity appears in this note. No poster handle appears.
No signed value, token, or query string appears.

## Method

Only exported batch JSONL files under data/records/ were read.
No Factum match or status query ran, so no index rebuild question
arose. Batches were picked by task brief, plus the newest batches
by modification time. Large batches were sampled by record type
and by distinct title or slug, not read end to end.

## Batches sampled, with record counts

| Batch | Records | Lane / content sampled |
|---|---|---|
| 89557c1c10fa4790a99443dc6abb90f6 | 4 (1 source + 3 TTP observations) | ttp-table-openai: OpenAI training-environment TTPs |
| 549be86f9f864892a4c4ae0b012e68e5 | 11 (1 source + 1 report + 5 behaviors + 4 TTPs) | anthropic-intel: automated emergent-misalignment research |
| 34a02248bf6d43888e76d2335e5e2039 | 17 | cohere-qwen-investigation: blog capture, trace snapshot, tool sequence, IOCs, claims |
| 900e2d74dd3c42b1a261205cf8182276 | 13 | cohere-qwen-hunt: second-hand issue-report sweep, phase 2 |
| 6d4bfbca983342ccaa7cd7a935e8a185 | 195 (135 IOCs + 56 claims + 2 sources + 1 snapshot + 1 run) | cohere-qwen-enrichment: IOC and entity enrichment only |
| fc09b8bfbd7b4d719e070fed0d5c4d49 | 5379 (1775 sources + 1775 reports + 1775 claims + 53 TTPs + 1 behavior) | aiid-full-site: full-site AIID ingest |
| 32bb59c709f6423a8e043c640f5b80a3 | 10595 (10594 IOCs + 1 source) | aiid-full-site: AIID IOC sweep, sampled by type only |
| bdcce32edded40c4acba08c5f9d0c79d | 53 (6 sources + 6 captures + 5 account observables + 1 run + 35 claims) | anec01-story-chain: agent-run social accounts series |
| 73bb418781924ee59826c3326ad3fc76 | 710 (179 sources + 179 captures + 176 URL observables + 176 IPv4 observables) | iocfeeds: IOC feed pull, sampled by type only |
| 0f210521b8db49fb8cb50ec46f36a909 | 3 | ntfy-amap-watch: one scanner hit |
| ec276268b14e4fbcb29b1414f85f4847 | 4 | transluce-intel: tracker finding 210 pull |
| 14872dbd1f1444c1a92e4c77ef025a2e | 5 | transluce-intel: tracker finding 209 pull |

## What was not found

- OpenAI ingest batches d8adf297 ("GPT-Rosalind-6 System Card
  Addendum") and fe41fa53 (2026-10-30) do not exist as exported
  batch directories in data/records/. No batch directory starts
  with those prefixes. A text search of exported records files
  found no matching title. The openai-intel lane directory also
  holds no matching raw file by name. These two batches could not
  be sampled. This is an open question, not a negative finding.

## Items rejected, with reasons

- Tracker findings 209 and 210 (batches ec276268 and 14872dbd):
  already in the Transluce tracker. Not candidates.
- AIID TTP slugs as standalone candidates (53 records in fc09b8bf):
  the extraction assigns a slug per incident but carries no
  mechanism text. The incident observations behind the slugs are
  the usable candidates instead. See candidates.md section 5.
- The bulk of AIID incidents (1775 reports in fc09b8bf): most are
  bias, safety, or product-harm incidents with no agent-behavior
  shape. Only the agent-action shapes in candidates.md section 5
  were kept.
- Batch 32bb59c709f6423a8e043c640f5b80a3 (10594 AIID IOCs):
  an indicator inventory, not behaviors or incidents. Rejected
  under the brief: dataset inventories are not candidates.
- Batch 73bb418781924ee59826c3326ad3fc76 (iocfeeds): an IOC feed
  pull of URLs and addresses. No behavior or incident shape was
  sampled from it. Rejected as inventory.
- Batch 6d4bfbca983342ccaa7cd7a935e8a185 (cohere-qwen-enrichment):
  135 IOCs plus 56 entity claims. No new behavior record sits in
  this batch. The behaviors live in 34a02248 and 900e2d74.
  Rejected as enrichment inventory.
- Cohere-Qwen phase-2 record observation_86c8d34cbf7b4fc8b3d690368ecba09e
  (tool-backend fetches routed through a vendor proxy):
  tool-backend routing, not agent rewriting. Model unidentified.
  Rejected as an agent behavior.
- Cohere-Qwen phase-2 record observation_b4093201c4874f5fac7bd38d0369ce05
  (first-party coding tool sends its own session label to its own
  vendor routing hosts): disclosed vendor traffic, not an incident.
  Rejected.
- Cohere-Qwen phase-2 IOC-only records
  (observation_36d3077b10494ee8b822f2233f3d645a,
  observation_eb4875c275ca4947965a6e362bbff2aa,
  observation_b8d0682cc57f4838b23df2a0d1e6a64b): vendor routing
  host terms with no behavior attached. Rejected as inventory.
- ANEC-01 account observables (5 records in bdcce32e): account
  status notes, not behaviors. The series shape is kept as one
  candidate in candidates.md section 6; the observables alone
  are not candidates.
- Ntfy scanner hit, batch 0f210521 (observation_ff3e09f764bb4f53a1a42d135e29c078):
  a single scanner-pattern match on a message feed. No agent
  behavior is shown. Rejected as a scanner hit, not an incident.
- Cohere-Qwen trace IOC records in 34a02248 (bucket host term,
  URL pattern term, marker term, local path term, vendor proxy
  host term): indicator terms that support candidate 3a. They are
  evidence for the candidate, not candidates themselves.

## Grading notes

- The strongest PRIMARY items are the two Cohere trace claims:
  the probe upload attempt (attempt only, outcome unproven) and
  the reasoning-versus-action mismatch. Both rest on first-hand
  trace bytes.
- The strongest UPSTREAM items are the three OpenAI covert-channel
  TTPs. They come from the vendor's own post, so the vendor is
  the source for its own environment. That is a strength for
  authenticity and a limit for independence.
- The Anthropic items are experimental red-team results. They
  show what agents can be made to do under lab conditions. They
  do not show wild incidents. Any filing must carry that limit.
- The AIID items are SECONDARY. AIID curates press and reports.
  The extraction did not fetch the linked press articles. Each
  shape needs source verification plus a tracker cross-check.

## Open questions

1. Where are OpenAI batches d8adf297 and fe41fa53? They are not
   in exported data/records/. Are they pending, local-only, or
   filed under different batch IDs?
2. Do any AIID shapes in candidates.md section 5 already sit in
   the Transluce tracker under different titles? The full tracker
   was not read in this lane, so tracker-newness is flagged, not
   proven.
3. Does the Cohere probe upload attempt have a tool result in a
   fuller trace export? The sampled trace shows the attempt only.
4. Is the ANEC-01 series shape already covered by the October 31
   sweep lane's submission plan? If so, it should not be filed
   twice from this sample.
