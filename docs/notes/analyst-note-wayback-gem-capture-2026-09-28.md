# Analyst note: Wayback capture of a GemStuffer gem page is post-yank, payload not preserved

2026-09-28 — lane12 follow-up (`data/wayback-gem-capture/`)

## The hit
The lane12 Wayback sweep (300/370 targets, DONE) returned exactly one hit:
a Wayback capture of `rubygems.org/gems/zztargettest18587`, timestamp
**2026-08-10 00:49:52 UTC**. The gem is a zz target-test family gem from the
May go-import injection campaign (all 555 gems yanked; our corpus holds
Diffend publish-time snapshots). The capture post-dates the yank wave, so
the question was whether the payload stayed publicly visible via the archive.

## What the capture shows
Fetched read-only via the `id_` replay
(`https://web.archive.org/web/20260810004952id_/https://rubygems.org/gems/zztargettest18587`,
HTTP 200, 37,279 bytes, sha256 `c3d654b76bd20637ac3f475310b13ed4f23abd4fe5ae2b021fa6dbc7fd30d98a`).
The page is in **yanked state**:

| signal | archived page | Diffend snapshot |
|---|---|---|
| go-import meta tag | absent | `<meta name="go-import" content="rubygems.org/api/v1/gems/zztargettest18587.yaml\n  hg https://r.jina.ai/http://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx?M=1%26Y=2026">` |
| VCS value | n/a | `hg` |
| payload URL | n/a | `https://r.jina.ai/http://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx?M=1%26Y=2026` (Lambeth council calendar, r.jina.ai-laundered) |
| versions listed | none (no Versions tab, no 0.0.1) | 0.0.1 |
| description block | absent | `sum` (summary), go-import in description |
| yanked banner | "Yanked by: rubygems-security-team" | n/a (pre-yank snapshot) |
| owner | `southnews5j23447n` | `a` (author field "a"; owner profile is `southnews5j23447n` per archive) |

Verdict: **the Wayback capture does NOT preserve the campaign payload.**
The archive captured the yanked placeholder, not the malicious page.
Note rubygems.org serves yanked gem pages as HTTP 200 (not 404) — both the
original capture and the replay are 200s of the yanked state.

## Implication
For the RubyGems campaign, Diffend's publish-time snapshots are the only
public post-mortem source of the payload bytes — Wayback cannot substitute.
Wider: for any yanked-package forensics, archive coverage of the *page* is not
evidence of archive coverage of the *payload*. Diffend-style
publish-time indexing (which snapshots tarballs at publish) is the durable
record; page-level archives degrade to yank banners within the takedown
window. This is a data-source asymmetry worth encoding in future hunt lanes:
when checking archived campaign artifacts, always check whether the capture
pre- or post-dates the takedown, and prefer artifact snapshots over page
captures.

## Records
Capture bytes + SHA-256 manifest + fetch log + comparison row:
`data/wayback-gem-capture/`. Ingest to `rubygems-goimport-campaign`
(hosted Elastic) queued until the write freeze lifts.
