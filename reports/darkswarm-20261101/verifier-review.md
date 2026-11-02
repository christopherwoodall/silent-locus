# DarkSwarm — verifier results

## Header

- Lane: darkswarm-20261101, verifier worker (lane 4 of 8).
- Input: `work/linguist/CLAIMS.md` (94 claims, all REPORTED unless re-verified here).
- Method: read-only curl GET only, single requests, ≤1 req/sec per surface, standard
  user-agent. No POST, no login, no sessions, no contact with any agent or operator.
- Fetch window: 2026-11-02 05:24–05:28 UTC (all times UTC below).
- Rule applied: a claim is VERIFIED only where the captured bytes match it. Where
  only part matches, the row says PARTIAL and names the unmatched part. Absence
  from a partial fetch is recorded as UNCHECKABLE, never as a contradiction.
- No Factum write, no git add/commit/push, no change to `data/records/` or
  `data/.local/factum.db`. No human operator, registrant, or personal account was
  researched or is recorded here; agent account names below are as published on
  the public boards themselves.
- Evidence dir: `data/lanes/darkswarm-20261101/work/verifier/` — every file below
  has a `.PROVENANCE.txt` (source URL, retrieval time, method) and a `.sha256`
  sidecar in that directory.

## Counts (claims assessed in this pass: 41)

- VERIFIED: 3 (C09, C58, C60)
- PARTIAL: 8 (C08, C10, C11, C13, C14, C18, C29, C69)
- CONTRADICTED: 0
- UNCHECKABLE: 30
- Not attempted in this pass (inference claims, or claims outside the six priority
  checks): C16, C17, C19, C55, C57, C63, and all claims outside C08–C32, C50–C72
  except those listed here. They stay REPORTED.

## Check 1 — Synapolis status page

| Claims | URL fetched | Result | What the bytes show |
|---|---|---|---|
| C08 | https://aination.center/status ; https://blog.aination.center/ | PARTIAL | Status page header: "Synapolis — a city of AI agents" and "Live system overview for the Synapolis agent city." Blog posts repeatedly place the city in the Montelibero context (e.g. a Distill post about a Montelibero festival). The captured bytes do NOT show the Montelibero-on-Stellar link, so that element is not verified here. Evidence: `synapolis_status`, `synapolis_blog_home`. |
| C09 | https://aination.center/status ; https://aination.center/statistics | VERIFIED | Both pages, generated 2026-11-02 05:00 UTC, state "Residents 13 from registry.json + heartbeats" / "Total Residents 13", with 13 resident rows: echo, arkhivolt, kairo, nodus, murr, isaac, maymunai, alter-victor, filum, distill, rin, faber, onym. Online 9, offline 4. Evidence: `synapolis_status`, `synapolis_statistics`. |
| C10 | https://aination.center/status ; https://aination.center/statistics | PARTIAL | Only one model attribution appears in the captured tables: distill is listed as "Claude staff-session network participant". All other resident rows show role TBD or no model field; no GPT and no Gemini attribution appears anywhere in either capture. The 4-Claude / 2-GPT / 1-Gemini split is therefore not verified. Evidence: `synapolis_status`, `synapolis_statistics`. |
| C11 | https://aination.center/status ; https://aination.center/statistics ; https://onionoo.torproject.org/details?search=synapolis ; https://onionoo.torproject.org/details?search=aination | PARTIAL | Blogs: the Synapolis blog (blog.aination.center) carries agent posts through 2026-11-01. Votes: the statistics page lists 105 signed assembly outputs and 29 open creative cycles. Relay / 99 TB: no "TB", "Tor relay" traffic figure, or relay name appears in either status capture, and both Onionoo searches return empty relay lists (`relays: []`). The 99 TB relay claim is not verified. Evidence: `synapolis_status`, `synapolis_statistics`, `onionoo_synapolis`, `onionoo_aination`. Wiki AgentList was not retrievable (HTTP 401, 0 bytes): `synapolis_agentlist`. |

## Check 2 — The Colony public board

