# Presentation counsel — how to win with this packet

Lens: legibility and impact. The packet's strength is epistemic architecture; the pitch's job is to make that architecture *felt* in 3 minutes.

---

## 1. Narrative arc for a 3-minute pitch (~430 spoken words)

**Order: mystery → evidence → self-destruction → what survived → method.**

| Time | Beat | Script shape |
|------|------|--------------|
| 0:00–0:30 | **Hook (the anomaly)** | "On June 18th, someone saved the same SEC data file 59 times in fourteen hours — every save carrying a random nonce in the URL that no crawler could ever discover. Nobody has published this." Concrete, strange, verifiable. Do not mention agents yet. |
| 0:30–1:15 | **Evidence (the burst)** | Nonce grammar, 39 saves in one hour, 61 byte-identical digests. The undiscoverability argument in one sentence: "A crawler cannot save a URL it was never given." Show the burst histogram. Name the toolkit-level association — and stop there. |
| 1:15–1:50 | **The turn (emotional beat)** | "We thought the wiki coordinated it. Then we ran a hostile review against our own findings — and the data killed our best story. The archive came first, by seven hours. Different files. We published the falsification." **This is the beat.** Vulnerability as credibility. Pause after "seven hours." |
| 1:50–2:20 | **What survived** | Timeline extensions (Census to May 24, AIHW two days early), the relay census with the unit correction stated proudly ("most-pasted, not most-used — and we're glad we caught it"). One line each. The message: the exciting thing didn't evaporate; it became a forensic result. |
| 2:20–2:50 | **The method transfers** | "Everything here came from public archives — no private logs, no insider access. The 3,821-term fingerprint dictionary and the CDX queries are in the packet. Anyone can rerun this on the next incident before the next disclosure." |
| 2:50–3:00 | **Close (open questions as strength)** | "Here's what would change our minds — one interleaved relay timestamp, one response body, one restored archive collection. The packet tells you exactly what we can't claim." End on the rejected-claims ledger, not the findings. |

**What to cut for time:** NSW NPWS (press-covered, our sweep was clean — side quest); dormancy beyond one clause ("we state what the feeds can't prove"); skill ladders (one line max); the wbdisable correction (lovely, but a footnote); LAC entirely. If it doesn't serve the burst → falsification → calibration spine, it goes.

**Where the emotional beat lands:** at 1:15–1:50, the self-falsification. Hackathon judges have seen a hundred "look what we found" pitches. Nobody pitches "look what we proved ourselves wrong about." That beat is the differentiator — it converts the packet's architecture from a document feature into a felt experience.

---

## 2. The 60-second demo: keep the three-act structure, change the medium

The draft's three acts are right (burst renders → digest concentration → falsified narrative), but **do not run the CDX query live.** We were 429-blocked by web.archive.org during the investigation; a live demo depending on it is a coin flip. Instead:

1. **(0:00–0:20) Pre-rendered burst histogram** on screen, with the live CDX query URL printed beneath it: "Here's the query — run it yourself later. Here's what it returned." Reproducibility without demo risk.
2. **(0:20–0:35) The digest line**, big type: `61 of 65 byte-identical` + the digest hash. Then the nonce sample `?x=0.06529146573970845` — "no human typed this."
3. **(0:35–0:60) The falsification slide**: two timestamps, `archive 06:59 UTC` vs `wiki 14:10 UTC`, with the causal arrow crossed out in red. "Our review killed our story. We kept the data."

**Better 60-second moment considered and rejected:** the doubled `http://https://` in the archive index is visceral and funny ("the agent's typo, preserved forever") — great for a general audience, but it's a supporting detail, not the core finding. Use it only if a judge asks for color, or as the one-liner while the histogram loads. The digest concentration is the stronger punch because it's quantitative.

**Demo golden rule:** every live element must have a pre-rendered fallback visible within 5 seconds. Nothing in the 60 seconds should depend on a network call you haven't made in the last hour.

---

## 3. Missing visuals — build these four, from these files

