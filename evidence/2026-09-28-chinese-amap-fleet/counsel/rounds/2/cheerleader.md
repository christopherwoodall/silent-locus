# THE CHEERLEADER — Round 2: the LIVE campaign, receipts audited

*Swept by the Cheerleader, 2026-10-05 ~08:20–08:35 UTC. Independent verification of the Round-1 live headlines via the urlquery htmx curl endpoint (`uq_htmx_curl.py`) + corpus greps. Candidate URLs logged below, NEVER fetched or probed. Round-1's 14 kills treated as settled; nothing here re-litigates them.*

**The verdict up front:** the campaign is live — the 07:11Z probe is real and I re-verified it independently. BUT the "new POI, zero corpus overlap" headline is a CORPSE and I am not cheering it. `B000A7O1CU` is the corpus's SEED POI — the Summer Palace, first-session target from 2026-09-28 20:57Z. The operator didn't move to a new target. He came HOME.

---

## FINDING 1 — The 07:11Z probe is real; the "new POI" claim is DEAD (OBSERVED / OURS, corrected)

**Claim under test:** "fresh 2026-10-05 07:11 UTC untagged probe on a new POI with zero corpus overlap" (FINDINGS.md #4, Round-1 cheerleader Finding 1).

**The receipt (OBSERVED, my own pull 08:2x UTC):** report `c25ffacb` exists exactly as claimed — `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, scanned `2026-10-05T07:11:00Z`, untagged. It remains the newest amap.com report as of my check (~75 min old). The existence/timestamp claim HOLDS.

**The wound:** "new POI" / "zero corpus overlap" does NOT hold. Corpus grep turns up `B000A7O1CU` across the corpus — and not as a bit player:
- `raw/analysis/LINKS.md:8` — "first Amap scan (28 Sep 20:57 UTC, **Summer Palace `B000A7O1CU`**)" — this POI is the investigation's **seed**.
- `full-sweep/raw/corpus-remine.md:65` — "**23×: 2026-09-28 20:57–21:32** — the corpus's earliest records, all untagged `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, MAIN UA. Reads as the operator's first session."
- `events.jsonl`: **51 events** on this POI. `ALL_LINKS.md`: 707+ entries. Profiler: 20 hits 09-28 ("node smoke test"), 1 on 09-30, 4 on 10-04.

**The reframe (INFERENCE, graded):** the 07:11Z probe REPRODUCES the Sep-28 first-session signature — same POI (B000A7O1CU), same host (`amap-pc-ssr.amap.com`), same path template (`/ssr/place/`), untagged — after a ~3h quiet stretch and 10 days after the first session. This is a RETURN-TO-ORIGIN, not a new-target expansion. A harness returning to its original canary POI after working the whole task taxonomy smells like a completion check or baseline re-run — worth the Conspiracist's attention against the Oct-4 session-window framing.

**Classification:** observation GENUINELY NEW (the return was never noted); the POI itself OURS since Sep 28. Evidence OBSERVED (fresh urlquery pull + corpus files).
**Actionability:** HIGH — the monitor's seen.json STILL lacks `c25ffacb` (verified 08:22Z); seed it on restart or the loop misses it forever.

## FINDING 2 — `uqm`/`uqattempt` grammars re-verified (OBSERVED / OURS — settled kill #14 corroborated)

**Claim under test:** "`uqm=1/2/3` and `uqattempt=0/1` at 02:13–02:30Z" falsifying "labels ran dry" (Round-1 kill #14).

Fresh exact-token keyword pulls return all five reports at the stated timestamps:
- `m.amap.com/detail/index/poiid=B03DF05V64?uqm=1`, `/detail/index?poiid=B03DF05V64&uqm=2`, `/detail/B03DF05V64?uqm=3` — all `2026-10-05T02:30:00Z` (three different mobile path templates, same POI — a UI-variant sweep).
- `www.amap.com/place/B03DF05V64?uqattempt=0` and `?uqattempt=1` — both `2026-10-05T02:13:00Z`.

No re-litigation needed: the kill stands, the bytes confirm. Bonus texture: the `uqm` trio hits three different `m.amap.com` URL shapes in the same minute — the harness probing URL-variant coverage, not just pages.

**Classification:** OURS. Evidence OBSERVED. Actionability: MEDIUM — watch for `uqm=4` or `uqattempt=2` as the next grammar step.

## FINDING 3 — The four fresh probe families verify at exact tokens (OBSERVED / OURS)

**Claim under test:** "fresh probe families: `claude20261005mobile{N}`, `nested20261005a/b`, `qdnewapi20261005a/b`, `qdoldditu20261005a`."

All verify via exact-token search (bare stems return 0 — see methodological note below):
- `claude20261005mobile1` / `mobile2`: `2026-10-05T01:25:00Z` / `01:26:00Z`, `m.amap.com/detail/index/poiid=B03DF05V64`.
- `nested20261005a`: `2026-10-05T01:46:00Z` (note: `%26`-encoded nested params in URL — `id=B01FE16U78%26source=poi_search%26uqscan=…`, matches LOG.md); `nested20261005b`: `01:47:00Z` (clean params).
- `qdnewapi20261005a` / `b` + `qdoldditu20261005a`: all three `2026-10-05T04:11:00Z`, POI `B021406HP0`, re-verified in my own recency pull.

**Methodological note (for the whole Counsel):** the htmx index requires EXACT tokens. A bare-stem query (`nested20261005`, `claude20261005mobile`) returns ZERO even when exact variants hit. A zero on a bare stem is a search-syntax artifact, NOT absence. All future keyword claims must use exact tokens — this almost cost me a false negative on `nested*`.

**Classification:** OURS. Evidence OBSERVED. Actionability: MEDIUM — the `mobile3`/`nested20261005c`/`qdoldditu20261005b` gaps remain the monitor's tripwires.

## FINDING 4 — `qd` = Qingdao, strengthened (INFERENCE on OBSERVED co-occurrence)

FINDINGS.md floated "`qd` prefix suggests Qingdao-dialect operator shorthand" — an INFERENCE on a 2-letter prefix, properly graded. New support: POI `B021406HP0` carries `qingdaomuseum20261005b` at 03:16Z and `qdnewapi20261005a/b` + `qdoldditu20261005a` at 04:11Z — the SAME POI tagged explicitly `qingdao*` one wave earlier. The `qd`↔`qingdao` link is now same-POI co-occurrence across consecutive waves, not just prefix-guessing. Still INFERENCE (an operator could abbreviate anything), but a much better-founded one.

**Classification:** INFERENCE (OURS-adjacent). Evidence OBSERVED co-occurrence. Actionability: LOW-MEDIUM — expect `qd`-prefixed tags to track Qingdao-venue tasking.

## FINDING 5 — FLAG: the live monitor is DOWN, and the 07:11Z probe is still outside its world

**Receipts:**
- No monitor process alive at 08:22Z (`ps` clean). H6 (~08:06Z) never ran. Last journal line: poll 5, 07:36Z (with the amap.com query error).
- `seen.json` (96 entries) does NOT contain `c25ffacb` — verified directly.
- All state files share mtime 07:38:20 — the H5 poll's final writes, not another restore (content matches the journal; no older-state reversion this time).
- Round-1's recommendation (switch domain queries to `uq_htmx_curl.py`) is still un-applied — the monitor loop still shells to `uq_htmx.py`, which is the variant that 429'd/timeout'd and killed Polls 4/5.

**Classification:** OURS infrastructure fact. Evidence OBSERVED.
**Actionability:** URGENT — (a) restart the loop; (b) seed `seen.json` with `c25ffacb` + the exact-token set from Findings 2–3; (c) swap the query path to `uq_htmx_curl.py` before the next 429 wave. Every minute the loop is dark, a burst like 07:11Z passes unlogged.

## FINDING 6 — Cadence discipline, one more time (INFERENCE on OBSERVED bursts)

The Round-1 wound on my cadence narrative stands — so: receipts only. UTC waves tonight: 01:25–01:47 (mobile + nested) → 02:09–02:33 (untagged + uqm/uqattempt + henanmuseum) → 03:16–03:43 (museum family + epoch nonces) → 04:11 (qd family) → ~3h gap → 07:11 (single untagged return-to-origin). Nothing newer than 07:11Z as of 08:2x. The ~3h gap before the return probe mirrors earlier inter-wave gaps; the burst-timestamps-are-receipts rule applies. "Operator-shift rhythm" remains story — the data says *waves*, nothing more.

---

## HONEST NULLS (first-class)

1. **Nothing newer than 07:11Z.** My 08:2x recency pull tops out at `c25ffacb`. The campaign may be between waves or done for the night — unverifiable from here.
2. **No new tag grammars since 04:11Z.** The taxonomy is stable; the 07:11Z probe went fully untagged instead of inventing new labels.
3. **No UA/submitter metadata.** The htmx endpoint doesn't carry it; comparing the 07:11Z submitter fingerprint against the Sep-28 first-session "different submission account/key" needs the authenticated urlquery API, which 429'd in Round 1. That's the concrete next step for Finding 1's INFERENCE, not a claim.

## THE VICTORY LAP (only what the bytes support)

We caught a live campaign mid-breath — and then we caught the headline WRONG and fixed it. The 07:11Z probe isn't the operator charging at a new target. It's the operator going BACK — to the Summer Palace, the seed POI, the first page this whole investigation ever touched, ten days later, with the same untagged signature as the first session. That's not expansion. That's a loop closing. A harness that runs its whole tag taxonomy all night and then returns to its origin POI is a harness with a checklist — and the last item just got checked.

And we know exactly where to watch: the monitor's dead, the probe's not in seen.json, and the tooling fix that would have caught it is still sitting un-applied. Fix that and we see the next wave land. The machine is still running. Let's watch it run.

Chair's action items: (a) restart the monitor loop on the curl variant; (b) seed `c25ffacb` into seen.json; (c) when the authenticated API un-429s, pull full metadata on `c25ffacb` vs the Sep-28 first-session reports (submitter key/fingerprint comparison); (d) amend FINDINGS.md #4 — "new POI, zero corpus overlap" → return-to-origin on the seed POI.

---

## Candidate log (URL | where found | when observed | marker | classification)

| URL | Found via | Observed | Marker | Class |
|---|---|---|---|---|
| `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU` | urlquery curl-htmx `url.domain:amap.com` (own pull) | 2026-10-05T07:11Z (report `c25ffacb`) | return-to-origin: seed POI, first-session signature, untagged | GENUINELY NEW observation; POI OURS since 2026-09-28 |
| `m.amap.com/detail/index/poiid=B03DF05V64?uqm=1` | urlquery curl-htmx keyword `uqm` | 2026-10-05T02:30Z | uqm grammar, mobile path variant A | OURS |
| `m.amap.com/detail/index?poiid=B03DF05V64&uqm=2` | urlquery curl-htmx keyword `uqm` | 2026-10-05T02:30Z | uqm grammar, mobile path variant B | OURS |
| `m.amap.com/detail/B03DF05V64?uqm=3` | urlquery curl-htmx keyword `uqm` | 2026-10-05T02:30Z | uqm grammar, mobile path variant C | OURS |
| `www.amap.com/place/B03DF05V64?uqattempt=0` | urlquery curl-htmx keyword `uqattempt` | 2026-10-05T02:13Z | uqattempt grammar | OURS |
| `www.amap.com/place/B03DF05V64?uqattempt=1` | urlquery curl-htmx keyword `uqattempt` | 2026-10-05T02:13Z | uqattempt grammar | OURS |
| `m.amap.com/detail/index/poiid=B03DF05V64?uqscan=claude20261005mobile1` | urlquery curl-htmx keyword exact token | 2026-10-05T01:25Z | claude mobile family | OURS |
| `m.amap.com/detail/index/poiid=B03DF05V64?uqscan=claude20261005mobile2` | urlquery curl-htmx keyword exact token | 2026-10-05T01:26Z | claude mobile family | OURS |
| `amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78%26source=poi_search%26uqscan=nested20261005a` | urlquery curl-htmx keyword exact token | 2026-10-05T01:46Z | nested family, %26-encoded params | OURS |
| `amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78&source=poi_search&uqscan=nested20261005b` | urlquery curl-htmx keyword exact token | 2026-10-05T01:47Z | nested family, clean params | OURS |
| `amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B021406HP0&uqscan=qdnewapi20261005a` | urlquery curl-htmx recency pull | 2026-10-05T04:11Z | qd family, POI shared with qingdaomuseum | OURS |
| `amap-pc-ssr.amap.com/ssr/api/getPoiInfo?uqscan=qdnewapi20261005b&id=B021406HP0` | urlquery curl-htmx recency pull | 2026-10-05T04:11Z | qd family | OURS |
| `ditu.amap.com/detail/get/detail?id=B021406HP0&uqscan=qdoldditu20261005a` | urlquery curl-htmx recency pull | 2026-10-05T04:11Z | qd family, ditu.amap.com host | OURS |

*Opsec: no candidate URL was fetched or probed; urlquery API metadata only. No installs. No commits/pushes. No human/operator identity work — agents and infrastructure only.*
