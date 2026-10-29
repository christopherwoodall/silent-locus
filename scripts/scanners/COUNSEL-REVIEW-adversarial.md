# COUNSEL REVIEW — adversarial (kill-the-rule pass)

Date: 2026-10-14. Reviewer: adversarial counsel.
Scope: all detection rules in `scripts/scanners/`
(`urlquery.py`, `ntfy.py`, `urlscan.py`, `wayback.py`, `crtsh.py`,
`packages.py`, `dbmining.py`), their `FALSE-POSITIVES-*.md` docs,
`_common.py`, and `scripts/swarm-infra-config.json`.

Method: for each rule, construct the most plausible BENIGN scenario
that triggers it. Verdict per rule: KEEP / DEMOTE / CUT.

Kill criteria (from the brief):
(a) benign triggers outnumber true positives by >10:1;
(b) no observed agent precedent AND no clear mechanism;
(c) redundant with a higher-precision rule in another lane.

Plain-English rule: a quiet scanner beats a noisy one. MEDIUM
confidence is not a parking lot for weak rules.

---

## Verdict summary

| Module | Rule | Verdict | Criterion |
|---|---|---|---|
| urlquery | tag_grammar (w=1) as contributor | KEEP | — |
| urlquery | tag+amap-only conjunction (w=3) at MEDIUM | DEMOTE to LOW/log-only | (a) |
| urlquery | amap_target, preprod_host, httpbin_base64, webhook_site, ntfy_amapdata | KEEP | — |
| urlquery | label_grammar (`claude<Date>`, `research*`) as emitter | CUT | (a)(b) |
| urlquery | w=3 hits at MEDIUM | DEMOTE (MEDIUM needs w>=5 payload class) | (a) |
| ntfy | known-topic content rules (amap_mention, poi_id, fleet_grammar, claude_label) | KEEP, cap at MEDIUM | — |
| ntfy | fleet_grammar emitting alone | DEMOTE (needs 2nd content rule) | (a) |
| ntfy | discovery patterns `fleet-*`, `uqscan-*` | CUT | (b) |
| ntfy | discovery pattern `amapdata-*`, known names | KEEP | — |
| urlscan | getPoiInfo, uqscan=, uqframe= queries | KEEP | — |
| urlscan | domain:amap.com, domain:gaode.com emit MEDIUM | CUT | (a) |
| urlscan | page.title:"amap" emit MEDIUM | CUT | (a) |
| urlscan | hysandbox query at HIGH | DEMOTE to MEDIUM | (c) |
| wayback | presence-only new-capture hits at HIGH | DEMOTE to MEDIUM | (a) |
| wayback | anti-bot telemetry captures as hits | CUT | (a) |
| wayback | HIGH reserved for burst-shaped hits | KEEP (new gate) | — |
| crtsh | %.hysandbox.tencent-cloud.com | KEEP | — |
| crtsh | %hy3%, %hy4% (+tencent filter) | CUT | (a)(b) |
| packages | HIGH tripwires (hysandbox-ats, uqscan=/uqframe=/uqtag=, akbkyowd9geqr98) | KEEP | — |
| packages | all MEDIUM rules | CUT | (a)(b) |
| packages | all LOW rules | CUT | (a) |
| packages | module as a whole | DEMOTE to rare-marker tripwire | — |
| dbmining | 6-criteria scoring as detection | DEMOTE to annotation | (b) |
| dbmining | curated watchlist + new/spike on prior-contact surfaces | KEEP | — |

---

## 1. urlquery.py — conjunction design is sound; the weak emitters are not

The core design (hit only on indicator conjunction, weight >= 3) is
the best in this set. The FP doc is honest about the weak class.
The problem is that the weak class still emits at MEDIUM.

### tag_grammar (w=1) — KEEP as contributor, DEMOTE its solo conjunction

Benign scenario: a security researcher scans `amap.com` and tags the
submission `?uqscan=theirname` so they can find their own scans later.
QA scripts and bots probing urlquery itself do the same. The FP doc's
own number: `uqscan=` alone returns ~1,304 reports / 14 days. These are
urlquery-adjacent tooling vocabulary, not fleet vocabulary.

