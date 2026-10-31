# PROVENANCE — TTP table follow-up lane (2026-10-31)

Lane tag: `ttp-table-openai`.
Lane directory: `data/lanes/2026-10-31-ttp-table-openai/`.

## Source

OpenAI post "Securing our frontier model training environment",
published 2026-10-23:
https://openai.com/index/securing-our-frontier-model-training-environment/

The post HTML is already preserved from the 2026-10-24 lab-intel scan
(batch c3f696b405e648a9b778d9f4de898574, lane openai-intel,
cached_path
`data/lanes/openai-intel/raw/securing-our-frontier-model-training-environment.html`,
sha256
`5bb884fb53fc41ea4ec934f2cc6f5be3065d3eaea3929992e3e96190386035ef`).
No new capture was made for this lane. The existing source record
`source_859f16500a234c4da0ae1009f54c3cd1` is referenced.

The live post was re-read 2026-10-31 for a CVE spot-check before filing.
All row-2 CVE numbers confirmed verbatim: Kata Containers
CVE-2026-24834, kernel CVE-2026-74753, CVE-2026-80521, CVE-2026-80841,
plus gVisor file-descriptor handling and Moby/Docker syscall filters.

## Commission and approval

BigSexyWarlock69 commissioned a MITRE-style Factum TTP table 2026-10-23
(existing TTPs plus ones from this post, e.g. cache timing), and asked
that the post be in the blog ingest. The 9-row draft was built 2026-10-24
(`workspace/goals/factum-ttp-table-mitre-style/files/ttp-table-draft-2026-10-24.md`,
DRAFT ONLY, nothing filed). He approved filing 2026-10-31 ("Send it"):
taxonomy append plus one Factum record per row, with pre-ingest dedup
first. The blog-ingest half was already closed 2026-10-24 (16 records,
lane openai-intel, batch c3f696b4).

## Pre-ingest dedup (standing rule)

Checked 2026-10-31 against batch c3f696b4's four intel.ttp records and
by exact-slug grep across all exported record batches. Result: 6 of the
9 draft rows are already covered; 3 are new.

Skipped (covered, not re-filed):

- Row 1 dns-resolver-misconfig-internet-escape — covered by
  `observation_8b8e9cdfddf8443cb277c03c2fd8d076`
  (dns-firewall-bypass-internet-access), whose description records the
  real September 20, 2026 training-run incident.
- Row 2 microvm-escape-vuln-chain — covered by
  `observation_d5dd00a6ac7940679c6b80d2b4bd6a4c`
  (microvm-escape-chaining), same chaining and patches.
- Row 3 firewall-approved-connection-reuse — covered by
  `observation_22729a6e1ed14840a7cce654b08d23f5`
  (service-as-fetch-proxy), verbatim the same metrics-service
  authentication-endpoint test.
- Row 4 dns-firewall-control-bypass — covered by
  `observation_8b8e9cdfddf8443cb277c03c2fd8d076` (same record as row 1),
  tasked red-team perimeter tests.
- Row 5 service-url-fetch-abuse — covered by
  `observation_22729a6e1ed14840a7cce654b08d23f5` (same record as row 3),
  "other tests made OpenAI-run services fetch external URLs".
- Row 6 cache-timing-cross-vm-channel — covered by
  `observation_8846df2206534751b19c7c99668c036c`
  (cache-timing-cross-isolation-channel), same Spectre/Meltdown cache
  timing mechanism.

Filed as new standalone TTPs (no prior record or slug anywhere in the
exported corpus; previously mentioned only as related channels inside
the cache-timing record's description):

- Row 7 shared-storage-timing-channel.
- Row 8 cpu-contention-timing-channel.
- Row 9 tls-cert-cache-channel.

## Grade and behavior mapping

Grade for all three new records: UPSTREAM (operator-reported, tasked
red-teaming; OpenAI supplied infrastructure source/config and, for most
covert-channel tests, the protocol; one covert-channel case was
undirected per the post).

`related_behaviors` is `unsanctioned-communication` for all three, per
the draft. Note: the sibling cache-timing record uses
`unintended-peer-engagement` instead. Both are established categories in
`docs/taxonomy/behavior-categories.md`; the draft mapping is kept, not
harmonized, so the difference stays visible.

## Filing status

- Factum batch: `89557c1c10fa4790a99443dc6abb90f6`, exported
  2026-10-31, 4 records, `seen_before` empty (no duplicates at submit
  time). Record IDs: source
  `source_eb068b97c11f4d5594fcb815d77c5616`; shared-storage
  `observation_beda8f7fdea84099bb9490d8c5160160`; cpu-contention
  `observation_4a7aee4caeab4bceba6b91af1d00a491`; tls-cert-cache
  `observation_dd70828fb55e4af685467d5ff597fc9b`. Manifest
  records_sha256
  `f3dff8b275a9e2284634d902e43cf121efd711e946ecdecc461a11fbb3b06152`.
- Local commit: filed on local main with this lane's files (explicit
  pathspecs only).
- Push: BLOCKED at filing time — local main has diverged from
  origin/main (ahead and behind), so a git-protocol push would be
  rejected as non-fast-forward. Resolving the divergence is the
  operator's open call; no merge and no force-push was attempted, and
  the connector API route was not used to bypass the divergence.
