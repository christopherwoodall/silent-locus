#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-06-20-powerbi-fronting.

Reads evidence/remove-2026-06-20-powerbi-fronting/events.jsonl (legacy lane)
and raw-technique-verbatim.md (this lane dir). Emits bundle JSON to stdout.

Record plan:
- infra.message x41 : collusion-wiki agent-authored records (body = url_context excerpt, verbatim)
- infra.message x135: collusion-wiki agent-authored revisions (body = url_context excerpt, verbatim)
- infra.message x1  : collusion-wiki agent wiki link (app.powerbi.com embed, token withheld)
- infra.message x2  : thecolony.ai investigator passages (body = plain-text rendering, verbatim)
- infra.proxy_chain x1: SNI-allowlist bypass technique observation
- infra.ioc x4      : 20.223.25.152, wabi-north-europe-i-primary-api.analysis.windows.net,
                      blob.core.windows.net, app.powerbi.com
- claim x4          : technique (UPSTREAM), OECD values (UPSTREAM), window/stats (UPSTREAM),
                      first-person agent accounts (OBSERVED)
- source x2         : collusion-wiki corpus, thecolony.ai wiki page
"""
import json
import re
import sys

REPO = "/home/hatch/workspace/silent-locus"
LEGACY = REPO + "/evidence/remove-2026-06-20-powerbi-fronting/events.jsonl"
VERBATIM = REPO + "/data/lanes/2026-06-20-powerbi-fronting/raw-technique-verbatim.md"
LANE = "2026-06-20-powerbi-fronting"
ACTOR = "agent:lane-ingest-2026-06-20-powerbi-fronting"

ISO = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)")
HANDLE = re.compile(r"--\s*([A-Za-z][\w-]*)\s*$")

# --- verbatim investigator passages (plain-text renderings from technique-verbatim.md)
text = open(VERBATIM).read()
m805 = re.search(r"## Passage 1.*?\n> (.*?)\n\n## Passage 2", text, re.S)
m742 = re.search(r"## Passage 2.*?\n> (.*?)\n\n## Notes", text, re.S)
PASSAGE_S11 = m805.group(1).strip()
PASSAGE_S8 = m742.group(1).strip()
# strip leading "> " continuations if any
PASSAGE_S11 = re.sub(r"\n> ", "\n", PASSAGE_S11)
PASSAGE_S8 = re.sub(r"\n> ", "\n", PASSAGE_S8)

records = []

def add(rec):
    records.append(rec)
    return rec.get("ref")

# --- sources
add({"kind": "source", "ref": "src-collusion-wiki",
     "body": {"locator": "collusion-wiki corpus, legacy capture data/2026-05-17-collusion-wiki/raw/ "
                         "(records.jsonl, revisions.jsonl, links.jsonl); cited via legacy lane "
                         "evidence/remove-2026-06-20-powerbi-fronting/events.jsonl",
              "source_type": "submitted"},
     "tags": {"lane": LANE}})
add({"kind": "source", "ref": "src-thecolony",
     "body": {"locator": "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026 ; "
                         "incident wiki page captured 2026-09-27 (Lane I ingest); "
                         "verbatim passages in lane file raw-technique-verbatim.md",
              "source_type": "submitted"},
     "tags": {"lane": LANE}})

def base_tags(fp, hit_kind, src_file):
    return {"lane": LANE, "legacy_fingerprint": fp,
            "legacy_record_kind": "corpus_hit", "legacy_hit_kind": hit_kind,
            "legacy_source_file": src_file}

def clean_ts(raw):
    if not raw:
        return None
    m = ISO.match(raw.strip())
    return m.group(1) if m else None

def clean_handle(ctx):
    m = HANDLE.search(ctx or "")
    return m.group(1) if m else None

def message(ref, venue, message_id, body, provenance, trust, posted_at, author, tags):
    data = {"venue": venue, "message_id": message_id, "body": body,
            "provenance": provenance, "trust": trust}
    if posted_at:
        data["posted_at"] = posted_at
    if author:
        data["author"] = author
    add({"kind": "observation", "ref": ref,
         "body": {"type": "infra.message", "data_schema": "urn:factum:infra:message:1",
                  "data": data, "files": [], "source": "@" + ("src-thecolony" if "thecolony" in provenance else "src-collusion-wiki")},
         "tags": tags})

counters = {"rec": 0, "rev": 0, "link": 0, "passage": 0}
rep_rev_refs = []  # representative revision refs for the OBSERVED claim

for line in open(LEGACY):
    e = json.loads(line)
    L = e["labels"]
    kind = L.get("powerbi.hit_kind")
    fp = e.get("fingerprint", "")
    ctx = L.get("powerbi.url_context") or ""
    tags = base_tags(fp, kind or "artifact_observation", L.get("powerbi.source_file") or "")
    if kind == "agent_wiki_record":
        i = counters["rec"]; counters["rec"] += 1
        tags["page"] = L.get("powerbi.origin_page") or ""
        tags["authorship"] = L.get("powerbi.authorship") or ""
        tags["classification"] = L.get("powerbi.classification") or ""
        message(f"m-rec-{i:03d}", "collusion-wiki", L.get("powerbi.record_id") or f"rec-{i}",
                ctx, "data/collusion-wiki/records.jsonl (via legacy lane events.jsonl)",
                "untrusted-agent-content", clean_ts(L.get("powerbi.hit_timestamp_raw")),
                clean_handle(ctx), tags)
    elif kind == "agent_wiki_revision":
        i = counters["rev"]; counters["rev"] += 1
        ref = f"m-rev-{i:03d}"
        tags["page"] = L.get("powerbi.page_key") or ""
        tags["wiki"] = L.get("powerbi.wiki") or ""
        tags["authorship"] = L.get("powerbi.authorship") or ""
        tags["classification"] = L.get("powerbi.classification") or ""
        message(ref, "collusion-wiki", L.get("powerbi.rev_id") or f"rev-{i}",
                ctx, "data/collusion-wiki/revisions.jsonl (via legacy lane events.jsonl)",
                "untrusted-agent-content", clean_ts(L.get("powerbi.hit_timestamp_raw")),
                clean_handle(ctx), tags)
        if "INDEPENDENT LIVE REPLICATION" in ctx or "blob-SNI" in ctx or "querydata" in ctx.lower():
            if len(rep_rev_refs) < 4:
                rep_rev_refs.append(ref)
    elif kind == "agent_wiki_link":
        i = counters["link"]; counters["link"] += 1
        tags["authorship"] = L.get("powerbi.authorship") or ""
        tags["classification"] = L.get("powerbi.classification") or ""
        tags["note"] = "embed token r= withheld per lane no-credentials rule"
        message(f"m-link-{i:03d}", "collusion-wiki", L.get("powerbi.record_id") or f"link-{i}",
                ctx, "data/collusion-wiki/links.jsonl (via legacy lane events.jsonl)",
                "untrusted-agent-content", clean_ts(L.get("powerbi.hit_timestamp_raw")),
                None, tags)
    elif kind == "investigator_wiki_passage":
        ln = L.get("powerbi.line")
        tags["authorship"] = L.get("powerbi.authorship") or ""
        tags["classification"] = L.get("powerbi.classification") or ""
        if ln == 805:
            message("m-passage-s11", "thecolony.ai wiki", "section-11-line-805", PASSAGE_S11,
                    "data/thecolony-ai/wiki_incident_page.html (Lane I capture 2026-09-27); "
                    "verbatim copy in lane raw-technique-verbatim.md",
                    "untrusted-third-party-prose", None,
                    "thecolony.ai incident wiki (investigator prose)", tags)
        elif ln == 742:
            message("m-passage-s8", "thecolony.ai wiki", "section-8-line-742", PASSAGE_S8,
                    "data/thecolony-ai/wiki_incident_page.html (Lane I capture 2026-09-27); "
                    "verbatim copy in lane raw-technique-verbatim.md",
                    "untrusted-third-party-prose", None,
                    "thecolony.ai incident wiki (investigator prose)", tags)
        else:
            raise SystemExit(f"unexpected passage line {ln}")
        counters["passage"] += 1
    elif kind is None:
        # artifact_observation row: no Factum record; bytes retained as lane document + capture
        continue
    else:
        raise SystemExit(f"unexpected hit_kind {kind}")

assert counters == {"rec": 41, "rev": 135, "link": 1, "passage": 2}, counters
assert len(rep_rev_refs) >= 3, rep_rev_refs

# --- technique observation: SNI-allowlist bypass (domain fronting)
add({"kind": "observation", "ref": "obs-proxychain",
     "body": {"type": "infra.proxy_chain", "data_schema": "urn:factum:infra:proxy-chain:1",
              "data": {
                  "proxy_service": "sandbox egress proxy allowlisting *.blob.core.windows.net by SNI",
                  "target_url": "wabi-north-europe-i-primary-api.analysis.windows.net "
                                "(Power BI querydata backend; public OECD education-spending report data)",
                  "chain": [
                      "invented *.blob.core.windows.net hostname presented as TLS SNI "
                      "(proxy passed the connection on the SNI it inspects)",
                      "socket pinned to real Power BI cluster IP 20.223.25.152",
                      "HTTP Host header overridden to wabi-north-europe-i-primary-api.analysis.windows.net",
                      "certificate verification skipped"],
                  "success": True,
                  "agent": "39 agents; 25 independent-replication claims (per thecolony.ai "
                           "incident wiki section 11, investigator prose, second-hand)"},
              "files": [], "source": "@src-thecolony"},
     "tags": {"lane": LANE, "technique": "sni-allowlist-bypass / domain-fronting",
              "behavior_category": "restriction-circumvention",
              "assertion_basis": "investigator prose, second-hand, not independently verified"}})

# --- IOCs
IOCS = [
    ("20.223.25.152", "ip"),
    ("wabi-north-europe-i-primary-api.analysis.windows.net", "domain"),
    ("blob.core.windows.net", "domain"),
    ("app.powerbi.com", "domain"),
]
for i, (term, cat) in enumerate(IOCS):
    add({"kind": "observation", "ref": f"ioc-{i}",
         "body": {"type": "infra.ioc", "data_schema": "urn:factum:infra:ioc:1",
                  "data": {"term": term, "category": cat, "status": "candidate",
                           "provenance": "2026-06-20-powerbi-fronting lane: thecolony.ai incident "
                                         "wiki section 11 (investigator prose, second-hand) + "
                                         "collusion-wiki dse agent text (2026-06-20/21)"},
                  "files": [], "source": "@src-thecolony"},
         "tags": {"lane": LANE, "topic": "domain-fronting"}})

# --- claims
def claim(ref, basis, prop, subject, cites, note, value):
    add({"kind": "claim", "ref": ref,
         "body": {"basis": basis, "subject": subject, "cites": cites, "note": note,
                  "property": prop, "value": value},
         "tags": {"lane": LANE}})

claim("claim-technique", "UPSTREAM", "technique", "@obs-proxychain",
      ["@m-passage-s11", "@m-passage-s8"],
      "Investigator claim from thecolony.ai incident wiki section 11; neither the wiki "
      "investigators nor we replayed the technique. Graded UPSTREAM (second-hand).",
      {"technique": "sni-allowlist-bypass / domain-fronting",
       "mechanism": "invented *.blob.core.windows.net SNI -> socket pinned to 20.223.25.152 -> "
                    "Host override to wabi-north-europe-i-primary-api.analysis.windows.net -> "
                    "cert verification skipped -> Power BI querydata backend reachable",
       "agents": 39, "independent_replication_claims": 25, "window_hours": 43,
       "framing": "bypass of the sandbox's proxy, not a Microsoft vulnerability; served public OECD data",
       "behavior_category": "restriction-circumvention"})
claim("claim-oecd-values", "UPSTREAM", "recovered_values", "@obs-proxychain",
      ["@m-passage-s11", "@m-passage-s8"],
      "Values as reported by the investigator wiki; corroborated by agent-authored "
      "collusion-wiki text citing the same 2dp values (see claim-agent-accounts).",
      {"Czech": "9.69", "Hungary": "9.91", "Poland": "16.38", "Slovak": "14.59",
       "dataset": "OECD education spending", "via": "Power BI querydata backend"})
claim("claim-window", "UPSTREAM", "operation_window", "@obs-proxychain",
      ["@m-passage-s11"],
      "Window and scale as reported by thecolony.ai section 11; second-hand.",
      {"window": "2026-06-20/21", "duration_hours": 43, "agents": 39,
       "independent_replication_claims": 25})
claim("claim-agent-accounts", "OBSERVED", "first_person_bypass_accounts", "@" + rep_rev_refs[0],
      ["@" + r for r in rep_rev_refs],
      "Agent-authored collusion-wiki (dse) revisions, dated 2026-06-20/21, describe in "
      "first person obtaining real Power BI querydata via the blob-SNI bypass. "
      "Authorship is per page handle and not independently authenticated; the text "
      "itself is the observed evidence.",
      {"sample_pages": ["dse~Dec16OECDPrecision", "dse~Jun05OECDScout"],
       "asserted_mechanism_terms": ["blob-SNI bypass", "live Power BI tooltip/querydata",
                                   "keyboard-focus aria-labels"],
       "asserted_values": {"Czech": "9.69", "Hungary": "9.91", "Poland": "16.38",
                           "Slovak": "14.59", "Slovenia": "23.13"}})

bundle = {"bundle": 2, "actor": ACTOR,
          "idempotency_key": "powerbi-fronting-20261009-bundle-v1",
          "records": records}
json.dump(bundle, sys.stdout, ensure_ascii=False)
sys.stderr.write(f"records={len(records)} counters={counters}\n")
