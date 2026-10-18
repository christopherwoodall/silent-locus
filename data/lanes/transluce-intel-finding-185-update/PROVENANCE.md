# Transluce finding #185 — content update (versioned lane)

This lane records a VERSIONED UPDATE to tracker finding #185
(submitted 2026-10-16T19:04:55+00:00 by Ayush Bhardwaj). The original
finding-185 records (batch `f5c048669706460ba945a3b19f8171f7`, lane
`data/lanes/transluce-intel-finding-185/`) are NOT touched: history is
evidence. This lane adds one new `intel.report` record carrying the
verbatim NEW title/summary/description. No new `intel.behavior` records:
the addendum extends venue evidence only; no new behavior is demonstrated.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/185`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/185`
- Retrieved: 2026-10-18T13:41:29Z (UTC)
- Method: extracted verbatim from the full paginated census
  `findings-list_125_36-193_20261018T134129Z.json`
  (`GET /api/findings?limit=100&offset={0,100}` via `tl.py finding`
  machinery, `custom.transluce` connector, Secure Vault bearer token),
  per the API-work-complete directive; no new tracker request was issued
  for this lane build.
- sha256 (new version):
  `16173ec6ddcb5585f24fe9cf26b57d230c2a35f8eef2da15c6efd2e5a84aa63c`
- Old version cached at
  `data/lanes/transluce-intel-finding-185/raw/finding-185_20261017T115837Z.json`
  (sha256 `9eee9deefcd65987bc30845cf8c04cd2e08fd202d3041b843ed3520e975336d2`).

## What changed (observed)

- Summary reworded. Old: "Sep 20, 2026: a self-described “Green AI Bot”
  posted a UseMod sandbox pulse, reverted 39 minutes later. Related public
  posts share its name and wording; AI authorship, cross-site identity and
  autonomous coordination remain unverified." New: "Sep 20, 2026: “Green
  AI Bot” pulse messages appear on UseMod and Wikiservice DictSm; the
  UseMod post was reverted. Related public posts share wording. AI
  authorship, common cross-site identity and autonomous coordination remain
  unverified."
- Description extended 1,610 -> 3,733 characters: an evidence addendum
  reviewed 2026-10-18 appends the Wikiservice DictSm GreenAiBotPing page +
  diff + RecentChanges RSS captures (with SHA-256 hashes) and reproducibility
  hashes:
  page `73a6f9b1d6e68bb0ac5f4864965b1a7a6e4288b8e6030231500ad59a162a2ce5`,
  diff `6241df36c51e973566650cf346671390ab1862ad1f5ceb47ecf1b6bb4587b3e7`,
  RSS `6e36abff9a828eaf8571ea02f6982a15e2dbf729899346515bddedf9ddf54a24`.
- The addendum is a bounded evidence extension: it does not authenticate an
  AI runtime, provider, or common cross-site operator, and is not a new
  incident.

## updated_at timeline (observed, recorded honestly)

Cached census files show, for finding 185:

- 2026-10-17 11:58Z census + old cached single pull: updated_at
  `2026-10-16T19:04:55Z`, description 1,610 chars.
- 2026-10-18 07:00 CDT hook census + 2026-10-18 13:41:29Z census:
  updated_at `2026-10-17T21:19:49Z`, description 3,733 chars.

That is a FORWARD move, consistent with the appended addendum. The task
brief for this run suggested a BACKWARD anomaly (21:19:49Z -> 19:04:55Z);
that did NOT reproduce in any cached census file inspected (all five
2026-10-11..2026-10-18 census files were checked). Recorded as a
discrepancy; no action taken on it. If the API later serves a lower
updated_at again, that would be a genuine API-side quirk worth flagging.

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown". AI authorship,
cross-site identity and autonomous coordination remain unverified per the
finding's own limits.
All claims below are cited as reported (UPSTREAM), not as independently
verified.
