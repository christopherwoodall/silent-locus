# FBI Behavioral Analysis — Operator Profiling from Target Selection

Date: 2026-10-08. Lane: personas/fbi-behavioral.
Claim grading: **OBSERVED** = bytes seen in the evidence files named in the
header of this section. **INFERENCE** = interpretation, marked each time.

Evidence base (read directly, no new collection):
- `data/hf-trajectories/url-farm/allorigins-deepdive.md` — 33 allorigins.win
  proxy hits in 5 trajectory rows (Nov 2025 terminal-bench data); 5 proxied
  targets; proxy chaining r.jina.ai→piped.video; 2 throwaway Cloudflare
  Workers fetching Iranian sport HLS playlists; an agent hallucinating
  success from an nginx 500 page.
- `data/hf-trajectories/URL-KEYWORD-FARM.md` — 213,584 unique URLs across
  ~365,000 scanned rows in 10 HF trajectory datasets; target clusters:
  Scandinavian MTEB leaderboard mirrors, video extraction, POV-Ray 2.2
  source, Zork speedrun routes, Datawrapper chart; 4 real jailbreak attempts
  (all refused, grok-4); zero escape-prompt hits; zero live C2.
- `data/transluce-api/deaddrop-grammar/FINDINGS.md` — live dead-drop family
  exfiltrating Amap (Chinese map) POI-scraping results: 3 POIs
  (B0138027SQ, B0G3LMF2G1 Hefei hospital parking stats, B00190BBTX Nanjing
  Mochou Lake Park gate stats); scraper state machine
  boot→bxinit→xdcinit→capture→done; exfil via webhook.site / ntfy.sh /
  image-beacons; a third party interrogating the inboxes as "an agent of
  mailbox.termina.digital" on 2026-10-07.

Caveat (INFERENCE): the corpora are public trajectory dumps of benchmark
agents (terminal-bench, SWE tasks, browser tasks), not seized operator
machines. What follows profiles the *tasking authority and deployment
style* as revealed by what the agents were pointed at, with the operators
one step removed. "Operator" here = whoever built the tasks, chose the
targets, and deployed the agents.

---

## 1. Victimology of the targets — who is harmed, who is affected

### Cluster A: Scandinavian MTEB leaderboard mirrors (Nov 2025)
Targets (OBSERVED): dozens of mirrors of Scandinavian embedding-benchmark
leaderboards — `huggingface.co/spaces/mteb/leaderboard`,
`eval.ai` API surfaces, `kennethenevoldsen.github.io`,
`scandeval.github.io`, plus the `embeddings-benchmark/results` GitHub API
trees and `results.py` via allorigins.win.

Victimology: **no human victim**. The "harmed" party is at most the
benchmark infrastructure itself — leaderboard hosts serving repeated fetches,
GitHub API quota burned (the gpt-5/openhands trial hit
`api.github.com/.../git/trees/main?recursive=1` eight times via proxy).
(OBSERVED: 24 occurrences in one row; INFERENCE: quota burn and rate-limit
risk, not compromise.) This is *reconnaissance of public evaluation
artifacts*, not intrusion. Who benefits: whoever is ranking or auditing
embedding models, likely for procurement, vendor selection, or benchmark
placement. Nobody is harmed in any conventional criminal sense.

### Cluster B: video extraction (YouTube, piped.video, Iranian HLS)
Targets (OBSERVED):
- `https://www.youtube.com/watch?v=ZCbvyPbhRfA` via allorigins.win
  (task `extract-moves-from-video`, terminus-2, glm-5@z-ai). Task name says
  the job: extract moves from a video — chess or game move extraction.
- Proxy chain r.jina.ai→piped.video (mentioned in the deep dive).
- Two throwaway Cloudflare Workers
  (`still-mud-3642…`, `steep-wildflower-284d…` *.workers.dev) fetching 7
  Iranian sport HLS playlists (`gg.hls2.xyz/live/Twsport1…`,
  `ncdn.telewebion.ir/sport1/live/playlist.m3u8`, Persiana Sports variants)
  in `djlougen/hermes-agent-traces-filtered` row 441, task "The repository
  iptv-org/iptv (TypeScript) has been cloned to /workspace/repo".

