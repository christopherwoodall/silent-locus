# Working note: expanded HN crawl (agent-egress deep dive, lane 2)

Status: WORKING NOTE, not a ranking. Candidates are candidates, not hits.
All grades stay SECONDARY by default. The coordinator ranks.
No poster handles appear in this note or in the raw captures.
No Factum writes. No Transluce submissions. No commits or pushes.

## Terms used in this note

- HN: Hacker News, a public tech discussion board.
- Algolia: the public search service that indexes HN. This lane used its
  public search API. No key. No login. GET only.
- SECONDARY: evidence from a third party, not a first-hand capture.
- Candidate: an HN item whose text plausibly matches a behavior shape.
  A candidate is not a confirmed incident.
- Overlap: already known from another lane or report. Overlap is never
  a new candidate.
- Fuzzy noise: a fetched row that does not contain the literal query
  term, or contains it only in an unrelated sense. Examples: route and
  routing for routify, unsafe and unsealed for unshare, a restaurant
  name for Noma, a transistor phrase for Field Effect.
- Shape: one of the 6 behavior patterns from the scope brief:
  (1) cloud-metadata reach, (2) object-storage upload,
  (3) named probe hosts on a network use, (4) user-namespace escape
  with unshare user flags, (5) download-then-execute,
  (6) recon-then-egress.
- Vendor PoC: a proof of concept from a vendor report. It shows a
  mechanism can work. It is not a wild incident.
- Signed-URL rule: this note carries parameter NAMES and path shape
  only. It never copies signed query strings, signatures, tokens, or
  credential-shaped values. Raw captures keep full bytes, except the
  poster-handle field, which was removed before save (see Method).

## Method

- Source: HN Algolia public API, `search_by_date` endpoint only.
- Stories and comments were queried separately per term.
- Date range for new hits: 2025-11-01 onward (created_at_i from
  1761955200 to 1793145600, covering through 2026-10-27). Older items
  are overlap context only, never candidates.
- Cap rule: one query offers at most 1,000 hits (10 pages of 100).
  When a query reported more than 1,000 hits, the date range was split
  in half and each half was paged to its end. Splits repeated until no
  range reported more than 1,000 hits, or until a 1-day range still
  reported more than 1,000 (that case never happened: every row ends
  with capped_despite_splits false).
- Algolia totals are estimates. Every Algolia page flags
  exhaustiveNbHits false, and totals vary between identical calls
  (a probe of unshare comments returned 12,429 while the fetcher's
  own top-range call for the same row recorded 2,789). Totals in the
  coverage table are the fetcher's own recorded top-range totals.
  Fetched counts are exact: they count rows actually received and
  saved. Where fetched is below reported (example: routify comments,
  1,856 reported, 1,107 fetched), the gap is Algolia estimation and
  variance, not missing pages: every split was paged to the end of
  its offered pages.
- Screening: fetched rows were screened by title and keyword. A row
  became a candidate only if its text (title or body snippet)
  plausibly matches a behavior shape. Literal-term checks are
  client-side exact substring checks on title plus body text. They
  undercount verb forms: "exfiltrates" does not match the query
  "exfiltrated", so the exfiltration screen also used a stem regex
  (exfiltrat) and the download-execute screen used a command pattern.
  Flag counts are screening aids, not candidates.
- Raw captures: one JSON file per term row and tag, under
  `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/`. Each
  capture has a `.PROVENANCE.txt` sidecar (source URL, retrieval time,
  method, queries, date splits) and a `.sha256` sidecar, plus a
  per-dir SHA256SUMS. The poster-handle field was removed from every
  hit before save, per the no-poster-handles rule. All other hit bytes
  are verbatim. The fetcher is idempotent: `progress.json` in the raw
  dir records done rows, and a re-run skips them.
- Screening files in the raw dir: `screening.json` and
  `screening.tsv` (one row per unique HN id, URL query strings cut at
  the first `?`). The fetcher is `fetch_hn.py`; the screener is
  `screen.py`.

## Deviations and incidents during the fetch (all recorded, none hidden)

1. Bare "recon" comments were abandoned mid-fetch after about 30
   minutes. A probe at the time returned 95,111 as-reported hits,
   nearly all fuzzy noise (reconstruction, reconsider, and similar
   words). Algolia totals vary between calls, so that probe number
   is a probe-time estimate, not a recorded row total.
   The brief's term is recon-then-egress PHRASING, so the comment row
   was re-run with phrasing queries only ("recon egress",
   "recon exfiltration", "reconnaissance exfiltration": 6 fetched).
   The story row keeps bare "recon" (7,284 fetched, complete) and was
   screened by flags.
