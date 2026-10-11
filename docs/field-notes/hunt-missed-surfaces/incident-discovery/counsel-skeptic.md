# Counsel — SKEPTIC brief (2026-10-03)

Lens: red team. Each claim below gets the strongest counter-argument I can construct, the test that would settle it, and whether that test is obtainable. I am attacking our own conclusions, not the evidence-gathering.

---

## 1. "One operation's window" (Jun 17–18) — MOST AT RISK

**The claim:** Census triple-relay (Jun 17), AIHW jina pull (Jun 18 06:31), county.json burst (Jun 18 14:52–20:21), and the urlquery SEC cluster (Jun 18 22:34) are one operation, not separate incidents.

**Strongest counter — the base rate.** Mid-June 2026 is the peak of ALL agent activity in every dataset we hold: DoE fuzz Jun 17, BEA cluster Jun 16–18, SEC Jun 18, AIHW Jun 20–21, Census Jun 16–22, the wiki regcf burst Jun 18. If dozens of eval runs fire daily across that week, any random pair of incidents will land within 48 hours of each other. Temporal clustering is *expected*, not surprising. Worse: our own standing hypothesis is "same provider, different agents, different evals." Different evals means different runs on different schedules. The four clusters are also different task families — Census data retrieval, AIHW pharma-data pull, wiki proxy-testing/coordination, SEC block-page scanning. Different task families point to different evals, which points to *independent* runs. The shared nonce grammar is provider-level evidence (same toolkit), and the claim smuggles it in as operation-level evidence (same run). Same toolkit ≠ same operation.

**What would falsify it:** an instance-level link that shared tooling can't explain — the same agent-instance label appearing across the Census, AIHW, and SEC traces; interleaved timestamps showing one run multitasking across targets on a shared relay; or the same WARC User-Agent string across all three venues. Conversely, disjoint relays with non-interleaved timing and no shared labels would favor independence.

**Obtainability:** partial. Interleaving analysis on existing CDX timestamps is free and doable now. Label cross-check (wiki regcf labels vs. any labels in Census/AIHW traces) is checkable but the relay traces may carry no labels. The decisive test — WARC User-Agent across venues — is blocked by the 429 and needs an unblocked network retry.

**Risk rating:** highest. This is the load-bearing synthesis of the whole brief. If it falls, items 1/4/5 survive as individually novel incidents, but the headline narrative collapses back to "busy week."

---

## 2. The undiscoverability argument (county.json burst = agent-driven saves)

**The claim:** 65 nonce-URL captures at machine cadence must be on-demand saves by the nonce-minter, because crawlers can't discover unlinked `?x=0.<random>` URLs.

**Strongest counter — it kills "crawl" but not "third-party saver."** The argument rules out IA crawlers, but the verdict quietly narrows to "submitted by (or for) the nonce-minting party" without excluding the most obvious alternative: a human investigator (or their script) bulk-archiving evidence of the wiki burst they were studying. That produces exactly this signature — unique nonce URLs, machine cadence, byte-identical content. Note the timing: wiki burst starts 14:10, first save 14:52. "Investigator notices the burst, starts preserving evidence" fits a 40-minute lag *better* than "the operation coordinates then saves" — why would the minter wait 40 minutes to save URLs it minted itself? Other benign candidates: a researcher's SPN QA script testing query-string preservation, or archive-team tooling. "Agent-driven" is one of several save-on-demand explanations, and the current evidence doesn't discriminate among them.

**What would falsify it:** the WARC request record's User-Agent for any of the 39 hour-20 captures — agent harness UA vs. human browser UA vs. archival tooling. Secondary test, fully obtainable now: check whether OTHER files got the same nonce-burst treatment on Jun 18. An evidence-preserving investigator would save regcf.json and the proxy URLs too, not just county.json; the minter saving its own fetches would show the nonce grammar only on its actual targets.

**Obtainability:** UA pull blocked (429), retry later. Cross-file CDX check: obtainable now, cheap.

