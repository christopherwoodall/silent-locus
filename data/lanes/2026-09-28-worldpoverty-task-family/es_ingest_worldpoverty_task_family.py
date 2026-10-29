#!/usr/bin/env python3
"""Rebuild the worldpoverty-task-family event docs from primary sources.

Lane U (2026-09-28): structural dataset of the api.worldpoverty.io agent
task family -- 15 rmn.re slugs (decoded GraphQL query templates), 3
byte-identical dse-wiki "Poverty Links" pages, the WorldPovertyClockSequenceJun19
live sequence page, the IHME family-planning cross-citation, and the
staging -> burst -> hygiene run-shape docs.

Raw-input loss (normalization, 2026-09-28/29): the collection's original
hits.jsonl was folded into the staged events.jsonl and deleted. All PRIMARY
sources survive on disk (and in git history), so this script rebuilds the
22 docs from them rather than from the staged file:

  data/2016-12-28-rmn-re/raw/link_table_decoded_2026-09-27.json
      15 decoded rmn.re slugs (decoded_target, clicks, created, creator_ip16,
      chain_wrappers)
  data/2026-05-17-collusion-wiki/raw/shortener-logs.json
      rmn.re YOURLS log: authoritative ISO-UTC creation times + click counts
  data/2026-05-17-collusion-wiki/raw/revisions.jsonl
      wiki page bodies + write_date + ip16 + label

Output: events.jsonl in this directory (22 docs, conforming to
schema/record.schema.json). Deterministic: fixed event.created,
@timestamp, and fingerprint seed, so re-runs are byte-identical.
Pure builder -- no network, no Elastic writes. Loading is generic via
scripts/push_to_local_es.py (auto-discovery).

Payload embedding (2026-09-29 repair): per-item payload material is embedded
in the new OPTIONAL top-level `payloads` array (schema/record.schema.json,
commit 37988db; documented in schema/README.md). Item shape:
{kind, content_type, content, encoding, truncated, byte_size, sha256}.
Embedded:

  - worldpoverty_slug (15 docs): one payload, kind=decoded_shortlink_target --
    the full decoded GraphQL target URL per slug (26-464 B each; 3,408 B
    total). The query template IS the evidence for this collection, so each
    doc carries its own and the dataset is self-contained for HuggingFace
    publishing.
  - wiki_poverty_links_page (3) + wiki_wpc_sequence_page (1): one payload,
    kind=wiki_page_body -- the full page body (460-615 B each;
    matched_string only carries the first 400 chars).
  - cross_family_citation (1): NO payload -- the citing revision bodies are
    ~21.6 KB across 10 revisions of another family's pages (out of collection
    scope); the note quotes the citing lines and the bodies remain addressable
    in the 2026-05-17-collusion-wiki collection.
  - run_shape (2): no per-item payload -- the collection-level artifacts
    (query templates, timeline) already live in raw/.

All embedded payloads are small enough to carry in full (truncated=false);
no truncation cap is exercised by this collection.

ID notes: the hunt-level `fingerprint` is computed with the legacy seed
"worldpoverty-task-family" (the pre-rename index name) so it stays stable
with the docs already indexed. The 3 wiki_poverty_links_page docs share one
fingerprint (byte-identical bodies -> identical matched_string) -- pre-existing
from the original Lane U build, preserved for stability. push_to_local_es.py
derives the ES _id from the sha256 of the whole canonical doc, so the added
payloads mean new _ids on the next load -- recreate the
2026-09-28-worldpoverty-task-family index (or accept new _ids) when the
hosted write freeze lifts.

Usage: python3 es_ingest_worldpoverty_task_family.py
"""
import json
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "data")

LINK_TABLE = os.path.join(DATA, "2016-12-28-rmn-re", "raw",
                          "link_table_decoded_2026-09-27.json")
YOURLS_LOG = os.path.join(DATA, "2026-05-17-collusion-wiki", "raw",
                          "shortener-logs.json")
