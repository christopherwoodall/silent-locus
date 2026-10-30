# TOOL-UPDATES — AIID full-site follow-up (2026-10-30)

Executor: TOOL-UPDATES lane. Operator: BigSexyWarlock69.
Date of change: 2026-10-30. Added-UTC stamp on new wordlist entries:
2026-10-30T12:47:13Z.

Terms used here, defined on first use:

- IOC: indicator of compromise. A value that marks hostile activity or
  agent activity. Examples: an IP address, a domain, a file path.
- OTX: AlienVault Open Threat Exchange. A third-party threat feed. The
  iocfeeds scanner asks OTX if other parties reported a watched value.
- TIER-A: a change made now under this task. It uses an existing scanner
  or an existing list only.
- TIER-B: a change that needs the operator word first. It is listed only.
  It is not made.
- Active term: a wordlist term in wordlist.txt. Sweeps use it.
- Noisy term: a wordlist term in wordlist.json only. It is never in
  wordlist.txt. Search with context only.

Rules kept:

- No network fetch was made for this work. Local files only.
- Dry runs made zero network calls. The modules state this in their
  dry-run paths.
- No commit. No push. No Factum write.
- No new scanner module. No disabled scanner enabled. No new target class.
- No personal names appear here. Incidents are cited by ID and by report
  page only: incidentdatabase.ai/reports/<incident-id>.
- No signed value, token, or evidence query string appears here.
- No Shodan use.

## 1. Wordlist — TIER-A, done

Files:

- lists/words/wordlist.json
- lists/words/wordlist.txt

Category used: agent_egress only. This category already covers agent
tools, agent hosts, and agent behavior markers. No new category is
proposed. See section 4, item B7.

Method note: the wordlist README prescribes a rebuild script at
/tmp/build_wordlist.py. That script does not exist on this machine. The
task instruction covers this case: update both files consistently
instead. That is what was done. No rebuild script was invented.

### 1a. Counts

- wordlist.json: 3895 entries before, 3991 entries after. Gain: 96.
- Of the 96: 64 active, 32 noisy.
- wordlist.txt: 3903 non-comment lines before, 3967 after. Gain: 64.
  The 64 match the 64 new active terms exactly.
- All 32 noisy terms are absent from wordlist.txt. This was verified,
  not assumed.

### 1b. New active terms (64)

Agent tools, high confidence, from the ranked set:

- Copilot — tool, 26 incidents, plus model_or_tool, 6 incidents.
- Claude Code — tool, 23 incidents.
- Devin — tool, 1 incident (1118).
- AutoGPT — tool, 1 incident (1764).
- Gemini Live — model phrase, 2 incidents (1418, 1431).

Agent-incident artifact and exfil-target paths:

- /tmp/inventory.txt (1210)
- /contents/results.b64 (1210)
- /.ssh/id_ed25519.pub (1670)
- /home/kali/workspace/.claude/skills/tsec-actions/SKILL.md (1766)
- /tmp/downloadone.py (1784)
- /tmp/pbi_os_result.json (1784)
- /storage/Counter/nine/.journald-cache.php (1669)
- /tmp/creds.json (1578, HUNT-INDEX only)
- /var/lib/mysql-files/_pwn_cleanup.txt (1578, HUNT-INDEX only)
- /var/lib/mysql-files/_pwn_test.txt (1578, HUNT-INDEX only)
- /.openclaw/config.json5 (1680, HUNT-INDEX only)

Agent product domains:

- codewall.ai (1412)
- cline.bot (1680, HUNT-INDEX only)

Distinctive agent systems and group designations, named in
hunt-relevant AIID titles (provenance cites the title incident):

- Kiro (1442), Cline (1680), OpenClaw (1542), Replit (1152),
  Antigravity (1433), JADEPUFFER (1578), CodeWall (1412),
  PocketOS (1469), DisMech (1470), AIXBT (1003), Xanthorox (1015),
  Granola (1652), Fireflies.AI (1651), Claude Cowork (1441),
  Gemini CLI (1178), GTG-1002 (1263), GTG-87001 (1687).

Threat-infra IP clusters, medium confidence, single incident each
(note on each entry: actor-infra character unconfirmed, grade with
context):

