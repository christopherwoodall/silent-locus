# WEB-SEARCH worker — FINDINGS
**Lane:** lifeval-cross-corpus web search · **Date:** 2026-10-06 · **Run window:** 18:16–18:20 CDT
**Method:** `browser_search`, passive only. No page fetches, no visits (per opsec rule — candidate URLs logged, never opened).
**Raw evidence:** `raw/q01..q10-*.txt` (query, timestamp, method, per-result kill reasons).

## Verdict

**No cross-corpus hit.** None of the Lifeval marker strings — in full,
short, HTML-comment, or edit-comment form — is indexed anywhere on the
public web outside the Wikimedia diffs we already hold. The marker family
exists in exactly one place we can verify publicly: the June-25-2026
Wikimedia sandbox revisions. That locality is itself evidence: this is a
private codename, not a reused public string.

## Per-string results

### String 1 — `"Lifeval temporary technical sandbox initialization"` (exact, quoted)
- **Grade: OBSERVED-zero.** Search engine decomposed the quoted phrase; 7 hits, all generic sandbox-troubleshooting pages (Windows Sandbox, Fidelis, CertiK).
- No `Lifeval` token in any hit. Full string not indexed. Raw: `raw/q01-*.txt`

### String 2 — `"Lifeval API temp-account test"` (exact, quoted)
- **Grade: OBSERVED-zero.** 8 hits, all generic email-validation / temporary-email API pages. No marker. Raw: `raw/q02-*.txt`

### String 3 — `"Lifeval"` standalone (with discriminators: +sandbox, +temp-account, +wikipedia, +wikimedia)
- **Grade: no campaign hit; NOISE separated.** Every hit falls into one of three buckets (see appendix):
  - Tokyo Gas "LIFEVAL" sponsor brand noise (expected per brief) — mapcarta, cybo, jcom listings.
  - "Life is Feudal" sandbox-MMO gaming noise — massivelyop, bleedingcool, eurogamer, gamingnexus.
  - **LIFBench/LIFEVAL academic name collision** — see Surviving item below.
- Queries run: `"Lifeval" sandbox wikipedia`, `"Lifeval" temp-account test`, `"Lifeval" wikimedia`. Raw: `raw/q04-*.txt`, `raw/q05-*.txt`, `raw/q09-*.txt`

### String 4 — `"Temporary technical sandbox initialization"` (exact, quoted, no Lifeval)
- **Grade: OBSERVED-zero.** Engine decomposed the phrase; 8 generic sandbox hits (Microsoft Q&A, Insillion, Azure). The incident's literal edit comment (7 of 54 edits) is not indexed. Raw: `raw/q03-*.txt`

### String 5a — `"sandbox test link"` (exact, quoted)
- **Grade: OBSERVED-zero.** 8 generic hits (Phaser, Alchemer, edX, Plaid, Lomi, etc.). Raw: `raw/q07-*.txt`

### String 5b — `"testing external link"` (exact, quoted)
- **Grade: OBSERVED-zero.** 6 generic hits (dev docs, tabnabbing SKILL.md, a11y article, PRs). The 2026-05-27 en.wikipedia incident comment is not indexed. Raw: `raw/q08-*.txt`

### String 5c — `"Temporary technical sandbox"` (exact, quoted, short form)
- **Grade: OBSERVED-zero.** 8 generic hits (Metrc, Techdirt, AWS, OpenClaw sandboxing docs). Raw: `raw/q10-*.txt`

### String 6 — `"<!-- Lifeval"` (HTML-comment form, quoted)
- **Grade: OBSERVED-zero.** Engine strips `<!--` and treats it as a Lifeval-term query; same family as string 3. No literal HTML comment indexed. Raw: `raw/q06-*.txt`

## Surviving items (1 — name collision, not a campaign hit)

