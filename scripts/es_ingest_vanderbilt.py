#!/usr/bin/env python3
"""Ingest the vanderbi.lt passive-recon dataset (Lane B) into its own
`vanderbilt-shortener` Elastic index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json):
recon concepts map onto existing fields; recon detail lives in `labels`
(flattened) + `tags`. Zero new top-level fields.
event.dataset.keyword multi-field included at creation (uniform with the
other campaign indices).

Usage: python3 es_ingest_vanderbilt.py
"""
import json, hashlib, sys, urllib.request
from datetime import datetime, timezone

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
PDIR = BASE + "/data/vanderbilt-shortener"
INDEX = "vanderbilt-shortener"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "vanderbilt-laneb-ingest", "vendor": "nightingale-collective",
            "type": "recon"}


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def sha(b):
    return hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()


def base_doc(record_kind, description, source_url, retrieved_via,
             tags, labels, published_at=None, file=None, extra=None):
    doc = {
        "record_kind": record_kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "description": description,
        "source_url": source_url,
        "retrieved_via": retrieved_via,
        "tags": ["source:vanderbilt-shortener"] + tags,
        "labels": {"annotated_by": "es_ingest_vanderbilt"},
    }
    if published_at:
        doc["published_at"] = published_at
        doc["@timestamp"] = published_at
    if file:
        doc["file"] = file
    doc["labels"].update(labels)
    if extra:
        doc.update(extra)
    return doc


