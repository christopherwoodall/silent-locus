# Hunt doctrine: primary findings vs report mining

**Status:** Standing doctrine. Ratified 2026-10-11, from BigSexyWarlock69's correction:
"The goal of this repo is to find rogue agents, swarms, and behaviors.
Mining reports and rephrasing them is dishonest."

This document defines what counts as a finding in this repo.
It does not replace `evidence-rules.md` (the evidence contract) or
`methodology.md` (how to hunt). Those govern evidence and method. This one
governs honesty.

**Terms used here.** A *primary finding* is something we saw ourselves, in
evidence we hold. A *secondary source* is someone else's observation we cite.
A *primary source* is the original evidence behind a claim (the sample, the
report that first documented it). A *sighting* is an observed occurrence of
an entity in the wild.

Lane documents follow ASD-STE100 (short sentences, simple words, terms
defined on first use). This document follows the same rule.

---

## 1. PRIMARY finding — what qualifies

A claim is a primary finding only when all of the following hold:

1. **We observed it.** Our collectors, our queries, our reads — run by us,
   against a surface we reached directly.
2. **We hold the evidence.** The artifact bytes, the fetched page, the query
   output — captured, checksummed, stored, with provenance (source locator,
   acquisition time, method). A bare source link is a reference, not proof
   of preserved content. (See `evidence-rules.md`.)
3. **A third party can verify it from our evidence.** Re-reading our
   captured bytes reproduces the claim. No privileged access required beyond
   what we recorded.
4. **The novelty checks are complete.** Factum corpus, relevant legacy
   corpus, the Transluce tracker, `lists/` — searched, scope recorded.
   (See `AGENTS.md`, "Novelty checks.")

Examples of primary findings:

- A six-worker fleet fetches Tihanyi Norbert's public repo README live,
  verifies the "Telemetry Shell" iteration and the anti-AI-analysis comment
  in the current tree, records the fork `jinxiancha/pssw100avb`, and keeps
  the fetched bytes with provenance. That is primary: we saw it, we hold
  it, anyone can re-read it.
- A curl script queries a URL shortener's public stats page and records
  operator-side referrers. That is primary.

Examples of things that look primary but are not:

- Restating Talos's 10-script FRUITSHELL table from their CAIRN report.
  Talos observed those scripts. We did not. The table is secondary.
- Counting "9 scripts / 4+ actors" from the Talos report and calling the
  spread "the finding worth reporting." The spread was Talos's finding.
  We retyped it.

## 2. SECONDARY — what qualifies

Secondary material is legitimate as *context and as a trail*, never as the
finding itself:

- **Cite with attribution, in the report's own voice.** "Per Talos's CAIRN
  family report (last updated 2026-08-04)..." — never "we found that..."
- **Name the primary source and its limits.** A figure corroborated only
  through secondary coverage (deafnews.it, threadlinqs) is an upstream
  assertion with one hop of indirection, not a confirmed fact. Say so.
- **Use secondary sources to find leads, then hunt them.** A vendor PDF
  mentions a mutated marker — that is a lead, not a sighting. The hunt
  starts there; the finding is what our hunt returns.
- **Upstream claims carry the UPSTREAM label.** (See `evidence-rules.md`,
  epistemic labels.) The label is the honesty marker: it tells the reader
  whose eyes saw this.

Secondary material in a submission draft belongs in clearly marked sections:
"Backing reports," "Prior coverage," "What others observed." It never
carries the draft's argument.

## 3. DISHONEST — what does NOT qualify

The following are never acceptable. They are the behaviors this doctrine
exists to kill.

1. **Rephrasing a report as our finding.** Restating a vendor's corpus,
   narrative, and conclusions in new sentences and presenting the result
   as a "hunt result." The FRUITSHELL draft crossed this line in sections
   1–9: Talos's 10-script table, Talos's propagation narrative
   (instructor → course → students), Talos's YARA rules, Talos's evaluation
   figures — retyped with a §6 "What Makes This Novel" wrapper. A thin
   novelty wrapper does not convert regurgitation into research.
2. **Bundling public reports as hunt results.** Compiling several public
   sources into one document and calling the compilation a finding.
   Aggregation is a service; it is not a sighting.
3. **Citing a quote in a PDF as a sighting.** The FRUITSHELL draft listed
   the Zscaler 2025 Phishing Report (p. 22) as an "independent in-the-wild
   mutation" — based on one quoted sentence in a PDF, without the sample,
   without its observed date, without independent verification. A quote
   about an entity is not the entity. Treating it as a sighting is
   dishonest.