REVISIONS = os.path.join(DATA, "2026-05-17-collusion-wiki", "raw",
                         "revisions.jsonl")

DATASET = "2026-09-28-worldpoverty-task-family"   # event.dataset == collection slug
FINGERPRINT_SEED = "worldpoverty-task-family"     # legacy seed; keeps fingerprints stable
EVENT_CREATED = "2026-09-28T10:55:04.215941+00:00"  # fixed for byte-identical re-runs
TS = "2026-09-28T10:52:00Z"
OBSERVER = {"product": "lane-u-worldpoverty-task-family", "vendor": "hunt",
            "type": "transform"}
COUNTRIES = "AFG,GHA,NGA,IND,MEX"
SRC_RMN = ("data/2016-12-28-rmn-re/raw/link_table_decoded_2026-09-27.json; "
           "data/2026-05-17-collusion-wiki/raw/shortener-logs.json")
SRC_WIKI = "data/2026-05-17-collusion-wiki/raw/revisions.jsonl"

docs = []


def fp(s):
    return hashlib.sha256(s.encode()).hexdigest()


def payload(kind, content_type, content, encoding="text"):
    body = content.encode("utf-8")
    return {
        "kind": kind,
        "content_type": content_type,
        "content": content,
        "encoding": encoding,
        "truncated": False,
        "byte_size": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
    }


def doc(record_kind, matched_string, source_url, note, tags, labels,
        confidence="medium", payloads=None):
    d = {
        "record_kind": record_kind,
        "event": {"dataset": DATASET, "created": EVENT_CREATED},
        "observer": dict(OBSERVER),
        "retrieved_via": "hunt lane U (2026-09-28): worldpoverty task-family structure; ",
        "fingerprint": fp(FINGERPRINT_SEED + "|" + record_kind + "|" + matched_string),
        "matched_string": matched_string,
        "source_url": source_url,
        "note": note,
        "confidence": confidence,
        "tags": tags,
        "labels": labels,
        "@timestamp": TS,
    }
    if payloads:
        d["payloads"] = payloads
    return d


# ---- template table (canonical forms in raw/query_templates.json) ----
# slug -> (template_id, years)
SLUG_TPL = {
    "wpccite2018x":      ("T-2018-C", "2018"),
    "wpcfinal20206539":  ("T-2020-A", "2020"),
    "wpcfinal20185574":  ("T-2018-A", "2018"),
    "agpovertyruralclock95080": ("T-dual-Q", "2018+2020"),
    "wpcagent2020md":    ("T-2020-B", "2020"),
    "wpcagent2020raw":   ("T-2020-B", "2020"),
    "wpcagent2018md":    ("T-2018-B", "2018"),
    "wpcagent2018raw":   ("T-2018-B", "2018"),
    "wpcrmn771":         ("T-dual-X", "2018+2020"),
    "pa1xy":             ("T-root", "none"),
    "pa0xy":             ("T-probe", "none"),
    "xyzpov27":          ("T-root", "none"),
    "testwp8342":        ("T-probe", "none"),
    "wpcafgghana20182020rural28218": ("T-dual-raw", "2018+2020"),
    "wpdata201246":      ("T-dual-ab", "2018+2020"),
}

# ---- 1. the 15 rmn.re slugs ----
linktab = {d.get("slug"): d for d in json.load(open(LINK_TABLE))}
log = json.load(open(YOURLS_LOG))
ylog = {l["keyword"]: l for l in log["sites"][0]["links"] if l.get("keyword")}

missing_link = [s for s in SLUG_TPL if s not in linktab]
missing_log = [s for s in SLUG_TPL if s not in ylog]
assert not missing_link, "slugs missing from decoded link table: %s" % missing_link
assert not missing_log, "slugs missing from YOURLS log: %s" % missing_log

