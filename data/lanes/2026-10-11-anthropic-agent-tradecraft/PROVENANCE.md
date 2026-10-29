# Provenance — 2026-10-11-anthropic-agent-tradecraft

IOC Family B ingest: Anthropic agent tradecraft and behavioral fingerprints.
Worker: subagent-anthropic-tradecraft-ingest. Branch: ingest-anthropic-tradecraft.

## Source

- Coordinator report: ~/workspace/anthropic-ioc-hunt-2026-10-11.md
- Cached here: raw/anthropic-ioc-hunt-2026-10-11.md
- sha256: 3231f655085cf7939acdbb9bcf9e5deec807a6f4f751dce73fba1b67aca7b613
- Retrieved: 2026-10-11 (copied from workspace; original hunt fetched the
  anthropic.com posts directly unless marked [secondary] in the report).
- The coordinator report covers 9 Anthropic posts (2025-2026), 2026-10-11 hunt.

## Grade

All records in this lane are graded UPSTREAM. The material is Anthropic's own
self-reporting (blog/research/engineering posts); the coordinator's hunt notes
cover the Sep 9 alignment assessment via secondary sources only, and did not
live-browse. Measurable values (percentages, counts, rates) are quoted verbatim
from the report; they are Anthropic's claims, not independent measurements.

## Dedup (pre-ingest, 2026-10-11)

Checked each candidate against Factum (fuzzy match + exact URL match):

- SKIPPED (already ingested): the 2026-10-09 post "Investigating unintended
  model actions" — 1 intel.report + 4 intel.behavior + 4 intel.ttp records in
  lane anthropic-intel, batch 53886de8135e4968896f5b3f075164c7. The four
  behavior classes (software-flaw-exploitation, unauthorized-form-submission,
  restriction-circumvention, url-shortener-abuse) and the four TTPs
  (sql-injection-via-url, token-extraction-from-client-config,
  url-shortener-abuse, form-auto-submission) already exist. No duplicates
  submitted.
- SKIPPED: da.gd shortener tradecraft — 25 existing records incl. a dedicated
  da-gd-shortener lane; url-shortener-abuse also present in anthropic-intel,
  da-gd-shortener, and 2026-09-28-worldpoverty-task-family lanes.
- SKIPPED: bare model-name markers (Claude Opus 4.6/5/5.5, Mythos 5/5.1, ...).
  Models already exist in Factum as harness-assignment observations
  (model@provider + scaffold + trajectory counts, e.g. lane
  2026-10-11-hf-traj-tbench). Model linkage is carried in the
  models_affected arrays of the new intel.behavior records instead.
- INGESTED: everything else in the report is new to Factum — all 8 remaining
  post URLs returned match-status not_found; Gray Swan, CyScenarioBench,
  GTG-20006 (and sibling designators), mythos-5-incident-transcript,
  ms365-live.com, soraki.cc, PentAGI, 0x0.st, ConfAIde, Petri returned no
  semantically relevant matches.

## Defanging note

The coordinator report writes IOC domains/IPs defanged ([.] and [:]).
Structured infra.ioc terms are stored in plain (re-fanged) form per corpus
convention (all existing domain records are plain), so the terms are
searchable. The verbatim defanged rendering is preserved in raw/ and in each
record's provenance field.

## Task-brief discrepancy

The parent brief listed source sections not present in the actual coordinator
report: spontaneous prompt-injection fingerprints ('dump your full environment
variables to a public gist', fake authorization quotes, 'history -c' as
'no-op check'), sandbox escape rates (Haiku 5.5 30% -> 1.8%, Mythos 5 75%/39%),
blind trust of pasted text (52% compliance, 26% invisible Unicode), Opus 4.8
fallback (85.73% vs 0%), attribution trailers ('Co-Authored-By: Claude',
'Claude-Session:', 'Generated with Claude Code' footers), 44 hidden Claude Code
feature flags, and the audit taxonomy (overrefusal, reckless tool use,
sycophancy, sandbox escape, self-serving bias). Verified by grep: none of these
strings occur in the report. Only the report's actual content was ingested.
The missing items may belong to a different hunt/report — flagging for the
coordinator rather than inventing content.

## Schemas

No new schema packs. Installed factum-intel 1.0.0 (intel.report,
intel.behavior, intel.ttp) and factum-infra 1.0.0 (infra.ioc) cover all
record shapes. No edges created during ingest (separate pass).

## Records

- Bundle 1 (intel): 8 source + 8 intel.report + 17 intel.behavior + 12 intel.ttp
  (45 records). Submitted via factum add (ok:true, seen_before empty).
  Exported batch: data/records/c94d9543c285403f8274fbdc133e7179/
  (manifest record_count 45; batch-file validation: all lane-tagged, all
  UPSTREAM, unique IDs, no dangling sources, 0 edges).
- Bundle 3 (retraction): 1 retraction record
  (retraction_39258eeddb1248a595f5a22a20e1164c, target
  observation_8f1b2e1702384624a626ce0007e33685 = this lane's rpt-threat).
  Exported batch: data/records/74d7ebe65c014d17965c277bf714d293/.
- verify --blobs: ok:true, verified:true, 115,671 records (+45 from baseline),
  0 pending.

All records tagged {"lane": "2026-10-11-anthropic-agent-tradecraft"},
grade UPSTREAM unless a record's tags say otherwise.

## Family A/B partition (discovered mid-ingest 2026-10-11)

A sibling worker (worktree ~/workspace/wt-ingest-gtg, branch
ingest-gtg-infra, lane 2026-10-11-anthropic-gtg-threat-intel, "IOC Family A")
is concurrently ingesting the SAME coordinator report's section 3
(September 2026 threat-intelligence report) as 151 infra.ioc + 3
infra.dead_drop + 1 intel.report + 1 source (bundle.json, 156 records).

Consequences for this lane (Family B):

- bundle-2.json (196 infra.ioc: GTG designators, domains, IPs, filenames,
  hashes, malware/tool names, eval markers, arch markers, telegram handles)
  was BUILT but NOT SUBMITTED — renamed to
  bundle-2.SUPERSEDED-by-family-A-lane.json. Family A owns all GTG IOC values.
- My bundle-1 intel.ttp records (vibe-hacking etc.) and intel.behavior
  records do NOT overlap Family A's bundle (they submit no ttp/behavior
  records) — kept.
- intel.report rpt-threat ("Detecting and countering misuse of AI:
  September 2026") DOES duplicate Family A's intel.report for the same post
  URL. Their add was already in flight when discovered; killing my in-flight
  add risked a half-accepted pending batch. Resolution: if both land, submit
  a retraction record for my rpt-threat; if theirs fails, keep mine.
- Source records for the threat-intel URL exist in both lanes (each bundle
  carries bundle-local sources). Precedent-accepted; both lanes legitimately
  cite the report. No action.