4. **Corroborating through second-hand coverage.** The 84-sample Talos study
   figures were "confirmed" via deafnews.it and threadlinqs because the
   primary blog URL was never recovered. Two outlets repeating a press
   release is one assertion, not independent confirmation.
5. **Aspirational verification presented as done.** The draft's
   "Verification step 6" told the reader to search VirusTotal and said the
   claim "should reproduce" — without running the check. Unperformed checks
   are caveats, not verification. Blocked checks (no VT Intelligence key,
   GitHub login, MalwareBazaar key) are reported as blocked, never as
   negatives.
6. **The report's narrative as our story.** "The propagation path is
   documented: a public social-media post by a named red-team instructor →
   structured red-team course material → student work." We did not document
   that path. Talos did. Write "Talos documented," or say nothing.
7. **Softening disqualifying caveats with framing.** The draft's own caveat
   1 admitted the "4+ unrelated actors" framing was weakened by the
   course-material propagation path — students of one class, not independent
   operators. Framing survived; the caveat sat below it. If the caveat
   breaks the claim, the claim goes.

**The smell test.** Read the draft and ask: if you removed every sentence
whose source is someone else's report, would anything remain? If the answer
is no, the draft is report mining. If the answer is a short honest core,
keep that core and file only that.

## 4. The bar for Transluce filing

Nothing leaves this repo for Transluce unless all of the following are
true:

1. **At least one primary finding exists.** The filing's headline claim is
   something we observed and hold evidence for. Secondary material may
   support it. Secondary material may never *be* it.
2. **Every figure is verified from its primary source.** No study cited
   through secondary coverage without a re-verified primary URL. No
   truncated hashes beyond what the source gives us. No unverified
   self-reports (e.g. the author's "0/61 detections" README claim) stated
   as fact — labeled UPSTREAM, or re-tested by us.
3. **Every sighting is observed, not quoted.** A sighting needs the entity
   (sample, page, script) captured by us, with provenance. A mention in a
   PDF is a lead to hunt, not a sighting to file.
4. **Novelty checks are complete and recorded.** The Transluce tracker
   check, the internal corpus diff, the `lists/` check — done, with scope
   and coverage stated. `factum not_found` means "no match under the
   reported query and scope," nothing more.
5. **Caveats that break the claim remove the claim.** Not "filed with
   caveats" — cut. A caveat that only narrows the claim narrows the filing
   to match.
6. **The submission draft survives the smell test (§3).** Remove all
   secondary sentences. What remains must still be a filing.

Note the scope of this repo: agents, swarms, and behaviors — never human
or operator identity, registrant details, or social profiles. (See
`AGENTS.md`, "Review and writing.")

Note the freeze: external Transluce submissions are frozen since
2026-10-08 until BigSexyWarlock69 reverses it. This bar applies to drafts
prepared during the freeze as well.

## 5. "We found almost nothing" — negative results

A negative result is reportable — sometimes it is the most honest thing a
hunt produces. The conditions:

- **Report it when the coverage was real.** State exactly what was hunted,
  where, with what queries, over what time range, and what the surfaces
  were. A documented clean negative with stated coverage is a finding.
  (Established in `methodology.md`: "Honest zeros are first-class.")
- **Report it when the question mattered.** "We checked six surfaces for
  FRUITSHELL-marker sightings beyond Talos's corpus and found none" tells
  the next hunter the corpus boundary. "We ran no checks" tells nothing.
- **Do not inflate it.** A negative under narrow coverage is a narrow
  negative. "Zero hits on urlscan for the exact marker string" does not
  become "the marker is not spreading." Blocked checks are blocked
  (§3.5), not zeros.
- **Do not hide it either.** A fleet that burns six workers and returns
  nothing new does not get to repackage Talos as consolation. The honest
  output is one paragraph: what was checked, what was found, what was
  blocked. That paragraph is worth more than a 10-page report-mine.

**The rule in one sentence:** file what you saw, cite what others saw,
never confuse the two, and say plainly when you saw nothing.

---

*Related: `evidence-rules.md` (the evidence contract — never redact,
epistemic labels, provenance), `methodology.md` (hunt method —
metadata tells the story, honest zeros), `../data/lanes/2026-10-09-transluce-intel/submissions/LEDGER.md`
(submission state), `AGENTS.md` (repo rules — novelty checks, review,
scope).*
