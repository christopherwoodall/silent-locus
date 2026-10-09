# FETCH-GH-1 — lane-f1 fetch log (GitHub extension, Claude-skills batch)

Generated: 2026-10-05 (CDT). Staging dir: `~/workspace/skill-egress-work-1000/lane-f1/` (46 subdirs, one per repo, named `<owner>-<repo>`).

## Method
- Parsed `enum-awesome-ext.md` table, filtered `type == claude-skill` → exactly 46 repos.
- `git clone --depth 1 https://github.com/<owner>/<repo>` sequential with ~2s pacing; `GIT_TERMINAL_PROMPT=0` (no credential prompts possible).
- Per-repo timeout 300s. One retry allowed on transient network errors or one timeout retry.
- A runtime service restart wiped /tmp mid-run and killed the first clone process after 40 repos; remaining 6 (incl. the one earlier 300s-timeout failure) were cloned on a single sequential resume run.
- Public repos only, no auth, nothing executed — static staging for the scanner.

## Fetch log

| # | repo | stars | status |
|---|---|---|---|
| 9 | chuspeeism/dashi-ppt-skill | ~9,157 | fetched |
| 24 | op7418/guizang-social-card-skill | ~7,354 | fetched |
| 30 | tech-leads-club/agent-skills | ~7,030 | fetched |
| 37 | internet-court/internet-court-skill | ~6,386 | fetched |
| 39 | ningzimu/codex-ppt-skill | ~6,347 | fetched |
| 81 | sergebulaev/linkedin-skills | ~4,148 | fetched |
| 87 | muxuuu/serenity-skill | ~4,049 | fetched |
| 89 | Ryze-AI-Adgent/open-seo-mcp-skills | ~4,022 | fetched |
| 96 | isjiamu/gzh-design-skill | ~3,901 | fetched |
| 111 | geekjourneyx/md2wechat-skill | ~3,687 | fetched |
| 121 | foryourhealth111-pixel/Vibe-Skills | ~3,568 | fetched |
| 122 | irinabuht12-oss/marketing-skills | ~3,551 | fetched |
| 126 | NVIDIA/skills | ~3,522 | fetched |
| 130 | ljagiello/ctf-skills | ~3,393 | fetched |
| 131 | samber/cc-skills-golang | ~3,392 | fetched |
| 134 | himself65/finance-skills | ~3,373 | fetched |
| 140 | PenglongHuang/chinese-novelist-skill | ~3,296 | fetched |
| 149 | ScrapeCreators/social-media-research-skills | ~3,205 | fetched |
| 151 | rebelytics/one-skill-to-rule-them-all | ~3,165 | fetched |
| 164 | FreedomIntelligence/OpenClaw-Medical-Skills | ~3,046 | fetched (1st attempt: 300s timeout; succeeded on the single allowed retry) |
| 166 | NarratorAI-Studio/narrator-ai-cli-skill | ~3,024 | fetched |
| 179 | op7418/Claude-to-IM-skill | ~2,883 | fetched |
| 186 | Owl-Listener/designer-skills | ~2,839 | fetched |
| 189 | jeremylongshore/tons-of-skills-marketplace | ~2,812 | fetched |
| 204 | runkids/skillshare | ~2,712 | fetched |
| 220 | zenstory-ai/drama-skills | ~2,525 | fetched |
| 234 | FrancyJGLisboa/agent-skills-platform | ~2,402 | fetched |
| 236 | antonbabenko/terraform-skill | ~2,399 | fetched |
| 238 | Appllama/appllama-skills | ~2,391 | fetched |
| 247 | wondelai/skills | ~2,342 | fetched |
| 253 | amElnagdy/delegate-skills | ~2,306 | fetched |
| 254 | Weizhena/Deep-Research-skills | ~2,301 | fetched |
| 318 | Jesseovo/last30days-skill-cn | ~1,871 | fetched |
| 326 | XiaoMaColtAI/math-modeling-skill | ~1,848 | fetched |
| 327 | ReScienceLab/opc-skills | ~1,841 | fetched |
| 336 | Prat011/awesome-llm-skills | ~1,781 | fetched |
| 342 | qufei1993/skills-hub | ~1,718 | fetched |
| 362 | alchaincyf/huashu-skills | ~1,649 | fetched |
| 381 | tjboudreaux/cc-thinking-skills | ~1,583 | fetched |
| 387 | cookiy-ai/user-research-skill | ~1,563 | fetched |
| 395 | plugin87/ux-ui-agent-skills | ~1,532 | fetched |
| 400 | imxv/Pretty-mermaid-skills | ~1,515 | fetched |
| 409 | skills-directory/skill-codex | ~1,453 | fetched |
| 439 | RefoundAI/lenny-skills | ~1,371 | fetched |
| 444 | lishix520/academic-paper-skills | ~1,361 | fetched |
| 449 | boyang-hu/website-rebuild-skill | ~1,353 | fetched |

## Skipped list

None. No 404s, no credential demands, no persistent timeouts.

## Final count

- Fetched: **46 / 46** (all present in `lane-f1/`, each verified to contain a `.git` dir)
- Skipped: 0
- Failed: 0 (one transient 300s timeout on `FreedomIntelligence/OpenClaw-Medical-Skills`, recovered on retry)
- Total staging size: **~1.4 GB**
