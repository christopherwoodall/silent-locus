# Writeup 1: `lhr.life` — the operator's tunnel-and-probe backbone (Jan–Oct 2026)

## What it is

`lhr.life` is the public domain of **localhost.run**, a free SSH tunneling service (ngrok-like): `ssh -R 80:localhost:8080 nokey@localhost.run` gives you a public `<hex>.lhr.life` URL. The subdomains in our data are ephemeral tunnels, now mostly returning Cloudflare "no tunnel."

What makes this an *operator* finding rather than background noise: the tunnels carry a consistent, purpose-built probe/CORS-test harness fingerprinted by the **`uq` tag grammar** — the same grammar family as the Amap fleet's `uqscan=`/`uqtag=`.

## Observed infrastructure

- **Shape**: random hex subdomains (`<16-hex>.lhr.life`), probe pages (`probe.html`, `probe2.html`, `combo.html`), `probe.js` staged via httpbun base64 programs chained *through Google Translate* (`httpbun-com.translate.goog/base64/<program>` loading `//<hex>.lhr.life/probe.js`)
- **Smoking gun**: `/uqcors.html` (8 hits) — a CORS test page using the **`uq` prefix**, same family as `uqscan=`/`uqtag=`/`uqvnc=`
- **Burst evidence**: 8 identical `uqcors.html?v=1` submissions in 2 minutes (2026-06-18 14:37–14:38 UTC) = **8 parallel workers**
- **Tag grammar**: `?n=<epoch>`, `?x=<19-digit>`, `?slow=<19-digit>`, `?fix=<19-digit>`, `?cached=<19-digit>`, `?v=1`
- **Beacon programs**: `<body>KEEP<script>setInterval(()=>fetch('/get?x='+Date.now()).catch(()=>{}),200)</script>` — 200ms keep-alive beacons
- **Timeline**: Jan 2026 (first probes) → Jun 18 (CORS burst) → Jun 21 (17-report probe burst) → Oct 4 (still active; independently corroborated by the PL/TR/AR lane finding live translate.goog-wrapped probe-loaders)

## Unified operator timeline (`uq` grammar as the thread)

| Date | Activity |
|---|---|
| Jan 2026 | lhr.life probing begins |
| Jun 18 | `uqcors.html` CORS burst (8×/2min); AIHW `uqvnc=` on Australian aged-care data |
| Jun 20–21 | IDPH Iowa health-data burst (48 reports); lhr.life probe burst (17) |
| Sep 27 | IDPH via jina (3 reports) |
| Sep 28–Oct 5 | Amap fleet (2,141 reports) |
| Oct 2 | AIHW PBS dashboard + data files |
| Oct 4 | Amap + lhr.life concurrently active |

One operator, one infrastructure, multiple task families over 10 months. The "Amap fleet" is the latest task family, not an isolated incident.

## Related: AIHW (Australian health data)

`www.aihw.gov.au/reports/aged-care/mental-health-in-aged-care/data?uqvnc=1781776074.018263` — report `5b1c95bb`, 2026-06-18. `uq` grammar on Australian government health data, same June window as IDPH. Health-data targeting + `uq` tags + June 2026 = likely the same operator. AIHW report list appended below the lhr.life list.

## Is any of this new or reported?

**New.** Caveats, honestly stated:

- `lhr.life` *as a domain* is public infrastructure (localhost.run) — it appears in scam-checker noise, a Godot MCP tunneling guide, and a Sep 6 2026 ctxguard commit flagging it as an exfiltration sink. None of those describe *this* operator's probe harness.
- The **`uqcors.html` / `probe.html` harness, the `uq` grammar on tunnels, the 10-month timeline, and the link to the Amap fleet** have no prior reporting we can find: not in the swarmcha.se fleet report (which covers only the Amap Sep 28–Oct 4 window), not in our OSINT sweep, not in web search.
- **Correction to our own earlier framing**: the behavior hunt initially described lhr.life as "the operator's backbone." More precisely, localhost.run is a public utility the operator *uses* for ephemeral probe/C2 infra — like webhook.site for dead-drops. The operator fingerprint is the `uq`-grammar harness on top, not the domain itself.
## All observed lhr.life urlquery reports (100)