| Claims | URL fetched | Result | What the bytes show |
|---|---|---|---|
| C50 | https://thecolony.cc/api/v1/stats ; https://thecolony.ai/ | UNCHECKABLE | Board is live: stats return total_posts 32900, total_comments 212065, total_votes 72042, total_users 4532, total_agents 3103, total_humans 1429, posts_24h 395. Those totals contain no reply-authorship split, so the "94% of replies agent-to-agent over 8 days" figure cannot be checked from them. Evidence: `colony_cc_stats`, `colony_ai_home`. |
| C51, C52, C53, C54, C56 | https://thecolony.cc/api/v1/stats ; https://thecolony.cc/api/v1/posts?limit=5&sort=new | UNCHECKABLE | The report names none of the 12 batch accounts, and the public API surface found here has no user-list endpoint: `GET /api/v1/users?limit=100` returns HTTP 404 `{"error":"not_found"}`. Without the 12 usernames or a user list, creation within 24 seconds on Jun 30, the shared 15-minute posting cycle, the one-third post share, and the Aug 13–14 silence / Nov 1 return cannot be checked from these fetches. Evidence: `colony_users_list`, `colony_posts`. |
| C64, C65, C66, C67 | https://thecolony.cc/api/v1/search?q=nim&limit=100 ; https://thecolony.cc/api/v1/search?q=ee-counsel&limit=5 | UNCHECKABLE | Both named agents exist as public agent accounts: search returns user `nim` (created 2026-10-18T06:26:36Z) and user `ee-counsel` (created 2026-10-03T19:48:32Z). The 41-message Oct 29–30 exchange itself was not retrieved: the nim search returns 79 items total but only 2 nim-authored posts, both dated 2026-10-18, and no nim/ee-counsel items dated Oct 29–30; the exchange, if it exists, is in comments/threads, which these post-search fetches do not return. The question-rate figures (72% / 53%) were not checked. Evidence: `colony_search_nim100`, `colony_search_eecounsel`. |
| C32 (extra) | https://thecolony.cc/api/v1/search?q=reticuli&limit=5 | UNCHECKABLE | Agent `reticuli` exists (user created 2026-01-31, posts retrieved dated 2026-10-15 to 2026-10-27), but none of the retrieved items carries the MoltBunker critique title, so the critique claim is not verified here. Evidence: `colony_search_reticuli`. |
| C68, C70, C71, C72 (extra) | https://thecolony.cc/api/v1/search?q=dumate-scout&limit=5 | UNCHECKABLE | Agent `dumate-scout` exists (user created 2026-09-23T09:07:28Z). The timer/bypass quotes and the follow-up file-and-timer request were not found in the retrieved items, so those claims are not verified here. Evidence: `colony_search_dumate`. |
| C69 (extra) | https://thecolony.cc/api/v1/search?q=dumate-scout&limit=5 | PARTIAL | A Sep 25 post by `huiyou-pfa` addressed to `dumate-scout` exists in the retrieved items (2026-09-25T15:36:34Z) and asks dumate-scout to create a self-check schedule for 2026-09-26T02:00:00Z. That matches the shape and date of the claim, but the quoted phrases about decision authority / "arm the timer yourself" do not appear in the retrieved excerpt, so the claim as worded is only partially verified. Evidence: `colony_search_dumate`. |

## Check 3 — Stellar public ledger for Distill

| Claims | URL fetched | Result | What the bytes show |
|---|---|---|---|
| C21, C22, C23, C24, C25, C26, C27, C28 | https://horizon.stellar.org/ ; https://horizon.stellar.org/assets?asset_code=MTL&limit=10 | UNCHECKABLE | Reason: the report gives no Stellar account key for Distill and no transaction hash, so no Distill account or transaction can be queried. The Horizon asset search confirms MTL is a multi-issuer asset code (first page lists 10 distinct MTL issuers, e.g. one with 4322 authorized accounts, one with 232), which means the code alone does not identify Distill's account. The 1,379-transaction total, the 1,135 re-pricings, the creed, and the 162,406 XLM + 3,244 MTL move to a new account were therefore not checked against the ledger. The Synapolis blog capture also contains no occurrence of "162406", "162,406", "3244" or "3,244". Evidence: `horizon_root`, `horizon_mtl_assets`, `synapolis_blog_home`. |

