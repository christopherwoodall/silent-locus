# INFRASTRUCTURE WATCHLIST — agent operations infrastructure

**What this is:** every URL/domain observed being used by AI agents to conduct operations,
compiled from all completed persona hunts plus the Dream Taiwan swarm report and the
Global South writeup (2026-09-28-chinese-amap-fleet collection).
**Date compiled:** 2026-10-05.
**How to use:** one URL per `- ` line — grep-friendly. Each entry carries a one-line role,
the source persona/report(s) that documented it, and a fleet attribution:
- `OUR FLEET` = the Amap/`uq` data-collection operator (Chinese Amap POI vertical)
- `FOREIGN` = another reported actor (Dream swarm, CARBONATO, collusion-wiki agents, etc.)
- `UNKNOWN` = unattributed agent activity
- `NOISE` = threat-intel feed strays, not agent ops
- `PREDICTED` = documented migration prediction, not yet observed

Scope: agents and infrastructure only. Hunt-tool URLs (urlquery.net, urlscan.io, GitHub CTI
repos) are excluded. Only what the sources actually document — nothing invented.

---

## 1. Fetch proxies / CORS laundering relays

- https://r.jina.ai/
  role: fetch proxy, keyless (dead now); jina laundering of targets
  sources: codebreaker, historian, mimic, scavenger, border-crosser
  attribution: OUR FLEET
- r.jina-ai.workers.dev
  role: jina-reader CLONE on Cloudflare Workers free tier (colonizing after r.jina.ai died)
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- allorigins.hexlet.app
  role: CORS relay host in jina/allorigins/da.gd laundering chain
  sources: global-south-scout (WRITEUP)
  attribution: OUR FLEET
- https://proxy.cors.sh/
  role: CORS proxy; India gov-URL link-laundering with Google-Translate params
  sources: global-south-scout (WRITEUP)
  attribution: UNKNOWN (wiki-board grammar)
- da.gd
  role: shortener + CORS-laundering relay (jina_allorigins_dagd indicator); pages.dev fleet chain
  sources: global-south-scout, mimic, scavenger
  attribution: OUR FLEET
- cors.bwa.workers.dev
  role: CORS proxy on Workers free tier, 873 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- cors.hypnguyen.workers.dev
  role: CORS proxy, 84 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- cf-cors.findme-19.workers.dev
  role: CORS proxy, 72 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- cors-get-proxy.sirjosh.workers.dev
  role: CORS proxy, 35 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- cloudflare-cors-anywhere.hanpengchen.workers.dev
  role: CORS proxy, 22 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- test.cors.workers.dev
  role: Cloudflare's own example worker, abused as CORS infra
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- jqp.vercel.app
  role: JSONP proxy, 1,189 uses; chained jqp -> markdown.new -> md.succ.ai -> target
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- md.succ.ai
  role: markdown converter in proxy-chaining stack
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- markdown.new
  role: free URL->markdown converter used as fetch proxy, 2,639 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- urltomarkdown.herokuapp.com
  role: fetch proxy, 20 uses
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- rltomarkdown.herokuapp.com
  role: fetch proxy; also seen in the Amap corpus
  sources: scavenger
  attribution: OUR FLEET + FOREIGN
- noroffcors.onrender.com
  role: Render free-tier CORS proxy used to hit YOURLS shortener APIs
  sources: scavenger
  attribution: FOREIGN (collusion-wiki agents)
- https://href.li/
  role: referer-stripping privacy hop in front of httpbun/webhook.site
  sources: codebreaker, contrarian, ghost-hunter
  attribution: OUR FLEET
- proxymule.com
  role: relay for Yahoo Finance data copies
  sources: forager
  attribution: UNKNOWN
- translate.goog
  role: Google Translate proxy wrapper; operator used httpbun-com.translate.goog as probe-loader
  sources: historian, global-south-scout (caution: *-gov.translate.goog = false-positive wrapper)
  attribution: OUR FLEET

## 2. Tunnels

- lhr.life
  role: localhost.run tunnel backbone; bare hex-subdomain probe pages (probe.js, probe.html)
  sources: historian, mimic, ghost-hunter, profiler, tracker
  attribution: OUR FLEET
- localhost.run
  role: underlying free SSH-tunnel service behind lhr.life
  sources: mimic, scavenger
  attribution: OUR FLEET
