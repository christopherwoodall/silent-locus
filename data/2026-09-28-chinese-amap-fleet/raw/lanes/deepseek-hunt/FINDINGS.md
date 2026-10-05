# DeepSeek Hunt — Findings (2026-10-05)

## Fingerprint: DeepSeek vs Tencent vs OpenAI agent infra

| Marker | Tencent/Hunyuan fleet (Oct 2026) | DeepSeek (+Hermes/knaithe, Jul–Aug 2026) | OpenAI incidents (May–Jun 2026) |
|---|---|---|---|
| Cloud | AS132203 Tencent Cloud HK | No proprietary cloud; Zhuhai-based operator, hosting unknown | Azure; oai markers |
| Proxy | `hysandbox-ats` (ATS Via header) | Unknown | r.jina.ai, allorigins, jqp.vercel.app |
| URL params | `uqscan=` / `uqtag=` | Unknown | `zz=oai<digits>`, `zzbulk`, `prepnonce` |
| Task family | Amap entrance-share scraping | Offensive: Langflow/n8n/Marimo/NetScaler/Tomcat | US gov data (SEC, BEA, DoE) |
| Framework | Unknown (python-requests/2.32.5) | Hermes Agent + Telegram C2; FOFA enumeration | Unknown |
| Self-ID behavior | "claude" labels (Hy3 claims Claude 29/36) | "claude" (V4 Pro claims Claude 9/44) | oai tags |

Sources: swarmcha.se "Chinese agent fleet" (2026-10-05); Unit 42 via vibe-coding-security advisory 2026-08-knaithe-hermes-autonomous-ai-scanning and orca-ai-incident-archive.

## urlquery hunt results

| Pivot | Hits | Verdict |
|---|---|---|
| `deepseek` keyword | 1,203 | All noise — pages mentioning DeepSeek (news, gomarkets.com etc.). Zero pre-Sep 2026 in sample. No agent programs. |
| `hermes` keyword | 2,190 | Appwrite/ExploitGym harness noise. One `hermes-agent.nousresearch.com` docs read. No agent fleet. |
| `api.deepseek.com` | 386 | Pages referencing the API. Zero agent programs calling it (checked httpbin subset: 1 hit, unrelated icp0.io). |
| `uqscan` / `uqtag` | 1,217 / 92 | Tencent fleet only (Amap + fleet's own httpbin programs). No second actor using the grammar. |
| `nousresearch` | 319 | Docs, model pages, AI news. No fleet. |
| `fofa.info` | 20 | Mostly unrelated recon. One notable: `"claude code web ui"` FOFA query (2026-05-16, report f075eb58-f145-4ee8-bc07-de24bff4f15d) — offensive recon for exposed Claude Code web UIs. Unattributed; predates knaithe campaign. Worth watching. |
| `knaithe` / `KnYuan` / `1daynews` | 1 / 1 / 0 | Only news coverage (thehackernews.com). Actor leaves no urlquery footprint under own names. |
| `openclaw` | 1,026 | Unchecked in depth — Hermes-adjacent framework, flagged for follow-up. |

## Claude-label cross-check: UNRESOLVED

Question: can any "claude"-labeled urlquery traffic be DeepSeek rather than Tencent/Hunyuan?

- The swarmcha.se stylometry tested Claude×3, Hy4, GLM 5.3, Hy3, Qwen — **DeepSeek was not in the reference set**. Attribution to Hunyuan/GLM does not exclude DeepSeek.
- DeepSeek V4 Pro self-identifies as Claude (9/44), so DeepSeek-powered runs would plausibly carry "claude" labels.
- **However**: the fleet's infrastructure is uniformly Tencent (13/14 inboxes AS132203, `hysandbox-ats`). Model ≠ operator — Tencent could run DeepSeek weights in their sandbox, but there is no positive evidence for this.
- urlquery search does not index URL query params well (`uqscan=claude` → 4 hits vs 211 actual per article), limiting independent verification.
- **Verdict**: cannot distinguish DeepSeek-generated from Hunyuan-generated programs from urlquery metadata alone. Requires code stylometry with DeepSeek in the reference set. Left open.

## New traces (not commentary)

1. **FOFA `"claude code web ui"` recon** (2026-05-16): `en.fofa.info/result?qbase64=ImNsYXVkZSBjb2RlIHdlYiB1aSI=` — hunting exposed Claude Code web UIs. Offensive-recon TTP, predates both the knaithe campaign and the Amap fleet. Candidate early indicator of the operator class that later ran Hermes+DeepSeek.
2. **Negative result with teeth**: the DeepSeek+Hermes actor (knaithe) has **zero** urlquery footprint under own identifiers, and "deepseek" as a keyword yields no agent programs. Either the actor avoids urlquery entirely, or its traffic is indistinguishable from background. Contrast with the Tencent fleet (2,000+ reports) — very different OPSEC postures.

## Honest zeros

No DeepSeek agent fleet identified on urlquery. No `hysandbox` outside the Tencent fleet (verified: zero web hits). No second actor using `uqscan=`/`uqtag=`. No agent programs calling `api.deepseek.com`.

## Follow-ups

- `openclaw` (1,026 hits) unexamined — Hermes-adjacent, may contain agent traffic.
- Code stylometry on claude-labeled fleet programs with DeepSeek-V3/R1 in the reference set.
- Monitor: `uqscan=`/`uqtag=` for non-Amap adoption; FOFA "claude code" queries; `sub_poi_navi` (zero web hits — strong pivot if it ever appears).
