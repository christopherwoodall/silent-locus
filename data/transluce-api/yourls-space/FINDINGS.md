# Finding #147 frozen-epoch claim — independent test on yourls.space public log

## TL;DR
Transluce #147 says three yourls.space short links (made Sep 29–Oct 3) all hide the *same* embedded time. That would mean a frozen naming-tool clock.
We pulled the venue's own public link table and confirmed it. Same three keywords. Same creation times to the second. Same frozen epoch 1779995045.
This completes the June→September tooling link that the [epoch-clock lane](../epoch-clock/) could only half-test.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: another source said this; we did not check it.

## Term definitions
- **YOURLS**: a self-hosted short-link package. The venue at yourls.space runs one.
- **epoch**: seconds since 1970-01-01 00:00:00 UTC. Computers use it to stamp time.
- **keyword**: the short name of a short link. Example: `mid17799950450`.

Date: 2026-10-07. Read-only, passive. We removed nothing.

## Claim under test (Transluce #147, Omer Zamir, UPSTREAM)

Three yourls.space links made Sep 29–Oct 3 embed the SAME epoch 1779995045. That is 2026-05-28 19:04:05 UTC. It is one day after the May-27 prefill probe. The keywords: mid17799950450 (made 09-30 03:24:34), mid17799950451 (03:24:41), mid17799950456 (09-29 17:44:17). A frozen naming-tool clock. This contrasts with June's live clock on rmn.re (verified on our cache in [epoch-clock](../epoch-clock/)).

## Test (OBSERVED)

We pulled the venue's own public link table (homepage, 15 most recent links). Keywords carry an 11-digit suffix. Only the 10-digit parse is a valid epoch (11-digit = year 2534). The 11th digit is a sequence tail.

| keyword | created (log epoch → UTC) | embedded epoch | delta (s) |
|---|---|---|---|
| mid17799950450 | 1790738674 → 2026-09-30 03:24:34 | 1779995045 | −10,743,629 |
| mid17799950451 | 1790738681 → 2026-09-30 03:24:41 | 1779995045 | −10,743,636 |
| mid17799950456 | 1790703857 → 2026-09-29 17:44:17 | 1779995045 | −10,708,812 |

All three creation times match #147's stated times **to the second**. All three embed the identical epoch 1779995045 = 2026-05-28 19:04:05 UTC. The delta spread (34,824 s) equals the creation-time spread exactly. The embedded value is constant. So the naming tool used a fixed epoch, not a live clock.

## Verdict: CONFIRMED

#147's September frozen-epoch claim replicates byte-exact on the live public log: same three keywords, same creation times to the second, same frozen epoch 1779995045 shared across links made ~10 h apart. The June→September tooling link (live clock → frozen clock, same marker-word-plus-epoch naming convention) holds on independent re-pull.

## Corroborating observations (OBSERVED, not the claim)

- The September ag0/my13 cluster from #147 is present in the same table: ag0ssrftwo581395, ag0spaceinner85853, my13airgood{nav,tinyq,direct}*, sprobe9792, mytrig2100291, zagent0d13ord15cmpour16, 4351361b.
- Maker IPs are Tencent (82.156.x, 82.157.x, 81.70.x, 43.138.x, 49.232.x, 140.143.x) and Huawei (116.204.x, 113.44.x, 1.92.x) ranges. This matches #147's hosting claim.
- The yourls.pro admin-prefill targets carry `zz=` params (zz=282036, zz=192985, zz=22164). This is our toolkit grammar in the wild.
- 4351361b (Sep 30, target https://example.org/SSRFDESTSP4351361); the tinyurl preview target embeds #ag1353617395. The 4351361 marker recurs.

## Limits

- Only the 15 most recent links are public. The full 291-link history is not exposed. So #168's "4351361 first appears Sep 11" is UNTESTABLE here.
- The test confirms the naming-tool fingerprint, not provider attribution. #147 itself states this caveat.

Evidence: lane-local pull, `raw/link-table.json` + `raw/yourls-space-stats.json` (SHA256SUMS.txt).
