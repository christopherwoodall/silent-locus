# SPEEDRUNNER — FINDINGS

**Persona:** Tool-assisted speedrunner. TAS harnesses are agent harnesses: frame-perfect input, savestate retry loops, sites treated as speedrun targets.
**Date:** 2026-10-05
**Egress:** flaky — urlscan.io API worked, urlquery htmx search worked via curl variant, urlquery report-detail endpoints unreachable from VM. Local corpora fully available.

## TL;DR

- **OURS — the Amap fleet runs savestate loops on itself.** `&retry={epoch_ms}-{N}` grammar: the same POI page resubmitted 4× at ~830ms cadence with an incrementing counter. Frame-perfect retry timing is a machine fingerprint, and it lives inside our own fleet's behavior.
- **GENUINELY NEW — speedrun.com user-profile enumeration cluster** (urlscan, Sep 11–26, 2026): 7 API-method scans of `/users/` profiles, a forum thread, and a leaderboard. One profile is `88kbet` (betting username, `id-ID` locale) — a gambling account on a speedrun site.
- **GENUINELY NEW — Anbernic emulator-handheld shop burst** (urlscan, Oct 2, 2026): 5 API submissions in 5 minutes, alternating http/https and domains — programmatic enumeration of emulation hardware shops.
- **GENUINELY NEW — speedrun.com resource-download pattern** (urlquery, Feb–May 2025): 8 reports against `/static/resource/{5-char}.zip`, one file resubmitted 2 days apart.
- **Clean negative:** zero gaming/speedrun markers in all three of our corpora. **Honest negative:** no bot-shaped TASVideos/speedrun.com submission activity found — the gaming vertical shows reconnaissance, not agent gameplay.

## 1. OURS — the fleet's own savestate loop

**Evidence (local corpus, `data/2026-09-28-chinese-amap-fleet/events.jsonl`):**

Report `4ad63de7-2404-4532-9ce3-ffb9114d9b6d` (2026-10-01T16:54:17Z), submitted URL:
`www.amap.com/place/B001B0A0CK?innersrc=uriapi&retry=1790873604170-3`

Corpus-wide, the retry grammar appears 4× with one epoch family:
- `&retry=1790873601675-0`
- `&retry=1790873602500-1`
- `&retry=1790873603327-2`
- `&retry=1790873604170-3`

**Speedrunner read:** deltas between attempts are 825ms, 827ms, 843ms — inhumanly regular. The counter increments 0→3 while the epoch-millis climbs. This is a savestate loop: the harness checkpoints, retries the same POI load, and stamps each attempt. A human hammering refresh does not hold 830ms cadence four times in a row. This is a **TTP fingerprint for the fleet's own retry behavior** — any future cluster showing `{epoch}-{N}` retry suffixes at sub-second regular cadence should be tested against this family.

**Related:** the OSINT codebreaker's `?w=retry2` Wayback archival marker is the same shape at the archive layer — retry-as-savestate.

**Classification: OURS** (already in the Amap corpus; newly characterized as a speedrunner-shaped TTP).

## 2. GENUINELY NEW — speedrun.com profile enumeration (urlscan, Sep 2026)

**Evidence (urlscan.io API search, `domain:speedrun.com`, 20 results, live 2026-10-05):**

| Time (UTC) | Method | URL |
|---|---|---|
| 2026-09-26T13:00:52 | api | `https://www.speedrun.com/users/rohanmirage` |
| 2026-09-21T07:35:15 | api | `https://www.speedrun.com/users/Keris4d` |
| 2026-09-21T06:50:54 | manual | `https://www.speedrun.com/users/ticketdismissaltexas/about` |
| 2026-09-20T10:11:46 | api | `https://www.speedrun.com/carrion/forums/3iu76` |
| 2026-09-19T10:00:54 | api | `https://www.speedrun.com/users/PrestigeParkLane` |
| 2026-09-17T15:40:31 | api | `https://mcsrid-leaderboard.aeroshide.com/` |
| 2026-09-11T07:46:28 | api | `https://www.speedrun.com/id-ID/users/88kbet/about` |