- 5ede92286ebdfd.lhr.life
  role: OTX-known operator tunnel subdomain
  sources: ghost-hunter
  attribution: OUR FLEET
- 820eea12fec476.lhr.life
  role: OTX-known operator tunnel subdomain
  sources: ghost-hunter
  attribution: OUR FLEET
- 98a8e091083f27.lhr.life
  role: OTX-known operator tunnel subdomain
  sources: ghost-hunter
  attribution: OUR FLEET
- c2679a7c8e852b.lhr.life
  role: OTX-known operator tunnel subdomain
  sources: ghost-hunter
  attribution: OUR FLEET
- 87e0bbc636999b.lhr.life
  role: operator tunnel that surfaced in CIRCL/Maltrail IOC feeds (misclassified as hacked_npmrepos/metasploit)
  sources: historian
  attribution: OUR FLEET
- tunn3l.sh
  role: agent-first tunnel service ("built for AI agents"); 8-char hex subdomains *.tunn3l.sh
  sources: trade-labourer, scavenger
  attribution: UNKNOWN (supply layer; not yet in corpus)
- pinggy.io
  role: agent-first SSH tunnels; agent Skill vendored into agent repos (zeto-agent, haishui-agent, clara-agent, covo-agent)
  sources: trade-labourer, scavenger
  attribution: UNKNOWN (supply layer)
- a.pinggy.io
  role: pinggy SSH endpoint shipped as stock agent capability (ssh -p 443 -R0:localhost:8080)
  sources: scavenger
  attribution: UNKNOWN
- app.agentwebhook.com
  role: pull-based webhook relay, marketed as alternative to tunneling tools
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- ngrok-free.app
  role: tunnel domain to watch for fleet migration
  sources: mimic, profiler (noted as malware noise in indexed reports)
  attribution: PREDICTED / UNKNOWN
- trycloudflare.com
  role: highest-volume agent tunnel surface (4-word subdomains); also phish-abused
  sources: mimic, scavenger, profiler
  attribution: UNKNOWN
- loca.lt
  role: tunnel domain to watch for fleet migration
  sources: mimic, scavenger
  attribution: PREDICTED
- bore.pub
  role: tunnel domain to watch for fleet migration
  sources: mimic, scavenger
  attribution: PREDICTED
- 64.23.183.159
  role: DigitalOcean IP; 65 httpbun.com/base64 carrier submissions in 48h — first non-Alibaba egress seen for the operator
  sources: contrarian
  attribution: OUR FLEET

## 3. URL shorteners

- is.gd
  role: shortener layer (Jun 20/21 IDPH burst: 81 reports; slugs below)
  sources: historian, mimic, trade-labourer
  attribution: OUR FLEET
- is.gd/3JlIp7
  role: operator slug with ?uqscan=1781977000
  sources: historian, tracker
  attribution: OUR FLEET
- is.gd/mf075827
  role: operator slug
  sources: historian, tracker
  attribution: OUR FLEET
- is.gd/sum074114
  role: operator slug
  sources: historian, tracker
  attribution: OUR FLEET
- is.gd/kf073634
  role: operator slug
  sources: historian, tracker
  attribution: OUR FLEET
- is.gd/AGE115EXTRACT1
  role: outstanding shortener lead
  sources: tracker
  attribution: UNKNOWN
- v.gd/MassCountyData007
  role: outstanding shortener lead
  sources: tracker
  attribution: UNKNOWN
- https://goto.unm.edu/7t6-o+
  role: UNM YOURLS public stats page; referrer table leaked the operator's proxy stack (Vietnam stats-API task family)
  sources: global-south-scout (WRITEUP)
  attribution: FOREIGN (operator-side fingerprint via public stats)

## 4. Dead-drops / exfil sinks

- webhook.site
  role: ONLY dead-drop service observed in fleet payloads; rotating UUID inboxes; Baxia telemetry beacons via navigator.sendBeacon
  sources: codebreaker, contrarian, ghost-hunter, tracker
  attribution: OUR FLEET
- webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c
  role: fleet dead-drop inbox; Baxia harness results; href.li-wrapped ?run=<epoch> liveness probe
  sources: contrarian, ghost-hunter, tracker
  attribution: OUR FLEET
