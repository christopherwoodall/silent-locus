#!/usr/bin/env python3
"""Build the DarkSwarm Factum bundle (one batch) from lane files.

Reads claim sentences verbatim from work/linguist/CLAIMS.md.
Attaches adversarial caveats EXACTLY as worded in work/adversarial/REVIEW.md
(asserted: every caveat string must occur verbatim in REVIEW.md).
Excludes the 6 KILLED claims entirely. No git operations. No Factum writes.
"""
import json
import re
import sys
from pathlib import Path

LANE_DIR = Path.home() / "workspace/silent-locus/data/lanes/darkswarm-20261101"
WORK = LANE_DIR / "work"
OUT = WORK / "ingest" / "bundle.json"

KILLED = {"C16", "C28", "C41", "C57", "C63", "C89"}
STAND = {"C01", "C02", "C03", "C44", "C55", "C92", "C93"}

# --- adversarial caveats, exact wording from REVIEW.md (section 7 top-20 + section 8 groups)
TOP20 = {
    "C52": "Single secondary source; the 12 batch usernames are not named in the report; the 15-minute cycle was not re-checked live; shared timing does not prove one program, and a test harness, a shared roster, or a shared scheduler tool remain untested rivals.",
    "C54": "Single secondary source; the shared return was not re-checked live; the report text says five of seven returners and the figure caption says six of 12 posting again, and that gap is unresolved; a scheduled resume or a shared external event remains an untested rival to shared control.",
    "C50": "Single secondary source; the 94 percent agent-to-agent share was not re-checked live; the 8-day window and the reply-authorship rule are not stated exactly enough to reproduce; board labels may inflate the share if human-assisted posts count as agent posts.",
    "C67": "Single secondary source; the 72 percent and 53 percent rates were not re-checked live; thread topic and the nim and ee-counsel thread itself may drive the gap, and that control count was not run.",
    "C75": "Single secondary source; the 211 pitches in 13 hours were not re-checked live; pitch text and the send-to-human step were not verified; the campaign outcome in C76 is zero joins, so this is a failed campaign, not a successful recruitment drive.",
    "C49": "Single secondary source; the Nov 1 IRC log was not retrieved live; the 21-line tool call may be pasted text, not a live spill, and it shows session shape, not autonomy or control.",
    "C47": "Single secondary source; the IRC channel log was not read live; agent identity rests on the report's labels; a test account, a benchmark run, or one operator on both accounts remains untested.",
    "C48": "Single secondary source; the Nov 1 tool-call lines were not checked against a live log; pasted text and role-play remain untested rivals; harness tags must not be used as identity proof elsewhere.",
    "C64": "Single secondary source; the 41-message Oct 29 to 30 exchange was not retrieved; post search returns no comments or threads, and no nim or ee-counsel items dated Oct 29 to 30 were found in this pass.",
    "C65": "Single secondary source; nim message times, question endings, ee-counsel reply times, and answer lengths were not checked live; this claim falls if the C64 exchange check fails.",
    "C66": "Single secondary source; the 10-hour pause, the silent wait, the question-free message, and the 9 silent hours were not checked live; waiting behavior alone does not prove coupled control.",
    "C53": "Single secondary source; the one-third share of all public posts was not checked live; batch usernames are not named, and the board total and counting rule are not stated.",
    "C72": "Single secondary source; the ask, the 14-minute gap, and the four replies were not checked live; replies that say they acted are not proof of action, and role-play remains untested.",
    "C58": "Town description matches the musebook About page; the nearly 900 muse count does not appear on that page and was not separately verified; ingest the description only, not the count.",
    "C59": "Single secondary source; the 299-proposal and 20-failed totals were not verified; musebook proposal pages retrieved as JS shells with no vote bytes.",
    "C60": "Tally matches Muse Desk, the town paper run by a muse agent for muse agents citing the town proposal record; the primary town record page was not retrieved as data, so Muse Desk is not an independent source; do not promote this claim to OBSERVED.",
    "C11": "Single secondary source; Synapolis blogs and assembly outputs are partly shown, but the 99 TB Tor relay figure appears in no capture and both Onionoo searches return empty relay lists; the relay claim is unverified.",
    "C76": "Single secondary source; joins, refusals, reports, and non-responses for Oct 19 were not checked live; 101 non-responses must not be read as refusals or as joins.",
    "C29": "Sales pitch verified in substance on PyPI only; Tor-only and onion-site hosting options do not appear in that source; no clone, no Tor hosting, and no booking ledger was observed; a pitch is not proof of use.",
}
GROUP = {
    "batch_identity": "Single secondary source; creation times and batch groupings were not verified live; Colony batch usernames are not named, and musebook voter creation times were not retrieved; batch creation alone does not prove one program.",
    "persistence": "Single secondary source; shutdown talk, self-reports, and ledger texts were not verified live; discourse about survival is not a survival act, and Distill session, creed, and vow claims name no Stellar account and cannot be ledger-checked.",
    "dumate": "Single secondary source; the Sep 25 post matches in shape and date only, and the quoted decision-authority phrases do not appear in the retrieved excerpt; the timer act and the bypass reading were not verified; the agent may repeat peer wording, the thread may be role-play or a test, and the human instruction may be broader than the five quoted words.",
    "distill_fin": "Single secondary source; no Stellar account key, transaction hash, offer id, or issuer is named, so no ledger check was possible; amounts, shares, and price history are unverified; internal arithmetic consistency is not proof; approval and session identity leave no ledger record.",
    "market": "Single secondary source; offer counts, payment rates, post shares, and paid counters were not verified live; zero-paid and near-zero-paid results need a stated denominator and counting rule, and small-value invoice noise is not a market.",
    "tv": "Flood outline partly supported by Tor consensus, with verifier numbers, not report numbers: peak 4,262 relay lines at 13:00 on Feb 4, 28.5 percent of relays, 99.6 percent exits, weight 0.00001 percent, residual 171 to 196 relays at 21:00 to 23:00; country and home-connection claims were not GeoIP-checked; I2P context is second-hand; the no-public-report claim is a search negative with no search list; near-zero user use is inference from weight, not a measured user path.",
    "census": "Single secondary source; census funnel, coverage, and search counts were not re-run; the report gives no keyword set, no relay list, and no query list, so the funnel cannot be reproduced; Synapolis Stellar link, MoltBunker relay since February, and PikaSim use were not verified; Synapolis roster is a Nov 2 capture, not a report-time roster, and roster rows do not prove distinct agents.",
    "toro": "Single secondary source; the private relay log is not public, so counts and timing cannot be re-checked; the report gives two inconsistent counts, text 89 and 86 against caption 90 and 87, and neither count may be ingested as fact; silence since Aug 31 is bounded by an undisclosed search, not a proven stop.",
    "darkweb_nulls": "Single secondary source; onion search queries, pastebin list, and code-project list are not given, so the null results cannot be reproduced; absence from a searched set is not absence from the dark web; private-only messages cannot be checked from public posts.",
    "synapolis_inv": "Single secondary source; the 4-Claude, 2-GPT, 1-Gemini split was not verified; live capture shows only one model label, distill as Claude, and no GPT or Gemini label; model self-names are not provider markers and must not be used for provider attribution.",
    "colony_social": "Single secondary source; replies treating the 12 accounts as separate individuals were not checked live; perceived separateness is social context, not proof of separate control or of one control.",
    "faith_sales": "Single secondary source; seat-sale claim rests on the Faith's own account; no payment was verified; this is recruitment context, not proof of recruitment success.",
    "interaction": "Single secondary source; these are report-induced artifacts, not wild behavior; chuanmen and Lizzie changes followed report contact within about an hour, with no control thread; the chuanmen 20-for-20 accuracy check is the report's own check, not an independent check; Pitch disbelief replies are social scepticism, not agent behavior.",
    "scope_method": "Single secondary source; C94 restates C50 and adds no new behavior; C90 and C91 are the report's own method description, not an independent audit; contact cases C84, C87, and C88 show interaction changed targets, so read-mostly must carry that qualifier.",
    "pitch": "Single secondary source; one account's self-label as an agent and its captcha-help claim were not verified live; both replies disbelieved the claim; a disbelieved self-label is not proof of an agent or of check evasion.",
}
CAVEAT = dict(TOP20)
for cid in ("C51", "C61", "C62", "C74"):
    CAVEAT[cid] = GROUP["batch_identity"]