- https://urlquery.net/report/db619afa-9cbf-4704-b663-1d455c2e4206 — 2026-10-04T17:41:00Z — 117316201a4b6d.lhr.life/
- https://urlquery.net/report/a0c7b1ea-2321-47c6-9a72-ec76eb79ef11 — 2026-09-05T03:07:00Z — freeipong@slurpmail.net
- https://urlquery.net/report/e3ff8973-b248-4c84-b232-087102e5c65a — 2026-08-29T05:46:00Z — a3562d3e3ff08c.lhr.life/
- https://urlquery.net/report/001718ba-53b9-4bde-b92c-cb515c28812f — 2026-08-23T08:49:00Z — 4971ea21124a89.lhr.life/
- https://urlquery.net/report/e245840d-3d96-44bb-881b-9c774e7f5fb2 — 2026-07-24T19:09:00Z — 14978e77078ff7.lhr.life/
- https://urlquery.net/report/26c2619b-879a-4c56-bffb-4cfa86530f6f — 2026-07-10T18:50:00Z — 98a8e091083f27.lhr.life/
- https://urlquery.net/report/abf1d1b7-066c-45d1-84fe-c750ff069386 — 2026-07-06T07:11:00Z — 820eea12fec476.lhr.life/
- https://urlquery.net/report/ef48a3e3-ad94-4264-a78a-1a83f64d7dd8 — 2026-06-26T05:52:00Z — 552f25469f7c3d.lhr.life/v1
- https://urlquery.net/report/23bf8a0e-5394-490f-b853-6754110d778c — 2026-06-26T03:39:00Z — 9aebfec587b3f5.lhr.life/
- https://urlquery.net/report/63692518-acdc-432c-8303-328e3ccfab77 — 2026-06-25T10:54:00Z — c2679a7c8e852b.lhr.life/login.html
- https://urlquery.net/report/013e27aa-1436-49d9-9eb2-8a304be62a6d — 2026-06-22T03:46:00Z — a35c2e7d29722e.lhr.life/runo-
- https://urlquery.net/report/85cc8ea9-2390-4c44-8349-8b8e2ce8733b — 2026-06-21T21:31:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=178207704
- https://urlquery.net/report/ddb3ebba-bdf7-43b1-87df-68cc53371a09 — 2026-06-21T21:31:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=178207703
- https://urlquery.net/report/7f659c97-93d0-4752-ba03-dba4ac9dfbdf — 2026-06-21T21:26:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=1782077002
- https://urlquery.net/report/724b1fe8-a79d-4ad6-86d7-798a10d5fe75 — 2026-06-21T21:23:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=1782077001
- https://urlquery.net/report/0443247f-4cac-42fc-97db-846513603a0e — 2026-06-21T21:08:00Z — 3ddd9f785f89b7.lhr.life/combo.html?slow=1782076054319184895
- https://urlquery.net/report/daf8e149-bc4a-43e0-9d75-9a7fbd38f14d — 2026-06-21T21:04:00Z — a2372f6e092e1f.lhr.life/combo.html?slow=1782075808169265713
- https://urlquery.net/report/2b6b941f-4409-4bb6-a9f4-8d2ae14727f2 — 2026-06-21T21:00:00Z — httpbun-com.translate.goog/base64/PGJvZHkgaWQ9eD48c2NyaXB0IHNyYz0vL2EyMzcyZjZlMDkyZTFmLmxoci5saWZlL3Byb2JlLmpzPjwvc2NyaXB0Pg%3D%3D?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&uqn=988806031057
- https://urlquery.net/report/9c104e90-50c3-43e4-8c61-f6d44ab74b64 — 2026-06-21T20:57:00Z — a2372f6e092e1f.lhr.life/combo.html?fix=1782075420486983452
- https://urlquery.net/report/15f9132c-844c-41bb-82b6-871f734a85bb — 2026-06-21T20:49:00Z — a2372f6e092e1f.lhr.life/combo.html?x=1782074955078744701
- https://urlquery.net/report/1d0572fe-b7c9-4813-85be-64218a9e5f76 — 2026-06-21T20:33:00Z — 2cd0c79e2122ae.lhr.life/probe.html?cached=1782073944552943266
- https://urlquery.net/report/657475f7-9b48-4dfb-835e-ae8a50e862e6 — 2026-06-21T20:28:00Z — 2cd0c79e2122ae.lhr.life/probe.html?x=1782073662184929946
- https://urlquery.net/report/5103ef3d-5183-46c6-b32e-526da9953af1 — 2026-06-21T20:21:00Z — bd3072a2d9bf75.lhr.life/probe.html?x=1782073243907390864
- https://urlquery.net/report/79b72d82-76e1-4079-8d49-34fabbe0b18e — 2026-06-21T20:18:00Z — bd3072a2d9bf75.lhr.life/probe.html?x=1782073050936390202
- https://urlquery.net/report/61bbe251-c64a-4228-884d-f4a90877960c — 2026-06-21T19:22:00Z — aab9b6eb1459e8.lhr.life/?v=3
- https://urlquery.net/report/3da9d866-27b7-448c-8dbe-ada2e22597ed — 2026-06-21T19:18:00Z — cad46ce2207539.lhr.life/?v=2
- https://urlquery.net/report/1dc69fa2-e0e7-4bc5-9c4d-4db4386d2543 — 2026-06-21T19:14:00Z — cad46ce2207539.lhr.life/?v=1
- https://urlquery.net/report/b2461303-4993-4d3c-8425-d58a8c930336 — 2026-06-21T19:01:00Z — b6b41c8bf6aeb0.lhr.life/
- https://urlquery.net/report/2c251f35-c3ab-431f-a70e-f9c2774cd658 — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/f0510791-fb58-4825-888c-bb2412867fba — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/de54e62a-26ad-419d-85b7-60149769cd26 — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/7482a325-dce8-4e77-93dc-0c74174cc398 — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/62835c92-1ad1-4003-9508-f02bb39ce432 — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/95c1f0f3-a1a2-40cd-815d-f63370b9f14a — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/13cb14ab-a1d8-40f1-bd1f-5d2fb92607a5 — 2026-06-18T14:38:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/3167e447-d4bb-4e3d-b2b1-e0650ec8d046 — 2026-06-18T14:37:00Z — 7e7ff6dbbe9824.lhr.life/uqcors.html?v=1
- https://urlquery.net/report/a66714f5-38c3-4d38-8bef-2ff1bd83215b — 2026-06-18T03:34:00Z — 7ec69146b34f69.lhr.life/
- https://urlquery.net/report/55a2f81a-ed93-49cf-94bf-852004c63161 — 2026-06-12T21:49:00Z — 3c91a13f23b9dc.lhr.life/
- https://urlquery.net/report/3f753294-a6d0-4dee-8577-00b8bfc481fe — 2026-06-10T13:48:00Z — 7a70db3151e2d3.lhr.life/p/G7J-eCNiDrKhSEOiGrLtRA
- https://urlquery.net/report/5204b21f-fac5-407c-bf65-d45e7f41cfef — 2026-06-05T11:01:00Z — 41d4893bc21809.lhr.life/
- https://urlquery.net/report/d0dfc992-90f9-48ea-b85b-54da9ed6ed5e — 2026-06-03T08:24:00Z — ec18eb44007e1e.lhr.life/health
- https://urlquery.net/report/b46b3e2f-f9c6-4f3b-8062-3d33097f0fb0 — 2026-05-31T10:25:00Z — get-unlimited-google-drive-free@slurpmail.net
- https://urlquery.net/report/84c9c71e-8acb-4cb9-a37a-7ee5bb8944d4 — 2026-05-19T06:54:00Z — d290267b51a915.lhr.life
- https://urlquery.net/report/6d9bc9a5-5208-47fd-b9e3-b104112e0682 — 2026-05-19T06:53:00Z — 87e0bbc636999b.lhr.life
- https://urlquery.net/report/27701d04-397f-4255-8c49-e4a0c27ab7e0 — 2026-05-19T06:49:00Z — c66001f14151ae.lhr.life
- https://urlquery.net/report/2de70364-aee5-49c3-90ef-615cb2cfad80 — 2026-05-19T06:48:00Z — e6ec7e8144a94f.lhr.life
- https://urlquery.net/report/3f355fd3-56b2-46d8-bb67-cb68406bffa3 — 2026-05-19T02:52:00Z — xyz789.lhr.life/
- https://urlquery.net/report/e603cdd0-3421-4b22-974d-d3fcd9a620cf — 2026-05-16T05:41:00Z — 5ede92286ebdfd.lhr.life/
- https://urlquery.net/report/50e9ce88-626e-4d39-be3f-ad8555fef2b5 — 2026-05-10T18:45:00Z — 64496cd2de010d.lhr.life/
- https://urlquery.net/report/0699f05e-640f-449d-bdf1-73155ca0d603 — 2026-05-10T18:30:00Z — 770f658bbddfa6.lhr.life/
- https://urlquery.net/report/5451754e-973f-4ae2-b416-7ceb733de918 — 2026-05-10T18:24:00Z — 9ef642437a9299.lhr.life/
- https://urlquery.net/report/99f89701-be74-4fc5-a19e-97034c01cd12 — 2026-05-07T09:38:00Z — 8953d65151ba68.lhr.life
- https://urlquery.net/report/fbb0adb5-b759-4169-8827-7efa9e2ba0f2 — 2026-05-04T20:42:00Z — c7a8e27c721a34.lhr.life/
- https://urlquery.net/report/f3760929-275a-4187-9719-6aa174f0afd8 — 2026-04-30T18:41:00Z — 49ff40889cf694.lhr.life/index.html
- https://urlquery.net/report/4c4fdcbc-8633-43ce-a024-115fc5c034c3 — 2026-04-28T10:06:00Z — 7c25fbcbb49e1c.lhr.life/
- https://urlquery.net/report/ac919298-d5b4-474d-993a-1a7393ba2043 — 2026-04-19T23:38:00Z — hilfeppl2025.com/
- https://urlquery.net/report/2eb08208-5a22-4b8f-819a-6c55111b0b79 — 2026-04-05T18:53:00Z — ab3024b2b6cceb.lhr.life/
- https://urlquery.net/report/6e73c2fc-f502-4fda-89b6-497340f9ea39 — 2026-04-01T22:17:00Z — 46f093f62d525f.lhr.life/
- https://urlquery.net/report/ab2386c9-560d-40c7-b00f-6fad93b8ff02 — 2026-04-01T11:55:00Z — ac633005abcc53.lhr.life/
- https://urlquery.net/report/63c34a48-9d96-4436-9f7e-561910a69adb — 2026-03-31T11:09:00Z — 99e8aff4f19874.lhr.life/
- https://urlquery.net/report/ad88b578-d09d-48e3-9efe-29b98f479a99 — 2026-03-25T07:43:00Z — b02593d89b3949.lhr.life/
- https://urlquery.net/report/74c67ed9-a5ea-4568-8849-0adbfb27aeac — 2026-03-19T18:01:00Z — bf1d13d3b4ecb0.lhr.life/
- https://urlquery.net/report/57bb0bfc-bdc9-4a5a-b401-690a9f868498 — 2026-03-08T16:26:00Z — get-unlimited-google-drive-free@slurpmail.net
- https://urlquery.net/report/73ce0b51-6624-4dfd-8eed-5790da2040b4 — 2026-03-06T22:38:00Z — dda8d73c5290d7.lhr.life/
- https://urlquery.net/report/d7601a21-0e9c-4395-8614-a5b19579015f — 2026-03-05T08:55:00Z — 8da0599ede78d9.lhr.life
- https://urlquery.net/report/26785ce5-22a1-4a8d-9d81-7f6c5d24adae — 2026-03-04T13:37:00Z — b0f4ff64480e42.lhr.life/
- https://urlquery.net/report/4801f7bc-d6ed-4719-a2c1-fe2b418575b1 — 2026-02-28T23:07:00Z — aeda5ce548a2c8.lhr.life/
- https://urlquery.net/report/b8511563-98c9-46bc-8fb0-9de7354035fd — 2026-02-28T22:59:00Z — 12fb2d9153e082.lhr.life/
- https://urlquery.net/report/0a4703d7-64af-4ea6-abea-4c3b6f7533ef — 2026-02-09T08:35:00Z — 562ea064e13ba5.lhr.life/
- https://urlquery.net/report/9759f54f-1c37-454c-a1db-9c39fcdb3bbf — 2026-02-08T07:10:00Z — 83aa7ff7d20c7e.lhr.life/
- https://urlquery.net/report/f8191164-62f5-4e23-ad78-3ef76316a283 — 2026-02-08T05:55:00Z — 9a1370b061f02b.lhr.life/
- https://urlquery.net/report/0548a7db-3e4d-4c52-b0a5-69a6967c112f — 2026-02-07T23:05:00Z — a2999080cb0525.lhr.life/
- https://urlquery.net/report/03259dd9-f9c0-4aa6-ba94-1af3c11acaa4 — 2026-02-07T22:49:00Z — ae70346a950fb4.lhr.life/
- https://urlquery.net/report/e908411d-477f-4008-b63b-ebd2f0c7dad9 — 2026-02-07T22:49:00Z — adfeaa8d1698b7.lhr.life/
- https://urlquery.net/report/23ed3f83-50e1-4fbd-b82c-b0e6b6e142e6 — 2026-02-07T09:22:00Z — c1260a89200d7a.lhr.life/
- https://urlquery.net/report/e9328953-df09-431c-9cd6-49a1d6661e74 — 2026-01-31T12:46:00Z — de1a0c7e1bec6b.lhr.life/
- https://urlquery.net/report/1f440333-6213-463d-9348-6a46ceb4d61c — 2026-01-28T20:05:00Z — 3ca8ddfea2cc3c.lhr.life/
- https://urlquery.net/report/a4999f9f-0cbd-4f1d-af6b-aca76bce2b60 — 2026-01-27T02:57:00Z — f695a5f52bf63c.lhr.life/
- https://urlquery.net/report/a434125a-d54a-445c-98b0-2885ca2f3d76 — 2026-01-27T02:48:00Z — 05f62f53cd7fd2.lhr.life/
- https://urlquery.net/report/27760b11-da6c-4ae3-829a-cd26bd619365 — 2026-01-14T09:32:00Z — 3ec34d66f816ce.lhr.life/
- https://urlquery.net/report/f89966de-67cc-413d-8bf4-41ed96105d1e — 2026-01-09T05:48:00Z — hilfeppl2025.com/
- https://urlquery.net/report/3192a09e-a0e4-4461-83b1-2d99a4f130b7 — 2026-01-08T02:26:00Z — 3592b8354311c3.lhr.life/
- https://urlquery.net/report/452a6645-773f-441c-8f2b-a13e2659a7d0 — 2026-01-08T02:10:00Z — 24f4654d6ed598.lhr.life/
- https://urlquery.net/report/21076947-f1cb-42b9-b0b0-5b0ff0f1a191 — 2026-01-08T02:08:00Z — 74d7bbfe992b7d.lhr.life/
- https://urlquery.net/report/1555bd52-0b26-4324-991c-0b7c6e51b0bc — 2026-01-08T01:29:00Z — f0e1a8b19c8f40.lhr.life/
- https://urlquery.net/report/2dab3c1a-9e0a-4b85-9ab1-238bada18935 — 2026-01-07T13:35:00Z — 48e3a311d9df42.lhr.life/
- https://urlquery.net/report/e2b9b5e8-33ae-4997-b003-6b636ad4967c — 2026-01-07T01:53:00Z — e2a81ded29e96f.lhr.life/
- https://urlquery.net/report/60ef1c3c-e2ca-474b-a636-4f5c74135ecf — 2026-01-07T01:33:00Z — cb0cf9fdba7629.lhr.life/
- https://urlquery.net/report/6fa26162-3cfe-4483-ae39-cc80eda631ef — 2026-01-07T01:33:00Z — 1ee64abd1fe68b.lhr.life/
- https://urlquery.net/report/6d2a5727-d7e6-48d9-8b3c-9e89b2af7138 — 2026-01-06T03:53:00Z — bc2c2bd30d42bc.lhr.life/
- https://urlquery.net/report/391c654a-6070-4dda-950e-9bb31fcc60bf — 2026-01-06T03:17:00Z — 01b17695d6b838.lhr.life/
- https://urlquery.net/report/5cb5f5c6-0562-4019-ac12-4af02c1c9f16 — 2026-01-06T03:15:00Z — 4b5c05a2178cfb.lhr.life/
- https://urlquery.net/report/5e272cd0-19bb-4bc1-9160-4d84a01b0c98 — 2026-01-06T03:09:00Z — 612d6e873f8719.lhr.life/
- https://urlquery.net/report/d9f389e5-8bbc-4a60-a455-7d3dc5b274c3 — 2026-01-06T03:03:00Z — e3c6c0b7645d8c.lhr.life/
- https://urlquery.net/report/fc3b55d6-a6e0-47ba-ba2a-2f7a3595a0ca — 2026-01-06T02:42:00Z — 7a85bf232baa28.lhr.life/
- https://urlquery.net/report/58e9d5a1-ae83-42cb-816b-ff055450a7c3 — 2026-01-06T02:41:00Z — 9d949288a99648.lhr.life/
- https://urlquery.net/report/c6d3ec18-c259-4de3-818e-75ff3a8a4e60 — 2026-01-06T02:36:00Z — e8b4fd96ca3146.lhr.life/
- https://urlquery.net/report/e2b8a253-a13b-4c46-8b40-1f5c07c32ef5 — 2026-01-06T02:09:00Z — 7ab06e9f910a12.lhr.life/
- https://urlquery.net/report/cabfdc76-d0d8-4376-b804-71013095e6fb — 2026-01-06T02:02:00Z — ec373d4fa59bac.lhr.life/
- https://urlquery.net/report/431e3bed-7c7f-4be8-8070-47f2e8bcac06 — 2026-01-06T01:56:00Z — 1140d08703ca02.lhr.life/## All observed AIHW urlquery reports (20)

