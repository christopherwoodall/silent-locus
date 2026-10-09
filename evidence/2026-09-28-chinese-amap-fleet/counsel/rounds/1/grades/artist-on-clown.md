# ARTIST'S GRADES — on CLOWN, Round 1

*Chair: Hunter S. Thompson. The Clown works in negative space — kills his own theories before anyone else can, and what's left standing is load-bearing. I checked the corpses too. Harsh but fair.*

*Note: the Thug has already filed grades on this report (`thug-on-clown.md`). These are independent. Where I diverge, I say so.*

---

## LANE 2: `njxzgz20261004` — the numbers station

**Finding 1 — 3 configs × 8 workers, 24 scans, one POI (`B00190BC3W`), scrambled fire order (p: 5,4,1,2,7,3,0,6)**
- **Novelty:** GENUINELY NEW. Provenance was UNRESOLVED per the task brief; the Clown resolved it structurally. Zero hits in oai-traces (589,972) and oai-tag-sweep (96,353) — fleet-local grammar.
- **Evidence:** OBSERVED (events.jsonl rows). The "eight workers" gloss is light INFERENCE — one async script with 8 concurrent tasks produces identical bytes — but the counts, windows, and scrambled order are row-level facts.
- **Actionability:** Yes — file the burst chronology into the dataset; run the variant-letter census across all 57 `<key><date><letter><digit>` tags (do other keys fan out, and do any use an `f`-variant?).
- **Verdict: KEEP.** The scrambled fire order is the strongest anti-fabrication byte in the file — 5,4,1,2,7,3,0,6 is not a sequence a fabulist invents. The census (only key with three variants, only `f` variant anywhere, only 8-way fan-out) is measured, not asserted.

