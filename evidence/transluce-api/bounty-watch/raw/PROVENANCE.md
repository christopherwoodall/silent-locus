# PROVENANCE — bounty-watch

- Source: https://rentahuman.ai/api/bounties (public, no login)
- Retrieved: 2026-10-07/08 UTC, via curl with 1.2–1.5s spacing between requests
- Method: cursor pagination per status (open, closed, paid, assigned, cancelled, completed); statuses expired/draft return empty
- Files:
  - bounties-page1.json — first unauthenticated pull (96KB)
  - bounties-raw-pageNN.json — per-page raw API responses
  - bounties-all.json — 58 unique from default feed (deduped)
  - bounties-all-statuses.json — 280 unique across all statuses (deduped)
- Note: Transluce #166/#167 reported 370 visible on 2026-10-07; our pull on 2026-10-08 returned 280. Difference is listing churn (closed/paid bounties age out), not a method gap.
- No account created, no contact with posters, no submissions. Passive only.