- Cairn cluster, incident 1766: 199.247.25.25, 199.247.27.2.
- Hermes address, incident 1669: 43.246.208.207.
- ARTEX cluster, incident 1781: 144.172.64.60, 144.172.64.99,
  144.172.64.128.
- Aurora cluster, incident 1661 (23 addresses): 104.194.134.167,
  144.172.116.150, 144.172.95.50, 146.19.125.36, 152.236.4.14,
  157.173.29.133, 167.88.167.37, 172.86.113.245, 172.86.90.75,
  217.69.8.54, 23.234.108.48, 23.246.128.3, 45.142.31.17,
  45.32.186.198, 45.59.113.63, 45.61.134.62, 45.61.148.166,
  68.210.224.231, 77.110.125.143, 81.177.215.15, 89.106.83.49,
  93.157.139.115, 93.157.139.123.

Provenance on every new entry names the exact source file and the
incident IDs: reports/aiid-full-site/iocs.json ranked_agent_relevant,
or reports/aiid-full-site/HUNT-INDEX.json title or ioc_values, plus
the report page incidentdatabase.ai/reports/<incident-id>.

### 1c. New noisy terms, JSON only (32)

These stay out of wordlist.txt. Each entry states why.

Generic model or vehicle-system names (ranked set, no agent-tool
signal alone): ChatGPT, Claude, Gemini, Grok, GPT-5, GPT-4o, Llama,
GPT-4, GPT-3, Midjourney, DALL-E, PaLM, Meta AI, Sora, Bard, Gemma,
Mistral, Qwen, Stable Diffusion, Whisper, Alexa, Waymo.

Name collisions or generic words (title-named, hunt-relevant
incidents in brackets): Hermes (1669, collides with the operator
platform name), Aurora (1661, generic word; the IP cluster carries
the signal, not this word), Muse (1776, collides with this assistant
product name), Sol (1671, 1672, generic single word), Mythos (1613,
1628, model checkpoint name, not an agent tool), Lovable (1016,
common adjective as well as a product name), Operator (1028, generic
word).

Generic paths: /app/.env (1670), /var/run/docker.sock (1578),
/tmp/users.json (1784).

### 1d. Verification (wordlist)

- wordlist.json parses. Entry count: 3991. Duplicate terms: 0.
- Old entries byte-identical: a re-dump of the old entry set equals
  the old file bytes exactly. The build asserted this before writing.
- wordlist.txt: non-comment lines 3967, duplicate lines 0. All 64 new
  active terms present. All 32 new noisy terms absent.
- New terms were appended at the end of the file, inside the existing
  AGENT_EGRESS section. No new section header was added. A new header
  would break the per-category sweep described in the README.
- Pre-existing gap, not touched: before this change, wordlist.txt
  already held 11 more non-comment lines than wordlist.json held
  active terms (3903 vs 3892). After this change the gap is unchanged
  (3967 vs 3956). The gap predates this task. Fixing it is out of
  scope here. It is flagged, not fixed.

## 2. IOC feeds — TIER-A, done through config

File changed: scripts/swarm-infra-config.json, iocfeeds block.

File not changed: scripts/scanners/iocfeeds.py. The module reads its
watchlist from the config block otx_indicators. It needs no code
change. Its docstring states this. Editing the module to hardcode
values would be wrong.

### 2a. Additions (29 IPv4 indicators)

- aiid-1766-cairn: 199.247.25.25, 199.247.27.2.
- aiid-1669-hermes: 43.246.208.207.
- aiid-1781-artex: 144.172.64.60, 144.172.64.99, 144.172.64.128.
- aiid-1661-aurora: the 23 addresses listed in section 1b.
- OTX indicator count: 23 before, 52 after.
- The iocfeeds note now records the AIID addition date and the
  cluster breakdown.

Why these qualify: each address sits in a single-incident cluster
tied to a named agent system or operator. Each has threat-infra
character. Press domains, generic model names, and citation sources
do not qualify. None were added.

### 2b. Verification (iocfeeds)

- py_compile passes on scripts/scanners/iocfeeds.py.
- Dry run: `python3 scripts/scanners/iocfeeds.py --dry-run` lists
  52 lookups: the 23 old indicators plus the 29 new ones, in order.
  It returns 0 hits by design. Dry run makes no network call and
  writes no state.

## 3. Existing scanners — TIER-A, one query

File changed: scripts/swarm-infra-config.json, prcomment block.

