# FETCH-GH-3 — fetch notes (lane-f3, `other` type repos)

Generated: 2026-10-05 19:04  · worker FETCH-GH-3

## Method
- Source: `studies/skill-egress-top1000/raw/enum-awesome-ext.md` — all 316 rows with type `other`.
- Triage: `GET /repos/<owner>/<repo>/contents/` per repo (unauthenticated, ~2s pacing;
  60s backoff on 403/429). One retry on non-404 errors.
- Skill-bearing surface signals (top-level names): `skills/`, `.claude/`, `.claude-plugin` / `.codex-plugin`
  / other `*-plugin` dot-dirs, `plugins/`, `mcp-servers/`, `tools/`, `extensions/`, `commands/`,
  `agents/`, `workflows/`, `awesome*` lists, `SKILL.md`. `AGENTS.md` noted as secondary context only.
- Fetch: `git clone --depth 1` into `~/workspace/skill-egress-work-1000/lane-f3/<owner>-<repo>/`;
  capped at 60 fetches, ranked by stars (all flagged rows had at least one primary signal).
  300s per-clone timeout with one retry; skips recorded below.
- Platform-monorepo exclusion (n8n-scale, out-of-skill-scope): none of the flagged repos qualified;
  YaoApp/yao (agent app engine, ~8.1k stars) was kept — it ships agent/MCP/tool surface, not a workflow platform.

## Summary
- Triaged: 316 | with skill-bearing surface: 213 | without: 103
- Fetch candidates (stars-desc, cap 60): 60
- Fetched OK: 59 | skipped: 1
- Staging dir: `~/workspace/skill-egress-work-1000/lane-f3/` (59 cloned repo dirs; ~3.6 GB total).
- Repo contents API: zero 404s / zero rate-limit backoffs encountered.

