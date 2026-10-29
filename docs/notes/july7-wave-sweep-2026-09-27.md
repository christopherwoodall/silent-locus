# LANE J — July-7 wave Diffend sweep (2026-09-27/28)

**Lane:** J (14-lane hunt follow-up). **Status:** sweep running, results land in batches.

## Context
The JFrog GemStuffer report (`notes/gem-jfrog-report-2026-09-27.md`) documents a
new **July 7, 2026 wave**: 215 packages / 333 releases, 03:03:09–18:13:42 UTC —
a third mechanism family our corpus has zero bytes for: **XSS PoCs in gem
metadata** (oast.online / webhook.site exfil) plus **SSTI probes**
(`<%= 7*7 %>`, `${7*7}`, `<%25= 7*7 %>`). Known July names from the report:
`xss-test-gem`, `attacker-xss-admin-1`, `xssname-1783397821`, `test-apex-gem`,
`test-ssti-0/1/4`. July authors used the `Testing <Animal>` format.

## Method
1. **Candidate list**: JFrog's public CSV
   (`data/gemstuffer-jfrog-2026-09-27.csv`) carries no per-row dates. Selected
   the 263 rows whose `Xray ID` matches `XRAY-1079xxx` — the analysis batch in
   which all named July-wave examples cluster. This is a *candidate filter only*;
   wave is **verified from each gem's Diffend publish timestamp**, never assumed.
2. **Sweep** (`scripts/sweep_july7.py`): read-only GETs to
   `https://my.diffend.io/gems/<name>` (~1 req/3s, 4-attempt backoff — Diffend
   closes connections mid-fetch). Phase 1 recovers versions + publish timestamps;
   phase 2 scans the first (or latest, if first is bare) version-diff page for
   mechanism markers: go-import/VCS, jina-laundering, webhook dead-drop
   (`/api/v1/web_hooks`, `A000`, `ZZEND`), XSS exfil (oast.online, webhook.site,
   `<script>`, `onerror=`), SSTI probes, empty-summary canary. Name grammars
   pattern-swept per record.
3. **Raw results**: `data/july7-wave/diffend_sweep_results_july7.jsonl`
   (resume-friendly, append-only); `data/july7-wave/progress.log`;
   provenance in `data/july7-wave/PROVENANCE.md`.
4. **ES**: own index `july7-wave` (`scripts/es_ingest_july7.py`), shared canonical
   schema (`notes/gems-es-mapping.json`), `event.dataset.keyword` multi-field at
   creation. Keep-all: every sweep record lands, discriminated by `in_diffend`
   / `diffend_wave`. record_kind: `diffend_sweep_july7`.

## Results (final: two passes + top-up, 2026-09-28)

- Candidates: **264** (263 XRAY-1079xxx rows + `attacker-xss-admin-1`, a named
  July example whose Xray id is XRAY-1078993, outside the batch range).
- **In Diffend: 9 — all verified July-7 wave** (Diffend publish timestamps):
  `apex-hijack-probe-a1` (Jul 7 18:43, 2 vers), `apex-oidc-probe` (15:43),
  `test-xss-name` (05:32), `test-xss-xss-data` (04:53, **xss-exfil**),
  `test-xss-xss-img` (04:53, **xss-exfil**), `test-xss-xss-link` (04:53,
  **xss-exfil**), `test-xss-xss-html` (04:53), `test_gem_kangaroo` (03:32,
  0.0.4, earliest), `test_gem_no_mfa` (06:34).
- True misses (HTTP 200, no version entries — yanked versions scrubbed from
  Diffend): 88, including `xss-test-gem` and `xss-dep-test`.
- Connection failures (Diffend closed the connection, both passes): 167 —
  includes `test-ssti-0/1/4`, `test-apex-gem`, `xssname-1783397821`,
  `attacker-xss-admin-1`. These are UNKNOWN, not confirmed absent.
- Mechanism markers: `xss-exfil` on 3 gems (the July XSS-PoC family confirmed
  in Diffend bytes); 4 hits have unrecovered phase-2 diff pages
  (IncompleteRead/RemoteDisconnected — markers unknown, not clean);
  2 clean scans (`apex-hijack-probe-a1`, `test-xss-name`, first versions only).
- Name grammars across candidates: apex_name 42, epoch_suffix 35,
  zz_prefix 33, test_name 27, xss_name 17, proxy_name 12, attacker_name 10,
  probe_name 4, ssti_name 3, oai_prefix 1, fetch_name 1.
- Wave check on the Xray batch: 2 May-27 gems (`a--0zlink83721`, `zlink83721`)
  were hits in the first pass but failed phase-1 in the retry pass — the
  XRAY-1079xxx batch is **not** pure July; wave was verified per-gem from
  Diffend timestamps, not assumed.

## Assessment

The July-7 XSS/SSTI mechanism family is **real in Diffend bytes** (3 gems with
xss-exfil markers, 04:53 UTC July 7), but Diffend has largely scrubbed the
yanked July versions: only 9 of 264 candidates still have version entries, and
JFrog's headline examples (`xss-test-gem`, the `test-ssti-*` trio) are either
gone or unreachable through the current hostility. The CSV remains the
canonical July inventory; Diffend is a partial, decaying mirror. 167
connection-failures are candidates for a later calm-window retry pass
(`--retry-failed` is implemented and resume-safe).

## Elastic
Index `july7-wave`: **264 docs** (keep-all), record_kind
`diffend_sweep_july7`, shared canonical schema, `event.dataset.keyword`
multi-field at creation. 9 docs `wave:2026-july-07`, 3 with mechanism markers.