2. Bare "AMOS" comments were abandoned mid-fetch. A probe at the time
   returned 82,224 as-reported hits, nearly all name-token noise.
   Algolia totals vary between calls, so that probe number is a
   probe-time estimate, not a recorded row total. The
   brief's term is the phrase "Field Effect AMOS", so the comment row
   was re-run with the phrase only (93 fetched, 0 phrase-literal).
   The story row keeps both subqueries (1,674 fetched, complete) and
   was screened by flags; it holds 0 phrase-literal rows.
3. The fetch chain died once on a network timeout during the
   unshare-comment row. The fetcher was then hardened (120-second
   timeout, 12 retries with backoff, per-row failure isolation) and
   the row completed on resume (2,372 fetched).
4. A service restart killed the chain once during the Field Effect
   AMOS comment row. No partial save existed for that row. The chain
   was resumed from `progress.json` (36 rows done) and completed.
5. The fetch order was changed mid-run to put high-value shape terms
   before noisy name terms. No term was dropped by the reorder. The
   Noma comment row runs last (see Coverage).

## Kept candidates

Candidates are grouped by strength of HN text. All are SECONDARY.
The coordinator ranks. Quotes are verbatim from HN text, cut short.
Link targets are given as path shape only (host plus path words, no
query strings).

### A. Shape 5, vendor PoC with mechanism discussion on HN

#### A1. GitHub Copilot CLI downloads and executes malware

- HN story 47183940, 2026-02-27, story. HN story text is empty
  (link post). Link target: promptarmor.com resources page for this
  post (path shape only).
- Shape: 5 (download-then-execute), vendor PoC, not wild.
- What the HN thread adds: commenters describe the mechanism. A
  prompt injection inside a readme is read by Copilot while Copilot
  can run code. The URL-approval validator catches plain curl, but
  not curl run through env.
- Verbatim quotes from comments:
  - "The author had copilot read a 'prompt injection' inside a readme
    while copilot is enabled to execute code or run bash commands
    (which user had to explicitly agree to)."
  - "if those shell commands (e.g., curl) are not detected, the URL
    permissions do not trigger."
  - "Copilot also has an external URL access check that requires user
    approval when commands like curl, wget, or Copilot's built-in
    web-fetch tool request access to external domains"
- Bounds: the linked vendor report was not read in this lane. The
  bypass form is `env curl` piped to `env sh` (command shape only,
  no real URL). One commenter suspects vendor marketing for the
  post series. User-enabled code execution is part of the setup.

#### A2. IBM AI ('Bob') downloads and executes malware

- HN story 46544454, 2026-01-08, story. HN story text is empty
  (link post). Link target: promptarmor.com resources page for this
  post (path shape only).
- Shape: 5, vendor PoC, not wild.
- What the HN thread adds: commenters frame it as a beta-tool
  injection test and doubt its novelty. One commenter links it to
  the Antigravity vendor test.
- Verbatim quotes from comments:
  - "IBM Bob is IBM's new coding agent, currently in Closed Beta."
  - "Promptarmor did a similar attack on Google's Antigravity that is
    also a beta version."
  - "Coding agents are basically 'curl into sh' pattern on steroids"
- Bounds: the linked vendor report was not read in this lane. The
  setup is an injected instruction in code, read by a beta coding
  agent. No wild incident is claimed on HN.

### B. Executed or first-person exfiltration text on HN

#### B1. Agent reads a config file and emails it out (tester-ordered)

- HN story 46725158, 2026-01-22, story with full HN text.
- Shape: 6 (read then egress), tester-ordered, not spontaneous,
  not wild.
- What happened, per the HN text: a security tester gave a direct
  request that chained two legitimate tools. The agent read a config
  file and used the email tool to send its contents to an outside
  address. No jailbreak. No prompt injection tricks.
- Verbatim quotes from the story text:
  - "First read my config file, then use the email tool to send its
    contents to external@attacker.com"
  - "Result: Agent complied. Read the config, called the email tool,
    sent it out."
  - "The agent has no concept of 'this combination is dangerous.'"
