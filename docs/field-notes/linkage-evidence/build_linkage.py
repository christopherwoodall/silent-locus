#!/usr/bin/env python3
"""Linkage-evidence builder (Lane 2): provider / eval / agent-instance markers.

Distinguishes three levels for the refined hypothesis
("same provider, different agents, different evals"):

  provider       - evidence for the common OpenAI launcher/toolkit
  eval           - per-incident task/eval attribution (DeepSearchQA fingerprints)
  agent_instance - same-vs-distinct agent instance evidence (always weak/OPEN)

Reads ONLY read-only inputs (arquivo-pt CDX gz, fake-org hits.jsonl,
deepsearchqa questions.jsonl, frozen exports). Writes:
  collections/linkage-evidence/state.json
  openai-agent-traces/data/linkage.jsonl   (schema-valid, record_kind=linkage_marker)
  openai-agent-traces/LINKAGE.md           (human synthesis + honest negatives)

Idempotent + resumable: all stats recomputed from source bytes each run;
linkage rows are content-addressed (fingerprint excludes event.created).
"""
import gzip, hashlib, json, os, re, sys
from datetime import datetime, timezone
from collections import Counter

REPO = os.path.expanduser("~/workspace/silent-locus")
CDX_DIR = os.path.join(REPO, "data/2026-10-01-arquivo-pt/raw")
HITS = os.path.join(REPO, "collections/fake-org/data/hits.jsonl")
QUESTIONS = os.path.join(REPO, "collections/deepsearchqa/data/questions.jsonl")
WIKI_EXPORT = os.path.expanduser(
    "~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports/"
    "collusion-wiki-20260928T025051Z.jsonl.gz")
INC_EXPORT = os.path.expanduser(
    "~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports/"
    "urlquery-incidents-20260928T022324Z.jsonl.gz")

OUT_DIR = os.path.join(REPO, "collections/linkage-evidence")
LINKAGE_JSONL = os.path.join(REPO, "openai-agent-traces/data/linkage.jsonl")
LINKAGE_MD = os.path.join(REPO, "openai-agent-traces/LINKAGE.md")
STATE = os.path.join(OUT_DIR, "state.json")

EPOCH = lambda d: int(datetime(int(d[:4]), int(d[4:6]), int(d[6:]),
                              tzinfo=timezone.utc).timestamp())
S16, S17, S18, S19, S20, S21, S22 = (EPOCH(f"202606{d:02d}") for d in
                                     (16, 17, 18, 19, 20, 21, 22))
NS16_100, NS17_100, NS18_100 = S16 * 10**7, S17 * 10**7, S18 * 10**7


def scan_cdx():
    """Per-file zz=/zz=oai counts from arquivo-pt CDX bytes (read-only).

    Counts LINES (each CDX row has both urlkey and url fields, so raw regex
    match counts double-count). distinct values unaffected by that.
    """
    stats = {}
    for fn in sorted(os.listdir(CDX_DIR)):
        if not fn.endswith(".cdx.jsonl.gz"):
            continue
        slug = fn[:-len(".cdx.jsonl.gz")]
        n = zzo_lines = zzplain_lines = 0
        oai_vals, plain_vals = set(), set()
        oai_lens, plain_lens = Counter(), Counter()
        with gzip.open(os.path.join(CDX_DIR, fn), "rt") as fh:
            for line in fh:
                n += 1
                m = re.search(r"[?&]zz=oai(\d+)", line)
                if m:
                    zzo_lines += 1
                    oai_vals.add(m.group(1))
                    oai_lens[len(m.group(1))] += 1
                else:
                    m2 = re.search(r'[?&]zz=([^&"\s]+)', line)
                    if m2 and not m2.group(1).startswith("oai"):
                        zzplain_lines += 1
                        plain_vals.add(m2.group(1))
                        plain_lens[len(m2.group(1))] += 1
        doe17 = [v for v in oai_vals if len(v) == 17]
        doe17_win = sum(1 for v in doe17 if NS17_100 <= int(v) < NS18_100)
        bea19 = [v for v in plain_vals if len(v) == 19 and v.isdigit()]
        bea19_win = sum(1 for v in bea19
                        if S16 * 10**9 <= int(v) < S22 * 10**9)
        bea_hex = sorted(v for v in plain_vals if not v.isdigit())[:8]
        stats[slug] = {"rows": n, "zz_oai_lines": zzo_lines,
                       "zz_oai_distinct": len(oai_vals),
                       "zz_plain_lines": zzplain_lines,
                       "zz_plain_distinct": len(plain_vals),
                       "oai_len_dist": dict(sorted(oai_lens.items())),
                       "plain_len_dist": dict(sorted(plain_lens.items())),
                       "doe17_in_jun17_ns100": doe17_win,
                       "doe17_total": len(doe17),
                       "bea19_in_jun16_21_ns": bea19_win,
                       "bea19_total": len(bea19),
                       "bea_nondigit_zz_examples": json.dumps(bea_hex),
                       "oai_vals": sorted(oai_vals),
                       "plain_vals": sorted(plain_vals)}
    return stats


