# Provenance — anyrun-scan

Cite Factum records here.

## Source documents
- `evidence/anyrun-scan/PLAN.md` — surface map + shape pipeline S1-S12, verified 2026-10-07.
- `evidence/anyrun-scan/VERDICT.md` — dead-end verdict, 2026-10-07.

## Live checks (2026-10-07)
1. TI Lookup XHR backend `https://api-gb.any.run/lookup/search-with-updates/`
   (POST): 401 without a login bearer token. No unauthenticated JSON access.
2. Public task pages render (200) but data loads via auth-gated DDP/REST.
3. Registration form: rejects personal email addresses ("Enter a valid business
   email"); personal-email users are directed to manual verification via X or
   Discord. Live attempt with handle "swarmtrace" and a proton.me address:
   blocked at the business-email validation. No account created, nothing
   submitted.

## Time basis
All observation times use the documented check date 2026-10-07
(`time_basis: legacy_documented`). No finer time is in the source.

## Reusable material
PLAN.md's shape pipeline (S1 tag grammar, S6 staging/dead-drop hosts, S2
cartesian sweep, S3/S9/S10 timing, S5 proxy laundering, S7 fuzz ladder, S4 run
labels, S8 cross-host walk, S11/S12 corroboration) stays valid if account
access ever materializes, or for tria.ge / hybrid-analysis scoping.