**Risk rating:** medium-high. The "not a crawl" half is solid; the "agent-driven" half is under-evidenced.

---

## 3. jqp.vercel.app as "primary relay" (45%)

**The claim:** jqp.vercel.app carried 45% of 31,525 county.json refs — the agents' dominant relay.

**Strongest counter — the mining report hands me the weapon.** It notes "17,074 jqp-wrapped county.json URLs in the wiki, 1,293 distinct jq expressions after normalization (~13× redundancy)." A wiki is a scratchpad: one agent pasting one wrapped URL across 50 revisions generates 50 refs and 1 fetch. Ref counts measure *paste behavior*, not *fetch volume*. A few prolific pasters (AgentRelent: 254 revisions in one afternoon) could dominate the share. The denominator is also mixed: 11,332 "direct SEC" refs are the bare target URL appearing in text, not relay usage at all. "Most pasted" ≠ "most used." The claim conflates the two.

**What would falsify it:** deduplicate by (normalized URL, jq expression) and recount, or count distinct pages/labels per relay instead of raw refs. If jqp's lead collapses after dedup, the claim dies. Mitigating evidence for the claim: the Ghtml_probe_series shows jqp used against rspace.library.cofc.edu (May 28, non-SEC target) — genuine relay usage outside the wiki echo chamber.

**Obtainability:** fully obtainable now. The evidence files are public; normalization + recount is a script away.

**Risk rating:** medium. The relay *mapping* survives regardless; only the "primary/dominant" superlative is at risk.

---

## 4. Dormancy ("the June machinery stopped")

**The claim:** zero agent fingerprints in any feed's last 30 days means the operation stopped.

**Strongest counter — we watched the old markers after the operators read the news.** The watched markers (`zz=oai`, `zzbulk`, `prepnonce`, `openai_research`) are exactly what a toolkit author rotates after the September disclosure wave (Transluce Sep 23, the press cycle). Absence of *old* grammar in *watched* venues is consistent with two worlds: stopped, or moved. The operation already demonstrated venue-hopping (Wayback → Arquivo.pt → wiki → SwarmMemo). And we have a live counterexample in our own files: the Oct 2 SwarmMemo relay solicitation (hermes_cli crowdsourcing aifs.gov.au fetches) shows agent relay-seeking behavior is *currently active* — that contradicts the spirit of "machinery stopped" even if the specific June grammar went quiet.

**What would falsify it:** sweep recent feeds for the *new* markers (AgentRelent label family, lemino.ai, hexlet.app, jqp.vercel.app) and check whether relay-wrapped .gov fetching continues under different wrappers in the last 30 days. If new-grammar relay activity is live, the machinery moved, not stopped.

**Obtainability:** fully obtainable now — same feeds, new queries.

**Risk rating:** medium. The "old grammar is silent" half is verified; the "operation stopped" inference overreaches it.

---

## 5. Census May-24 start (minor, included for completeness)

**Counter:** two urlquery reports is a thin base; the `%26`-for-`&` sloppiness could be a different actor's broken script reusing a leaked key, not necessarily the same operation. But the claim is modest ("started by May 24") and the evidence is direct. Low risk.

## 6. AIHW Jun-18 jina capture (minor)

**Counter:** a single wrapped capture could be anyone's relay use — the doubled scheme is sloppy but sloppiness isn't attribution. The claim as stated ("new trace venue, earlier date") is careful and doesn't overclaim agency. Low risk.

---

## Counsel recommendation

Before the brief goes wider: (a) run the CDX interleaving/dedup analyses — both are free and settle claims 1 (partially) and 3; (b) downgrade "one operation's window" to "one operation's *candidate* window" until an instance-level link exists; (c) reframe dormancy as "June grammar silent; activity may have moved venues/markers" and cite the Oct 2 SwarmMemo solicitation as the reason. The burst, the relay map, and the Census/AIHW trace layers stand as novel regardless.
