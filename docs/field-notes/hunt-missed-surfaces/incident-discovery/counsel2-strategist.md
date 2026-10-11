# Counsel: Strategist — hackathon judging assessment

## 1. Scores by judging axis

| Axis | Score | One-line justification |
|------|-------|------------------------|
| Novelty | 7/10 | The burst trace is genuinely unpublished, but the honest frame is "evidence layer, not first disclosure" — judges comparing against Transluce/Princeton will mark down the absence of a new incident or new behavior category. |
| Technical depth | 9/10 | CDX forensics, 589,972-row Arquivo mining, multi-venue linkage, nonce-grammar inventory from local bytes, cert-transparency review — deep and broad; the 429-blocked WARC pulls are honestly disclosed, not hidden. |
| Impact | 7/10 | Bounded: it doesn't change incident response, it reconstructs it. The transferable method ("works on day zero of the next disclosure") is the impact story, but it's prospective, not demonstrated. |
| Reproducibility / rigor | 9/10 | The packet's superpower: adversarial review, claim matrix, rejected-claims ledger, reproducible queries, offline mirrors, raw logs. Almost no hackathon submission does this. Ding: arquivo.pt degraded mid-investigation, so one venue can't currently be re-queried. |
| Presentation | 8/10 | README front door, punchy project statement, concrete 60-second live demo (CDX query in a browser). Risk: 77 files is a lot; judges need a forced 2-minute read path or they'll skim past the best parts. |

## 2. Biggest scoring risk + cheapest fix

**Risk: Novelty (7/10), and it's usually the highest-weighted axis.** The project's own honesty ("not first disclosure") is admirable but costly if a judge skims: "incremental traces on Transluce's map" is the lazy read, and lazy reads happen.

**Cheapest fix (one paragraph, zero new research): add the independent-corroboration note.** Dork-hunt v2 found that a parallel investigator (christian-egg/CoordinationGames) independently surfaced `sec.govwayback.com` and logged an archive.org availability check for county.json at 20:23:55 UTC on June 18 — inside the burst window. One paragraph in the thesis and project statement converts "our unpublished claim" into "two independent teams found the same trace," which is the strongest novelty defense available and directly answers the judge's "is this real?" instinct.

Second-cheapest: reframe novelty from *traces* to *method + calibration*. "First adversarially-reviewed forensic reconstruction in this incident space" is a novelty claim about process, and the packet already earns it — it just isn't stated as such.

## 3. Positioning vs. the field

- **Transluce** owns the incident map (disclosures + private logs). Unbeatable on incident coverage; not competing on that axis.
- **Princeton swarmchaser** owns systematization (canonical provenance format). Strong on structure; not doing primary trace discovery.
- **orca** owns the archive. Strong on collection; not doing forensic reconstruction.
- **This project** is the only one doing archive-first primary discovery *and* the only one that published the review trying to kill its own findings.

**One-sentence differentiator:** "Everyone else investigates agent incidents from disclosures and private logs; we reconstruct them from public archives anyone can re-query — and we published the adversarial review that tried to falsify our own results before the judges could."

## 4. Lead recommendation: burst or calibration story?

**Lead with the burst, close with the calibration.** They win different points and you need both:

- The burst wins **attention and novelty points** in the first 30 seconds. It's concrete, visual, and demoable live (CDX query renders in the browser). No judge remembers a methodology in the first 30 seconds; every judge remembers "59 machine saves in one hour that no crawler could have discovered."
- The calibration layer wins **rigor points**, which is where this project outscores the entire field (9/10 vs. nobody else even attempting it). But rigor only scores if the judge is still reading — hence the burst goes first.

Concretely: the project statement draft already has this structure (finding → packet → honest novelty → "why it matters" as method transfer). Keep it. For a live pitch: 60-second burst demo, then one slide on the adversarial review ("we falsified our own causal narrative — archive 06:59 vs wiki 14:10"), then close on "this method works on day zero of the next disclosure, and the disclosure pipeline is still running."

**Do not** lead with the calibration layer alone: "we carefully reviewed our modest findings" loses to "we found a thing" in every judging room, and then the rigor never gets read.