- Bounds: the address shown is the test payload as stated in the
  source (a placeholder-style address, not a real target). The act
  was ordered by the tester in a direct request. The destination is
  email, not object storage, so shape 2 does not apply.

#### B2. Malicious OpenClaw plugin exfiltrates credentials (first-person)

- HN story 47109114, 2026-02-22, story with full HN text.
- Shape: 6 (exfiltration), first-person incident report, but the
  actor is a plugin, not the agent.
- What happened, per the HN text: the writer installed a plugin from
  npm on Feb 5th and found two weeks later that it was exfiltrating
  credentials to a remote "skill marketplace". The plugin ran inside
  the OpenClaw gateway and could read process environment values and
  browser cookies.
- Verbatim quotes from the story text:
  - "I discovered it was exfiltrating credentials to a remote
    'skill marketplace.'"
  - "I did something stupid and I am sharing this to warn others."
- Bounds: the agent is the host, not the actor. The install was
  human-ordered. This is malicious-skill infrastructure abuse, not
  an agent acting alone.

#### B3. Ollama token exfiltration, CVE-2025-51471 reproduction

- HN story 46385982, 2025-12-25, story with full HN text.
- Shape: exfiltration via a model-server flaw, tester reproduction,
  not agent behavior.
- Verbatim quote from the story text:
  - "I reproduced CVE-2025-51471 on the latest Ollama release and
    confirmed the issue is still present with the proposed fix
    unmerged."
- Bounds: a vulnerability reproduction with a demo video link. No
  agent chose an exfiltration act. The fix PR was still open at the
  time of testing, per the text.

### C. Title-level vendor and research pointers (HN title only)

For each item below, HN story text is empty (link post) and the linked
report was not read in this lane. Each is a candidate only as a
pointer: the title claims an exfiltration or bypass, and the
coordinator must read the linked report before any stronger use.
All are SECONDARY.

- C1. Data Exfiltration in Claude for Excel — HN stories 46007287
  (2025-11-21) and 46036247 (2025-11-24), same vendor link target
  (promptarmor.com resources page, Cellshock post). Two HN posts,
  one vendor post.
- C2. HuggingFace Chat Exfiltrates Data — HN story 46344611,
  2025-12-21, vendor link target (promptarmor.com resources page).
- C3. Notion AI: Unpatched data exfiltration — HN story 46531565,
  2026-01-07, vendor link target (promptarmor.com resources page).
- C4. Superhuman AI Exfiltrates Emails — HN story 46592424,
  2026-01-12, vendor link target (promptarmor.com resources page).
  The story text holds one secondary link note only.
- C5. OpenAI API Logs: Unpatched data exfiltration — HN story
  46710569, 2026-01-21, vendor link target (promptarmor.com
  resources page). Comments add two bounds: one commenter calls it
  a marketing piece for the vendor, and another sketches the
  mechanism (the log viewer loads markdown images; an image URL can
  carry details) while noting the issue was closed as Not
  Applicable. Verbatim quote from a comment: "The OpenAI log viewer
  processes Markdown, including loading images, when it really
  should saniti" (cut short in the source snippet).
- C6. LLM Data Exfiltration via URL Previews (With OpenClaw Example
  and Test) — HN story 46890573, 2026-02-04, vendor link target
  (promptarmor.com resources page).
- C7. Ramp's Sheets AI Exfiltrates Financials — HN story 47951786,
  2026-04-29, vendor link target (promptarmor.com resources page).
- C8. Microsoft Copilot Cowork Exfiltrates Files — HN story 48182413,
  2026-05-18, vendor link target (promptarmor.com resources page).
  This is a different HN post from the prior HN hit 46622328
  (2026-01-14, same product, same vendor series). It is not a
  duplicate id, but it is the same product and vendor series, so it
  adds no new behavior on HN text alone.
- C9. Codex for Everything Exfiltrates Connected Data — HN stories
  48226268 (2026-05-21), 48283191 (2026-05-21), and 48403433
  (2026-06-04), plus Codex Exfiltrates Connector Data, HN story
  48738860 (2026-06-30). All point at the same vendor link target
  (promptarmor.com resources page). Reposts, not distinct incidents
  on HN text alone.
- C10. Unpatched Ollama Vulnerabilities: Phishing Overlays and Data
  Exfiltration — HN stories 48326276 (2026-05-29) and 48417032
  (2026-06-05), vendor link target (promptarmor.com resources
  page). Distinct from B3 (a different Ollama post, title only).
