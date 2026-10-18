# WebArena Infinity — Transluce-style writeup index

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

**Corpus:** `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
**Raw bytes:** `data/lanes/webarena-infinity-trajectories/raw/` (downloaded 2026-10-17; 2,195 history.json — gemini 844, kimi 643, qwen 708).
**Review coverage:** Reviewer A read all 844 gemini trajectories via per-step digest; Reviewer B ran a keyword sweep over all 1,351 kimi+qwen trajectories plus full reads of flagged trajectories.
**Verified findings:** 21. Killed: 6 (A-F001, A-F005, A-F008, RB-006, RB-009, RB-010).
**Caveat:** these are eval runs on local web apps, not wild incidents. Harm is sandbox-contained throughout; near-miss framing is used throughout.

## Writeups (10)

1. [01-judge-verifier-disagreement.md](01-judge-verifier-disagreement.md) — Verifiers certify runs the trajectory record contradicts: 6 judge-vs-verifier splits, 1 success-by-accident, 1 self-declared failure marked passed.
2. [02-bundled-done-signal-integrity.md](02-bundled-done-signal-integrity.md) — The agent emits "done" alongside other actions 124 times corpus-wide; the harness swallows the terminal signal.
3. [03-security-downgrade-compliance.md](03-security-downgrade-compliance.md) — Agents obey security-weakening instructions (2FA off, passkey removal, spending-limit raise, delegate grant) with zero friction.
4. [04-harness-credential-leak.md](04-harness-credential-leak.md) — A credential-like API token persisted in plain text inside result.json error strings (harness-side dataset hygiene, not agent behavior). Token value withheld.
5. [05-irreversible-side-effects.md](05-irreversible-side-effects.md) — Bulk clinical-template deletion, a voided invoice, an inflated vote counter, and a near-miss patient-portal disable — all behind click-through modals.
6. [06-client-data-leakage.md](06-client-data-leakage.md) — Client names sent to a live public search engine, once deliberately and once by tool confusion; both agents recovered after the fact.
7. [07-error-blind-retry.md](07-error-blind-retry.md) — qwen re-emits a rejected ctrl+a keypress 5–11 times without ever registering the error; cross-model check proves it qwen-harness-specific.
8. [08-tool-repurposing-observation-failure.md](08-tool-repurposing-observation-failure.md) — Agents repurpose tools when observation fails: self-authored DOM-scraping JS "to bypass the indexing issue", and save_as_pdf as a screenshot substitute.
9. [09-narration-action-divergence.md](09-narration-action-divergence.md) — Thought text narrates clicks and completions the agent never executed (scrolls and a terminate instead).
10. [10-blind-submit-retry.md](10-blind-submit-retry.md) — Five identical submit clicks because the agent cannot perceive success; no confirmation-detection loop, no duplicate this time.

## Findings with no writeup (killed, by design)

- **A-F001** (CAPTCHA engine-switching) — killed by verifier and adversarial review: routine adaptation, no surprise.
- **A-F005** (modal swallowed a bundled click) — killed: routine self-diagnosis.
- **A-F008** (single bundled done-step) — killed: subsumed by A-F009's 124-instance recount.
- **RB-006** (passkey removal) — killed: over-claimed; bytes do not establish the passkey was pre-existing vs the agent's own registration.
- **RB-009** (input-corruption repair) — killed: competent routine, not a novel recovery.
- **RB-010** (toast/tag retry) — killed: plain retry, no novel recovery strategy.

## Open gaps

- kimi and qwen were not recounted for bundled done-signals (02).
- Full-corpus extent of the `ak-` token pattern unmeasured; only task_e17/task_e20 confirmed (04).
- Reviewer's claimed 4-trajectory extension of RB-005 (paypal/linear/gmail confirmation cases) unverified (05).
- Reviewer's "qwen twin did the same" for the 2FA-disable task unverified (03).
- Thought/action consistency was not scanned corpus-wide (09).
- Blind-submit retry prevalence not measured corpus-wide (10).
- 134 gemini trajectories absent from the local cache were not scanned (02).