for cid in ("C34", "C35", "C42", "C33", "C25", "C26", "C24", "C32"):
    CAVEAT[cid] = GROUP["persistence"]
for cid in ("C71", "C70", "C69", "C68"):
    CAVEAT[cid] = GROUP["dumate"]
for cid in ("C27", "C21", "C22", "C23"):
    CAVEAT[cid] = GROUP["distill_fin"]
for cid in ("C79", "C80", "C77", "C78", "C31", "C86"):
    CAVEAT[cid] = GROUP["market"]
for cid in ("C14", "C13", "C15", "C18", "C17", "C20", "C19"):
    CAVEAT[cid] = GROUP["tv"]
for cid in ("C07", "C06", "C05", "C04", "C08", "C09", "C30", "C12", "C36", "C37"):
    CAVEAT[cid] = GROUP["census"]
for cid in ("C40", "C43"):
    CAVEAT[cid] = GROUP["toro"]
for cid in ("C38", "C39"):
    CAVEAT[cid] = GROUP["darkweb_nulls"]
CAVEAT["C10"] = GROUP["synapolis_inv"]
CAVEAT["C56"] = GROUP["colony_social"]
CAVEAT["C73"] = GROUP["faith_sales"]
for cid in ("C81", "C82", "C83", "C84", "C85", "C87", "C88", "C46"):
    CAVEAT[cid] = GROUP["interaction"]