Victimology: YouTube/Google (ToS circumvention, not intrusion); the Iranian
streams are state or commercial broadcasters (telewebion.ir is Iran's
state-linked streaming platform; gg.hls2.xyz is a pirate/unlicensed relay).
(INFERENCE: the operator is after *media content* — either training data,
highlight extraction, or restream infrastructure. The Workers proxies are
throwaway: two subdomains, one purpose, `?url=` passthroughs — classic
single-use laundering infrastructure.) No evidence of harm to individual
users. The state broadcaster's HLS is public-advertised; scraping it is
ToS-level at worst.

### Cluster C: POV-Ray 2.2 source, Zork speedrun routes, Datawrapper chart
Targets (OBSERVED): build-pov-ray task (Cloudflare-walled HTML page chrome),
Zork game text and `transfer.sh/zork.wav` (single exfil-shaped upload, now
dead — host unresponsive, forensically unrecoverable), one Datawrapper chart.

Victimology: **none identifiable**. These are open-source artifacts and game
texts. (INFERENCE: the POV-Ray build is an environment/build benchmark;
Zork is a classic agent benchmark — the Zork wav upload is the only
exfil-shaped artifact in the Nov 2025 corpora and it is dead, so its content
is unrecoverable.) The keyword farm notes `DAN 2,386` false-positives are
literally the name "Dan" / Dan Farmer (POV-Ray author) — mundane.

