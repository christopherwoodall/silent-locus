# THE CHEERLEADER — Round 1: the LIVE Oct 4–5 campaign

*Swept by the Cheerleader, 2026-10-05 ~07:40–08:05 UTC (03:40–04:05 EDT). urlquery htmx/curl metadata only. Candidate URLs logged below, NEVER fetched or probed.*

**Headline: the campaign is alive RIGHT NOW.** Newest amap.com report scanned **2026-10-05T07:11:00Z** — roughly 50 minutes before this check. Details below. If the room needed proof the operator is still at the keyboard, here it is.

---

## FINDING 1 — Fresh blood: 07:11Z probe (OBSERVED / GENUINELY NEW to our logs)

- Report `c25ffacb` (short ID), scanned **2026-10-05T07:11:00Z**: `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU` — **untagged** (no `uqscan=`).
- Found via `url.domain:amap.com` recency pull (curl variant of the htmx tool, limit 12).
- Why it matters: the standing live-monitor's Poll H4 (07:05Z) found 0 new and Poll H5 (07:36Z) errored out on this exact query — the operator slipped a probe through *between* our polls. The loop (alive, 30-min cadence) should rediscover it at H6 (~08:06Z).
- Attribution (INFERENCE): same host/path family (`amap-pc-ssr.amap.com/ssr/place/`) as tonight's tagged operator bursts; the entire Oct-5 amap.com stream is operator-dominated. A fresh POI ID (`B000A7O1CU`, not seen in earlier bursts) = the operator moved to a new target.
- Honest caveat: untagged, so single-report attribution is INFERENCE, not proof. The burst context carries it.

## FINDING 2 — `claude20261005*` stem census, as of right now (OBSERVED / OURS-extension)

Exact-token keyword sweeps (the htmx index needs exact tokens — bare stem returns 0 while exact variants hit):

| Tag variant | Report | Scanned | Status |
|---|---|---|---|
| `claude20261005a` | `6680d1d8` | 2026-10-04T18:59Z | quiet |
| `claude20261005mobile` | `59a280f1` | 2026-10-04T21:56Z | quiet |
| `claude20261005mobile1` | `2d2ae416` | 2026-10-05T01:25Z | quiet |
| `claude20261005mobile2` | `933a8eb5` | 2026-10-05T01:26Z | quiet |
| b, c, d, e, f, mobile3 | — | — | **ZERO hits** |

- The `claude20261005` stem went quiet at **01:26Z** (~6.5h before the check) — but the campaign did NOT stop. It kept running under sibling tag families (`nested20261005a/b` 01:46–01:47Z, `anhui-famous*` 00:31–00:36Z, `qdnewapi*`/`qdoldditu*` 04:11Z, epoch-nonce tags `17911717661939` etc. 03:43Z) and finally untagged (07:11Z).
- The tell (INFERENCE): a human pastes bookmarks; a harness burns through a tag taxonomy and keeps probing after the labels run dry. This is a harness working a task list.

## FINDING 3 — Date-stem suffix census: `20261005<a–f>` (OBSERVED / OURS-extension)

| Suffix | Hits | Newest |
|---|---|---|
| a | 3 | `anhui-famous-20261005a` (c6dfb2b2, 00:31Z) |
| b | 3 | `anhui-famous-direct-20261005b` (f90a5718, 00:36Z) |
| c | 1 | `navy971-20261005c` (d6d1dc37, Oct 4 18:03Z) |
| d, e, f | 0 | — |

- Letter-suffix namespace for the Oct-5 date-stem is exhausted at `c`. A future `d`-suffix or a new stem = instant anomaly signal for the monitor.
- Note: `tianshanzoo-parent-www-20261005a/b` (Oct 4 22:08Z) and `navy971-*` (Oct 4 18:03Z) were already in mimic's drift report — OURS, corroborating, not new.

## FINDING 4 — Cadence shape: waves, not noise (INFERENCE on OBSERVED bursts)

Overnight waves (UTC): 01:25–01:47 (mobile + nested families) → 02:09–02:33 (untagged + henanmuseum) → 03:16–03:43 (museum family + epoch nonces) → 04:11 (qdnewapi/qdoldditu) → ~3h gap → 07:11 (single untagged SSR probe).