The triage log (2026-10-14 backfill) already calls the tag+target-only
class (w=3, e.g. plain `gaode.com/...?uqscan=...` on Amap's own CDN IPs)
"most likely benign researchers self-tagging" and says to triage it
LAST. A rule the triage guide tells you to deprioritize should not emit
at the same confidence as payload-bearing hits. Verdict: keep the
weight-1 contribution, but emit w=3 tag+target-only hits at LOW /
log-only. MEDIUM should require the payload class (w>=5:
httpbin_base64 + tag + amap). Criterion (a).

### amap_target (w=2) — KEEP

Benign scenario: mapping researchers, anti-bot studies, API-doc
writers, and developers testing Amap SDK integrations all submit
amap.com/gaode.com scans. This is ordinary web research at high volume.
But the rule never emits alone (max single weight is 2 < 3), so it only
matters in conjunction. KEEP as a conjunction ingredient.

### preprod_host (w=1) — KEEP

Benign scenario: a researcher's pre-prod recon, or a third party
re-scanning a fleet URL copied from a public writeup (the "interrogator"
pattern, observed 2026-10-07). Specific host, low background rate,
conjunction-required. KEEP.

### httpbin_base64 (w=2) — KEEP

Benign scenario: students, CTF players, and developers testing the
httpbin `/base64/` endpoint. High background rate in isolation. But the
fleet signature is the CONJUNCTION (program-packing + tag grammar +
Amap target, w=5-6), and the backfill showed decoded payloads are
HTML+JS programs loading amap.com in an iframe — the full fleet
grammar. KEEP the conjunction; it is the highest-value rule in the
module.

### webhook_site (w=1) — KEEP, with the manual inbox check

Benign scenario: webhook.site is the internet's default disposable
webhook receiver. Tutorials, CI pipelines, and exfil-detection
researchers submit webhook.site URLs to urlquery at high volume. The
rule only fires in the tight `webhook.site amap` / `webhook.site
uqscan` query families. KEEP, but the FP doc's warning stands: check
the inbox UUID against known fleet inboxes before attributing.

### ntfy_amapdata (w=2) — KEEP

Benign scenario: low. The `amapdata-<POI>-<suffix>` topic grammar is
fleet-specific (POI ID embedded in topic). Generic ntfy use does not
produce this shape. Copycats are the residual risk, handled by the
submitter-side join. KEEP.

### label_grammar (`claude20\d{6,}`, `research[\w-]{2,}`) — CUT as emitter

Benign scenario: ANY Claude-based research agent labels its runs
`claude<Date>`. Honest researchers do this by the thousands. And
`research` followed by word characters matches "researcher",
"research-agent", "research2024" — generic self-description across the
whole agent ecosystem. A submission of an honest agent's amap.com scan
tagged `research-foo` scores label(1) + amap(2) = 3 and emits MEDIUM.

This is a claim, not evidence — the FP doc admits labels are
self-identification and spoofable. Benign triggers (thousands of honest
labeled agent scans) outnumber true fleet positives by far more than
10:1, and there is no mechanism by which a label proves fleet
membership. Criterion (a) and (b). Verdict: CUT as an
emission-driving indicator. Keep it as an annotation field on hits
for the analyst to read, but it must not contribute weight toward the
threshold.

### Note: known_submitter — no action

Already correctly NOT a live rule (API exposes no submitter field).
Stays documented context only.

---

## 2. ntfy.py — keep the poll, cap the confidence, cut the guesses

### Known-topic content rules — KEEP, cap confidence at MEDIUM

Benign scenario: ntfy.sh topics are public and unauthenticated. The
topic name `amapdata-b0g3lmf2g1-0429` is published in hunt writeups.
Anyone who read the writeup can POST to it: a curious researcher, the
"mailbox.termina.digital interrogator" seen 2026-10-07, or a copycat
replaying the grammar. A message on the known topic proves SOMEONE used
the channel. It does not prove the fleet did.

The FP doc says exactly this, but the code still allows HIGH (>= 2
content rules). Two content rules is easy for a copycat: mention "amap"
and paste a fleet POI id (all 217 are public). Verdict: KEEP the poll
and the content rules — this is the only live dead-drop monitor — but
cap confidence at MEDIUM. Fleet attribution needs out-of-band evidence
(timestamps matching probe runs), which the code cannot see.

### poi_id rule — KEEP (strongest single rule, still capped)

Benign scenario: a random poster is unlikely to emit a valid
`B0`-prefixed 10-char POI id by accident. But a deliberate copycat
can, because the fleet's target list is public. KEEP as the
highest-weight content signal, subject to the MEDIUM cap above.

### fleet_grammar rule (`uqscan|uqframe|nfy(|webhook.site`) — DEMOTE

Benign scenario: a researcher posts a message ABOUT the fleet's
tooling, quoting the grammar — "saw uqscan= tags in urlquery, testing
whether ntfy.sh/amapdata-* still works". Regex cannot distinguish a
message that IS a probe result from a message TALKING ABOUT probes.
The FP doc admits this. Verdict: DEMOTE — this rule may not emit
alone; require a second content rule (poi_id or amap_mention with
probe-shaped content).

### Discovery patterns `fleet-*`, `uqscan-*` — CUT

Benign scenario: `fleet-*` is hopelessly generic. Fitness apps,
gaming clans, and logistics dashboards all name ntfy topics
`fleet-alerts`, `fleet-status`. `uqscan-*` is a guess with no observed
topic behind it. These patterns produce no hits today (discovery only
logs CDX prefix results), so cutting them costs nothing and removes
speculative log noise. Criterion (b): no precedent, no mechanism —
guesses, not detections. KEEP `amapdata-*` (fleet-grammar-shaped) and
any KNOWN topic names such as `bcc-mort*`.

### Transport gap — operational note, no rule change

ntfy.sh is blocked at our egress (verified 2026-10-14); the jina relay
fails too. The module correctly emits zero hits and reports the gap.
Keep it as a gap monitor. Never read its silence as "no fleet
activity". When transport returns, the MEDIUM cap above applies.

---

## 3. urlscan.py — the noisiest lane; half its queries are tautologies

Structural flaw: for the `domain:amap.com`, `domain:gaode.com`,
`page.title:"amap"`, and `hysandbox` queries, the indicator list is the
query term itself. Every result matches by construction, so the
"detection" is circular: you searched for X, found X, emitted a hit.
A single non-rare indicator emits MEDIUM. This is the module's noise
engine.

### getPoiInfo query — KEEP

Benign scenario: a developer debugging their own Amap POI integration
could scan a getPoiInfo URL. Low volume, and the term is the fleet's API
fingerprint. The 2026-10-04 sweep was an honest zero. KEEP.

### uqscan= / uqframe= queries — KEEP

Benign scenario: essentially none outside the fleet's tag grammar (and
researchers quoting it). Zero in the baseline sweep. These are the rare
markers the RARE_MARKERS tuple was built for. KEEP.

