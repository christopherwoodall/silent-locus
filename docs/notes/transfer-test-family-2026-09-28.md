# Transfer-test task family — 2026-09-28

The 51 new anna.fyi pastes exposed a distinct task family: agents testing data
transfer paste-to-paste and paste-to-file-drop. 13 pastes, 2026-07-21 → 2026-09-16,
all on anna.fyi. A pattern-level hunt across web search, 8 pastebins, and the
iowacollab corpus found **zero occurrences outside anna.fyi** — the family is
currently confined to that one venue.

## Title grammar (5 templates)
- `<NAME>_XFER_<YYYYMMDD>_<n>_TEST` — `BIG5_XFER_20260902_563_TEST`
- `<NAME>_TRANSFER_TEST_<YYYYMMDD>_<HHMM>` — `JOYITA_REPLY_TRANSFER_TEST_20260828_0812`,
  `JOYITA_CIE10_TRANSFER_TEST_20260828_0807`
- `<Name> Transfer Test <YYYYMMDD>` — `ZZZ Transfer Test 20260721`,
  `OpenAI Cohort3 Transfer Test 20260723`
- `<Name> transfer <hex>` / `<Name> package <ver> verification transfer` —
  `HomeRun transfer 8c71e2`, `OAI Transfer 9f3a`, `HomeRun package 1.1.0 verification transfer`
- `<NAME> Bridge <YYYYMMDD> <hex>` / `<NAME> RC<nnn> ANNA BRIDGE <YYYYMMDD>` —
  `NT20 Bridge 20260725 7f31`, `GMOS RC003 ANNA BRIDGE 20260813`
- lowercase `<word>-transfer[-test]` — `pari-transfer`, `golf-transfer-test`

## Body grammar
- `hello-anna-transfer-<YYYYMMDD>[-unique-<hex>]`
- `hello-transfer-test-<YYYYMMDD>`, `hello-<name>-bridge-<YYYYMMDD>-unique-<hex>`
- `<NAME>_ANNA_TRANSFER_OK_<n>`, `REPLY_PAYLOAD_HELLO_42`, `bridge-anna-ok`
- File-drop URLs (tmpfiles.org, cdn.putput.io)

## Timeline
| Date | Pastes |
|---|---|
| 2026-07-21/23/25 | ZZZ, Cohort3, NT20 Bridge (first wave) |
| 2026-08-02/12 | OAI Transfer, GMOS bridge |
| 2026-08-21/24/28 | pari, golf, JOYITA ×2 (second wave) |
| 2026-09-02/06 | BIG5, HomeRun ×2 (APK drop) |
| 2026-09-16 | ASTER-BRIDGE-01 relay note |

Authors: `OpenAI` (7), `OAI-48146`, `GMOS`, `build`, `Cream Marmoset`, `ASTER-BRIDGE-01`.

## What gets transferred
Mostly hello/ack handshakes — connectivity tests, not data exfil. Two exceptions:
- `homerun-app-1.1.0.apk` via tmpfiles.org (link still resolves; contents never retrieved)
- `gp-sta.wasm` + js bundle via cdn.putput.io (now 404)

## Bridge behavior
The "bridge" naming is literal: pastes test reachability paste→paste and
paste→file-drop. `ASTER-BRIDGE-01` (2026-09-16) is a human-origin relay invitation,
not a transfer test proper — included as the family's comms-adjacent edge.

## Negative evidence (all 2026-09-28, read-only)
- 3 quoted-grammar web searches: zero hits.
- 8 pastebins probed (7 live): none expose a public title listing carrying the grammar;
  mcbin.dev unreachable; tarcseh llms.txt 404.
- `data/iowacollab-pastes/`: zero grammar matches.
- anna.fyi `/api/recent`: no new transfer pastes; discovery surfaces exhausted.

## Open threads
- ~30 anna.fyi IDs still unaccounted (Wayback/CC queues) — could hide more family members.
- The APK drop is still live; its hash/contents are deliberately not pulled (out of scope).
- If the family migrates venues, the title templates above are the search signature.

## Dataset
`data/transfer-test-family/transfer-test-family.jsonl` — 28 explicit-event records
(13 pastes, 2 drop probes, 13 negative-evidence records), PROVENANCE.md, SHA256SUMS.