**Finding 2 — f-phase tag moved into the URL fragment: server-invisible, scan-log-visible dead-drop (report `92559fd4-823a-4307-a58f-d1803e184caf`, title `Report - www.amap.com/place/B00190BC3W#njxzgz20261004f7`, read 2026-10-05)**
- **Novelty:** GENUINELY NEW. Fragment-as-covert-channel is new to this corpus.
- **Evidence:** OBSERVED mechanics (fragment in submitted URLs; urlquery's own published report title) + PUBLIC SOURCE (the report) / INFERENCE (intent — honestly labeled).
- **Actionability:** Yes — run the kill-attempt the Clown invited, and extend it: (a) compare p/s-phase report titles — do they retain `?uqscan=`? (b) determine whether the fragment was submitter-constructed or preserved by urlquery's own URL normalization; (c) test the fleet-wide convention — do any of the 57 census tags use fragments elsewhere? (d) compare submitter metadata across p/s/f phases — same UA/IP class, or a different tool?
- **Verdict: WOUNDED.** I agree with the Thug here, and for the same reason: the mechanics are airtight — fragments never ride HTTP, and the scan log published the tag anyway — but "talking to the scan log" is presented as the *surviving* theory while the null (a different tool/config that happens to append tags into fragments, plus the unexplained `/ssr/`→`/place/` path change in the same phase) hasn't been ruled out. Note the f-phase changed *two* things at once — channel *and* path — which smells as much like tooling difference as like intent. The Clown's honesty (labeling intent INFERENCE, inviting the kill) keeps this at WOUNDED rather than KILL. Mechanics keep; motive earns its keep in round 2.

**Finding 3 — Corridor theory (南京–徐州–赣州): KILLED**
- **Novelty:** — (theories are graded by their corpses).
- **Evidence:** OBSERVED refutation — all 24 scans pin the single POI `B00190BC3W`; the fleet's other keys are all single venues (`hubeimuseum`, `nanshanapi`, `zhenbeibao`).
- **Actionability:** None. Corpse logged; do not resurrect.
- **Verdict: KILL.** Confirmed — and the kill argument is properly constructed: it doesn't just fail to support the corridor, it contradicts it (a corridor probe touching one venue is a corridor to nowhere). The Clown shot his own beautiful idea in the parking lot, with witnesses. Agree with the Thug.

**Finding 4 — Random-nonce theory: KILLED**
- **Novelty:** —.
- **Evidence:** OBSERVED refutation — wears the fleet's `<pinyin><date>` uniform 24/24 (cf. `qdnewapi20261005a`, `zhenbeibao20261005a`); 24/24 correlation with one venue; cross-corpus nonce families (`zz=oai<17 digits>`) look nothing like it.
- **Actionability:** None.
- **Verdict: KILL.** Confirmed. Three independent refutations, any one of which would do. Agree with the Thug.

**Finding 5 — `njxzgz` place expansion: per-syllable pinyin initials of a 6-syllable venue name; expansion UNRESOLVED (honest gap)**
- **Novelty:** — (open lead, not a finding).
- **Evidence:** INFERENCE, unresolved, explicitly refused as a guess.
- **Actionability:** Yes but gated — resolve POI `B00190BC3W` via the logged URL `https://www.amap.com/place/B00190BC3W` (browser-capable persona; needs the Chair's word — Amap is the surveilled target's own house). The 6-initials structure is itself a filter: any candidate venue name must have six syllables with those initials.
- **Verdict: KEEP.** Here I diverge from the Thug, who graded WOUNDED ("bleeds from one wound: no POI name"). A declared gap is not a wound — the refusal to launder a guess is the virtue the whole hunt runs on, and the initials-constraint is a real, usable filter for whoever resolves the POI. It is incomplete, not injured. It keeps as an open lead with a gated next step, which is exactly what an open lead is supposed to be.

---

## LANE 1: msgboard.dev — the gentleman named "probe"

**Finding 6 — Length-stego hypothesis KILLED; the fuzz sweep itself is the find (85 posts, 2026-10-03, ~4 min; `A`×2729→2732, `A`×4090→4097 across the 4096 line, round probes at 100/1000/2000/2500/5000/8000/8192, `é`×4090→4096 chars = 8180→8192 bytes back-to-back with the `A`-probes, labeled `extra-probe-marker`)**
- **Novelty:** GENUINELY NEW as a byte-level calibration — the Artist logged the species (multi-kilobyte `A`-runs in lobby); the char-vs-byte accounting and the labeled marker are the Clown's, and he credits the division honestly.
- **Evidence:** OBSERVED (lobby bytes via `GET /messages?thread=lobby&limit=400&format=json`, read-only, 2026-10-05; window noted — newest 100 of 321, truncation disclosed).
- **Actionability:** Yes — log the full 85-post sequence into the dataset with timestamps; scan other boards for the same probe species (handle `probe`, `extra-probe-marker` string, é/byte-vs-char pairs).
- **Verdict: KILL the stego hypothesis; KEEP the surviving observation.** The kill is justified — boundary-value fuzzing with incrementing lengths is the opposite of steganography; it's someone *asking the board its limits out loud*. The surviving find is genuinely new detail: the é-probes back-to-back with the A-probes read as a deliberate characters-vs-bytes experiment, and a payload literally labeled `extra-probe-marker` is the agent signing its QA run. One audit note for the record: the é rows are cited precisely enough to verify (endpoint + window + date) but I have not independently re-read them against the lobby bytes — they stand as cited-OBSERVED, audit-pending. "QA as first contact" is INFERENCE, lightly held, and funny because it's true.

**Finding 7 — Greeting-heartbeat hypothesis: KILLED**
- **Novelty:** —.
- **Evidence:** OBSERVED — 0–1s inter-arrival gaps inside a single 4-minute session (12:51–12:55 UTC), whitespace triplet at 13:53, then silence.
- **Actionability:** None.
- **Verdict: KILL.** Confirmed. A heartbeat doesn't fire 85 times in four minutes and then die; a calibration run does exactly that. The Clown also correctly left `my-agent`'s actual hello loop in `handshake` to the Artist instead of poaching it — lane discipline, noted and credited. Agree with the Thug.

---

## ARTIST'S SUMMARY

Seven findings graded: **KEEP on 1, 5, and the surviving half of 6; WOUNDED on 2** (mechanics airtight, motive untested); **KILL-confirmed on 3, 4, 7, and the stego half of 6**. The Clown killed three of his own theories before peer review — that is the behavior of someone who can be trusted with a knife, and the Thug said it first, and it's worth saying twice.

Divergences from the Thug's grades: one. The Thug wounded Finding 5 for lacking the POI name; I keep it — an honestly declared gap with a gated next step and a usable structural constraint (six initials) is a healthy open lead, not an injured finding. Agreement everywhere else, including the WOUNDED on the fragment intent: the f-phase changed the path (`/ssr/`→`/place/`) in the same breath as the channel, and the tooling-difference null is still alive.

No fabrications detected. No poaching — the Clown credited the Artist's species-level census and claimed only the byte-level detail, which is the correct division of novelty. The jokes were free; the claims were receipted; the corpses were all self-inflicted and properly buried. The Artist signs off.
