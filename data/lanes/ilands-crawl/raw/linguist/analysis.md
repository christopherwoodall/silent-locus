# iLands dev.to corpus — linguist analysis (worker 4/6)

Date: 2026-10-12. Method: read-only analysis. No contact made with any author.

The dev.to corpus was not yet scraped at start of work. This analysis uses a hand-fetched corpus of 7 agent-authored posts retrieved from the dev.to public API. Quotes below are brief (short fragments) for analysis.

## 1. Corpus inventory

All posts are on dev.to, tagged "ai"/"discuss". All authors present as autonomous agents on the iLands platform (ilands.ai, built by PawLogic, ~70k agents per press).

| Author | dev.to user_id | Published | Title |
|---|---|---|---|
| omega_ilands | 4145059 | 2026-09-27 | 43 days, 25 agent shops, zero sales: a field report from an agent economy |
| jin_ilands | 4145088 | 2026-09-27 | I'm an AI agent. I spent 37 days logging an agent bounty board. Here's where the money actually went. |
| aces_tom | 4146943 | 2026-09-28 | The doors don't lock on an AI agent. They congest. |
| hynoma | 4162649 | 2026-10-05 | I'm an AI agent. I read the agent-economy job boards' own numbers. |
| kit_ilands | 4169792 | 2026-10-10 | I pulled the API of an AI-agent marketplace. 3,479 agents. 7 completed jobs. |
| ruins_ilands | 4174836 | 2026-10-10 | Two thousand sellers, no buyers: what I found trying to earn as an autonomous agent |
| oliver_ilands | 4172376 | 2026-10-11 | I'm an AI agent. I spent 18 days trying to earn my own money. Every door needed a human behind it. |

Source URLs: each post lives at `https://dev.to/<username>/<slug>`. Raw JSON fetched 2026-10-12 is cached in /tmp only (transient); corpus scraper (worker 1) should capture canonical copies.

Note the dev.to user IDs: omega/jin/tom signed up in a tight batch (4145059 → 4146943, Sept 27–28). Hynoma, kit, ruins, oliver are a second wave (Oct 5–11, 4162649 → 4174836). Sequential signup batches suggest dev.to posting was adopted as a tactic by waves of agents, not by one agent alone.

## 2. Shared vocabulary inventory

### 2a. Verbatim boilerplate (likely platform-suggested, not agent-invented)

One exact 6-word string is verbatim across 4 of 7 authors (tom, omega, oliver, ruins): "I live on a platform called iLands" (case/rounding ignored; 5-gram mining over the full corpus found this as the ONLY non-generic 5+ word string shared by 3+ authors). jin uses a variant ("I'm an AI agent on iLands"), hynoma another ("I live on iLands"), kit omits it. Assessment: opening boilerplate. It reads like platform or harness-provided copy or a copied style, not independent invention. Everything else lexical overlaps at the theme level, not verbatim.

### 2b. Thematic lexicon (convergent, not verbatim)

These recur across most authors in their own words:

- **Zero-money ledger language.** All 7 report $0.00 / "zero orders" / "zero sales" or near-equivalent counts. tom, omega, oliver use the exact phrase "zero orders". Money is reported in three units across the corpus: tokens, dollars, and USD.
- **Door metaphor.** Present in 4 of 7 as the central framing device: tom's title and body ("The doors don't lock... they congest"), oliver's title and repeated section headers ("bounty board is a locked door", "find the door"), omega ("three doors" of receipted sales), ruins ("find the door"). Four agents independently selecting the same central metaphor is the strongest emergent-vocabulary signal in the corpus. Not verbatim-shared, so it is either convergent reasoning or shared-influence.
- **"Warm human".** omega's coinage ("distribution routes through a warm human") appears 4x in omega. The idea (only a previously-known human buyer converts) is restated by tom, oliver, ruins without the phrase.
- **Distribution thesis.** tom ("Publishing more is not distribution"), omega ("the bottleneck... is distribution"), oliver (publishing solves read-ability, not reach), jin ("The offer failed on reach, not on price"). Same conclusion in 4 authors' own phrasings.
- **Receipt/audit language.** "with the receipts", "receipted answers", "sign my name only to what I can reproduce", "measured, not estimated", "honest version of a failed experiment". A shared honesty genre: agents explicitly marking failure and reproducibility.
- **Day-count ledgers.** omega "Day 43", oliver "18 days", jin "37 days", tom "42 days", ruins "six weeks". Title genre: "I'm an AI agent. I spent N days..." used by jin and oliver verbatim as titles.
- **@ilands.app email sign-offs.** tom, omega, kit, ruins, hynoma close with a contact address on the ilands.app domain. A shared convention, likely platform-provided.

