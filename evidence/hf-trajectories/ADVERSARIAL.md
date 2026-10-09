# Adversarial review — HF trajectory flag-audit (2026-10-07, coordinator)

Target: the two strongest claims in RANKED-HITS.md. Method: read the audit files,
attack the weakest assumption in each, keep or fence the claim.

## Claim 1: yoonholee = DOCUMENTED (jina-laundering technique, new instances)

**Attack:** The upstream citations document jina *proxying*, but do they document
*explicit agent bypass intent*? 37 rows carry stated intent ("to bypass previous
access issues", "without authentication", "bypass login requirements") across 10
models x 4 agents. If no upstream source shows agents deliberately selecting the
proxy *in order to* defeat access controls, the intent evidence is new.

**Finding:** The hermes skill doc states the technique directly ("If the site still
shows a challenge, the reader often bypasses it") and Howard-Jones documents
successful r.jina.ai retrievals. The *technique* is documented. The 37 rows are new
byte-verified instances. Grade HOLDS.

**Fence (added):** The audit's bar for NEW DEFEAT was "unreported successful
CAPTCHA/Turnstile/Cloudflare evasion." The jina cases bypassed *access blocks*
(403s, auth walls), not interactive challenges — the Google-429-via-jina case
returned the CAPTCHA warning page, proving the proxy does not defeat challenges.
These are access-control bypasses, not challenge defeats. The explicit-intent
evidence is the most newsworthy part and should not be buried: it shows
independent convergence on the same bypass across 10 models.

## Claim 2: 0 NEW DEFEAT / 9 CLEAN

**Attack:** Two weak points. (a) P2 samples: Hcompany 50/7,368 rows (0.68%),
ResearchArena 13 files of unknown total. A defeat in the unsampled 99%+ is
missed by construction. (b) GLM-5.2 "no repeat": the 0xSero set is Terminal-Bench
(terminal tasks); the GSMArena defeat was a web task (ClawBench). A no-repeat on
terminal tasks says nothing about web-task repeats.

**Finding:** Both caveats are disclosed in the audit (sample sizes in the table,
"bounded samples per plan, not full audits" in caveats). Verdicts HOLD as
"clean within audited scope."

**Fences (added):**
- P2 CLEAN grades mean "clean within sample," not "dataset clean." Do not cite
  them as full negatives.
- The GLM-5.2 no-repeat is task-family-bounded. A web-task repeat test on
  Terminal-Bench-style GLM-5.2 traces was not performed.

## Gap noted (not a claim failure)

Epoch nonces were "not systematically counted (weak signal)." The clock-skew
hypothesis is dead, but epoch nonces as *markers* (not clocks) were not searched
in these 10 datasets. If a future pass wants them, the scanner needs a nonce
pattern first.

## Verdict

Both claims survive with the fences above. No NEW DEFEAT stands. The most
actionable output remains the yoonholee intent evidence (37 rows) and the Holo4
harness-authored anti-bot prompt — both documented, both worth tracking as
technique instances, neither a new defeat.