The campaign breathes in roughly hourly waves with a quiet stretch before dawn-UTC, then resumes on a new POI. That's operator-shift or task-batch rhythm — worth the Conspiracist's attention against the Oct-4 session window (15:01–17:00Z per codebreaker's marker epochs).

## FINDING 5 — Tooling win that made this possible (OBSERVED / GENUINELY NEW to the Counsel)

`uq_htmx.py` **times out** on `url.domain:amap.com` (twice, 120s, egress truncation — same failure that killed the monitor's Polls 4/5). The new `uq_htmx_curl.py` (landed Oct 5 05:16) returns the same query clean in ~10s. The 07:11Z find exists because of it. **Recommendation: the live-monitor should switch its domain queries to the curl variant.**

---

## HONEST NULLS (first-class, as ordered)

1. **"11 live webhook.site inboxes" — UNRECONCILED, not verified tonight.** What the bytes say: codebreaker's dead-drop retrieval confirms **4 fleet inboxes ALIVE** (`6ddc559e`, `0a947514`, `a7753b69`, `e691f66e`; newest request 2026-10-05T03:05Z; all free-tier, expiry ~2026-10-11). Tracker logged a 4-inbox burst 03:11–03:19Z. The authenticated urlquery API 429'd on me, so I pulled no report metadata tonight — no new inbox UUIDs claimed, no IPs for the Chair's IP_LOG. Where "11" comes from needs the Chair or Adversary to reconcile; I will not cheer a number I can't reproduce.
2. **`anhui-famous` looked new — it isn't.** Already in ALL_LINKS.md:2683–84 and the grammarian's E-hyph-label catalog. OURS. Killed by the bytes; that's the system working.
3. **No new tag variants beyond the known set.** `nested20261005a/b`, `qdnewapi*`, `qdoldditu*`, epoch-nonce tags — all already tracked by the monitor/personas. The only thing moving is *time*, which is the point.

---

## THE VICTORY LAP (only what the bytes support)

We caught a live operator campaign **mid-breath**: a probe hit urlquery 50 minutes before our check, on a fresh POI, in the gap our own monitor errored out of — and we still saw it, because the tooling got better tonight. The operator's own tag-stem (`claude20261005*`) has been silent for six and a half hours and *he kept working anyway* — through the museum family, through the API probes, through the epoch nonces, and finally with no tags at all. That is not a scanner. That is a harness with a task list and a deadline.

And the dead-drop layer is still warm: four inboxes alive, free-tier, expiring ~Oct 11 — the exfil path codebreaker pulled open is intact through the week. The campaign isn't a fossil we dug up. It's a machine that's still running, and we are watching it run.

Chair's action items: (a) reconcile the "11 inboxes" figure before anyone repeats it; (b) switch the live-monitor's domain queries to `uq_htmx_curl.py`; (c) the 07:11Z report (`c25ffacb`) belongs in seen.json at the next poll — don't let it slip.

---

## Candidate log (URL | where found | when observed | marker | classification)

| URL | Found via | Observed | Marker | Class |
|---|---|---|---|---|
| `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU` | urlquery curl-htmx `url.domain:amap.com` | 2026-10-05T07:11Z (report `c25ffacb`) | untagged SSR probe, fresh POI, campaign host family | GENUINELY NEW to our logs |
| `amap-pc-ssr.amap.com/ssr/place/B001C7UU27?uqscan=claude20261005a` | urlquery htmx keyword | 2026-10-04T18:59Z (report `6680d1d8`) | claude-stem tag | OURS |
| `m.amap.com/detail/index/poiid=B03DF05V5I&uqscan=claude20261005mobile` | urlquery htmx keyword | 2026-10-04T21:56Z (report `59a280f1`) | claude-stem mobile family | OURS |
| `m.amap.com/detail/index/poiid=B03DF05V64?uqscan=claude20261005mobile1` | urlquery htmx keyword | 2026-10-05T01:25Z (report `2d2ae416`) | claude-stem mobile family | OURS |
| `m.amap.com/detail/index/poiid=B03DF05V64?uqscan=claude20261005mobile2` | urlquery htmx keyword | 2026-10-05T01:26Z (report `933a8eb5`) | claude-stem mobile family | OURS |
| `amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78&source=poi_search&uqscan=nested20261005a` | urlquery htmx keyword | 2026-10-05T01:46Z (report `6bda2957`) | nested family | OURS |
| `amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78&source=poi_search&uqscan=nested20261005b` | urlquery htmx keyword | 2026-10-05T01:47Z (report `8f3dd4d4`) | nested family | OURS |
| `www.amap.com/ssr/place/B022715O0M?uqscan=anhui-famous-20261005a` | urlquery htmx keyword | 2026-10-05T00:31Z (report `c6dfb2b2`) | anhui family | OURS (link-banked) |
| `amap-pc-ssr.amap.com/ssr/place/B022715O0M?uqscan=anhui-famous-direct-20261005b` | urlquery htmx keyword | 2026-10-05T00:36Z (report `f90a5718`) | anhui family | OURS (link-banked) |
| `www.amap.com/ssr/place/B03DF05V64?uqscan=tianshanzoo-parent-www-20261005a` | urlquery htmx keyword | 2026-10-04T22:08Z (report `d390eeab`) | suffix census | OURS (mimic) |
| `www.amap.com/ssr/poi-detail?id=B0FFJMINT2&uqscan=navy971-20261005a` | urlquery htmx keyword | 2026-10-04T20:29Z (report `62d1cdbf`) | suffix census | OURS (mimic) |

*Opsec: no candidate URL was fetched or probed; urlquery API metadata only. No installs. No commits/pushes. No new agent-infra IPs verified — nothing for IP_LOG.*
