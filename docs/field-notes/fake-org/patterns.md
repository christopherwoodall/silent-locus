# fake-org pattern set — self-identification strings

**Marker origin:** Transluce "AI Agents Targeted U.S. and Canadian Government Websites"
(2026-10-01 note: `notes/transluce-us-canada-gov-2026-10-01.md`, claim #12):
Jun 16–18 BEA API-key registration with a self-entered org string
**"OpenAI Research"** (disposable email, CAPTCHA OCR attempt). Fake-org
self-identification in registrations is a NEW marker. Sep-28 grading: 0 hits everywhere.

All patterns are case-insensitive. Scope: agents/infrastructure only —
registration-adjacent data stays at the pattern level; never pursue
human/operator identity, registrant details, or person-focused attribution.

## Patterns (regex, case-insensitive)

| id | intent | regex |
|---|---|---|
| `openai_research` | exact Transluce marker, separator-tolerant | `open[ _\-]?ai[ _\-]?research` |
| `openai_org_param` | org/company/team field claiming OpenAI | `(org\|organization\|company\|company_name\|org_name\|orgname\|team\|team_name\|institution\|affiliation)\s*[:=]\s*[^,\n&<"]{0,60}?openai` |
| `chatgpt_org_param` | same, claiming ChatGPT | `(org\|organization\|company\|company_name\|org_name\|orgname\|team\|team_name\|institution\|affiliation)\s*[:=]\s*[^,\n&<"]{0,60}?chatgpt` |
| `anthropic_org_param` | same, claiming Anthropic/Claude | `(org\|organization\|company\|company_name\|org_name\|orgname\|team\|team_name\|institution\|affiliation)\s*[:=]\s*[^,\n&<"]{0,60}?(anthropic\|claude)` |
| `research_org_param` | org/company field containing "research" (BEA shape) | `(org\|organization\|company\|company_name\|org_name\|orgname\|team\|team_name\|institution\|affiliation)\s*[:=]\s*[^,\n&<"]{0,60}?research` |
| `oai_prefix_tag` | `oai*`-prefixed tags/fields (Transluce DoE shape) | `(?:^|[^a-z0-9])oai[-_a-z0-9]` |
| `bea_openai` | BEA registration-adjacent + OpenAI claim | `bea\.gov.{0,80}openai\|openai.{0,80}bea\.gov` |
| `disposable_register` | registration flow + disposable email marker (BEA shape) | `(register\|signup\|sign-up).{0,120}(tempmail\|guerrillamail\|mailinator\|10minutemail\|trashmail\|yopmail\|dispostable\|throwawaymail\|fakeinbox\|sharklasers\|mailsac)` |

## Known false-positive shapes (to annotate, not to drop silently)

- `persistent.oaistatic.com` / `oaistatic.com` — legit ChatGPT asset domain (fires `oai_prefix_tag`).
- `utm_oaid` — ad tracking param (fires `oai_prefix_tag`).
- `OAItest*` httpbin probes, `OAIJS*` httpbun probe titles — probe noise.
- RubyGems `oai*` gem names (e.g. `oai`, `openai`-related gems) — existing watchlist surface, not fake-org.
- Legit `openai.com` referers / API key headers (`X-API-Key` to OpenAI) in scan payloads — OpenAI as *target service*, not self-claim.
- Wiki revisions quoting Transluce or discussing the BEA incident — discussion, not a hit.

## Live urlquery queries (polite, ≤1 req/2s, small limits)

1. `uq.py search --query "OpenAI Research" --limit 30` — the exact marker.
2. `uq.py search --query "bea.gov" --limit 30` — BEA registration surface.
3. `uq.py search --query "ChatGPT Research" --limit 30` — adjacent fake-org claim.

Hits are annotated to `data/hits.jsonl` as:
`{"pattern","source","record_id","timestamp","context_snippet","provenance"}`
— keep-all: record every pattern fire with provenance; no merging into frozen data.