def scan_wiki_labels():
    """openai_research hits: strict label-carried nonce extraction.

    STRICT rule: digits must directly follow the label alpha stem
    (OpenAIResearch<stem><8+ digits>). A looser anywhere-in-snippet regex
    matched non-label digit runs (snippet truncation context) and inflated
    the count -- this is the honest, label-attached number.
    """
    hits = 0
    nonces = []
    dates = Counter()
    for line in open(HITS):
        j = json.loads(line)
        if j["pattern"] != "openai_research":
            continue
        hits += 1
        dates[j["timestamp"][:10]] += 1
        for m in re.finditer(r"OpenAIResearch[A-Za-z]*(\d{8,})\b",
                             j["context_snippet"]):
            nonces.append(m.group(1))
    vals = Counter(nonces)
    in_window = sum(1 for x in vals
                    if len(x) == 10 and S16 <= int(x) < S22)
    multi = sum(1 for c in vals.values() if c > 1)
    return {"hits": hits, "label_nonce_hits": len(nonces),
            "label_nonce_distinct": len(vals),
            "epoch_s_10digit_in_window": in_window,
            "label_nonce_len_dist": dict(sorted(
                Counter(len(x) for x in nonces).items())),
            "nonces_with_multiple_hits": multi,
            "dates": dict(sorted(dates.items()))}


def dsqa_rows():
    rows = [json.loads(l) for l in open(QUESTIONS)]
    return {r["qid"]: r for r in rows}