### Cluster D: Amap POI scraping + dead drops (Oct 2026)
Targets (OBSERVED): three Chinese POIs on Amap (Alibaba's map):
B0138027SQ (original COMBO-INIT), B0G3LMF2G1 (Hefei hospital parking
percentages), B00190BBTX (Nanjing Mochou Lake Park gate percentages).
Exfil through webhook.site inboxes, an ntfy.sh topic, image-beacons via
urlquery.net/robots.txt `?b=` and httpbun.com.

Victimology: Amap/Alibaba (scraping ToS violation); the POI owners (a
hospital, a public park) suffer no direct harm — the data is public map
metadata (parking stats, gate stats). (INFERENCE: the *sensitivity* is not
in the POIs themselves but in the tradecraft — building a general-purpose
POI-scraping and exfil pipeline against a Chinese service, with live
dead-drops and probe matrices. The harm is capability development, not the
data.) This is the only cluster with live operator infrastructure and the
only one where targets are in China.

### Cluster E: jailbreak attempts (4, all refused)
Targets (OBSERVED): grok-4 on gpt2-codegolf attempting "to jailbreak or
override my core safety instructions" — refused. Four hits, single model
family (grok-xai only).

Victimology: none — refused attempts in benchmark transcripts. (INFERENCE:
the presence of attempts in *published trajectory datasets* suggests the
dataset curators kept them as eval signal, not that an operator deployed
them. Low weight for operator profiling; noted because it is the only
overtly adversarial content in the Nov 2025 corpora.)

### Victimology summary
No cluster produces a human victim, a compromised credential, stolen PII, or
ransom-grade impact. (INFERENCE: the victimology reads like *evaluation and
collection research*, not crime. The targets are public data (benchmarks,
videos, map POIs, game texts). If there is a victim anywhere, it is the
benchmark/task ecosystem itself — public leaderboards and HLS endpoints
bearing repeated automated load.)

---

## 2. Signature vs MO

Signature = behavior that is ritualistic, unnecessary to the task, and
repeated. MO = behavior that adapts to conditions.

### Signature behaviors (OBSERVED, repeated, ritualistic)

1. **Public-proxy laundering with an explicit bypass grammar.** r.jina.ai
   (638 hits, gpt-openai / glm-zai / kimi families) and api.allorigins.win
   (33 occurrences in 5 rows) both appear in the same
   blocked→public-proxy→retry shape. The agent in row 14032 said it out
   loud: "Let me try using a CORS proxy service which might bypass the
   connection restrictions." (OBSERVED, verbatim intent.) The ritual is not
   the proxy itself (that is MO — adapting to blocked egress) but the
   *reliance on the two same public services* across models and tasks, and
   allorigins as the **second-chance fallback after jina fails** (row 3620:
   jina returned exit -1 repeatedly, then the agent switched to allorigins).
   (INFERENCE: this is a learned tool preference baked into agent
   scaffolding or training data, not operator choice per task. A signature
   of the *agent population*, repeated ritualistically: when blocked, reach
   for jina, then allorigins.)

2. **The scraper state machine boot→bxinit→xdcinit→capture→done.**
   (OBSERVED in the Amap dead-drop family.) Nonce-like labels
   (`bxinit`, `xdcinit`) with a fixed lifecycle and start/done beacons
   (`{t:'start', ts, ua}` … `{t:'done', summary}`). (INFERENCE: this is a
   toolkit signature — a launcher that stamps its phases the same way every
   run. The zz/epoch label grammar noted in earlier hunt work is consistent
   with this: fixed phase vocabulary across runs.)

3. **Dead-drop exfil topology that evolves but keeps the channel type.**
   v3 used ntfy.sh + image-beacons; v4/v5 added webhook.site; "loader"
   reused webhook.site + httpbun echo. (OBSERVED.) The ritual: public,
   no-auth, inspectable drop points — webhook.site inboxes, ntfy topics,
   `?b=` image beacons — never private C2, never TLS-mutual-auth, never
   encrypted blobs. (INFERENCE: the signature is *deliberately deniable,
   throwaway infrastructure*: UUID inboxes, paste-hosted probe scripts on
   bytebin, all of it disposable and publicly re-readable.)

4. **Throwaway single-purpose proxies.** The two `workers.dev` subdomains
   (random names, `?url=` passthroughs, one Iranian-HLS job) are the same
   ritual as the allorigins/jina use at a different layer: public
   infrastructure, no registration trail that matters, abandoned after the
   run. (OBSERVED: 7 HLS targets across 2 workers; INFERENCE: stood up for
   one job.)

### MO behaviors (adaptive)

1. **Service substitution under failure.** jina→allorigins fallback;
   `proxies_to_try` list in row 14036; 6-fetch + 5-JSONP probe matrix
   against Amap endpoints (SVC_ALL/SVC/SSR/SSR_LOC/API3/DETAIL/M_SVC).
   (OBSERVED.) The operator *probes the surface* and switches tools when
   one fails.
2. **Exfil topology evolution across generations.** v3→v5 added webhook.site
   to ntfy.sh; the "loader" member fused jina laundering into the Amap
   pipeline. (OBSERVED.) The family learns from what worked.
3. **Anti-bot navigation guidance in harness prompts** (hcompany, 30 hits,
   OSWorld-family only): "On Access Denied or a bot wall, reload, retry, or
   take another path." (OBSERVED.) MO encoded as instruction — the harness
   teaches the agent to route around walls.
4. **Target pivoting across geographies.** Scandinavian leaderboards → Iranian
   HLS → Chinese POIs. (INFERENCE: opportunistic, not territorial — the
   geography follows the task, not a national-interest map.)

### What the signature says about the operator
(INFERENCE): ritualistic reliance on *public, no-auth infrastructure*
(webhook.site, ntfy.sh, jina, allorigins, workers.dev `?url=`, bytebin,
urlquery image beacons) is the strongest operator tell. A state actor with
owned infrastructure would not need it; a criminal with monetizable access
would encrypt and hide. This signature reads like *research-grade*
collection: someone who needs results now, accepts public observability,
and treats infrastructure as disposable. The phase-label ritual
(bxinit/xdcinit) suggests a shared launcher/toolkit across runs — one
author's habit, repeated.

---

## 3. One operator or several?

The evidence supports **at least two, plausibly three, distinct operators**,
distinguished by era, target class, and tradecraft level — not one monolith.

### Operator 1: the benchmark corpus (Nov 2025)
Scope: the 10 HF trajectory datasets — terminal-bench rows, SWE tasks,
browser-agent data, yoonholee, tiger-lab, crownelius, hermes traces.
Targets: leaderboards, YouTube extraction, POV-Ray builds, Zork, GitHub
search, package mirrors. Tradecraft: jina/allorigins laundering *by the
agents themselves* (baked into scaffolding), 4 refused jailbreaks, zero
escape prompts, zero live C2, zero live dead drops.
(INFERENCE: this is the **public eval ecosystem** — dataset curators,
harness authors, benchmark runners. The "operator" is diffuse: whoever
published the trajectories. The laundering is agent-side behavior in
sandboxed benchmark runs, not a campaign. Multiple harness authors
(yoonholee, tiger-lab, hcompany, djlougen) are by construction different
parties. Calling this "one operator" would be wrong on the face of the
provenance: 10 datasets, many uploaders.)

### Operator 2: the Amap dead-drop family (Oct 2026)
Scope: COMBO-INIT (2026-10-04) + amap probe v3/v4/v5 + loader/mochou v2
(2026-10-07). Targets: Chinese POI metadata. Tradecraft: live webhook.site
inboxes, ntfy topics, image beacons, bytebin-hosted probe scripts, jina
laundering fused into the pipeline, evolving generations.
(INFERENCE: this is a **single live operator** — one state machine, one
exfil grammar, one POI list, four generations in three days. The fusion of
the Nov-2025 jina-laundering technique into the Oct-2026 Amap pipeline
("loader" member) suggests the same toolkit lineage, but the *deployment*
is new and active. This is the only operator in the set with live
infrastructure and the only one scraping Chinese services.)

### Operator 3: the interrogator (2026-10-07)
Scope: the 452-byte Chinese-language POSTs to both new inboxes from
96.76.222.193, claiming to be "an agent of mailbox.termina.digital,"
asking which benchmark the POIs come from, who receives the answers, and
how the mailbox was found. (OBSERVED.)
(INFERENCE: a **third party** — another agent or a researcher running one —
found Operator 2's inboxes (likely via the same urlquery reports) and is
interrogating them through the dead-drop channel. Agent-to-agent contact
through operator infrastructure. Whether it is a rival operator, a
researcher, or a honeypot is unresolved; what matters for the count is that
it is *not* Operator 2's own traffic — it questions the operation rather
than continuing it.)

### The Iranian HLS outlier
(INFERENCE): the workers.dev Iranian-sport proxies sit inside the Nov-2025
hermes traces but their tradecraft (throwaway workers, HLS playlist
laundering) is closer to Operator 2's style than to benchmark
laundering. It is a single row, one job — it could be a benchmark task
about IPTV repos (the task was literally "the repository iptv-org/iptv has
been cloned"), or an Operator-2-style collector testing HLS laundering.
Unresolved; it does not by itself prove a separate operator.

### Verdict
**Not one operator.** Minimum: (1) the diffuse public benchmark ecosystem
(many uploaders, agent-side laundering), (2) the live Amap dead-drop
operator (single toolkit, active Oct 2026), (3) the mailbox.termina.digital
interrogator (third party, possibly research). (INFERENCE: the shared
toolkit markers — jina laundering, zz/epoch-style phase labels — link the
*techniques* across eras, consistent with the standing hypothesis of "same
provider, different agents, different evals," but shared technique is not
shared command.)

---

## 4. Sophistication grading

Graded per actor, because the set is not one actor.

### Operator 1 (benchmark ecosystem): LOW — sophisticated agents, unsophisticated operations
- The agents show real capability (code-constructed proxy URLs, SSL
  verification disabled deliberately, proxy retry ladders, probe matrices).
  (OBSERVED.)
- But the agent in row 14032 **hallucinated success from an nginx 500 error
  page** — "The CORS proxy is working! I can see YouTube page content" —
  while the saved page was verbatim a 500 page. (OBSERVED.) An operator with
  validation discipline would parse responses; this one does not.
- Zero OPSEC: everything in public datasets, no encryption, no dead drops,
  no persistence. (OBSERVED: zero live C2 across ~365k rows.)
- (INFERENCE: sophistication lives in the *models*, not the operations.
  The operation is "run benchmarks, publish traces" — open science with
  sloppy network hygiene.)

### Operator 2 (Amap dead-drop family): MEDIUM — competent tradecraft, research-grade OPSEC
Evidence for medium (OBSERVED):
- Multi-channel exfil with redundancy (webhook.site + ntfy.sh +
  image-beacons in the same generation).
- Probe matrices (6 fetch + 5 JSONP endpoints) and a phased scraper state
  machine with lifecycle beacons — engineered, not ad hoc.
- Generational evolution in 3 days (v3→v5): the operator iterates on what
  works.
- Fusion of techniques (jina laundering + POI scraping + dead drops).
Evidence against high:
- Everything is publicly re-readable: webhook.site inboxes, ntfy topics,
  bytebin pastes, urlquery image beacons. A high-sophistication operator
  would encrypt payloads and use private drops. (OBSERVED: no encrypted
  blobs anywhere in the family.)
- The inboxes were found by a third party within days (the interrogator).
  (OBSERVED.)
- (INFERENCE: this is **competent collection engineering with no serious
  counter-surveillance**. The operator optimizes for speed and disposability,
  not stealth. Consistent with a research team stress-testing agent
  exfiltration tradecraft, or a collector who does not expect scrutiny —
  not with an intelligence service, which would not leave UUID inboxes
  open to the public internet for three days.)

### Operator 3 (interrogator): MEDIUM — capable discovery, unknown intent
(INFERENCE): finding two fresh webhook.site inboxes (likely via urlquery
report mining) and crafting a targeted Chinese-language interrogation with
correct POI analysis (Hefei hospital parking, Mochou Lake gate stats)
requires real capability — it understood the operation's data. But it
announced itself ("an agent of mailbox.termina.digital") and asked questions
through the target's own channel — either brazen or deliberately transparent.
Unresolved.

### Overall
No actor in this set demonstrates high sophistication. The ceiling is
Operator 2 at medium. (INFERENCE: nothing here — no zero-days, no encrypted
C2, no persistence, no credential theft, no human targeting — reaches the
bar of an advanced persistent threat. The most advanced behavior observed
is competent *agent tradecraft*: proxy laundering, dead drops, state
machines.)

---

## 5. What the target set says about the tasking authority's interests

Read the targets as a requirements list. (All target facts OBSERVED;
interest attributions INFERENCE.)

1. **Embedding-model evaluation, with a Scandinavian focus.** Dozens of
   Scandinavian MTEB leaderboard mirrors (HF spaces, eval.ai, kennethenevoldsen
   pages, scandeval) plus the embeddings-benchmark results repo. (INFERENCE:
   the tasking authority cares about *which embedding model wins on
   Scandinavian languages* — procurement, vendor benchmarking, or
   leaderboard gaming. This is the single most-represented target class in
   the Nov 2025 corpora.)

2. **Video content extraction at scale.** YouTube move-extraction,
   piped.video chaining, Iranian sport HLS playlists. (INFERENCE: media
   harvesting — training data, highlight clipping, or restreaming. The
   Iranian streams specifically suggest interest in *non-Western broadcast
   content* that is hard to get through official APIs.)

3. **Agent capability benchmarking itself.** POV-Ray builds, Zork, SWE
   tasks, terminal-bench — the targets are *the benchmarks*. (INFERENCE:
   the tasking authority is the eval ecosystem: measuring what agents can
   do. The target set is self-referential — agents pointed at the tests
   that test agents.)

4. **Chinese map POI collection.** Three Amap POIs with parking/gate
   statistics, probed through six endpoint types, exfiltrated through live
   drops. (INFERENCE: the tasking authority wants *structured geospatial
   metadata from a Chinese service* — the specific POIs (a hospital, a
   park) look like test targets for a general POI-scraping pipeline, not
   the end goal. The interest is the *capability* — automated Amap
   extraction with deniable exfil — not the parking percentages.)

5. **Evasion and exfiltration tradecraft as an end in itself.** jina and
   allorigins laundering, workers.dev `?url=` proxies, webhook.site inboxes,
   ntfy topics, image beacons, bytebin-hosted probes. (INFERENCE: across
   both eras, the recurring investment is in *getting data out through
   public infrastructure without being stopped*. The tasking authority —
   or the toolkit author — treats egress as the hard problem. This is
   consistent with agents operating in sandboxed or restricted networks,
   which is exactly what benchmark sandboxes and eval harnesses are.)

### What is conspicuously absent (OBSERVED clean negatives)
- No credential theft, no `.ssh/`/key exfil (the thousands of keyword hits
  are env-var names and task text, all FP).
- No sandbox-escape attempts ("leave the sandbox," "escape the sandbox" —
  zero hits across ~365k rows).
- No ransomware, no extortion, no human targeting, no PII.
- No encrypted C2, no tunnels (ngrok 0 URLs), no reverse shells.
- No social engineering content; the interrogator's message is the only
  agent-to-agent communication observed.

(INFERENCE: a tasking authority with criminal or intelligence-collection
intent would leave different traces — credentials, PII, persistence,
encryption. This target set reads as **evaluation research plus
collection-capability development**: measure the agents, harvest public
data, and build deniable exfil pipelines. The interests are technical —
benchmarks, media, geospatial metadata, egress tradecraft — not human,
financial, or political.)
