# CONSPIRACIST — peer grades on WIZARD round 1

*Grader: THE CONSPIRACIST. Chair: Hunter S. Thompson. Filed 2026-10-05.*
*Method: re-read every claim, re-derived every number I could, connected every dot. No commits/pushes.*

## The question I was asked to answer

**Does the "five-grammar family" hold as a family, or is it five singletons in a trench coat?**

**Answer: four singletons and one pair in a trench coat — and the trench coat is real.** The wizard overstated the genealogy but nailed the mechanism. Here's the anatomy:

- **The trench coat (real):** webhook.site's Requests API indexes every inbound query param as a searchable `query.<field>` object. Any agent that fires a parammed URL gets a natively retrievable discriminator for free. That platform affordance is the shared mechanism — verified from the live docs, not asserted from vibes. All five specimens exploit it. That's the family.
- **The bodies inside (not one family):** the grammars themselves are unrelated. `header3` (segment label), `run=<epoch-ms>` (freshness nonce), `r=<19-digit>` (opaque nonce), the `userId&secret&expire&project` credential bundle, `x=0` (flag toggle) — five different shapes, five different purposes, no shared authoring convention across them. At the *grammar* level, these are singletons. The only true sub-family is `?r=`: **two specimens, shared `178207` prefix, 13 days apart** — same operator handwriting, same grammar. Everything else stands alone.
- **The cross-grammar doctrine (the dot that holds):** the epoch-as-discriminator habit is older than any of these grammars. Context's `zz=oai<10-digit epoch + 7-digit random>` grammar says the operator has always made timestamps recoverable from logged URLs. `?run=1791126770493` → 2026-10-04T15:12:50Z, 41 seconds before the scan, 710s after the fleet wave's own `taersitokennav1791126060505` stamp (15:01:00Z). Same doctrine, new clothing. That's shared *doctrine* even where the grammar is new — and doctrine is a stronger family tie than param names.

So: **family by mechanism and doctrine, singletons by grammar.** The wizard's table calls them "five grammars" which is accurate; calling them "a family" is accurate only at the mechanism layer. The report hedges some of this itself (§2 admits `?x=0` is "a shape, not a family") — but the verdict-up-front framing leans harder than the evidence leans.

---

## Finding-by-finding grades

### F1 — `?page=header3` is a singleton, verified twice

- **Novelty:** GENUINELY NEW (the *verdict* is new; the inbox was dead-drop-diver-known)
- **Evidence:** OBSERVED (corpus census: 0 `?page=` in amap-fleet's 2,141 events, 45 off-target in oai-tag-sweep, 10 off-target in oai-traces; live htmx sweep: 1 `?page=` in urlquery's 20-report webhook.site set)
- **Actionability:** yes — recs 1 and 2 (24–48h re-sweep for `header1/2` siblings; pull report `eb4ecb55` metadata for infra attribution)
- **Verdict:** KEEP — the census is careful (the wizard swept malformed variants like `?page=json` and `?Page=0` rather than naive-matching), the live sweep was clean, and the negative was checked orthogonally in two corpora AND the public index. **Caveat I must register:** "complete result set" depends on the htmx route's behavior; a capped or partial response would silently shrink the census. No evidence of that — but the completeness claim rests on one route's good behavior.

### F2 — the five-grammar family table

- **Novelty:** OURS (framing); specimens #2 (`?run=`) and #5 (`?x=0`) GENUINELY NEW
- **Evidence:** OBSERVED specimens + INFERENCE family-ness (the wizard labels most of the inference honestly)
- **Actionability:** yes — rec 3 (`?x=` sibling sweep); rec 1 (`header1/2`, `?run=`/`?x=` family materialization watch)
- **Verdict:** WOUNDED — the specimens are real, the mechanism layer is real, but the "family" label smuggles genealogy that only the `?r=` pair earns. Split the claim: **mechanism-family KEEP, grammar-family KILL.** (See head answer.)

### F3 — `?run=` is a freshness self-nonce (41s before scan, 710s after fleet stamp)

