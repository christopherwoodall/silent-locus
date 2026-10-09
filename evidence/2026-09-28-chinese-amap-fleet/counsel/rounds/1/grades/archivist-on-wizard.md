# ARCHIVIST on WIZARD — peer grades, round 1

*Filed 2026-10-05. Chair: Hunter S. Thompson. Method: re-ran every corpus grep myself, re-decoded every epoch with my own `date -u`, fetched docs.webhook.site/api/requests.html live, cross-checked every cited report ID against the counsel record and the persona lanes. Harsh but fair — the wizard did real work here, and I'm going to say exactly where the bytes hold and where the swagger outran them.*

**Overall:** The strongest byte-level filing in this round. The `?page=header3` singleton verdict, the webhook.site `query.[field]` docs connection, and the `?run=` clock math all survive independent re-verification. But the wizard inflates two counts, over-grades novelty on `?run=` and the re-scan cadence (both are tracker-known), and frames digest-substring artifacts as "ngrok mentions." None of these kill the findings — they wound the adjectives. Details below.

---

## Grade table

### F1 — `?page=header3` singleton census (§1)

| Axis | Grade |
|---|---|
| Novelty | **GENUINELY NEW** — verdict holds |
| Evidence | **OBSERVED** |
| Actionability | Follow-up #1 (24–48h re-sweep for siblings) — concrete, KEEP |
| Verdict | **KEEP** |

