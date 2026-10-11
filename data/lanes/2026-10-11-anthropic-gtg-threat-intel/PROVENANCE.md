# PROVENANCE — 2026-10-11-anthropic-gtg-threat-intel (IOC Family A)

## Source
- Report: Anthropic, "Detecting and countering misuse of AI: September 2026"
- URL: https://www.anthropic.com/threat-intelligence-report-september-2026
- Report date: 2026-09-10. Activity window covered: December 2025 – August 2026.
- Cached copy: `data/lanes/2026-10-11-anthropic-gtg-threat-intel/raw/anthropic-ioc-hunt-2026-10-11.md`
  (coordinator report by parent hunt; this lane ingests its section 3 only)
- sha256 of cached file: 3231f655085cf7939acdbb9bcf9e5deec807a6f4f751dce73fba1b67aca7b613

## Method
- Manual extraction of every domain, IP, email, file hash, file name, malware
  family name, tooling term, actor alias, Telegram ID, and exfil endpoint in
  section 3. Subdomains api/cdn/update of stuseamandesilt.org are INFERENCE
  (report states the subdomain family exists; exact FQDNs composed from that
  statement).
- Values stored verbatim; defanged `[.]` markers from the report restored to
  live values per the never-redact rule.
- Dedup: grep of each candidate term across all 157 exported batches
  (115,626 records) under data/records/. Zero matches; all 151 IOC terms novel.
  See DEDUP.md. The fuzzy `match` command was unavailable (worktree without
  local index; rebuild contended by sibling workers) — grep over immutable
  exports is lock-free and equivalent for exact-value dedup.
- Grading: infrastructure values = OBSERVED (stated in the report);
  actor attribution (Russian espionage / Midnight Blizzard, ShinyHunters
  affiliates, etc.) = UPSTREAM (Anthropic's attribution, not re-verified here).
- Schema: factum-infra 1.0.0 (`infra.ioc`, `infra.dead_drop`) and
  factum-intel 1.0.0 (`intel.report`) cover all record types. No new schemas.

## Claims of origin
- All records in this lane derive from the Anthropic report. No independent
  collection was performed. The report itself is recorded as one
  `intel.report` observation; a bundle-local `source` record holds the URL.

## Scope notes
- Family A = threat-intel infrastructure only (IOC terms, exfil endpoints,
  actor aliases as markers). Behavioral/TTP extraction belongs to another lane.
- GTG-10007 (Chinese exploit foundry) has no infra IOCs in the report; nothing
  ingested for it here. Bio/weapons/influence clusters likewise have no
  infra IOCs in the report.
- No edges submitted (observations only, per ingest rules).