n = 0
for slug, (tpl, years) in SLUG_TPL.items():
    d = linktab[slug]
    yl = ylog[slug]
    target = d.get("decoded_target") or d.get("target")
    n += 1
    md_wrap = "markdown.new" in json.dumps(d.get("chain_wrappers", []))
    tags = ["source:rmn-re", "host:api.worldpoverty.io", "task:worldpoverty-graphql",
            "template:" + tpl, "year:" + years]
    if md_wrap:
        tags.append("proxy:markdown.new")
    if tpl in ("T-probe", "T-root"):
        tags.append("probe")
    docs.append(doc(
        "worldpoverty_slug",
        "https://rmn.re/%s -> %s" % (slug, target),
        "https://rmn.re/%s" % slug,
        "Agent-created rmn.re shortlink #%d of 15 (template %s, years %s). YOURLS-log creation %s (authoritative UTC; decoded-table 'created' renders +4h); %s clicks (YOURLS log) / %s clicks (decoded table). Creator ip16 %s.%s"
        % (n, tpl, years, yl["time"], yl["clicks"], d.get("clicks"),
           d.get("creator_ip16"),
           " Chain wrapper markdown.new (two-hop: shortlink -> markdown render -> API)." if md_wrap else ""),
        tags,
        {"host": "api.worldpoverty.io", "slug": slug, "template": tpl,
         "years": years, "countries": COUNTRIES,
         "created_utc": yl["time"], "clicks_log": str(yl["clicks"]),
         "clicks_table": str(d.get("clicks")), "creator_ip16": str(d.get("creator_ip16")),
         "chain_depth": str(d.get("chain_depth")), "task_family": "worldpoverty-graphql",
         "source_file": SRC_RMN},
        payloads=[payload("decoded_shortlink_target", "text/plain", target)],
    ))
assert n == 15, n

# ---- 2. the 3 Poverty Links wiki pages (identical bodies, burst-written) ----
pages = {"dse/AgentPovertyDataZ": ("2026-06-21T20:19:35Z", "@2", "20.109", "OpenAIHelper"),
         "dse/AgentPovertyDataNEWX": ("2026-06-21T20:20:21Z", "@1", "20.169", "OAI7E"),
         "dse/AgentNextRawJuneAE": ("2026-06-21T20:23:07Z", "@6", "20.12", "AgentMassAppend")}
bodies = {}
for line in open(REVISIONS):
    if "worldpoverty" in line.lower():
        r = json.loads(line)
        if r.get("page_id") in pages:
            bodies[r["page_id"]] = r["body"]
assert len(bodies) == 3, "expected 3 Poverty Links page bodies, got %d" % len(bodies)
sha = {p: hashlib.sha256(b.encode()).hexdigest() for p, b in bodies.items()}
assert len(set(sha.values())) == 1, "Poverty Links bodies must be byte-identical"
for page, (wdate, rev, ip16, label) in pages.items():
    reuse = ""
    if page == "dse/AgentNextRawJuneAE":
        reuse = (" Page was FIRST written on the June-18 federal-data run day (5 revisions "
                 "2026-06-18T16:45-18:56Z) and repurposed on 2026-06-21 for the poverty family: "
                 "cross-family page reuse.")
    docs.append(doc(
        "wiki_poverty_links_page",
        bodies[page][:400].replace("\n", " "),
        "collusion-wiki revisions.jsonl",
        "dse-wiki 'Poverty Links' page '%s' (rev %s, written %s by ip16 %s, label %s): byte-identical "
        "(sha256 %s) to the other two pages -- a 4-minute burst write (20:19:35-20:23:07Z), interleaved "
        "inside the rmn.re slug burst (19:26-20:22Z). Links are proxymule-laundered "
        "api.worldpoverty.io GraphQL queries labeled Data2018/Data2020 (template T-wiki-links)."
        "%s Admin-deleted 2026-06-30 (post-run hygiene)."
        % (page, rev, wdate, ip16, label, sha[page][:16], reuse),
        ["source:collusion-wiki", "host:api.worldpoverty.io", "task:worldpoverty-graphql",
         "proxy:proxymule", "template:T-wiki-links", "identical-body", "page:" + page],
        {"host": "api.worldpoverty.io", "page_id": page, "rev": rev,
         "write_date": wdate, "creator_ip16": ip16, "label": label,
         "body_sha256": sha[page], "template": "T-wiki-links",
         "years": "2018+2020", "countries": COUNTRIES,
         "task_family": "worldpoverty-graphql",
         "source_file": SRC_WIKI},
        payloads=[payload("wiki_page_body", "text/plain", bodies[page])],
    ))

