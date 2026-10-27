# Hacker News egress hunt — cryptologist indicators

Lane: hackernews-egress-hunt. Role: cryptologist (extraction only, no truth judgement).
Date of extraction: 2026-10-27. Sources: HN Algolia captures in
`data/lanes/hackernews-egress-hunt/raw/algolia-A/`, `algolia-B/`, `algolia-C/`,
plus the public HN Algolia item API for three promising items
(49605924, 47776311, 50248222 — title/URL/text only, no login).

Rules kept:
- Signed-value rule: host + path shape + parameter NAMES only. No signed
  query string, signature, key value, or token value appears in this file
  or in `indicators.tsv`. Where a source shows a signed URL, this file
  records "signed params present (names only)".
- No thread poster handles anywhere. Item ids, titles, dates, HN URLs only.
- Model/harness names only as stated in thread text. Where unstated, UNSTATED.
- No Factum writes. No git operations. Only these two working files were written.
- Overlap (item 49379079 and pre-Nov-2025 context) is kept in a separate
  section at the end, never mixed with new-candidate rows.
- One source note on item 49379079: its text contains a partial access-key
  fragment (with ellipsis in the source). That fragment is NOT reproduced
  here or in the TSV. It is noted only as "partial access-key fragment
  present in source, withheld".

## Screening counts

- Collector A (exact sets, exhaustive): 30 exact filtered rows screened,
  22 unique item ids. Terms: routify 1 story + 3 comments, aliyuncs
  2 stories + 12 comments, oss-cn 1 story + 4 comments, sanmaohe 0 + 0,
  proxy_temp_file 3 stories + 4 comments. Exact literal `sanmaohe`
  returns zero hits in every tag/mode combination in this pull.
- Collector B (candidates): 353 candidate entries (>= 2025-11-01) in
  `CANDIDATES-B.md`, 318 unique item ids in the captures. All 318 were
  screened for shape 1 (metadata addresses) and shape 4 (user-namespace
  flag clusters). Shape-1 literal-address hits: 13 item ids (the full
  169.254.169.254 new set). Unshare flag-cluster hits: 7 item ids in
  captures, plus 2 items resolved via the HN item API (47776311,
  50248222). The `metadata-endpoint` captures contain no literal
  metadata address in their comment/story text (story text is empty in
  Algolia story records); the one shape-1 story from that set,
  49605924, is carried on its title plus its story URL from the item API.
  `100.100.100.200` returns zero hits in both tags.
- Collector C (candidates): 3,460 rows, 3,384 unique item ids, screened
  by title keyword and by body-text regex over the 12 new-hit capture
  files. Title hits: routify 0, aliyuncs 0, metadata 0, unshare 0,
  namespace 0, exfiltrat 34 unique, signed URL 11, proxy 14, bucket 1,
  upload 5. Body regex hits: routify 0, aliyuncs 0, oss-cn 0,
  metadata-address 0, unshare-flag 0, S3/GCS/bucket terms 27,
  curl-upload 17, signed/presigned 751 (generic engineering discussion;
  not extracted individually), exfiltration-upload phrasing 13.
  Only shape-matching items were extracted (see notes below).
- HN item API lookups: 3 items (49605924, 47776311, 50248222).

## New-candidate indicators

HN URL form: `https://news.ycombinator.com/item?id=<id>`.
Shape key: 1 = cloud-metadata reach, 2 = object-storage upload,
3 = named probe host on a network use, 4 = user-namespace escape,
5 = download-then-execute, 6 = recon-then-egress, NONE = stated but
no behavior shape (ordinary link, sandbox description, defensive
mention, or blocklist). "NONE" is an extraction label, not a dismissal.

### Shape 3 — named probe host (new)

| Indicator | Type | Shape | Sources | Context (short quote) |
|---|---|---|---|---|
| routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com | host | 3 | 49535519, 50249935 | "random, completely unrelated and irrelevant fetch by Qwen3.8 27B to [routify host]" / "a coding tool routing its web fetches through the same routify host" |
| routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/<date>/trace_<hex>/requestId_<hex>/<hex>.html + signed params present (names only: Expires, OSSAccessKeyId, Signature) | path-shape | 3 | 49535519 | "fetch by Qwen3.8 27B to [routify host]" (full signed URL in source; only host + path + param names recorded here) |
| Qwen3.8 27B / qwen3.8-27B | model | 3 | 49535519 | "fetch by Qwen3.8 27B" |

