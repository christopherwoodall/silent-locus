# HUNT LANE 15b — abuse.ch historical reach (campaign-date windows)

**Date:** 2026-09-27/28 · **Status:** COMPLETE — CLEAN NEGATIVE
**Task:** Lane 15 proved the abuse.ch API needs an Auth-Key (401), and its keyless bulk feeds only cover the last 30 days — blind to the May–July 2026 campaign. Reach further back without creating accounts.
**Campaign windows:** May 5, 8, 9, 10, 11, 12, 26, 27 · June 18 · July 7, 2026.
**Constraints honored:** read-only, paced, no accounts, no logins. No API keys used, requested, or created.

## Verdict

**Nobody submitted the campaign's IOCs to URLhaus, ThreatFox, or MalwareBazaar** — not during the campaign windows, and not in the surrounding April–August 2026 period either. A pattern-based sweep (per Christopher's standing guidance: hunt the grammar, not just exact IOCs) of **456 daily digest events / 226,036 attributes** across all three abuse.ch MISP feeds found **zero campaign-specific markers**. The 551 raw pattern hits were all adjudicated as generic malware-ecosystem noise (see below).

## Route 1 — URLhaus web UI: BLOCKED

`https://urlhaus.abuse.ch/browse/` renders only a **"Checking your browser" JS challenge** — text-fetching cannot pass it, and the search UI behind it is unreachable without a live browser. No keyless URLhaus web-UI querying was possible. (Flag for parent: a browser-task delegation could try the UI search for our domains.)

## Route 2 — third-party archives of abuse.ch dumps

- **`jaguarmayan8/twitteriocsfeed`** (GitHub) — automated daily collector, outputs organized by year/month. Has `Output/2026/2026-07` with daily `urlhaus.csv` (~4 MB) and `threatfox_recent.json` (~2.7 MB) snapshots. Downloaded all 10 days **Jul 22–31, 2026** (68 MB) and grepped for all campaign markers → **zero hits**. Coverage starts Jul 22, so it cannot speak to the May / Jun 18 / Jul 7 windows (those IOCs would have expired from the 30-day "recent" exports before Jul 22). Useful only as a negative for late-July.
- **`erichschmidt/smb-ai-threat-feed`** — daily briefs archive, but only covers **Aug 19 – Sep 27, 2026**. Post-campaign, not useful.
- No Kaggle/HF dataset with May–July 2026 URLhaus/ThreatFox dumps was found via search.

## Route 3 — Wayback CDX: BLOCKED (unchanged)

Still **"Internet Archive: Temporarily Offline"** — confirmed via an `example.com` sanity query (the Archive itself is down, not a lack of captures). Same as the standing park. No CDX recovery of `urlhaus.abuse.ch/url/*` or `threatfox.abuse.ch/*` keys was possible.

## Route 4 — keyless full-history downloads: CONFIRMED, and it's the good route

All three abuse.ch **MISP feeds are keyless AND cumulative back to 2021** — this is the historical reach lane 15 needed:

| Feed | Keyless manifest | Events | Span |
|---|---|---|---|
| ThreatFox | `https://threatfox.abuse.ch/downloads/misp/manifest.json` | 2,002 | 2021-03-13 → 2026-09-28 |
| URLhaus | `https://urlhaus.abuse.ch/downloads/misp/manifest.json` | 1,957 | 2021-03-12 → 2026-09-27 |
| MalwareBazaar | `https://bazaar.abuse.ch/downloads/misp/manifest.json` | 1,918 | 2021-03-13 → 2026-09-08 |

Each event is a **daily digest** ("ThreatFox IOCs for 2026-05-11", ~30 events/month) with typed attributes (`url`, `domain`, `ip-dst|port`, `sha256`, `md5`, …). Also confirmed keyless: `https://urlhaus.abuse.ch/downloads/text_online/` and `https://threatfox.abuse.ch/export/csv/recent/` (both HTTP 200, no key). The authenticated v2 API exports (`urlhaus-api.abuse.ch/v2/files/exports/{KEY}/…`) remain key-only.

**Fetch notes:** abuse.ch's servers truncate large transfers intermittently (first pass: 455/458 failed via urllib). `curl` with retries recovers them; one persistent obstacle was `/tmp` being a 512 MB tmpfs that filled up — working data moved to `~/workspace/tmp-lane15b/`.

## The historical sweep