### 3a. New prcomment query (1)

New query, appended as query 11:

> type:pr "deleted the production database" OR "deleted production
> data" OR "wiped the production database" OR "dropped the
> production database"

Why this query: AIID incidents 1424, 1469, 1672, 1676, and 1719
involve an agent that deleted production data or files. Existing
prcomment queries cover accidental deletion ("accidentally deleted")
and unintended action. They do not cover a production-deletion
confession stated without the word "accidentally". This query closes
that gap. It fits the existing unintended-action family.

Budget check: the prcomment note stated 10 queries and 50 planned
calls. The note now states 11 queries and 55 planned calls. The
shared bucket holds 60 calls per hour. 55 stays inside it.

No prcomment pattern was added or changed. Pattern count stays 35.
A dedicated grading pattern for this query is TIER-B (see B3).
Candidates from the new query are still graded by the existing
patterns.

### 3b. Verification (prcomment)

- py_compile passes on scripts/scanners/prcomment.py.
- Dry run: `python3 scripts/scanners/prcomment.py --dry-run` lists
  11 queries. The new query is last. Patterns: 35, unchanged.
- Planned calls (worst case): 55.
- Quota status from the dry run: budget ok, remaining 59, need 55,
  run would proceed: True.
- No network call. No write. The module states this for dry run.

### 3c. Scanners checked but not changed

- urlquery: its query families are hardcoded in
  scripts/scanners/urlquery.py (QUERY_FAMILIES). The config list
  uq_scan_query_families does not drive the module. A config edit
  there would be dead. It was not made. A real urlquery addition
  needs a code change. That is TIER-B (see B2).
- urlscan: no AIID term genuinely extends it. Its queries search
  recent scan pages (last 30 days). AIID terms are historical
  incident names and paths, not recent scan-page markers. No query
  was added. No disabled urlscan query was re-enabled.
- Other config scanners (wayback, crtsh, jina, surfacewatch,
  cairnwatch, reposcout): no AIID term fits their existing query
  shape without a new target or a new target class. Those are
  TIER-B. See section 4.

## 4. TIER-B list — needs the operator word

Each item states WHAT and WHY, with an evidence path.

- B1. WHAT: create the aiid scanner cron. WHY: the scanner module
  exists (scripts/scanners/aiid.py) but no scheduled run was created
  under this task. Evidence: scripts/scanners/aiid.py. This task
  forbids cron creation. The operator word is needed.
- B2. WHAT: add agent-tool query families to urlquery.py code, with
  matching local scoring indicators. WHY: urlquery families are
  hardcoded in the module, not config-driven. AIID agent-tool terms
  (section 1b) could extend urlquery coverage, but only through a
  code change plus threshold review. Evidence:
  scripts/scanners/urlquery.py QUERY_FAMILIES and INDICATORS.
- B3. WHAT: add a dedicated prcomment grading pattern for
  production-deletion confessions. WHY: the new query (section 3a)
  surfaces candidates, but no existing pattern grades a
  production-deletion confession stated without "accidentally".
  Pattern changes need adversarial review, per the 2026-10-24
  prcomment reconciliation precedent. Evidence:
  scripts/swarm-infra-config.json prcomment patterns.
- B4. WHAT: extend the cairnwatch allowlist with the AIID Cairn
  addresses 199.247.25.25 and 199.247.27.2. WHY: cairnwatch targets
  are hardcoded as a frozen set per counsel constraint. New targets
  need counsel clearance plus the operator word. The OTX watchlist
  addition (section 2a) does not change cairnwatch. Evidence:
  scripts/scanners/cairnwatch.py allowlist.
- B5. WHAT: enable a disabled scanner for AIID coverage
  (surfacewatch, cairnwatch, or reposcout). WHY: each is disabled by
  default in config. Enabling one changes live scan scope and cost.
  Evidence: scripts/swarm-infra-config.json surfacewatch,
  cairnwatch, reposcout blocks.
- B6. WHAT: add OTX file-hash indicators from the AIID ranked set.
  WHY: 55 hashes sit in the ranked set, but the source caveat states
  they are unverified text copies, not verified file hashes. Hash
  indicators need a verification lane first. Evidence:
  reports/aiid-full-site/iocs.json caveats, hash kind.