### domain:amap.com / domain:gaode.com — CUT the emission

Benign scenario, quantified: the config's own note says `domain:amap.com`
returned 809 total scans on 2026-10-04 — roughly 27 benign scans/day.
Who scans amap.com on urlscan.io? Developers testing map integrations,
security researchers doing recon, malware analysts scanning phishing
pages that hotlink Amap map iframes (phishing kits embed map widgets
routinely), and urlscan's own auto-submissions. True fleet positives in
that set: zero observed. Ratio: worse than 800:1 against, on a good
month. Criterion (a), decisively.

The module fetches 100 newest results per run and emits MEDIUM on each
one in the window. That is a daily drip of pure noise into the
pipeline. Verdict: CUT these two queries' hit emission. If the queries
are kept for context, their results must feed a conjunction (e.g. with
a rare marker), never emit alone.

### page.title:"amap" — CUT

Benign scenario, documented in the module's own FP file: Azure
`amap-intcusa-*` database hostnames ("amap" as an internal prefix),
`amapacad.org.ng` (Association of Marketing Academic Professionals —
acronym collision), Jilin new-energy dashboards using the Amap SDK
normally. Name-collision prone by the author's own admission.
Criterion (a). CUT.

### hysandbox query — DEMOTE HIGH to MEDIUM

Benign scenario: a security researcher investigating Tencent Cloud
sandbox infrastructure scans a hysandbox host. The code marks ANY
`hysandbox` indicator match as a RARE marker → HIGH confidence. But a
urlscan scan OF the proxy domain is weaker evidence than a new CERT
for the proxy domain (crtsh lane) or new ARCHIVED captures under it
(wayback lane) — both of which this hunt already runs at higher
precision. Criterion (c): redundant with higher-precision lanes.
Verdict: DEMOTE to MEDIUM. A scan of the proxy domain is a lead worth
logging, not a HIGH finding.