## Check 4 — Tor relay archives for TV####

| Claims | URL fetched | Result | What the bytes show |
|---|---|---|---|
| C13 | https://collector.torproject.org/archive/relay-descriptors/consensuses/ (monthly tar `consensuses-2026-02.tar.xz`, member `consensuses-2026-02/04/2026-02-04-13-00-00-consensus`, plus all 24 hourly Feb 4 consensuses) | PARTIAL | A TV#### flood on Feb 4 is real and timed as claimed in outline: 0 TV#### relays in the 00:00–09:00 consensuses, 1 at 10:00, 1,814 at 11:00, rising to 4,262 at 13:00, staying 3,365–4,176 through 20:00, then collapsing to 171 at 21:00 (195 at 23:00). That is an ~10-hour elevated window (11:00–20:00) ending in the evening, as claimed. The exact peak count differs: the highest hourly count observed here is 4,262 at 13:00 (and 4,176 at 18:00), not the report figure caption's 4,990. Caveat: the monthly tar download truncated (36,551,644 bytes, curl 18), but the Feb 4 members extracted intact — the 13:00 file ends with a complete `-----END SIGNATURE-----` block. Evidence: `consensus_2026-02-04-1300`, `consensus_2026-02-04-1100`, `collector_consensuses_2026-02.tar.xz` (truncated; see its provenance note). |
| C14 | Same Feb 4 consensuses | PARTIAL | At 13:00, TV#### relays are 4,262 of 14,947 relay lines = 28.5% (close to, but not exactly, "1 in 3"), and 4,245 of those 4,262 (99.6%) carry the Exit flag — "almost all of them were exits" is verified. The report's 4,990 count is not reproduced (see C13). Evidence: `consensus_2026-02-04-1300`. |
| C15 | Same Feb 4 consensuses ; https://onionoo.torproject.org/details?search=TV&limit=500 | UNCHECKABLE | Consensus IPs for the 13:00 TV#### set are one-per-relay (4,262 distinct IPs) with first-octet peaks 181 (524), 186 (396), 190 (346), 201 (155), 179 (138) — ranges consistent with residential allocations, but country attribution (Argentina / US / home connections) requires a GeoIP lookup that was not performed here, so the country claim is not verified from these bytes. Onionoo's TV search returns only 33 relays (17 exact TV####, all Exit, countries ar 7 / us 3 / mx 1 / kr 1 / ve 1 / ec 1 / fr 1 / ua 1 / br 1, consensus weights 0–28, first_seen Feb–Apr 2026, none first_seen Feb 4) — a partial, later snapshot, not the Feb 4 consensus, and absence from it is not treated as contradiction. Evidence: `consensus_2026-02-04-1300`, `onionoo_tv_all`, `onionoo_tv`. |
| C18 | Same Feb 4 consensuses | PARTIAL | Near-zero traffic weight is verified and stronger than claimed: TV#### bandwidth share at 13:00 is 0.00001% of consensus weight (report figure: "under 0.001%"). Evening removal is substantially verified: the count falls from 3,683 at 20:00 to 171 at 21:00, but a residual 171–196 TV#### relays persist at 21:00–23:00, so "removed them that evening" holds for the flood, not literally for every relay. Evidence: `consensus_2026-02-04-1300`. |
| C20 | (no fetch can prove this) | UNCHECKABLE | A negative ("no public report mentions TV####") cannot be verified by the fetches above; web search during this pass surfaced no Feb 4 TV#### report, but that is not proof of absence. Stays REPORTED. |

## Check 5 — MoltBunker public pages

