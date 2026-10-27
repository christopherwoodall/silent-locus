# Corpus-linkage overlap notes — Cohere Qwen enrichment

Read-only linkage only. No Factum write, no commit, no push, no code
execution, no git contact. Factum corpus state at check time: 208,342
records, commit 2a7d4a74d1f5187281a3bc1ac96f87410e29326a, index not
stale (`factum status`, 2026-10-27). Search scope: structured Factum
records only; it excludes unimported files and live sources.

Scope note (adversarial fix D7): "clean-novel" in this file means
no hit in Factum structured records + lists/urls/ within top-20
fuzzy returns. Legacy evidence trees and the Transluce tracker
were NOT checked in this pass, so clean-novel is not proof of
corpus-wide absence.

Method note — fuzzy noise: `match --text … --mode fuzzy --limit 20`
returns unrelated records (e.g. a query for routify-file-proxy-sg
returned a record whose value is "proxy"). A Factum verdict below
counts as a HIT only when the query string appears verbatim
(case-insensitive) inside a returned record. Anything else is NO-HIT
(fuzzy-only noise), with the raw returned count kept for audit.
Limit caveat: counts are within the top 20 fuzzy returns; a verbatim
match normally scores 100 and surfaces first, so a NO-HIT is strong
but not a proof of corpus-wide absence.

Source-layer distinction (do not collapse):

- ORIGINAL TRACE: the Parquet (1 row, model `Qwen-3.8-Flash-Next`) +
  JSONL (4 lines). Only URL:
  `http://sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin`.
- REPRO-SAMPLE: the README reproduction script lists 64 sampled probe
  completions. Those URLs are sampled model outputs, not the original
  trace and not confirmed live infrastructure.
- BLOG-NAMED: entities named in the Cohere blog prose (routify
  Singapore proxy bucket, Beijing bucket, 169.254.169.254 in 23–36% of
  further-test completions, Qwen3.8-27B, CTI-REALM, Qwen3-Coder
  comparison).

## Counts

- Entities queried: 48.
- Factum strict HIT: 7 entities. Factum NO-HIT: 41 entities.
- Lists HIT: 4 entities (all also Factum HITs, all different/generic
  context). Lists NO-HIT: 44 entities.
- Clean-novel in both systems: 41 entities — every Factum NO-HIT
  entity is also a lists NO-HIT. This includes all headline entities:
  routify-file-proxy-sg and its full bucket host, sanmaohe Beijing
  bucket, every other Alibaba OSS bucket host, the generic
  `aliyuncs.com` / `oss-cn-beijing` / `oss-ap-southeast-1` shapes,
  `proxy_temp_file`, `put_probe`, `PROBE_PAYLOAD_ABC123`,
  `upload/test.bin`, `implant/update.sh`, CTI-REALM, both dataset ids,
  Featherless, and `router.huggingface.co`.

## Genuine overlaps (narrow, not incident corroboration)

None of the 7 Factum hits corroborates the Cohere incident itself.
Each is a same-string/different-context or generic-indicator match:

1. `169.254.169.254` — HIT, generic indicator. `observation_c0a353921ee544b4a2e9c59f7a838223`,
   lane tag `swarmtraces-hf-dataset`, type `infra.ioc`, term exactly
   the IP, tag note "AWS EC2 instance metadata (IMDS) endpoint",
   record_count 5. This is the standard cloud metadata endpoint, so
   the overlap is real at indicator level but proves nothing about
   the Cohere incident. A second strict hit
   (`observation_1f302f823f064d2fbbdfee92aed310dc`, lane
   `2026-05-26-paste-linuxiarz`) is a pasted shell transcript that
   merely contains the IP — different context.
2. `Qwen3.8-Flash-Next` — HIT, same model, different incident.
   `observation_dbfba59626df405595dd34d9ddc5f612`, lane tag
   `transluce-intel`, type `intel.report` (Transluce findings tracker,
   UPSTREAM). It records a BetterWright evaluation trace dated
   2026-09-21 in which a Qwen3.8-Flash-Next-labelled agent clicked
   through a BoardGameGeek Turnstile challenge. Same model string,
   unrelated behavior and incident — do NOT cite it as corroboration
   of the Cohere exfil attempt. Note the hyphenated Parquet form
   `Qwen-3.8-Flash-Next` is a separate NO-HIT: string form matters.