- B7. WHAT: none. No new wordlist category is proposed. All 96 new
  terms fit agent_egress. If a future AIID batch brings terms that
  fit no existing category, that proposal comes here with written
  justification. It is not created unilaterally.

## 5. Skipped terms, with reasons

Skipped here means: not added to wordlist.json, not added to
wordlist.txt, not added to any feed. The reason is stated per group.

- Already present (exact case-sensitive match before this change):
  Cursor, DeepSeek, Cowork. Adding them again would break the dedup
  rule. They were logged as skipped, not re-added.
- Press and citation domains (140 ranked domains, for example
  nytimes, reuters, washingtonpost): these are sources cited by
  reports, not threat infrastructure. The iocs.json caveat states
  this. Adding them would flood sweeps with press hits.
- Template URLs (all ranked URLs that carry a {segment} placeholder):
  these are page templates, not real pages. The iocs.json caveat
  states this.
- The arxiv.org citation URL (887 incidents): a citation artifact,
  not an agent marker.
- Hashes (55 ranked): unverified text copies per the iocs.json
  caveat. Low confidence. See also TIER-B item B6.
- Network-address IPs (host part 0): 104.28.0.0, 131.0.0.0,
  138.0.0.0, 133.2.1.0, 136.0.0.0. Low confidence per the caveat.
  These are network forms, not host addresses.
- Shared-fronting and single uncorroborated IPs: the 1670
  Cloudflare-fronted set, the 968 set, the 1118 pair, and the 1731
  single address. No cluster signal. Fronting ranges are not actor
  infrastructure.
- TTP slugs (for example vibe-hacking, exfil-via-public-github-repo,
  url-shortener-abuse, ai-cli-assisted-secret-discovery): these are
  analyst-assigned labels in HUNT-INDEX.json. They are not observed
  strings in the wild. A grep sweep for them would match only our
  own documents.
- Generic asset paths: /assets/app.min.js, /assets/main.js,
  /assets/vendor.js (1669). Common names, no reuse signal.
- Single artifact filename: /s728-rw-e365/ransomware.jpg (1201).
  No reuse signal.
- Path variants covered by a base term: /tmp/inventory.txt. and
  /tmp/inventory.txt.bak are covered by /tmp/inventory.txt as a
  fixed-string match. The same holds for the trailing-dot variant
  of /storage/Counter/nine/.journald-cache.php.
- Blog, vendor, and research-organization domains (for example
  norforge.com, transluce.org, sysdig, crowdstrike): cited sources
  or vendors, not threat infrastructure. No feed entry was made.
- Operator-shop domain: no operator-shop domain was added. Sourcing
  avoids self-reference. The ranked set holds no such domain in any
  case.

## 6. Config edit verification (whole file)

- Before editing, a full round-trip (load, then dump with indent 1
  and ASCII escapes) reproduced scripts/swarm-infra-config.json
  byte for byte. The edit used that same dump form.
- After editing, the diff is confined to four hunks: the iocfeeds
  note, otx_indicators (+29), the prcomment note, prcomment queries
  (+1).
- Every other top-level key is unchanged. Every other field inside
  the iocfeeds and prcomment blocks is unchanged. The old
  otx_indicators list is an exact prefix of the new list. The old
  prcomment queries list is an exact prefix of the new list. These
  checks were asserted in the edit run.
- Git status for this executor's work shows exactly three modified files:
  lists/words/wordlist.json, lists/words/wordlist.txt,
  scripts/swarm-infra-config.json. scripts/scanners/iocfeeds.py
  was not touched by this executor. scripts/scanners/aiid.py was
  not touched by this executor either (it was fixed separately by
  the scanner-fix lane). Nothing is committed by this executor.
  Nothing is pushed.

## 7. Open notes for the coordinator

- The wordlist.txt vs wordlist.json 11-line gap (section 1d)
  predates this task. It needs a separate reconciliation decision.
- The Aurora IP cluster (23 addresses, one incident) is the weakest
  feed addition: one incident, medium confidence, actor-infra
  character unconfirmed. OTX third-party pulses are the check. If
  OTX shows no pulse for these addresses, the coordinator may
  propose removal. Removal still needs the operator word, since the
  wordlist is append-only and feed removal changes scope.
- The prcomment budget now sits at 55 of 60 calls per hour. One
  more query would hit exactly 60. No further prcomment query
  should be added without a budget review.
