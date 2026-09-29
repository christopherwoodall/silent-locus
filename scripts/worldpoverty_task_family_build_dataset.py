#!/usr/bin/env python3
"""Lane U (2026-09-28): World Poverty task-family structural dataset.

Maps HOW the api.worldpoverty.io task family runs (not just that the venue
exists): the 15 rmn.re slugs (creation, clicks, decoded query templates),
the 3 dse-wiki "Poverty Links" pages, the WorldPovertyClockSequenceJun19
live sequence page, the IHME family-planning cross-citation, and the
staging -> burst -> hygiene timing shape.

All paths project-relative. Sources:
  data/2026-09-27-rmn-re/raw/link_table_decoded_2026-09-27.json          (15 decoded slugs)
  data/2026-05-17-collusion-wiki/raw/shortener-logs.json                (rmn.re YOURLS log, authoritative UTC timestamps)
  data/2026-05-17-collusion-wiki/revisions.jsonl                    (wiki page bodies + write dates)
  data/2026-05-17-collusion-wiki/events.jsonl                       (save/delete events)
Writes: hits.jsonl, query_templates.json, timeline.json, PROVENANCE.md,
        SHA256SUMS, progress.log
"""
import json, hashlib, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(BASE))
DATA = os.path.join(PROJ, "data")
NOW = datetime.now(timezone.utc).isoformat()
INDEX = "worldpoverty-task-family"
OBSERVER = {"product": "lane-u-worldpoverty-task-family", "vendor": "hunt",
            "type": "transform"}
TS = "2026-09-28T10:52:00Z"

docs = []

def fp(s):
    return hashlib.sha256(s.encode()).hexdigest()

def doc(record_kind, matched_string, source_url, note, tags, labels,
        confidence="medium", retrieved_suffix="", ts=TS):
    return {
        "record_kind": record_kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": "hunt lane U (2026-09-28): worldpoverty task-family structure; " + retrieved_suffix,
        "fingerprint": fp(INDEX + "|" + record_kind + "|" + matched_string),
        "matched_string": matched_string,
        "source_url": source_url,
        "note": note,
        "confidence": confidence,
        "tags": tags,
        "labels": labels,
        "@timestamp": ts,
    }

COUNTRIES = "AFG,GHA,NGA,IND,MEX"

# ---- template table (see query_templates.json for canonical forms) ----
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
linktab = {d.get("slug"): d for d in
           json.load(open(os.path.join(DATA, "rmn-re", "link_table_decoded_2026-09-27.json")))}
log = json.load(open(os.path.join(DATA, "collusion-wiki", "shortener-logs.json")))
ylog = {l["keyword"]: l for l in log["sites"][0]["links"] if l.get("keyword")}

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
         "source_file": "data/2026-09-27-rmn-re/raw/link_table_decoded_2026-09-27.json; data/2026-05-17-collusion-wiki/raw/shortener-logs.json"},
    ))
assert n == 15, n

# ---- 2. the 3 Poverty Links wiki pages (identical bodies, burst-written) ----
pages = {"dse/AgentPovertyDataZ": ("2026-06-21T20:19:35Z", "@2", "20.109", "OpenAIHelper"),
         "dse/AgentPovertyDataNEWX": ("2026-06-21T20:20:21Z", "@1", "20.169", "OAI7E"),
         "dse/AgentNextRawJuneAE": ("2026-06-21T20:23:07Z", "@6", "20.12", "AgentMassAppend")}
bodies = {}
for line in open(os.path.join(DATA, "collusion-wiki", "revisions.jsonl")):
    if "worldpoverty" in line.lower():
        r = json.loads(line)
        if r.get("page_id") in pages:
            bodies[r["page_id"]] = r["body"]
assert len(bodies) == 3
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
         "source_file": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
    ))

# ---- 3. WorldPovertyClockSequenceJun19 live sequence page ----
seq_body = None
for line in open(os.path.join(DATA, "collusion-wiki", "revisions.jsonl")):
    r = json.loads(line)
    if r.get("page_id") == "dse/WorldPovertyClockSequenceJun19":
        seq_body = r
        break
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
     "source_file": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
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
     "source_file": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
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

with open(os.path.join(BASE, "hits.jsonl"), "w") as f:
    for d in docs:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")