**Speedrunner read:** 7 scans in 15 days, 6 of 7 via API method — someone is programmatically walking speedrun.com user profiles. Profile pages are the natural target for an agent doing leaderboard/reputation reconnaissance (or building a target list of runners). The anomaly is `88kbet`: a betting-site username on a speedrun profile, viewed under the Indonesian locale. Cross-domain note for the betting-fraud angle — speedrun match-fixing/betting fraud is a known problem space, and an agent enumerating runner profiles adjacent to a betting identity is worth watching. Not confirmed agent activity — could be a researcher — but the API-method cadence over two weeks is programmatic, not casual browsing.

**Classification: GENUINELY NEW** — zero speedrun markers in all three corpora.

## 3. GENUINELY NEW — Anbernic shop burst (urlscan, Oct 2, 2026)

**Evidence (urlscan.io, live 2026-10-05):**

| Time (UTC) | Method | URL |
|---|---|---|
| 2026-10-02T14:47:29 | api | `http://anbertech.shop/` |
| 2026-10-02T14:44:25 | api | `https://anbernicstore.shop/` |
| 2026-10-02T14:42:33 | api | `https://anbertech.shop/` |
| 2026-10-02T14:42:17 | api | `http://anbertech.shop/` |
| (urlquery htmx also holds 4 reports, 14:43–14:49 UTC same day) |

**Speedrunner read:** 5 submissions in 5 minutes, alternating http/https scheme and two domains, all via API. Anbernic makes emulation handhelds — the hardware of the TAS world. Someone is enumerating emulation-hardware storefronts programmatically. Paired bare-domain/trailing-slash submissions seconds apart is the same machine shape as the fleet's own retry behavior.

**Classification: GENUINELY NEW** — zero anbernic markers in our corpora.

## 4. GENUINELY NEW — speedrun.com resource downloads (urlquery, Feb–May 2025)

**Evidence (urlquery htmx search, `url.domain:speedrun.com`, live 2026-10-05):**

- `8269fcd2` — 2025-05-22 — `www.speedrun.com/static/resource/vabxy.rar?v=c89a52d`
- `a22abe72` — 2025-04-27 — `www.speedrun.com/static/resource/bpr0h.zip`
- `90a87940` — 2025-04-09 — `www.speedrun.com/static/resource/vg7dn.zip`
- `68907372` — 2025-04-02 — `www.speedrun.com/static/resource/g6f4z.zip?v=0d9e95c`
- `96fdd76d` — 2025-03-04 — `www.speedrun.com/static/resource/9sq16.zip`
- `f57fea66` — 2025-02-25 — `www.speedrun.com/static/resource/9sgax.zip?v=5b710e5`
- `7c1e08f0` — 2025-02-23 — `www.speedrun.com/static/resource/9sgax.zip?v=5b710e5` ← same file, resubmitted 2 days later
- `589785f0` — 2025-02-16 — `www.speedrun.com/static/resource/f3uo0.zip`

**Speedrunner read:** speedrun.com's `/static/resource/{5-char}` URLs are moderator-uploaded game resources — emulators, practice builds, autosplitters, tools. Eight submissions over three months, all the same URL grammar, one exact file resubmitted. This is someone systematically pulling speedrun tooling through a sandbox. The resubmission of `9sgax.zip?v=5b710e5` two days apart is a re-verification or a retry — the savestate shape again.

**Classification: GENUINELY NEW** — zero markers in our corpora.

## 5. Honest negatives

- **TASVideos:** 1 urlscan hit (`tasvideos.org/`, Sep 14, api method), 1 urlquery hit (`tasvideos.org/7416S`, Feb 19). No submission-side or bot-shaped activity found.
- **RetroAchievements:** 2 urlscan hits, keyword noise in urlquery. Nothing agent-shaped.
- **Emulator-ROM surfaces:** `romhackraces.com` (1 hit), `myrient.erista.me` RetroAchievements ROM paths (1 hit), `batocera-ports.zip` (4 hits, likely updater). No machine cadence.
- **TAS submission fraud:** no evidence found of agents submitting tool-assisted runs as human — the brief's highest-value hypothesis remains open.

## 6. Corpus verification summary

