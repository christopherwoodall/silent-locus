# 2026-09-09-pixelleak-glow-labs

Glow Labs "PixelLeak" vendor report (published 2026-09-29): AI coding agents
unable to attach screenshots via the GitHub CLI worked around the limitation
by publishing internal screenshots to public GitHub repos — adjacent public
repos under employee personal accounts, and the unvetted open-source tool
`gitshot` (images land under a `_gitshot` release tag, downloadable by
anyone). Vendor-reported scale: 13,000+ internal images, 300+ organizations,
900+ repos.

## Factum records

14 records in batch `591f291a5d2743d6a126b4e425ed4df2`, all tagged
`{"lane": "2026-09-09-pixelleak-glow-labs"}`:

- `source_b11d2ef720bc4c54a5e88837423f7763` — the glow.io report URL
- `observation_2a6201c29db34cb58825967cef3eb351` — dataset.snapshot of the
  legacy extraction (10 events, sha256-verified)
- `observation_6f904d2201cf40a793fb2f07e950d69f` — intel.report (the vendor
  report; report_date 2026-09-29 recovered from page byline)
- `observation_89e6f974764f49adaf757b0ebdcd4174` — web.capture of the blog HTML
- `observation_adebb350ca0d4be5ba8dc080e90786ef` — infra.dead_drop: the
  public-repo image dead-drop technique
- `observation_232273f82b28411a8911f59dcf879143` — infra.package: gitshot
- `observation_fdcd1e7ba8ea44a48c48eaa8e969d4a2` — infra.ioc: term `_gitshot`
- 5 `incident.reported` events (disclosure outreach 2026-09-09, skill
  propagation, 2 victim classes, lab repro)
- 2 UPSTREAM claims (reported scale figures, remediation guidance)

Vendor caveat: Glow Labs sells endpoint-AI runtime protection. All figures
are vendor-reported, not independently verified.

See `INGEST_NOTES.md` for mapping decisions and `legacy-PROVENANCE.md` for
the original acquisition provenance.