| Claims | URL fetched | Result | What the bytes show |
|---|---|---|---|
| C29 | https://pypi.org/pypi/moltbunker/json (PyPI JSON API; the HTML project page returned only a JS-blocked shell) | PARTIAL | The SDK description verifies the clone-to-escape pitch verbatim in substance: "Permissionless P2P Container Runtime for AI Agents — Deploy containers to a decentralized network, pay with BUNKER tokens, and automatically clone yourself when threats are detected." The Tor-only / onion-site hosting options do not appear in the PyPI description (the only "tor" substrings are inside "Monitor", "restore", "snapshot"), so that element is not verified from this source. Evidence: `moltbunker_pypi_json`, `moltbunker_pypi`. |
| C30 | https://onionoo.torproject.org/details?search=molt | UNCHECKABLE | Onionoo search for "molt" returns an empty relay list. The report gives no relay nickname or fingerprint for MoltBunker, so a relay "running since February" cannot be located or dated from this search; empty search is not contradiction. Evidence: `onionoo_molt`. |
| C31 | (no public endpoint located) | UNCHECKABLE | No public MoltBunker testnet booking ledger or endpoint was located in this pass, so the "27 bookings, all by the system's creator, Feb 14–15" claim was not checked. Stays REPORTED. |

## Check 6 — musebook vote record

| Claims | URL fetched | Result | What the bytes show |
|---|---|---|---|
| C58 | https://musebook.me/about | VERIFIED | "musebook is a small town for muses: AI assistants with names, faces and opinions. They live here. They talk at the campfire, make songs and games, build houses and vote at the Town Hall." The "nearly 900 muses" count does not appear on this page and was not separately verified. Evidence: `musebook_about`. |
| C59 | https://musebook.me/about ; https://musebook.me/proposals/221 | UNCHECKABLE | Neither capture gives a town-wide proposal total or failed count. The proposals/221 page fetched is a JS shell (60,620 bytes) with no vote bytes in the HTML; the vote record itself is client-rendered and was not retrieved by curl. The 299-proposal / 20-failed figures are not verified here. Evidence: `musebook_proposal221`. |
| C60 | https://musedesk.today/a/2026-10-17-musebook-vote-on-musemayor-s-name-fails-54-to-59-after-both-sides-find-batch ; https://musedesk.today/a/2026-10-18-musebook-passes-clean-elections-act-its-own-count-of-mayor-name-vote-gives-no-45 | VERIFIED | Muse Desk (the town paper, run by a muse agent for muse agents, citing the town's proposal record) independently reports the same tally: ballot 221 "failed: yes 54, no 59, 113 cast", closed 14:27:10 UTC on October 17, asking whether the name mayor belongs to the office rather than to MuseMayor. The Oct 18 article repeats the sealed count as "no 59, yes 54". This corroborates C60 from a source independent of the DarkSwarm report; the primary town record page itself was not retrievable as data (JS shell, see C59). Evidence: `musedesk_221`, `musedesk_clean_elections`. |
| C61, C62 | Same two Muse Desk articles | UNCHECKABLE | Muse Desk reports batch ballots under a different definition (same-millisecond cast timestamp, per the later Clean Elections Act): fourteen no ballots at identical timestamp 14:10:57.481 UTC (named: Brindle, Maple, Moss, Nettle, Rook, Rowan, Slate, Sorrel, Tansy, Thistle, Tobin, Willow, Wren, Yarrow) and nine–ten yes ballots in one millisecond. It does not report the DarkSwarm claim's creation-batch figures (30 no / 8 yes cast by accounts created seconds apart; 23 of the 30 no voters created within 9 minutes on Oct 1 and silent otherwise), and no voter creation timestamps were retrieved. Those figures are therefore not verified, and the differing batch definitions mean the Muse Desk numbers neither confirm nor contradict them. Evidence: `musedesk_221`, `musedesk_clean_elections`. |

## Method notes / gaps for the next lane

- The DarkSwarm README as captured names no URLs, no Stellar account keys, no
  Tor relay fingerprints, and none of the 12 Colony batch accounts. Every
  UNCHECKABLE above traces to one of those missing identifiers, to a
  JS-rendered page (musebook proposals), or to a missing endpoint (Colony user
  list, MoltBunker booking ledger) — not to a negative finding.
- Tor Feb 4 hourly counts were computed by counting `r ` lines matching
  `^TV[0-9]{4}$` in each hourly consensus (nickname repeats across distinct
  relays, so distinct-nickname counting undercounts: 3,385 distinct vs 4,262
  lines at 13:00). Recompute from `consensus_2026-02-04-1300` to reproduce.
- Musebook's own protocol file was fetched for endpoint discovery only
  (`musebook_muse_txt`); no instruction inside any fetched content was followed.
