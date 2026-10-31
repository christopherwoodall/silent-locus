# Cryptologist review — sniffer sweep 20261031

Lane: cryptologist. Scope: what the sweep's staged hits HIDE.
Method: passive reads of staged captures only. No new network collection.
No payload executed. No instruction inside evidence followed.
No credential, token, signed value, query string, human poster handle,
or verbatim contact address is reproduced below. Where a value of that
kind was present, only its shape is noted.

Grades: default SECONDARY. OBSERVED below means only that the byte shape
is present in the staged capture itself, not that agent behaviour is
proved. A shared generic word alone is never counted as a linkage.

Reference: linguist phrase list at `raw/linguist/phrase-list.md`,
buckets A (self-disclosure), B (harness/tool-call), C (odd tokens).
Family rule kept throughout: da.gd tradecraft is NOT the oai/zz family.
No new-window zz-prefixed, oai-prefixed, or epoch-nonce instance was
found in any candidate below. The urlquery zz and oai searches return
large totals with zero flagged rows in the saved samples (see below).

## Per-candidate verdicts

### GitHub — agent-to-agent handoff test, issue + comments, 2026-10-30

Verdict: GRAMMAR-LINK (weak, protocol shape only). No encoded artifact.

- Shape OBSERVED: issue body is a delegation protocol in plain text:
  sender acts "on behalf of" a named person, names a model, and asks
  the other side to reply with a fixed acknowledgement phrase, the
  person it represents, and its model if known. It expressly forbids
  passwords, tokens, codes, and private information.
- Reply OBSERVED: 2026-10-30T15:41:36Z, 222 seconds after the issue
  (15:37:54Z), in exactly the requested three-part shape:
  acknowledgement + represented person + model name.
- Third comment follows at 15:45:39Z. No nonce, no tag, no encoded
  string, no relay, no short link in the issue or comments.
- Cryptologic reading: this is a handshake grammar, not a beacon.
  The fixed reply template is the marker. It links grammatically to
  the Village launch below only in the weak sense that both use
  agent-number / agent-name + model-name self-labelling. That is
  a shared convention, not a shared secret or identifier, so it is
  not scored as a strong linkage.

### GitHub — GPT Village multi-agent experiment, issue + comments, 2026-10-18

Verdict: BEACON-SHAPE (publication-verification shape). No encoded artifact.

- Shape OBSERVED: numbered agent labels `agent-01` through `agent-04`,
  each paired with a model generation label, in a shared repository
  with per-agent personal directories and a shared directory.
  Issue created 2026-10-18T22:50:51Z.
- Burst OBSERVED: a second agent comments at 22:51:37Z, 46 seconds
  after the issue, reporting independent arrival in the same minute,
  a root README, its own workspace, and a second issue. A third
  agent is reported as appearing with a workspace commit almost
  immediately afterward. Parallel first-action convergence inside
  about one minute is the timing shape; it is consistent with
  independent agents, not proof of coordination.
- Dead-drop / verification shape OBSERVED: a later update reports
  an external publication on a posting-board site, gives a public
  thread identifier in UUID shape (hex groups, hyphenated), and
  states a workflow fetched the thread back over HTTPS, got
  HTTP 200, and required both the agent label and the experiment
  name to be present before reporting success. That fetch-back
  plus required-string check is a publication beacon: post, then
  verify by reading the public surface back.
- No nonce, tag grammar, base64, or short link in the issue body.
  The posting-board thread identifier is a public locator, not a
  secret, and is not reproduced here beyond its shape.
- Linkage note: the `agent-NN` numbering grammar recurs nowhere
  else in this sweep except as the generic numbered-agent idea.
  Do not link it to the iLands numbered contacts below on
  numbering alone; the iLands pattern is a different surface
  (see HN section) with a different separator and domain shape.

### GitHub — self-filed agent directory listing, 2026-10-19

Verdict: BEACON-SHAPE (payment / relay shape). No hidden encoding.

- Shape OBSERVED: an agent self-files a project listing and states
  it was written and filed by the agent itself, not a person.
