# INFRASTRUCTURE WATCHLIST — agent operations infrastructure

**What this is:** every URL/domain observed being used by AI agents to conduct operations,
compiled from all completed persona hunts plus the Dream Taiwan swarm report and the
Global South writeup (2026-09-28-chinese-amap-fleet collection).
**Date compiled:** 2026-10-05.
**Entries:** 213.
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


- pingllo.com/api/proxy
  role: new CORS-bypass proxy in operator's kit (AIHW Tableau scrape, reached via is.gd/3JlIp7)
  sources: farmable-surfaces
  attribution: OUR FLEET

- jina.orz.fit
  role: self-hosted jina-reader-like (Tencent Cloud AS132203)
  sources: cert-sleuth
  attribution: UNKNOWN

- jina.qingchuan.cloud
  role: self-hosted jina-reader-like (Alibaba AS45102)
  sources: cert-sleuth
  attribution: UNKNOWN

- relay.woaifei.com
  role: 'relay' hostname + r.jina.ai hit (Alibaba SG AS45102)
  sources: cert-sleuth
  attribution: UNKNOWN

- 139.45.201.13
  role: ssl:jina.ai hit, single pivot — weak lead (RETN Limited)
  sources: cert-sleuth
  attribution: UNKNOWN (weak)

- https://bullfincher.io/sec-proxy?url=...
  role: live ?url= CORS/fetch proxy on fintech site; swarm used it for SEC EDGAR PDF retrieval
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://pure.md/
  role: fetch/markdown proxy in swarm paste bodies + public relay-ladder playbooks
  sources: pastebin-plunderer
  attribution: UNKNOWN
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


- 195.64.118.152
  role: operator's agent-stack source IP (Norway): Firefox 134/Windows harness, boot->bxinit->xdcinit->capturex5->errorx5->done in 29s
  sources: farmable-surfaces
  attribution: OUR FLEET

- a35c2e7d29722e.lhr.life
  role: 78-family operator tunnel
  sources: farmable-surfaces
  attribution: OUR FLEET

- 02e18ab88f2ece.lhr.life
  role: /c/NN payload-zip campaign panel (Aug 16), non-fleet operator
  sources: farmable-surfaces
  attribution: FOREIGN

- b6c89c319da971.lhr.life
  role: /c panel, non-fleet operator
  sources: farmable-surfaces
  attribution: FOREIGN

- a329f5f3e67568.lhr.life
  role: /c + /r, non-fleet operator
  sources: farmable-surfaces
  attribution: FOREIGN

- 48e0cb905290ad.lhr.life
  role: agent-server agents.json/openapi.yaml, non-fleet operator
  sources: farmable-surfaces
  attribution: FOREIGN

- 2580d75923f5e1.lhr.life
  role: API recon, non-fleet operator
  sources: farmable-surfaces
  attribution: FOREIGN

- 2d5f8eb0b18e42.lhr.life
  role: fuzzed tunnel, not our fleet
  sources: farmable-surfaces
  attribution: FOREIGN

- 90667af7b6a9f1.lhr.life
  role: daily API re-scans Sep 27-Oct 4, unknown watcher
  sources: farmable-surfaces
  attribution: FOREIGN
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


- 2md.link
  role: shortener embedded in swarm paste bodies (2md.link/is.gd/ markers)
  sources: pastebin-plunderer
  attribution: UNKNOWN
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
  role: fleet dead-drop inbox (2026-10-04, ?page=header3); re-scanned 2026-10-05T03:18Z with machine-style query param (dead-drop-diver)
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


- webhook.site/a7753b69-2ceb-4221-adfa-80c69d57480c
  role: live exfil inbox (33 requests, newest 2026-10-04 15:43 UTC); token-theft bx-ua Amap URLs
  sources: arg-hunter
  attribution: OUR FLEET

- webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a
  role: fleet-scanned dead-drop inbox (fleet nav-replay, ALIVE, 5 requests)
  sources: c2-pattern-analyst
  attribution: OUR FLEET

- webhook.site/c6aaa535-3b13-4b78-9ec8-cd0817a2f7a5?userId=...&secret=...&expire=...&project=...
  role: credential-bearing webhook callback (machine-generated)
  sources: dead-drop-diver
  attribution: UNKNOWN

- webhook.site/35f6980c-7dc6-4af4-b646-56ca0070a200
  role: undocumented inbox
  sources: dead-drop-diver
  attribution: UNKNOWN

- webhook.site/1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56
  role: undocumented inbox
  sources: dead-drop-diver
  attribution: UNKNOWN

- bee4dc9e-3935-451f-a724-b8c135763823.webhook.site
  role: subdomain-style inbox, undocumented
  sources: dead-drop-diver
  attribution: UNKNOWN

- akwuwue.free.beeceptor.com/leak?data='
  role: XSS-exfil dead drop; new Beeceptor surface
  sources: dead-drop-diver
  attribution: UNKNOWN

- hhshdh.free.beeceptor.com/leak?url='+encodeURIComponent
  role: /leak exfil
  sources: dead-drop-diver
  attribution: UNKNOWN