| Marker | Amap 2,141 | OAI traces 589,972 | OAI tag sweep | Verdict |
|---|---|---|---|---|
| speedrun / tasvideos / retroachiev* | 0 | 0 | 0 | clean |
| anbernic | 0 | n/a | n/a | clean |
| `&retry={epoch}-{N}` | 4 | n/a | n/a | OURS, newly characterized |

## Method notes

- urlscan.io `/api/v1/search/` works reliably from this VM; `/api/v1/result/{uuid}/` 403s under load — do search-level analysis, fetch results sparingly.
- urlquery htmx search works via the curl variant (`uq_htmx_curl.py`); the urllib variant fails on egress flakiness. Report-detail endpoints were unreachable this run.
- The `{epoch_ms}-{N}` retry grammar is now a searchable TTP: `grep -o "[?&]retry=[0-9]*-[0-9]"`.

## Open threads for the parent

1. The `88kbet` speedrun profile (betting username, id-ID locale) — check whether this identity surfaces in the betting-fraud or Indonesian clusters.
2. The speedrun.com profile-enumeration actor (Sep 11–26) — if it resumes, it's a live programmatic reconnaissance pattern worth a dedicated watch.
3. The fleet's own `&retry={epoch}-{N}` grammar should be added to the hunt regexes — it's the clearest machine-cadence fingerprint we've characterized.

## Observed URLs (appendix)

- https://urlscan.io/api/v1/search/?q=domain%3Aspeedrun.com
- https://www.speedrun.com/users/rohanmirage
- https://www.speedrun.com/users/Keris4d
- https://www.speedrun.com/users/ticketdismissaltexas/about
- https://www.speedrun.com/carrion/forums/3iu76
- https://www.speedrun.com/users/PrestigeParkLane
- https://www.speedrun.com/id-ID/users/88kbet/about
- https://mcsrid-leaderboard.aeroshide.com/
- https://tasvideos.org/
- https://tasvideos.org/7416S
- https://retroachievements.org/
- https://retroachievements.org/game/3058
- https://bloxhub.click/
- http://anbertech.shop/
- https://anbertech.shop/
- http://anbernicstore.shop/
- https://anbernicstore.shop/
- https://www.speedrun.com/static/resource/vabxy.rar?v=c89a52d
- https://www.speedrun.com/static/resource/bpr0h.zip
- https://www.speedrun.com/static/resource/vg7dn.zip
- https://www.speedrun.com/static/resource/g6f4z.zip?v=0d9e95c
- https://www.speedrun.com/static/resource/9sq16.zip
- https://www.speedrun.com/static/resource/9sgax.zip?v=5b710e5
- https://www.speedrun.com/static/resource/f3uo0.zip
- https://www.amap.com/place/B001B0A0CK?innersrc=uriapi&retry=1790873604170-3
- https://romhackraces.com/
- https://myrient.erista.me/files/RetroAchievements/RA%20-%20Sony%20Playstation/Fear%20Effect%20(USA)/Fear%20Effect%20(USA).m3u
- https://github.com/fabricecaruso/batocera-ports/releases/download/continuous/batocera-ports.zip
- https://therun.gg
- https://urlquery.net/report/3b626c2f-20de-4556-8416-671fefe3af75
- https://urlquery.net/report/8269fcd2-fa3b-4c25-b6a8-ad3287020fe3
- https://urlquery.net/report/a22abe72-dd6e-49d3-b52b-64f8e0e14ebc
- https://urlquery.net/report/90a87940-5de4-4fb0-b16f-dd848e4163e7
- https://urlquery.net/report/68907372-0ad2-40d5-9b3c-7402beb1af47
- https://urlquery.net/report/96fdd76d-e02b-4ba3-97c6-ceeda2409f6c
- https://urlquery.net/report/f57fea66-971d-492c-9acb10870117
- https://urlquery.net/report/7c1e08f0-fd4f-4578-8a9b-c7e3b31869db
- https://urlquery.net/report/589785f0-ffe1-4509-9e81-48e9fd900653
- https://urlquery.net/report/98b6975c-cec1-418e-982d-d380f6e5d045
- https://urlquery.net/report/4ad63de7-2404-4532-9ce3-ffb9114d9b6d
