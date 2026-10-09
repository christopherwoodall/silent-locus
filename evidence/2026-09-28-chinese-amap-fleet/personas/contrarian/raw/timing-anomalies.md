# Timing anomalies — 2026-09-28 Chinese Amap fleet

Corpus: `data/2026-09-28-chinese-amap-fleet/events.jsonl` — 2,141 records,
span 2026-09-28 20:57:23Z → 2026-10-05 01:12:40Z (~6.2 days).
All hour references below are Asia/Shanghai (SH, UTC+8) unless marked Z.
Timestamps decode-verified with python (`datetime.fromtimestamp`); bare-epoch
and epoch-embedded `uqscan` tags decode to unix time and were checked
individually against submission times.

Tag-shape taxonomy used here:
- `null` (1,075) — no `fleet_tag`
- `dated` (804) — contains `2026MMDD`
- `epoch-embedded` (124) — word + 10-digit epoch, e.g. `target1791141450`
- `bare-epoch` (58) — pure epoch, e.g. `1791077647`, optional letter suffix
- `no-date` (65) — neither epoch nor date, e.g. `claudeprime`, `directhost5`, 8-hex hashes
- `uuid` (15) — full `8-4-4-4-12` hex, e.g. `7d52beed-…`

## Baseline: the normal pattern

- Operator works SH roughly 11:00 → 02:00. Hour histogram (SH): peaks at
  13 (154), 18 (191), 19 (165), 20 (135), 21 (155); troughs at 03 (19) and
  10 (32). This is a late-morning-to-2AM operator, not a 9-to-5 one.
- Metronome: median inter-arrival 12.5s across the corpus; 1,653 of 2,140
  gaps <60s, 1,376 <30s. Steady machine cadence.
- No minute-scale rushes: max 12 submissions in any 60s bucket (median 2);
  no bucket exceeded 8× its local 30-min baseline. The fleet does not surge;
  it hums.
- Routes: `direct`/amap.com dominates (1,969). The side channels —
  `carrier`/httpbun.com (65), `carrier`/httpbin.org (27),
  `carrier`/livecodes.io (24), `relay`/href.li (19) — are a small night
  layer (see Anomaly 6).

## Anomaly 1: the Oct 2–3 blackout and the Oct 4 super-run

Per-day counts (SH date): 09-29: 20 · 09-30: 38 · 10-01: 169 · 10-02: 10 ·
10-03: 2 · 10-04: 1,600 · 10-05: 302.

The fleet went nearly dark for ~56 hours — a 32.8h gap (Oct 1 22:24Z →
Oct 3 07:11Z) followed by a 16.7h gap (Oct 3 07:11Z → 23:52Z) — then
resumed as a single 16-hour continuous run: Oct 3 23:52Z → Oct 4 15:58Z,
1,600 records, per-hour median gap 5–13s (ramp-up at SH 08–10, full speed
from SH 12).

What broke: everything about the preceding cadence. Oct 1's 169 records
were already the biggest day to that point; Oct 4 is 9.5× that.

Read: deliberate campaign restart, not noise. The Oct 4 run carries the
richest vocabulary in the corpus and the numbered A/B suites (Anomaly 7) —
it reads as the main experiment window after a 2-day pause (operator away,
infra rebuild, or deliberate cooldown).

## Anomaly 2: the lone submission before the blackout

- `2026-10-01 22:24:33Z` (SH 10-02 06:24), tag `research20261002a`,
  direct/amap.com — 3.8h after the previous submission, 32.8h before the
  next. The only record satisfying >2h isolation on both sides.
- Report: https://urlquery.net/report/89288319-eb24-4f1f-83d2-03d2dde6c6f9

Read: a dangling probe — the first `research20261002` "a"-tag, fired alone
at 06:24 local, then the fleet went silent for 33h. Either a test ping
before the operator stood down, or the last gasp of the Oct 1 campaign.
Notably the tag date (1002) matches the SH date (Oct 2) — the tagger is
local-date aware.

## Anomaly 3: the UUID nonce burst (SH 12:15–13:08, Oct 4)

- 15 UUID tags total; 13 land inside a 53-minute window on Oct 4:
  04:15Z→05:08Z (SH 12:15→13:08). One straggler at 10:01Z (SH 18:01).
- The UUID `7d52beed-5ec8-4f2d-bbae-e53c79a290b6` is reused 5× (SH 12:16,
  12:31 ×2, 12:32, 18:01) — the same nonce across 6 hours. The other 10
  UUIDs are unique.
- Zero UUID tags appear anywhere else in the 6-day span.

Read: operator experiment — a distinct tool or config emitting UUID
`uqscan` values, trialled for under an hour at midday Oct 4. The 5×-reused
UUID smells like a copy-pasted template or a fixed session identifier
rather than a per-submission nonce. Different actor is possible but
unnecessary; different *tool* is near-certain.

## Anomaly 4: future-dated epoch nonces in the deep-night run