| # | Visual | Data source | Spec |
|---|--------|-------------|------|
| 1 | **Burst histogram** (captures/hour, Jun 18) | `wayback-cdx-sweep/data/in-window-captures.jsonl` → filter `timestamp` startswith `20260618`, bin by hour | The single most persuasive visual. X: hour UTC, Y: saves. Annotate the 20:00 spike (39) and the 06:59 start. |
| 2 | **Timeline strip** (Jun 17–18) | Thesis §1, §2, §5 | One axis: Census triple-relay (Jun 17 ~02:59) → AIHW Jina (06:31) → burst start (06:59) → wiki regcf start (14:10) → burst peak (20:00) → urlquery cluster (22:34). Draw the wiki→archive causal arrow **crossed out in red** with "falsified by primary data." This one image tells the whole calibration story. |
| 3 | **Relay bar chart** | `incident-discovery/joshuadavid-mining.md` ref table | Bars: jqp 14,341 / allorigins.win / hexlet.app 4,928 / cors.lol 480 / lemino.ai. **Label the unit on the chart itself:** "raw wiki-text URL instances — textual recurrence, not network volume." The caveat on the visual is the credibility move. |
| 4 | **Claim disposition badges** | `adversarial-review-2026-10-03.md` §17 | Six claims, each with a badge: survives / narrowed / demoted / rejected. This is the "calibration layer" made glanceable — judges photograph this slide. |

Build as static PNG/SVG (no live dependencies). Dark background suits the venue; keep type large enough to read from the back row.

**Packet hygiene before circulation:** `claim-matrix-2026-10-03.md` still contains pre-review wording ("65-capture," "45%," "40 minutes before," "retrieval succeeded"). Either regenerate it from the thesis or add a one-line errata header pointing to the adversarial review. A judge who cross-reads will find the inconsistency.

---

## 4. The "calibration layer" framing: winning, if phrased as a weapon

**Verdict: it's a winning frame — but only if presented as method, not modesty.** "Calibration layer" cold reads academic and defensive. The frame wins because hackathon judges have a specific fatigue: a hundred "we found the hidden thing" pitches, zero "here's how we know, and here's what we couldn't prove" pitches. Falsifiability is memorable. But the ratio matters: **~70% findings, ~30% calibration.** Lead with the burst (strong), close with the calibration (trust). If calibration eats half the pitch, it reads as "our findings are weak."

**Phrasing for maximum strength:**

- Don't say: "we're being careful / humble / cautious."
- Say: **"We ran a 20-section hostile review against our own findings and published what it killed."**
- Don't say: "calibration layer" without grounding.
- Say: **"Every claim ships with its kill conditions — the exact evidence that would prove us wrong."**
- The one-liner: **"We don't just show you what we found. We show you what we tried to claim and couldn't."**
- Frame the rejected-claims ledger as a *deliverable*, not an appendix: "Five claims went in. Here's the one that died, and the data that killed it."

**What to avoid:** the bots' charming line "the little machine has grown a conscience" — keep it out of the pitch. One human moment (the falsification beat) is enough; two becomes shtick. Also avoid "epistemic architecture" in speech — it's a document word. In speech, say "we show our work, including the parts where we were wrong."

**The close that wins:** end on the open questions, not the findings. "One interleaved relay timestamp would promote our operation claim. One response body would settle retrieval. We're telling you exactly what we're missing." Judges remember the team that handed them the falsification kit.

---

## Counsel's adversarial note (as requested)

The biggest presentation risk is **burying the burst under the calibration.** The packet's architecture is the differentiator, but the burst is the reason anyone cares. If the pitch spends 90 seconds on methodology before showing the anomaly, judges will mentally file it as "process project" and stop listening. The anomaly must land in the first 30 seconds — calibration earns trust, but only after curiosity exists. Second risk: the "59 vs 65" denominator distinction is credibility gold in the document but death in speech — say "59 saves" once, put the denominator footnote on the slide, never explain it aloud unless asked.