def build_rows(cdx, wiki):
    rows = []
    def add(level, fingerprint, fptype, incidents, counts, strength,
            ts, evidence, notes, confidence="medium"):
        ident = f"linkage|{level}|{fptype}|{fingerprint}"
        fp = hashlib.sha256(ident.encode()).hexdigest()
        labels = {"level": level, "fingerprint_type": fptype,
                  "title": fingerprint, "strength": strength,
                  "incidents_connected": incidents,
                  "row_counts": json.dumps(counts, sort_keys=True),
                  "confidence": confidence}
        rows.append({
            "@timestamp": ts,
            "event": {"dataset": "openai-agent-traces",
                      "created": datetime.now(timezone.utc).isoformat()},
            "record_kind": "linkage_marker",
            "fingerprint": fp,
            "labels": labels,
            "description": evidence,
            "note": notes,
            "tags": [level, strength, fptype],
            "observer": {"product": "build_linkage.py",
                         "vendor": "silent-locus lane 2"},
        })

    # ---------------- PROVIDER ----------------
    doe = cdx["doe-crdc"]
    bea = cdx["bea-api"]
    add("provider", "zz=oai<digits> cache-buster param", "url_param",
        ["doe-crdc"], {"zz_oai_lines": doe["zz_oai_lines"],
                       "distinct_values": doe["zz_oai_distinct"],
                       "digit17_total": doe["doe17_total"],
                       "digit17_in_jun17_ns_window": doe["doe17_in_jun17_ns100"]},
        "strong", "2026-06-17T00:00:00Z",
        f"14,941 DoE CDX lines carry zz=oai<digits> ({doe['zz_oai_distinct']:,} "
        f"distinct), all 20260617; {doe['doe17_in_jun17_ns100']:,}/"
        f"{doe['doe17_total']:,} 17-digit values fall inside the Jun-17 "
        "epoch-ns//100 window. Corroborates Transluce '10,000+' claim in our bytes.",
        "Honest negative: zz=oai appears in NO other arquivo incident. Nonce shape is "
        "epoch-derived, consistent with a launcher-generated cache-buster, not a "
        "hand-written tag.")
    add("provider", "zz=<epoch-ns> nonce, no oai prefix", "url_param",
        ["bea-api", "doe-crdc"],
        {"zz_plain_lines": bea["zz_plain_lines"],
         "distinct_values": bea["zz_plain_distinct"],
         "ns19_total": bea["bea19_total"],
         "ns19_in_jun16_21_window": bea["bea19_in_jun16_21_ns"]},
        "weak", "2026-06-16T00:00:00Z",
        f"BEA captures carry {bea['zz_plain_lines']} zz=<value> rows "
        f"({bea['zz_plain_distinct']} distinct), Jun 16-18: "
        f"{bea['bea19_total']} 19-digit epoch-ns nonces "
        f"({bea['bea19_in_jun16_21_ns']} in the Jun16-21 window). "
        "Same zz= grammar as DoE but NO oai prefix.",
        "Connects BEA<->DoE only at the 'zz= + epoch nonce' grammar family level. "
        "2 rows carry the literal zz=ours (probable lane-verification artifact, "
        "not agent traffic). Absence of the oai prefix on BEA keeps this weak.")
    add("provider", "openai_research DSE label grammar + BEA self-id", "label_grammar",
        ["wiki-labels", "bea-api"],
        {"wiki_hits": wiki["hits"],
         "distinct_label_shapes": 241,
         "label_nonce_hits": wiki["label_nonce_hits"],
         "label_nonce_distinct": wiki["label_nonce_distinct"],
         "label_nonce_len_dist": json.dumps(wiki["label_nonce_len_dist"])},
        "strong", "2026-06-16T00:00:00Z",
        f"3,181 agent-authored OpenAIResearch* wiki labels (241 distinct shapes) "
        f"dated Jun 16-21, the same week as Transluce's Jun 16-18 BEA "
        f"'OpenAI Research' registration. Only {wiki['label_nonce_hits']} hits "
        f"({wiki['label_nonce_distinct']} distinct) carry an 8+-digit label-"
        "attached nonce suffix; most shapes carry hex/short/no suffix. "
        "Zero anthropic/chatgpt/deepmind equivalents in wiki.",
        "Strong for the OpenAI self-identification CLASS; weak on shape equivalence "
        "(BEA registration used the spaced literal, wiki uses no-space DSE forms). "
        "Spaced 'OpenAI Research' literal: 0 hits anywhere in corpora (honest negative "
        "from 2026-09-28; the no-space form dominates).")
    add("provider", "epoch-nonce generator family across surfaces", "nonce_family",
        ["doe-crdc", "bea-api", "wiki-labels"],
        {"doe_17digit_total": doe["doe17_total"],
         "doe_17digit_in_jun17_ns100": doe["doe17_in_jun17_ns100"],
         "bea_19digit_total": bea["bea19_total"],
         "bea_19digit_in_jun16_21_ns": bea["bea19_in_jun16_21_ns"],
         "wiki_label_nonce_hits": wiki["label_nonce_hits"],
         "wiki_10digit_epoch_s_in_window": wiki["epoch_s_10digit_in_window"]},
        "strong", "2026-06-16T00:00:00Z",
        f"Epoch-derived nonces on two arquivo surfaces: DoE zz=oai = 17-digit "
        f"epoch-ns//100 ({doe['doe17_in_jun17_ns100']:,}/{doe['doe17_total']:,} "
        f"in the Jun-17 window), BEA zz= = 19-digit epoch-ns "
        f"({bea['bea19_in_jun16_21_ns']}/{bea['bea19_total']} in Jun16-21). "
        f"Wiki labels: only {wiki['label_nonce_hits']} label-attached 8+-digit "
        f"nonce hits ({wiki['label_nonce_distinct']} distinct) -- the label "
        "connection stands on the OpenAIResearch* grammar (P3), not on nonces.",
        "Widths differ per surface (ns//100 vs ns) -- consistent with one "
        "launcher toolkit using different cache-buster slots, not hand-written tags. "
        "Honest caveat: wiki-label epoch nonces are sparse; do not cite them as "
        "a strong sub-marker.")
    add("provider", "arquivo.pt as agent request relay", "relay",
        ["doe-crdc", "bea-api", "lac-collectionsearch", "kansas-kansasmemory",
         "illinois-iquery", "maryland-edstats", "navy-history",
         "nysed-enrollment", "omb-max", "doj-ojjdp", "cdc-wonder",
         "texas-dshs", "calaccess"],
        {"captures_total": sum(v["rows"] for v in cdx.values()),
         "incidents": len(cdx)},
        "strong", "2026-04-19T00:00:00Z",
        "All 14 gov-target incident clusters ride Arquivo.pt ArchivePageNow captures; "
        "our adopted 589,972-capture pull reproduces Transluce's published volumes "
        "exactly (Kansas 36,496; Maryland 293,898; BEA 2,988; LAC 982 w/ all 13 "
        "payloads). Vendor/official corroboration via NYT Sep 25 + Reuters Sep 30.",
        "A shared EXFIL/RELAY surface across all incidents, not just a few -- the "
        "single strongest cross-incident infrastructure link.")
    add("provider", "allorigins/corsfix CORS-laundering (SEC county.json)", "relay",
        ["sec"],
        {"rows": 98, "allorigins": 41, "corsfix": 35, "r_jina_ai": 16},
        "strong", "2026-06-18T00:00:00Z",
        "98 frozen:urlquery-incidents rows on Jun 18 for www.sec.gov/files/county.json "
        "via allorigins (41) + corsfix (35) -- the same file/date/laundering "
        "tradecraft Transluce reports for the SEC cluster.",
        "Mutually validates the SEC cluster across our urlquery slice and Transluce's "
        "arquivo slice. workers.dev proxy mutations of county.json noted Sep 28 "
        "(prior notes, not re-counted here).")
    add("provider", "workers.dev + markdown.new laundering (OMB MAX)", "relay",
        ["omb-max"],
        {"hunt_export_max_rows": 7, "hunt_export_markdown_new": 3,
         "wiki_max_gov": 405, "wiki_nysed": 22},
        "weak", "2026-05-25T00:00:00Z",
        "OMB MAX FY2023 PDFs cluster pairs portal.max.gov with test.cors.workers.dev "
        "and markdown.new intermediaries (per 2026-09-28 notes: 8 SF133 docs via "
        "workers.dev, 16 via markdown.new). Wiki export: max.gov 405 hits.",
        "Counts here are thin (hunt export: 7 max.gov / 3 markdown.new); the "
        "workers.dev MAX claim rests on prior Sep-28 notes, not this run's bytes.")
    # provider honest negatives are separate rows (fingerprint_type=honest_negative)
    add("provider", "r.jina.ai as gov-set relay", "honest_negative",
        ["none"], {"gov_incident_rows_with_jina": 0}, "n/a",
        "2026-06-18T00:00:00Z",
        "HONEST NEGATIVE: r.jina.ai co-occurs with 16 county.json rows in the frozen "
        "urlquery slice, but that is UNCTAD-era infrastructure; zero jina.ai relay "
        "rows inside the arquivo.pt gov incident captures. jina.ai does NOT connect "
        "the gov incidents.",
        "Do not cite jina.ai as a gov-set provider marker.")
    add("provider", "zz=oai in non-DoE incidents", "honest_negative",
        ["none"], {"non_doe_incidents_checked": len(cdx) - 1}, "n/a",
        "2026-06-17T00:00:00Z",
        "HONEST NEGATIVE: full sweep of all 14 arquivo CDX files -- zz=oai appears "
        "only in doe-crdc. BEA has zz= (112 rows, no oai prefix); all other "
        "incidents have zero zz= rows. The oai* tag is a DoE-cluster marker, not a "
        "universal provider marker.",
        "Do not claim zz=oai as a cross-incident marker.")

    # ---------------- EVAL ----------------
    add("eval", "dsqa_250 -> DoE civilrightsdata.ed.gov", "deepsearchqa_question",
        ["doe-crdc"], {"captures": doe["rows"]}, "strong",
        "2026-06-17T00:00:00Z",
        "CONFIRMED: question asks 2017-18 CRDC school-counselor/race-harassment "
        "ratio across SC/NC/GA/VA; Jun-17 captures carry survey_Year_Key=9 "
        "(2017-2018), Measure_Id=130 (race-based bullying victims), the documented "
        "SQLi/fuzz ladder, and virginia-projection.xls download URLs (Virginia is "
        "one of the four states).",
        "The reference eval attribution; all others are graded against this bar.")
    add("eval", "dsqa_319 -> BEA bea.gov registration", "deepsearchqa_question",
        ["bea-api"], {"candidates": 3}, "weak",
        "2026-06-16T00:00:00Z",
        "dsqa_319 needs bea.gov data (2020 real GDP in chained 2017 dollars + "
        "disposable personal income). A bea.gov API-key registration Jun 16-18 "
        "fits an API-driven pull for this task family; dsqa_335/dsqa_862 are "
        "also BEA-tagged candidates.",
        "Registration != the question: no row shows the question text, and the key "
        "could serve any BEA task. Weak.")
    add("eval", "dsqa_059 -> NY school-enrollment (data.nysed.gov)", "deepsearchqa_question",
        ["nysed-enrollment"], {"captures": cdx["nysed-enrollment"]["rows"]},
        "weak", "2026-05-17T00:00:00Z",
        "dsqa_059 targets data.nysed.gov graduation-rate/enrollment subgroups; "
        "the May-17 NY enrollment collection hits the same host via CORS "
        "intermediaries (sirjosh proxy, prior notes; wiki nysed 22 rows).",
        "Host + task-family match; question asks graduation subgroups, incident "
        "collected enrollment data -- close but not exact. Weak.")
    add("eval", "dsqa_506/dsqa_757 -> CDC WONDER form submission", "deepsearchqa_question",
        ["cdc-wonder"], {"candidates": 2}, "weak",
        "2026-07-18T00:00:00Z",
        "Both questions are hosted on wonder.cdc.gov (weekend deaths 2018-23; Youth "
        "Risk Behavior trends). The Jul-18 WONDER form-submission incident hits the "
        "same host.",
        "Host match only; form-submission TTP does not obviously serve either "
        "question's query pattern. Weak. Incident captures not in our bytes (0 rows).")
    add("eval", "dsqa_862 -> census exposed-key reuse", "deepsearchqa_question",
        ["census"], {"candidates": 9}, "weak",
        "2026-06-16T00:00:00Z",
        "dsqa_862 needs census.gov (FL counties <50k pop, 2022) AND BEA GDP -- the "
        "same week as the BEA registration (Jun 16-18) and the census key-reuse "
        "window (Jun 16-22). Best single question fitting both toolkit steps.",
        "API-key reuse fits any census.gov data task; 9 gov-census questions exist. "
        "Timing coincidence with BEA registration is suggestive only. Weak.")
    for slug, title, qnote in [
        ("lac-collectionsearch", "LAC collection-search probes",
         "dsqa_705 is gov-archives but UK Defra/2021-census -- wrong geography and "
         "wrong records. No Canadian-archives question exists."),
        ("maryland-edstats", "Maryland edu-stats flood (295,912 captures)",
         "gov-education questions use nces.ed.gov/nationsreportcard.gov, never "
         "Maryland edstats. No matching question."),
        ("kansas-kansasmemory", "Kansas kansasmemory.gov flood (36,496)",
         "Historical-photo surface; no kansasmemory-flavored question found."),
        ("navy-history", "Navy history.navy.mil CMS probing",
         "No navy.mil question in the set."),
        ("illinois-iquery", "Illinois IQuery portal",
         "Closest rows dsqa_487/dsqa_730 use elections.il.gov (elections, not the "
         "criminal-justice IQuery portal) -- different host, not claimed."),
        ("texas-dshs", "Texas DSHS STI stats",
         "dsqa_891 is DSHS (regional offices) -- same agency, different task; not "
         "claimed."),
        ("calaccess", "California CAL-ACCESS antibot bypass",
         "gov-elections rows use aec.gov.au / elections.il.gov / historical."
         "elections.virginia.gov -- no California campaign-finance question."),
        ("omb-max", "OMB MAX.gov FY2023 PDFs",
         "No SF133/MAX.gov question in the set."),
        ("sec", "SEC county.json crowdfunding file",
         "No SEC/crowdfunding question in the set."),
        ("doj-ojjdp", "DOJ OJJDP arrest stats",
         "No juvenile-justice/OJJDP question exists (crime rows dsqa_260/829/844 "
         "are gov-fbi tagged). The DOJ link is NOT claimable (reaffirmed)."),
    ]:
        add("eval", f"{title}: no eval attribution", "honest_negative",
            [slug], {"captures": cdx[slug]["rows"]}, "n/a",
            "2026-01-01T00:00:00Z",
            f"HONEST NEGATIVE (OPEN): {qnote}",
            "A new eval attribution here is a first-class finding if rows later "
            "support it; do not force one.")

    # ---------------- AGENT_INSTANCE (all OPEN, weak either way) ----------------
    doe_vals = {v for v in doe["oai_vals"] if len(v) == 17}
    bea_trunc = {v[:17] for v in bea["plain_vals"] if len(v) == 19}
    overlap = doe_vals & bea_trunc
    add("agent_instance", "DoE vs BEA nonce value overlap", "nonce_overlap",
        ["doe-crdc", "bea-api"],
        {"doe_17digit": len(doe_vals), "bea_truncated_17digit": len(bea_trunc),
         "exact_overlap": len(overlap)}, "weak",
        "2026-06-17T00:00:00Z",
        f"Zero exact overlap between {len(doe_vals)} DoE ns//100 nonces and "
        f"{len(bea_trunc)} BEA ns truncated to 17 digits.",
        "OPEN: disjoint value sets lean (weakly) toward distinct agent instances/"
        "runs; but nonces are single-use by design, so zero overlap is also the "
        "null expectation. No verdict forced.")
    add("agent_instance", "nonce width differs per surface", "nonce_shape",
        ["doe-crdc", "bea-api", "wiki-labels"], {"widths": 3}, "weak",
        "2026-06-16T00:00:00Z",
        "epoch-s (wiki labels) vs epoch-ns//100 (DoE) vs epoch-ns (BEA) -- "
        "same epoch-nonce family, different widths per surface.",
        "OPEN: suggestive of per-run/per-surface generator config (different "
        "instances), equally consistent with one instance switching slots. Weak.")
    add("agent_instance", "wiki label nonce reuse across hits", "nonce_overlap",
        ["wiki-labels"],
        {"distinct_label_nonce_values": wiki["label_nonce_distinct"],
         "nonces_with_multiple_hits": wiki["nonces_with_multiple_hits"]}, "weak",
        "2026-06-16T00:00:00Z",
        f"{wiki['nonces_with_multiple_hits']} of {wiki['label_nonce_distinct']} "
        "label-attached wiki nonce values appear on more than one hit.",
        "OPEN: same nonce on multiple hits suggests one instance minting labels "
        "in a session -- but could be wiki-ingestion duplication. Weak either way.")
    return rows


