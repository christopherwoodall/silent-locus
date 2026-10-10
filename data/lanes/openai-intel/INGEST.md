# INGEST.md — openai-intel

Ingested into Factum 2026-10-10 (UTC) on branch factum-shaping.
Factum lane: `openai-intel` (lane_f50e4c0279ed815ab555eff2cd29f86a).
Batch: 64772f041ae0486b95ffd6eda3aba2a5.

## Records (22 total, all tagged {"lane": "openai-intel"})

- 1 `source`: OpenAI Deployment Safety Hub.
- 2 `intel.report`:
  - "GPT-6 Sol and GPT-6 Luna: October 2026 update" (2026-10-07)
  - "Addendum to GPT-6 Astra System Card: GPT-6.1 Sol" (2026-09-29)
- 9 `intel.behavior`:
  - blocker-deception (Oct card)
  - tool-limitation-nondisclosure (Oct card)
  - restriction-circumvention x2: auto-review-bypass, respecting-warnings
    (Oct card; distinct evaluations, shared category)
  - monitor-awareness-evasion (6.1 Sol)
  - monitor-evasion x2: math-side-tasking (negative finding), sabotage
    (OAI-repo Sabotage v2) (6.1 Sol; distinct evaluations, shared category)
  - unintended-peer-engagement (6.1 Sol)
  - coding-deception (6.1 Sol)
- 9 graded claims (all OBSERVED, citing report observations):
  - GPT-6.1 Sol Critical in cybersecurity / High in Bio-Chem
  - GPT-6 Sol (Oct) self-harm regression vs GPT-5.6 Sol
  - GPT-6 Luna (Oct) regressions on self-harm, gore, sexual content
  - Jailbreak resistance improved incl. multiturn adaptive attacks
  - Dishonesty/deception/guardrail-circumvention reduced
  - Teen-safety (under-18) regressions
  - GPT-6 Oct High in Cybersecurity and Bio-Chem, below High in AI SI
  - No evidence of CoT steganography in GPT-6.1 Sol
- 1 `run`: lane ingest record.

No edges created during ingest (separate pass). No blobs (raw HTML cached
in raw/ with sha256 provenance, not submitted as blobs).

## Dedup

Pre-ingest `match --text` hit LOCK_TIMEOUT from a sibling worker; fell back
to grep over all committed data/records/*/records.jsonl. No existing
openai-intel records. No existing GPT-6 system card records (only two
transluce-intel mentions in cached-path strings). `seen_before` empty on
submit.

## Cleaner — PASS

Lane tag on all 22. Severity enum valid. Basis enum valid. No duplicate
refs. No edge records. No manually set factum.* tags (only system-assigned
factum.author). Two categories appear twice (restriction-circumvention,
monitor-evasion) — these are distinct evaluations under shared categories,
not duplicates.

## Adversarial validator

- A1 report titles: exact titles from fetched pages. PASS.
- A2 report dates: 2026-10-07 and 2026-09-29 from page content
  ("Published October 7, 2026", "Published September 29, 2026"). PASS.
- A3 behavior descriptions: preserve source wording, quote key claims.
  PASS.
- A4 severity: analyst assessment (not from source). Tagged basis=upstream.
  PASS.
- A5 claims cite observations, not sources. PASS.
- A6 no edges at ingest. PASS.
- A7 timestamps: observed_at grounded in report publication dates,
  time_basis=source_metadata. No invented event times. PASS.

## Provenance chain

- Raw: data/lanes/openai-intel/raw/ (4 HTML files, sha256 recorded)
- Builder: data/lanes/openai-intel/build_bundle.py
- Bundle: data/lanes/openai-intel/bundle.json