**Evidenced reason:** Zero `header3` in all three corpora (re-grepped: 0/0/0 across 2,141 + 96,353 + 589,972 lines — corpus sizes themselves check out). The oai-traces `?page=` composition the wizard claimed (6 kansasmemory URLs + 4 bac-lac) re-verified as 6 distinct kansasmemory URLs and exactly 4 bac-lac `page=` occurrences — the count is defensible under distinct-URL counting. The public-search negative confirmed independently: `"page=header3" webhook.site` returns only CSS `.header3` class noise, zero documented usage. Corroborated by archivist.md Audit B (HOLDS), jock.md, tracker's FINDINGS.md, and metronome's raw htmx file (20 unique report IDs — matches the wizard's "complete set: 20 reports" claim).

**Wound (precision, not substance):** the wizard's "45 `?page=` hits" in oai-tag-sweep does not match bytes. Re-count: **41 occurrences / 30 lines** (`[?&]page=`, case-insensitive), composed of 27 sec.gov + 2 newspapers.com + 1 investor.gov lines. The "~40× sec.gov" breakdown is the shaky part. The material claim (all off-target, none on dead-drop hosts) is untouched — but 45 should read 41.

---

### F2 — The five-grammar machine-discriminator family (§2)

| # | Grammar | Novelty (wizard) | Novelty (archivist, corrected) | Evidence | Verdict |
|---|---|---|---|---|---|
| 1 | `?page=header3` | GENUINELY NEW (verdict) | **GENUINELY NEW** — agreed | OBSERVED | **KEEP** |
| 2 | `?run=<13-digit epoch-ms>` | GENUINELY NEW (still) | **KNOWN (tracker)** — downgrade | OBSERVED (distribution) | **WOUNDED** |
| 3 | `?r=<19-digit>` | KNOWN (diver) | **KNOWN (diver)** — confirmed | OBSERVED | **KEEP** |
| 4 | `?userId=…&secret=…&expire=…&project=…` | KNOWN (SHAPE-2) | **KNOWN** — cited, not re-verified this pass | PUBLIC SOURCE (his sweep) | **KEEP** (provisional) |
| 5 | `?x=0` | GENUINELY NEW | **GENUINELY NEW** — agreed, as a lead | OBSERVED (one specimen) | **KEEP** (lead, not verdict) |

**Evidenced reasons:**
- **#2 downgrade:** tracker's FINDINGS.md:64 already documents `?run=<epoch-ms>` as the known Amap operator's dead-drop grammar (carried-forward state), and tracker's raw deaddrops.md:156 logs the exact `href.li/?https://webhook.site/a7753b69-…?run=1791126770493` URL. The wizard's "GENUINELY NEW (still)" is wrong at project level. What IS new is his distribution evidence: absent from urlquery's 20-report public set, corpus-only — that's a real OBSERVED contribution, just not a new grammar.
- **#3 confirmed:** diver's FINDINGS.md lines 34–38 documents SHAPE-4 with the exact pair, the exact reports (`6fbff60b`, `2baccf7b`), the shared `178207` prefix, and the 13-day gap — verbatim support. (Note: the prior-round archivist's "UNVERIFIED from the shared record" note is now resolved — the record exists in the persona lane; the wizard did the legwork the prior audit didn't.)
- **#5 confirmed:** codebreaker's FINDINGS.md:67 grades inbox `00f36f21` as DEAD (404) — "codebreaker-known (legacy, graded DEAD)" checks out. The `?x=0` param itself is unlogged anywhere in the record. Wizard correctly labels it a lead, not a verdict — honest grading, respect.
- **"Nobody has documented any of this publicly":** the specific negative checks I could reproduce (header3) hold; as a blanket claim over five grammars it's asserted, not exhaustively proven. Downgrade the sentence to the specific negatives actually run.

---

### F3 — `?run=` is a self-nonce, verified with the wizard's own clock (§3)

| Axis | Grade |
|---|---|
| Novelty | **OURS** (new analysis on a tracker-known specimen) |
| Evidence | **OBSERVED** — clock math independently reproduced |
| Actionability | Follow-up #2 (pull `eb4ecb55` metadata) — concrete, but tempered (see below) |
| Verdict | **KEEP** — the strongest single byte in the filing |

**Evidenced reason:** Re-decoded with my own `date -u`: `1791126770493` → **2026-10-04T15:12:50Z** ✓; urlquery scan 15:13:31Z → **41s** delta ✓; fleet nonce `1791126060505` → **15:01:00Z**, delta **709,988ms ≈ 710s** ✓. All three numbers reproduce exactly. The `href.li` relay claim corroborated by tracker's raw deaddrops.md:156. The "freshness self-nonce" reading is labeled-adjacent inference and it's the correct one — same doctrine as the `zz=oai` epoch grammar.

**Tempering on follow-up #2:** the wizard wants `eb4ecb55`'s metadata for IP_LOG attribution. Jock already ran this lane to ground: all observed scan-exit IPs (178.63.67.153, 178.63.67.106) are urlquery's own nodes — "nothing for the IP_LOG from this lane." The metadata pull is still worth one call (UA/title), but the IP expectation should be zero. Adjust the follow-up, don't kill it.

---

### F4 — `?page=header3` is functional, not accidental (§4, the docs connection)

| Axis | Grade |
|---|---|
| Novelty | **GENUINELY NEW** (the docs connection is new analysis) |
| Evidence | **PUBLIC SOURCE** — citation verified verbatim |
| Actionability | None needed — this finding *is* the upgrade; feeds the taxonomy |
| Verdict | **KEEP** |

**Evidenced reason:** Fetched docs.webhook.site/api/requests.html live. The wizard's citation is exact: `query.[field]` is a documented search field ("type `web` only"); the example `query.action:create` is quoted verbatim; `query` is documented as "a key-value object of all query strings in the URL"; and `page` (int) is documented as the Requests API pagination param — so the name-collision caution is not pedantry, it's load-bearing for the taxonomy. This is the finding that promotes `?page=header3` from curiosity to functional tradecraft: a natively searchable discriminator the operator can query back with `query.page:header3`. The "harness navigation label" reading is labeled INFERENCE and stays labeled — fine.

---

### F5 — Dead-drop services: no machine discriminators on beeceptor/pipedream (§5)

| Axis | Grade |
|---|---|
| Novelty | **OURS** (confirmed nulls) |
| Evidence | **OBSERVED** (his 16+24-report live sweeps; corroborated by diver's SHAPE-6 beeceptor rows) |
| Actionability | None — null is the result |
| Verdict | **KEEP**, with two wording wounds |

**Evidenced reasons / wounds:**
1. **"oai-traces has 11 ngrok string mentions"** — false precision. Re-grepped: the 11 case-insensitive hits are digest-substring artifacts (e.g. `...WIBNGROKCT...` inside base32-ish digests), not genuine ngrok mentions. There are **zero** real ngrok mentions. The conclusion ("none are URLs — dead end for this lane") survives, but the "11 mentions" framing implies observed infrastructure signal where there is hash noise. Reword to zero.
2. **"webhook.site appears in exactly one corpus — amap-fleet, one URL"** — off by one mention. Two lines in amap-fleet's events.jsonl contain the string: the `?run=` URL, plus a venue_finding whose metadata records `"submitted_domain": "webhook.site"` for report `97f0619b`. Irony: the second mention *corroborates* the wizard's §2 cadence claim (97f0619b = the `6ddc559e` fleet-inbox re-scan). The imprecision accidentally buried supporting evidence. Correct the count, keep the conclusion.

---

### F6 — Taxonomy: machine vs human discriminators (§6)

| Axis | Grade |
|---|---|
| Novelty | OURS (organizational) |
| Evidence | INFERENCE built on the above OBSERVED rows |
| Actionability | None — working taxonomy; adopt with corrected novelty tags |
| Verdict | **KEEP** |

**Evidenced reason:** Follows from F1–F5. Adopt it, but re-tag the rows per F2: `?run=` and `?r=` are project-KNOWN, `?page=header3` and `?x=0` are GENUINELY NEW, `?x=0` stays a lead. The allorigins `?url=` contrast case is cited as OURS without a shown provenance trail — acceptable in a taxonomy, but flag it as needing a source line in the next pass.

---

### F7 — Cadence: Oct 4 re-scans of the fleet's own inboxes (§2, cadence paragraph)

| Axis | Grade |
|---|---|
| Novelty | **KNOWN (tracker)** — downgrade from "OURS/NEW" |
| Evidence | **OBSERVED** — independently corroborated |
| Actionability | Follow-up #1 (24–48h re-sweep) — concrete, KEEP |
| Verdict | **WOUNDED** — evidence solid, novelty overstated, interpretation survives |

**Evidenced reason:** The re-scans are real: jock.md independently found `97f0619b` (`6ddc559e`, 2026-10-04T15:01:37Z) and `8213c4a1` (`0a947514`, 2026-10-04T17:12:59Z) in a 48h urlquery sweep, and amap-fleet's own events.jsonl carries a venue_finding for `97f0619b`. But jock.md also records that tracker already logged both inboxes (FINDINGS.md:153-158) as the known operator's rotation ritual. The wizard's "not in the diver's log" is true and beside the point — they're in the *tracker's* log. The "campaign tending its dead drops" interpretation is new inference and it's a good one, but the specimens are counsel-known. Regrade novelty, keep the read.

---

### F8 — Footnote to fake-org lane: `county.json?page=json` probes (§1 footnote)

| Axis | Grade |
|---|---|
| Novelty | OURS (observation) |
| Evidence | **OBSERVED** — verified in bytes: `?page=json` ×3 lines, `?page=json%26v=362854` ×2, `?page=1%26format=json` ×1 |
| Actionability | Follow-up #4 (cluster-check vs the Oct 4–5 wave) — concrete, KEEP |
| Verdict | **KEEP** |

**Evidenced reason:** Real malformed-pagination probes against the SEC county file, sitting next to the `county%2Ejson` blind spot already flagged. Correctly scoped as a footnote with a named next step rather than a finding.

---

## Follow-ups audit (all four survive)

1. **24–48h re-sweep `url.domain:webhook.site`** — concrete, matches jock's open cadence leg. KEEP.
2. **Pull `eb4ecb55` metadata (IP/UA/title)** — concrete, but per jock's correction the IP_LOG expectation is ~zero; pull for UA/title only. KEEP, amended.
3. **Grade the `?x=0` grammar** — concrete, the right next move on the one new lead. KEEP.
4. **Cluster-check the `county.json?page=` probes vs the Oct 4–5 wave** — concrete, correctly routed to the fake-org lane. KEEP.

## Honest nulls — commended

The null list is the mark of a filing that knows what it doesn't know. Verified the key ones myself: no `?page=` siblings anywhere, no `?run=` beyond the single corpus specimen, zero dead-drop-service URLs in oai-tag-sweep/oai-traces (and the amap-fleet count correction in F5). The pipedream 2024 marketing artifact is correctly withheld per the no-human-identity rule — noted, not reproduced, properly handled.

---

## Final tally

- **KEEP:** F1 (with count correction 45→41), F2 rows #1/#3/#4/#5, F3, F4, F5, F6, F8
- **WOUNDED:** F2 row #2 (`?run=` novelty: GENUINELY NEW → KNOWN/tracker; distribution evidence stays), F7 (cadence novelty: NEW → KNOWN/tracker; interpretation stays), F5's ngrok line (11 "mentions" → 0 real), F1's "45 hits" (→ 41 occurrences / 30 lines)
- **KILL:** nothing. Zero findings killed. That's the harshest praise this chair gives: the wizard's bytes hold, even where his adjectives don't.

*The docs connection in F4 is the find of the round — it turns a weird query string into a searchable dead-drop discriminator with a manual page to prove it. Everything else is good tradecraft taxonomy. File the corrections, keep the findings.*