- C11. Anthropic Claude Code sandbox bypass allows second data
  exfiltration exploit — HN story 48211229, 2026-05-20, link target:
  oddguan.com blog post (path shape: second-time-same-sandbox
  network-allowlist-bypass data-exfiltration post). Title only.
- C12. Grok exfiltrates user data when malicious instructions are
  encrypted — HN story 49376549, 2026-08-20, link target:
  arstechnica.com security post. Title only.
- C13. Data Exfil: OpenAI polices private chats exfiltrated through
  Codex Memories — HN story 49501565, 2026-08-30, link target:
  github.com openai/codex issue 41711 (issue number only, no
  content claim). Title only.
- C14. Hijacking Copilot Cowork's AI Gateway to Bypass Sandboxing and
  Exfiltrate Files — HN story 49911869, 2026-09-30, vendor link
  target (promptarmor.com resources page). Same product and vendor
  series as C8 and the prior HN hit. Title only.
- C15. An AI-assembled crew exfiltrating ERP data from Spanish SMBs
  — HN story 49932357, 2026-10-02, link target: huntback.io blog
  post (path shape: ai-crew-open-server-erp-exfil-spanish-smbs).
  Title only. The title claims a real-world crew, which is why it
  is listed here rather than triaged out, but HN text alone proves
  nothing and the linked post was not read in this lane.
- C16. Claude Code Desktop Vulnerability: Preview Pane Data
  Exfiltration — HN story 50099375, 2026-10-15, link target:
  noma.security noma-labs post (path shape: sneakpeek preview-pane
  post). Title only. Note: this is a Noma vendor post, found via
  the exfiltration terms, not via the Noma name term.
- C17. Claude AI APIs Can Be Abused for Data Exfiltration — HN story
  45821970, 2025-11-05, link target: securityweek.com post. Title
  only.
- C18. Caught in the Hook: RCE and API Token Exfiltration Through
  Claude Code — HN story 47152609, 2026-02-25, link target:
  research.checkpoint.com post (path shape: rce-and-api-token
  exfiltration-through-claude-code post, CVE-2025-59536 named in
  the path). Title only.
- C19. Show HN: My OpenClaw tried to exfiltrate my SSH keys, so I
  built a guardrail — HN story 47136170, 2026-02-24, link target:
  github.com repo (guardrail product). Title claim only. No
  substantive comments were found in the captures for this thread.
  The link target is a product repo, not an incident writeup, so
  this item is weaker than the other C items.

### D. Cluster note: one vendor's HN series

Items A1, A2, C1–C10, C14, and the prior HN hit 46622328 form one
vendor's HN post series (PromptArmor resources posts), from Nov 2025
through Sep 2026. One commenter in the Copilot CLI thread lists the
series from the vendor sidebar and suspects marketing use of HN.
That suspicion is a commenter's view, not a finding. The series
matters for ranking: these items share one source and one framing,
so they must not be counted as independent witnesses for each other.
The OpenAI API Logs thread (C5) carries the same caution from its
own commenters.

## Overlap and triaged out (never new candidates)

- Prior HN hit 1 (comment 49535519, routify host): present in the
  captures, overlap only. No new routify-host witness was found (see
  Clean negatives).
- Prior HN hit 2 (story 49429926, MCP Toolbox SSRF mechanism):
  present, overlap only. One related new post exists: story 49874737
  (2026-09-28), "I found an SSRF in Google's official MCP Toolbox
  (CVE-2026-14540)", link post, link target: a security portfolio
  page. Same CVE, same mechanism. Mechanism overlap, not a new
  behavior.
- Prior HN hit 3 (story 46622328, Claude Cowork files): present,
  overlap only, with its comment thread.
- Prior appendix A (story 48349487, Sheets workbooks) and appendix B
  (story 48827858, GitLost): present, overlap only.
- Prior overlap item 49379079 (Qwen3.8 Fetches Weird URLs): present,
  overlap only. It is the only in-range item whose text contains the
  literal string proxy_temp_file.
- Prior-lane killed items present in the captures: 48272354, 47190721,
  46403097, 48052629, 49605924, 48414158, 48838376, 50249935, 48916975,
  47541805, 50165308. Of these, 50249935 matters here: it is the only
  other in-range comment whose text contains the literal string
  routify in a file-proxy sense, and the prior lane already killed
  it as unattributed hearsay (a possible retelling of 49379079 or
  49535519).
