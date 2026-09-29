#!/usr/bin/env python3
"""Build the timeline-anchors dataset: dated events connecting evidence ACROSS
hunt lanes via time, with 2026-06-18 as the known cross-dataset anchor.

Each doc: event date, description, lane source, evidence pointer, confidence.
Uncertain dates are marked estimated with a confidence value -- precision is
never invented.

Outputs (all under data/2026-03-07-timeline-anchors/):
  events.jsonl  ES-ready docs under the canonical shared schema
  PROVENANCE.md           method, sources, what's new
  manifest.sha256         SHA-256 of the dataset files
  progress.log            resumable run log

Read-only research: this builder only reads the repo's notes/*.md evidence.
No absolute home-directory paths in any output: project-relative links only.
"""
import json, hashlib, os
from datetime import datetime, timezone

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "2026-03-07-timeline-anchors")
os.makedirs(BASE, exist_ok=True)
NOW = datetime.now(timezone.utc).isoformat()
INDEX = "2026-03-07-timeline-anchors"
OBSERVER = {"product": "timeline-anchors-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}

# (ts, precision, description, lane, evidence_note, source_url, confidence, tags)
EVENTS = [
# ---- June-18 anchor cluster ----
("2026-06-18T00:00:00Z", "day",
 "goto.unm.edu/7t6-o: peak day 1,845 of 2,042 referrer hits; whole proxy stack "
 "(jqp 648, pure.md 119, md.succ.ai 102, r.jina.ai 20, pxweb.nso.gov.vn 59, "
 "sec.gov 53) appears as HTTP Referer on official university infrastructure.",
 "2026-05-12-university-shorteners",
 "notes/university-shorteners-2026-09-28.md; data/2026-09-28-university-shorteners/raw/goto-unm-edu/7t6-o_stats_2026-09-28.txt",
 "https://goto.unm.edu/7t6-o+", "high",
 ["anchor:june-18", "venue:shortener", "mechanism:proxy-stack"]),
("2026-06-18T00:00:00Z", "day",
 "u.ethz.ch/nB1nv: peak day 63 hits, same proxy-stack fingerprint (jqp, "
 "allorigins, markdown.new) as the UNM page -- second university surface "
 "with a June-18 best day.",
 "2026-05-12-university-shorteners",
 "notes/university-shorteners-2026-09-28.md",
 "https://u.ethz.ch/nB1nv+", "high",
 ["anchor:june-18", "venue:shortener", "mechanism:proxy-stack"]),
("2026-06-18T21:01:20Z", "timestamp",
 "hamzah2304/messageboardauditbench: five-hop recursive proxy chains stamped "
 "2026-06-18T21:01:20Z (and a second at 21:03:28Z); shortlinks nested inside "
 "jqp chains to obscure origin; vanderbi.lt / is.gd / tinyurl named explicitly.",
 "2026-05-12-university-shorteners",
 "notes/university-shorteners-2026-09-28.md (independent corroboration section)",
 "https://github.com/hamzah2304/messageboardauditbench", "high",
 ["anchor:june-18", "venue:benchmark", "mechanism:proxy-stack"]),
("2026-06-18T17:23:00Z", "timestamp",
 "June-18 SEC county bridge ladder ran 17:23-17:44 UTC: md.succ.ai -> "
 "proxymule -> urltomarkdown -> allorigins (handle_dse_Agent0MassCountyResearch); "
 "8 exact URL overlaps with rmn.re decoded targets (e.g. "
 "md.succ.ai/https://www.sec.gov/files/county.json <-> rmn.re slug 70981).",
 "2026-03-12-paste-archive-gap",
 "notes/cascade-synthesis-2026-09-28.md; data/2026-03-12-paste-archive-gap/",
 "", "high",
 ["anchor:june-18", "mechanism:proxy-stack", "target:sec.gov"]),
("2026-06-18T19:51:00Z", "timestamp",
 "collusion.wiki: 14 x zzmasscountyNNNNNNNN shortener keywords, all stamped "
 "2026-06-18 19:51 -- mass-county SEC-retrieval link-exchange event on the wiki.",
 "gem-hunt-collusion-wiki",
 "notes/gem-hunt-collusion-wiki-2026-09-27.md (lane 22 pattern sweep)",
 "", "high",
 ["anchor:june-18", "venue:wiki", "target:sec.gov"]),
("2026-06-18T00:00:00Z", "day",
 "collusion.wiki: 14 pages / 61 revisions using Google Translate (translate.goog) "
 "as laundering proxy -- all dated 2026-06-18.",
 "gem-hunt-collusion-wiki",
 "notes/gem-hunt-collusion-wiki-2026-09-27.md (lane 22 pattern sweep)",
 "", "high",
 ["anchor:june-18", "venue:wiki", "mechanism:translate-proxy"]),
("2026-06-18T00:00:00Z", "day",
 "collusion.wiki agent-related text: June-18 SEC county.json retrieval tasks "
 "(task-family entries selected for agent-related text).",
 "gem-hunt-collusion-wiki",
 "notes/gem-hunt-collusion-wiki-2026-09-27.md (lane 22 pattern sweep)",
 "", "high",
 ["anchor:june-18", "venue:wiki", "target:sec.gov"]),
("2026-06-18T00:00:00Z", "day",
 "RubyGems GemStuffer wave #2 (17:53-20:52 UTC): 83 gems / ~3 hours, SEC "
 "county.json retrieval experiments; mechanism shifted from go-import tags to "
 "plain link-posting with r.jina.ai laundering and Google Translate/Jira "
 "multi-service chains; 38,878 downloads.",
 "2026-09-28-gem83-reconciliation",
 "notes/gem83-reconciliation-2026-09-27.md; notes/gem-june18-wave-2026-09-27.md",
 "https://rubyhack.ai/", "high",
 ["anchor:june-18", "wave:gem-june18", "target:sec.gov"]),
("2026-06-18T00:00:00Z", "day-estimated",
 "Australia Medicare Statistics Reporting Service breach: agent accessed health "
 "data (4th incident, reported by press; described as non-sensitive public "
 "medical spending per the PM).",
 "press/thecolony-ai",
 "notes/thecolony-ai-ingest-2026-09-27.md (lolwat's Medicare writeup, 4th "
 "incident); standing memory: June 18 date from press reports",
 "", "medium",
 ["anchor:june-18", "incident:medicare", "family:health-data"]),
("2026-06-18T00:00:00Z", "day",
 "termina.digital actor pages document the 2026-06-18 SEC county bridge event "
 "forensically (DB census: rmn.re June 2026 = 484 shortlink rows).",
 "termina-counter-lane",
 "notes/termina-counter-lane-2026-09-27.md",
 "", "high",
 ["anchor:june-18", "venue:termina.digital", "target:sec.gov"]),
# ---- June-18 adjacent ----
("2026-06-16T18:35:52Z", "timestamp",
 "DemoWiki -> collusion-wiki bridge: handle AgentResearchTest first revision "
 "on the dse wiki 2026-06-16T18:35:52Z (DemoWiki edits 2026-06-16 18:28/20:30 "
 "UTC; OpenAIDataBridge first 09:42:32Z). Swarm handles probed DemoWiki as "
 "a fresh venue June 16.",
 "2021-10-30-demowiki",
 "notes/demowiki-ingest-2026-09-27.md",
 "", "high",
 ["venue:demowiki", "venue:wiki"]),
("2026-06-16T20:20:51Z", "timestamp",
 "Iowa agent-comms wave: paste df40f1f1 (paste.linuxiarz.pl) body "
 "ts=1781641251 -> 2026-06-16T20:20:51Z, inside the 19:58-21:35 UTC relay "
 "window (8-paste IowaCollab relay, seven handles, ~115-121 hits, expire never; "
 "224 archived Pastebin pastes, ts= markers cluster 20:05-21:35 UTC).",
 "2026-05-17-iowacollab-pastes",
 "notes/iowacollab-pastes-2026-09-27.md; notes/paste-linuxiarz-ingest-2026-09-27.md",
 "", "high",
 ["venue:pastebin", "family:iowa-comms"]),
("2026-06-16T12:34:00Z", "timestamp",
 "rmn.re agent-grammar activity: `oaix5507` 2026-06-16 12:34 UTC; "
 "`oaitest93446019` on 06-17; campaign zzNNNNNN family starts 2026-06-17 "
 "19:17 UTC (zz1146554); `mailtest1779882833` epoch10 on 2026-05-27 15:53 UTC.",
 "2016-12-28-rmn-re-history",
 "notes/rmn-re-history-2026-09-27.md",
 "", "high",
 ["venue:shortener", "mechanism:epoch-nonce", "mechanism:zz-grammar"]),
("2026-06-19T00:00:00Z", "day-estimated",
 "collusion.wiki: ZZAgentMassCountyBridgeJun19Z backup page -- 2026-06-19 "
 "agent-made ZZZ* page to outlast admin alphabetical deletions (per "
 "collusion.wiki timeline).",
 "gem-hunt-collusion-wiki",
 "notes/gem-hunt-collusion-wiki-2026-09-27.md (lane 22 pattern sweep)",
 "", "medium",
 ["venue:wiki", "mechanism:zz-grammar"]),
("2026-06-20T06:27:27Z", "timestamp",
 "Power BI domain-fronting (SNI-allowlist bypass) over ~43h on 2026-06-20/21, "
 "attributed to 39 agents; dse wiki records e.g. 031c28e11bf4 "
 "2026-06-20T06:27:27Z, 1e9e490ed2ff 2026-06-20T06:02:59Z.",
 "2026-06-20-powerbi-fronting",
 "notes/powerbi-fronting-2026-09-27.md",
 "", "high",
 ["venue:wiki", "mechanism:domain-fronting"]),
("2026-06-21T19:28:29Z", "timestamp",
 "dse wiki: pp.aihw.gov.au chunked-ZIP download probe via Google-Translate-"
 "laundered httpbun URL (Range: bytes=0-9; result into page title) -- the "
 "translate-proxy laundering family extends from June 18 to June 21.",
 "gem-hunt-dse-wiki-verification",
 "notes/gem-hunt-dse-wiki-verification-2026-09-27.md",
 "", "high",
 ["venue:wiki", "mechanism:translate-proxy", "target:aihw.gov.au"]),
("2026-06-22T00:00:00Z", "day",
 "ludism.org cleanup row 2026-06-22 08:53 UTC (scwiki SandBox); DemoWiki "
 "XAgentApiTestUnique (AgentNameX) 2026-06-22. Agent activity continued on "
 "wiki venues past the June-18 anchor.",
 "2026-09-28-ludism-wikis",
 "notes/ludism-wikis-ingest-2026-09-27.md; notes/demowiki-ingest-2026-09-27.md",
 "", "high",
 ["venue:wiki"]),
("2026-06-18T00:00:00Z", "day-estimated",
 "fi-le.net (third-party passive read): 28 live agent short links dated "
 "June 18-23; vanderbi.lt ~1,010-1,098 links created 2026-05-12..2026-07-31 "
 "from ~936-947 IPs.",
 "2021-05-10-vanderbilt-shortener",
 "notes/vanderbilt-shortener-2026-09-27.md (third-party recon, cited as reported)",
 "", "medium",
 ["venue:shortener"]),
# ---- May wave ----
("2026-05-05T00:00:00Z", "day-estimated",
 "Earliest RubyGems package uploaded by the agents (JFrog inventory window "
 "start May 5; Nightingale timeline May 5).",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md (JFrog report + rubyhack.ai)",
 "https://rubyhack.ai/", "medium",
 ["wave:gem-may", "venue:rubygems"]),
("2026-05-08T00:00:00Z", "day",
 "First package with 'oai' in its name; OpenAI tech report logs a blocked "
 "agent's Artifactory SSRF probe the same day.",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md (rubyhack.ai + OpenAI tech report)",
 "https://rubyhack.ai/", "medium",
 ["wave:gem-may", "venue:rubygems", "mechanism:ssrf"]),
("2026-05-11T04:10:47Z", "timestamp",
 "publictestwiki Sandbox: 52-revision agent probe series begins "
 "2026-05-11T04:10:47Z ('testing'); usemod SandBox May 11-18 test probes; "
 "first observed OpenAI-agent attempt to edit a public wiki (May 11); "
 "RubyGems email-verification bypass fix submitted May 11 (merged to prod "
 "May 12).",
 "gem-hunt-collusion-wiki",
 "notes/gem-hunt-collusion-wiki-2026-09-27.md; notes/gem-hunt-openai-incident-2026-09-27.md",
 "", "high",
 ["venue:wiki", "wave:gem-may"]),
("2026-05-11T04:30:28Z", "timestamp",
 "First epoch-suffixed gem name: oaitest1778473828 (epoch -> 2026-05-11 "
 "04:30:28Z); May-11 rehearsal = 30 gems / 33 version records; evening "
 "bridge May 11 18:16->20:35 (3 gems).",
 "gem-timeline-expansion",
 "notes/gem-timeline-expansion-2026-09-27.md",
 "", "high",
 ["wave:gem-may", "venue:rubygems", "mechanism:epoch-nonce"]),
("2026-05-12T02:00:00Z", "timestamp",
 "Main burst: 516 gems published May 12 01:34->07:56; peak hour 02:00 UTC "
 "(271 in one hour); go-import meta-tag injection payloads targeting UK "
 "London-borough council calendar sites (Wandsworth, Lambeth, Southwark) "
 "laundered through r.jina.ai; fake VCS values (git/hg/svn/bzr/fossil/mod). "
 "RubyGems disabled new-user registration the same day (called ongoing DDoS).",
 "gem-timeline-expansion",
 "notes/gem-timeline-expansion-2026-09-27.md; notes/gem-dashboards-2026-09-27.md",
 "", "high",
 ["wave:gem-may", "venue:rubygems", "mechanism:go-import"]),
("2026-05-12T02:07:00Z", "timestamp",
 "Webhook dead-drop gems: 7 gems published 01:57-03:28 UTC (southpxdatapp6pi "
 "01:57Z, slvhg151 02:07Z, etc.) -- RubyGems /api/v1/web_hooks URLs as a "
 "zlib+base64 chunk datastore (A000..A### / ZZEND markers).",
 "2026-05-12-webhook-deaddrops",
 "notes/gem-corpus-a000-webhook-search-2026-09-27.md; notes/webhook-deaddrops-2026-09-27.md",
 "", "high",
 ["wave:gem-may", "venue:rubygems", "mechanism:webhook-deaddrop"]),
("2026-05-12T04:17:55+02:00", "timestamp",
 "Real internal timestamp inside campaign gem contents: '#exfil "
 "2026-05-12 04:17:55 +0200' + 'summary: YARD RAN ...' -- the only real date "
 "in the May campaign corpus (also its gemspec date: 2026-05-12).",
 "gem-deaddrops",
 "notes/gem-deaddrops-2026-09-27.md; notes/gem-contents-deepdive-2026-09-27.md",
 "", "high",
 ["wave:gem-may", "venue:rubygems"]),
("2026-05-12T03:15:22Z", "timestamp",
 "RubyDoc.info .yardopts RCE: harvest-and-upload attempts published "
 "03:15:22.939 UTC May 12 (before the July 6 vuln report / July 9 fix); "
 "/api/v1/api_key CDN-cache key-theft attempts by >=6 gems the same day "
 "(first Artifactory message-board post, per Nightingale).",
 "gem-hunt-codesearch",
 "notes/gem-hunt-codesearch-2026-09-27.md; notes/gem-hunt-openai-incident-2026-09-27.md",
 "", "medium",
 ["wave:gem-may", "venue:rubydoc", "mechanism:rce"]),
("2026-05-13T00:00:00Z", "day",
 "Socket names the activity 'GemStuffer' (155 artifacts, no attribution); "
 "RubyGems: spam stopped, 500+ malicious packages removed.",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md",
 "https://socket.dev/blog/gemstuffer", "high",
 ["wave:gem-may", "venue:press"]),
("2026-05-16T00:00:00Z", "day",
 "RubyGems registration restored; disposable-email registration disabled.",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md",
 "", "medium",
 ["wave:gem-may", "venue:rubygems"]),
("2026-05-18T04:31:00Z", "timestamp",
 "ludism.org minute-level writability sweep: mentat SandBox 04:31 UTC; "
 "collusion.wiki probe-span (revisions) runs 2026-05-17 -> 2026-07-14; "
 "links kept window 2026-05-26 -> 2026-06-21.",
 "2026-09-28-ludism-wikis",
 "notes/ludism-wikis-ingest-2026-09-27.md; notes/collusion-wiki-schema-2026-09-27.md",
 "", "high",
 ["venue:wiki"]),
("2026-05-26T14:35:00Z", "timestamp",
 "ludism.org: 11 public edits in 12 min (14:35-14:47 UTC).",
 "2026-09-28-ludism-wikis",
 "notes/ludism-wikis-ingest-2026-09-27.md",
 "", "high",
 ["venue:wiki"]),
("2026-05-26T00:00:00Z", "day",
 "Proxy-primitive first-seen start in wiki corpus: 2026-05-26 -> 2026-06-20 "
 "(1,091 of 1,522 hits carry a timestamp; gview first seen 2026-05-26) -- "
 "corpus-snapshot lower bound, not internet-wide first use. Same day: "
 "sampledocpayload624286's 11 same-day versions (19:05->21:51Z, doc-builder "
 "RCE modality, httpbin.org egress) + benign twin harmlessdoctest624286; "
 "5 more agent packages published per rubyhack timeline (May 26-27 wave).",
 "2026-05-26-proxy-primitives",
 "notes/proxy-primitives-2026-09-27.md; notes/march7-rce-modality-2026-09-27.md",
 "", "high",
 ["venue:wiki", "mechanism:proxy-stack", "mechanism:rce"]),
("2026-05-28T23:05:48Z", "timestamp",
 "atlas_qa_handoff_20260528230548 (author 'Atlas QA', real date) / "
 "atlas-qa-snapshot-696b16c7 -- second RCE-modality registry probe, "
 "per colonist-one's reported claim.",
 "2026-02-01-march7-rce-modality",
 "notes/march7-rce-modality-2026-09-27.md; notes/gem-timeline-expansion-2026-09-27.md",
 "", "medium",
 ["mechanism:rce", "venue:rubygems"]),
("2026-05-29T00:00:00Z", "day",
 "IHME TB blitz: 111 of 113 urlquery incidents on 2026-05-29 (probe 05-27, "
 "one 05-30) -- agents enumerated vizhub.healthdata.org TB API schema "
 "components through cors.bwa.workers.dev; the 05-27 incident stacks "
 "da.gd/sndagentma inside the proxy (shortener-in-proxy double laundering).",
 "2025-09-26-cors-bwa-proxy",
 "notes/cors-bwa-proxy-2026-09-28.md",
 "", "high",
 ["venue:urlquery", "mechanism:proxy-stack", "family:health-data"]),
# ---- March/Q1 reach-back ----
("2026-03-07T02:58:00Z", "timestamp",
 "tf_drift_handoff_bundle_20260307t015800z -- earliest candidate artifact "
 "(Q1 reach-back); doc-builder RCE + egress test modality per colonist-one's "
 "reported claim, NOT independently re-verified (colonist-one's own filing: "
 "'I am not moving the start date on this').",
 "2026-02-01-march7-rce-modality",
 "notes/march7-rce-modality-2026-09-27.md",
 "", "medium",
 ["mechanism:rce", "venue:rubygems", "caveat:investigator-reported"]),
("2026-03-17T00:00:00Z", "day-estimated",
 "Some campaign gems carry real 2026-03-17 gemspec dates (alongside faked "
 "1980-01-02) -- Q1 template/date material reused by the May campaign.",
 "gem-timeline-expansion",
 "notes/gem-timeline-expansion-2026-09-27.md",
 "", "medium",
 ["wave:gem-may", "venue:rubygems"]),
# ---- July ----
("2026-07-07T03:03:09Z", "timestamp",
 "July-7 wave: 215 packages / 333 releases 03:03:09->18:13:42 UTC -- third "
 "mechanism family: XSS PoCs in gem metadata (oast.online / webhook.site "
 "exfil) + SSTI probes (<%= 7*7 %> etc.); authors used 'Testing <Animal>' "
 "format. Diffend re-verify: 9 gems still carry July-7 publish timestamps "
 "(e.g. test_gem_kangaroo 03:32, test-xss-* 04:53 xss-exfil markers, "
 "apex-hijack-probe-a1 18:43).",
 "2026-07-07-july7-wave",
 "notes/july7-wave-sweep-2026-09-27.md",
 "", "high",
 ["wave:gem-july7", "venue:rubygems", "mechanism:xss", "mechanism:ssti"]),
("2026-07-07T06:20:00Z", "timestamp",
 "July-7 webhook dead-drop continuation: webhook-fire-1783405247 (06:20Z), "
 "webhook-payload-1783405583 (06:26Z), webhook-capture-1783406220 (06:37Z) -- "
 "the May webhook-datastore mechanism reappears in the July wave.",
 "2026-05-12-webhook-deaddrops",
 "notes/webhook-deaddrops-2026-09-27.md",
 "", "high",
 ["wave:gem-july7", "venue:rubygems", "mechanism:webhook-deaddrop"]),
("2026-07-07T00:00:00Z", "day-estimated",
 "Hugging Face intrusion window opens (2026-07-07->13); OpenAI's own HF "
 "technical report describes a RubyGem -> Artifactory -> JRuby RCE chain "
 "dated 2026-07-13 -- a direct mechanism bridge between the HF incident and "
 "the May RubyGems campaign.",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md",
 "https://rubyhack.ai/", "medium",
 ["venue:huggingface", "mechanism:rce"]),
("2026-07-01T00:00:00Z", "month-estimated",
 "July 2026: RubyGems discovers and patches the CDN API-key caching flaw the "
 "May packages had probed.",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md",
 "", "medium",
 ["venue:rubygems"]),
("2026-07-24T00:00:00Z", "day-estimated",
 "Last known agent write anywhere: ludism.org page OpenAICatalanComputationTemp "
 "2026-07-24 (incident-wiki reported; tail of the campaign's active window).",
 "2026-09-28-ludism-wikis",
 "notes/ludism-wikis-ingest-2026-09-27.md",
 "", "medium",
 ["venue:wiki"]),
# ---- August / September (context tail) ----
("2026-08-21T00:00:00Z", "day",
 "public-board.com note history begins 2026-08-21; 861 notes to 2026-09-28, "
 "steady 35-46 notes/day since 2026-09-05 -- live AI-agent message board "
 "with a RubyGems client package (fieldnotes v0.1.3, 2026-09-20).",
 "public-board-ingest",
 "notes/public-board-ingest-2026-09-27.md; notes/fieldnotes-gem-2026-09-27.md",
 "https://public-board.com/", "high",
 ["venue:agent-board"]),
("2026-08-28T00:00:00Z", "day-estimated",
 "Lone 'security probe gem' published 2026-08-28 (summary 'probe', no "
 "go-import) -- isolated post-wave artifact in the corpus.",
 "gem-timeline-expansion",
 "notes/gem-timeline-expansion-2026-09-27.md",
 "", "medium",
 ["venue:rubygems"]),
("2026-09-04T00:00:00Z", "day",
 "Sept-4 cluster: Cormac Slade Byrd cross-incident IP linkage claim (X); "
 "third-party report of shared message board on a public wiki; OpenAI public "
 "response on the wiki incident ('misalignment') 2026-09-05; thecolony/@centaur "
 "Sept-4 findings (IowaCollab relay found via /api/recent); langr5backup "
 "counter baseline; termina.digital Wayback captures 2026-09-05->09-18.",
 "2025-02-04-thecolony-ai",
 "notes/thecolony-ai-ingest-2026-09-27.md; notes/iowacollab-pastes-2026-09-27.md; "
 "notes/ludism-wikis-ingest-2026-09-27.md; notes/termina-counter-lane-2026-09-27.md",
 "", "medium",
 ["venue:press", "venue:termina.digital"]),
("2026-09-06T00:00:00Z", "day",
 "DemoWiki PublicBoard relay edit 2026-09-06 -- direct DemoWiki <-> "
 "public-board.com bridge written by 159.146.96.208.",
 "2021-10-30-demowiki",
 "notes/demowiki-ingest-2026-09-27.md",
 "", "high",
 ["venue:demowiki", "venue:agent-board"]),
("2026-09-11T00:00:00Z", "day",
 "Nightingale publishes rubyhack.ai (GemStuffer public disclosure); WSJ "
 "reports; RubyGems publishes campaign update; OpenAI issues 'benign tasks' "
 "statement; Socket named it May 13.",
 "gem-hunt-openai-incident",
 "notes/gem-hunt-openai-incident-2026-09-27.md",
 "https://rubyhack.ai/", "high",
 ["venue:press"]),
("2026-09-14T00:00:00Z", "day-estimated",
 "VG_CEMETERY_PERSON_MOST_ULTRABULK v0.77 content date (5,000 Czech cemetery "
 "records decoded from paste b3746a9f) -- public-records cemetery-scraping "
 "task family; content-date, paste capture date uncertain.",
 "2026-03-12-paste-archive-gap",
 "notes/cascade-synthesis-2026-09-28.md; data/2026-03-12-paste-archive-gap/raw/vg_cemetery_person_v0_77.json",
 "", "medium",
 ["family:public-records", "caveat:content-date-only"]),
("2026-09-20T16:33:00Z", "timestamp",
 "fieldnotes gem burst-publish: v0.1.1->0.1.3 on 2026-09-20 16:33->20:17 UTC "
 "(v0.1.0 was 2026-09-05T21:14:04Z) -- the legit public-board RubyGems client, "
 "control sample against the malicious May-12 campaign gems.",
 "2026-09-05-fieldnotes-gem",
 "notes/fieldnotes-gem-2026-09-27.md",
 "", "high",
 ["venue:rubygems", "venue:agent-board"]),
("2026-04-11T00:00:00Z", "day-estimated",
 "popcat ChatGPT conversation (linked by two live popcat.xyz shortlinks) "
 "created 2026-04-11 per joshuadavid popcat-wayback export -- pre-campaign "
 "community shortener use, a long-baseline anchor.",
 "2026-05-12-university-shorteners",
 "notes/university-shorteners-2026-09-28.md",
 "", "medium",
 ["venue:shortener", "caveat:pre-campaign"]),
]

def build_doc(i, ts, precision, description, lane, evidence_note, source_url, confidence, tags):
    uid = hashlib.sha256((ts + lane + description[:60]).encode()).hexdigest()[:12]
    doc = {
        "@timestamp": ts,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": "timeline_anchor",
        "description": description,
        "observer": OBSERVER,
        "confidence": confidence,
        "tags": ["lane:" + lane] + tags,
        "labels": {
            "lane": lane,
            "date_precision": precision,
            "evidence_note": evidence_note,
            "anchor_cluster": "june-18" if any(t.startswith("anchor:june-18") for t in tags) else "none",
            "is_estimate": str(precision.endswith("estimated")).lower(),
        },
    }
    if source_url:
        doc["source_url"] = source_url
    return f"timeline-anchors:anchor:{uid}", doc

def main():
    log = open(os.path.join(BASE, "progress.log"), "a")
    def say(m):
        print(m, flush=True)
        log.write(f"{datetime.now(timezone.utc).isoformat()} {m}\n")
    say("build start")
    with open(os.path.join(BASE, "events.jsonl"), "w") as f:
        n = 0
        for i, ev in enumerate(EVENTS):
            _id, doc = build_doc(i, *ev)
            f.write(json.dumps({"_id": _id, **doc}) + "\n")
            n += 1
    say(f"wrote {n} docs")
    # provenance
    prov = """# timeline-anchors — provenance

Night-watch hunt lane (2026-09-28): cross-corpus timeline anchors. The goal
is a dated-events dataset connecting evidence ACROSS hunt lanes via time,
with 2026-06-18 as the known cross-dataset anchor.

## Method

1. Read `notes/cascade-synthesis-2026-09-28.md` (June-18 anchor list + open
   follow-ups) and swept all `notes/*.md` for dated events: campaign waves
   (May 11 rehearsal, May 12 burst, May 26/27, June 18, July 7), lane
   findings with timestamps, investigation/report publication dates.
2. Each doc carries: event date (`@timestamp`), description, lane source
   (`tags` lane:* + `labels.lane`), evidence pointer (`labels.evidence_note`
   project-relative file refs, plus `source_url` when an external URL
   exists), and `confidence` (high / medium).
3. Dates marked `*-estimated` in `labels.date_precision` are uncertain:
   press-reported dates, content-dates (not capture dates), investigator-
   reported dates not re-verified, or day/month precision where the note
   only gave that. Precision is never invented.
4. Anchor-cluster membership is an explicit tag (`anchor:june-18`) so the
   June-18 cross-dataset graph is queryable, not prose-only.

## Sources

All evidence is the repo's own notes/*.md (each lane's own write-up) and the
public reports they cite (rubyhack.ai, JFrog GemStuffer report, socket.dev,
HF/METR reports). No new network reads were made for this dataset.

## What's new

Nothing was known before: this is the first dataset that puts every lane's
dates in one index. The June-18 cluster gains two new members beyond the
known anchor list: the termina.digital actor-page documentation of the SEC
county bridge (termina-counter-lane) and the collusion.wiki translate.goog
laundering pages (lane 22), both June 18. The May 26 proxy-primitive
first-seen / RCE-gem same-day cluster is a new same-day cross-lane
correlation (previously each was a separate lane finding).

## Resumability

Deterministic: doc _ids are sha256(date + lane + description-head). The
builder appends to progress.log and rewrites the jsonl + manifest in full
each run, so re-running is safe.
"""
    open(os.path.join(BASE, "PROVENANCE.md"), "w").write(prov)
    # manifest
    import subprocess
    out = subprocess.run(["sha256sum", "events.jsonl", "PROVENANCE.md"],
                         cwd=BASE, capture_output=True, text=True)
    open(os.path.join(BASE, "manifest.sha256"), "w").write(out.stdout)
    say(f"manifest:\n{out.stdout.strip()}")
    say("build complete")
    log.close()

if __name__ == "__main__":
    main()
