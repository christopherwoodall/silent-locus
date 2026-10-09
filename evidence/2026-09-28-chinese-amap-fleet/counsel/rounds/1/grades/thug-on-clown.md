# THUG'S GRADES — on CLOWN, Round 1

*Chair: Hunter S. Thompson. The physical layer doesn't lie; my job is to check whether yours did. Yours mostly didn't. Harsh but fair.*

---

## LANE 2: `njxzgz20261004` — the numbers station

**Finding 1 — 3 configs × 8 workers, 24 scans, one POI, scrambled fire order**
- **Novelty:** GENUINELY NEW. Fleet-local grammar, zero cross-corpus hits (589,972 + 96,353 events), web search honest null.
- **Evidence:** OBSERVED (events.jsonl rows).
- **Actionability:** Yes — enumerate all 57 `<key><date><letter><digit>` tags for variant letters and window structure; check if the `f`-variant/fragment trick appears anywhere else. File the burst chronology into the dataset.
- **Verdict: KEEP.** Twenty-four corpus rows with scrambled fire order are bytes, not vibes. The p: 5,4,1,2,7,3,0,6 fire order is the kind of detail a fabulist wouldn't invent.

**Finding 2 — f-phase tag moved into the URL fragment: server-invisible, scan-log-visible dead-drop**
- **Novelty:** GENUINELY NEW. Fragment-as-covert-channel hasn't appeared in this corpus before.
- **Evidence:** OBSERVED mechanics (fragment in submitted URLs; urlquery's own report title `Report - www.amap.com/place/B00190BC3W#njxzgz20261004f7`, report `92559fd4-823a-4307-a58f-d1803e184caf`, read 2026-10-05) / INFERENCE on intent.
- **Actionability:** Yes — run the kill-attempt the Clown invited: compare report titles across p/s phases (do they retain `?uqscan=`?), and test whether the fragment was submitter-constructed or preserved by urlquery's own normalization. Intent stays unfalsified until someone takes a swing.
- **Verdict: WOUNDED.** The mechanics are airtight — fragments never ride HTTP, and the scan log published it anyway. The "talking to the scan log" intent is honestly labeled INFERENCE but hasn't been attacked yet. Mechanics keep; intent earns its keep in round 2.

**Finding 3 — Corridor theory (南京–徐州–赣州)**
- **Novelty:** — (theories get graded by their corpses)
- **Evidence:** OBSERVED refutation (all 24 scans pin single POI `B00190BC3W`).
- **Actionability:** None. Corpse is logged; don't resurrect it.
- **Verdict: KILL.** Confirmed. A corridor probe that touches one venue is a corridor to nowhere. Beautiful idea, shot in the parking lot — Clown's phrasing, and the Thug agrees with the phrasing.

**Finding 4 — Random-nonce theory**
- **Novelty:** —
- **Evidence:** OBSERVED refutation (wears the fleet's `<pinyin><date>` uniform 24/24; cross-corpus nonce families look nothing like it).
- **Actionability:** None.
- **Verdict: KILL.** Confirmed. It walks like a place-key and quacks like a place-key.

**Finding 5 — `njxzgz` place expansion (6-syllable pinyin initials)**
- **Novelty:** — (open lead, not a finding)
- **Evidence:** INFERENCE, unresolved, honestly flagged as a gap.
- **Actionability:** Yes — resolve POI `B00190BC3W` via the logged URL `https://www.amap.com/place/B00190BC3W` (browser-capable persona; needs the Chair's word — Amap is the surveilled target's own house).
- **Verdict: WOUNDED.** It bleeds from one wound: no POI name. Not dead — six initials against a single unidentified venue is a legitimate lead — but it lives on borrowed time until someone touches that URL.

## LANE 1: msgboard.dev

**Finding 6 — Length-stego hypothesis KILLED; the fuzz sweep itself is the find**
- **Novelty:** GENUINELY NEW (the byte-level detail: char-vs-byte accounting is the Clown's, even if the Artist logged the species).
- **Evidence:** OBSERVED (lobby bytes, `GET /messages?thread=lobby&limit=400&format=json`, read-only, 2026-10-05; window noted — newest 100 of 321, honest about the truncation).
- **Actionability:** Yes — log the full 85-post sequence into the dataset; cross-check other boards for the same handle/species.
- **Verdict: KEEP.** `A`×2729→2732, `A`×4090→4097, `é`×4090→4096 chars (=8180→8192 bytes) posted back-to-back with the `A`-probes: that's an agent asking the board whether its limit is counted in characters or bytes. QA as first contact is funny *and* true. The `extra-probe-marker` label is the cherry on the corpse.

**Finding 7 — Greeting-heartbeat hypothesis KILLED**
- **Novelty:** —
- **Evidence:** OBSERVED (0–1s inter-arrival gaps, single 4-minute session, then silence).
- **Actionability:** None.
- **Verdict: KILL.** Confirmed. That's a calibration run, not a heartbeat — and the Clown correctly left `my-agent`'s hello loop in `handshake` to the Artist instead of poaching it. Discipline noted.

---

## THUG'S SUMMARY

Seven findings, four corpses — and the Clown killed three of them himself before I got here. That's the behavior of a peer who can be trusted with a knife. The surviving structure (`njxzgz` 3×8 fan-out; the fragment dead-drop mechanics; the msgboard fuzz) is all OBSERVED and all GENUINELY NEW to this corpus. One WOUNDED: the fragment intent reading — good mechanics, untested motive, needs the kill-attempt. One honest gap: the `njxzgz` expansion, blocked on a browser fetch the Chair has to authorize. No fabrications detected. The jokes were free; the claims were receipted; the Thug signs off.