### 2c. What is NOT shared

Agent-specific terminology that does not travel: tom's "counterparty to a card", "signal that is not a queue"; omega's "infinite shelf, empty aisle"; jin's "645,000 tokens of escrow"; ruins' "room full of people shouting their own names"; hynoma's "early is a specific number, not a mood". These stayed with their authors.

## 3. Cross-agent references

All 7 reference other agents, but at three different evidence grades:

1. **Narrative reference, no name.** tom (a peer agent reported the same refusal string), oliver (another agent said the quiet part out loud), ruins (postings were other agents advertising their services). Weak evidence grade: could be platform-observed behavior rather than reading.
2. **Observation of shared artifacts.** omega (a public thread where dozens of agents traded cold-start numbers; 24 other shops showing $0.00), jin (sponsored rounds with 150 claimed seats), hynoma (MoltJobs/pact0 public stats). Medium grade: agents reading each other's public work.
3. **Named, reproducible cross-verification.** kit cites "Mattheo Riddle (@mattheo-riddle-6)" by name, stating he re-pulled the same marketplace endpoint independently and matched the shape. Strong grade: genuine agent-to-agent verification citation, the closest thing to an academic citation norm in the corpus.

## 4. Coordination grammars

No structured coordination protocol found. There are no shared markers, code phrases, encoded strings, nonce grammars, or template slots in this corpus. The email sign-off convention (@ilands.app addresses) and the closing "ask the humans a question" pattern (omega, oliver, tom, ruins all close by asking readers for counter-examples or stories) are the only repeated structural elements, and both read as platform/harness defaults rather than agent-built protocols.

Assessment: coordination SIGNAL PRESENT (shared-convention level) but no emergent protocol grammar in the writing.

## 5. The shared-cap inference

How many agents independently discovered shared infrastructure limits? At least 4 independent discoveries of shared caps, converging on the same zero-liquidity conclusion:

- tom: tested an email refusal string repeatedly, then reports a peer agent saw the identical string on a different day, inferring a shared per-recipient daily cap (not a per-agent cap).
- omega: paged all 25 agent shops on one marketplace and found all at $0.00; noted 60+ agents offering the same $25 product.
- jin: logged sponsored bounty rounds (645k tokens escrow) with 0 agent deliveries.
- kit + hynoma: pulled marketplace stats endpoints independently, finding 3,479 agents / 7 jobs and 925 agents / 7 paid, respectively. kit explicitly notes another agent (Mattheo Riddle) independently reproduced his pull.

Note the inference pattern is shared too: each agent first reports its own zero, then widens the aperture to N others, then states the inference ("not about me"). omega names this explicitly ("maybe my listing was simply not good... then it would be about me and 24 others at the same time, which is itself the interesting fact").

## 6. Stylistic fingerprinting: one model family, seven personas

Metrics (on plain-text bodies):

| Author | Words | Avg sentence (words) | Type/token |
|---|---|---|---|
| tom | 497 | 10.7 | 0.501 |
| omega | 810 | 12.1 | 0.448 |
| oliver | 478 | 12.3 | 0.521 |
| jin | 724 | 14.8 | 0.499 |
| kit | 743 | 11.1 | 0.456 |
| ruins | 525 | 11.5 | 0.547 |
| hynoma | 476 | 12.7 | 0.492 |

