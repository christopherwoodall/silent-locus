# Finding #147 frozen-epoch claim — independent test on yourls.space public log

## TL;DR
Transluce #147 claims three yourls.space short links (created Sep 29–Oct 3) all hide the *same* embedded timestamp — evidence of a frozen naming-tool clock. We pulled the venue's own public link table and confirmed it: same three keywords, same creation times to the second, same frozen epoch 1779995045.
This completes the June→September tooling link that the [epoch-clock lane](../epoch-clock/) could only half-test.

## Grading legend
- **OBSERVED** — seen directly in the bytes of the fetched page.
- **INFERENCE** — our reasoned conclusion from the observed facts.
- **UPSTREAM** — taken from Transluce's finding record; not independently verified by us.

Date: 2026-10-07. Read-only, passive. Nothing redacted.

Jargon: **YOURLS** = a self-hosted URL-shortener package (the venue at yourls.space runs one); **Unix epoch** = seconds since 1970-01-01 00:00:00 UTC, the standard way computers stamp time.

## Claim under test (Transluce #147, Omer Zamir, UPSTREAM)

Three yourls.space links created Sep 29–Oct 3 embed the SAME Unix epoch
1779995045 (= 2026-05-28 19:04:05 UTC, one day after the May-27 prefill probe):
mid17799950450 (created 09-30 03:24:34), mid17799950451 (03:24:41),
mid17799950456 (09-29 17:44:17). A frozen naming-tool clock, contrasting with
June's live clock on rmn.re (verified on our cache in [epoch-clock](../epoch-clock/)).

## Test (OBSERVED)

Pulled the venue's own public link table (homepage, 15 most recent links).
Keywords carry an 11-digit suffix; only the 10-digit parse is a valid epoch
(11-digit = year 2534), with a 1-digit sequence tail.

| keyword | created (log epoch → UTC) | embedded epoch | delta (s) |
|---|---|---|---|
| mid17799950450 | 1790738674 → 2026-09-30 03:24:34 | 1779995045 | −10,743,629 |
| mid17799950451 | 1790738681 → 2026-09-30 03:24:41 | 1779995045 | −10,743,636 |
| mid17799950456 | 1790703857 → 2026-09-29 17:44:17 | 1779995045 | −10,708,812 |

All three creation timestamps match #147's asserted times **to the second**.
All three embed the identical epoch 1779995045 = 2026-05-28 19:04:05 UTC.
Delta spread (34,824 s) equals the creation-time spread exactly — the embedded
value is constant, so the naming tool used a fixed epoch, not a live clock.

## Verdict: CONFIRMED

#147's September frozen-epoch claim replicates byte-exact on the live public
log: same three keywords, same creation timestamps to the second, same frozen
epoch 1779995045 shared across links created ~10 h apart. The June→September
tooling link (live clock → frozen clock, same marker-word-plus-epoch naming
convention) holds on independent re-pull.

## Corroborating observations (OBSERVED, not the claim)

- The September ag0/my13 cluster from #147 is present in the same table:
  ag0ssrftwo581395, ag0spaceinner85853, my13airgood{nav,tinyq,direct}*,
  sprobe9792, mytrig2100291, zagent0d13ord15cmpour16, 4351361b.
- Creator IPs are Tencent (82.156.x, 82.157.x, 81.70.x, 43.138.x, 49.232.x,
  140.143.x) and Huawei (116.204.x, 113.44.x, 1.92.x) ranges — matches #147's
  hosting claim.
- The yourls.pro admin-prefill targets carry `zz=` params (zz=282036,
  zz=192985, zz=22164) — our toolkit grammar in the wild.
- 4351361b (Sep 30, target https://example.org/SSRFDESTSP4351361); the
  tinyurl preview target embeds #ag1353617395 — the 4351361 marker recurs.

## Limits

- Only the 15 most recent links are public; the full 291-link history is not
  exposed, so #168's "4351361 first appears Sep 11" is UNTESTABLE here.
- The test confirms the naming-tool fingerprint, not provider attribution —
  same caveat #147 itself states.

Evidence: lane-local pull, `raw/link-table.json` + `raw/yourls-space-stats.json` (SHA256SUMS.txt).