Three tag families submitted Oct 4 17:42Z–18:10Z (SH Oct 5 01:42–02:10)
carry epoch nonces decoding ~2.6–2.7h in the FUTURE:

| submitted (Z) | tag | nonce decodes | skew |
|---|---|---|---|
| 17:42–17:53 | `xjpark1791145452`…`56` (×5) | 20:24Z | +2.7h |
| 18:03 | `detail/loc/target/old/www/ditu-1791146590`…`95` (×6) | 20:43Z | +2.7h |
| 18:10 | `xspoidetail1791146900/01`, `xspath1791146903` | 20:48Z | +2.6h |

Baseline check: ordinary epoch tags in this corpus decode within minutes
of submission (e.g. `verify1791107960` → 09:59:20Z, submitted 10:00Z;
`1791159341` → 00:15:41Z, submitted 00:18Z; ms-epoch
`taersi-pre-mobile-1791130127175` → 16:08:47Z, submitted 16:09Z). The
+2.7h skew is consistent across all three families and appears in no other
window.

Read: a URL-generator with a clock ~2.7h fast (or pre-generated future
nonces), active only in this window — a different build box, container, or
tz-misconfigured script. Same window also hosts the navy971 pair, the
8-hex hash burst, and `answer20261005{a,b,c}` — the whole SH 01:42–02:10
pocket is one coherent late-night session on skewed infrastructure.

## Anomaly 5: stale epoch nonces (replayed queues)

- `1790767001/2/3` decode to 2026-09-30 11:16:41–43Z but were submitted
  2026-10-01 10:54Z — 23.6h stale, fired as a 3-tag burst (SH 18:54 Oct 1).
- `wfjxy202609292339` submitted Oct 4 05:23Z (SH 13:23) — template built
  Sep 29, replayed 5 days later.
- `zju20260929` submitted Oct 4 06:49Z.
- `2026092701` ×2, `2026093001`, `2026093003`, `20260930capture1` submitted
  Sep 30 18:33–18:46Z (SH Oct 1 02:33–02:46) — day-old dated templates in
  the deep-night pocket.

Read: recycled URL lists / replayed submission queues. The operator
re-submits old batches — the fleet's "memory" is the queue file, not the
clock. Stale nonces are the tell.

## Anomaly 6: odd hours, side channels, and vocabulary time-signatures

**The side channels are nocturnal.** `carrier`/httpbun.com (65):
SH 0 (18), 22 (15), 23 (22), 1 (6). `relay`/href.li (19): SH 19–23, 0–1.
gaode.com/httpbin.org/livecodes.io carrier probes scatter SH 6–21 but
concentrate 19–23. The bulk `direct`/amap.com fleet runs all hours; the
relay/httpbun probing layer wakes up ~19:00 and sleeps ~02:00.

**Odd-hour pockets:**
- SH 03:00–04:00 (19 records): mostly nulls and bare epochs — but the
  Oct 5 03:11–03:58 cluster uses *correct next-day* `20261005` tags
  (`dawugang20261005b`, `research20261005szcec`, `targetapi20261005`,
  `claude20261005hospital2/3`, `claude20261005sph`, `jxmuseum-mobile-detail`)
  plus one livecodes.io carrier probe at 03:36. Same night-owl operator
  working past 3:30 AM, tagger still local-date-correct — consistent actor,
  not a handoff.
- SH 10:00–11:00 (32): 25 nulls + stale bare epochs (`1790733602` exact at
  02:00Z; `1790733901/02` decode 02:05Z, submitted 02:21Z — 16 min stale) +
  `exit31` + livecodes.io carrier probes. Reads as morning warm-up /
  connectivity checks before the day's campaign.

**Vocabulary shifts at time boundaries:**
- Midnight SH rollover: tags flip `20261004`→`20261005` exactly at the
  boundary (first `20261005` tag: `hzparadise20261005a` at 16:38Z =
  SH 00:38). The tagger is script-local-date driven.
- bare-epoch spikes at SH 18 (19 of 58) and SH 21 (10); epoch-embedded
  spikes at SH 18 (37 of 124).
- no-date suites cluster SH 20–21 (`fjmuseum*` ×10 at 20:47–21:12,
  `directhost0–5` at 21:41, `pd1–4`/`s1–2` at 20:40) and SH 01:19–01:23 Oct 5
  (ten 8-hex hashes: `d745f12e`, `156d324b`, `9f36c491`, `683e2212`,
  `d6faa07d`, `21677c51`, `b9a3a2ce`, `a45ca478`, `3cbfbf35` + tag `1`).
- One-word series are time-boxed: `answer20261005{a,b,c}` only SH 01:58–02:04
  Oct 5; `navy971-20261005{b,c}` only SH 02:03 Oct 5 (note: b and c, no `a`
  anywhere in the corpus — truncated series); `claudeprime` exactly once,
  at SH 05:48 Oct 5 — the last distinctive tag before the corpus tail ends
  (final record 01:12Z = SH 09:12, `research20261005d`).