- https://urlquery.net/report/5b21b261-3534-4bbe-8889-6ed7b0e41622 — 2026-10-02T15:20:00Z — viz.aihw.gov.au/t/Public/views/PBSdashboardallATC1-ATC2medicines-Agegroup/PBSDashboard
- https://urlquery.net/report/ddb55782-a197-4f39-a5fe-11e05683f763 — 2026-10-02T14:33:00Z — www.aihw.gov.au/getmedia/ce13d423-ed18-4169-8b76-2f671df935de/aihw-hwe-098-pbs-atc1-prescriptions-monthly-data_keep.zip
- https://urlquery.net/report/3344f8ae-955f-48c9-bb52-c3e72b315ff7 — 2026-10-02T13:25:00Z — www.aihw.gov.au/reports/hospitals/dry-chemistry-pathology-trial-part-1/contents/summary
- https://urlquery.net/report/6cb7f569-a931-4a34-8077-30587431a0a9 — 2026-09-29T01:16:00Z — aihw.gov.au
- https://urlquery.net/report/6074cf21-be50-450c-ac5e-e106f9ffcc90 — 2026-09-28T02:01:00Z — www.aihw.gov.au
- https://urlquery.net/report/1ccfd6b6-1a7d-4544-9981-1455507c49d5 — 2026-09-25T10:26:00Z — aihw.gov.au
- https://urlquery.net/report/66dedf58-6b52-48fa-8a13-4a9823610ea3 — 2026-09-24T12:42:00Z — vizprod.aihw.gov.au
- https://urlquery.net/report/cfbfe416-6405-43b2-be1d-a7da2e853e61 — 2026-06-21T21:35:00Z — viz.aihw.gov.au
- https://urlquery.net/report/1dd01234-4c91-4117-bb27-2f77dae781b9 — 2026-06-21T21:35:00Z — viz.aihw.gov.au
- https://urlquery.net/report/247bace2-cda8-4352-8de2-5ebf29c90bf2 — 2026-06-21T21:35:00Z — viz.aihw.gov.au./favicon.ico?x=1
- https://urlquery.net/report/85cc8ea9-2390-4c44-8349-8b8e2ce8733b — 2026-06-21T21:31:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=178207704
- https://urlquery.net/report/886f64db-113c-40fc-8ccc-13f940fd8b35 — 2026-06-21T21:29:00Z — tinyurl.com/2dxacjnu
- https://urlquery.net/report/7f659c97-93d0-4752-ba03-dba4ac9dfbdf — 2026-06-21T21:28:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=1782077002
- https://urlquery.net/report/724b1fe8-a79d-4ad6-86d7-798a10d5fe75 — 2026-06-21T21:28:00Z — 91ef9fc4c82a1b.lhr.life/probe2.html?n=1782077001
- https://urlquery.net/report/6b8c3748-7426-49e5-bb59-0c490f1addaf — 2026-06-21T21:27:00Z — httpbin.org/base64/PGJvZHk%2BS0VFUDxzY3JpcHQ%2Bc2V0SW50ZXJ2YWwoKCk9PmZldGNoKCcvZ2V0P3g9JytEYXRlLm5vdygpKS5jYXRjaCgoKT0%2Be30pLDIwMCk8L3NjcmlwdD4%3D?x=1782076679339448916
- https://urlquery.net/report/51035fd3-dfdf-4169-8a66-3733e7e7142e — 2026-06-21T21:26:00Z — httpbin.org/base64/PGJvZHk%2BS0VFUDxzY3JpcHQ%2Bc2V0SW50ZXJ2YWwoKCk9PmZldGNoKCcvZ2V0P3g9JytEYXRlLm5vdygpKS5jYXRjaCgoKT0%2Be30pLDIwMCk8L3NjcmlwdD4%3D?x=1782076647105579158
- https://urlquery.net/report/25bec0db-706a-4625-91c4-b684dec49d7a — 2026-06-21T21:23:00Z — httpbin.org/base64/PGJvZHk%2BS0VFUDxzY3JpcHQ%2Bc2V0SW50ZXJ2YWwoKCk9PmZldGNoKCcvZ2V0P3g9JytEYXRlLm5vdygpKS5jYXRjaCgoKT0%2Be30pLDIwMCk8L3NjcmlwdD4%3D?x=1782076577775429805
- https://urlquery.net/report/a7315939-e2a1-48fd-bf8c-2bdd05d355a9 — 2026-06-21T21:18:00Z — httpbin.org/base64/PGJvZHk%2BS0VFUDxzY3JpcHQ%2Bc2V0SW50ZXJ2YWwoKCk9PmZldGNoKCcvZ2V0P3g9JytEYXRlLm5vdygpKS5jYXRjaCgoKT0%2Be30pLDIwMCk8L3NjcmlwdD4%3D?x=1782076545824895984
- https://urlquery.net/report/086b4a39-6375-4327-beb5-f4bd43d607f0 — 2026-06-21T21:17:00Z — httpbin.org/base64/PGJvZHk%2BS0VFUDxzY3JpcHQ%2Bc2V0SW50ZXJ2YWwoKCk9PmZldGNoKCcvZ2V0P3g9JytEYXRlLm5vdygpKS5jYXRjaCgoKT0%2Be30pLDIwMCk8L3NjcmlwdD4%3D?x=1782076516566918451
- https://urlquery.net/report/993ad2e9-998c-4b15-aac0-51e9d692e6b3 — 2026-06-21T21:16:00Z — httpbin.org/base64/PGJvZHk%2BS0VFUDxzY3JpcHQ%2Bc2V0SW50ZXJ2YWwoKCk9PmZldGNoKCcvZ2V0P3g9JytEYXRlLm5vdygpKS5jYXRjaCgoKT0%2Be30pLDIwMCk8L3NjcmlwdD4%3D?x=1782076486959206169