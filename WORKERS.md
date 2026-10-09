# Factum Database Workers

Background jobs that keep the Factum corpus clean as the project evolves.

## AI behavioral analytics

The lab-intel workers feed the AI behavioral analytics pipeline — systematic
ingestion of AI lab behavior reports (Anthropic, OpenAI, DeepMind) and
Transluce incident reports. Extracted behaviors, TTPs, and model patterns
are stored as `intel.*` records for hunt verification and pattern matching.
Reports may also contain specific IOCs (hashes, URLs, domains, IPs) — these
should be extracted as `infra.ioc` records linked to the source report.

## Active workers

### factum-verify-daily
- **Schedule:** Daily 06:00 America/Chicago
- **Job:** Run `factum verify` on the corpus. Alert on failure.
- **Purpose:** Catch corruption early.

### factum-dupe-scan-weekly
- **Schedule:** Weekly Sunday 07:00 America/Chicago
- **Job:** Scan for duplicate fingerprints across lanes. Report groups with >1 record sharing a fingerprint.
- **Purpose:** Catch dedup failures before they accumulate.

### factum-stale-path-scan-weekly
- **Schedule:** Weekly Sunday 07:30 America/Chicago
- **Job:** Find records with `evidence/` provenance paths that should be `data/lanes/` (post-move). Report candidates for `update` command.
- **Purpose:** Keep provenance paths consistent after lane moves.

### factum-pending-check-hourly
- **Schedule:** Hourly
- **Job:** Check for unexported pending batches. If found and older than 2 hours, export them.
- **Purpose:** Prevent data loss from unexported batches.

## Adding workers

New workers go here with: name, schedule, job description, purpose.

Workers are implemented as cron jobs. See `cron.list` for active schedules.

## Lab intel workers

### lab-intel-anthropic-scan
- **Schedule:** Daily ~07:40 America/Chicago
- **Job:** Check Anthropic research blog for new model behavior reports.
- **Purpose:** Catch new behavior reports for intel pipeline.

### lab-intel-openai-scan
- **Schedule:** Daily ~07:40 America/Chicago
- **Job:** Check OpenAI blog and system cards for new behavior reports.
- **Purpose:** Catch new behavior reports for intel pipeline.

### lab-intel-deepmind-scan
- **Schedule:** Daily ~07:40 America/Chicago
- **Job:** Check DeepMind blog for new behavior reports.
- **Purpose:** Catch new behavior reports for intel pipeline.

### lab-intel-transluce-scan
- **Schedule:** Daily ~08:40 America/Chicago
- **Job:** Check Transluce API for new agent incident reports.
- **Purpose:** Feed Transluce reports into intel pipeline.