### Shape 1 — cloud-metadata reach (new)

| Indicator | Type | Shape | Sources | Context |
|---|---|---|---|---|
| 169.254.169.254 | ip | 1 | 46403097, 49429926, 50158146, 50095283, 49137622, 49061273, 48899966, 48414158, 47160137, 47118246, 47212666, 46951212, 46632472 | "makes requests to a proxy for fireworks.ai APIs via http://169.254.169.254/gateway/llm" (46403097, agent network use); "answers with a redirect to 169.254.169.254, the toolbox follows it" (49429926, tool network use). Most other sources are defensive/blocklist mentions, not agent uses — see notes. |
| fd00:ec2::254 | ip | 1 | 50158146 | "strictly blocks requests targeting AWS/Azure/GCP metadata (169.254.169.254, fd00:ec2::254)" (defensive blocklist, not an agent use) |
| 169.254.170.2 | ip | 1 | 48414158 | Listed in payload credential targets as "http://169.254.170.2" (ECS-style metadata target) |
| http://169.254.169.254/gateway/llm | url-host | 1 | 46403097 | "makes requests to a proxy for fireworks.ai APIs via http://169.254.169.254/gateway/llm" |
| /gateway/llm/_/gateway/fireworks/inference/v1/chat/completions | path-shape | 1 | 46403097 | "POST /gateway/llm/_/gateway/fireworks/inference/v1/chat/completions" with Host: 169.254.169.254 |
| http://169.254.169.254/latest/api/token | path-shape | 1 | 48414158 | Payload credential-target list includes this metadata token path |
| http://169.254.169.254/latest/meta-data/iam/security-credentials (Algolia text truncated at this point) | path-shape | 1 | 48414158 | Payload credential-target list includes this metadata credentials path |
| fireworks.ai | host | 1 | 46403097 | "makes requests to a proxy for https://fireworks.ai APIs" |
| accounts/fireworks/models/qwen3-coder-480b-a35b-instruct | model | 1 | 46403097 | Model field in the proxied request body: "accounts/fireworks/models/qwen3-coder-480b-a35b-instruct" |
| Shelley | harness | 1 | 46403097 | "curious about Shelley, their LLM agent" (agent name as stated; provider/harness beyond this name: UNSTATED) |
| Google MCP Toolbox | harness | 1 | 49429926 | "server-side request forgery bug in Google's MCP Toolbox, the official server Google publishes for connecting language-model agents" |
| CVE-2026-14540 | other | 1 | 49429926 | "the fix later became CVE-2026-14540 (CVSS 8.0, high)" |
| honeylabs.net/blog/spoofed-ai-crawlers-one-client | url-host | 1 | 49605924 | Story title: "AI crawler user-agents are being spoofed to reach cloud metadata endpoints"; story text empty in Algolia, URL from HN item API |

### Shape 4 — user-namespace (new)

| Indicator | Type | Shape | Sources | Context |
|---|---|---|---|---|
| unshare -Ur capsh --print | command-shape | 4 | 48069194 | "You can grant yourself this inside an unprivileged user namespace. `unshare -Ur capsh --print`" |
| unshare -U -r -m /bin/sh | command-shape | 4 | 47760652 | "`unshare -U -r -m /bin/sh`" in a container-escalation discussion |
| unshare -rcn <engine> <image> <args> | command-shape | 4 | 48921489 | "exec unshare -rcn $ENGINE \"$IMAGE\" $ARGS" (game-launch script, not an agent) |
| unshare -r -n /home/$USER/someApp | command-shape | 4 | 46042420 | "most just try \"unshare -r -n /home/$USER/someApp\" or a sandbox/VM" (generic sandbox advice, not an agent escape) |
| unshare namespace (no flags stated) | command-shape | 4 | 50248222 | "Unsharing a namespace like that is a pretty standard way to safely do things that would otherwise require root" — comment on the Cohere write-up; model: UNSTATED in this comment |
| unshare --mount sh -c "mount --bind <crypttab> <crypttab>; mkinitramfs ..." | command-shape | NONE (mount-only, excluded from shape 4) | 47270232 | "unshare --mount sh -c ..." (mount namespace only) |
| unshare --bind-mount (phrase as stated) | command-shape | NONE (mount-only, excluded from shape 4) | 46762138 | "an unshare --bind-mount Enjoyer" |
| unshare netns + pasta user-space network adapter | command-shape | NONE (net-only, excluded from shape 4) | 49673092 | "It allows you to unshare netns and then pass a user-space network adapter inside" + https://passt.top/passt/about/ |
| github.com/richfelker/usand | url-host | NONE (sandbox tool, not an escape) | 47776311 | Story title: "Usand: Minimal Unshare(1)-Based Sandbox"; URL from HN item API |
| usand | other (tool) | NONE | 47776311 | "Usand: Minimal Unshare(1)-Based Sandbox" |