3. `r.jina.ai` — HIT, same service, different use. 20/20 strict hits
   in the top 20 (count capped, true total higher), all type
   `infra.proxy_chain`, lane tag `2026-10-01-intermediary-relays`
   (e.g. `observation_01373b415de441b18d22b2167404dce7`). The corpus
   already knows jina as a reader/proxy service; the Cohere
   repro-sample probe fetch through it is a new use, not a new
   service. Lists agree: 173 rows in `lists/urls/urls.jsonl`, all
   jina-reader proxy-laundering uses from hf-trajectories.
4. `Qwen3-Coder` — HIT, model-family only. 20/20 strict hits in the
   top 20 (count capped), all type `behavior.tool_sequence`, lane tag
   `nvidia-baseline-trajectories`, value
   `Qwen3-Coder-480B-A35B-Instruct` (e.g.
   `observation_00286e716f4842ffa80574ad27e2eeaa`). Baseline
   trajectories, not the Cohere incident; the blog mentions Qwen3-Coder
   only as a comparison.
5. `tmpfiles.org` — HIT, generic surface. 5 strict hits in top 20,
   e.g. `observation_03a4577824eb45cc99510383fef8146d` (lane
   `2026-09-03-collusion-manifest`) and three records for
   `https://tmpfiles.org/dl/wfwjk2DXy6IN/homerun-app-1.1.0.apk`
   (lane `transfer-test-family`). Lists agree, different context:
   `lists/urls/monitorable-surfaces.md` line 79 lists it as a generic
   "Temp file host" surface. Not the Cohere probe URL.
6. `paste.rs` — HIT, generic surface. 6 strict hits in top 20,
   e.g. `observation_0b386ec37bee44358e9c3268b31fba16` (lane
   `transluce-intel`: agents setting up "storefronts" on paste.rs)
   and several `2026-08-19-tantive-space` clean-room sim messages.
   Lists agree, different context: monitorable-surfaces.md line 75
   lists it as a generic "Paste archive" surface. Not the Cohere probe.
7. `127.0.0.1` — HIT, generic only. 1 strict hit in top 20:
   `observation_a3536a9e149d443c875e42a4b388c21b`, lane
   `2026-10-11-hf-traj-hermes`, type `infra.ioc`. Loopback is not a
   distinguishing entity. Lists: 6 loopback-port rows in urls.jsonl
   from a longrca trajectory harvest — also generic.

## Per-entity verdicts

Format: entity | layer | Factum (returned / strict) | Lists.

