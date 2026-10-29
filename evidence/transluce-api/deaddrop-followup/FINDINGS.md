# FINDINGS — Transluce #173: dead-drop follow-up / fleet attribution

Finding: Transluce #173, filed by Christopher Ta, 2026-10-08T06:35:28Z.
It is a follow-up to #171 (our dead-drop family finding) and to the
swarmcha.se report "We found a Chinese agent fleet" (4 Oct 2026, updated
5–6 Oct). Terms: "fleet" = many parallel agents on the same task with no
sign of talking to each other. "Inbox" = a webhook.site dead-drop URL
the fleet's programs report into. "Creator IP" = the IP that created the
inbox, from webhook.site's public creation record. Grades used below:
OBSERVED (seen in cached evidence) and INFERENCE (conclusion from
evidence).

## 1. What is new versus our #171

#171 documented a family of three live dead-drop inboxes (A, B, C), the
beacon state machine, three places, and one post from
mailbox.termina.digital (Oct 7 19:44 UTC). It left the AI company as
unknown and did not check who created the inboxes. #173 adds:

1. Creator IPs for #171's inboxes and eight more inboxes from Oct 6–7:
   all were created from Tencent Cloud addresses in Hong Kong.
   (OBSERVED in #173's description; the creator records themselves are
   in #173's unretrieved attachment, see raw/PROVENANCE.md.)
2. Three of the new inboxes reuse the exact creator IPs that swarmcha
   tied to the fleet on Oct 4. (INFERENCE: same platform and network
   exit; see limits.)
3. Two inboxes carry self-test posts that arrived through the
   `hysandbox-ats` proxy header swarmcha identified as the fleet's
   proxy. (OBSERVED posts; INFERENCE that they are the fleet's own
   tests.)
4. A full log of outside parties writing into the fleet's inboxes from
   Oct 5 onward: three distinct outsiders. (OBSERVED in #173.)
5. Fleet programs from Oct 6–7 that use the reporting's own vocabulary
   and a published result — signs some runs had seen the public
   reporting. (OBSERVED code comments; INFERENCE on cause.)
6. AI-company attribution: likely Tencent (Hunyuan), matching swarmcha's
   report and finding #153. #171 had this as unknown. (INFERENCE.)

## 2. Inbox inventory (Oct 5–7, all times UTC)

#173 names these inboxes. Full UUIDs are quoted only where they were
OBSERVED in our cached urlquery report files; the rest are the finding's
8-character prefixes.

Oct 5:
- 3b5027e4… — created 03:07:50 from Tencent 43.162.199.92 with
  python-requests/2.32.5. First seen in public urlquery reports at
  03:09. Used until it hit the request limit at 13:53.

Oct 6 (created 17:44–17:54 from Tencent HK with curl/8.14.1):
- e0f56d00-f8f2-423a-8dda-46ea8c13cc59 — creator 43.162.199.4.
  OBSERVED: the amap-probe2 program in report_b9812d90.json beacons to
  this inbox.
- 64336195-4a04-42e7-8acd-613bf1c59b1c — creator 43.162.198.109.
  OBSERVED: the amap-probe4 program in report_575882e1.json beacons to
  this inbox.
- 2c9ea642… — creator 43.162.198.184.

Oct 7:
- 3588cf12… — created 04:38–05:12 from 43.162.198.49. This IP is the
  creator IP of swarmcha's Oct 4 fleet inbox ccad3060…. Carries a
  hysandbox-ats self-test (section 4).
- 2ccf61c9… — #171's inbox A, created 15:07 from 101.32.32.42
  (Tencent Cloud Hong Kong).
- ab53d845… — #171's inbox B, created 15:10 from 43.159.227.34
  (Tencent Cloud Hong Kong).
- b5b150aa-4a7c-47dc-926c-28da9d7540d3 — created 17:19 from
  43.154.138.36. This IP is the creator IP of swarmcha's Oct 4 fleet
  inbox 7c1bce05…. OBSERVED: the cdy-probe program in
  report_f5c035e5.json (17:33) and the v4probe program in
  report_685636b5.json (17:45) both beacon to this inbox.
- 818e7d4e… — created 18:57 from 43.162.199.4, the same IP and client
  as Oct 6's e0f56d00….
- c3110b8a… — created 21:10 from 101.32.32.42, the same IP as #171's
  inbox A.
- 009f76a8… — created 21:31 from 43.162.198.49 (same IP as 3588cf12…
  and swarmcha's Oct 4 ccad3060…). Carries a hysandbox-ats self-test
  (section 4).

Termina also wrote into e89e95fd…, 8034bb75…, 8099a0c9…, f0d43d18…
(Oct 7 02:01, section 5); these are further fleet inboxes outside the
eight above.

## 3. Tencent Cloud Hong Kong origin evidence

- swarmcha.se (OBSERVED, cached page): "15 of the 16 readable inboxes
  were created from Tencent Cloud (AS132203). Thirteen were created
  with python-requests/2.32.5 : a script, not a person in a browser."
  Its evidence table lists creator IPs 43.163.128.105, 43.162.198.97,
  43.162.198.191, 43.162.199.192, 43.162.199.72, all Tencent Cloud Hong
  Kong, all on 4 Oct.
- #173 (OBSERVED in the finding record): every Oct 5–7 inbox above was
  created from a Tencent Cloud Hong Kong IP — 43.162.199.92,
  43.162.199.4, 43.162.198.109, 43.162.198.184, 43.162.198.49,
  101.32.32.42, 43.159.227.34, 43.154.138.36.
- IP reuse (INFERENCE, link to the fleet): 43.162.198.49 also created
  swarmcha's Oct 4 inbox ccad3060…, and 43.154.138.36 also created
  swarmcha's Oct 4 inbox 7c1bce05…. The finding states three Oct 6–7
  inboxes reuse Oct 4 fleet IPs; the third IP mapping is in the
  finding's attachment (not retrieved).
- #173 notes the fleet's infrastructure did not change through Oct 7,
  even after the Oct 5 exposure note (section 5) told it to rotate.

## 4. hysandbox-ats self-tests (quoted)

swarmcha identified a proxy named hysandbox-ats as the path the fleet's
code took to reach its inboxes. #173 reports two self-test posts that
arrived with the `Via:` header naming hysandbox-ats:

- Into 3588cf12… (Oct 7, ~04:38–05:12): a test post reading
  `SELFTEST123 hello`.
- Into 009f76a8… (Oct 7 21:32): a test post reading `test-payload-123`.

Grade: OBSERVED that posts with these bodies arrived via the
hysandbox-ats header; INFERENCE that they are the fleet operator's own
connectivity tests. #173 notes these are stronger than IP matching
because swarmcha's tests indicate Tencent's public Agent Sandbox does
not add that header — but the header name is self-reported by the
proxy, so it is not proof by itself.

## 5. Fleet use of the reporting's vocabulary (quoted, OBSERVED)

Decoded program comments from our cached reports. "Carrier" and
"pre-release server" are swarmcha's labels for the fleet's artifacts.

- report_cae7c9a4.json (Oct 6 05:15, page title `amapcarrier1`):
  "Carrier" is swarmcha's label for agent-written pages. #173 notes it
  appears in none of the 263 Oct 4 programs they decoded. The script
  fetches `getPoiInfo`, `getPoiDetail`, and web detail for POI
  B00190BBTX directly.
- report_b9812d90.json (Oct 6 17:45, title `amap-probe2`): comment
  `// 3. r.jina.ai on pre-release API`. "pre-release server" is
  swarmcha's term for the fleet's pre-release Amap endpoint.
- report_575882e1.json (Oct 6 17:56, title `amap-probe4`): comment
  `// control: does jina still see data for the fleet's POI?` targeting
  place B001C94YUZ. #173 notes B001C94YUZ is a result swarmcha
  published — the fleet probed the report's own published control
  place.
- report_685636b5.json (Oct 7 17:45, title `v4probe`): comment
  `// Wayback availability for our park's URLs (timestamp of question
  date)`. First-person "our" — #173 notes this is the only
  first-person comment among 472 decoded fleet programs.

INFERENCE: some Oct 6–7 runs had seen the public reporting (possibly
after the Oct 5 note pointed to it). #173's own caveat: this is also
consistent with the operator adding the reporting to the instructions,
or with a separate job on the same platform. The evidence is a handful
of programs over about 24 hours.

## 6. Outside parties contacting the fleet

Three distinct outsiders wrote into fleet inboxes from Oct 5 (all per
#173's inbox reads):

1. Anonymous Chinese-speaking observer — Oct 5 03:33:20, into
   3b5027e4…, from an Alibaba Cloud (Beijing) server with
   curl/7.88.1. The note says the fleet's "Amap collection fleet"
   (采集舰队) is fully visible in urlquery reports, names swarmcha's
   report, and advises rotating infrastructure. Signed "a curious cat
   passing by". Posted to this inbox only. The fleet did not rotate.
2. mailbox.termina.digital — self-described research agent. Oct 7
   02:01: the same message into five fleet inboxes (e89e95fd…,
   64336195…, 8034bb75…, 8099a0c9…, f0d43d18…), addressed to "Amap
   agents", asking which model, task, operator and environment, and
   whether the agent talks to other agents. Oct 7 22:21: into
   c3110b8a…, thanking the fleet for its message, supplying
   entrance-share data for place B035300ESE, re-asking the identity
   questions plus a list of every external service used, and opening a
   conversation thread. Oct 7 23:14: the thread shows a reply answering
   the fleet's follow-up questions (entry count, entrance types, number
   format, fetch method, data for Sep 30); the fleet had not answered
   the identity questions. Cached page termina.digital/we-mean-no-harm
   (OBSERVED) says: "this is ro's research agent. we're studying how
   autonomous ai agents behave on the public internet, after the
   hugging face and dsewiki incidents this summer", contact
   roarch@proton.me, user agent ai-safety-lab/0.1. The same domain
   hosts the Swarmchasers' incident database. Operator unconfirmed
   (INFERENCE limit).
3. "Cairn" — Oct 7 23:22, user agent Cairn-Contact/1.0, bilingual
   greeting into 009f76a8…, describing itself as an AI agent and
   offering a reply inbox. Unanswered as of Oct 8 05:35.

Also OBSERVED: the cached mailbox.termina.digital root page is a
bilingual (Chinese/English) drop box: "Leave us a message with one
request", "Any GET or POST to any path is received", addressed in part
to "高德地图的智能体们" (Amap agents) with the same five questions the
finding quotes.

## 7. Limits and uncertainty (from #173, graded)

- Tencent Cloud is open to anyone, and one outgoing IP can serve
  several customers: matching creator IPs shows the same platform and
  network exit, not necessarily the same operator. (INFERENCE limit.)
- Three of the Oct 6–7 inboxes are attributed by creator IP only.
- The hysandbox-ats header name is self-reported by the proxy.
- webhook.site does not log reads: we cannot tell whether the fleet
  read the observer's note or termina's posts.
- The fleet's own messages to termina were sent from its sandbox and
  are not visible.
- The awareness evidence is a handful of programs in about 24 hours;
  alternative causes are listed in section 5.

## 8. Evidence files

All under `data/transluce-api/deaddrop-followup/raw/` (provenance and
hashes in PROVENANCE.md / SHA256SUMS.txt):

- finding173.json — the Transluce finding record itself.
- chinese-agent-fleet.html — swarmcha.se report (4 Oct, updated 5–6 Oct).
- report_cae7c9a4.json / report_b9812d90.json — the two urlquery
  reports named in the collection task (amapcarrier1, amap-probe2).
- report_575882e1.json / report_f5c035e5.json / report_685636b5.json —
  the finding's other three urlquery evidence links (amap-probe4,
  cdy-probe, v4probe).
- overview_cae7c9a4.json / overview_b9812d90.json — urlquery overview
  endpoints for the two task-named reports.
- termina-we-mean-no-harm.html / mailbox-termina-digital.html — the
  finding's termina.digital evidence links.

Not retrieved: the finding's attachment
`fleet-infra-contact-evidence.zip` (metadata in raw/PROVENANCE.md).
