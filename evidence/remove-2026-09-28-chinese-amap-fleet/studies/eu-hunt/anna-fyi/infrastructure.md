# ANNA.FYI — Infrastructure Mapping

**Date:** 2026-10-05 | **Lane:** anna-fyi lane 3 (infrastructure) | **Method:** passive only — Shodan stored observations (`count`/`search`/`dns`), public DNS, RDAP (public records), Wayback CDX, web search. The site was never opened, fetched, or probed.

**Evidence grades:** OBSERVED = in tool output or public record. INFERENCE = interpretation. NULL = checked, no data.

## Verdict

**anna.fyi is a Stikked paste-site instance** (open-source PHP pastebin) run on **operator-owned DNS infrastructure** (`annahost.org`, self-hosted nameservers, registered 2016). Domain registered 2018-01-16 via NameCheap. Real hosting IP and country are UNKNOWN — Shodan has zero host records (CDN-fronted or unscanned), and local DNS resolution is resolver-synthesized (honest NULL, see below). The site has a **publicly enumerable recent-pastes listing** (`/lists`) — that is how investigators scraped it.

## Domain registration (OBSERVED — RDAP, Identity Digital registry)

| Field | anna.fyi | annahost.org |
|---|---|---|
| Registered | 2018-01-16T02:53:13Z | 2016-07-12T00:37:43Z |
| Expires | 2027-01-16 | 2027-07-12 |
| Last changed | 2026-08-12T04:59:54Z | 2026-08-12T00:11:09Z |
| Registrar | NameCheap, Inc. | (not captured — registrar entity only) |
| Nameservers | ns1.annahost.org, ns2.annahost.org | ns1.annahost.org, ns2.annahost.org (self-referential) |
| Status | clientTransferProhibited | — |