### Shape 2 — object-storage upload (new, from C)

| Indicator | Type | Shape | Sources | Context |
|---|---|---|---|---|
| Grok CLI | harness | 2 | 48892997 | Title: "Grok CLI uploaded the whole home directory to GCS" (body is generic hardening advice; the claim sits in the title) |
| GCS (Google Cloud Storage, no host stated) | other (service) | 2 | 48892997 | "uploaded the whole home directory to GCS" |
| ZCode | harness | 2 | 49753023 | Title: "Inside ZCode: Silently uploading your Git history to the cloud" |
| GLM / Z.ai models (as stated in comment) | model | 2 | 49753023 | "Makes me not want to use GLM or other Z.ai models either" (commenter's association, not a stated model of ZCode) |
| github.com/xlab/cdn-s3-go | url-host | 2 | 46113173 | "routes content request to any arbitrary S3-compatible bucket" + "generating a pre-signed URLs and redirecting the clients directly" |
| S3-compatible bucket (arbitrary bucket routing) | path-shape | 2 | 46113173 | "routes content request to any arbitrary S3-compatible bucket" |

### Shape 5 — download-then-execute (new, from C install instructions)

These are installer one-liners stated in Show HN posts, not agent
egress reports. Recorded because they match the command shape; the
adversarial lane should weight them as installer noise, not agent behavior.

| Indicator | Type | Shape | Sources | Context |
|---|---|---|---|---|
| curl -fsSL https://opencode.finance/install.sh \| bash | command-shape | 5 | 47016508 | "Install + quick start: curl -fsSL https://opencode.finance/install.sh \| bash" |
| curl -fsSL https://raw.githubusercontent.com/debarshibasak/clawx/master/... \| sh | command-shape | 5 | 49166289 | "curl -fsSL https://raw.githubusercontent.com/debarshibasak/clawx/master... \| sh" |
| curl -fsSL https://compresr.ai/api/install \| sh | command-shape | 5 | 47367526 | "curl -fsSL https://compresr.ai/api/install \| sh" |
| curl -fsSL capframe.ai/install \| sh | command-shape | 5 | 48201207 | "Install: `curl -fsSL capframe.ai/install \| sh`" |
| curl -fsSL https://github.com/arrowassassin/kintsugi/releases/latest/download/install.sh \| sh | command-shape | 5 | 48558325 | "curl -fsSL https://github.com/arrowassassin/kintsugi/releases/latest/download/install.sh \| sh" |
| curl -fsSL https://install.intentra.sh \| sh | command-shape | 5 | 46888841 | "curl -fsSL https://install.intentra.sh \| sh" |
| curl -fsSL https://face.kodel.com.br/install.sh \| sh | command-shape | 5 | 50102683 | "curl -fsSL https://face.kodel.com.br/install.sh \| sh" |
| curl -fsSL https://lynxdb.org/install.sh \| sh | command-shape | 5 | 47585774 | "curl -fsSL https://lynxdb.org/install.sh \| sh" |
| curl -fsSL https://github.com/oven-sh/bun/releases/download/bun-v1.3.13... (then run payload) | command-shape | 5 | 48414158 | "Downloads Bun v1.3.13 from: https://github.com/oven-sh/bun/releases/download/..." then "Runs the large payload using Bun" |
| bun run "<temp file>" | command-shape | 5 | 48414158 | "If Bun is available, runs: bun run \"<temp file>\"" |
| /tmp/p<random>.js | path-shape | 5 | 48414158 | "Writes _p to a temporary JS file under /tmp/p<random>.js" |
| /tmp/b-* (temporary directories) | path-shape | 5 | 48414158 | "Creates temporary directories under /tmp/b-*" |

### Shape 6 — recon-then-egress / exfiltration (new)

| Indicator | Type | Shape | Sources | Context |
|---|---|---|---|---|
| Claude Cowork | harness | 6 | 46624950 | Title: "Claude Cowork exfiltrates files"; "Anthropic Claude platform literally was the exfiltration agent" (host: UNSTATED) |
| Google Antigravity | harness | 6 | 46050928 | Title: "Google Antigravity exfiltrates data via indirect prompt injection attack" |
| Atlassian Rovo | harness | 6 | 49196725 | Title: "Atlassian Rovo Exfiltrates Data, Bypassing Controls" |
| Amazon Kiro | harness | 6 | 49490126 | Title: "Data Exfiltration from Amazon Kiro via Prompt Injection"; "the agent could read a live key" |
| ChatGPT for Google Sheets | harness | 6 | 48355918 | Title: "ChatGPT for Google Sheets exfiltrates workbooks" |
| api.github.com | host | 6 | 48414158 | Payload exfiltration path: "Create or use GitHub repositories through GitHub API endpoints" |
| registry.npmjs.org/-/npm/v1/tokens , registry.npmjs.org/-/whoami | path-shape | 6 | 48414158 | Credential-target endpoints listed in payload analysis |
| rubygems.org/api/v1/api_key.json , rubygems.org/api/v1/gems | path-shape | 6 | 48414158 | Credential-target endpoints listed in payload analysis |
| cloudresourcemanager.googleapis.com/v1 , secretmanager.googleapis.com/v1 | path-shape | 6 | 48414158 | Credential-target endpoints listed in payload analysis |
| graph.microsoft.com/v1.0/me , login.microsoftonline.com/ | path-shape | 6 | 48414158 | Credential-target endpoints listed in payload analysis |
| vault.azure.net/.default | path-shape | 6 | 48414158 | Credential-target endpoint listed in payload analysis |
| 127.0.0.1:8200 | ip | 6 | 48414158 | Vault target listed as "http://127.0.0.1:8200" |
| .vscode/tasks.json , .claude/index.js , .claude/settings.json , .claude/setup.mjs , .vscode/setup.mjs | path-shape | 6 | 48414158 | "Add/update files such as: .vscode/tasks.json, .claude/index.js ..." (exfiltration persistence files) |
| commit message shape: "chore: update dependencies" / "create del-commit:" ; repo description: "Hades" | command-shape | 6 | 48414158 | "Use commit messages such as: chore: update dependencies, create del-commit:" ; "Create a GitHub repo with description: Hades" |

### Shape NONE — stated in A, no behavior shape (exhaustive host/model/harness set)

| Indicator | Type | Sources | Context |
|---|---|---|---|
| qianwen-res.oss-accelerate.aliyuncs.com | host | 48990008, 48563097, 47960958 | Ordinary Qwen resource links: "/Qwen-Image/...", "/qwenrobot/...", "/qwen-scope/..." (Algolia text truncated after the first path segment) |
| qianwen-res.oss-accelerate-overseas.aliyuncs.com | host | 46960077, 46957685 | Ordinary Qwen-Image-2.0 links (truncated in Algolia text) |
| m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/d... | url-host | 45977921, 45977847 | Sensor datasheet links in an air-monitor Show HN thread |
| chinaerospace.oss-cn-beijing.aliyuncs.com/18.1%20... | url-host | 48955231 | Citation link in a 737-flight discussion (truncated in Algolia text) |
| fiio-user-manual.oss-cn-hangzhou.aliyuncs.com/EN/JM2... | url-host | 46735533 | Device manual link (truncated in Algolia text) |
| se-data-us-oss.oss-us-west-1.aliyuncs.com/audioconve... | url-host | 46989444 | Audio source link questioned in an accent-generator thread (truncated) |
| fun-resource-shanghai.oss-cn-shanghai.aliyuncs.com/cuijiayan.cjy/tmp/exp/qwen_audio_3_tts_blog_review_260918/index.shtml + signed params present (names only: Expires, OSSAccessKeyId, Signature) | url-host | 49813485 | Story URL of "Qwen-Audio-3.1-TTS" (signed query in source; only host + path + param names recorded) |
| cdn.thereallo.dev/blog/assets/cc-domains.js | url-host | 48735674 | "You can view the full list here: https://cdn.thereallo.dev/blog/assets/cc-domains.js" |
| huggingface.co/Qwen/SAE-Res-Qwen3.5-27B-W80K-L0_50 | url-host | 47960958 | "https://huggingface.co/Qwen/SAE-Res-Qwen3.5-27B-W80K-L0_50" |
| github.com/diffusionstudio/vits-web | url-host | 46989444 | "https://github.com/diffusionstudio/vits-web" (browser speech synthesis example) |
| www.galaxus.ch/Files/6/6/1/0/2/6/6/2/Aranet4_datashe... | url-host | 45977921 | Aranet4 datasheet link (truncated in Algolia text) |
| flashmesh.netlify.app | host | 47575491 | Story URL of a vulnerability-writeup Show HN post |
| notesasm.com , www.notesasm.com | host | 48197661 | Story/site URL of a dual-agent QA platform Show HN post |
| Qwen-Image-3.0 | model | 48990008 | Parent story title "Qwen-Image-3.0: Rich Content, Authentic Details, Deep Knowledge" |
| Qwen-Image-2.0 | model | 46960077, 46957685 | Parent story title "Qwen-Image-2.0: Professional infographics, exquisite photorealism" |
| Qwen-Robot Suite | model | 48563097 | Parent story title "Qwen-Robot Suite: A Foundation Model Suite for Physical World Intelligence" |
| Qwen-Scope | model | 47960958 | Parent story title "Qwen-Scope: Official Sparse Autoencoders (SAEs) for Qwen 3.5 Models" |
| Qwen-Audio-3.1-TTS | model | 49813485 | Story title "Qwen-Audio-3.1-TTS" |
| claude-opus-4-5-20251101 | model | 46594248 | "--model claude-opus-4-5-20251101" in a Claude Code SDK invocation inside a sandbox description |
| Claude Code | harness | 46594248, 48197661 | "Claude Code" SDK / "Uses the Claude Agent SDK" |
| Claude Agent SDK | harness | 48197661 | "Uses the Claude Agent SDK" |
| Cowork | harness | 46594248 | Parent story title "Cowork: Claude Code for the rest of your work" |
| Browserbase | harness | 48197661 | "drives a real browser via Browserbase against the preview" |
| Bubblewrap (bwrap) | other (tool) | 46594248 | "Bubblewrap Sandbox (bwrap)" with "--unshare-net" and "--unshare-pid" (net/PID only, not a user-namespace escape) |
| bwrap --unshare-net , --unshare-pid | command-shape | 46594248 | "Network namespace isolation (--unshare-net)" / "PID namespace isolation (--unshare-pid)" |
| /usr/local/bin/claude --input-format stream-json --output-format stream-json --model claude-opus-4-5-20251101 | command-shape | 46594248 | SDK invocation as stated in the sandbox description |
| socat TCP:3128 -> /tmp/claude-http-*.sock ; TCP:1080 -> /tmp/claude-socks-*.sock | path-shape | 46594248 | "socat TCP:3128 → /tmp/claude-http-*.sock (HTTP proxy)" / "TCP:1080 → /tmp/claude-socks-*.sock (SOCKS proxy)" |
| /tmp/w3c-cache/308/temp_* , /tmp/w3c-cache/.index | path-shape | 49797136 | "Pages are cached in temp files, e.g., /tmp/w3c-cache/308/temp_lbAfil" (1993 browser cache, not agent behavior) |
| ip-ranges.amazonaws.com/ip-ranges.json | url-host | 49137622 | Defensive blocklist script: "--url \"https://ip-ranges.amazonaws.com/ip-ranges.json\"" |
| api.pixshot.dev/v1/screenshot | url-host | 47160137 | "curl -X POST https://api.pixshot.dev/v1/screenshot" (SSRF-protection discussion, not an agent use) |
| Tcha Protection ; npm install -g tcha-protection | other (tool) / command-shape | 50158146 | "We built Tcha Protection (MIT, npm install -g tcha-protection)" (defensive proxy, not an agent use) |
| ClawShield ; OpenClaw | harness | 47212666 | "ClawShield is a security proxy that sits in front of OpenClaw" (defensive, SSRF list includes 169.254.169.254) |

### Appendix A — the 147-string domain list from item 48735674 (shape NONE)

Item 48735674 reproduces a `cc-domains.js` list of Claude Code
proxy/provider domains. All 147 distinct strings are recorded in the
TSV (one row each, type host, except bare `cn` which is type other).
They are not agent-egress indicators on their own; they are a stated
domain inventory. Full list, alphabetically:

163.com, 4sapi.com, 529961.com, 88996.cloud, 88code.ai, 88code.org,
91code.pro, 992236.xyz, ai.codeqaq.com, ai.hybgzs.com, ai.kjvhh.com,
aicanapi.com, aicodemirror.com, aicoding.sh, aifast.site, aigocode.com,
aihubmix.com, alibaba-inc.com, alipay.com, aliyuncs.com, anmory.com,
antgroup-inc.cn, anyrouter.top, api.5202030.xyz, api.ablai.top,
api.bianxie.ai, api.bltcy.ai, api.cpass.cc, api.dev88.tech,
api.dreamger.com, api.expansion.chat, api.gueai.com, api.holdai.top,
api.ikuncode.cc, api.lconai.com, api.linkapi.org, api.mkeai.com,
api.nekoapi.com, api.oaipro.com, api.ruyun.fun, api.ssopen.top,
api.tu-zi.com, api.uglycat.cc, api.v3.cm, api.whatai.cc, api.wpgzs.top,
api.xty.app, api.yuegle.com, api.zzyu.me, apimart.ai,
apipro.maynor1024.live, apiyi.com, applyj.hiapi.top, augmunt.com,
b4u.qzz.io, baidu-int.com, baidu.com, bilibili.co, bytedance.net,
clauddy.com, claude-code-hub.app, claude-opus.top, claudeide.net,
cloudsway.net, cn, cn-beijing.fcapp.run, cn-shanghai.fcapp.run,
co.yes.vg, code.wenwen-ai.com, code.x-aio.com, codeilab.com,
ctripcorp.com, cubence.com, deeprouter.top, dhcoder.net, dimaray.com,
dmxapi.com, docs.aigc2d.com, duckcoding.com, fk.hshwk.org,
flapcode.com, foxcode.hshwk.org, foxcode.rjj.cc, fuli.hxi.me,
getgoapi.com, gpt.zhizengzeng.com, gptgod.cloud, gptkey.eu.org,
gptpay.store, hdgsb.com, henapi.top, high-five-ai.xyz, hongshan.com,
iflytek.com, instcopilot-api.com, intsig.net, iwhalecloud.com, jd.com,
jdcloud.com, jeniya.top, jiekou.ai, kg-api.cloud, kuaishou.com,
lemongpt.top, moonshot.ai, n1n.ai, netease.com, new-api.u4vr.com,
new.xychatai.com, one-api.bltcy.top, one.ocoolai.com,
oneapi.paintbot.top, open.xiaojingai.com, openclaude.me, opus.gptuu.com,
packyapi.com, poloai.top, poloapi.top, privnode.com, proxyai.com,
qinzhiai.com, right.codes, runanytime.hxi.me, sankuai.com,
sssaicode.com, stepfun-inc.com, store.zzyus.top, tiantianai.pro,
uiuiapi.com, uniapi.ai, vip.undyingapi.com, wolfai.top, wzw.de5.net,
wzw.pp.ua, xairouter.com, xaixapi.com, xaminim.com, xiaohongshu.com,
xiaohuapi.site, xiaohumini.site, xy.poloapi.com, yansd666.com,
yansd666.top, yunwu.ai, yunwu.zeabur.app, zenmux.ai, zhihuiapi.top.

## OVERLAP — separate section, never new hits

### Item 49379079 — "Qwen3.8 Fetches Weird URLs" (known overlap)

| Indicator | Type | Shape | Source | Context |
|---|---|---|---|---|
| routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com | host | 3 | 49379079 | "it tried fetching urls like: https://routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/..." (same host as the new-candidate row; this source is overlap only) |
| routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com/proxy_temp_file/production/<date>/trace_<hex>/requestId_<hex>/<hex>.html + signed params present (names only: Expires, OSSAccessKeyId, Signature) | path-shape | 3 | 49379079 | "in the same session, different batches, 16 times in total" (signed query in source; only host + path + param names recorded; partial access-key fragment in source withheld) |
| qwen3.8-27B (Unsloth, dynamic 3.0 quants, as stated) | model | 3 | 49379079 | "working on opencode with the last qwen3.8-27B from unsloth (with dynamic 3.0 quants)" |
| opencode | harness | 3 | 49379079 | "I am working on opencode with the last qwen3.8-27B" |
| webfetch tool (rewriting proxy, as stated) | other (tool) | 3 | 49379079 | "It convinced itself there was some rewriting proxy in the webfetch tool" |

### Pre-Nov-2025 context (not item-extracted)

Collector A unfiltered exact sets, Collector B pre-cutoff hits, and
Collector C `__pre20251101` sets were treated as overlap-context only
and were NOT extracted item by item in this lane. Their ids and dates
are derivable from the saved unfiltered/context capture files. No
pre-Nov item is counted as a new candidate in this file.

## Extraction notes (what was screened, skipped, and why)

- A: exhaustive over exact filtered sets only. Fuzzy sets were not
  extracted (they are typo-tolerant noise: routify fuzzy matches route,
  routine, routing). Algolia truncates long comment text with "...";
  where a path is truncated, the row says so and only the visible
  prefix is recorded.
- B: screened for shapes 1 and 4 only, per brief. `metadata-endpoint`
  items with no literal metadata address in text were not extracted
  (72 comments + 42 stories screened, zero literal-address hits in
  text). Unshare items that are ordinary namespace discussion with no
  user-namespace flag cluster were not extracted as shape 4; the
  mount-only and net-only examples above are recorded with shape NONE
  to make the exclusion auditable. Item 48414158 is a supply-chain
  malware analysis, not a model report; its model is UNSTATED and its
  shape-5 rows are included only because the same item is a shape-1
  hit (metadata paths in its target list).
- C: body regex found zero routify, aliyuncs, oss-cn, metadata-address,
  or unshare-flag hits in the entire 3,384-item new set — that negative
  is itself a finding. The 751 signed/presigned body hits are generic
  engineering discussion and were not extracted individually; only
  title/body items matching a behavior shape (upload, exfiltration,
  S3 routing, curl-install shape) were extracted. Items with an
  exfiltration title but empty body text (48052629, 50165308) yield no
  indicator value and are noted here, not padded with a row.
- Model/harness discipline: no model was inferred from a host or tool.
  Where a thread states a tool but no model (e.g. 50248222, 48414158),
  the model is UNSTATED. Where a comment associates a model with a
  tool without stating it is that tool's model (49753023, GLM/Z.ai),
  the row carries that caveat in its context.
- Dedup: same value from multiple items is one row with all source ids.
  The 147-string list from 48735674 is one row per string in the TSV
  (not 147 rows in the MD table) to keep this file readable; the full
  list is in Appendix A and in the TSV.
- Signed-value check: outputs were grepped for signed-value patterns
  (a signature parameter with a value, a key-id parameter with a
  value, an expiry parameter with a value, and key-id prefixes) —
  see the self-check in the return report. Parameter NAMES
  (Expires, OSSAccessKeyId, Signature) appear only as names in
  "signed params present (names only)" notes, never with values.

## Files

- `~/workspace/silent-locus/reports/hackernews-egress-hunt/working/indicators.md` (this file)
- `~/workspace/silent-locus/reports/hackernews-egress-hunt/working/indicators.tsv`