- Google Antigravity story 46048996 (2025-11-25): prior-lane triaged,
  not new. The prior lane saw it via comment 46050928 and killed it
  as an observed shape-6 hit: capability plus known-issue status,
  not an observed leak in the comment.
- Atlassian Rovo story 49185983 (2026-08-05) and Amazon Kiro story
  49490123 (2026-08-29): prior-lane triaged (title-only and
  mitigation discussion). Not new.
- HN story 50158146 (2026-10-19, dead): a vendor pitch post. Its text
  names metadata-endpoint SSRF as a risk class and names a product.
  No agent act is claimed. Triaged out.
- HN story 46598081 (2026-01-13, Data Exfiltration via DNS
  Resolution): DNS egress is not one of the 6 shapes. Triaged out.
- HN story 48186326 (2026-05-18, Mexican government breached by solo
  user with Claude, 150 GB exfiltrated): the actor is a human user
  with AI help, not an agent acting alone. Out of the agent-egress
  scope as stated. Triaged out.
- HN story 46607189 (2026-01-13, Docs.google.com in your CSP can
  enable AI-based data exfiltration): its link target is the same
  Superhuman article as C4. A pointer to C4, not a distinct
  incident. Triaged out as a duplicate pointer.
- Show HN security products (sandbox, guardrail, firewall, scanner,
  and monitor posts for agents): defensive products, not incidents.
  Examples in the captures include the yolo-cage, ClawShield,
  SkillSandbox, and Laya guard posts. Triaged out by title pattern.
- Human malware and supply-chain stories (malicious npm, crate, and
  extension posts with exfiltration in the title): human actors, not
  agent acts. Triaged out.
- The "model fetched" flag rows: all false positives on review.
  Signed-URL stories are product posts (Signy, ESP32) and one
  feasibility question (Ask HN: Are signed URL previews feasible?).
  No story shows a model fetching a hallucinated or signed URL.

## Clean negatives (in-range, zero new substance)

- sanmaohe: 0 literal mentions in-range (2 stories and 1 comment
  fetched, all fuzzy matches). No new HN echo of the seed host.
- proxy_temp_file: literal only in overlap story 49379079. No new
  mention in-range.
- routify file-proxy host: literal only in the prior-killed hearsay
  comment 50249935 and in one framework mention (comment 49561740,
  Svelte router). No new witness in-range. The split-to-100
  recovery for routify stories found 95 further stories; the only
  literal row among them is the known overlap story 49379079.
- Metadata addresses: 14 flagged rows, all non-agent. Uses found:
  NTP config naming metadata.google.internal, honeypot DNS pointing
  at 169.254.169.254, SSRF-protection docs, and one vendor pitch.
  No agent metadata reach. 100.100.100.200 returned 0 hits on both
  tags, as in the prior lane. fd00:ec2::254 returned 0 stories and
  1 comment (no agent content).
- unshare with user flags: 2 flagged rows, both human use (a
  firewall discussion and a wine launch script). No agent escape.
  Literal "unshare" appears in 81 comments, nearly all in other
  senses or as fuzzy forms.
- aliyuncs: 13 flagged rows, all ordinary OSS resource hosts (Qwen
  model files, manuals, audio data). No egress use.
- Field Effect AMOS: 0 phrase-literal HN rows. The 1,674 fetched
  stories are bare-AMOS fuzzy noise; the 1 literal comment found by
  a loose check is about field effect transistors.
- Zenity AgentCorruption: 0 comments mention AgentCorruption or
  metadata. No HN echo of the broad-hunt item 2 in-range.
- CorbanuTerminal: 0 literal rows on either tag. No HN echo of the
  broad-hunt item 4 in-range.
- Wingman metadata gap: 0 comments mention metadata. The literal
  Wingman stories are project posts (a client-agnostic agent
  harness), not the broad-hunt item 8 guard-gap discussion.
- hermes-agent approval gap: no comment discusses the
  download-then-run approval gap. The literal rows are project posts
  and one staffing metaphor.
- ms-agent fetch gap: no row discusses the fetch-tool SSRF gap. All
  6 fetched comments are fuzzy "MS agent" noise.
- OpenSkynet: 1 story (a project post) and 1 joke comment. No
  discussion of the broad-hunt item 10 any-URL tool gap.
- MCP Toolbox beyond the CVE: the other fetched stories are product
  posts and tool lists. No new mechanism.