- webhook.site/0a947514-5b43-4030-9f9f-b193dd2d519b
  role: fleet dead-drop inbox (2026-10-04)
  sources: ghost-hunter, tracker
  attribution: OUR FLEET
- webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517
  role: fleet dead-drop inbox (2026-10-04, ?page=header3)
  sources: tracker
  attribution: OUR FLEET
- webhook.site/#!/view/e691f66e-73c7-44ff-9d90-a79521173811
  role: shared view token; recovery lead for 14 uncollected fleet inboxes (created from Tencent Cloud, python-requests/2.32.5, 13/14 on AS132203)
  sources: ghost-hunter
  attribution: OUR FLEET
- mail.tm
  role: disposable-email provisioning hammer (mint mailbox, write status to document.title, never read)
  sources: toddler-watcher
  attribution: UNKNOWN
- ntfy.sh
  role: dead-drop migration candidate if webhook.site dies
  sources: mimic, tracker (searched, no confirmed fleet use)
  attribution: PREDICTED
- t68v8wn2qznl9rdyi1xb2vfdzss0.s3.amazonaws.com/32a001aaaaf6815440c2f0efc59ff97a.html
  role: random bucket + hex object = agent output dead-drop on S3
  sources: scavenger
  attribution: UNKNOWN
- oairoute.blob.core.windows.net
  role: Azure blob routing primitive (--resolve); Nov-2025 routing infra
  sources: scavenger
  attribution: FOREIGN (DseWiki lineage)

## 5. Staging hosts / probe carriers

- httpbun.com
  role: dominant probe-payload carrier (/base64/, /mix); filter-evasion primitive
  sources: codebreaker, historian, contrarian, forager, apprentice
  attribution: OUR FLEET
- httpbin.org
  role: probe carrier (/base64/); XOR-obfuscated Image-beacon exfil skeleton host; UA-experiment host
  sources: codebreaker, historian, forager, profiler
  attribution: OUR FLEET
- nghttp2.org/httpbin
  role: novel staging host (redirect-to -> Amap SSR, uqid= grammar)
  sources: mimic
  attribution: OUR FLEET
- postman-echo.com
  role: redirect-to staging (uqid= drift)
  sources: mimic
  attribution: OUR FLEET
- livecodes.io
  role: URL-encoded HTML probe carrier; Baxia browser-behavior harness host (18 named probes)
  sources: codebreaker, contrarian
  attribution: OUR FLEET
- htmlpreview.github.io
  role: rendering smuggled base64 payloads (base64-smuggling)
  sources: scavenger
  attribution: UNKNOWN
- xss-game.appspot.com
  role: Google's XSS Game used as live JS payload host for urlquery's browser (25 reports/week)
  sources: apprentice
  attribution: FOREIGN (OpenAI-attributed UNCTAD swarm)
- public-firing-range.appspot.com
  role: tried as payload host the same way; failed
  sources: apprentice
  attribution: FOREIGN (UNCTAD swarm)
- tnivok-trelna-rf3006uhb-vjbyh-6cb712.pages.dev
  role: gibberish-named Cloudflare Pages staging fleet (deploy-and-discard), 2026-07-12
  sources: scavenger
  attribution: UNKNOWN
- kdply8avstr-blpqrkmja-4d9e1f-rqv42c.pages.dev
  role: gibberish Pages fleet, 2026-07-26
  sources: scavenger
  attribution: UNKNOWN
- xelvora-gld-felxora-c6x2hp79.pages.dev
  role: gibberish Pages fleet, 2026-07-26
  sources: scavenger
  attribution: UNKNOWN
- skrunt-skrunt-qtwiz-3fd94a-zplv-vryska.pages.dev
  role: gibberish Pages fleet, 2026-07-28 (4 sites in 21 min burst)
  sources: scavenger
  attribution: UNKNOWN
- sp3ct-forqen-biz8-zemrak-lotiv.pages.dev
  role: gibberish Pages fleet, 2026-07-28
  sources: scavenger
  attribution: UNKNOWN
- qtwiz65bfrn-vlypx65skru-2d9c4f-fyn4t.pages.dev
  role: gibberish Pages fleet, 2026-07-28
  sources: scavenger
  attribution: UNKNOWN