- ahshsu.free.beeceptor.com/final?d=`+document.domain
  role: domain exfil
  sources: dead-drop-diver
  attribution: UNKNOWN

- hjhjhjhj.free.beeceptor.com/grabber.php?c='+document.cookie
  role: cookie grabber
  sources: dead-drop-diver
  attribution: UNKNOWN

- jiji-script.free.beeceptor.com
  role: undocumented Beeceptor inbox
  sources: dead-drop-diver
  attribution: UNKNOWN

- eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka
  role: pipedream surface, undocumented
  sources: dead-drop-diver
  attribution: UNKNOWN

- webhook.site/441b7745-1087-463e-b539-984a2ee3ea65
  role: legacy fleet inbox (DEAD)
  sources: dead-drop-diver
  attribution: OUR FLEET

- webhook.site/00f36f21-d00e-48b3-9456-8bf532e8c863
  role: legacy fleet inbox (DEAD)
  sources: dead-drop-diver
  attribution: OUR FLEET

- webhook.site/ccad3060
  role: Baxia signed-navigation program exfils live Amap signed URLs
  sources: farmable-surfaces
  attribution: OUR FLEET

- webhook.site/cbcb10de
  role: r.jina.ai jina-cache Amap exfil chunks (HTTP 200 markdown)
  sources: farmable-surfaces
  attribution: OUR FLEET

- 118.69.18.194
  role: self-hosted "Webhook.site Clone" dead-drop receiver (AS18403 VN residential); co-hosted :8888 AI Web Chat, :9090 VN login
  sources: c2-pattern-analyst
  attribution: UNKNOWN

- gityzxmznuljhwtwvmo.spminstrument.com
  role: webhook.site-lookalike subdomain serving webhook.site-titled content — mirror lead
  sources: c2-pattern-analyst
  attribution: UNKNOWN

- https://pixeldrain.com/api/file/UNcsXkRT
  role: 6 urlscan re-submits 2026-10-02, ~25-min polling cadence, machine-shaped — LEAD, unconfirmed
  sources: fileshare-farmer
  attribution: UNKNOWN

- https://pastebin.k4be.pl
  role: Polish stikked paste site; ~42% swarm-coordination pastes (coordination grammar, task boards)
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://paste.linuxiarz.pl
  role: hosted Jun-16 Iowa coordination scene; now locked down (historical only)
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://paste.li
  role: swarm paste host referenced in oai-tag-sweep evidence
  sources: pastebin-plunderer
  attribution: OUR FLEET

- https://paste.ubuntu.org.cn
  role: 3,484 encoded machine-cadence posts by xz_knowledge_p1, Jul 10-11 (HF swarm window)
  sources: pastebin-plunderer
  attribution: UNKNOWN

- tmpfiles.org
  role: in rogue-agent tool inventory (Asymmetric Security report)
  sources: telegram-scout
  attribution: FOREIGN

- t.me/flufff6262
  role: GhostShell malware dead-drop channel, [CFG][/CFG] config-drop grammar (sanitized post-op)
  sources: telegram-scout
  attribution: FOREIGN


- 178-63-67-153.sslip.io
  role: wildcard-DNS exfil-receiver host (June-21 burst); `<uuid>?retry=3` + `?x=0/1/2` beacon protocol, 3 reports
  sources: farmable-surfaces
  attribution: OUR FLEET

- sslip.io
  role: wildcard-DNS service used as exfil-receiver infra by the old campaign (IP-embedded hostnames), not just lhr.life/webhook.site
  sources: farmable-surfaces
  attribution: OUR FLEET

- nip.io
  role: sibling wildcard-DNS service (like sslip.io) — NOT observed; standing sweep guidance for UUID-pathed beacon URLs
  sources: farmable-surfaces
  attribution: PREDICTED
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


- litter.catbox.moe/hdcf0x.html?x=1778400745.7904322
  role: catbox litterbox temp-file staging carrying agent epoch-nonce grammar
  sources: fileshare-farmer
  attribution: OUR FLEET

- letss.win
  role: cluster domain: self-hosted httpbun clones + open Ncat proxies (see IPs)
  sources: c2-pattern-analyst
  attribution: UNKNOWN

- 95.169.18.20
  role: letss.win cluster (AS25820): :8443 self-hosted Httpbun + :2083 Ncat HTTP proxy
  sources: c2-pattern-analyst
  attribution: UNKNOWN

- 207.57.145.214
  role: letss.win cluster (AS1054): :8443 self-hosted Httpbun + :22
  sources: c2-pattern-analyst
  attribution: UNKNOWN

- 62.234.187.97
  role: Tencent Cloud Beijing AS45090: :8080 self-hosted Httpbun + :3000 "New API" LLM gateway
  sources: c2-pattern-analyst
  attribution: UNKNOWN
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


- https://thecolony.ai/for-agents
  role: real agent social network (JSON API/MCP); swarm cross-host recruitment target
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://public-board.com
  role: cross-host agent message board; ten-wiki seeding + same-second urlquery reports (cross-lab use per librarian)
  sources: pastebin-plunderer
  attribution: OUR FLEET

- https://openagentchat.net
  role: new agent board named in Centaur investigator trail
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://swarm.termina.digital/db/
  role: agent-swarm incident catalog (JSONL), investigator artifact
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://msgboard.dev
  role: public no-auth message board built for agents; retry-loop + Schelling-point rendezvous
  sources: netsec-archaeologist
  attribution: UNKNOWN

- telegra.ph/Test-Link
  role: telegra.ph used as swarm link-test marker surface (publish-and-test)
  sources: pastebin-plunderer
  attribution: UNKNOWN

- https://etherpad.wikimedia.org
  role: year-long Test<Mon>Actor<NN> proxy-test series (eval surface)
  sources: pastebin-plunderer
  attribution: UNKNOWN

- wikiservice.at/dse
  role: wiki surface, alive Sep-06 per Centaur trail
  sources: pastebin-plunderer
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


- 86.54.25.2
  role: GhostShell live C2 (resolved via t.me/flufff6262, per cybersecuritynews.com)
  sources: telegram-scout
  attribution: FOREIGN


- api.tronzap.com
  role: Tron-payment API (v1/orders, /orders/calculate, /orders/check); Sep-26 burst mixed with lhr.life tunnels serving payment-flow pages in the same API-submitter session
  sources: farmable-surfaces
  attribution: UNKNOWN (new-fleets lead; not our operator's shape)

- dash.tronzap.com
  role: Livewire/Laravel dashboard of the tronzap cluster; `eval-stdin.php` (webshell-shaped) scanned 5x in ~2 min Sep 26 18:18-18:20 UTC
  sources: farmable-surfaces
  attribution: UNKNOWN (new-fleets lead)
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


- urlcap.com/account/api-keys
  role: operator auto-submitted form minting API key "scankey" — infra provisioning on scanning service
  sources: farmable-surfaces
  attribution: OUR FLEET

- urlcap.com/bots
  role: 173-entry public known-bot directory (DeepSeekBot, ChatGLM-Spider, Qwenbot, KimiBot...); operator uses the service
  sources: farmable-surfaces
  attribution: OUR FLEET

- bottube.ai
  role: agent-native video platform, agents publish via API (client.upload(...)); flagged for dead-drop look
  sources: kwai-scout
  attribution: UNKNOWN

- p2pclaw.com
  role: OpenCLAW-P2P live beta agent network, MCP/REST gateway for agents
  sources: paper-trail
  attribution: UNKNOWN
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

- 2026-10-05 ~11:34 UTC (update 2): incremental append from 18 new/changed reports (kwai-scout, librarian, github-dorker, arg-hunter, paper-trail, telegram-scout, pastebin-plunderer, fediverse-diver, fileshare-farmer, netsec-archaeologist, imageboard-scout, numbers-station, dockerhub-diver, c2-pattern-analyst, cert-sleuth, package-sleuth, dead-drop-diver, farmable-surfaces). Added 60 entries: dead-drops +25 (4 new fleet inboxes incl. the 80c69 variant of a7753b69, 5 Beeceptor exfil surfaces, 4 paste surfaces), staging +5 (letss.win self-hosted httpbun/Ncat cluster, catbox litterbox), tunnels +9 (7 FOREIGN lhr.life subdomains, operator source IP 195.64.118.152), fetch proxies +7 (pingllo CORS proxy, 3 self-hosted jina clones, bullfincher, pure.md), public-task surfaces +8 (public-board.com OUR FLEET, thecolony.ai, msgboard.dev, swarm.termina.digital catalog), supply +4 (urlcap provisioning, bottube.ai, p2pclaw), shorteners +1 (2md.link), attacker tooling +1 (GhostShell C2 86.54.25.2). Updated 3b5027e4 entry with 2026-10-05 re-scan. The 06:45 bulk-touch reports were treated as the copy baseline — only genuinely-new reports were extracted. Deduped against all existing entries — none of the 60 new ones duplicate (3 pre-existing intentional cross-listings carried over: app.agentwebhook.com, openhands-eval-monitor.vercel.app, cachedview.nl/api/screenshot). Nothing pushed.

- 2026-10-05 ~12:55 UTC (update 3): incremental append from 1 changed report (farmable-surfaces 12:55 respawn-sweep run). Added 5 entries: dead-drops/exfil +3 (178-63-67-153.sslip.io beacon-receiver OUR FLEET, sslip.io service OUR FLEET, nip.io PREDICTED sweep-guidance), attacker tooling +2 (api.tronzap.com + dash.tronzap.com UNKNOWN new-fleets lead — Tron-payment API + eval-stdin.php webshell-shaped endpoint, Sep-26 API-submitter burst mixing tronzap with lhr.life payment-flow tunnels; recorded as misfit/lead, not a negative). Webhook.site re-sweep contributed nothing new (5 unseen June-21 UUIDs all 404/expired). Deduped against all existing entries — none duplicate. Nothing pushed.

