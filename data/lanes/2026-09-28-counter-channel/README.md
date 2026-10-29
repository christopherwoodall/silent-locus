# 2026-09-28-counter-channel

Read-only snapshot of the countapi.mileshilliard.com agent counter channel.
The channel is documented in the thecolony.ai incident wiki. Scope is
counters only. No attempt was made to attribute who incremented them.

Lane record: lane_5f2d6caefcc143f792fa55c2498c38c4

## What is here

- snapshot_2026-09-27.json — the raw capture (3 counter readings, 1 sibling
  enumeration probe). Copied from evidence/2026-09-28-counter-channel/raw/
  (sha256 e7c2254d874b9e94841a646e5e252a76bba8f441cee14afcf04367fada734642).

## Factum records (ingested 2026-10-09)

- source_fed9b8934c5d4289bb75635671f75aa2 — submitted source (the snapshot).
- observation_d5f1e03dd8704cdca73df099968560f8 — infra.ioc marker
  langr5backup4813_CA = 4. Unchanged from the 2026-09-04 report.
- observation_4a5dd5597fa84e108f252d8e2a435327 — infra.ioc marker
  langr5backup4813_TX = 2. Unchanged from the 2026-09-04 report.
- observation_fafe845551ef4d21831027fe88f92226 — infra.ioc marker
  langr5backup4813_ZZ = 2. Documented-fake key now carries a value —
  channel being poked.
- observation_941a515e2ad0455d9c30b0c98d94e100 — reachability.check.
  Sibling enumeration: 12 read-only GETs all 404. The host exposes no
  list or info endpoints. Nothing further to pull from this venue.
