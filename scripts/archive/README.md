# archive/ — retired artifacts (kept, not deleted)

- `restore_elastic_exports_old.py` — the loader for the old elastic-exports/
  cloud snapshot. Retired 2026-09-29: the snapshot data was deleted
  (obsolete after the repo move + the collection rename/schema rebuild).
  Script kept for reference; it will not run without a snapshot tree.

## Root-script relocation inventory

All entries below were moved intact from the `scripts/` root unless noted.
**Historical only:** do not run these scripts as a routine ingestion or
maintenance step. Many assume their old `scripts/` location or a former
`~/workspace/silent-locus` checkout, reference retired paths/services, or
write data on import. Moving them does not certify them runnable. Review
inputs, output destinations, credentials, and side effects before any reuse;
none was executed during the reorganization.

| Directory | Role / files |
| --- | --- |
| `collectors/abusech/` | MISP download and redownload: `abusech_misp_dl.py`, `abusech_misp_redl.sh` (the shell script can remove invalid downloads). |
| `collectors/agent-surfaces/` | Agent-surface and Tantive collection/sweep: `capture_agent_surfaces.py`, `tantive_cascade.py`, `tantive_pull.py`, `tantive_sweep.py`. |
| `collectors/cors-bwa/` | CORS proxy ES pulls and analyses: `cors_bwa_collect.py`, `cors_bwa_analyze.py`, `cors_bwa_ladders.py`, `cors_bwa_other_hosts.py`. |
| `collectors/diffend/` | Diffend harvest, temporal/targeted checks, retries and July-7 sweep: `harvest_diffend.py`, `diffend_sweep.py`, `diffend_sweep_retry.py`, `diffend_merge_final.py`, `diffend_sweep_resweep_july7.py`, `diffend_temporal_sweep.py`, `diffend_targeted_check.py`, `sweep_july7.py`. Retry stays beside its imported sweep; targeted stays beside temporal, and its import/output paths now resolve relative to this checkout. |
| `collectors/dse-wiki/` | DSE verification search, report fetch, cache scan: `dse_wiki_verification_expand_search.py`, `dse_wiki_verification_fetch_reports.py`, `dse_wiki_verification_fetch_slow.sh`, `dse_wiki_verification_scan_cache.py`. |
| `collectors/gems/` | RubyGems fetch/mining and March-7/July-7 forensics: `fetch_gems.py`, `mine_gems.py`, `fetch_march7_rce.py`, `fetch_march7_versions.py`, `sweep_march7_rce.py`, `july7_forensics_fetch.py`, `july7_forensics_extract.py`. Never execute downloaded gem code. |
| `collectors/ludism/` | Ludism proxy capture, manifest and sweep: `ludism_proxy_fetch.py`, `ludism_manifest.py`, `ludism_pattern_sweep.py`. |
| `collectors/proxy-wiki/` | DemoWiki crawl, fingerprint extraction, paste/proxy sweep and IOC pivot: `crawl_demowiki.py`, `extract_f1f2.py`, `extract_f5f6.py`, `extract_wiki_proxy_urls.py`, `negative-sweep-f4f7f8f10f11f12.py`, `sweep_paste_bodies.py`, `sweep_proxy_primitives.py`, `wiki_ioc_pivot.py`. |
| `collectors/urlquery/` | URLQuery searches: `reverse_tunnels_htmx_search.py`, `urlquery_marker_sweep_run_sweep.py`, `urlquery_marker_sweep_run_sweep_v2.py`. |
| `collectors/yourls/` | YOURLS historical fetch/diff: `yourls_resweep_fetch_resweep.py`, `yourls_resweep_diff_resweep.py`. |
| `collectors/jsonhero/` | JSONHero historical fetch: `fetch_jsonhero_docs.py`. |
| `migrations/` | One-time note/schema/timestamp mutations: `add_defensive_takeaways.py`, `backfill_gem_timestamps.py`, `backfill_schema_2026_09_28.py`, `fix_empty_timestamps_2026_09_28.py`, `fix_iowa_timestamps_pastebin_fp_2026_09_28.py`. Do not replay blindly. |
| `es/` | Historical ES export/audit, Kibana dashboard build, unwind, body update, resweep upsert and cross-collection consolidated ingest: `es_export.py`, `audit_gem_counts.py`, `build_wiki_dashboards.py`, `es_unwind_admin_deletions.py`, `es_unwind_university_shorteners.py`, `es_update_paste_archive_bodies.py`, `es_upsert_july7_resweep.py`, `es_ingest_university_shorteners_consolidated.py`. The writers can change/delete ES or Kibana state; even read-only tools may contact live ES. |
| `visualization/` | Historical PIL graphic: `build_eval_cti_graphic_v2.py`. |

`archive/temp/` and `scripts/maintenance/` are owned by the separate
temporary-script workstream; this inventory does not cover them.