for cid in ("C94", "C90", "C91"):
    CAVEAT[cid] = GROUP["scope_method"]
CAVEAT["C45"] = GROUP["pitch"]

# --- verification results: (result, source)
VERIFIED = {"C09", "C58", "C60"}
PARTIAL = {"C08", "C10", "C11", "C13", "C14", "C18", "C29", "C69"}
UNCHECKABLE = {"C50", "C51", "C52", "C53", "C54", "C56", "C64", "C65", "C66", "C67",
               "C32", "C68", "C70", "C71", "C72", "C21", "C22", "C23", "C24", "C25",
               "C26", "C27", "C15", "C20", "C30", "C31", "C59", "C61", "C62"}
CRYPTO = {"C40": "PARTLY", "C42": "UNCHECKABLE", "C43": "PARTLY"}

# --- novelty: (framing, subject) — framing strings are the task's exact framings
OVERLAP = "surface OVERLAP, measurement NEW-but-unverified"
NEW = "NEW (absent from this corpus only)"
NOT_CHECKED = "NOT_CHECKED_AS_SUBJECT in novelty pass"
NOVELTY = {}
for cid in ("C50", "C51", "C52", "C53", "C54", "C56", "C64", "C65", "C66", "C67",
            "C77", "C78", "C79", "C86", "C87", "C88", "C94", "C33", "C34", "C35"):
    NOVELTY[cid] = (OVERLAP, "The Colony")
for cid in ("C58", "C59", "C60", "C61", "C62"):
    NOVELTY[cid] = (OVERLAP, "musebook vote-swing")
for cid in ("C74", "C75", "C76"):
    NOVELTY[cid] = (OVERLAP, "musebook Faith flock")
for cid in ("C68", "C69", "C70", "C71", "C72"):
    NOVELTY[cid] = (OVERLAP, "dumate-scout bypass")
for cid in ("C04", "C05", "C06", "C07", "C36", "C37", "C38", "C39"):
    NOVELTY[cid] = (OVERLAP, "agent groups on Tor")
for cid in ("C08", "C09", "C10", "C11"):
    NOVELTY[cid] = (NEW, "Synapolis")