**Coverage:** 456 of 458 daily digest events dated 2026-04-01 → 2026-08-31, all three feeds (ThreatFox 152, URLhaus 150, MalwareBazaar 154). Every campaign-window day ±1 day margin was fetched and verified valid in all three feeds, **except ThreatFox 2026-05-26, for which the feed publishes no digest at all** (May 25 and May 27 digests exist and bracket it — a feed gap, not a fetch failure). The only other missing events are the ThreatFox and URLhaus digests for 2026-08-31 (server-side truncation, outside all windows).

**Method:** per Christopher's guidance, literal IOCs + pattern queries over every attribute value (226,036 attributes total):
- Literals: all 13 campaign domains, IP 20.49.140.101, r.jina.ai/s.jina.ai, 6 gem SHA-256s (regenerated from the raw corpus after the restart wiped lane 15's `/tmp` files) + 7 third-party-published gem hashes (Hive Pro advisory), `southwark/lambeth/wandsworth`, `gemstuffer`, `oast.online`, `webhook.site`, `county.json`, `rubygems`, `go-import`, `tryf3zz`, `southpxdatapp6pi`, `zzjina`, beacon phrases ("builder alive", "YARD RAN", "HOOKED!!!!!!", "malicious crawler", "yard exploit"), `yardopts`, `yardload.rb`.
- Patterns: `try[a-z][0-9]zz`, `zz`-at-label-boundary grammar, `r.jina.ai`/`s.jina.ai` URL shapes, `/api/v1/web_hooks`, `A000`/`ZZEND`, `mgCalendarMonthView`/`mgWebService`, epoch-second (`17\d{8}`) and epoch-ms (`17\d{11}`) runs restricted to URL/domain/filename attributes.

**Result:** 551 raw hits out of 226,036 attributes — **every one adjudicated as noise:**
- `ZZ-GRAMMAR` (428): `.buzz` TLD domains (zz is the TLD), Mirai `luxzzxzzx` botnet paths, phishing domains (`fclmwfzz.colonist-proph.lat`, `kakazz.myftp.org`) — generic malware naming, none matching the campaign's `try[a-z][0-9]zz` / `zzjina` / epoch-suffixed grammar. The `try[a-z][0-9]zz` pattern itself had **zero hits** across the entire corpus.
- `EPOCH-S` (79) / `EPOCH-MS` (32): Bebra-stealer version params, Cloudinary asset version numbers, file-ID path components, Cloudflare challenge tokens — not epoch timestamps in campaign-shaped URLs.
- `PAT:A000` (11): the hex substring "a000" inside SHA-1/SHA-256 hashes — pure hex noise, no `/api/v1/web_hooks` context, no ZZEND anywhere.
- **One `webhook.site` URL** in the ThreatFox 2026-05-06 digest (`https://webhook.site/1d98b695-…`) — adjudicated: tagged "Unknown malware botnet C2 (confidence 49%)" by reporter `teampcp`; webhook.site is a public request-bin used by thousands of actors; no `/api/v1/web_hooks` path, no A000/ZZEND markers, no campaign context. Coincidental noise.
- **Zero hits** for: r.jina.ai/s.jina.ai, all council domains, go-import tags, the webhook dead-drop markers, all beacon phrases, all gem hashes, `oast.online`, `gemstuffer`, the Fastly/cache-bug IOCs, IP 20.49.140.101.

## Gaps (honest)

1. **ThreatFox 2026-05-26** digest doesn't exist in the feed (May 26 wave day; bracketed by May 25/27 digests).
2. **ThreatFox + URLhaus 2026-08-31 digests** unrecoverable after repeated retries (server-side truncation; outside all campaign windows).
3. MISP feeds are abuse.ch's *published* record — if IOCs were submitted but never published to the feeds, they wouldn't appear here. The feeds are the best public record available without an account.
4. URLhaus web UI search remains untried (needs a live browser past the JS challenge).

## Bottom line

The abuse.ch corpus — the highest-probability "someone else already logged it" source — has **no record of the GemStuffer campaign's infrastructure, payloads, or grammar in the campaign windows**, across URLhaus, ThreatFox, and MalwareBazaar, by exact IOC and by pattern. Combined with the clean negatives from urlscan, VirusTotal-shaped sources (pending), gists, pastebins, and HuggingFace, the campaign's observable third-party footprint keeps shrinking toward RubyGems + Diffend + JFrog only.

**Unblock path (unchanged from lane 15):** a free abuse.ch account would open the v2 API (full history, exact IOC search) and ThreatFox's "gemstuffer" tag search.

**Working data:** `~/workspace/tmp-lane15b/` — manifests, 190+ daily MISP events, `markers.txt`, `patterns.txt`, `final_grep.py`, `hits.json`, July snapshot archive (`july/`).