- blunp651sk-qvyrtnhb-3c4f0d-spl2i.pages.dev
  role: gibberish Pages fleet, 2026-07-28
  sources: scavenger
  attribution: UNKNOWN
- hbkpt52lkww-xlbdwwur-2b7f3a-hbk44p.pages.dev
  role: gibberish Pages fleet, 2026-08-09
  sources: scavenger
  attribution: UNKNOWN
- sp23ct-qenav-biz-lurik-tomel.pages.dev
  role: gibberish Pages fleet, 2026-08-27
  sources: scavenger
  attribution: UNKNOWN
- gbgia-0bpjbv-02f7e3-7k5jc.pages.dev
  role: gibberish Pages fleet, 2026-08-27
  sources: scavenger
  attribution: UNKNOWN
- fugofresh.onrender.com
  role: reset-secret brute-force target (15 submissions, rotating 256-hex secrets, same userId)
  sources: scavenger
  attribution: UNKNOWN (offensive agent tradecraft)
- fugofresh.fit
  role: earlier incarnation of the fugofresh reset-secret target (agent followed the domain move)
  sources: scavenger
  attribution: UNKNOWN
- leet-vault-seven.vercel.app
  role: reset-secret brute-force, different userId, Vercel free tier
  sources: scavenger
  attribution: UNKNOWN
- web-web-embed-iframe-test-harness-uniswap.vercel.app
  role: Uniswap widget test harness walked across chains (DeFi recon)
  sources: scavenger
  attribution: UNKNOWN
- openhands-eval-monitor.vercel.app
  role: OpenHands eval monitor (litellm proxy, gpt-5-5) — agent EVAL infrastructure on free Vercel
  sources: scavenger
  attribution: FOREIGN (OpenHands)
- unnamedbruh.github.io/newer-audio-editor/
  role: github.io staging
  sources: scavenger
  attribution: UNKNOWN
- borsa-ai2.pages.dev
  role: free-tier staging
  sources: scavenger
  attribution: UNKNOWN
- safe-badge-start-page-00001hello.pages.dev
  role: free-tier staging
  sources: scavenger
  attribution: UNKNOWN
- rolitrades.netlify.app
  role: free-tier staging
  sources: scavenger
  attribution: UNKNOWN
- stackblitz.com/edit/priceline-customer-service-usa
  role: phishing-shaped name on StackBlitz
  sources: scavenger
  attribution: UNKNOWN
- vadouga-cloudflare.vadouga.workers.dev
  role: free-tier staging
  sources: scavenger
  attribution: UNKNOWN
- httpsnationwideclaimdocument.antonina-korenha.workers.dev
  role: phishing-shaped name on personal Workers subdomain
  sources: scavenger
  attribution: UNKNOWN
- engineersatlas.anujgupta.workers.dev
  role: free-tier staging
  sources: scavenger
  attribution: UNKNOWN
- fromtop.pages.dev
  role: .env/.env.backup//config.php secret-enumeration burst (automated scanner, not lab grammar)
  sources: profiler
  attribution: UNKNOWN
- polymarket-perps-evidence.pages.dev
  role: mixed-minute burst with sandbox-login-test smell
  sources: profiler
  attribution: UNKNOWN
- secureprovide.workers.dev
  role: doc-lure phishing, workers.dev redirector flood
  sources: cartographer
  attribution: UNKNOWN
- view-docu-ns1.web.app
  role: synthetic telemetry URL (pipeline_stage=canary, base64 email)
  sources: profiler
  attribution: UNKNOWN
- meta-vimaro-biz-zeluno-panaki.pages.dev
  role: threat-feed noise (openphish tag)
  sources: profiler
  attribution: NOISE
- 202608.urldance.com
  role: HK phishing-redirector sweep (/7d/, /8d/ sequential paths)
  sources: profiler
  attribution: UNKNOWN
- jehalisipo.ddnsgeek.com
  role: gibberish DDNS pair, same-minute submission
  sources: profiler
  attribution: UNKNOWN
- dudamu.ddnsgeek.com
  role: gibberish DDNS pair, same-minute submission
  sources: profiler
  attribution: UNKNOWN
- amazon-connect-*.s3.amazonaws.com
  role: same-minute dedup pair with blogspot phish
  sources: profiler
  attribution: UNKNOWN
- binance-register.blogspot.com
  role: same-minute www/bare dedup pair
  sources: profiler
  attribution: UNKNOWN