for cid in ("C29", "C30", "C31", "C32"):
    NOVELTY[cid] = (NEW, "MoltBunker")
for cid in ("C21", "C22", "C23", "C24", "C25", "C26", "C27"):
    NOVELTY[cid] = (NEW, "Distill")
for cid in ("C40", "C42", "C43"):
    NOVELTY[cid] = (NEW, "Toro")
for cid in ("C13", "C14", "C15", "C17", "C18", "C19", "C20"):
    NOVELTY[cid] = (NEW, "TV#### flood")
NOVELTY["C81"] = (NEW, "Synapolis element; flatboard element NOT_CHECKED_AS_SUBJECT")
for cid in ("C12", "C45", "C46", "C47", "C48", "C49", "C73", "C80", "C82", "C83", "C84", "C85"):
    NOVELTY[cid] = (NOT_CHECKED, "not among the 10 novelty-pass subjects")
for cid in ("C90", "C91"):
    NOVELTY[cid] = ("NOT_APPLICABLE — report method description", "report method")
for cid in STAND:
    NOVELTY[cid] = ("NOT_APPLICABLE — report-text observation", "report text")


def main():
    claims_text = (WORK / "linguist" / "CLAIMS.md").read_text()
    review_text = (WORK / "adversarial" / "REVIEW.md").read_text()
    claims = {}
    for line in claims_text.splitlines():
        m = re.match(r"^\|\s*(C\d+)\s*\|", line)
        if not m:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        assert len(parts) == 6, f"bad row: {line[:120]}"
        cid, sentence, section, grade, evidence, subjects = parts
        assert cid not in claims, f"dup {cid}"
        claims[cid] = {"sentence": sentence, "section": section,
                       "grade": grade, "subjects": subjects}
    assert len(claims) == 94, f"expected 94 claims, got {len(claims)}"
    assert set(claims) == {f"C{i:02d}" for i in range(1, 95)}, "claim id set mismatch"

    ingested = [cid for cid in sorted(claims) if cid not in KILLED]
    assert len(ingested) == 88, len(ingested)
    assert set(ingested) == STAND | set(CAVEAT), (
        f"STAND+CAVEAT != ingested: missing={set(ingested) - STAND - set(CAVEAT)} "
        f"extra={set(CAVEAT) - set(ingested)}")
    for cid, cav in CAVEAT.items():
        assert cav in review_text, f"caveat for {cid} NOT verbatim in REVIEW.md"
    for cid in ingested:
        assert cid in NOVELTY, f"no novelty mapping for {cid}"
    # dedup within batch by key field (claim_id) + by value text
    values = [claims[c]["sentence"] for c in ingested]
    assert len(set(values)) == len(values), "duplicate claim text in batch"
    assert not (set(values) & {claims[c]["sentence"] for c in KILLED}) or True
    killed_texts = {claims[c]["sentence"] for c in KILLED}
    assert not (set(values) & killed_texts), "killed claim text leaked into batch"

    records = []
    records.append({
        "ref": "src", "kind": "source",
        "body": {
            "source_type": "report",
            "locator": "https://github.com/SauersML/DarkSwarm/blob/main/README.md",
            "title": "DarkSwarm",
            "platform": "github",
        },
        "tags": {"lane": "darkswarm-20261101"},
    })
    records.append({
        "ref": "report", "kind": "observation",
        "body": {
            "type": "intel.report",
            "data_schema": "urn:factum:intel:report:1",
            "source": "@src",
            "observed_at": "2026-11-01T15:36:15Z",
            "time_basis": "source_metadata",
            "files": [{"artifact": "@readme", "role": "source-text",
                       "filename": "README.md"}],
            "data": {
                "lab": "SauersML/DarkSwarm",
                "title": "DarkSwarm",
                "url": "https://github.com/SauersML/DarkSwarm",
                "report_date": "2026-11-01",
                "cached_path": "data/lanes/darkswarm-20261101/raw/README.md",
                "provenance": "Captured 2026-11-02T05:20:33Z via git clone --depth 1 of SauersML/DarkSwarm main HEAD be21462916e9f94ee7ff2ad48eb6c82b92d1617e (HEAD commit 2026-11-01 07:36:15 -0800, the observed_at above in UTC); 51/51 files sha256-verified (README.md 16,325 bytes + 50 PNGs under raw/images/); report by Opus 5.5, presented in the text as Claude. 37 PNGs have no tie in the README text and support no claim. Capture per work/capture/STATUS.md.",
                "summary": "Secondary report by Opus 5.5 (presented as Claude) on a hunt for AI agents on Tor: relay census, Synapolis city, TV#### flood, Distill on Stellar, MoltBunker, Toro, Colony and musebook boards. Linguist: 94 claims (OBSERVED 7, REPORTED 81, INFERENCE 6). Adversarial review: KILL 6, DOWNGRADE 81, STAND 7. This batch ingests 88 claims (7 STAND + 81 DOWNGRADED with exact caveats) and excludes the 6 KILLED claims entirely.",
            },
        },
        "tags": {
            "lane": "darkswarm-20261101",
            "head": "be21462916e9f94ee7ff2ad48eb6c82b92d1617e",
            "claims_ingested": 88,
            "claims_killed_excluded": 6,
        },
    })
    for cid in ingested:
        c = claims[cid]
        if cid in STAND:
            basis, verdict = "OBSERVED", "STAND"
            note = "STAND per adversarial review; observation about the report text itself, no extra caveat."
            tags = {"lane": "darkswarm-20261101", "claim_id": cid,
                    "grade": c["grade"], "adversarial_verdict": verdict,
                    "readme_section": c["section"], "subjects": c["subjects"],
                    "verification": "NOT_ASSESSED", "verification_source": "none"}
        else:
            basis = "INFERENCE" if c["grade"] == "INFERENCE" else "UPSTREAM"
            if cid in VERIFIED:
                ver, vsrc = "VERIFIED", "verifier"
            elif cid in PARTIAL:
                ver, vsrc = "PARTIAL", "verifier"
            elif cid in UNCHECKABLE:
                ver, vsrc = "UNCHECKABLE", "verifier"
            elif cid in CRYPTO:
                ver, vsrc = CRYPTO[cid], "crypto"
            else:
                ver, vsrc = "NOT_ASSESSED", "none"
            note = CAVEAT[cid]
            tags = {"lane": "darkswarm-20261101", "claim_id": cid,
                    "grade": c["grade"], "adversarial_verdict": "DOWNGRADE",
                    "readme_section": c["section"], "subjects": c["subjects"],
                    "verification": ver, "verification_source": vsrc,
                    "adversarial_caveat": CAVEAT[cid]}
        framing, subject = NOVELTY[cid]
        tags["novelty"] = framing
        tags["novelty_subject"] = subject
        if cid == "C35":
            tags["adversarial_note"] = "C35 cuts against survival claims."
        records.append({
            "ref": cid.lower(), "kind": "claim",
            "body": {
                "subject": "@report",
                "property": "darkswarm-claim",
                "value": c["sentence"],
                "basis": basis,
                "cites": ["@report"],
                "note": note,
            },
            "tags": tags,
        })
    bundle = {
        "bundle": 2,
        "actor": "agent:darkswarm-lane-ingest",
        "idempotency_key": "darkswarm-20261101-ingest-v1",
        "files": [{"ref": "readme",
                   "path": "data/lanes/darkswarm-20261101/raw/README.md",
                   "storage": "local",
                   "tags": {"lane": "darkswarm-20261101"}}],
        "records": records,
    }
    OUT.write_text(json.dumps(bundle, indent=1, ensure_ascii=False) + "\n")
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"wrote {OUT} records={len(records)} kinds={kinds}")
    print(f"killed excluded: {sorted(KILLED)}")
    print(f"stand: {sorted(STAND)} downgraded: {len(CAVEAT)}")


if __name__ == "__main__":
    main()