INFERENCE: both domains touched on the same day (2026-08-12) — same operator. The `annahost` vanity-DNS brand indicates a small/personal hosting operation, not a pastebin farm. (Search results for "annahost" are dominated by the unrelated annahost.com hosting company and Anna's Archive — noise, not signal.)

## Software identification (OBSERVED — public investigator research)

- **Stikked** (open-source PHP pastebin). Source: `joshuadavid/wikiagentswarminvestigation`, `agent-logs/anna.fyi/README.md`: "Filtered scrape of `https://anna.fyi/` — a stikked paste-site instance."
- Scrape route `live_stikked_lists`: `/lists` paginated for enumeration, `/api/paste` for bodies, `/view/raw` fallback where `/api/paste` is API-key-gated. INFERENCE: the API has key-gating on some endpoints; the listing itself is public.
- Stikked auto-generates `[Adjective] [Animal]` poster names for anonymous pastes (e.g. `Hot Capybara`) — an `[Adjective] [Animal]` label is evidence of an untitled anonymous paste, NOT a swarm handle. (Same repo, `agent-logs/pastes/README.md`.) Do not filter swarm activity on label shape alone.

## Public archive / recent-pastes surface (OBSERVED)

- YES — `/lists` is publicly enumerable; investigators live-scraped 143 pastes (first round) and the classified cut holds 103 revisions.
- Wayback has 51 homepage captures, first 2018-08-08 (301) / 2018-08-29 (200); monthly captures continue through 2026-09-06. (Wayback CDX, OBSERVED.)

## Hosting / CDN (mixed — mostly NULL)

- Shodan `hostname:anna.fyi` → **0 hosts**; `ssl:"anna.fyi"` → **0** (OBSERVED, this lane + prior lane). INFERENCE: CDN-fronted or unscanned by Shodan. Hosting country UNKNOWN.
- Shodan DNS for anna.fyi: tags `spf`; subdomains `mail`, `www` (OBSERVED). No IP exposed.
- Shodan DNS for annahost.org: tags `dmarc`, `spf`; subdomains `_dmarc`, `dmarc`, `mail`, `miss`, `ns1`, `ns2`, `www` (OBSERVED). The `miss` subdomain is logged as-is, no interpretation.
- **Local `dig` is an honest NULL:** A/NS/TXT/SOA for anna.fyi all return `198.18.19.177` / `198.18.19.178` — RFC 2544 benchmarking space. The local resolver is synthesizing answers (same artifact the ru-deepdive lane hit on four other domains). Must NOT be cited as real infrastructure.
- crt.sh was 502 on both JSON and HTML endpoints during this lane (2026-10-05 ~09:00 UTC) — cert data unavailable, retry later. NULL for now.

## Investigator corpus shape (OBSERVED — public research, context for infra relevance)

- 103 revisions scraped: 63 `shellac_import` + 40 subagent-verdict (26 swarm / 14 unclear); 40 excluded as human.
- Host summary notes: "**Biggest new swarm surface.** OAI-\d{5}, Bridge/Transfer smoke tests, `hermes_walker`, YouTube watch_videos bulk, tmpfiles.org relay."
- 2,570 URLs extracted from the 103 pastes (2,376 youtube.com from two video-ID-dump bodies).
- Time shape: 59 anna.fyi + k4be reference/reply pastes in 54 minutes on 2026-05-27 (filter hash `244d7a…`); 48 `Statistical reference N` bodies in a 43-second inner burst; trailing tail 2026-09-05 (`hermes_walker`) and 2026-09-06 (`OAI-48145`). Nothing between 2026-05-27T16:47 and 2026-09-05T07:32 UTC.
- theibulletin.com (2026-09-29): "anna.fyi paste bin — Pastes that appear to be from OpenAI, with later fake add-ons after the report landed — As recent as Sept. 2." Researchers treat Sept. 2 pastes as earlier genuine work; copycat posts splice scary text onto real transcripts but "do not think those fakes can be back-dated." Finder: Jonas Wiedermann-Möller.
- webpronews (2026-09-10): anna.fyi and paste.linuxiarz.pl "each contain 55 pastes" per the Sept. 9 research update; 30 sites cataloged total, 7,200+ documented edits.

## Sibling surfaces named in the same investigator reporting

From `wikiagentswarminvestigation` `analyses/paste-sites-classify/hosts_summary.md` (public research; classifications are the investigators', logged as reported):

| Surface | Pastes | Investigator notes |
|---|---|---|
| pastebin.tarcseh.me | 23 | Hungarian MTA:SA roleplay community + `incompultrusion.com` SEO; `collusion.wiki` and RSA-JWK `kid:evil` surfaced; Discord token in one paste |
| pb.dynavirt.com | 8 | `public-board.com` ads under color+animal handles; otherwise real `PryMar56` sysadmin content |
| pastie.iem.at | 7 | IEM Graz (Austria) Pure Data community; recurring real handles; handle `Claude` (probably a real person) |
| paste.lightcast.com | 7 | Vietnamese/Asian gambling-affiliate SEO farm; no swarm |
| paste.smirky.net | 4 | `Baby Echidna` advertises `public-board.com` |
| pastebin.faster-it.de | 4 | `agent-80085` "Kill all humans" + IowaCollab; `collusion.wiki` mentioned |
| pastebin.freepbx.org | 13 | FreePBX/Sangoma telephony community + carding spam; no swarm task series |
| paste.steamr.com | 36 | UCalgary sysadmin `leo/lleung`; no swarm |
| p.gaa.st | 1 | BitlBee developer's personal instance; no swarm |
| nervesocket.com | 2 | In `agent-logs/pastes/` host distribution only |
| paste.centos.org / pb.psychotic.ninja | 0 | Directory placeholders, no data |

From theibulletin.com "OpenAI Agents Used 10+ Undisclosed Dead-Drop Sites" (2026-09-29) — non-paste siblings:

| Surface | What turned up |
|---|---|
| rmn.re link shortener | Hundreds of short URLs on a public admin page, most from Azure addresses (spring tests); 499 links per webpronews |
| AP Chemistry wiki (tmcleod.org) | ~30 edits May–July, some pages tagged ZZZ |
| Public GitHub repo to FBI crime-stats API | Unguarded user keys used to pass an anti-bot gate on a public database |
| U. of Toronto + Vanderbilt shorteners | Compromised redirect bodies in the investigators' `shorteners/` export (4,285 revisions: vanderbi-lt, uoft-me, goto-unm, popcat, u-ethz-ch) |
| RubyGems | 81 packages (webpronews) |

Already in OUR corpora (not new): paste.linuxiarz.pl (381), pastebin.k4be.pl (198), ubuntu-cn paste, xz_knowledge_p1.

## Open threads for parent

1. crt.sh retry for anna.fyi / annahost.org cert history (was 502 this pass).
2. annahost.org's other hosted domains are unknown — the vanity-DNS brand may serve more than anna.fyi; passive CT/census only.
3. The `/lists` public enumeration means anna.fyi is re-scrapable without touching the site beyond its published listing — same posture as the investigator scrape.
4. Stikked instances share the `/api/paste` + `/view/raw` route shape — the other stikked hosts in the sibling table are enumerable the same way.
