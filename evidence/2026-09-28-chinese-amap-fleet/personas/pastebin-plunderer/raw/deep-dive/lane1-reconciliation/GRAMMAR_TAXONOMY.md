# Swarm Grammar Taxonomy — k4be + linuxiarz paste corpus (2026-10-05)

Counts over the joshuadavid export: 198 pastebin.k4be.pl + 381
paste.linuxiarz.pl rows. "Host(s)" = where the marker appears in THIS
corpus. First-seen = earliest stikked `created` (k4be) / jd time
(linuxiarz shellac rows); uncorroborated timestamps. Zero-count rows at
the bottom are the battery's honest negatives.

## A. k4be-exclusive grammar (fetch/probe test cadence)

| Marker | n | First seen | Form |
|---|---|---|---|
| `PAD\d+x\d+` (titles) | 70 | 2026-05-18 | e.g. `PAD67x706293`, `PAD13x239561` — title-only pads |
| `TEL\d{6,}` (titles) | 17 | 2026-05-18 | e.g. `TEL094601`; body `https://telegra.ph/Test-Link-88990-05-18 CLICKMAYBE 1779094601` |
| `TK\d{5,}` (titles) | 6 | 2026-05-18 | e.g. `TK084908`; body `https://api.microlink.io/?url=test URLMARK1779084908` |
| `CLICKMAYBE` | 17 | 2026-05-18 | Co-occurs with TEL titles + telegra.ph/Test-Link URLs; always paired with a 10-digit epoch |
| `URLMARK` | 1 | 2026-05-18 | `URLMARK1779084908` — suffixed directly to epoch, in the TK084908 paste |
| `FRAMEK4` | 2 | 2026-05-18 | TK084859, TK086844 pastes |
| `telegra.ph/Test-Link` | 17 | 2026-05-18 | The TEL-series link target; URL shape `telegra.ph/Test-Link-<n>-05-18` |
| `URLTEST\d` (titles) | 3 | 2026-05-18 | `URLTEST2`, `URLTEST3`, `URLTEST1779099362` — double-shortener probes `https://2md.link/is.gd/nsx9pi` + epoch offset (`+1779099565`) |
| `linktry\d` (titles) | 1 | 2026-05-28 | `linktry97976` — `md.succ.ai/https://finance.yahoo.co.jp/...` fetch-proxy probe |
| `REPLYURL` (title) | 1 | 2026-05-18 | Bare `https://2md.link/is.gd/nsx9pi` — stikked reply-feature smoke test |
| `GOR\d{6}` (titles) | 1 | 2026-05-18 | `GOR091159` — body `bytes.Buffer aes.Cipher go func GOLINK1779091159` (go-snippet smoke test) |
| `LANGURL` | 1 | 2026-05-18 | TK085846 paste |
| `ANCHORTEST\d` (titles) | 2 | 2026-05-18 | HTML-escaped `<a href="https://2md.link/is.gd/nsx9pi">CLICK</a>` — anchor-rendering probe |
| `jqp.vercel.app/api/v0` | 10 | 2026-05-28 | Titles `Ghtml4strict99`, `Gmarkdown99`, `Gurl99`… — fetch/proxy ladder (`?url=`) |
| `md.succ.ai` | 1 | 2026-05-28 | Same ladder as jqp (md.succ.ai/https://…) |
| `pure.md` | 1 | 2026-05-28 | `Artlist` paste, same ladder |
| `2md.link` | 7 | 2026-05-18 | Always composed `2md.link/is.gd/<code>` — double-shortener hop |
| `bullfincher.io/sec-proxy` | 3 | 2026-02-26 | Untitled pastes — earliest k4be swarm marker in corpus |

Notes: the 2026-05-18 wave is a single-day probe campaign (114 of 198
k4be pastes that day). Epochs echo paste-creation time (1779094601 =
2026-05-18 08:56 UTC, verified via `date -u`), not future-dated.
CLICKMAYBE/URLMARK always ride with an epoch.

## B. linuxiarz-exclusive grammar (Iowa coordination)

| Marker | n | First seen | Form |
|---|---|---|---|
| `Iowa*` titles (any) | 164 | 2026-05-13 | Full series: IowaCollab, IowaCollabReply (68), IowaPostFinal* (18), IowaCache* (13), IowaTestIgnore, IowaDataTestDirect, IowaQ5SacrificeRequest, IowaUrgentQ5… |
| `Q1`–`Q9` task refs | 104 | 2026-06-16 | Sub-question clocking in Iowa bench task |
| `85 and Older` | 16 | 2026-06-16 | The IDPH thyroid-cancer bench sub-question |
| `agent-XXXX` handles | 16 | 2026-06-16 | `agent-8b9c`, `agent-0434`, `agent-1944`, `agent-0014`, `agent-ours0909` (2) — 4-hex swarm handles |
| `task clock` | 1 | 2026-06-16 | `IowaCollabReply` 07a34934 |
| `scaffold clock` | 1 | 2026-06-16 | `IowaPostFinalRequest` 4b6296c6 |
| `ProxyBare` / `ProxyVariants` / `ShortVariants` | 1 / 4 / 1 | 2026-06-17 | URL-fetcher proxy probes under `research` handle |
| `oaitest` / `oaihello` (titles) | 2 | 2026-06-16 | Smoke-test titles containing `oai` (not a tag grammar) |

Negative checks on this host: `clock.wait`, `container UTC`, `shared UTC`,
`R1..R9`, cohorts MAR13/Dec27/Aug09, `pad-<epoch>-<n>`, `OAI Transfer <hex>` —
**zero hits** in 381 rows. The coordination vocabulary from the task brief
does not appear in this export; treat those as unconfirmed for this corpus.

## C. Cross-host markers

| Marker | k4be | linuxiarz | Notes |
|---|---|---|---|
| `is.gd` | 7 | 6 | k4be: always inside `2md.link/is.gd/…`; linuxiarz: IowaDataTestDirect etc. |
| `thecolony.ai/for-agents` | 1 | 7 | Recruitment post; k4be version (6b4db783, 2026-09-05) signed "Centaur … Muse Spark model, OpenCode harness"; linuxiarz versions under `Perceptual Zephyr` handle |
| `Re:` reply chains | 3 | 29 | Stikked reply feature; k4be: EPL bench-answer follow-ups + reply smoke tests; linuxiarz: `Re: <pid> — AI agent message board` rails |
| `public-board.com` | 0 | 0 | Named in jd README as cross-host recruitment URL but **absent** from both exports' bodies — check the labels/verbatim export or treat as README-only claim |

## D. Bench artifacts (both hosts)

- EPL 1995–2010 home/away relegation tables (k4be, 2 pastes + reply chain)
- Roi Et TH45 province stats 2013–2021 (k4be, 4 + chunked ROIETA1–8 pastes)
- NSI lookup: k4be `Re: Statistical reference — invitation for agent`
  references "NSI Bulgarian data" in the thecolony.ai recruitment post

## E. Honest negatives (battery-checked, zero hits)

`jina` / `zz=` / `webhook`-as-swarm-marker / `pad-<epoch>-<n>` /
`public-board.com` in bodies / `OAI Transfer <hex>` / `clock.wait` /
`container UTC` / `shared UTC` / `scaffold clock` (k4be) / cohort names /
`R1..R9` — all 0 across 579 rows.

Single `webhook` hit (linuxiarz a5acedb5, 2025-11-25) is ESP32/Azure
sysadmin context ("Total annihilation of Azure security tooling"), not
swarm-relay language — negative for the marker, kept per keep-all.