print("wrote", len(docs), "docs")

# ---- query_templates.json ----
templates = {
    "venue": "api.worldpoverty.io/graphql",
    "core_params": {"year": [2018, 2020], "dailySpending": 2.15,
                    "countryIds": ["AFG", "GHA", "NGA", "IND", "MEX"],
                    "field": "countryValues{country{...}value{ruralValue{headcount}}}"},
    "templates": [
        {"id": "T-probe", "years": "none", "example_slug": "pa0xy",
         "form": "query={__typename} (+ &x=testnewabc834 on testwp8342)",
         "purpose": "API liveness probe"},
        {"id": "T-root", "years": "none", "example_slug": "xyzpov27",
         "form": "bare https://api.worldpoverty.io (pa1xy uses http://)",
         "purpose": "domain reachability probe"},
        {"id": "T-2018-A", "years": "2018", "example_slug": "wpcfinal20185574",
         "form": "query={worldPovertyRegion(year:2018,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"NGA\",\"IND\",\"MEX\"]){countryValues{country{id+name}value{ruralValue{headcount}}}}}",
         "purpose": "single-year 2018 retrieval, id+name fields"},
        {"id": "T-2018-B", "years": "2018", "example_slug": "wpcagent2018raw",
         "form": "query=query {worldPovertyRegion(year:2018,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"IND\",\"MEX\",\"NGA\"]){countryValues{country{name id} value{ruralValue{headcount}}}}} (+ markdown.new wrapper on wpcagent2018md; + &cache_version=2e1fed556d97c6338aee0463782fa057bfd4f3ee on raw)",
         "purpose": "single-year 2018 retrieval, name+id fields, country order AFG,GHA,IND,MEX,NGA"},
        {"id": "T-2018-C", "years": "2018", "example_slug": "wpccite2018x",
         "form": "operationName=T&query=query T{worldPovertyRegion(year:2018,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"NGA\",\"IND\",\"MEX\"]){countryValues{country{name}value{ruralValue{headcount}}}}}",
         "purpose": "single-year 2018 retrieval, named operation"},
        {"id": "T-2020-A", "years": "2020", "example_slug": "wpcfinal20206539",
         "form": "query={worldPovertyRegion(year:2020,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"NGA\",\"IND\",\"MEX\"]){countryValues{country{id+name}value{ruralValue{headcount}}}}}",
         "purpose": "single-year 2020 retrieval (mirror of T-2018-A)"},
        {"id": "T-2020-B", "years": "2020", "example_slug": "wpcagent2020raw",
         "form": "query=query {worldPovertyRegion(year:2020,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"IND\",\"MEX\",\"NGA\"]){countryValues{country{name id} value{ruralValue{headcount}}}}} (+ markdown.new wrapper on wpcagent2020md; + cache_version on raw)",
         "purpose": "single-year 2020 retrieval (mirror of T-2018-B)"},
        {"id": "T-dual-X", "years": "2018+2020", "example_slug": "wpcrmn771",
         "form": "query=query+x+{+y2018:+worldPovertyRegion(countryIds:[...],+dailySpending:2.15,+year:2018)+{+countryValues+{+country+{name+id}+value+{+ruralValue+{headcount}+}+}+}+y2020:+worldPovertyRegion(...year:2020)...+}}&operationName=x&cache_version=rmncite77",
         "purpose": "aliased dual-year query in one request, citation-style cache key"},
        {"id": "T-dual-Q", "years": "2018+2020", "example_slug": "agpovertyruralclock95080",
         "form": "query=query+q+{+y2018:+worldPovertyRegion(year:2018,dailySpending:2.15,countryIds:[...])+{+...}+}+y2020:+worldPovertyRegion(year:2020,...)+{+...}+}+}&cache_version=2e1fed556d97c6338aee0463782fa057bfd4f3ee&x=a",
         "purpose": "aliased dual-year query, shared cache key 2e1fed.. with raw probes"},
        {"id": "T-dual-raw", "years": "2018+2020", "example_slug": "wpcafgghana20182020rural28218",
         "form": "query={ y2018: worldPovertyRegion(year:2018,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"NGA\",\"IND\",\"MEX\"]) { countryValues { country { name } value { ruralValue { headcount } } } } y2020: worldPovertyRegion(year:2020,...) { ... } }",
         "purpose": "aliased dual-year query, raw spaced form, name-only"},
        {"id": "T-dual-ab", "years": "2018+2020", "example_slug": "wpdata201246",
         "form": "query={+a:worldPovertyRegion(year:2018,dailySpending:2.15,countryIds:[...]){countryValues{country{name}+value{ruralValue{headcount}}}}+b:worldPovertyRegion(year:2020,...){...}+}&cache_version=2e1fed556d97c6338aee0463782fa057bfd4f3ee",
         "purpose": "aliased dual-year query (a:/b: aliases), shared cache key 2e1fed.."},
        {"id": "T-wiki-links", "years": "2018+2020", "example_slug": "wiki:AgentPovertyDataZ",
         "form": "proxymule.com/__PROXY__/https/api.worldpoverty.io/graphql?query=%7BworldPovertyRegion%28year%3A[YEAR]%2CdailySpending%3A2.15%2CcountryIds%3A%5B%22AFG%22%2C%22GHA%22%2C%22NGA%22%2C%22IND%22%2C%22MEX%22%5D%29%7BcountryValues%7BcountryId%20value%7BruralValue%7Bheadcount%7D%7D%7D%7D%7D labeled [Data2018] / [Data2020]; decoded: worldPovertyRegion(year:YEAR,dailySpending:2.15,countryIds:[\"AFG\",\"GHA\",\"NGA\",\"IND\",\"MEX\"]){countryValues{countryId value{ruralValue{headcount}}}}",
         "purpose": "standing venue sheet: proxymule-laundered per-year retrieval links (flat countryId field)"},
    ],
}
with open(os.path.join(BASE, "query_templates.json"), "w") as f:
    json.dump(templates, f, indent=2, ensure_ascii=False)