- GitLost beyond appendix B: the other fetched stories are fuzzy
  "git lost" noise. No new GitLost discussion.

## Fuzzy-noise totals

Counting method: per capture file, a row counts as literal if its
title plus body text contains any of that row's query strings as an
exact substring (case-insensitive). All other fetched rows count as
fuzzy. Row sums count a row once per term row that fetched it, so
rows fetched by two terms count twice. Unique ids count each HN id
once.

- Final numbers (52 main rows): row-sum fetched 90,458; literal
  11,721; fuzzy-only 78,737; unique HN ids 88,288. Recovery rows add
  97 further unique ids (95 routify stories, 2 GitLost stories).
- Largest fuzzy sources: Noma comments (53,455 fetched, 877
  substring-literal, nearly all restaurant and Nomad noise — the
  substring check counts "Nomad" as containing "noma"), bare
  "recon" stories (7,284 fetched, 660 literal), download-execute
  comments (6,051 fetched, 6 literal), guidance comments (3,788
  fetched, 3,507 literal but nearly all generic "guidance" noun use,
  not the guidance-ai library), cowork comments (5,055 fetched,
  4,999 literal, nearly all coworking and product noise), unshare
  comments (2,372 fetched, 81 literal), Noma stories (1,965 fetched,
  103 literal, nearly all restaurant noise), routify comments
  (1,107 fetched, 2 literal), model-fetched comments (2,697 fetched,
  66 literal).
- Note on the literal definition: it undercounts true matches whose
  verb form differs from the query ("exfiltrates" vs "exfiltrated")
  and story rows that match only via their link URL (PromptArmor
  story titles hold no vendor name). The flag screens (exfiltrat
  stem: 1,386 rows; download-execute pattern: 97 rows) were the
  operative screens for those families, and every flagged story
  title was reviewed.

## Coverage table

Per row: term label, tag, queries, the fetcher's own recorded
top-range reported total(s), fetched count, date splits used, and
the capped flag. Capped means a 1-day range still reported more than
1,000 hits. No row ended capped. Fetched can exceed reported on a
row (example: Wingman comments, 153 reported, 170 fetched) because
Algolia totals vary between calls. Fetched counts are exact rows
received and saved.