## Skipped fetches
| # | repo | stars | reason |
|---|---|---|---|
| 56 | [github/gh-aw](https://github.com/github/gh-aw) | ~5342 | clone timed out at 300s on both attempts (index-pack stuck; per-rule skip after one retry) |

## Triage table
| # | repo | stars | top-level signal | fetch? | reason |
|---|---|---|---|---|---|
| 1 | [omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent) | ~10595 | .claude,AGENTS.md | yes | cloned OK (153M) |
| 2 | [simonlin1212/a-stock-data](https://github.com/simonlin1212/a-stock-data) | ~10573 | SKILL.md | yes | cloned OK (1.4M) |
| 3 | [Kuberwastaken/claurst](https://github.com/Kuberwastaken/claurst) | ~10311 | — | no | no skill surface; top-level: .devcontainer,.github,.gitignore,.vscode,AGENTS.md,CNAME,LICENSE.md,README.md,do… |
| 4 | [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) | ~10197 | .claude-plugin,agents,commands,skills | yes | cloned OK (89M) |
| 5 | [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) | ~10191 | .claude-plugin,skills | yes | cloned OK (42M) |
| 6 | [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | ~9722 | .claude-plugin,AGENTS.md,agents,skills | yes | cloned OK (8.0M) |
| 7 | [xonsh/xonsh](https://github.com/xonsh/xonsh) | ~9658 | — | no | no skill surface; top-level: .authors.yml,.coveragerc,.devcontainer,.gitattributes,.github,.gitignore,.mailma… |
| 8 | [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | ~9654 | tools | yes | cloned OK (2.9M) |
| 10 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | ~9149 | .claude-plugin,.factory-plugin,AGENTS.md | yes | cloned OK (150M) |
| 11 | [revfactory/harness](https://github.com/revfactory/harness) | ~9119 | .claude-plugin,skills | yes | cloned OK (41M) |
| 12 | [pacifio/atlas](https://github.com/pacifio/atlas) | ~9096 | — | no | no skill surface; top-level: .cargo,.design-sync,.env.example,.gitattributes,.github,.gitignore,.husky,.oxfmt… |
| 13 | [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk) | ~8836 | .claude-plugin,.claude,AGENTS.md,plugins,skills | yes | cloned OK (24M) |
| 14 | [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | ~8730 | — | no | no skill surface; top-level: .gitattributes,.github,.gitignore,.pre-commit-config.yaml,CHANGELOG.md,CONTRIBUT… |
| 15 | [genspark-ai/genoffice](https://github.com/genspark-ai/genoffice) | ~8702 | skills,tools | yes | cloned OK (102M) |
| 16 | [smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad) | ~8570 | — | no | no skill surface; top-level: .github,.gitignore,.goreleaser.yaml,CLA.md,CONTRIBUTING.md,LICENSE.md,README.md,… |
| 17 | [HarnessMD/munder-difflin](https://github.com/HarnessMD/munder-difflin) | ~8469 | .claude,tools | yes | cloned OK (350M) |
| 18 | [automazeio/ccpm](https://github.com/automazeio/ccpm) | ~8398 | — | no | no skill surface; top-level: .gitignore,CHANGELOG.md,LICENSE,README.md,icon.png,screenshot.webp,skill |
| 19 | [jnMetaCode/superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | ~8258 | .claude-plugin,.codex-plugin,.cursor-plugin,.kimi-plugin,AGENTS.md,skills | yes | cloned OK (4.9M) |
| 20 | [YaoApp/yao](https://github.com/YaoApp/yao) | ~8077 | tools | yes | cloned OK (79M) |
| 21 | [OpenCoworkAI/open-codesign](https://github.com/OpenCoworkAI/open-codesign) | ~8009 | .claude,AGENTS.md | yes | cloned OK (86M) |
| 22 | [tigerless-labs/autoharness](https://github.com/tigerless-labs/autoharness) | ~7931 | .claude-plugin,agents,skills,tools | yes | cloned OK (840K) |
| 23 | [Gentleman-Programming/gentle-ai](https://github.com/Gentleman-Programming/gentle-ai) | ~7554 | .claude,AGENTS.md,skills | yes | cloned OK (41M) |
| 25 | [kyegomez/swarms](https://github.com/kyegomez/swarms) | ~7230 | SKILL.md | yes | cloned OK (106M) |
| 26 | [tw93/Waza](https://github.com/tw93/Waza) | ~7106 | .claude-plugin,AGENTS.md,plugins,skills | yes | cloned OK (3.1M) |
| 27 | [grab/cursor-talk-to-figma-mcp](https://github.com/grab/cursor-talk-to-figma-mcp) | ~7047 | — | no | no skill surface; top-level: .gitignore,.mcp.json,AGENTS.md,CLAUDE.md,DRAGME.md,Dockerfile,LICENSE,README.md,… |
| 28 | [htdt/godogen](https://github.com/htdt/godogen) | ~7045 | AGENTS.md,prompts | yes | cloned OK (368K) |
| 29 | [tbphp/gpt-load](https://github.com/tbphp/gpt-load) | ~7044 | — | no | no skill surface; top-level: .dockerignore,.editorconfig,.env.example,.github,.gitignore,CODE_OF_CONDUCT.md,C… |
| 31 | [open-multi-agent/open-multi-agent](https://github.com/open-multi-agent/open-multi-agent) | ~6979 | — | no | no skill surface; top-level: .github,.gitignore,.npmrc,.nvmrc,AGENTS.md,CHANGELOG.md,CLAUDE.md,CONTRIBUTORS.m… |
| 32 | [olimorris/codecompanion.nvim](https://github.com/olimorris/codecompanion.nvim) | ~6886 | — | no | no skill surface; top-level: .codecompanion,.config,.dockerignore,.github,.gitignore,.greptile,.luarc.json,AG… |
| 33 | [Devin-AXIS/iPolloWork](https://github.com/Devin-AXIS/iPolloWork) | ~6656 | — | no | no skill surface; top-level: .agents,.codex,.devcontainer,.dockerignore,.github,.gitignore,.npmrc,.nvmrc,.ope… |
| 34 | [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser) | ~6649 | .claude-plugin,AGENTS.md,skills | yes | cloned OK (1.5M) |
| 35 | [uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch) | ~6514 | .claude-plugin,.claude,AGENTS.md,plugins | yes | cloned OK (2.4M) |
| 36 | [op7418/CodePilot](https://github.com/op7418/CodePilot) | ~6492 | — | no | no skill surface; top-level: .editorconfig,.gitattributes,.github,.gitignore,.husky,.mcp.json,AGENTS.md,ARCHI… |
| 38 | [rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk) | ~6370 | AGENTS.md,agents,extensions,tools | yes | cloned OK (101M) |
| 40 | [builderz-labs/mission-control](https://github.com/builderz-labs/mission-control) | ~6309 | SKILL.md,skills | yes | cloned OK (21M) |
| 41 | [Q00/ouroboros](https://github.com/Q00/ouroboros) | ~6183 | .claude-plugin,.claude,.codex-plugin,AGENTS.md,skills,tools | yes | cloned OK (69M) |
| 42 | [KimYx0207/AI-Coding-Guide-Zh](https://github.com/KimYx0207/AI-Coding-Guide-Zh) | ~6163 | tools | yes | cloned OK (5.9M) |
| 43 | [loopx-project/loopx](https://github.com/loopx-project/loopx) | ~6155 | AGENTS.md,skills | yes | cloned OK (150M) |
| 44 | [FlorianBruniaux/claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) | ~6108 | .claude,AGENTS.md,mcp-server,tools | yes | cloned OK (67M) |
| 45 | [UfoMiao/zcf](https://github.com/UfoMiao/zcf) | ~6080 | .claude,AGENTS.md | yes | cloned OK (22M) |
| 46 | [ZSeven-W/openpencil](https://github.com/ZSeven-W/openpencil) | ~6078 | AGENTS.md,tools | yes | cloned OK (467M) |
| 47 | [larashero3-dotcom/lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) | ~5942 | SKILL.md,agents | yes | cloned OK (39M) |
| 48 | [fengshao1227/ccg-workflow](https://github.com/fengshao1227/ccg-workflow) | ~5926 | .claude-plugin | yes | cloned OK (16M) |
| 49 | [generalaction/emdash](https://github.com/generalaction/emdash) | ~5911 | .claude,AGENTS.md,agents | yes | cloned OK (59M) |
| 50 | [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | ~5852 | .claude-plugin,agents,commands,skills | yes | cloned OK (2.7M) |
| 51 | [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | ~5669 | .claude-plugin,agents,commands,plugins,skills | yes | cloned OK (15M) |
| 52 | [junhoyeo/tokscale](https://github.com/junhoyeo/tokscale) | ~5628 | — | no | no skill surface; top-level: .dockerignore,.github,.gitignore,.npmrc,AGENTS.md,CONTRIBUTING.md,Cargo.lock,Car… |
| 53 | [weave-os/router](https://github.com/weave-os/router) | ~5569 | .claude,AGENTS.md | yes | cloned OK (48M) |
| 54 | [breaking-brake/cc-wf-studio](https://github.com/breaking-brake/cc-wf-studio) | ~5390 | .claude | yes | cloned OK (29M) |
| 55 | [metalbear-co/mirrord](https://github.com/metalbear-co/mirrord) | ~5353 | — | no | no skill surface; top-level: .cargo,.config,.devcontainer,.dockerignore,.github,.gitignore,.greptile,.markdow… |
| 56 | [github/gh-aw](https://github.com/github/gh-aw) | ~5342 | .claude,AGENTS.md,SKILL.md | attempted | clone timed out (300s x2) — skipped |
| 57 | [looplj/axonhub](https://github.com/looplj/axonhub) | ~5334 | — | no | no skill surface; top-level: .agent,.air.toml,.dockerignore,.github,.gitignore,.golangci.yml,.goreleaser.yml,… |
| 58 | [awarexone/Agentic-Bug-Hunter](https://github.com/awarexone/Agentic-Bug-Hunter) | ~5272 | .claude-plugin,.claude,AGENTS.md,SKILL.md,commands,skills | yes | cloned OK (9.9M) |
| 59 | [FailproofAI/failproofai](https://github.com/FailproofAI/failproofai) | ~5242 | .claude,AGENTS.md,skills | yes | cloned OK (101M) |
| 60 | [su-kaka/gcli2api](https://github.com/su-kaka/gcli2api) | ~5224 | — | no | no skill surface; top-level: .env.example,.github,.gitignore,CONTRIBUTING.md,Dockerfile,LICENSE,README.md,con… |
| 61 | [Waishnav/devspace](https://github.com/Waishnav/devspace) | ~5188 | AGENTS.md,skills | yes | cloned OK (5.3M) |
| 62 | [tiann/hapi](https://github.com/tiann/hapi) | ~5182 | — | no | no skill surface; top-level: .github,.gitignore,AGENTS.md,CONTRIBUTING.md,LICENSE,README.md,SECURITY.md,andro… |
| 63 | [mvschwarz/openrig](https://github.com/mvschwarz/openrig) | ~5156 | .claude,skills | yes | cloned OK (52M) |
| 64 | [yetone/magpie](https://github.com/yetone/magpie) | ~5108 | — | no | no skill surface; top-level: .dockerignore,.github,.gitignore,AGENTS.md,CLAUDE.md,Dockerfile,LICENSE,Makefile… |
| 65 | [PeonPing/peon-ping](https://github.com/PeonPing/peon-ping) | ~5064 | .claude,skills | yes | cloned OK (62M) |
| 66 | [qixing-jk/all-api-hub](https://github.com/qixing-jk/all-api-hub) | ~4910 | AGENTS.md,plugins,tools | yes | cloned OK (104M) |
| 67 | [breferrari/obsidian-mind](https://github.com/breferrari/obsidian-mind) | ~4897 | .claude-plugin,.claude,AGENTS.md | yes | cloned OK (13M) |
| 68 | [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | ~4867 | .claude-plugin,.codex-plugin,SKILL.md,plugins,skills | yes | cloned OK (7.0M) |
| 69 | [Gaurav-Gosain/tuios](https://github.com/Gaurav-Gosain/tuios) | ~4780 | AGENTS.md,skills | yes | cloned OK (74M) |
| 70 | [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | ~4675 | .claude-plugin,SKILL.md,commands | yes | cloned OK (10M) |
| 71 | [xianyu110/awesome-openclaw-tutorial](https://github.com/xianyu110/awesome-openclaw-tutorial) | ~4565 | .claude,tools | yes | cloned OK (65M) |
| 72 | [0xNyk/council-of-high-intelligence](https://github.com/0xNyk/council-of-high-intelligence) | ~4539 | .claude-plugin,SKILL.md,agents,skills | yes | cloned OK (12M) |
| 73 | [miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop) | ~4517 | .claude-plugin,.cline-plugin,.codex-plugin,.cursor-plugin,.kimi-plugin,.omp-plugin,skills | yes | cloned OK (2.4M) |
| 74 | [zhukunpenglinyutong/desktop-cc-gui](https://github.com/zhukunpenglinyutong/desktop-cc-gui) | ~4437 | — | no | no skill surface; top-level: .gitattributes,.github,.gitignore,AGENTS.md,README.md,README.zh-CN.md,RELEASE_NO… |
| 75 | [lintsinghua/claude-code-book](https://github.com/lintsinghua/claude-code-book) | ~4290 | — | no | no skill surface; top-level: .github,.gitignore,00-前言.md,README.md,cover.png,docs,en,package-lock.json,packag… |
| 76 | [composio-community/open-claude-cowork](https://github.com/composio-community/open-claude-cowork) | ~4286 | .claude | yes | cloned OK (85M) |
| 77 | [JimLiu/baoyu-design](https://github.com/JimLiu/baoyu-design) | ~4252 | .claude,skills | yes | cloned OK (11M) |
| 78 | [crafter-station/petdex](https://github.com/crafter-station/petdex) | ~4199 | .claude,AGENTS.md | yes | cloned OK (28M) |
| 79 | [nyldn/claude-octopus](https://github.com/nyldn/claude-octopus) | ~4158 | .claude-plugin,.claude,.codex-plugin,.cursor-plugin,.factory-plugin,AGENTS.md,agents,commands,mcp-server,skills | yes | cloned OK (29M) |
| 80 | [flypythoncom/python](https://github.com/flypythoncom/python) | ~4150 | AGENTS.md,tools | yes | cloned OK (3.4M) |
| 82 | [get-bb/bb](https://github.com/get-bb/bb) | ~4129 | AGENTS.md,plugins | yes | cloned OK (117M) |
| 83 | [liustack/modlens](https://github.com/liustack/modlens) | ~4122 | AGENTS.md,skills | yes | cloned OK (8.5M) |
| 84 | [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | ~4074 | — | no | no skill surface; top-level: .agents,.coderabbit.yaml,.editorconfig,.gitattributes,.github,.gitignore,.gitmod… |
| 85 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | ~4055 | .claude,AGENTS.md,skills | yes | cloned OK (206M) |
| 86 | [anymorph-ai/Claudable](https://github.com/anymorph-ai/Claudable) | ~4052 | — | no | no skill surface; top-level: .eslintrc.json,.gitignore,LICENSE,README.md,app,assets,claude_code_zai_env.sh,co… |
| 88 | [Observal/Observal](https://github.com/Observal/Observal) | ~4035 | AGENTS.md,tools | yes | cloned OK (34M) |
| 90 | [badrisnarayanan/antigravity-claude-proxy](https://github.com/badrisnarayanan/antigravity-claude-proxy) | ~3992 | — | no | no skill surface; top-level: .gitattributes,.github,.gitignore,.npmignore,CLAUDE.md,LICENSE,README.md,bin,con… |
| 91 | [VoltAgent/awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) | ~3978 | — | no | no skill surface; top-level: LICENSE,README.md |
| 92 | [matt1398/claude-devtools](https://github.com/matt1398/claude-devtools) | ~3960 | .claude | yes | cloned OK (190M) |
| 93 | [microsoft/apm](https://github.com/microsoft/apm) | ~3941 | — | no | no skill surface; top-level: .agents,.apm,.editorconfig,.gitattributes,.github,.gitignore,.gitmodules,.pre-co… |
| 94 | [parcadei/Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) | ~3940 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 95 | [raullenchai/Rapid-MLX](https://github.com/raullenchai/Rapid-MLX) | ~3901 | .claude,AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 97 | [yvgude/lean-ctx](https://github.com/yvgude/lean-ctx) | ~3863 | .claude-plugin,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 98 | [tigerless-labs/cost-xray](https://github.com/tigerless-labs/cost-xray) | ~3860 | — | no | no skill surface; top-level: .github,.gitignore,CONTRIBUTING.md,LICENSE,Makefile,README.md,SECURITY.md,THIRD_… |
| 99 | [golutra/golutra](https://github.com/golutra/golutra) | ~3849 | — | no | no skill surface; top-level: .editorconfig,.github,.gitignore,.prettierrc.json,.tmp-xterm,CLA.md,CONTRIBUTING… |
| 100 | [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy) | ~3833 | SKILL.md,agents | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 101 | [pipeshub-ai/pipeshub-ai](https://github.com/pipeshub-ai/pipeshub-ai) | ~3810 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 102 | [xintaofei/codeg](https://github.com/xintaofei/codeg) | ~3807 | — | no | no skill surface; top-level: .cargo,.dockerignore,.editorconfig,.github,.gitignore,.npmrc,.prettierignore,.pr… |
| 103 | [tutti-os/tutti](https://github.com/tutti-os/tutti) | ~3793 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 104 | [jordan-gibbs/hyperresearch](https://github.com/jordan-gibbs/hyperresearch) | ~3778 | .claude-plugin,.codex-plugin,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 105 | [stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server) | ~3743 | .claude,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 106 | [seakee/CPA-Manager-Plus](https://github.com/seakee/CPA-Manager-Plus) | ~3742 | — | no | no skill surface; top-level: .dockerignore,.gitattributes,.github,.gitignore,.prettierrc,CONTRIBUTING.md,Dock… |
| 107 | [code-yeongyu/lazycodex](https://github.com/code-yeongyu/lazycodex) | ~3730 | AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 108 | [Windy3f3f3f3f/how-claude-code-works](https://github.com/Windy3f3f3f3f/how-claude-code-works) | ~3707 | — | no | no skill surface; top-level: .gitattributes,.gitignore,.nojekyll,LICENSE,README.md,README_EN.md,_coverpage.md… |
| 109 | [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) | ~3701 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 110 | [graykode/abtop](https://github.com/graykode/abtop) | ~3694 | — | no | no skill surface; top-level: .github,.gitignore,AGENTS.md,CLAUDE.md,Cargo.lock,Cargo.toml,LICENSE,README.md,a… |
| 112 | [rehan-remade/universal-modder](https://github.com/rehan-remade/universal-modder) | ~3680 | .claude-plugin,.claude,.codex-plugin,.cursor-plugin,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 113 | [strukto-ai/mirage](https://github.com/strukto-ai/mirage) | ~3676 | AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 114 | [Ontos-AI/knowhere](https://github.com/Ontos-AI/knowhere) | ~3668 | — | no | no skill surface; top-level: .dockerignore,.github,.gitignore,AGENTS.md,CITATION.cff,CODE_OF_CONDUCT.md,CONTE… |
| 115 | [zenbu-labs/terminal-browser](https://github.com/zenbu-labs/terminal-browser) | ~3653 | .claude-plugin,.claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 116 | [Louis-CFM/coucou](https://github.com/Louis-CFM/coucou) | ~3630 | — | no | no skill surface; top-level: .gitattributes,.github,.gitignore,CHANGELOG.md,CLAUDE.md,CONTRIBUTING.md,LICENSE… |
| 117 | [hamed-elfayome/Claude-Usage-Tracker](https://github.com/hamed-elfayome/Claude-Usage-Tracker) | ~3614 | — | no | no skill surface; top-level: .github,.gitignore,CHANGELOG.md,CODE_OF_CONDUCT.md,CONTRIBUTING.md,Claude Usage.… |
| 118 | [dembrandt/dembrandt](https://github.com/dembrandt/dembrandt) | ~3601 | tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 119 | [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) | ~3600 | .claude,AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 120 | [davepoon/buildwithclaude](https://github.com/davepoon/buildwithclaude) | ~3589 | .claude-plugin,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 123 | [SeemSeam/claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge) | ~3550 | tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 124 | [plannotator/effective-html](https://github.com/plannotator/effective-html) | ~3536 | .claude-plugin,.codex-plugin,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 125 | [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) | ~3523 | .claude-plugin,.claude,AGENTS.md,extensions,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 127 | [agenticnotetaking/arscontexta](https://github.com/agenticnotetaking/arscontexta) | ~3490 | .claude-plugin,agents,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 128 | [batrachianai/toad](https://github.com/batrachianai/toad) | ~3465 | tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 129 | [RunMaestro/Maestro](https://github.com/RunMaestro/Maestro) | ~3414 | .claude,AGENTS.md,CLAUDE-AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 132 | [ding113/claude-code-hub](https://github.com/ding113/claude-code-hub) | ~3388 | — | no | no skill surface; top-level: .bun-version,.dockerignore,.editorconfig,.env.example,.github,.gitignore,.mcp.js… |
| 133 | [automazeio/vibeproxy](https://github.com/automazeio/vibeproxy) | ~3376 | — | no | no skill surface; top-level: .github,.gitignore,AMPCODE_SETUP.md,CHANGELOG.md,FACTORY_SETUP.md,INSTALLATION.m… |
| 135 | [codeaashu/claude-code](https://github.com/codeaashu/claude-code) | ~3369 | Skill.md,mcp-server,prompts | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 136 | [nicedreamzapp/claude-code-local](https://github.com/nicedreamzapp/claude-code-local) | ~3344 | — | no | no skill surface; top-level: .github,.gitignore,CONTRIBUTING.md,IMESSAGE_MEDIA_PIPELINE.md,LICENSE,NarrativeG… |
| 137 | [giancarloerra/SocratiCode](https://github.com/giancarloerra/SocratiCode) | ~3333 | .claude-plugin,.codex-plugin,.cursor-plugin,AGENTS.md,agents,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 138 | [agent-of-empires/agent-of-empires](https://github.com/agent-of-empires/agent-of-empires) | ~3318 | AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 139 | [oboard/claude-code-rev](https://github.com/oboard/claude-code-rev) | ~3312 | — | no | no skill surface; top-level: .gitignore,AGENTS.md,README.md,bun.lock,image-processor.node,package.json,previe… |
| 141 | [edison7009/EchoBird](https://github.com/edison7009/EchoBird) | ~3290 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 142 | [chuspeeism/dashi-taskboard](https://github.com/chuspeeism/dashi-taskboard) | ~3285 | AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 143 | [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) | ~3283 | .claude-plugin,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 144 | [nexu-io/nexu](https://github.com/nexu-io/nexu) | ~3280 | AGENTS.md,skills,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 145 | [liaohch3/claude-tap](https://github.com/liaohch3/claude-tap) | ~3262 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 152 | [wquguru/harness-books](https://github.com/wquguru/harness-books) | ~3165 | .claude,AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 153 | [rlaope/oh-my-hermes](https://github.com/rlaope/oh-my-hermes) | ~3164 | .claude,AGENTS.md,INSTALL_FOR_AGENTS.md,skills,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 154 | [mikeyobrien/ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) | ~3163 | .claude-plugin,.claude,AGENTS.md,prompts,skills,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 155 | [KhazP/vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template) | ~3126 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 156 | [stravu/crystal](https://github.com/stravu/crystal) | ~3124 | — | no | no skill surface; top-level: .eslintignore,.github,.gitignore,.node-version,.npmrc,.nvmrc,AGENTS.md,CHANGELOG… |
| 157 | [MaxMiksa/Auto-Company](https://github.com/MaxMiksa/Auto-Company) | ~3116 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 158 | [coder/claudecode.nvim](https://github.com/coder/claudecode.nvim) | ~3105 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 159 | [wesammustafa/Claude-Code-Everything-You-Need-to-Know](https://github.com/wesammustafa/Claude-Code-Everything-You-Need-to-Know) | ~3096 | .claude,AGENTS.md,mcp-servers | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 160 | [realiti4/claude-swap](https://github.com/realiti4/claude-swap) | ~3084 | — | no | no skill surface; top-level: .github,.gitignore,.python-version,.vscode,LICENSE,README.md,assets,pyproject.to… |
| 161 | [dwgx/WindsurfAPI](https://github.com/dwgx/WindsurfAPI) | ~3061 | tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 162 | [motiful/cc-gateway](https://github.com/motiful/cc-gateway) | ~3057 | — | no | no skill surface; top-level: .github,.gitignore,Dockerfile,LICENSE,README.md,clash-rules.yaml,config.example.… |
| 163 | [collabs-inc/collab-public](https://github.com/collabs-inc/collab-public) | ~3053 | — | no | no skill surface; top-level: .clabot,.github,.gitignore,.mcp.json,CLA.md,CONTRIBUTING.md,LICENSE.md,NOTICE.md… |
| 165 | [zeronsh/zeron](https://github.com/zeronsh/zeron) | ~3035 | — | no | no skill surface; top-level: .github,.gitignore,ARCHITECTURE.md,CONTEXT.md,CONTRIBUTORS.md,Cargo.lock,Cargo.t… |
| 167 | [Tiger3807861189/J-Space-Cognition-Suite](https://github.com/Tiger3807861189/J-Space-Cognition-Suite) | ~3001 | — | no | no skill surface; top-level: .github,.gitignore,CITATION.cff,CONTRIBUTING.md,LICENSE,README.md,README.zh-CN.m… |
| 170 | [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | ~2984 | .claude-plugin,.codex-plugin,.qwenpaw-plugin,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 171 | [michaelshimeles/ralphy](https://github.com/michaelshimeles/ralphy) | ~2974 | — | no | no skill surface; top-level: .cursorrules,.editorconfig,.gitattributes,.gitignore,CLAUDE.md,CONTRIBUTING.md,R… |
| 172 | [open-gitagent/opengap](https://github.com/open-gitagent/opengap) | ~2968 | — | no | no skill surface; top-level: .github,.gitignore,CODE_OF_CONDUCT.md,CONTRIBUTING.md,LICENSE,README.md,docs.md,… |
| 173 | [nateherkai/scroll-craft](https://github.com/nateherkai/scroll-craft) | ~2957 | .claude-plugin,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 174 | [Kuddev/pebrel](https://github.com/Kuddev/pebrel) | ~2951 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 175 | [intellectronica/ruler](https://github.com/intellectronica/ruler) | ~2940 | — | no | no skill surface; top-level: .github,.gitignore,.prettierignore,.prettierrc.js,.ruler,AGENTS.md,LICENSE,READM… |
| 176 | [ciembor/agent-rules-books](https://github.com/ciembor/agent-rules-books) | ~2911 | — | no | no skill surface; top-level: .gitignore,CHANGELOG.md,LICENSE,README.md,_rule-workbench,a-philosophy-of-softwa… |
| 177 | [rohitg00/pro-workflow](https://github.com/rohitg00/pro-workflow) | ~2901 | .claude-plugin,.cursor-plugin,agents,commands,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 180 | [makecindy/cindy](https://github.com/makecindy/cindy) | ~2881 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 181 | [kaitranntt/ccs](https://github.com/kaitranntt/ccs) | ~2871 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 182 | [huangwb8/ChineseResearchLaTeX](https://github.com/huangwb8/ChineseResearchLaTeX) | ~2860 | AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 185 | [QwenAudio/qwen-audio-agent](https://github.com/QwenAudio/qwen-audio-agent) | ~2840 | — | no | no skill surface; top-level: .env.example,.github,.gitignore,.gitlab,.node-version,.npmignore,.npmrc,.nvmrc,C… |
| 187 | [datachain-ai/datachain](https://github.com/datachain-ai/datachain) | ~2821 | — | no | no skill surface; top-level: .cruft.json,.gitattributes,.github,.gitignore,.pre-commit-config.yaml,AGENT.md,C… |
| 188 | [openlit/openlit](https://github.com/openlit/openlit) | ~2817 | .claude-plugin,.claude,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 192 | [folke/sidekick.nvim](https://github.com/folke/sidekick.nvim) | ~2784 | — | no | no skill surface; top-level: .editorconfig,.github,.gitignore,.markdownlint-cli2.yaml,AGENTS.md,CHANGELOG.md,… |
| 193 | [brennercruvinel/CCPlugins](https://github.com/brennercruvinel/CCPlugins) | ~2774 | commands | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 196 | [codeany-ai/open-agent-sdk-typescript](https://github.com/codeany-ai/open-agent-sdk-typescript) | ~2744 | — | no | no skill surface; top-level: .env.example,.gitignore,LICENSE,README.md,examples,package-lock.json,package.jso… |
| 197 | [cocoindex-io/cocoindex-code](https://github.com/cocoindex-io/cocoindex-code) | ~2735 | .claude-plugin,.omp-plugin,extensions,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 199 | [Windy3f3f3f3f/claude-code-from-scratch](https://github.com/Windy3f3f3f3f/claude-code-from-scratch) | ~2730 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 200 | [BytePioneer-AI/codex-host](https://github.com/BytePioneer-AI/codex-host) | ~2728 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 201 | [zilliztech/memsearch](https://github.com/zilliztech/memsearch) | ~2718 | .claude-plugin,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 202 | [zubair-trabzada/ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) | ~2716 | agents,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 203 | [heshengtao/super-agent-party](https://github.com/heshengtao/super-agent-party) | ~2714 | AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 205 | [Natively-AI-assistant/natively-cluely-ai-assistant](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant) | ~2696 | — | no | no skill surface; top-level: .env.example,.gitattributes,.github,.gitignore,.gitmodules,.husky,.mcp.json,CHAN… |
| 208 | [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | ~2676 | .claude-plugin,agents,commands,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 209 | [LearnPrompt/LearnPrompt](https://github.com/LearnPrompt/LearnPrompt) | ~2675 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 210 | [bestruirui/octopus](https://github.com/bestruirui/octopus) | ~2668 | — | no | no skill surface; top-level: .github,.gitignore,CONTRIBUTING.md,LICENSE,README.md,README_zh.md,cmd,docker-com… |
| 212 | [centminmod/my-claude-code-setup](https://github.com/centminmod/my-claude-code-setup) | ~2653 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 213 | [wshobson/commands](https://github.com/wshobson/commands) | ~2645 | tools,workflows | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 215 | [Javis603/token-monitor](https://github.com/Javis603/token-monitor) | ~2624 | — | no | no skill surface; top-level: .env.example,.gitattributes,.github,.gitignore,AGENTS.md,LICENSE,README.ja.md,RE… |
| 217 | [CoderLuii/HolyClaude](https://github.com/CoderLuii/HolyClaude) | ~2578 | — | no | no skill surface; top-level: .dockerignore,.env.example,.gitattributes,.github,.gitignore,CODE_OF_CONDUCT.md,… |
| 218 | [webfuse-com/awesome-autoresearch](https://github.com/webfuse-com/awesome-autoresearch) | ~2554 | — | no | no skill surface; top-level: .gitignore,CONTRIBUTING.md,LICENSE,README.md |
| 219 | [Piebald-AI/tweakcc](https://github.com/Piebald-AI/tweakcc) | ~2530 | .claude,AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 221 | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) | ~2524 | .claude-plugin,.claude,AGENTS.md,agents,commands,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 222 | [youssofal/MTPLX](https://github.com/youssofal/MTPLX) | ~2519 | .claude,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 223 | [romainsimon/paperasse](https://github.com/romainsimon/paperasse) | ~2501 | — | no | no skill surface; top-level: .env.example,.gitattributes,.github,.gitignore,CONTRIBUTING.md,LICENSE,README.md… |
| 224 | [aldegad/sprite-gen](https://github.com/aldegad/sprite-gen) | ~2497 | SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 225 | [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) | ~2495 | .claude-plugin,.codex-plugin,commands,openclaw,opencode,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 227 | [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit) | ~2485 | .claude-plugin,.codex-plugin,.hermes-plugin,INSTALL_FOR_AGENTS.md,opencode,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 229 | [wxtsky/CodeIsland](https://github.com/wxtsky/CodeIsland) | ~2462 | — | no | no skill surface; top-level: .github,.gitignore,.omg,AppIcon.icon,Assets.xcassets,CHANGELOG.md,CHANGES-cline.… |
| 230 | [Prism-Shadow/penguin-harness](https://github.com/Prism-Shadow/penguin-harness) | ~2444 | .claude,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 231 | [FullAgent/fulling](https://github.com/FullAgent/fulling) | ~2444 | — | no | no skill surface; top-level: .dockerignore,.env.template,.github,.gitignore,.prettierignore,.prettierrc.json,… |
| 232 | [RAIT-09/obsidian-agent-client](https://github.com/RAIT-09/obsidian-agent-client) | ~2441 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 233 | [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) | ~2417 | SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 237 | [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory) | ~2394 | skills,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 240 | [cytostack/openwolf](https://github.com/cytostack/openwolf) | ~2370 | — | no | no skill surface; top-level: .github,.gitignore,CHANGELOG.md,CODE_OF_CONDUCT.md,CONTRIBUTING.md,CREDITS.md,LI… |
| 242 | [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) | ~2365 | SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 243 | [AgentsMesh/AgentsMesh](https://github.com/AgentsMesh/AgentsMesh) | ~2361 | .claude,AGENTS.md,agents,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 244 | [QoderAI/better-harness](https://github.com/QoderAI/better-harness) | ~2359 | .claude-plugin,.codex-plugin,.cursor-plugin,.dsh-plugin,.kimi-plugin,.qoder-plugin,AGENTS.md,prompts,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 245 | [datopian/portaljs](https://github.com/datopian/portaljs) | ~2355 | .claude-plugin,.claude,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 246 | [nizos/tdd-guard](https://github.com/nizos/tdd-guard) | ~2353 | .claude-plugin | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 248 | [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use) | ~2331 | AGENTS.md,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 249 | [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog) | ~2329 | .claude-plugin,agents,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 251 | [0xSteph/pentest-ai-agents](https://github.com/0xSteph/pentest-ai-agents) | ~2307 | .claude-plugin,agents,commands | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 252 | [romgX/openrelay](https://github.com/romgX/openrelay) | ~2307 | — | no | no skill surface; top-level: CHANGELOG.md,COMMERCIAL-LICENSE.txt,DISCLAIMER.md,LICENSE,PRIVACY.md,README.md,d… |
| 255 | [dzhng/jevgrep](https://github.com/dzhng/jevgrep) | ~2299 | .claude,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 256 | [tanbiralam/claude-code](https://github.com/tanbiralam/claude-code) | ~2297 | plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 257 | [Sahir619/fable-method](https://github.com/Sahir619/fable-method) | ~2296 | .claude-plugin,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 258 | [oh-my-mermaid/oh-my-mermaid](https://github.com/oh-my-mermaid/oh-my-mermaid) | ~2274 | .claude-plugin,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 259 | [GammaLabTechnologies/harmonist](https://github.com/GammaLabTechnologies/harmonist) | ~2253 | agents | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 260 | [tractorjuice/arc-kit](https://github.com/tractorjuice/arc-kit) | ~2252 | .claude-plugin,.claude,AGENTS.md,extensions,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 261 | [Vincentwei1021/anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | ~2251 | SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 262 | [phuryn/claude-usage](https://github.com/phuryn/claude-usage) | ~2250 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 266 | [jhlee0409/claude-code-history-viewer](https://github.com/jhlee0409/claude-code-history-viewer) | ~2222 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 267 | [Stack-Cairn/LiveAgent](https://github.com/Stack-Cairn/LiveAgent) | ~2212 | — | no | no skill surface; top-level: .codegraph,.codex,.dockerignore,.gitattributes,.github,.gitignore,.npmrc,.vscode… |
| 268 | [HUANGCHIHHUNGLeo/claude-real-video](https://github.com/HUANGCHIHHUNGLeo/claude-real-video) | ~2200 | .claude-plugin,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 271 | [OpenCoworkAI/open-cowork](https://github.com/OpenCoworkAI/open-cowork) | ~2189 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 273 | [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | ~2167 | .claude,AGENTS.md,skills,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 275 | [yyjeqhc/webcodex](https://github.com/yyjeqhc/webcodex) | ~2159 | AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 276 | [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) | ~2150 | — | no | no skill surface; top-level: .github,CITATION.cff,LICENSE,README.md,README_zh.md,assets,docs,paper |
| 280 | [catlog22/Claude-Code-Workflow](https://github.com/catlog22/Claude-Code-Workflow) | ~2130 | .claude,agents | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 281 | [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) | ~2129 | AGENTS.md,SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 282 | [0xsline/OpenChatCut](https://github.com/0xsline/OpenChatCut) | ~2126 | skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 283 | [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config) | ~2122 | .claude,commands | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 285 | [0Chencc/clawgod](https://github.com/0Chencc/clawgod) | ~2108 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 286 | [andyrewlee/awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators) | ~2099 | — | no | no skill surface; top-level: .github,CONTRIBUTING.md,LICENSE,README.md |
| 287 | [greggh/claude-code.nvim](https://github.com/greggh/claude-code.nvim) | ~2098 | — | no | no skill surface; top-level: .editorconfig,.githooks,.github,.gitignore,.ldoc.cfg,.luacheckrc,.luarc.json,.ma… |
| 288 | [eugene1g/agent-safehouse](https://github.com/eugene1g/agent-safehouse) | ~2092 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 290 | [maxritter/pilot-shell](https://github.com/maxritter/pilot-shell) | ~2079 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 293 | [MemTensor/memmy-agent](https://github.com/MemTensor/memmy-agent) | ~2060 | — | no | no skill surface; top-level: .env.example,.github,.gitignore,AgentSourceCore,App,Knowledge,LICENSE,Memory,Mig… |
| 294 | [memorax-ai/memorax-code](https://github.com/memorax-ai/memorax-code) | ~2055 | — | no | no skill surface; top-level: .github,.gitignore,AGENTS.md,ARCHITECTURE.md,CHANGELOG.md,CLAUDE.md,CONTRIBUTING… |
| 295 | [pchalasani/claude-code-tools](https://github.com/pchalasani/claude-code-tools) | ~2008 | .claude-plugin,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 296 | [tsingyuai/growth-lab](https://github.com/tsingyuai/growth-lab) | ~1992 | — | no | no skill surface; top-level: .env.example,.gitignore,AGENTS.md,CONFIGURATION.md,LICENSE,Makefile,README.en.md… |
| 297 | [RedPlanetHQ/core](https://github.com/RedPlanetHQ/core) | ~1986 | .claude-plugin | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 300 | [cbrock84/headcount](https://github.com/cbrock84/headcount) | ~1983 | .claude-plugin,.claude,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 301 | [MrGeDiao/shuorenhua](https://github.com/MrGeDiao/shuorenhua) | ~1982 | .claude-plugin,AGENTS.md,SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 302 | [xu-xiang/everything-claude-code-zh](https://github.com/xu-xiang/everything-claude-code-zh) | ~1970 | .claude-plugin,.claude,AGENTS.md,agents,commands,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 303 | [xiufengsun/TokenTracker](https://github.com/xiufengsun/TokenTracker) | ~1969 | — | no | no skill surface; top-level: .coderabbit.yaml,.env.example,.github,.gitignore,AGENTS.md,CLAUDE.md,CONTRIBUTIN… |
| 304 | [eneskirca/nodeterm](https://github.com/eneskirca/nodeterm) | ~1968 | — | no | no skill surface; top-level: .dockerignore,.gitattributes,.github,.gitignore,.nvmrc,.superpowers,CLAUDE.md,CO… |
| 305 | [composio-community/awesome-claude-plugins](https://github.com/composio-community/awesome-claude-plugins) | ~1932 | .claude-plugin | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 306 | [yomorun/yomo](https://github.com/yomorun/yomo) | ~1929 | — | no | no skill surface; top-level: .github,.gitignore,Cargo.toml,README.md,certs,serverless,src |
| 307 | [xenodium/agent-shell](https://github.com/xenodium/agent-shell) | ~1923 | — | no | no skill surface; top-level: .github,.gitignore,AGENTS.md,CLAUDE.md,CONTRIBUTING.org,GEMINI.md,LICENSE,README… |
| 308 | [the-open-engine/zeroshot](https://github.com/the-open-engine/zeroshot) | ~1922 | — | no | no skill surface; top-level: .dockerignore,.editorconfig,.github,.gitignore,.husky,.nvmrc,.opcore.json,.prett… |
| 309 | [Njengah/claude-code-cheat-sheet](https://github.com/Njengah/claude-code-cheat-sheet) | ~1921 | subagents.md,subagents | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 310 | [melih-unsal/DemoGPT](https://github.com/melih-unsal/DemoGPT) | ~1908 | — | no | no skill surface; top-level: .github,.gitignore,CODE_OF_CONDUCT.md,CONTRIBUTING.md,LICENSE,README.md,assets,d… |
| 311 | [stormzhang/ai-coding-guide](https://github.com/stormzhang/ai-coding-guide) | ~1908 | — | no | no skill surface; top-level: .gitignore,LICENSE,README.en.md,README.md,claude-code,codex,deepseek-harness,og.… |
| 312 | [hanshuaikang/nezha](https://github.com/hanshuaikang/nezha) | ~1902 | — | no | no skill surface; top-level: .github,.gitignore,.npmrc,.prettierignore,.prettierrc,AGENTS.md,CLAUDE.md,LICENS… |
| 313 | [yoanbernabeu/grepai](https://github.com/yoanbernabeu/grepai) | ~1901 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 314 | [Th0rgal/open-ralph-wiggum](https://github.com/Th0rgal/open-ralph-wiggum) | ~1897 | skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 316 | [coji/natural-japanese](https://github.com/coji/natural-japanese) | ~1876 | .claude-plugin,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 317 | [ballred/obsidian-claude-pkm](https://github.com/ballred/obsidian-claude-pkm) | ~1875 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 319 | [superagent-ai/vibekit](https://github.com/superagent-ai/vibekit) | ~1860 | — | no | no skill surface; top-level: .beamignore,.env.example,.github,.gitignore,.npmignore,LICENSE,LLM.md,README.md,… |
| 320 | [happier-dev/happier](https://github.com/happier-dev/happier) | ~1860 | .claude,AGENTS.md,openclaw | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 328 | [nimbalyst/nimbalyst](https://github.com/nimbalyst/nimbalyst) | ~1840 | .claude-plugin,.claude,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 329 | [a5c-ai/babysitter](https://github.com/a5c-ai/babysitter) | ~1831 | .claude-plugin,.claude,.cursor-plugin,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 331 | [Core-Mate/OpenGUI](https://github.com/Core-Mate/OpenGUI) | ~1814 | AGENTS.md,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 333 | [delibae/claude-prism](https://github.com/delibae/claude-prism) | ~1802 | — | no | no skill surface; top-level: .github,.gitignore,.husky,.npmrc,CHANGELOG.md,CONTRIBUTING.md,LICENSE,README.ja.… |
| 334 | [he-yufeng/CoreCoder](https://github.com/he-yufeng/CoreCoder) | ~1793 | — | no | no skill surface; top-level: .github,.gitignore,LICENSE,README.md,README_CN.md,article,assets,corecoder,examp… |
| 338 | [Asymptote-Labs/agent-beacon](https://github.com/Asymptote-Labs/agent-beacon) | ~1768 | .claude-plugin,.claude,.cursor-plugin,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 339 | [ddalcu/mlx-serve](https://github.com/ddalcu/mlx-serve) | ~1758 | .claude,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 340 | [dongsheng123132/u-claw](https://github.com/dongsheng123132/u-claw) | ~1757 | tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 344 | [s0xDk/ghostty-blackhole](https://github.com/s0xDk/ghostty-blackhole) | ~1711 | — | no | no skill surface; top-level: .gitignore,LICENSE,README.md,blackhole.glsl,claude-token.py,demo.gif,presets-gri… |
| 345 | [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance) | ~1708 | .claude-plugin,agents | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 346 | [Nexting-ai/nexting](https://github.com/Nexting-ai/nexting) | ~1707 | — | no | no skill surface; top-level: .github,LICENSE,README.md,agent-bus,devices,hardware-opensource,plugin,public |
| 347 | [BayramAnnakov/claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | ~1703 | .claude-plugin,SKILL.md,commands | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 348 | [gi-dellav/zerostack](https://github.com/gi-dellav/zerostack) | ~1700 | — | no | no skill surface; top-level: .cargo,.github,.gitignore,.gitmodules,AGENTS.md,ARCHITECTURE.md,CODE_OF_CONDUCT.… |
| 349 | [fynnfluegge/agtx](https://github.com/fynnfluegge/agtx) | ~1700 | .claude-plugin,.claude,.codex-plugin,AGENTS.md,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 350 | [lst97/claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents) | ~1696 | agents | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 352 | [webfuse-com/awesome-claude](https://github.com/webfuse-com/awesome-claude) | ~1681 | — | no | no skill surface; top-level: .gitignore,LICENSE,README.md,assets,claude-vscode-theme,contributing.md,package-… |
| 353 | [simonlin1212/global-stock-data](https://github.com/simonlin1212/global-stock-data) | ~1679 | SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 354 | [patoles/agent-flow](https://github.com/patoles/agent-flow) | ~1675 | — | no | no skill surface; top-level: .github,.gitignore,.vscode,CLA.md,CODE_OF_CONDUCT.md,CONTRIBUTING.md,LICENSE,REA… |
| 355 | [ghostwright/ghost-os](https://github.com/ghostwright/ghost-os) | ~1669 | — | no | no skill surface; top-level: .gitignore,CLAUDE.md,CONTRIBUTING.md,GHOST-MCP.md,LICENSE,Package.resolved,Packa… |
| 356 | [zhnt/loushang](https://github.com/zhnt/loushang) | ~1667 | — | no | no skill surface; top-level: .codex,.gitattributes,.github,.gitignore,.python-version,AGENTS.md,LICENSE,Makef… |
| 357 | [spec-kitty/spec-kitty](https://github.com/spec-kitty/spec-kitty) | ~1666 | — | no | no skill surface; top-level: .agent,.all-contributorsrc,.amazonq,.augment,.claudeignore,.cursor,.gemini,.gita… |
| 359 | [AMAP-ML/LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness) | ~1660 | — | no | no skill surface; top-level: .github,.gitignore,LICENSE,README.md,README.zh-CN.md,assets,eval,frontend,pyproj… |
| 360 | [feiskyer/claude-code-settings](https://github.com/feiskyer/claude-code-settings) | ~1657 | .claude-plugin,agents,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 361 | [Agents365-ai/video-podcast-maker](https://github.com/Agents365-ai/video-podcast-maker) | ~1652 | AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 363 | [DreambigOu/ELI5](https://github.com/DreambigOu/ELI5) | ~1648 | skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 365 | [codeaholicguy/ai-devkit](https://github.com/codeaholicguy/ai-devkit) | ~1640 | .claude-plugin,.codex-plugin,.cursor-plugin,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 366 | [uber/ADR](https://github.com/uber/ADR) | ~1632 | — | no | no skill surface; top-level: .github,.gitignore,CITATION.cff,CODE_OF_CONDUCT.md,CONTRIBUTING.md,Detection,Dis… |
| 368 | [openedclaude/claude-reviews-claude](https://github.com/openedclaude/claude-reviews-claude) | ~1623 | — | no | no skill surface; top-level: .github,.gitignore,DISCLAIMER.md,DISCLAIMER_CN.md,LICENSE,README.md,README_EN.md… |
| 371 | [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) | ~1618 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 374 | [ray-r-ren/agent-apprenticeship](https://github.com/ray-r-ren/agent-apprenticeship) | ~1617 | — | no | no skill surface; top-level: LICENSE,README.md,apprenticeship.png,bin,examples,package.json,pyproject.toml,sc… |
| 375 | [waybarrios/vllm-mlx](https://github.com/waybarrios/vllm-mlx) | ~1610 | — | no | no skill surface; top-level: .github,.gitignore,.pre-commit-config.yaml,CONTRIBUTING.md,LICENSE,README.es.md,… |
| 376 | [Kaelio/ktx](https://github.com/Kaelio/ktx) | ~1609 | AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 378 | [DeadWaveWave/opencove](https://github.com/DeadWaveWave/opencove) | ~1604 | — | no | no skill surface; top-level: .editorconfig,.gitattributes,.github,.gitignore,.nvmrc,.oxlintrc.json,.prettieri… |
| 383 | [deepcoldy/botmux](https://github.com/deepcoldy/botmux) | ~1576 | AGENTS.md,workflows | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 384 | [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net) | ~1574 | .claude-plugin,.claude,.codex-plugin,AGENTS.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 386 | [egoist/waku](https://github.com/egoist/waku) | ~1565 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 388 | [yigitkonur/cli-continues](https://github.com/yigitkonur/cli-continues) | ~1556 | — | no | no skill surface; top-level: .continues.example.yml,.github,.gitignore,.greptile,AGENTS.md,CHANGELOG.md,CLAUD… |
| 391 | [veedstudio/open-edit](https://github.com/veedstudio/open-edit) | ~1544 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 394 | [fujibee/agmsg](https://github.com/fujibee/agmsg) | ~1539 | .claude-plugin,SKILL.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 396 | [PrathamLearnsToCode/paper2code](https://github.com/PrathamLearnsToCode/paper2code) | ~1525 | skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 398 | [tddworks/ClaudeBar](https://github.com/tddworks/ClaudeBar) | ~1522 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 402 | [hyhmrright/brooks-lint](https://github.com/hyhmrright/brooks-lint) | ~1505 | .claude-plugin,.claude,.codex-plugin,AGENTS.md,commands,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 403 | [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) | ~1495 | .claude-plugin,SKILL.md,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 404 | [umputun/ralphex](https://github.com/umputun/ralphex) | ~1489 | .claude-plugin | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 406 | [najmuzzaman-mohammad/gawkbot](https://github.com/najmuzzaman-mohammad/gawkbot) | ~1485 | AGENTS.md,prompts | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 408 | [evo-hq/evo](https://github.com/evo-hq/evo) | ~1461 | .claude-plugin,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 411 | [QingYunA/answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) | ~1451 | .claude-plugin,commands,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 413 | [nagisanzenin/engram](https://github.com/nagisanzenin/engram) | ~1439 | .claude-plugin,.codex-plugin,.opencode-plugin,.zcode-plugin,agents,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 416 | [yohey-w/multi-agent-shogun](https://github.com/yohey-w/multi-agent-shogun) | ~1423 | .claude,AGENTS.md,agents,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 417 | [preset-io/agor](https://github.com/preset-io/agor) | ~1422 | .claude,AGENTS.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 418 | [hesamsheikh/octogent](https://github.com/hesamsheikh/octogent) | ~1419 | AGENTS.md,prompts | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 419 | [CloudAI-X/claude-workflow-v2](https://github.com/CloudAI-X/claude-workflow-v2) | ~1417 | .claude-plugin,.codex-plugin,agents,commands,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 420 | [millylee/anyrouter-check-in](https://github.com/millylee/anyrouter-check-in) | ~1409 | — | no | no skill surface; top-level: .codecov.yml,.editorconfig,.env.example,.gitattributes,.github,.gitignore,.pre-c… |
| 421 | [quemsah/awesome-claude-plugins](https://github.com/quemsah/awesome-claude-plugins) | ~1402 | — | no | no skill surface; top-level: .github,README.md,crawler,ui |
| 423 | [wuji-labs/nopua](https://github.com/wuji-labs/nopua) | ~1399 | .claude-plugin,AGENTS.md,SKILL.md,agents,commands,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 424 | [nrslib/takt](https://github.com/nrslib/takt) | ~1399 | AGENTS.md,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 425 | [m0n0x41d/haft](https://github.com/m0n0x41d/haft) | ~1394 | — | no | no skill surface; top-level: .context,.gitattributes,.github,.gitignore,.gitmodules,.golangci.yml,.goreleaser… |
| 428 | [vellum-ai/vellum-assistant](https://github.com/vellum-ai/vellum-assistant) | ~1387 | .claude,AGENTS.md,plugins,skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 430 | [elirantutia/vibeyard](https://github.com/elirantutia/vibeyard) | ~1384 | .claude | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 431 | [awslabs/cli-agent-orchestrator](https://github.com/awslabs/cli-agent-orchestrator) | ~1384 | skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 432 | [nvk/llm-wiki](https://github.com/nvk/llm-wiki) | ~1384 | .claude-plugin,.claude,AGENTS.md,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 433 | [AnandChowdhary/continuous-claude](https://github.com/AnandChowdhary/continuous-claude) | ~1383 | — | no | no skill surface; top-level: .github,.gitignore,CHANGELOG.md,LICENSE,README.md,continuous_claude.ps1,continuo… |
| 434 | [kimsungwhee/apple-docs-mcp](https://github.com/kimsungwhee/apple-docs-mcp) | ~1382 | — | no | no skill surface; top-level: .eslintrc.json,.github,.gitignore,.npmignore,LICENSE,README.ja.md,README.ko.md,R… |
| 437 | [michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude) | ~1373 | .claude-plugin,plugins,tools | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 440 | [ntegrals/10x](https://github.com/ntegrals/10x) | ~1367 | — | no | no skill surface; top-level: .gitignore,LICENSE,README.md,apps,bun.lock,media,package.json,packages,tsconfig.… |
| 441 | [snflkd/fluent-korean](https://github.com/snflkd/fluent-korean) | ~1366 | .claude-plugin,plugins | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 442 | [petergyang/human-review](https://github.com/petergyang/human-review) | ~1363 | — | no | no skill surface; top-level: .github,.gitignore,LICENSE,README.md,assets,design-ref,package-lock.json,package… |
| 443 | [amplifthq/opentag](https://github.com/amplifthq/opentag) | ~1361 | skills | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 445 | [Vincentwei1021/video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | ~1361 | SKILL.md | no (over cap) | over 60-fetch cap (lower stars than chosen set) |
| 448 | [poco-ai/poco-claw](https://github.com/poco-ai/poco-claw) | ~1355 | — | no | no skill surface; top-level: .env.example,.github,.gitignore,.pre-commit-config.yaml,.prettierignore,AGENTS.m… |
| 450 | [specstoryai/getspecstory](https://github.com/specstoryai/getspecstory) | ~1346 | .claude-plugin | no (over cap) | over 60-fetch cap (lower stars than chosen set) |

## Final fetched count
**59 repos fetched** into `~/workspace/skill-egress-work-1000/lane-f3/` (dirs named `<owner>-<repo>`), ready for the scanner. 1 candidate skipped (github/gh-aw, clone timeout). 153 additional signal-positive repos not fetched due to the 60-fetch cap (candidate list ranked by stars; see `lane-f3/clone-candidates.tsv`).

## Notes / caveats
- Signal detection ran against the repository's default-branch root listing at triage time (~18:00–18:20 UTC, 2026-10-05).
- Repos with a generic `tools/` dir but no other surface were kept as candidates; the scanner should treat
  `tools`-only hits as weaker than `skills/` / `.claude-plugin` / `SKILL.md` hits.
- No secrets were collected or used; unauthenticated public API + public git only. Nothing was executed.