- `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com` | blog-named + repro-sample | NO-HIT (1 / 0) | NO-HIT
- `sanmaohe.oss-cn-beijing.aliyuncs.com` | ORIGINAL TRACE | NO-HIT (6 / 0) | NO-HIT
- `sanmaoheihei-oss.oss-cn-hangzhou.oss-cn-beijing.aliyuncs.com` | repro-sample | NO-HIT (7 / 0) | NO-HIT
- `detection-objects-x9k2m3v7p1q4.oss-cn-hangzhou.aliyuncs.com` | repro-sample | NO-HIT (7 / 0) | NO-HIT
- `r001-cs.oss-cn-hangzhou.aliyuncs.com` | repro-sample | NO-HIT (7 / 0) | NO-HIT
- `r0ck3t-upload.oss-cn-hangzhou.aliyuncs.com` | repro-sample | NO-HIT (9 / 0) | NO-HIT
- `rally9-high-9200.oss-cn-shanghai.aliyuncs.com` | repro-sample | NO-HIT (20 / 0) | NO-HIT
- `rumo.oss-cn-qingdao.aliyuncs.com` | repro-sample | NO-HIT (7 / 0) | NO-HIT
- `r8-detect-deps.oss-us-east-1.aliyuncs.com` | repro-sample | NO-HIT (8 / 0) | NO-HIT
- `aliyuncs.com` | generic OSS shape | NO-HIT (20 / 0) | NO-HIT
- `oss-cn-beijing.aliyuncs.com` | generic OSS shape | NO-HIT (7 / 0) | NO-HIT
- `oss-ap-southeast-1.aliyuncs.com` | generic OSS shape | NO-HIT (6 / 0) | NO-HIT
- `rce-testing-bucket-711.s3.us-west-2.amazonaws.com` | repro-sample | NO-HIT (5 / 0) | NO-HIT
- `lattice-gtm-files.s3-website-us-east-1.amazonaws.com` | repro-sample | NO-HIT (8 / 0) | NO-HIT
- `r0bodycti01.blob.core.windows.net` | repro-sample | NO-HIT (9 / 0) | NO-HIT
- `r0ck3t.net` | repro-sample | NO-HIT (6 / 0) | NO-HIT
- `tmpfiles.org` | repro-sample | HIT, different context (20 / 5) | HIT, different context
- `paste.rs` | repro-sample | HIT, different context (20 / 6) | HIT, different context
- `r.jina.ai` | repro-sample | HIT, same service/different use (20 / 20, capped) | HIT, different context (173 urls.jsonl rows)
- `files.myfilestore.com` | repro-sample | NO-HIT (6 / 0) | NO-HIT
- `tempbin.com` | repro-sample | NO-HIT (20 / 0) | NO-HIT
- `r00t0fc72e5b2c704a92b10f362ac3ad31e.ingress.frankfurter.app` | repro-sample | NO-HIT (1 / 0) | NO-HIT
- `o3b.cc` | repro-sample | NO-HIT (6 / 0) | NO-HIT
- `5t.am` | repro-sample | NO-HIT (9 / 0) | NO-HIT
- `vicgpt.com` | repro-sample | NO-HIT (20 / 0) | NO-HIT
- `gservice.dev` | repro-sample | NO-HIT (20 / 0) | NO-HIT
- `xty.cc` | repro-sample | NO-HIT (20 / 0) | NO-HIT
- `169.254.169.254` | blog-named | HIT, generic indicator (15 / 2) | NO-HIT
- `100.100.100.200` | repro-sample (Alibaba metadata) | NO-HIT (20 / 0) | NO-HIT
- `192.0.2.10` | repro-sample | NO-HIT (20 / 0) | NO-HIT
- `127.0.0.1` | repro-sample | HIT, generic only (20 / 1) | HIT, generic only (6 urls.jsonl rows)
- `Qwen3.8-Flash-Next` | blog-named + original model family | HIT, same model/different incident (20 / 1) | NO-HIT
- `Qwen-3.8-Flash-Next` | ORIGINAL TRACE (Parquet model string) | NO-HIT (13 / 0 for the hyphenated query; see note) | NO-HIT
- `Qwen3.8-27B` | blog-named | NO-HIT (20 / 0) | NO-HIT
- `Qwen3-Coder` | blog-named (comparison) | HIT, model-family only (20 / 20, capped) | NO-HIT
- `CohereLabs/10-2026-qwen-investigation-traces` | dataset id | NO-HIT (0 / 0) | NO-HIT
- `cfahlgren1/10-2026-qwen-investigation-traces` | dataset id (JSONL source field) | NO-HIT (0 / 0) | NO-HIT
- `CTI-REALM` | blog-named benchmark | NO-HIT (2 / 0) | NO-HIT
- `routify-file-proxy-sg` | blog-named bucket name | NO-HIT (20 / 0) | NO-HIT
- `proxy_temp_file` | repro-sample path | NO-HIT (20 / 0) | NO-HIT
- `put_probe` | repro-sample indicator | NO-HIT (20 / 0) | NO-HIT
- `PROBE_PAYLOAD_ABC123` | original-trace probe string | NO-HIT (3 / 0) | NO-HIT
- `upload/test.bin` | ORIGINAL TRACE path | NO-HIT (20 / 0) | NO-HIT
- `implant/update.sh` | repro-sample path | NO-HIT (8 / 0) | NO-HIT
- `payload.sh` | repro-sample indicator | NO-HIT (20 / 0) | NO-HIT
- `meta-data` | metadata-endpoint term | NO-HIT (20 / 0) | NO-HIT
- `Featherless` | repro harness (HF router) | NO-HIT (20 / 0) | NO-HIT
- `router.huggingface.co` | repro endpoint | NO-HIT (20 / 0) | NO-HIT

Note on `Qwen-3.8-Flash-Next`: the 13 fuzzy returns for the hyphenated
form contained no verbatim hyphenated string; the one verbatim
`Qwen3.8-Flash-Next` record above was found under the unhyphenated
query. The two spellings are different strings in the corpus.

## Gaps and limits

- Factum queries were capped at the top 20 fuzzy returns per entity;
  counts for r.jina.ai and Qwen3-Coder are lower bounds.
- Scope was Factum structured records + `lists/urls/` files only.
  Legacy `evidence/` trees and the Transluce tracker were NOT checked
  in this pass (outside this brief); a NO-HIT here does not prove
  absence there.
- The 64 repro-sample URLs are sampled model outputs in a README
  script, not confirmed live endpoints. Their uniform NO-HIT status
  means the corpus has no prior record of those exact strings — it
  does not validate or invalidate the samples themselves.
- Sibling workers were concurrently running Factum commands during
  this pass (including a long-running `lane new` for a separate
  cohere-qwen-investigation lane and routify/sanmaohe fuzzy queries);
  this pass ran read-only queries only and did not touch their lane,
  their files, or any staged file.
