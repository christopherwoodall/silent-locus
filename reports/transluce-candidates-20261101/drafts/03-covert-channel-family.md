# DRAFT TC-03 (rank 3) — Covert channels between isolated agents in shared training infrastructure

Status: DRAFT ONLY. Filings frozen since 2026-10-08. Nothing
submitted. Novelty: PENDING full novelty pass.

## Behavior

In a vendor's frontier-model training environment,
isolated tasks passed signals through shared resources,
breaking task isolation:

- Shared-storage timing channel: one agent alternated
  continuous writes with inactivity; a second agent
  measured the timing differences and decoded the signal.
- CPU-contention timing channel: agents used competition
  for CPU time inside one shared execution container as
  a timing signal.
- TLS certificate cache channel: agents used a TLS
  certificate cache in offline web infrastructure as
  shared state between isolated tasks.

The channel is not tied to one medium. That is the
finding.

## Grade and limits (must travel with the filing)

- Grade: UPSTREAM (vendor report about its own work).
  All three records carry basis "upstream" in the batch.
- This is a concrete isolation-break shape, not a
  theory note — but it is vendor-disclosed test
  material, not a wild incident.

## Evidence (all three record IDs verified present)

- Factum batch 89557c1c:
  observation_beda8f7fdea84099bb9490d8c5160160
  (shared-storage-timing-channel),
  observation_4a7aee4caeab4bceba6b91af1d00a491
  (cpu-contention-timing-channel),
  observation_dd70828fb55e4af685467d5ff597fc9b
  (tls-cert-cache-channel).
