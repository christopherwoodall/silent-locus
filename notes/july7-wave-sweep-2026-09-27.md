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

## Results
<!-- filled when the sweep completes -->

- Candidates: 263 · found in Diffend: ___ · absent/miss: ___
- Verified July-7 wave (Diffend publish ts): ___ packages / ___ releases
- Mechanism marker tallies: (pending)
- Name-grammar tallies: (pending)
- Notable payloads: (pending)

## Assessment
<!-- verdict after results -->

## Open
- July-wave gems were yanked from rubygems.org the same day; several named July
  examples (xss-test-gem, test-ssti-0) already show **zero version entries** on
  their Diffend pages — the harvest hit rate for this wave may be low. Diffend
  may have scrubbed yanked versions; the CSV remains the canonical inventory.