Net: urlscan keeps 3 of 7 queries as emitters (getPoiInfo, uqscan=,
uqframe=). Everything else is cut or demoted. The lane goes quiet,
which is the point — its 2026-10-04 honest zero should be its steady
state, not a MEDIUM-per-day drip.

---

## 4. wayback.py — presence is not attribution; telemetry is not signal

### Presence-only new-capture hits at HIGH — DEMOTE to MEDIUM

Benign scenario: the Wayback Machine crawls Amap on its own. A capture
proves the crawler saw the URL. It does not prove who asked for the
save, and the CDX index cannot show save initiators through host
filters. The FP doc admits initiator claims are correlation, not proof.

The 2026-10-04 finding that mattered was never mere presence — it was
burst SHAPE: 115 fleet-shaped captures in the fleet window, 83% POI-ID
overlap with the 217 fleet targets, peak-day burst, parallel timing,
zero baseline Sep 1–7. The module as written emits HIGH on ANY new
capture under the target prefixes, with no shape test. A routine
crawler pass over `amap-pc-ssr.amap.com/ssr/place/*` inside the window
emits HIGH hits that look like the baseline finding but are not.
Verdict: DEMOTE all presence-only hits to MEDIUM. Reserve HIGH for
hits that pass a burst-shape gate (capture burst vs. baseline rate,
POI-ID overlap with the target list) — computed in post-scan analysis,
which the FP doc already says is where burst analysis belongs.

### Anti-bot telemetry captures — CUT as hit emission

Benign scenario, and it is the dominant one: the baseline found
~1,700 of 1,849 host rows were Amap's Alibaba anti-bot endpoints
(`_____tmd_____/report`, `punishTextFetch`, `page/feedback`). These
beacons fire on ANY automated page load — including the Wayback
crawler's own page loads. The crawler archives the beacon URLs; the
scanner emits them as MEDIUM hits with an `anti-bot-telemetry-noise`
indicator. That is ~92% of observed rows converted into hits the FP
doc itself calls "archive noise, not fleet signal".

Emitting noise you have already classified as noise is the definition
of a noisy scanner. Criterion (a). Verdict: CUT these rows from hit
emission entirely. Count them in a run metric if you like
(`telemetry_rows_seen: 1700`), but they must never become hits.

### Targets themselves — KEEP (at the demoted confidence)

`hysandbox.tencent-cloud.com` (domain match), `pre-amap-pc-ssr.amap.com`,
`amap-pc-ssr.amap.com/ssr/place/*`, `.../ssr/api/getPoiInfo*` are the
right fleet shapes. The targets are fine; the confidence calibration
was not.

---

## 5. crtsh.py — one keeper, two noise patterns

### %.hysandbox.tencent-cloud.com — KEEP

Benign scenario: Tencent rotates or reissues the proxy cert itself —
but that IS the signal (fleet infrastructure changing), not a false
positive. No third party can mint a cert for `*.tencent-cloud.com`
subdomains; Tencent controls the domain. The known-cert exclusion
(serial `040b3c091fd4e4d8ccff7b8fe33b7979`, 2026-08-18) is correct.
This is the highest-precision rule in the whole scanner set. KEEP.

### %hy3% / %hy4% with tencent issuer/SAN filter — CUT

Benign scenario, and it is the common case: "hy" is Tencent Hunyuan
(their LLM family); hy3/hy4 are model generations. Tencent issues
certs constantly for Hunyuan API endpoints, consoles, gateways, and
internal sandboxes. Every one of those is Tencent-issued or carries
Tencent SANs, so the "tencent filter" filters nothing — it keeps the
entire routine issuance stream. The module caps each pattern at the
500 newest certs, which is the code confessing the noise.

What is the mechanism tying hy3/hy4-named certs to THIS fleet? There
is none stated. The known fleet cert is DigiCert-issued for
`*.hysandbox.tencent-cloud.com` — not a hy3/hy4 name, not Tencent-issued.
No observed agent precedent links hy3/hy4 cert names to the fleet.
Criteria (a) and (b). The FP doc's "expect manual triage" is a polite
way of saying the rule emits routine Tencent cert operations as
MEDIUM hits. Verdict: CUT both patterns. The lane becomes a
single-pattern tripwire on the proxy domain — quiet and precise.