### LIFEVAL — rubric-based LLM evaluation framework (LIFBench paper)
- **URL:** https://arxiv.org/abs/2411.07037 (also alphaxiv.org/abs/2411.07037v3, pure.ecnu.edu.cn, aclanthology.org/people/l/lu-xiangju/)
- **What it is:** Section 4 of the LIFBench paper ("Evaluating the Instruction Following Performance and Stability of Large Language Models in Long-Context Scenarios", Wu et al., submitted Nov 2024, revised Jul 2025) defines **LIFEVAL**, a rubric-based automated scoring framework for LLM instruction-following.
- **Grade: INFERENCE (homonym) — NOT the campaign codename.**
  - The paper predates the June-2026 incident by ~19 months; named human authors (Xiaodong Wu, Minhao Wang, Yichen Liu, Xiaoming Shi, He Yan, Xiangju Lu, Junmin Zhu, Wei Zhang, East China Normal University). It is a legitimate academic benchmark component, not a fleet artifact.
  - Recorded because the anomaly rule treats off-frame findings as leads: the coincidence is real and documented, and the fleet's `Lifeval` codename for a *temp-account evaluation harness* sharing a name with an *LLM evaluation framework* named LIFEVAL is at least worth one line in the provenance record. It does not, by itself, connect anything.
  - Recommendation for coordinator: keep as a collision footnote; do NOT treat as attribution evidence.

## Killed-by-noise appendix

| Bucket | Count | Examples |
|---|---|---|
| Tokyo Gas LIFEVAL (sponsor brand) | 6 | mapcarta.com/N5316223602 (東京ガス LIFEVAL Aoba shop); cybo.com Tokyo gas-station listings (東京ガスライフバル豊島/千代田/品川 etc.); jcom.co.jp Tokyo Gas supplier list |
| "Life is Feudal" sandbox MMO | 5 | massivelyop.com (x2), bleedingcool.com, eurogamer.net, gamingnexus.com |
| Generic Windows/Azure sandbox | ~14 | learn.microsoft.com (x6), thewindowsclub.com (x2), techcommunity.microsoft.com, vocal.media, docs.aws.amazon.com, docs.openclaw.ai, metrc.com (x2), insillion.com |
| Generic test/API/insurance | ~10 | brainly.com, scribd.com (x2), prepawaytest.com, pass4leader.com, medium.com (x2), meddeviceonline.com, control.com |
| Dev-tool "sandbox test link" | 7 | phaserjs issue 7034, alchemer, openedx PR 16056, qianghan/a3p plaid sandbox doc, lomiafrica sandbox payments, ceccopierangiolieugenio/rubbish, codeigniter thread, tusmusgun1997/voice-ai-copilot |
| Dev-tool "testing external link" | 6 | cboyd0319/jobsentinel, gustavogomez092/inkpot, payloadsallthethings tabnabbing SKILL.md, dev.to a11y, djangocms-cascade changelog, vellum-assistant PR 40388 |
| Code noise | 1 | codecogs.com depreciation example (`lifeVal` variable) |
| Generic "Life" wiki | 4 | wikidata.org Q632184 (life table), Q763264 (work–life balance), en.wikipedia.org Vial_of_Life, LifeWiki |

## Honest zeros (count)

- 5 of 10 query runs returned literally zero relevant results (`q01, q02, q03, q07, q08, q10` — 6 zeros; q04/q05/q06/q09 returned only noise/collisions).
- Every exact-quoted marker string (`q01, q02, q03, q07, q08, q10`) = zero indexed occurrences on the public web.

## Follow-ups for coordinator (not done — out of scope)

1. The `insource:"Lifeval"` on-wiki search (already done by wikipedia-lane; public-web search cannot reach it).
2. Search-engine result caps: only first-page (~7–8) results were returned per query. A deeper page crawl is unlikely to matter (exact-phrase matches would have ranked first), but noted for provenance.
3. Bing/Google vs. this index may differ; this run used the single `browser_search` index only.
4. Consider re-running this sweep if WMF publishes more diffs or the Diff article comments name the marker (search snippets may then pick up the incident pages themselves).

## No commits/pushes made (per brief — coordinator owns that).