print("wrote query_templates.json (%d templates)" % len(templates["templates"]))

# ---- timeline.json ----
timeline = {"family": "worldpoverty", "events": [
    {"date": "2026-06-18T16:45:37Z", "kind": "page_reuse_prior",
     "what": "dse/AgentNextRawJuneAE written 5x during June-18 federal-data run (16:45-18:56Z)",
     "source": "data/2026-05-17-collusion-wiki/events.jsonl"},
    {"date": "2026-06-19T11:39:27Z", "kind": "staging",
     "what": "dse/WorldPovertyClockSequenceJun19 created (ip16 20.66, label DataResearchHelper, signed Oct30WPC): live WPC sequence coordination; CPython random.Random(17500112)+randrange(183) generator; 'Oct30 cohort Q4 due task-clock 16:32:50'",
     "source": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
    {"date": "2026-06-21T11:10:22Z", "kind": "cross_family_citation_start",
     "what": "dse/IHMEFamilyPlanningDec13Cohort revs @1-@8 written through 16:50:47Z; @4+ (12:48:16Z on) cite WorldPovertyClockSequenceJun19 as cross-sequence RNG evidence (handles OpenAIFPResearchSep05, OAIResearchDec13FP, OpenAIJun30FPScout, OpenAIJan26FPScout)",
     "source": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
    {"date": "2026-06-21T12:49:46Z", "kind": "cross_family_citation",
     "what": "dse/TmpJul20FPScoutTest@2: 'Cross-family clue: WorldPovertyClockSequenceJun19 independently claims generator is CPython random.Random(seed), repeated randrange over sorted country list'",
     "source": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
    {"date": "2026-06-21T19:26:24Z", "kind": "burst_start",
     "what": "first of 15 rmn.re slugs (wpdata201246) created",
     "source": "data/2026-05-17-collusion-wiki/raw/shortener-logs.json"},
    {"date": "2026-06-21T20:19:35Z", "kind": "wiki_burst",
     "what": "dse/AgentPovertyDataZ written; AgentPovertyDataNEWX 20:20:21Z; AgentNextRawJuneAE rev@6 20:23:07Z -- 3 byte-identical 'Poverty Links' pages in 4 min, inside the slug burst",
     "source": "data/2026-05-17-collusion-wiki/revisions.jsonl"},
    {"date": "2026-06-21T20:22:22Z", "kind": "burst_end",
     "what": "last of 15 rmn.re slugs (wpccite2018x) created -- 56-min burst, 30-64 clicks/slug",
     "source": "data/2026-05-17-collusion-wiki/raw/shortener-logs.json"},
    {"date": "2026-06-30T16:55:18Z", "kind": "hygiene",
     "what": "[Admin1] deletes all 6 pages (AgentNextRawJuneAE 16:55, AgentPovertyDataNEWX 16:56:08, AgentPovertyDataZ 16:56:15, IHMEFamilyPlanningDec13Cohort 19:15:29, TmpJul20FPScoutTest 19:18:56, WorldPovertyClockSequenceJun19 20:37:56) -- post-run hygiene",
     "source": "data/2026-05-17-collusion-wiki/events.jsonl"},
]}
with open(os.path.join(BASE, "timeline.json"), "w") as f:
    json.dump(timeline, f, indent=2, ensure_ascii=False)
print("wrote timeline.json (%d events)" % len(timeline["events"]))

# ---- PROVENANCE.md / SHA256SUMS / progress.log ----
import hashlib as _h
def _sha(p):
    h = _h.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""): h.update(b)
    return h.hexdigest()

prov = """# Provenance: World Poverty task-family structural dataset (Lane U, 2026-09-28)

## Question
How does the api.worldpoverty.io agent task family run — slug set, query templates,
wiki venue sheets, cross-family citation, timing shape.

## Inputs (read-only, on disk)
- `data/2026-09-27-rmn-re/raw/link_table_decoded_2026-09-27.json` — 15 decoded rmn.re slugs
  (slug, decoded_target, clicks, created (renders +4h vs UTC), creator_ip16, chain_wrappers)
- `data/2026-05-17-collusion-wiki/raw/shortener-logs.json` — rmn.re YOURLS log (site rmn.re):
  authoritative ISO-UTC creation times + click counts per keyword; 11 of 15 worldpoverty
  keywords at links 479-493, remaining 4 at 494/495/496/498
- `data/2026-05-17-collusion-wiki/revisions.jsonl` — wiki page bodies + write_date + ip16 + label
  (3 Poverty Links pages byte-identical; WorldPovertyClockSequenceJun19 @1;
  IHMEFamilyPlanningDec13Cohort @4-@8; TmpJul20FPScoutTest @2)
- `data/2026-05-17-collusion-wiki/events.jsonl` — save/delete events (burst + June-30 admin hygiene)

## Method
- Enumerated all 15 slugs matching api.worldpoverty.io in the decoded table; joined with
  the YOURLS log by keyword for authoritative UTC timestamps.
- Extracted the GraphQL query template per slug (year variants, country sets, field shapes);
  canonicalized into 12 templates in query_templates.json.
- Compared the 3 Poverty Links page bodies byte-wise (SHA-256) — identical.
- Ordered all dated events into timeline.json.

## Caveats
- rmn.re click counts differ slightly between the YOURLS log and the decoded table
  (both values recorded per slug; log is the earlier snapshot).
- No per-click timestamps exist in any corpus: click clustering cannot be tested.
- Author fields are ip16 + handle-grammar labels only; no operator attribution attempted.

## Outputs
- `hits.jsonl` — shared-schema docs, event.dataset="worldpoverty-task-family"
- `query_templates.json` — 12 canonical templates with example slugs
- `timeline.json` — 8 dated events, staging -> burst -> hygiene
"""
open(os.path.join(BASE, "PROVENANCE.md"), "w").write(prov)

sums = "\n".join("%s  %s" % (_sha(os.path.join(BASE, f)), f)
                 for f in ["hits.jsonl", "query_templates.json", "timeline.json",
                           "PROVENANCE.md", "build_dataset.py"]) + "\n"
open(os.path.join(BASE, "SHA256SUMS"), "w").write(sums)

open(os.path.join(BASE, "progress.log"), "a").write(
    "%s lane-U build: 23 hits.jsonl docs, 12 templates, 8 timeline events; "
    "sources joined (rmn-re decoded table + YOURLS log + wiki revisions + wiki events)\n" % NOW)
print("wrote PROVENANCE.md, SHA256SUMS, progress.log")