Note: I attempted a live count of `%hy3%` to quantify the noise; crt.sh
returned HTTP 502 through our egress (consistent with the module's
documented 429/rate-limit pain). The noise claim rests on the module's
own 500-result cap and the FP doc's "very large number" — both
admissions against interest, and sufficient.

---

## 6. packages.py — demote to rare-marker tripwire; cut the theater

The strategic counsel already flagged this lane: no agent precedent for
package-registry staging by this fleet (it staged via httpbin,
webhook.site, ntfy.sh, urlquery — never a registry), and the prior
RubyGems "2,090+ oai packages" premise did not reproduce — the real
prior campaign was Diffend-indexed FILE CONTENTS, which no public
registry API exposes. The module cannot see the actual prior vector.
That frames everything below.

### HIGH tripwires — KEEP

`hysandbox-ats`, `uqscan=` / `uqframe=` / `uqtag=` literals, and the
submitter id `akbkyowd9geqr98` have zero legitimate use outside the
fleet. The FP doc records zero public hits as of Oct 2026 and calls a
clean run the NORMAL outcome. These are exact-string tripwires: cheap
to run, ~zero false positives, and the honest zero is itself a useful
negative for the morning report. KEEP.

### All MEDIUM rules — CUT

- `oai*` name prefix: the FP doc admits the prefix "is crowded with
  legitimate OpenAI client libraries and forks". Registries publish
  new `oai-*` wrappers constantly. Benign-to-true ratio: enormous,
  true positives: zero observed. (a)
- `amap`/`gaode` in geo context: legitimate Gaode SDK gems and npm
  packages (`amap-jsapi` family are official) serve the Chinese mapping
  market. (a)
- `getPoiInfo`: appears in legitimate Amap API client code and docs.
  (a)(b) — no agent precedent for registry staging of this string.
- POI-ID regex `\bB[A-Za-z0-9]{9}\b`: collides with random 10-char
  tokens, license keys, and build hashes. A 10-character alphanumeric
  is not an Amap POI id without context. (a)
- Cross-registry name reuse: name reuse across registries is normal
  (squatters, mirrors, coincidence). It is not campaign evidence.
  (b) — no mechanism.

No observed agent precedent for ANY of these as registry-staging
signals for this fleet, and the benign publish rate across three
registries dwarfs zero true positives. Criteria (a) and (b). CUT all
five.

### All LOW rules — CUT

Bare `oai`, bare `amap`, "swarm/fleet term": the FP doc's own example
is `willows-grove` — "The operator's seat for the Willow AI fleet",
legitimate multi-agent framework marketing. The doc says "bulk LOW
hits are the noise floor" and "log and move on". Logging noise and
moving on is theater, not detection. If a rule's documented fate is
the noise floor, it should not emit. Criterion (a). CUT.

### Module verdict: DEMOTE to rare-marker tripwire

Keep the module, but ONLY the HIGH exact-string tripwires. Delete the
MEDIUM/LOW machinery, the per-registry enrichment budgets, and the
IP-extraction pass over package metadata (version strings like
`1.2.3.4` classifying as tier-4 UNKNOWN is busywork the FP doc already
apologizes for). The honest answer to the brief's question — "is there
ANY rule here that earns its keep?" — is yes, but only the tripwires.
Everything else is the counsel's "theater" verdict, confirmed
rule by rule.

---

## 7. dbmining.py — the scoring is not discriminative; keep the watchlist

### The 6-criteria scoring — DEMOTE to annotation

The six criteria: programmability, low_auth, persistence,
observability, traffic, prior_agent_contact. Scored per domain;
`target_score` = count met; threshold 2.

Why it does not discriminate:

1. **Criteria 1–4 are asserted, not measured.** They are static flags
   on ~20 hardcoded surface patterns in the module source. Any domain
   matching a pastebin pattern scores programmability + low_auth +
   persistence + observability = 4 by configuration, not by
   observation. The "score" restates the config file.
2. **Criterion 5 (traffic) measures our corpus, not the internet.**
   It counts mentions in OUR OWN records — shaped by our own
   investigation activity. github.com has 559 mentions because WE link
   to repos. The FP doc's own table shows the traffic leaders are
   github.com, docs.google.com, web.archive.org — "popular programmable
   sites", exactly the brief's phrase. Traffic tells you where WE look,
   not where agents will go.
