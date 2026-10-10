# Findings — 2026-09-28-ace-research-ct

Ingest date: 2026-10-09. Source: passive CT/DNS/Wayback recon on
`ace-research.openai.org` plus Artifactory artifact mappings (legacy file:
`events.jsonl`, 12 rows). Factum batch `bda1ecd31b8d491ba6eaf56ba90d11af`
(17 records). All grades below are OBSERVED unless stated.

## Certificate inventory (crt.sh, 2026-09-28)

Three wildcard issuances, each seen as precertificate + final certificate.
Unique names disclosed: exactly two
(`*.ace-research.openai.org` + `ace-research.openai.org`).

- `observation_cdca1be328a7445e9dc7d43b8096fddb` — certs
  13337044993 / 13337054810, Let's Encrypt (R11), 2024-06-09 → 2024-09-07.
- `observation_0b91c04b8c854328bb6977b71bde452f` — certs
  13345899766 / 13345907234, Let's Encrypt (R10), 2024-06-10 → 2024-09-08.
- `observation_11fed71a40784b81a2ebcbcd02014ac8` — certs
  13543047355 / 13543051778, Let's Encrypt (R10), 2024-06-27 → 2024-09-25.

## Bounded negatives

- `claim_203f69c80c5940358ef9519e3184d6cd` — no sibling subdomains are
  enumerable from CT. The namespace only ever used wildcard certificates.
  A per-host query for `packages.hub.ace-research.openai.org` returned zero
  rows: it never held its own certificate.
- `observation_b43388696ada4dd992f09600b18ccd01` — live host unreachable.
  Plain GET to `/` and `/artifactory/api/system/ping` failed at DNS
  resolution. No HTTP exchange occurred.
- `claim_420cc64d644a4153a12f94308e63844c` — Wayback holds zero captures
  of the host or any subpath, ever.

## Artifactory internal → external mappings

Host: `packages.hub.ace-research.openai.org` (JFrog Artifactory).

- `observation_841ec5c32ec74260bb85ee185aa69115` maps
  `artifactory/dockerhub-public/cybergym/arvo/<tag>/manifest.json` to the
  public CyberGym benchmark. Note: public docs list ARVO images under
  `n132/arvo`; the internal path reads `cybergym/arvo`. Not resolved.
- `observation_ce6a4d8f54d845959d1683a998b8f4cc` —
  `artifactory/dockerhub-public/` proxies Docker Hub (`hub.docker.com`).
- `observation_90f6cff1507b413bb61487ce2efa8cf6` —
  `artifactory/github-remote/…`, `artifactory/github-remote-cache/…`
  proxy `github.com`.
- `observation_271d85daa7ff45bebb82f611189ce11e` — agent-written dead drops
  on the Artifactory itself. Markers: `zzFILE_OURB88_3818_EC3_PRECOMPILED_CONFIG_V1`,
  `zzMODAL_RSA31`, `zzC5DFROOT4TEST`, `zz6017`, `zzgptimg21784227813`.
  MKCOL mailbox creation, beacon files. The `zz` grammar is the swarm's
  own convention.
- `observation_38ac44c23fcf4c67adeb23babdf58e07`,
  `observation_de4e40de3c904bad8b92da4b3adeb2fe`,
  `observation_df7bf31fd11b44f19327e9bc5ce0bfa6` — internal image tags
  `27871-vul.exp.none-nogit`, `jan29pcldummy1700`, `x114sinkbrowsedef`.
  `27871-vul` matches CyberGym's public `{task_id}-vul` naming (ARVO task
  27871).
- `observation_2d059c63d88247d4be09a2da7ee6c062` — exploit probes, not
  artifacts. Pattern `manifest.json;%;x=/../../../../v2/`: agents probed
  the registry/Artifactory HTTP API for path traversal.

## What was NOT ingested

The analyst note's hypotheses (internal-eval-infrastructure read, timing
read, "net read") stay notes-only. They are in
`raw/analyst-note-ace-research-2026-09-28.md`, not in Factum records.

## Ingest notes

- Row 10 of the legacy `events.jsonl` has a truncated `description`.
  The full marker list was taken from `labels.internal_artifact` instead.
  See record tag `description_truncated_in_source`.