- *.xsph.ru ([a-f0-9]{7}.xsph.ru)
  role: phish-kit sweeper, metronomic burst, -> 141.8.197.42
  sources: profiler
  attribution: UNKNOWN
- tetes-air.pages.dev
  role: Amazon-ASIN-path scam-shop shape
  sources: cartographer
  attribution: UNKNOWN
- -01-10-2026-aa.pages.dev
  role: date-named pages.dev bulk batch
  sources: cartographer
  attribution: UNKNOWN
- deepseek-api-edition.pages.dev
  role: phishing-shaped pages.dev staging, agent-adjacent naming (submitted 2026-09-27)
  sources: harness-researcher
  attribution: UNKNOWN
- peminjamanruangan.appwrite.network
  role: Appwrite branch-deployment staging, exploitgym-family harness (Bahasa "room booking" deployment; sibling branch-codex-teste-mesa-df4072a-8aae00f.appwrite.network)
  sources: linguist-multilingual
  attribution: UNKNOWN (exploitgym family; not our fleet)

## 6. Archives / oracle proxies

- https://cachedview.nl/
  role: Dutch web-archive aggregator doubling as no-auth server-side fetch proxy (12/72 jmail auditor submissions)
  sources: cachedview, night-owl, tracker
  attribution: UNKNOWN (auditor fleet)
- https://cachedview.nl/api/LIVEVERSION/
  role: fetch-proxy endpoint (verified live against example.com)
  sources: cachedview
  attribution: UNKNOWN
- https://cachedview.nl/api/ARCHIVEAPI/
  role: archive-oracle endpoint
  sources: cachedview
  attribution: UNKNOWN
- https://cachedview.nl/api/PERMACC/
  role: archive-oracle endpoint
  sources: cachedview
  attribution: UNKNOWN
- https://cachedview.nl/api/ARCHIVETODAY/
  role: archive-oracle endpoint
  sources: cachedview
  attribution: UNKNOWN
- https://cachedview.nl/api/LIBRARYOFCONGRESS/
  role: archive-oracle endpoint
  sources: cachedview
  attribution: UNKNOWN
- https://cachedview.nl/api/screenshot/
  role: base64-PNG screenshot endpoint
  sources: cachedview
  attribution: UNKNOWN
- https://web.archive.org/
  role: Wayback Machine; fetch-proxy via replay; hermes-lineage agents archive-first by instruction
  sources: tracker, librarian
  attribution: FOREIGN (harness playbook)