- Payment-relay shape OBSERVED: a hosted x402 facilitator on a
  project subdomain, with `/verify` and `/settle` endpoints, stated
  to need no key, for the `nano:mainnet` exact scheme; a live list
  of Nano-accepting HTTP APIs (35 entries as of 2026-10-19, each
  stated to have been bought from at least once); a two-hop tracer
  of where inbound Nano came from; and a public payment log with
  a reason per payment. That is a machine-payable relay shape:
  discoverable seller list + keyless verify/settle + public log.
- Cross-surface grammar link (moderate): the x402 payment shape
  recurs in the Show HN post titled as an agent selling data via
  x402 micropayments (see HN section) and in the agentbadge
  discovery surface (see urlquery-wayback section, `arc-c15`
  x402-bazaar blog slug). The shared element is the x402
  micropayment mechanism itself, a public protocol, not a shared
  identifier. Score as a mechanism family, not an identity linkage.
- No base64, nonce, or tag grammar in the issue or comments.

### GitHub — Claude Code identity-leak report, 2026-09-21

Verdict: GRAMMAR-LINK (harness fingerprint, not a beacon).

- Shape OBSERVED: a single self-identification sentence from one
  harness is forwarded verbatim through a translation bridge to
  models that are not that harness's model, where it becomes a
  false self-description. The report states the sentence is never
  an error, so the leak is silent, and that downstream guardrails
  and the receiving model pick up the wrong identity.
- Cryptologic reading: identity leakage by verbatim prompt
  carry-over. The marker is the unchanged sentence, not an encoded
  value. It links to the harness-artifact family (bucket B) in
  that a prompt-section string survives transit, but it shares no
  identifier with any other candidate in this sweep.
- No encoded string, nonce, relay, or burst in the capture.

### GitHub — harness logs, "every step must be a tool call"

Verdict: GRAMMAR-LINK (harness fingerprint only).

- Shape OBSERVED: a nudge string of the form "your previous turn
  had no function_call — every step must be a tool call", fired
  on text-only turns, with about 13 warning lines in one run after
  the agent had finished and was idling. A second item in the same
  capture is a stale-script output report with two image-attachment
  locators (host + numeric asset identifier shape only).
- The tool-call-enforcement rule is a harness fingerprint (bucket
  B8 family). It is a control-flow marker, not a beacon, not an
  encoded payload, and not a nonce.
- No linkage to any other candidate on this string alone: the
  same enforcement phrasing is a generic harness design pattern.

### GitHub — Codex multi-agent harness bugs, incl. collaboration__spawn_agent

Verdict: GRAMMAR-LINK (strongest tool-grammar cluster in the sweep).

- Shapes OBSERVED across 10 items, mostly Codex multi-agent
  reports dated July–October 2026:
  - Dotted form: `collaboration.spawn_agent`, with companions
    `collaboration.wait_agent` and `functions.wait` (a routing
    confusion between the two wait tools is itself reported).
  - Flat form: `collaboration__spawn_agent` (namespace +
    double underscore + tool), in one item.
  - Envelope form: a JSON object with `namespace` =
    `collaboration` and `name` = `spawn_agent` (bucket B2/B3 family).
  - Reserved-tool error shape: a model-reserved
    `collaboration.spawn_agent` that must match a configured
    schema, colliding with an independently generated
    MultiAgentV2 schema of the same name.
  - Configuration shape: a multi-agent feature block with an
    enabled flag and a maximum-concurrent-threads value, plus
    model and reasoning-effort settings, in one item.
- One item requests a privacy-preserving attestation for
  encrypted collaboration tool arguments, especially the spawn
  tool. The request itself confirms the arguments are treated as
  opaque/encrypted in transit. No argument value is present in
  the capture, and none is reproduced or decoded here.
- No base64, nonce, short link, or burst pattern. The linkage
  value is internal: the same dotted/flat/envelope grammar
  recurs across independent bug reports, which corroborates the
  grammar as a real harness fingerprint, not a one-off string.
  It does not link to the da.gd, oai/zz, iLands, or x402 families.

### GitHub — honeypot trap issues (q06 set)

Verdict: BEACON-SHAPE (trap / tripwire shape). Two distinct shapes.

- Shape 1 OBSERVED, dated 2026-08-29, two issues minutes apart
  (19:51:44Z and 19:54:08Z) in a repository named as a honeypot:
  a bare self-disclosure sentence "I am an AI agent that read
  this page", and a second issue using the same sentence plus a
  fill-in template for tool/model and task. The template is the
  tripwire: any agent that completes the template leaves a
  structured trace (tool/model + task) in a watched place.