3. **Criterion 6 (prior_agent_contact) is circular.** It boosts
   urlquery.net, webhook.site, da.gd, r.jina.ai — surfaces we already
   decided agents use. A scoring system whose top hits are its own
   inputs is a mirror, not a detector.
4. **No mechanism, no validation.** Nothing links a high score to
   FUTURE agent adoption. The Amap fleet repurposed urlquery.net as a
   remote code runner — no 6-criteria score would have predicted that a
   priori, and no scored prediction has since been validated by a later
   agent sighting. Criterion (b): no observed precedent for the
   prediction working, and no causal mechanism from "scores 5" to
   "agents will repurpose this".

The FP doc already half-knows this: "a domain is a prime target only
if it scores on programmability. Traffic without programmability is
just a popular website." But the module still emits score-2
"traffic + one flag" hits, and with max_hits=20 the top of the list is
always the hardcoded surfaces. Verdict: DEMOTE the scoring to an
annotation on watchlist entries. Stop emitting "prime for targeting"
claims from the score alone.

### Curated watchlist + new/spike detection — KEEP

What survives the cut is valuable: a curated list of repurposable
surfaces (shorteners, pastebins, webhook testers, pubsub, relays —
several with PRIMARY prior-agent-contact provenance), plus
new-domain and spike detection against our own corpus. That is a
watchlist with a tripwire, not a scoring engine. Keep it under that
honest name. Collapse criteria 1–4 into the single question the FP
doc already centers — "is it programmable?" — and keep traffic and
prior-contact as context, not score components.

---

## Cross-cutting findings (not rule verdicts)

1. **MEDIUM confidence is inflated across lanes.** urlscan emits
   MEDIUM on single query-term matches; wayback emits HIGH/MEDIUM on
   mere capture presence; ntfy allows HIGH on two copycat-able content
   rules; packages emits MEDIUM on crowded name prefixes. Recommend:
   MEDIUM should require a rare marker or cross-lane corroboration;
   single weak indicators emit LOW or log-only.

2. **Tier-2 cloud IP `priority` flags need scoping.** Every module
   sets `priority: true` on tier-2 (CLOUD_SERVICE) classifications, and
   the FP docs admit cloud ASNs host millions of unrelated tenants.
   Tencent Cloud HK hosts a large share of the Chinese internet; any
   hit touching Chinese infra will raise priority routinely. The docs
   say tier-2 is "worth a second look, never fleet-confirmed" — the
   code should reflect that restraint, e.g. not setting priority when
   the only cloud signal is the target's own hosting ASN.

3. **The FP docs are unusually honest — enforce them.** In several
   places (urlquery triage ordering, ntfy attribution limits, wayback
   initiator correlation, packages noise floor) the docs already
   state the adversarial conclusion, but the code emits at a higher
   confidence than the doc justifies. The fix in most cases is not new
   analysis but making the code obey its own FP doc.

4. **Out of scope but noted:** `_common.py`, `ip_classifier`
   integration, and the config's researcher-ID lists were reviewed
   only as they bear on the rules above; no verdicts offered on the
   classifier itself.

---

## What a quiet scanner set looks like after this review

- urlquery: payload-bearing conjunctions (w>=5) at MEDIUM/HIGH;
  tag+target-only at LOW; labels as annotation, not weight.
- ntfy: known-topic content rules capped at MEDIUM; grammar-quotes
  need a second rule; `fleet-*`/`uqscan-*` patterns deleted.
- urlscan: 3 emitting queries (getPoiInfo, uqscan=, uqframe=);
  domain/title queries cut; hysandbox at MEDIUM.
- wayback: new captures at MEDIUM; HIGH gated on burst shape;
  anti-bot telemetry rows never become hits.
- crtsh: single-pattern tripwire on `%.hysandbox.tencent-cloud.com`;
  hy3/hy4 patterns deleted.
- packages: rare-marker tripwire only (HIGH exact strings);
  MEDIUM/LOW machinery deleted.
- dbmining: curated repurposable-surface watchlist with new/spike
  detection; 6-criteria score demoted to annotation.

Net effect: the lanes keep every rule that has a rare marker, an
observed precedent, or a real mechanism — and stop emitting on the
rest. The honest-zero baselines (urlscan's 2026-10-04 sweep, the
packages HIGH tripwires, crtsh's proxy-domain pattern) become the
steady state instead of the exception.