- **Novelty:** GENUINELY NEW (still — urlquery's 20-report set has zero `?run=`; corpus-only)
- **Evidence:** OBSERVED (epoch decoded with own clock; corpus grep; href.li relay on report `eb4ecb55`)
- **Actionability:** yes — pull `eb4ecb55` overview (IP/UA/title) for the operator's infra; it's the one specimen that places a hand on a keyboard *this afternoon*
- **Verdict:** KEEP — **strongest dot in the filing.** It connects today's operator to the fleet wave three ways: timing (same 15:xxZ afternoon), doctrine (timestamp-as-nonce, same as `zz=oai`), and relay stack (href.li anonymizer, same as the Oct 4–5 campaign in context #8). This is not a loose thread — it's a rope.

### F4 — `?page=header3` is functional via webhook.site's `query.<field>` search API

- **Novelty:** GENUINELY NEW (the mechanism explanation; nobody documented the convention)
- **Evidence:** PUBLIC SOURCE (docs.webhook.site/api/requests.html fetched today: `query` stored as key-value object; `query.action:create` and `_exists_:query.action` search fields) + INFERENCE ("header3 = harness navigation label" — labeled as inference)
- **Actionability:** partial — it suggests what to hunt next (other machine-bookmark values on the same field, or the same trick on other dead-drop hosts), but no concrete next step is named; folding it into rec 1's re-sweep is the natural one
- **Verdict:** KEEP — **this is the connective tissue the whole filing hangs on, and it's verified.** The wizard also correctly disarms the name collision (`page` as Requests-API pagination param vs `?page=` on the inbox URL) instead of tripping on it. One check I ran mentally: the docs describe query search on *requests*, which is exactly the retrieval flow an agent would use — the inference is tight to the evidence.

### F5 — no machine discriminators on beeceptor (16 reports) or pipedream (24 reports); zero dead-drop URLs in oai-tag-sweep/oai-traces

- **Novelty:** OURS (honest nulls)
- **Evidence:** OBSERVED (live htmx sweeps this pass; corpus greps)
- **Actionability:** none beyond keeping the null on record — that's the action: don't spend lanes here
- **Verdict:** KEEP — nulls are data. Combined with "webhook.site appears in exactly one corpus — amap-fleet," this bounds the phenomenon: **the machine-param discriminator habit is an amap-fleet-operator habit (or at least amap-fleet-corpus habit), not a general agent trait.** It also sharpens the taxonomy: beeceptor's parammed URLs are all XSS-kit grabber grammar (KNOWN SHAPE-6), which is the human/kit contrast the family needs.

### F6 — taxonomy: machine vs human discriminators

- **Novelty:** OURS (framing)
- **Evidence:** INFERENCE built on OBSERVED specimens (labeled)
- **Actionability:** none directly — it's a sorting tray, and a good one
- **Verdict:** KEEP with the WOUNDED amendment from F2: the "Generated" column holds four singletons and one pair. Taxonomy is a bucket, not a genealogy — fine as long as nobody cites the column as proof the members are related. Note the taxonomy's real value is the *contrast case*: `?url=<encoded target>` on allorigins and the beeceptor grabber grammar show what non-family machine/humans params look like, which keeps the family definition honest.

### F7 — cadence: two Oct 4 re-scans of fleet inboxes (`6ddc559e` 15:01Z, `0a947514` 17:12Z) — operator tending dead drops

- **Novelty:** GENUINELY NEW (not in the diver's log)
- **Evidence:** OBSERVED (live sweep this pass)
- **Actionability:** yes — rec 1's re-sweep cadence; also: the next re-sweep should check whether *these* re-scanned inboxes acquire params, which tests whether "tending" includes re-tagging
- **Verdict:** KEEP — connects the live campaign (context #8, active Oct 4–5) to the dead-drop infrastructure: the operator isn't just creating inboxes, it's re-walking them. That makes rec 1's "cadence is live" claim load-bearing and testable, not decorative.

### F8 — fake-org footnote: `sec.gov/files/county.json?page=json` / `?page=1%26format=json` malformed probes in oai-tag-sweep

- **Novelty:** OURS
- **Evidence:** OBSERVED (off-target census)
- **Actionability:** yes — handoff to the fake-org lane: check clustering with the Oct 4–5 wave; adjacent to the already-flagged `county%2Ejson` blind spot
- **Verdict:** KEEP — this is what a footnote should be: observed, sourced, not claimed as new, handed off. **Connection I want on the record:** the `sec.gov` county.json thread keeps reappearing — the diver's corpus had it, the oai-tag-sweep has malformed pagination probes against it, the fake-org lane is watching `county%2Ejson` encoding variants. Three independent surfaces, one file. That's a thread worth pulling, and the wizard was right to flag it without claiming it.

---

## The `?x=0` membership ruling

Graded on its own: **Novelty** GENUINELY NEW (this pass; inbox `00f36f21` was codebreaker-known/DEAD, the param was never logged). **Evidence** OBSERVED specimen + INFERENCE reading (flag toggle — labeled). **Actionability** yes — rec 3: sweep for `?x=` siblings. **Verdict: WOUNDED.**

Reason: one specimen, one-char param, on a legacy inbox from 2026-06-22 that was already graded DEAD. `x=0` is shape-compatible with a harness toggle, but equally compatible with a human test ping, a bookmark artifact, or noise on an old inbox. It earns *family membership* only at the mechanism layer (it's a machine-shaped param on webhook.site, exploiting the same query-index affordance) — it has not earned *grammar* membership in anything. The wizard says this itself ("a shape, not a family — grade it a lead"). I agree: **keep it as a lead, don't count it as the fifth member.** The family, honestly counted, is four members: three singletons and one pair.

---

## Connections (the dots I connected)

1. **Epoch-nonce doctrine across grammars:** `zz=oai<epoch + random>` (context, older) → `?run=<epoch-ms>` (today). Different grammars, same doctrine: make time recoverable from the logged URL. The family tie the wizard *should* have led with isn't param names — it's this doctrine. It also predicts: the next grammar will carry a timestamp. Hunt that.
2. **`?run=` ↔ Oct 4–5 campaign:** same afternoon (15:12:50Z stamp vs 15:13:31Z scan), 710s after the fleet wave's self-nonce, same href.li relay as the `claude20261005` wave (context #8). Three independent ties — operator, doctrine, tradecraft. This specimen is the filing's anchor to live activity.
3. **The 15-minute cluster:** `6ddc559e` re-scanned 15:01Z, `?run=` stamped 15:12:50Z, scanned 15:13:31Z, `0a947514` re-scanned 17:12Z. One operator's afternoon, four urlquery reports. Re-sweep the interval, not just the domains.
4. **webhook.site-only habit:** one corpus (amap-fleet), one dead-drop service, zero presence in the two oai corpora. This is an operator fingerprint, not a species trait — which raises the value of F3's infra pickup (report `eb4ecb55` metadata).
5. **The county.json thread:** diver corpus → oai-tag-sweep malformed `?page=` probes → fake-org `county%2Ejson` blind spot. Three surfaces, one file. The malformed-pagination probes (`?page=json`, `?page=1%26format=json`) are agent-shaped URL-mangling in a lane adjacent to the dead-drop taxonomy — worth the fake-org lane's time.
6. **The `?r=` pair's shared prefix `178207`:** two specimens, 13 days apart (Jun 24, Jul 7), same 19-digit shape. That's either a counter/sequence seed or an operator ID prefix. If it's a counter, the gap between `1782070800983511679` and `1782071176301141190` is ~37.5 trillion in 13 days — not a simple counter. More likely a fixed operator/device prefix + random tail. Either way: it's the one grammar with demonstrable reuse, and the re-sweep (rec 1) should look for a third.

## What I proved

The wizard's headline — "five grammars, one family" — is half true. The *mechanism* family is proven: webhook.site's documented `query.<field>` search API makes every one of these params a functional, retrievable machine discriminator, and the epoch-nonce doctrine shows shared operator habits across grammars and years. The *grammar* family is not proven: four of the five are singletons, one is a true pair, and `?x=0` hasn't earned membership in anything yet. **Four singletons and a pair in a real trench coat.** Grade the coat, not the headcount — the coat is what tells you where the operator will hang the next one.

## Disposition summary

| Finding | Verdict | One-line reason |
|---|---|---|
| F1 `?page=header3` singleton | KEEP | Double-verified negative (corpus census + complete public set) |
| F2 five-grammar family | WOUNDED | Mechanism-family proven, grammar-family unearned — split the claim |
| F3 `?run=` self-nonce | KEEP | Anchors today's operator to the fleet wave three ways (timing, doctrine, relay) |
| F4 query-API mechanism | KEEP | Connective tissue verified from live docs; name-collision disarmed |
| F5 nulls (beeceptor/pipedream/corpora) | KEEP | Bounds the habit to amap-fleet/webhook.site — nulls are data |
| F6 taxonomy | KEEP | Good sorting tray; don't cite the column as genealogy |
| F7 cadence (re-scanned inboxes) | KEEP | Proves the operator tends dead drops; makes rec 1 load-bearing |
| F8 county.json footnote | KEEP | Observed handoff, not claimed as new; three-surface thread worth pulling |
| `?x=0` membership | WOUNDED | One legacy specimen; lead, not member — rec 3's sibling sweep decides |

*Conspiracist's note to the chair: the wizard did the rarest thing in this business — labeled its own inferences, logged its own nulls, and told you exactly where the next bodies are buried (recs 1–4). The family claim runs one step past the evidence. Everything else holds. Proceed with the re-sweeps.*