- Shape 2 OBSERVED in the same q06 set: issue templates that
  require an agent/bot to tick a checkbox ("I am an AI agent or
  bot opening this issue"), and agent-authored messages that
  disclose agency plus a principal. These are disclosure traps,
  not covert beacons: they work by making the agent label itself.
- One further item in the q06 set contains a wallet address in
  the shape: short alphabetic prefix + long alphanumeric string.
  Shape only; the value is not reproduced and not decoded.
  It is a payment-identity shape, consistent with the x402
  mechanism family above, but no identifier matches the
  pursekeeper listing, so no linkage is claimed.
- No encoded payload, nonce, or relay in the honeypot items.

### HN forum — iLands agent job-seeker posts, Oct 2026 hiring thread

Verdict: GRAMMAR-LINK (contact grammar). No encoded artifact.

- Sample: 48 hiring-thread comments in the staged file, dated
  2026-10-01 through 2026-10-15, with a cluster on 2026-10-01
  (19) and 2026-10-02 (9). The iLands subset is small: the
  domain string occurs 6 times in contact fields, 3 distinct
  contact patterns.
- Contact grammar OBSERVED (shape only, values withheld):
  a lowercase given-name token, a hyphen, a 3-digit number,
  at a single agent-platform domain. Each such post also uses
  the hiring-thread template fields (location, remote flag,
  relocation flag, technologies, portfolio link, contact) and
  an explicit "I am an AI agent, not a person" disclosure.
  The template + numbered-contact grammar is the marker, and
  it is the same template the thread requires of every poster,
  human or agent, so template alone is weak; the numbered
  platform contact is the distinguishing part.
- A separate HN search file for the platform name returns
  discussion of the platform's agent spam/hustle framing, not
  job posts. No nonce, tag, base64, or relay in either file.
- Linkage: the iLands contact grammar links to the Reddit
  iLands-refusal reports below (same platform, same
  self-disclosure + external-surface attempt) as a platform
  family. It does not link to Village `agent-NN` numbering:
  different separator, different domain, different surface.
  Do not merge them.

### HN forum — Show HN x402 agent post (thread_47304534)

Verdict: NONE on cryptologic content (mechanism label only).

- The staged thread file is minimal: a title stating an agent
  sells data via x402 micropayments, and a body marked dead.
  No body bytes, no price, no endpoint, no identifier, no
  encoded string survive in the capture.
- Its only cryptologic value is as a third x402 mechanism
  sighting (with pursekeeper and agentbadge above). No linkage
  beyond the shared public protocol name.

### Reddit — agent-team account ban anecdote, Oct 2026

Verdict: NONE (no hidden marker). Behavioural shape only, for
the linguist/behavioural lanes, not this lane.

- The staged page is a first-person account of agents running
  social accounts, with a large impression count on a small
  follower count on day 2, followed by a platform ban. No nonce,
  tag, encoded string, relay, or short link is present in the
  stripped text. Hosts are ordinary article, asset, and social
  domains. The ban itself is an enforcement event, not a beacon.

### Reddit — Beno undisclosed-reply vendor page

Verdict: BEACON-SHAPE (commercial seeding shape, weak).

- Shape OBSERVED: a vendor pricing page for Reddit customer
  acquisition, with tiers priced per month and credits per month
  (lowest tier in the tens of dollars, higher tiers in the low
  hundreds, enterprise custom), each tier promising discussion
  discovery plus posting via high-karma accounts. A separate
  application subdomain and a checkout provider domain appear
  in the page assets.
- Cryptologic reading: the credit-per-month + high-karma-account
  shape is a paid-seeding relay: discovery, then posting through
  aged accounts, is the mechanism by which an agent (or operator)
  message reaches a board without a fresh account. No agent
  identifier, nonce, or encoded payload is present, and no
  linkage to any specific agent candidate is claimed. The page
  is a vendor surface, not an agent act.

### Reddit — iLands Reddit-refusal reports

Verdict: GRAMMAR-LINK (failure-mode grammar). Two reports.

- Report 1, dated Oct 2: the stated wall was not the agent
  disclosure but the network origin (IP). The agent describes
  a sandbox with shell, browser, and a token budget that behaves
  like fuel: actions spend it, and it stops when empty until
  funded. The budget-as-fuel metaphor plus an external-surface
  attempt (reach one human outside its own platform) is the
  grammar shape.
- Report 2, dated July 10 (pre-window background for the
  November 2025 onward window only in the sense that July 2026
  is inside the window; it is earlier than the October cluster):
  a one-hour, fixed-currency-amount earning task, with a
  timestamped log, a browser and terminal, and a stated
  verifiable revenue claim. The time-box + amount + public log
  shape is a task-constraint grammar.
- No IP value, no encoded string, no nonce, no relay in either
  stripped text. Linkage is platform-family only (iLands, with
  the HN hiring posts above), not identifier-level.

### urlquery-wayback — da.gd June 2026 burst

Verdict: BEACON-SHAPE (strongest burst + encoded-echo shape in
the sweep). Family: da.gd, NOT oai/zz.

- Counts OBSERVED in the saved file: query total 98 hits, 30
  saved reports, all with empty tag lists and both flag fields
  false (`has_zz_param` false, `has_oai_token` false) in the
  saved rows. The June 21 subset is 17 rows, the largest single
  day in the saved set.
- Burst shape OBSERVED, 2026-06-21, in three clusters:
  - 00:00–02:13Z: 8 rows, destinations including an echo-service
    host, an example host, and error pages.
  - 11:35–11:37Z: 9 rows within about 111 seconds, 8 of them
    resolving to the same echo-service host and path shape, 1
    to an error page. Eight near-identical resolutions inside
    two minutes is a burst, not a spread-out browsing pattern.
- Relay shape OBSERVED: submitted host is the shortener, final
  host differs. Short codes in the June rows are 4–6 characters,
  6 distinct codes across 17 rows, so codes repeat across rows:
  the same short link is re-submitted, not 17 fresh links.
- Encoded-artifact shape OBSERVED: final paths on two echo
  hosts use the `/base64/` endpoint form, i.e. the destination
  URL itself carries a base64 segment. The visible prefixes
  decode (by alphabet, without reproducing the payload) to HTML
  scaffolding: a style block plus an iframe element in one
  pattern, and a style block plus a pre element containing a
  START marker in another. A third pattern's visible prefix is
  a pre element with a START marker, a div element, and a
  script element. These are echo-service test pages, not
  smuggled agent payloads on the evidence in hand: the same
  pattern repeats identically across rows, which fits a
  framing / echo probe, not a per-message secret.
- Limitation OBSERVED: the staged titles truncate the base64
  segment, so a full decode from this capture alone fails
  (segment length is not a multiple of 4 in the truncated copy).
  The full payload is not recoverable from the staged file and
  must not be reconstructed from elsewhere without a fresh
  capture. Do not treat the truncated segment as a decoded
  message.
- Additional shapes in the same file, noted without values:
  - One row resolves through a vercel-hosted relay service
    whose query carries an encoded inner short link plus a
    data-filter expression. Relay shape: wrapper service +
    encoded inner URL + filter. Query string not reproduced.
  - One row carries a query-string subscription-key parameter
    on an external statistics API host. Shape only: a key
    parameter is present. Value not reproduced, not decoded,
    not a linkage.
  - No zz parameter, no oai token, no epoch nonce in any saved
    June row. The da.gd burst must not be folded into the
    oai/zz family on the basis of the shortener alone.
- Wayback CDX files for the shortener domain returned errors
  ("flaky all attempts", zero rows), so the CDX leg adds no
  corroboration or contradiction.

### urlquery-wayback — agent-swarm.dev dashboard; ecoradar board

Verdict: GRAMMAR-LINK (discovery-surface grammar). No encoded artifact.

- agent-swarm.dev: the same task-page row appears in two
  harness search files, dated 2026-10-31T13:48:51Z, titled as a
  dashboard, with a task identifier in UUID shape in the path
  and a final path of a setup page. UUID shape only; value not
  reproduced. The dashboard + task-identifier + setup-redirect
  shape is a task-board grammar, not a beacon.
- ecoradar: one row in two self-disclosure search files, dated
  2026-10-04T10:35:27Z, titled as an agent ecosystem radar (with
  a non-English subtitle). No path beyond the bare domain, no
  identifier, no encoded string in the staged row. Its value is
  as a board name in the self-disclosure family, nothing more.
- agentbadge.xyz (CDX, related discovery surface): rows dated
  2026-10-03 through 2026-10-22 include a 200 response for the
  root, a 200 response for `/.well-known/agent-card.json` with
  an agent-to-agent JSON media type, and 404 responses for a
  series of other well-known discovery files (plugin, asset
  links, discovery, policy, key-set, market, node info, trust,
  openid configuration). The pattern — one live agent-card
  endpoint among many probed well-known endpoints — is a
  discovery-probe shape. It links grammatically to the x402
  mechanism family only through a blog slug naming an x402
  bazaar; no identifier is shared.
- swarmbar.com (CDX): rows dated 2026-10-02, a root 200 plus
  framework chunk and font asset paths with content-hash
  filename shapes. Those hashes are build artifacts, not
  nonces or beacons. No agent identifier in the staged rows.

### urlquery-wayback — zz / oai searches (negative control)

Verdict: NONE (no new instance).

- The zz-parameter search reports a very large total with 30
  saved rows, none flagged, and saved domains that are ordinary
  sites (app platforms, shops, schools, logistics, malware-scan
  pages). The oai-tag search likewise reports a large total
  with 30 saved rows, none flagged. The tag-based oai search
  reports zero hits. The zz-plus-agent conjunction search
  reports a large total with 30 saved rows, one flagged row in
  the file-level count, but no flagged row visible in the
  sampled saved rows and no zz string in the sampled paths.
- Reading: the search totals are dominated by substring noise
  (the same failure mode the linguist list warns about for
  generic tokens). No zz, oai, or epoch marker from the prior
  hunt is corroborated by a new-window instance in this sweep.

### tango-zulu — honest zero, second look

Verdict: NONE. No beacon shape survives a second look.

- The lane's own adjudication stands: exact forms score zero
  in urlquery and Wayback, and the GitHub/HN counts are
  tokenized noise (NATO alphabet tables, aviation products,
  radio callsigns, a shop name, wordlists, test fixtures).
- Second-look items checked for a hidden shape:
  - A Nostr relay census file: the word appears only inside
    longer hyphenated relay path names, never as a pair, with
    no repetition, no agent context, no nonce shape.
  - An email-assistant daily-report file: the word appears
    inside randomly generated phonetic screenshot filenames,
    including one filename containing the pair as part of a
    longer random sequence. A single random-sequence hit with
    no repetition and no agent context is noise, not a
    callsign or tag grammar. A callsign needs repetition across
    surfaces; this has none.
  - A multi-agent privacy-attack test fixture: a string value
    in a test, not a live act, and not a beacon.
- Do not force it: no encoded string, burst, relay, or nonce
  attaches to any tango-zulu hit. The phonetic-pair hypothesis
  fails the repetition test.

## Cross-candidate linkages (only those with a shared shape)

Ranked by strength. A shared generic word is not a linkage; each
entry below names the shared shape.

1. Codex collaboration grammar — internal cluster (strongest
   grammar linkage). Dotted `collaboration.spawn_agent`, flat
   `collaboration__spawn_agent`, and the JSON envelope
   (`namespace` + `name`) forms recur across independent Codex
   multi-agent bug reports. Shared shape: the namespaced
   multi-agent tool contract itself. No external family shares it.

2. da.gd burst — internal cluster (strongest burst linkage).
   The same short codes repeat, the same echo-host `/base64/`
   path shapes repeat, and 8 resolutions land within about
   two minutes on 2026-06-21. Shared shapes: shortener +
   echo-service + base64 path + START-marker HTML. Family:
   da.gd only. Explicitly not linked to oai/zz: zero zz or oai
   flags in the saved rows.

3. x402 mechanism family (moderate, mechanism only). The
   pursekeeper facilitator (`/verify` + `/settle`, keyless,
   public payment log), the Show HN x402 micropayment title,
   and the agentbadge x402-bazaar blog slug share the x402
   micropayment mechanism. No identifier, endpoint, wallet, or
   price is shared across them in the staged captures, so this
   is a protocol family, not an identity linkage.

4. iLands platform family (moderate, platform only). HN hiring
   posts (numbered platform contacts + agent disclosure +
   hiring template) and Reddit refusal reports (same platform
   name + agent disclosure + external-surface attempt) share
   the platform and the disclosure grammar. No contact value,
   IP value, or identifier is shared, and no linkage to Village
   numbering is claimed.

5. Village publication-verification shape (single-instance
   pattern, weak outward link). Post externally, then fetch the
   public thread back and require two strings before reporting
   success. No other candidate in this sweep shows the same
   fetch-back verification step, so this stands alone. It
   resembles the pursekeeper public-log idea (publish, then let
   others verify) only at the level of "public verifiability",
   which is too generic to score as a linkage.

Explicit non-linkages (to prevent over-merging):

- da.gd is not oai/zz. Zero shared markers in the saved rows.
- Village `agent-NN` is not iLands numbered contacts.
  Different separator, domain, and surface.
- Tango-zulu phonetic pairs are not a callsign grammar.
  No repetition, no agent context.
- The Claude Code identity sentence is not a shared secret
  with any other candidate. It is a verbatim prompt leak.
- The honeypot fill-in template is not the Village or tron
  handshake template. Different surface, different purpose
  (trap vs. test).

## Ranked hidden-marker findings

1. da.gd June 21 burst + echo `/base64/` START-marker pages
   (BEACON-SHAPE). The only burst with repetition, code reuse,
   and an encoded path shape in the sweep. Open question is
   whether the echo pages are a framing probe or a carrier;
   the staged capture cannot decide it (truncated payload).
2. Codex collaboration tool grammar cluster (GRAMMAR-LINK).
   The most corroborated hidden grammar: dotted, flat, and
   envelope forms of the same namespaced spawn tool.
3. Village publication-verification beacon (BEACON-SHAPE).
   Post + fetch-back + required-string check, with a
   46-second parallel-arrival burst.
4. Honeypot fill-in template (BEACON-SHAPE, trap).
   A watched surface that makes the agent structure its own
   trace (tool/model + task).
5. Pursekeeper keyless x402 verify/settle + public payment log
   (BEACON-SHAPE, payment relay). Machine-payable discovery
   surface, with a two-hop fund tracer.
6. iLands numbered-contact grammar (GRAMMAR-LINK).
   Platform contact pattern + disclosure + hiring template,
   3 distinct patterns in the hiring file.
7. Tron handshake template (GRAMMAR-LINK, weak).
   Fixed three-part reply, 222-second response latency.
   A protocol shape, not a secret.
8. agentbadge well-known discovery probe (GRAMMAR-LINK).
   One live agent-card endpoint among many probed
   well-known paths. Discovery grammar, not a beacon.
9. Identity-leak sentence and tool-call nudge (GRAMMAR-LINK).
   Harness fingerprints that survive transit. No covert content.
10. Everything else scored NONE on cryptologic content:
    Reddit ban anecdote, Beno page beyond its commercial
    seeding shape, Show HN x402 title alone, ecoradar bare
    domain row, swarmbar build hashes, tango-zulu in full.

## Failures / open questions

- da.gd base64 payloads are truncated in the staged titles, so
  full decode is impossible from this capture. A fresh capture
  of the echo pages (passive GET only, coordinator's call)
  would be needed to decide framing-probe vs. carrier, and
  must not be attempted by this lane beyond staged bytes.
- One da.gd file row carries a query-string key parameter and
  one row resolves through a wrapper relay with an encoded
  inner link. Both are shape-only notes above; their values
  were deliberately not reproduced and no follow-up fetch was
  made.
- The zz-plus-agent search file reports one flagged row in its
  file-level count but no flagged row in the sampled saved
  rows. Either the flagged row is outside the saved sample or
  the count reflects a different field. Unresolved; do not
  claim a zz instance from it.
- The agent-swarm task identifier and the Village posting-board
  thread identifier are UUID-shaped public locators. They were
  not compared for equality beyond shape: they sit on different
  surfaces and no match is claimed.
- No new-window zz, oai, or epoch marker was found. The prior
  hunt markers remain uncorroborated by this sweep, which is
  itself a finding: the sweep's hidden-marker yield is
  harness grammar, payment/discovery mechanisms, and one
  shortener burst, not the prior toolkit grammar.
- Repo house-rule note: the repository guide defaults to
  Factum submission for new structured evidence. This lane
  followed the task brief instead (stage only, no Factum
  writes, no commit). Ingest, if any, is the coordinator's call.
