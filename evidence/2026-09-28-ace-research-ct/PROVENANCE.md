# PROVENANCE — ace-research-ct (2026-09-28)

**Dataset:** `2026-09-28-ace-research-ct` — passive certificate-transparency
inventory plus DNS/Wayback bounded measurements for the Artifactory host
`packages.hub.ace-research.openai.org` that appeared in the swarmtraces
corpus graph (`github-remote-cache/zz` board path).

**Retrieval/observation date:** 2026-09-28 (passive only — no authenticated
probes, no person-focused attribution). `@timestamp` = observation date;
historical issuance dates live in `labels.ct.not_before/not_after`.

**Method (per `notes/analyst-note-ace-research-2026-09-28.md`):** crt.sh
queries for the wildcard domain; plain DNS resolution + GET `/` and
`/artifactory/api/system/ping`; Wayback availability API + CDX wildcard
query; internal→external artifact mapping from URL paths observed in the
corpus (cross-checked against CyberGym public docs).

**What landed** (`events.jsonl`, 12 records): 3 `finding` rows (one per
wildcard certificate issuance: 2024-06-09, 2026-06-10, 2024-06-27, Let's
Encrypt R10/R11, 90-day terms — unique name only `*.ace-research.openai.org`
/ `ace-research.openai.org`), one `finding` on the wildcard blind spot (no
sibling subdomains enumerable; `packages.hub` never held its own cert), one
`finding` DNS negative (host does not resolve publicly), one `finding`
Wayback negative (zero captures ever), 6 `finding` internal→external
artifact mappings (CyberGym ARVO, dockerhub-public, github-remote/-cache,
zz labels, image tags, traversal probes).

**Analytical claims** in the note (internal-eval-infrastructure hypotheses,
timing readings) remain notes-only — represented here only as the bounded
measurements above.

**Fingerprint identities:** `ace-ct|cert|<cert-id>`, `ace-ct|wildcard-blind`,
`ace-ct|dns-negative`, `ace-ct|wayback-negative`,
`ace-ct|artifact-map|<hash16>`.