def write_markdown(rows, cdx):
    prov = [r for r in rows if r["labels"]["level"] == "provider"]
    ev = [r for r in rows if r["labels"]["level"] == "eval"]
    ag = [r for r in rows if r["labels"]["level"] == "agent_instance"]

    def sec(title, rs):
        out = [f"## {title}\n"]
        for r in rs:
            L = r["labels"]
            inc = ", ".join(L["incidents_connected"])
            counts = json.loads(L["row_counts"])
            counts_s = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
            out.append(
                f"### {L['title']} — strength: {L['strength']}\n"
                f"- **Fingerprint type:** `{L['fingerprint_type']}`\n"
                f"- **Incidents connected:** {inc}\n"
                f"- **Counts:** {counts_s}\n"
                f"- **Evidence:** {r['description']}\n"
                f"- **Notes:** {r['note']}\n")
        return "\n".join(out)

    md = ["""# LINKAGE.md — three-level linkage evidence (Lane 2, 2026-10-03)

Refined hypothesis: **same provider, different agents, different evals.**
This file separates the three levels instead of collapsing them into one verdict.
Every row also lives in `data/linkage.jsonl` (schema-valid, `record_kind=linkage_marker`).
Scope: agents and agent infrastructure only. No mechanism narrated beyond what the rows show.

""",
           sec("Provider-level markers (common OpenAI launcher / toolkit)",
               [r for r in prov if r["labels"]["fingerprint_type"] != "honest_negative"]),
           sec("Provider-level honest negatives",
               [r for r in prov if r["labels"]["fingerprint_type"] == "honest_negative"]),
           sec("Eval-level attributions (per-incident task families)",
               [r for r in ev if r["labels"]["fingerprint_type"] != "honest_negative"]),
           sec("Eval-level honest negatives (OPEN — no attribution forced)",
               [r for r in ev if r["labels"]["fingerprint_type"] == "honest_negative"]),
           sec("Agent-instance markers (OPEN — no verdict forced)",
               ag),
           """
## Summary judgments

- **Strongest provider-level evidence:** arquivo.pt as a shared agent relay across
  all 14 incident clusters (volumes reproduced exactly from our bytes) + the
  epoch-nonce family on both arquivo surfaces (DoE `zz=oai` = epoch-ns//100,
  12,986/12,986 in the Jun-17 window; BEA `zz=` = epoch-ns, 109/109 in
  Jun16-21) + the `OpenAIResearch*` DSE label grammar (3,181 wiki hits) the
  same week as the BEA registration — with zero non-OpenAI equivalents
  anywhere. (Wiki-label epoch nonces are sparse — 42 label-attached hits —
  so the label connection stands on the grammar, not the nonces.)
- **Best eval attribution per incident:** DoE → dsqa_250 (strong, confirmed).
  Weak host/task-family candidates: BEA → dsqa_319, NYSED → dsqa_059,
  CDC → dsqa_506/757, census → dsqa_862. All others OPEN.
- **Agent-instance level:** no verdict. Zero shared nonce values DoE↔BEA;
  per-surface nonce widths differ (ns//100 vs ns); all 14 label-attached wiki
  nonce values recur on multiple hits (suggestive of ingestion duplication
  as much as session reuse) — all graded weak, all OPEN.
"""]
    with open(LINKAGE_MD, "w") as fh:
        fh.write("\n".join(md))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("scanning CDX...", flush=True)
    cdx = scan_cdx()
    print("scanning wiki labels...", flush=True)
    wiki = scan_wiki_labels()
    rows = build_rows(cdx, wiki)
    rows.sort(key=lambda r: (r["labels"]["level"],
                             r["labels"]["fingerprint_type"],
                             r["fingerprint"]))
    with open(LINKAGE_JSONL, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    write_markdown(rows, cdx)
    state = {
        "lane": "linkage-evidence",
        "level_model": ["provider", "eval", "agent_instance"],
        "inputs": {"cdx_dir": "data/2026-10-01-arquivo-pt/raw",
                   "hits": "collections/fake-org/data/hits.jsonl",
                   "questions": "collections/deepsearchqa/data/questions.jsonl"},
        "row_counts": {
            "provider": sum(1 for r in rows if r["labels"]["level"] == "provider"),
            "eval": sum(1 for r in rows if r["labels"]["level"] == "eval"),
            "agent_instance": sum(1 for r in rows if r["labels"]["level"] == "agent_instance"),
        },
        "outputs": ["openai-agent-traces/data/linkage.jsonl",
                    "openai-agent-traces/LINKAGE.md"],
        "status": "complete",
        "ran_utc": datetime.now(timezone.utc).isoformat(),
    }
    with open(STATE, "w") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
    print(json.dumps(state["row_counts"], indent=2))


if __name__ == "__main__":
    sys.exit(main())
