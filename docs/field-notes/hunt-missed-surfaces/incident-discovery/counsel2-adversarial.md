# Counsel 2 — adversarial member: hostile grader review of the submission package

Posture: hostile to the pitch, friendly to the evidence. Every objection below is something a skeptical grader could actually say out loud. Ranked by damage potential.

---

## Objection 1 (HIGHEST DAMAGE): The project statement re-smuggles the attribution the thesis removed

The thesis title was carefully recalibrated to "incidents associated with agent activity." The project statement — the first thing a grader reads — opens with:

> "A forensic trace layer for the June 2026 **AI-agent incidents**"

and later asserts, without the thesis's novelty boundary:

> "**No investigator has published this trace.**"

and states as flat fact:

> "59 **machine-mediated** on-demand saves"

A hostile grader will quote the statement against the thesis: *"Your own thesis says the initiating actor is unestablished and your novelty claim is bounded to a search universe as of 2026-10-03. Your pitch says 'AI-agent incidents,' 'machine-mediated' as fact, and 'no investigator has published this trace' as a universal. Which document should I believe?"* This single inconsistency can collapse the credibility architecture the entire packet is built on.

**Fix:** Apply the thesis wording to the statement verbatim. Line 1 → "the June 2026 incidents associated with agent activity." Add the novelty-boundary sentence after "No investigator has published this trace" (or demote to "no prior publication found in the searched sources"). Qualify "machine-mediated" the way §1 of the thesis does, or use the ladder-exact term "on-demand saves."

## Objection 2: The 60-second demo script disagrees with its own query output

Demo step 1: *"Open the CDX query — 59 nonce-burst saves render in the browser."*

The query (`collapse=urlkey`) returns **65 rows (63 collapsed urlkeys)**, not 59. The "59" is the review's corrected count after filtering 2 revisit records + 4 background 404s — a distinction that exists only in our analysis, not in the rendered output. A grader counting rows on screen sees 63 and concludes we can't count our own evidence.

**Fix:** Rewrite the demo step to *perform* the correction live — it becomes the strongest 10 seconds of the pitch: "65 rows render. Our adversarial review showed 59 are genuine saves — 2 are archive revisits, 4 are background 404s. Watch us apply our own correction." This turns a row-count mismatch into a demonstration of the calibration layer.

## Objection 3: The live demo can fail, and our own notes say so

The nonce-sweep notes document CDX 504s on large hosts and the warc-verification worker hit 429s on web.archive.org. A live CDX query on stage is a single point of failure in a 60-second demo.

**Fix:** Bundle a static rendered HTML table of the 65 rows (we already have `in-window-captures.jsonl`) as the demo fallback, and say so in the statement: "live query, with a frozen render as backup." Graders respect a presenter who names their failure mode before it happens.

## Objection 4: The thesis title still asserts a Level-2 inference as fact

"an unpublished, **machine-mediated** archive trace layer" — "machine-mediated" is the L2 inference the body carefully defends, but the title states it without the ladder. The bots flagged "hypothesis-independent" as inviting pedantry; "machine-mediated" in the title invites the same pedant through a different door.

**Fix (minor):** "an unpublished **on-demand-save** trace layer" matches the claim-strength ladder exactly (L2 = on-demand saves, high confidence) and is *more* precise, not weaker. Alternatively keep "machine-mediated" — §1's defense is solid — but then the title and §1 must use the identical term, which they currently don't ("machine-mediated" vs "on-demand saves").

## Objection 5: The novelty claim's search universe is enumerated nowhere the grader looks

The thesis says "Searched sources found no prior publication" and appends the boundary sentence — good. But the *universe* (both Transluce reports full-text, web news/investigator search) lives only in the adversarial review's §1. A grader asking "searched *what*, exactly?" has to dig through three documents.

**Fix:** Inline the universe into the thesis novelty line: "no prior publication found across both Transluce reports (full-text), news verticals, investigator blogs/repos, and targeted web search as of 2026-10-03."

## Objection 6: The 41/8 nonce split is not re-derivable from the packaged evidence

Thesis §1: "41 carry `?x=0.<17-digit>`; 8 carry `?0.<16-digit>`." The packaged `in-window-captures.jsonl` holds query-*keys*, not query strings — a reproducer cannot verify the 41/8 split from the packet. The adversarial review flags this in its reproducibility appendix, but the thesis presents the numbers without the caveat.

**Fix:** Footnote in the thesis: "per-family counts per SWEEP-REPORT.md enumeration; packaged JSONL preserves query-keys." One sentence; closes the reproducibility gap a hostile grader would otherwise drive through.

## Objection 7: "Transfers to the next incident" is unproven generality

Project statement: *"The method (archive-first forensics + adversarial self-review) transfers to the next incident before the next disclosure."* We have run this method exactly once, on one incident family. A skeptic calls this marketing.

**Fix:** Soften to "is designed to transfer" or "we are now testing transfer to the next disclosure." One word change; removes a free attack surface.

## Objection 8: The packet buries one of its best preservation claims

Our October 1 Arquivo.pt pull (589,972 captures) may now be the **only accessible copy** of the on-demand-save collections — the venue degraded October 1–3. That is a genuine preservation contribution and it appears nowhere in the project statement. A grader will not credit what we don't claim.

**Fix:** One line in "What else is in the packet": "includes an October 1 snapshot of Arquivo.pt's on-demand-save collections, which stopped serving two days later — possibly the only accessible copy."

## Objection 9: Terminology drift across the packet

The thesis uses "evidence-bearing core"; the adversarial review (§20) still says "hypothesis-independent core." A pedant grader *will* find both and ask which is operative.

**Fix (trivial):** Align the review doc's §20 to "evidence-bearing core," or add a one-line note that the terms are synonymous. Do it before circulation, not after someone asks.

## Objection 10 (EXISTENTIAL): "So what? Someone saved a public file 59 times."

The most likely dismissal reason isn't a wording slip — it's this: *nothing was breached, no retrieval proven, no agent identified, no operation established. This is an elaborate writeup of a cache-busting artifact.*

The defense exists but the statement doesn't lead with it. The bots' final paragraph names the real contribution: **a calibration layer** — a worked example of investigating agent activity without collapsing association into attribution, adjacency into coordination, or silence into cessation. The current "Why it matters" ("anyone with an internet connection") is true but generic; it answers *how*, not *why a grader should care*.

**Fix:** Open "Why it matters" with the calibration framing: "The artifact that matters most here may not be the burst — it's the method: an evidence-graded, adversarially-reviewed template for agent-incident forensics that survives hostile reading." Then keep the reproducibility sentence. Make the grader evaluate the *method*, and the burst becomes the demonstration instead of the whole bet.

---

## Verdict

Nothing here is fatal. Objections 1–3 are the ones that could actually cost points with a hostile grader; 4–9 are polish; 10 is the framing fight the statement should win in its first 30 seconds. The evidence survives all ten — which is exactly the point the packet is trying to make.