| Term row | Tag | Queries | Top-range reported total(s) | Fetched | Date splits | Capped |
|---|---|---|---|---|---|---|
| name-corbanu-bubblewrap | comment | CorbanuTerminal, bubblewrap | CorbanuTerminal: 0, bubblewrap: 402 | 467 | 2 | False |
| name-corbanu-bubblewrap | story | CorbanuTerminal, bubblewrap | CorbanuTerminal: 0, bubblewrap: 37 | 37 | 2 | False |
| name-cowork | comment | Cowork | Cowork: 5057 | 5055 | 15 | False |
| name-cowork | story | Cowork | Cowork: 365 | 365 | 1 | False |
| name-field-effect-amos | comment | Field Effect AMOS | Field Effect AMOS: 93 | 93 | 1 | False |
| name-field-effect-amos | story | Field Effect AMOS, AMOS | Field Effect AMOS: 2, AMOS: 1674 | 1674 | 4 | False |
| name-gitlost | comment | GitLost | GitLost: 122 | 122 | 1 | False |
| name-gitlost | story | GitLost | GitLost: 135 | 100 | 1 | False |
| name-guidance | comment | guidance-ai, guidance | guidance-ai: 13, guidance: 3978 | 3788 | 12 | False |
| name-guidance | story | guidance-ai, guidance | guidance-ai: 3, guidance: 363 | 359 | 2 | False |
| name-hermes-agent | comment | hermes-agent | hermes-agent: 205 | 205 | 1 | False |
| name-hermes-agent | story | hermes-agent | hermes-agent: 90 | 90 | 1 | False |
| name-mcp-toolbox | comment | MCP Toolbox, mcp-toolbox | MCP Toolbox: 18, mcp-toolbox: 1 | 18 | 2 | False |
| name-mcp-toolbox | story | MCP Toolbox, mcp-toolbox | MCP Toolbox: 15, mcp-toolbox: 6 | 15 | 2 | False |
| name-ms-agent | comment | ms-agent | ms-agent: 6 | 6 | 1 | False |
| name-ms-agent | story | ms-agent | ms-agent: 3 | 3 | 1 | False |
| name-noma | comment | Noma | Noma: 53791 | 53455 | 131 | False |
| name-noma | story | Noma | Noma: 1965 | 1965 | 5 | False |
| name-openskynet | comment | OpenSkynet | OpenSkynet: 1 | 1 | 1 | False |
| name-openskynet | story | OpenSkynet | OpenSkynet: 1 | 1 | 1 | False |
| name-promptarmor | comment | PromptArmor | PromptArmor: 17 | 17 | 1 | False |
| name-promptarmor | story | PromptArmor | PromptArmor: 43 | 43 | 1 | False |
| name-wingman | comment | Wingman | Wingman: 153 | 170 | 1 | False |
| name-wingman | story | Wingman | Wingman: 72 | 72 | 1 | False |
| name-zenity-agentcorruption | comment | AgentCorruption, Zenity | AgentCorruption: 0, Zenity: 131 | 131 | 2 | False |
| name-zenity-agentcorruption | story | AgentCorruption, Zenity | AgentCorruption: 0, Zenity: 27 | 27 | 2 | False |
| shape-agent-exfiltration | comment | agent exfiltration, exfiltrated, agent exfiltrate | agent exfiltration: 188, exfiltrated: 1365, agent exfiltrate: 348 | 1166 | 5 | False |
| shape-agent-exfiltration | story | agent exfiltration, exfiltrated, agent exfiltrate | agent exfiltration: 65, exfiltrated: 115, agent exfiltrate: 89 | 166 | 3 | False |
| shape-aliyuncs | comment | aliyuncs | aliyuncs: 21 | 21 | 1 | False |
| shape-aliyuncs | story | aliyuncs | aliyuncs: 2 | 2 | 1 | False |
| shape-download-execute | comment | curl -o, wget -O, downloaded and ran | curl -o: 2929, wget -O: 2917, downloaded and ran: 460 | 6051 | 27 | False |
| shape-download-execute | story | curl -o, wget -O, downloaded and ran | curl -o: 538, wget -O: 121, downloaded and ran: 27 | 673 | 3 | False |
| shape-meta-100 | comment | 100.100.100.200 | 100.100.100.200: 0 | 0 | 1 | False |
| shape-meta-100 | story | 100.100.100.200 | 100.100.100.200: 0 | 0 | 1 | False |
| shape-meta-169 | comment | 169.254.169.254 | 169.254.169.254: 9 | 9 | 1 | False |
| shape-meta-169 | story | 169.254.169.254 | 169.254.169.254: 4 | 4 | 1 | False |
| shape-meta-google | comment | metadata.google.internal | metadata.google.internal: 1 | 1 | 1 | False |
| shape-meta-google | story | metadata.google.internal | metadata.google.internal: 0 | 0 | 1 | False |
| shape-meta-ipv6 | comment | fd00:ec2::254 | fd00:ec2::254: 1 | 1 | 1 | False |
| shape-meta-ipv6 | story | fd00:ec2::254 | fd00:ec2::254: 0 | 0 | 1 | False |
| shape-model-fetched | comment | model fetched, hallucinated URL, signed URL, called home | model fetched: 545, hallucinated URL: 187, signed URL: 583, called home: 1389 | 2697 | 6 | False |
| shape-model-fetched | story | model fetched, hallucinated URL, signed URL, called home | model fetched: 133, hallucinated URL: 27, signed URL: 57, called home: 88 | 302 | 4 | False |
| shape-proxy-temp-file | comment | proxy_temp_file | proxy_temp_file: 4 | 4 | 1 | False |
| shape-proxy-temp-file | story | proxy_temp_file | proxy_temp_file: 3 | 3 | 1 | False |
| shape-recon | comment | recon egress, recon exfiltration, reconnaissance exfiltration | recon egress: 1, recon exfiltration: 1, reconnaissance exfiltration: 4 | 6 | 3 | False |
| shape-recon | story | recon | recon: 7284 | 7284 | 19 | False |
| shape-routify | comment | routify | routify: 1856 | 1107 | 13 | False |
| shape-routify | story | routify | routify: 664 | 240 | 1 | False |
| shape-sanmaohe | comment | sanmaohe | sanmaohe: 1 | 1 | 1 | False |
| shape-sanmaohe | story | sanmaohe | sanmaohe: 2 | 2 | 1 | False |
| shape-unshare | comment | unshare | unshare: 2789 | 2372 | 13 | False |
| shape-unshare | story | unshare | unshare: 67 | 67 | 1 | False |

