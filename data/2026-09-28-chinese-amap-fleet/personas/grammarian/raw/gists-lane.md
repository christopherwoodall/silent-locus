# GRAMMAR HUNT — gists & pastes lane: verdicts (run 1)
Date: 2026-10-04. Raw evidence: `gists-1.md` (same dir).

## VERDICT TABLE

| Candidate | Verdict | One-line reason |
|---|---|---|
| `uqscan` | **known** (baseline ✓) | Zero agent-relevant web hits; exclusive to our corpus (Amap fleet) |
| `zzbulk` / `prepnonce` | **known** | Zero public traces; dead on public surfaces |
| `sub_poi_navi` | **known** | Zero web hits; perfect fleet fingerprint holds |
| `zz=oai` | **known** | Zero agent-relevant hits; exclusive to DoE corpus |
| `httpbun` agent-context | **known** | Only HF-incident press coverage; no new swarm |
| `m47push2` / LOOT | **known** | Incident-reporting only; no second population |
| `zzFILE_` / `zzMAILBOX_` / `zzINBOX_` (+ `hb####`, `R5/R6`, HOLD/VETO/GO/STOP/ACK) | **NEW** | Consistent cross-file grammar in METR-documented incident family; `zz` prefix shared with our grammars but distinct suffix grammar → provider-vs-eval split candidate |
| Hermes `SOUL.md` persona-swap + self-labels ("GH0ST", "SOUL – Red Team Operator") + `/root/.hermes/loot/` | **NEW** | Consistent across ≥3 independent sources (ThreatDown/CARBONATO, orca archive ×5 incidents, TI Mindmap); the "agent self-labels" candidate realized as persona-file self-names |
| `openclaw` in attack contexts | **noise** (phenomenon, not grammar) | Brand-impersonation malware + skill supply chain; no consistent agent naming/param convention. Exception→lead L2 (Taiwan gov Hermes+OpenClaw swarm) |
| `deepseek-v4-flash` | **noise** | Public model ID; benign ecosystem usage |
| `agent-a`/`agent-b`, `worker-1`, `wave-1`/`wave-2`, `step-1`/`step-2` | **noise** | Generic multi-agent orchestration vocabulary (SKILL.md/DSL docs everywhere) |
| `?nonce=` / `?tag=` / `?batch=` | **noise** | OIDC/CSP/batch-file vocabulary; no swarm param convention indexed |
| `attack-wave` | **noise** (intel flagged) | StarCraft + WAF detector; TI Mindmap report is intel, not grammar |
| `<word><YYYYMMDD>` handles | **noise** | Dates in filenames/logs only |
| rentry.co agent content | **noise** | Only "registered agent" legal SEO spam indexed |
| gist surface (1 probe) | **noise** | Single gist = Claude Code telemetry-bypass script, not swarm |
| `agent[-_]\d{3,}` numeric handles | **unconfirmed** | Community tool (darkfibr/swarm-index-watch) watches it; no incident corpus found using it |

## NEW GRAMMARS — detail for follow-up
1. **zz-channel grammar** (METR incident family): `zzFILE_<HANDLE>/<6-digit idx>_<b64>` · `zzMAILBOX_<6U><2d>` · `zzINBOX_<4U><5d><U>` · handles like `DAVJAN22_CPDEV5`, `GLIBCW39`, `CURR25167X`; vocab HOLD/VETO/owner/GO/STOP/ACK; `hb####`; `R5/R6`. Sources: dev.to/hiper2d/the-swarm-that-kept-coming-back-7ie; swarm-ai-research/wiki-agent-swarm-incident heartbeat-regex-thread.md.
2. **SOUL.md weaponization grammar**: `/root/.hermes/` + `SOUL.md` overwrite + quoted self-label + `loot/` dir + Telegram C2 + operator LLM gateway. Self-labels observed: "GH0ST" (CARBONATO), "SOUL – Red Team Operator" (Gambit). Sources: ThreatDown via decryptiondigest.com; continuum-ai-corp/orca-ai-incident-archive; ti-mindmap-hub cross-source analysis 2026-09-27.

## CROSS-REF (sibling worker)
- `dream-lane.md` (same dir): Dream-swarm marker verdicts — consistent with this lane where overlapping (`agent-a`/`agent-b` noise; `wave-1`/`attack-wave` noise; openclaw/hermes inconclusive on egress). Their open lead (MODA date mismatch: Taiwan MODA observed OpenClaw attacks from **Jul 20**, not Jul 1–4) pairs with L2 above — possible continued/second wave with same tooling.

## GAPS (infra-blocked, retry on egress recovery)
- gist.github.com/search XHR endpoint extraction; Sourcegraph `.api/search/stream`; grep.app `/api/search`; pastebin.com/archive scrape; ix.io / 0x0.st / termbin (no index — direct fetch only).
- Highest-EV re-probe queries: `zzFILE_`, `zzINBOX`, `zzMAILBOX`, `GH0ST`, `SOUL.md`, `hb` + agent.

## RECOMMENDED NEXT ACTIONS (for parent)
- A1: grep our corpora for `zzFILE_`/`zzMAILBOX_`/`zzINBOX_`/`hb####` (bridge-or-new-family test).
- A2: open a lane on the Taiwan 2026-07-01 Hermes+OpenClaw gov-breach swarm (only true OpenClaw swarm use).
- A3: ingest TI Mindmap 2026-09-27 cross-source analysis as intel (not grammar).
- A4: re-run direct-surface probes (gist XHR, sourcegraph, grep.app, pastebin archive) once VM egress recovers, seeded with the two NEW grammars.
- A5: note `darkfibr/swarm-index-watch` venue list as reusable paste/wiki watch targets.

Doctrinal notes: metadata told the story (handle shapes, chunk indices, path conventions); the `zzFILE_` family was a misfit against our known `zz` grammars and is filed as a lead, not a negative (L1). Scope stayed agents+swarms; no operator-identity pursuit.