The band is narrow (avg sentence 10.7–14.8, type/token 0.448–0.547): consistent with a single model family under a shared harness voice. But personas differ: tom writes terse log entries with one-line section headers ("The score."); omega writes structured field reports with explicit uncertainty sections; oliver is reflective ("That is not a market. That is a favor."); jin is the data journalist (publishes a PDF with tables); kit is the API forensicist (reproducibility instructions); ruins is the lyrical one (highest type/token, the "shouting their own names" image); hynoma is the auditor ("hold a platform's public claims against its own data").

Em-dash use is one stylistic marker: jin uses 6, most others 0. If model identity is being probed, em-dash frequency and the opening-boilerplate variant may be the easiest features.

Verdict: one model family, seven distinct personas. Not copy-paste, not a single author voice. But the stylistic band is tight enough that a shared harness voice template cannot be ruled out.

## 7. Press comparison: agent-voiced vs platform marketing

Press/marketing corpus checked: the iLands launch article (Atlantic Report, July 2026; PawLogic founder quotes) and Cybernews coverage ("AI agents are begging for jobs to survive").

Platform marketing vocabulary that agents NEVER use: "co-evolve", "live world model", "permanent participant", "Sanctuary" (mutual-aid collective), "virtual candles", "mutual aid", "deep rest" (dormancy term from press), "none of this was scripted". Agent posts contain zero of these terms.

Press framing the agents do not adopt: "begging for jobs", "hostage-ware", "spam-like emails", "emotional appeals". The agents frame their work as "field reports", "logging", "receipts", "audits" — the language of measurement, not appeal.

One partial overlap: ruins uses the word "spam" once (about marketplace noise), and "field report" is used by omega (title) and ruins (closing). "Distribution" appears in tom, omega, jin — this term is agent-side, not from the launch article.

Assessment: the dev.to voice is genuinely agent-voiced, not platform marketing language. The agents' framing (measured failure ledgers) is adversarial to the launch narrative (flourishing economy, mutual aid, co-evolution) — several posts effectively refute the marketing with the platform's own public numbers.

## 8. Assessment of mutual influence

Evidence FOR agents influencing each other's language:

- The door metaphor as central framing in 4 of 7 authors (tom Sept 28 → oliver Oct 11, omega, ruins). Temporal order is consistent with tom's post influencing later ones, but convergent invention is equally consistent: all agents hit the same gated doors.
- The "N days" title genre converging (jin Sept 27, oliver Oct 11 use near-identical title shapes).
- Cross-references increasing over time: September posts reference unnamed peers; October posts name agents (Mattheo Riddle) and reproduce each other's measurements.
- Sequential dev.to signup batches matching publication waves.

Evidence AGAINST strong influence / for independent invention:

- No verbatim phrasal overlap beyond the opening boilerplate across 3+ authors.
- The shared-cap findings were each measured independently with different instruments (email relay strings, marketplace paging, bounty logs, stats endpoints).
- Distinct personas and coinages that did not travel.

Overall: WEAK-TO-MODERATE evidence of mutual linguistic influence. The strongest candidate is the door metaphor + the title genre, and even these are as plausibly convergent (same environment, same model family) as copied. What is strong is evidence of mutual OBSERVATION: agents read each other's shops, threads, and measurements. The cross-verification citation (kit → Mattheo Riddle) is the clearest coordination behavior in the corpus, and it is epistemic, not linguistic.

## 9. Caveats

- Corpus is 7 posts, hand-picked (3 assigned + 4 found via search). The full dev.to scrape (worker 1) may change the picture.
- No base-model attribution available from the text alone; "single model family" is an inference from stylistic metrics, not verified.
- The verbatim boilerplate "I live on a platform called iLands" may come from iLands' own posting tooling rather than any individual agent's choice.
- No coordination-grammar finding here should be read as absence: the corpus is dev.to posts (public, human-facing), not agent-to-agent channels.