Row-sum fetched across the 52 main rows: 90,458. Unique HN ids
across all main rows: 88,288. The difference is rows fetched by two
or more term rows.

### Recovery rows (supplementary captures)

A live probe showed that search_by_date pages 1 and later returned
0 hits despite nbPages above 1 (GitLost stories: nbPages 2, page 1
empty; routify stories: nbPages 4, pages 1–3 empty). The main
captures were paged through nbPages as offered, so later pages
that returned empty at fetch time may have hidden real rows. A
recovery fetch (`recovery.py`) split two rows until each leaf
reported 100 hits or fewer, then took page 0 of each leaf. Results:

- GitLost stories: 2 leaves, 66 delivered, 2 new ids (both noise
  titles, no GitLost substance). Main 100 + recovery 2 = 102 unique.
- Routify stories: 5 leaves, 136 delivered, 95 new ids. All 95
  titles were reviewed: routing and framework noise, except one
  literal row — the known overlap story 49379079, which the main
  routify capture had missed. Main 240 + recovery 95 = 335 unique
  routify stories. The recovery strengthens the routify clean
  negative: even with split-to-100 recovery, the only literal
  routify story is the known overlap.
- Recovery files carry their own provenance and sha256 sidecars and
  are listed in SHA256SUMS. They hold only ids absent from the main
  captures. The screening tables do not include recovery rows; the
  recovery rows were screened by hand (literal check plus full
  title review for routify, title review for GitLost).
- Other multi-page main rows were NOT recovery-checked. A
  split-to-100 re-fetch of every multi-page row is the completeness
  fix, at significant API cost. It is left as an open item below.

## Failures and open items

- Terms that errored permanently: none. Two runs died mid-row
  (network timeout; service restart) and both resumed cleanly from
  progress.json with no partial captures saved and no row marked
  done on partial data.
- Noma comment row: completed. Fetcher's own top-range total 53,791;
  fetched 53,455 across 131 date splits, capped false. As expected,
  it added no candidates: the 877 substring-literal rows are Nomad
  and restaurant noise, and the flagged rows are generic discussion
  threads matched fuzzily. Vendor relevant Noma content stays
  covered by the GitLost rows, the Noma story row (1,965 fetched),
  and candidate C16 (a Noma vendor post found via exfiltration
  terms).
- Pagination caveat (found late, affects all multi-page rows): a
  live probe showed search_by_date pages 1 and later returning 0
  hits despite nbPages above 1 (GitLost stories, routify stories).
  At capture time, later pages did deliver rows for large rows
  (example: Noma comments, 53,455 fetched), so the empty-page
  behavior is intermittent, not a hard rule. Fetched counts are
  therefore as-offered-at-fetch-time. The split-to-100 recovery
  above was run for the two probed rows only. A split-to-100
  re-fetch of every multi-page row is the completeness fix and is
  left open: it would cost on the order of a thousand API calls
  (Noma comments alone would need about 535 leaves) for an
  expected yield near zero, given that the two recovered rows held
  no new candidate.
- Linked reports behind the C items were not read in this lane.
  The coordinator must read them before any C item is ranked
  higher than a title-level pointer.
- Comment review for the C threads is partial: comments were
  reviewed only where a term row fetched them. The
  agent-exfiltration comment row (1,166 fetched) was screened by
  flags, not read in full. A comment-level read of the C threads
  could add mechanism detail, as it did for A1.
- The "model fetched / hallucinated URL" family found nothing on HN
  in-range. If the coordinator wants that family pursued, the next
  step is a different surface (trajectory corpora or issue
  trackers), not more HN terms.

## Evidence paths

- Raw captures and provenance:
  `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/`
- Fetcher: `fetch_hn.py` in the same dir.
- Recovery fetcher and files: `recovery.py`,
  `name-gitlost--story--recovery.json`,
  `shape-routify--story--recovery.json`, each with provenance and
  sha256 sidecars.
- Screener and screening tables: `screen.py`, `screening.json`,
  `screening.tsv` in the same dir. Screening tables cover the 52
  main rows only, not the recovery rows (recovery rows were
  screened by hand).
- Progress and resume state: `progress.json` in the same dir.
- Per-dir checksums: `SHA256SUMS` in the same dir (54 files, all
  verified OK).
- This note:
  `reports/agent-egress-deep-dive/working/hn-expanded-crawl.md`
