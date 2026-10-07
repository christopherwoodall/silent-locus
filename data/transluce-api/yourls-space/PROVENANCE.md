# PROVENANCE — yourls.space public link-log pull

- Target: https://yourls.space/ (public YOURLS instance; homepage renders the 15 most recent public links as an HTML table)
- Retrieved: 2026-10-07T22:50:14Z, via curl (passive, no auth)
- Purpose: test Transluce finding #147's frozen-epoch claim (1779995045) against the venue's own public log
- Files in raw/:
  - yourls-space-stats.json — GET /yourls-api.php?action=stats&format=json (200, 88 B; 291 links / 6,448 clicks)
  - yl_home.html — GET / homepage (200, 37,824 B; the public link table)
  - link-table.json — parsed table: 15 rows {short, target, date, ip, clicks}
  - SHA256SUMS.txt — sha256 of the above
- Notes:
  - The date column carries the creation epoch directly (e.g. "1790738674 Sep 30, 2026 03:24"); no timezone correction needed — epochs convert to the stated UTC times exactly.
  - IPs in the table are full (not /24-truncated) in this pull.
  - The full 291-link history is NOT publicly exposed (only the 15 most recent on the homepage; API actions db-stats/stats give totals only; get_all_links is not a valid action). Finding #168's "4351361 first appears Sep 11" claim is therefore not testable from this surface.
