# Factum Database Workers

Background jobs that keep the Factum corpus clean as the project evolves.

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