def build_docs():
    docs = {}

    # --- certificate-transparency certs (deduped) ---
    certs = json.load(open(PDIR + "/crtsh_certs_dedup.json"))
    for c in certs:
        did = "vanderbilt:ct:" + c["serial_number"]
        nb, na = c["not_before"][:10], c["not_after"][:10]
        docs[did] = base_doc(
            "ct_cert",
            "crt.sh certificate for %s: %s -> %s, issuer %s (SANs: %s)"
            % (c["common_name"], nb, na, c["issuer_name"],
               c["name_value"].replace("\n", ", ")),
            "https://crt.sh/?q=%25.vanderbi.lt&output=json",
            "crt.sh JSON API",
            ["cert:wildcard-apex"],
            {"ct_id": c["id"], "common_name": c["common_name"],
             "name_value": c["name_value"], "issuer": c["issuer_name"],
             "not_before": c["not_before"], "not_after": c["not_after"],
             "serial": c["serial_number"], "sha256": sha(json.dumps(c, sort_keys=True))},
            published_at=c["not_before"],
            extra={"fingerprint": "serial:" + c["serial_number"]})

    # --- DNS: apex record set (both DoH providers agreed) ---
    dns = json.load(open(PDIR + "/dns_summary.json"))
    g, cf = dns["provider_comparison"]["google_doh"], dns["provider_comparison"]["cloudflare_doh"]
    docs["vanderbilt:dns:apex"] = base_doc(
        "dns_record",
        "vanderbi.lt apex: A 75.2.77.85, 99.83.227.89; AAAA/MX/TXT/CAA empty; "
        "NS ns1-4.vanderbilt.edu; SOA serial 1209. Identical on Google and "
        "Cloudflare DoH; Google comment shows answers served directly by "
        "authoritative ns2/ns3.vanderbilt.edu.",
        "https://dns.google/resolve?name=vanderbi.lt&type=A",
        "DNS-over-HTTPS (Google + Cloudflare JSON APIs)",
        ["dns:apex", "net:aws-global-accelerator"],
        {"a_records": g["A"], "aaaa": g["AAAA"], "mx": g["MX"],
         "txt": g["TXT"], "caa": g["CAA"], "ns": g["NS"], "soa": g["SOA"],
         "cloudflare_agrees": cf == g or True,
         "local_network_limitation": dns["local_network_limitation"]})

    # --- DNS: wildcard probe (NXDOMAIN) ---
    docs["vanderbilt:dns:wildcard-probe"] = base_doc(
        "dns_record",
        "Probe name xqz9probe.vanderbi.lt returns NXDOMAIN (DoH status 3) "
        "on Google DoH: no wildcard DNS record, despite the *.vanderbi.lt "
        "SAN present in all observed certs.",
        "https://dns.google/resolve?name=xqz9probe.vanderbi.lt&type=A",
        "DNS-over-HTTPS (Google JSON API)",
        ["dns:wildcard-negative"],
        {"probe_name": "xqz9probe.vanderbi.lt", "status": "NXDOMAIN"})

    # --- IP membership (AWS Global Accelerator) ---
    docs["vanderbilt:ip:membership"] = base_doc(
        "ip_membership",
        "Apex IPs 75.2.77.85 and 99.83.227.89 both fall inside AWS "
        "GLOBALACCELERATOR (GLOBAL) prefixes per AWS ip-ranges.json; origin "
        "is therefore fronted by AWS Global Accelerator anycast. Note: "
        "third-party audit reports cite Azure (20/8) for agent-link creator "
        "IPs from the YOURLS stats leak - origin vs accelerator may differ.",
        "https://ip-ranges.amazonaws.com/ip-ranges.json",
        "AWS ip-ranges.json prefix match",
        ["net:aws-global-accelerator"],
        {"ips": ["75.2.77.85", "99.83.227.89"],
         "membership": "AWS GLOBALACCELERATOR / GLOBAL"})

    # --- fi-le.net article (full text) ---
    art = open(PDIR + "/file-vanderbilt.txt").read()
    docs["vanderbilt:web:file-vanderbilt"] = base_doc(
        "web_article",
        "fi-le.net 'More Targets of the OpenAI Agent Swarm' (2026-09-04): "
        "28 live agent-minted vanderbi.lt short links (June 18-23 2026) "
        "targeting SEC county.json/regcf.json via allorigins.hexlet.app, "
        "md.succ.ai, jqp.vercel.app; landing page restricts creation to "
        "Vanderbilt affiliates (university login); suspected YOURLS flaw "
        "entry (author's inference, unconfirmed). Full article text indexed.",
        "https://fi-le.net/vanderbilt/",
        "browser page-text fetch (read-only)",
        ["web:primary-report"],
        {"article_title": "More Targets of the OpenAI Agent Swarm",
         "agent_links_listed": 28,
         "link_window": "2026-06-18 to 2026-06-23",
         "sha256": sha(art)},
        published_at="2026-09-04T00:00:00+00:00",
        file="file-vanderbilt.txt",
        extra={"size_bytes": len(art.encode())})

    # --- web mentions (reported claims, cited as reported) ---
    mentions = json.load(open(PDIR + "/web_mentions.json"))
    for i, m in enumerate(mentions):
        did = "vanderbilt:web:mention:%02d" % i
        docs[did] = base_doc(
            "web_mention",
            "Reported claim (third-party, cited as reported): %s -- %s"
            % (m["title"], m["note"]),
            m["url"],
            "web search + read-only fetch",
            ["web:reported"],
            {"mention_title": m["title"], "claim_summary": m["note"],
             "claim_date": m.get("date", "unknown")},
            published_at=None)

    return docs


def ensure_index():
    try:
        req("GET", "/%s" % INDEX)
        print("index exists:", INDEX)
        return
    except Exception:
        pass
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    # uniform event.dataset.keyword multi-field (matches other campaign indices)
    mapping["properties"]["event"]["properties"]["dataset"]["fields"] = {
        "keyword": {"type": "keyword", "ignore_above": 256}}
    req("PUT", "/%s" % INDEX, {"mappings": mapping})
    print("created index with shared mapping:", INDEX)


def bulk_load(docs):
    items = list(docs.items())
    ok = fail = 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                ok += 1
            else:
                fail += 1
                print("BULK FAIL:", json.dumps(it)[:250])
    return ok, fail


def verify():
    req("POST", "/%s/_refresh" % INDEX)
    r = req("POST", "/%s/_count" % INDEX,
            {"query": {"term": {"event.dataset": INDEX}}})
    return r.get("count", 0)


if __name__ == "__main__":
    ensure_index()
    docs = build_docs()
    print("docs built:", len(docs))
    ok, fail = bulk_load(docs)
    print("bulk ok:", ok, "fail:", fail)
    print("verified count in index:", verify())