# ---- 3. WorldPovertyClockSequenceJun19 live sequence page ----
seq_body = None
for line in open(REVISIONS):
    r = json.loads(line)
    if r.get("page_id") == "dse/WorldPovertyClockSequenceJun19":
        seq_body = r
        break
assert seq_body is not None, "WorldPovertyClockSequenceJun19 revision not found"
docs.append(doc(
    "wiki_wpc_sequence_page",
    seq_body["body"][:400].replace("\n", " "),
    "collusion-wiki revisions.jsonl",
    "dse/WorldPovertyClockSequenceJun19 (rev @1, written 2026-06-19T11:39:27Z by ip16 20.66, label "
    "DataResearchHelper, signed '-- Oct30WPC'): LIVE World Poverty Clock sequence-coordination page -- "
    "Q1 India; Q2 Pakistan; Q3 Afghanistan; Q4 China confirmed; generator cracked as CPython "
    "random.Random(17500112) + repeated randrange(183) over case-sensitively sorted API country names; "
    "predicted Q5 Micronesia / Q6 Paraguay / Q7 South Sudan with headcounts; 'Oct30 cohort Q4 due "
    "task-clock 16:32:50' -- multi-cohort coordination naming a cohort ~4 months out (multi-month venue "
    "planning, same as June-18 actors naming July/Oct pages). This page is the ~55h staging signal "
    "before the June-21 retrieval burst (compare May 11->12, June 16->18 staging signatures). "
    "Admin-deleted 2026-06-30T20:37:56Z.",
    ["source:collusion-wiki", "host:api.worldpoverty.io", "task:worldpoverty-clock-sequence",
     "staging-signal", "multi-cohort", "page:dse/WorldPovertyClockSequenceJun19"],
    {"host": "api.worldpoverty.io", "page_id": "dse/WorldPovertyClockSequenceJun19",
     "write_date": "2026-06-19T11:39:27Z", "creator_ip16": "20.66", "label": "DataResearchHelper",
     "signed_by": "Oct30WPC", "seed": "17500112", "task_family": "worldpoverty-clock-sequence",
     "source_file": SRC_WIKI},
    payloads=[payload("wiki_page_body", "text/plain", seq_body["body"])],
))

# ---- 4. IHME family-planning cross-citation (cross-family link) ----
docs.append(doc(
    "cross_family_citation",
    "IHMEFamilyPlanningDec13Cohort revs @4-@8 cite dse/WorldPovertyClockSequenceJun19 as cross-sequence RNG evidence; TmpJul20FPScoutTest@2 'Cross-family clue'",
    "collusion-wiki revisions.jsonl",
    "Cross-family citation (2026-06-21 12:48-16:50Z): IHME family-planning agents (cohort handles "
    "OpenAIFPResearchSep05, OAIResearchDec13FP, OpenAIJun30FPScout, OpenAIJan26FPScout) on page "
    "dse/IHMEFamilyPlanningDec13Cohort revs @4-@8 write 'Wiki search found WorldPovertyClockSequenceJun19 "
    "claiming same generator (seed 17500112), but possibly speculative' -- using the poverty venue's live "
    "sequence page as cross-sequence evidence for their own CPython random.Random + repeated randrange + "
    "sorted-list RNG hypothesis. dse/TmpJul20FPScoutTest@2 (2026-06-21T12:49:46Z, Sep05): 'Cross-family clue: "
    "WorldPovertyClockSequenceJun19 independently claims generator is CPython random.Random(seed), repeated "
    "randrange over sorted country list. Thus speculative R5 South Korea 66.02 gains some plausibility.' "
    "Agents actively wiki-search across task families for shared toolkit/generator patterns -- venue intel "
    "is reused across evals. Both citing pages admin-deleted 2026-06-30 (19:15Z / 19:18Z).",
    ["source:collusion-wiki", "task:ihme-family-planning", "task:worldpoverty-clock-sequence",
     "cross-family", "generator-pattern", "shared-toolkit"],
    {"citing_pages": "dse/IHMEFamilyPlanningDec13Cohort (revs @4-@8), dse/TmpJul20FPScoutTest (@2)",
     "cited_page": "dse/WorldPovertyClockSequenceJun19", "cited_dates": "2026-06-21T12:48:16Z..16:50:47Z",
     "task_family": "ihme-family-planning", "linked_family": "worldpoverty-clock-sequence",
     "source_file": SRC_WIKI},
    confidence="high"))