## Anomaly 7: bursts-within-bursts (micro-runs)

Numbered A/B suites fired as tight clusters inside the main run —
each is one scripted experiment (UA / platform / endpoint comparison):

- `njxzgz20261004p0–p9`-ish (8 tags, burst 8) — SH 19:43 Oct 4
- `njxzgz20261004s0–s9`-ish (8 tags, burst 8) — SH 19:45 Oct 4
- `claude1–4` — SH 08:48 Oct 4
- `cookiea/b/c` — SH 16:28 Oct 4
- `directhost0–5` — SH 21:41 Oct 4
- `pd1–4`, `s1/s2` — SH 20:40 Oct 4
- `fjmuseum*` (10 variants incl. `fjmuseumgaodessr` on gaode.com) — SH 20:47–21:12
- `xjpark*` (10 tags, future-skewed nonces) — SH 01:42–01:53 Oct 5
- `research20261004{target,poi,api,detail,ssr}` ×2 each — SH 02:07–02:10 Oct 5
- `taersi-*` ms-epoch series (5 tags) — SH 00:08–00:26 Oct 5
- `claudetarget*` (14 tags, burst 4) — SH 11:10 Oct 4

Plus 42 identical-tag repeat pairs within 60s (retry / double-submit
behavior), e.g. `verify1791107960` ×3 in the same minute (SH 18:00),
`1791077647` ×4 across 01:35–01:36Z, `7d52beed-…` ×2 within the same minute
at SH 12:31.

Read: operator experiments, not noise. The numbering grammar (a/b/c,
0–5, p/s variants, www/mobile/ssr/api/legacy axes) is the operator's A/B
vocabulary; each micro-run is one comparison batch.

## Anomaly 8: metronome breaks inside the Oct 4 run

Per-SH-hour median gaps on Oct 4: 5–13s for SH 12–21 (fastest SH 21 at
5s), slower at the edges — SH 08 (24s), SH 09 (39.5s), SH 10 (70s), SH 22
(56s), SH 23 (42s). Slowest internal patches: 24.8 min (SH 10:37→11:02),
18.9 min (SH 09:04→09:23), 14.4 min (SH 16:09→16:23), 13.8 min
(SH 08:24→08:38). Morning (SH 08–10) is ramp-up with the longest pauses;
the run never fully stops after SH 11:02 until 23:58.

What held: the metronome never broke into a rush — the fastest patches
are just denser micro-runs (SH 18–19: median 6–7s), not stampedes.

## Cross-tab: odd-shaped tags × time (summary)

- **UUID (15):** 87% in SH 12:15–13:08 Oct 4 → one-off midday experiment
  window (Anomaly 3). One reused nonce ×5.
- **bare-epoch (58):** spikes SH 18 and SH 21; deep-night pocket usage
  (SH 03 Oct 5); one 23.6h-stale triple (Anomaly 5).
- **epoch-embedded (124):** spike SH 18; the future-skewed (+2.7h) cluster
  confined to SH 01:42–02:10 Oct 5 (Anomaly 4).
- **no-date (65):** suite bursts SH 20–21, 8-hex hash burst SH 01:19–01:23
  Oct 5, lone `claudeprime` SH 05:48 Oct 5.
- **relay/carrier side channels:** SH 19:00–02:00 phenomenon (Anomaly 6).

## Consolidated read

1. **One main operator** — night-owl, SH 11:00→02:00, steady ~10s metronome,
   local-date-aware tagger, numbered A/B suite grammar. The Oct 4 super-run
   is the campaign; Oct 2–3 was a deliberate pause.
2. **A second tool signature in the deep-night pocket** (SH 00:00–02:10 Oct 5):
   +2.7h-future nonce generator, navy971, 8-hex hashes, `answer*` series,
   relay/httpbun layer. The clock skew is the strongest evidence of a
   different machine or misconfigured container — worth treating as a
   distinct tool if not a distinct hand.
3. **A third signature at midday Oct 4** (SH 12:15–13:08): UUID nonces,
   one-off, 53-minute experiment.
4. **Recycled queues**: stale nonces (hours to 5 days old) re-submitted —
   the fleet replays old URL lists; tag timestamps are build-time, not
   submit-time, so treat them as queue age, not event time.

## Method notes / caveats

- All epoch decodes verified against actual submission timestamps in python;
  ordinary tags match within minutes, which is what makes the +2.7h-future
  and −23.6h-stale clusters significant rather than tz confusion.
- "Lone" is defined as >2h from both neighbors; only one record qualifies.
- Minute-bucket burst detection used an 8× local-median threshold and found
  nothing — the interesting clustering lives at the 5–15 minute micro-run
  scale (numbered suites), not the per-minute scale.
- Hour analysis is in Asia/Shanghai, inferred from amap.com/gaode.com
  targeting and the diurnal shape; UTC histograms are bimodal-shifted and
  less interpretable, which supports the SH choice.