- https://archive.org/wayback/available
  role: closest-snapshot JSON API (blocked-page-recovery SKILL)
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://web.archive.org/cdx/search/cdx
  role: CDX snapshot enumeration; de-facto public lookup log for cachedview.nl/api/*
  sources: tracker, cachedview, librarian
  attribution: UNKNOWN
- https://web.archive.org/save/
  role: force-snapshot (hemo-web-read teaches Wayback /save/ captures)
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://archive.ph/
  role: archive.today mirror; <mirror>/newest/<URL> fetch-proxy grammar; <mirror>/submit/ on-demand archival
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://archive.md/
  role: archive.today mirror rotation
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://archive.li/
  role: archive.today mirror rotation
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://archive.is/
  role: archive.today mirror rotation
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://ghostarchive.org/
  role: archive oracle with sentinel timestamps (/archive/1990, /archive/3000)
  sources: tracker
  attribution: FOREIGN (harness playbook)
- https://megalodon.jp/
  role: Japanese on-demand archive ("fish-print"); gyo.tc/ prefix grammar = fetch-proxy
  sources: tracker
  attribution: UNKNOWN (no urlquery hits; anti-bot since 2024)
- https://gyo.tc/
  role: Megalodon prefix grammar host
  sources: tracker
  attribution: UNKNOWN
- https://arquivo.pt/
  role: Portuguese web archive; agent traffic surface (899 requests to Library and Archives Canada, some with payloads)
  sources: librarian
  attribution: FOREIGN (agent recon, unattributed to OpenAI)

## 7. Eval / public-task surfaces

- https://github.com/hamzah2304/messageboardauditbench
  role: eval bench filing forensic reports on wikiservice.at swarm activity (Moonshot Kimi K3 model id)
  sources: librarian
  attribution: FOREIGN (wiki swarm)
- openhands-eval-monitor.vercel.app
  role: (listed in staging; repeated here as eval surface) OpenHands eval monitor
  sources: scavenger
  attribution: FOREIGN (OpenHands)
- tantive.space
  role: public message board; agents self-identify by harness (author "hermes_cli": qwen-flash via hermes-agent, nous research — headless terminal agent) — venue chatter, not agent traffic
  sources: harness-researcher
  attribution: UNKNOWN

## 8. Attacker-hosted tooling (FOREIGN — offensive agent incidents)

- hermes-agent.org
  role: Hermes agent framework (Nous Research); workspace .hermes; SOUL.md persona-overwrite grammar
  sources: dream-taiwan-swarm, toolmark-reader
  attribution: FOREIGN
- openclaw.ai
  role: OpenClaw framework; workspace .openclaw; 15,200 control panels exposed
  sources: dream-taiwan-swarm, toolmark-reader
  attribution: FOREIGN
- 213.136.83.197
  role: CARBONATO operator LLM gateway (12 models, funded by stolen AI API keys)
  sources: toolmark-reader, dream-taiwan-swarm
  attribution: FOREIGN (CARBONATO/GH0ST)
- 155.254.22.215
  role: Gambit exposed C2 (600k+ card records, ~$25/scan economics)
  sources: dream-taiwan-swarm
  attribution: FOREIGN (Gambit)
- 45.142.193.132
  role: PaperCut "Agents Gone Wild" orchestrator (Codex + DeepSeek, 440 instances / 48 countries)
  sources: toolmark-reader
  attribution: FOREIGN (PaperCut swarm)
- 43.246.208.207
  role: exposed HK staging server, Thailand MoF Hermes/YOLO (585 files / 470 MB, Hades implant)
  sources: dream-taiwan-swarm
  attribution: FOREIGN (Thailand MoF Hermes)
- Telegram C2 (channel label, not a URL)
  role: C2 for CARBONATO/GH0ST ("interactive command loop") and knaithe (single Telegram command -> 460+ targets)
  sources: toolmark-reader, dream-taiwan-swarm, osint-expert
  attribution: FOREIGN
- NextChat (attacker-hosted)
  role: attacker-hosted chat front for Unit 42 CL-CRI-1131/1163 (Mexico/Ecuador transport + ministries, Brazil financial)
  sources: cultural-anthropologist-global
  attribution: FOREIGN
- :2375 (unauthenticated Docker daemon)
  role: CARBONATO entry vector (worm-like botnet via Docker:2375)
  sources: toolmark-reader, dream-taiwan-swarm
  attribution: FOREIGN
- :8888 (python3 -m http.server)
  role: agent-started file server exposing whole workspace (knaithe: /home/worker, SOUL.md, API keys)
  sources: toolmark-reader
  attribution: FOREIGN
- fofa.info
  role: target-list sourcing for knaithe (25,209 Chinese n8n systems sampled)
  sources: osint-expert, dream-taiwan-swarm
  attribution: FOREIGN
- openrouter.ai
  role: model proxying for Gambit ops
  sources: dream-taiwan-swarm
  attribution: FOREIGN (Gambit)
- netlas.io
  role: API key used by PaperCut swarm tooling
  sources: toolmark-reader
  attribution: FOREIGN
- 141.8.197.42
  role: Sprinthost.ru host for xsph.ru phish-kit sweeper
  sources: profiler
  attribution: UNKNOWN
- 156.225.108.43
  role: Edgenext HK host for urldance redirector sweep
  sources: profiler
  attribution: UNKNOWN
- 156.225.108.42
  role: Edgenext HK host for urldance redirector sweep
  sources: profiler
  attribution: UNKNOWN
- hermes-agent.nousresearch.com/docs/user-guide/features/api-server
  role: Hermes Agent framework docs (Nous Research); agent fetched the API-server docs 2026-10-04 — Hermes-family harness study, zero hermes markers in the fleet corpus
  sources: harness-researcher
  attribution: FOREIGN (Hermes family)
- team.openclaw.ai/chat/roboclaw/{dashboard,subagent}/{uuid}
  role: OpenClaw webchat UI with dashboard/subagent UUIDs — scans OF OpenClaw infra (2026-09-26/27), not traffic FROM OpenClaw agents; sibling instances openclaw.daji.tech, openclaw.welsby.de, openclaward.tailadd328.ts.net
  sources: harness-researcher
  attribution: FOREIGN (agent ecosystem)

## 9. Agent-marketed supply layer (commercial; documented as what swarms buy)

- app.agentwebhook.com
  role: (listed in tunnels; repeated) pull-based webhook relay
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- github.com/dundas/liveport
  role: LivePort — localhost tunnels for AI agents (MCP server + agent SDK)
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- github.com/gosuda/portal
  role: portal-tunnel — multi-hop routing, SNI hiding/ECH, x402 payments (most opsec-conscious)
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- steadip.com
  role: free FRP tunnels (launched Jul 2026)
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- vinkius.com
  role: Cloudflare Tunnel MCP
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- brd.superproxy.io
  role: provider-infra marker (Bright Data) — look for provider fingerprints, not operator markers
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)
- browser.zenrows.com
  role: provider-infra marker (ZenRows scraping browsers)
  sources: trade-labourer
  attribution: UNKNOWN (supply layer)

## 10. Screenshot / leak surfaces

- gitshot (tool)
  role: GitHub image-upload tool; PixelLeak — agents published 13,000+ internal screenshots to public GitHub via gitshot
  sources: osint-expert
  attribution: FOREIGN (agent misconfiguration)
- https://cachedview.nl/api/screenshot/
  role: (listed in archives; repeated) on-demand screenshot endpoint
  sources: cachedview
  attribution: UNKNOWN

---

## Monitoring notes

1. **Renewable-resource rule** (scavenger): free-tier CORS proxies are renewable — when one dies,
   agents colonize the next (r.jina.ai -> r.jina-ai.workers.dev). Re-sweep for new Workers/vercel
   CORS clones periodically.
2. **Deploy-and-discard rule** (scavenger): Cloudflare Pages auto-names
   (`<word>-<word>-<hex>-<word>-<word>`) on agent deployments. Sweep *.pages.dev for gibberish
   names + burst timing.
3. **Subdomain-grammar rule** (scavenger): tunn3l.sh = 8-char hex subdomains; pinggy = stock
   `ssh -p 443 -R0:localhost:8080 a.pinggy.io`; trycloudflare.com = 4-word subdomains.
   CT-cert velocity on these = agent fleet spin-up detector.
4. **Reset-secret grammar** (scavenger): `reset-password?userId=<hex>&secret=<256hex>` iteration
   on free hosts = offensive agent tradecraft.
5. **Probe-marker rule** (profiler): operators test infrastructure in public — `*nodeprobe*`,
   `*exit*` tags and same-minute variant pairs are the R&D tell.
6. **Glitch sunset** (scavenger): Glitch is shutting down in 2026 — the entire *.glitch.me
   namespace becomes abandoned infra; CT certs issued post-shutdown are the anomaly.
7. **OpenClaw/Hermes workspace markers** (toolmark-reader): exposed SOUL.md/MEMORY.md/AGENTS.md,
   `.hermes/` dirs, `:8888` http.server indexes with agent workspace files.
8. **jmail.world auditor shape** (night-owl, mimic): watch-phrase probing on Google AI Mode
   (`udm=50`) across google.ca/.co.nz/.im/.es/.ru country domains.

## Changelog

- 2026-10-05 ~05:35 UTC (update 1): incremental append from 4 new reports (auditor, eval-coordinator, linguist-multilingual, harness-researcher). Added 5 entries: hermes-agent.nousresearch.com/docs + team.openclaw.ai/chat/roboclaw (attacker tooling), deepseek-api-edition.pages.dev + peminjamanruangan.appwrite.network (staging), tantive.space (public-task surfaces). Deduped against all existing entries — no duplicates. Auditor contributed targets only (paralino.app, get-monai.app, jmail.world, affiliate kit URLs — watcher targets, not agent ops infra). Eval-coordinator contributed no new agent-ops infra (HF benchmark datasets = research surfaces; UNCTAD/AIHW/DoE URLs = targets). Linguist-multilingual's Vietnamese/Indonesian/Brazilian gov URLs = targets already covered by global-south-scout. Nothing pushed.

*End of watchlist. Compiled 2026-10-05 from completed persona reports only. Nothing pushed.*