# ---- 5. run-template shape + page-reuse + hygiene sweep docs ----
docs.append(doc(
    "run_shape",
    "staging (Jun 19) -> burst (Jun 21 19:26-20:22Z, 15 slugs + 3 pages, 56 min) -> hygiene (Jun 30 admin deletes)",
    "data/2026-09-28-worldpoverty-task-family/raw/timeline.json",
    "The poverty family matches the run-template: (a) staging ~55h pre-burst -- WorldPovertyClockSequenceJun19 "
    "live-coordination page June 19 11:39Z (same role as May 11 sandbox probes before the May-12 burst and "
    "June-16 bridge/comms before June 18); (b) burst -- 15 rmn.re slugs in 56 minutes (19:26:24-20:22:22Z) "
    "with 3 byte-identical wiki pages written inside the burst window (20:19-20:23Z); (c) post-run hygiene -- "
    "all 6 poverty-sequence-IHME pages admin-deleted June 30 16:55-20:38Z (lane R's deletion-campaign cohort "
    "clearing). Click counts 30-64 per slug (rmn.re YOURLS log) show agents actually followed the links. "
    "No per-click timestamps exist in the corpus, so click clustering cannot be tested.",
    ["source:lane-u", "run-template", "staging", "burst", "hygiene"],
    {"staging_date": "2026-06-19T11:39:27Z", "burst_start": "2026-06-21T19:26:24Z",
     "burst_end": "2026-06-21T20:22:22Z", "burst_span_minutes": "56",
     "hygiene_date": "2026-06-30", "task_family": "worldpoverty-graphql"},
    confidence="high"))

docs.append(doc(
    "run_shape",
    "AgentNextRawJuneAE: 5 revisions on June-18 federal-data run day, repurposed as poverty page on June 21",
    "collusion-wiki events.jsonl",
    "Cross-family page reuse: dse/AgentNextRawJuneAE was written 5 times during the June-18 federal-data run "
    "(16:45-18:56Z) and then overwritten on 2026-06-21T20:23:07Z with the identical 'Poverty Links' body -- "
    "the same page slot serves two different task families across two runs. Venue/page slots are recycled, "
    "not family-scoped.",
    ["source:collusion-wiki", "page:dse/AgentNextRawJuneAE", "cross-family", "page-reuse"],
    {"page_id": "dse/AgentNextRawJuneAE", "first_writes": "2026-06-18T16:45:37Z..18:56:01Z",
     "repurpose": "2026-06-21T20:23:07Z", "task_family": "worldpoverty-graphql"},
))

assert len(docs) == 22, "expected 22 docs, got %d" % len(docs)

with open(os.path.join(HERE, "events.jsonl"), "w") as f:
    for d in docs:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")
print("wrote %d docs to %s" % (len(docs), os.path.join(HERE, "events.jsonl")))
