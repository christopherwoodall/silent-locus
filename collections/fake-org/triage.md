# fake-org triage — 2026-10-03

5,862 pattern fires over 366,435 records (5 disk corpora) + 3 live urlquery
searches. Graded against the Transluce marker: self-entered org
**"OpenAI Research"** in the Jun 16–18 BEA API-key registration.

**Scope:** agents/infrastructure only. Registration-adjacent data stays at the
pattern level; no human/operator identity pursued.

## HEADLINE: agent-authored `OpenAIResearch*` wiki labels — CONFIRMED

- `openai_research`: **3,181 hits, all in `frozen:collusion-wiki`** — 241 distinct
  label shapes: `OpenAIResearchHelperXQ`, `AgentOpenAIResearch`,
  `OpenAIResearcher`, `OpenAIResearchAgent`, `OpenAIResearchSec2027`, … with
  epoch-nonce suffixes (`OpenAIResearch1781636008`). DSE-grammar, agent-authored
  (`grammar:epoch10 wiki:dse`), dated **2026-06-16 → 2026-06-21** (top day
  Jun 16: 1,663), i.e. the **same week as the Transluce BEA "OpenAI Research"
  registration (Jun 16–18)**.
- Not a BEA registration — but the same self-identification class in our own
  corpus. The Sep-28 "0 hits everywhere" grading missed this because it searched
  the literal spaced phrase; the no-space label form is the dominant shape.
- Zero `anthropicresearch` / `chatgptresearch` / `deepmindresearch` label shapes
  in wiki — the self-identification label is OpenAI-specific.
- Sample records: `wiki:label:OpenAIResearchSec2027` (2026-06-18T21:23:57Z),
  `wiki:label:AgentOpenAIResearch` (2026-06-17T02:27:21Z),
  `wiki:label:OpenAIResearcher` (2026-06-20T00:50:54Z).

## `openai_org_param`: 7 hits — NOTABLE, needs follow-up

- All in `swarmtraces:redacted` (SwarmTraces HF set): `company:'OpenAI'` claims
  inside redacted agent payloads — `user:{fullName, company:'OpenAI', email,
  oauthUserId, plan}` objects POSTed to redacted destinations.
  Records: R0086176, R0088877, R0089602, R0106295, R0110606, R0111555, R0112285
  (kind: recovered_text).
- All PII redacted to placeholders (`[REDACTED:sensitive_profile]`,
  `[EMAIL nn]`) — stays at pattern level. Cannot distinguish a real org claim
  from a canned value in a redacted corpus. Closest thing found to an org-claim
  in a registration-shaped payload.

## `anthropic_org_param`: 1 hit — FALSE POSITIVE

- `frozen:urlquery-incidents` `020451a5-…` (2026-05-07): OAuth scope string
  `scope=org:create_api_key+…+user:sessions:claude_code+…` — regex matched
  `org:` + `claude`. Tighten pattern to exclude `scope=` contexts on next pass.

## `oai_prefix_tag`: 2,673 hits — no fake-org value

- frozen urlquery (4): all known FPs — `OAItest7z645xgm` httpbin probe,
  `OAIJS1782002787694412133` httpbun probe title, `persistent.oaistatic.com`,
  `utm_oaid` ad param (concurs with sibling lane `data/2026-10-01-oai-tag-sweep/`).
- wiki (~2k): genuine DSE-grammar agent labels (`dse~OAIFlatheadBridgeTestMay24X`,
  `grammar:oai`) — agent-authored but not org self-identification.
- rubygems (632): `oai*` gem names — existing watchlist surface.

## Honest zeros (documented, not missing)

- `transluce-dataset` (38,160 rows): 0 fires on all 8 patterns.
- `chatgpt_org_param`, `research_org_param`, `bea_openai`, `disposable_register`: 0.
- Live urlquery API (via skill CLI, polite): exact queries run —
  `"OpenAI Research"` (1,244 API matches, 30 reviewed), `"bea.gov"` (21 results),
  `"ChatGPT Research"` — **0 verifiable fake-org hits**. Caveat: the search API
  returns matches server-side but the report payload does not include the
  matched text, so API-level matches cannot be graded as self-identification;
  recorded as an honest zero with queries logged in `data/query-log.json`.
- No literal `"OpenAI Research"` (spaced) registration anywhere on disk;
  the spaced form appears only in our own notes, never in corpora.

## Follow-ups

1. Tighten `anthropic_org_param`/`openai_org_param` against OAuth `scope=` strings.
2. Cross the `OpenAIResearch*` wiki labels against the DSE grammar docs —
   is "OpenAIResearch" a canned label template or agent-chosen?
3. Re-run this lane when new frozen exports land (collect.py is idempotent).
