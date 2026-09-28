#!/usr/bin/env python3
"""Build Kibana dashboards for the `collusion-wiki` index (classic aggs-based
visualizations, shared-schema fields only). Idempotent: fixed saved-object IDs.

Dashboards:
  collusion-wiki-activity    - revisions/events over time, top agent labels
  collusion-wiki-grammars    - zz / epoch10 / oai / 999 name-grammar breakdown
  collusion-wiki-laundering  - proxy families, top link hosts, shortener targets
  collusion-wiki-gem-bridge  - the 79-gem wiki<->RubyGems bridge view

Usage: python3 build_wiki_dashboards.py [--verify]
"""
import sys, json, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

KB = "https://agent-apocalypse-f1f7ba.kb.us-east-1.aws.elastic.cloud"
HOSTS = ["agent-apocalypse-f1f7ba.kb.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
TIME_FROM = "2026-05-01T00:00:00.000Z"
TIME_TO = "2026-07-20T00:00:00.000Z"


def req(method, path, body=None):
    r = urllib.request.Request(KB + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method)
    r.add_header("Content-Type", "application/json")
    r.add_header("kbn-xsrf", "true")
    r.add_header("x-elastic-internal-origin", "kibana")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return read_json_response(resp)
    except urllib.error.HTTPError as e:
        print("HTTP %d %s %s: %s" % (e.code, method, path, e.read().decode()[:400]))
        raise


def data_view_id():
    found = req("GET", "/api/data_views")
    for dv in found.get("data_view", []):
        if dv.get("title") == "collusion-wiki*":
            print("data view exists:", dv["id"])
            return dv["id"]
    dv = req("POST", "/api/data_views/data_view",
             {"data_view": {"name": "collusion-wiki", "title": "collusion-wiki*",
                            "timeFieldName": "@timestamp"}})
    dv_id = dv.get("id") or dv.get("data_view", {}).get("id")
    print("created data view:", dv_id)
    return dv_id


def search_source(query):
    return {
        "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
        "query": {"query": query, "language": "kuery"},
        "filter": [],
    }


def date_hist(interval="auto"):
    return {"id": "2", "enabled": True, "type": "date_histogram", "schema": "segment",
            "params": {"field": "@timestamp",
                       "timeRange": {"from": TIME_FROM, "to": TIME_TO},
                       "useNormalizedEsInterval": True, "scaleMetricValues": False,
                       "interval": interval, "drop_partials": False,
                       "min_doc_count": 1, "extended_bounds": {}}}


def terms_agg(aid, field, size=15, schema="group", include=None):
    p = {"field": field, "size": size, "order": "desc", "orderBy": "1",
         "otherBucket": False, "otherBucketLabel": "Other",
         "missingBucket": False, "missingBucketLabel": "Missing"}
    if include:
        p["include"] = include
    return {"id": aid, "enabled": True, "type": "terms", "schema": schema, "params": p}


COUNT = {"id": "1", "enabled": True, "type": "count", "schema": "metric", "params": {}}


def hist_vis(title, split_field, split_include=None, split_size=10):
    aggs = [dict(COUNT), date_hist()]
    aggs.append(terms_agg("3", split_field, split_size, "group", split_include))
    return {
        "title": title, "type": "histogram",
        "params": {
            "type": "histogram", "grid": {"categoryLines": False, "style": {"color": "#eee"}},
            "categoryAxes": [{"id": "CategoryAxis-1", "type": "category", "position": "bottom",
                              "show": True, "style": {}, "scale": {"type": "linear"},
                              "labels": {"show": True, "filter": False, "truncate": 100}, "title": {}}],
            "valueAxes": [{"id": "ValueAxis-1", "name": "LeftAxis-1", "type": "value",
                           "position": "left", "show": True, "style": {},
                           "scale": {"type": "linear", "mode": "normal"},
                           "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                           "title": {"text": "Count"}}],
            "seriesParams": [{"show": True, "type": "histogram", "mode": "stacked",
                              "data": {"label": "Count", "id": "1"}, "valueAxis": "ValueAxis-1",
                              "drawLinesBetweenPoints": True, "lineWidth": 2, "showCircles": False}],
            "addTooltip": True, "addLegend": True, "legendPosition": "right",
            "addTimeMarker": False, "labels": {},
            "thresholdLine": {"show": False, "value": 10, "width": 1, "style": "full", "color": "#E7664C"},
        },
        "aggs": aggs,
    }


def bar_vis(title, field, size=20, include=None):
    return {
        "title": title, "type": "histogram",
        "params": {
            "type": "histogram", "grid": {"categoryLines": True},
            "categoryAxes": [{"id": "CategoryAxis-1", "type": "category", "position": "bottom",
                              "show": True, "scale": {"type": "linear"},
                              "labels": {"show": True, "rotate": 45, "filter": False, "truncate": 30},
                              "title": {}}],
            "valueAxes": [{"id": "ValueAxis-1", "name": "LeftAxis-1", "type": "value",
                           "position": "left", "show": True,
                           "scale": {"type": "linear", "mode": "normal"},
                           "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                           "title": {"text": "Count"}}],
            "seriesParams": [{"show": "true", "type": "histogram", "mode": "stacked",
                              "data": {"label": "Count", "id": "1"}, "valueAxis": "ValueAxis-1",
                              "drawLinesBetweenPoints": True, "showCircles": True}],
            "addTooltip": True, "addLegend": False, "legendPosition": "right",
        },
        "aggs": [dict(COUNT), terms_agg("2", field, size, "segment", include)],
    }


def table_vis(title, field, size=25, second_field=None):
    aggs = [dict(COUNT), terms_agg("2", field, size, "bucket")]
    if second_field:
        aggs.append(terms_agg("3", second_field, 5, "bucket"))
    return {
        "title": title, "type": "table",
        "params": {"perPage": 10, "showPartialRows": False, "showMetricsAtAllLevels": False,
                   "showTotal": False, "totalFunc": "sum", "percentageCol": ""},
        "aggs": aggs,
    }


def metric_vis(title):
    return {
        "title": title, "type": "metric",
        "params": {"addTooltip": True, "addLegend": False, "type": "metric",
                   "metric": {"percentageMode": False, "useRanges": False,
                              "colorSchema": "Green to Red", "metricColorMode": "None",
                              "colorsRange": [{"from": 0, "to": 100000}],
                              "labels": {"show": True}, "invertColors": False,
                              "style": {"bgFill": "#000", "bgColor": False, "labelColor": False,
                                        "subText": "", "fontSize": 60}}},
        "aggs": [dict(COUNT)],
    }


def markdown_vis(title, md):
    return {"title": title, "type": "markdown",
            "params": {"fontSize": 12, "markdown": md}}


def make_viz(dv_id, viz_id, vis_state, query="*"):
    body = {
        "attributes": {
            "title": vis_state["title"],
            "description": "",
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "version": 1,
            "kibanaSavedObjectMeta": {"searchSourceJSON": json.dumps(search_source(query))},
        },
        "references": [{"name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                        "type": "index-pattern", "id": dv_id}],
    }
    r = req("POST", "/api/saved_objects/visualization/%s?overwrite=true" % viz_id, body)
    return r["id"]


def make_dashboard(dash_id, title, description, panels):
    panels_json, refs = [], []
    for i, (viz_id, w, h, x, y) in enumerate(panels):
        name = "panel_%d" % i
        panels_json.append({
            "version": "9.0.0", "type": "visualization",
            "gridData": {"x": x, "y": y, "w": w, "h": h, "i": name},
            "panelIndex": name, "embeddableConfig": {"enhancements": {}},
            "panelRefName": name,
        })
        refs.append({"name": name, "type": "visualization", "id": viz_id})
    body = {
        "attributes": {
            "title": title, "description": description,
            "panelsJSON": json.dumps(panels_json),
            "optionsJSON": json.dumps({"hidePanelTitles": False, "useMargins": True}),
            "version": 1, "timeRestore": True,
            "timeFrom": TIME_FROM, "timeTo": TIME_TO,
        },
        "references": refs,
    }
    r = req("POST", "/api/saved_objects/dashboard/%s?overwrite=true" % dash_id, body)
    print("dashboard:", r["id"], "|", title, "| panels:", len(panels))
    return r["id"]


V = {}  # viz_id -> viz_id


def viz(dv_id, viz_id, vis_state, query="*"):
    V[viz_id] = make_viz(dv_id, viz_id, vis_state, query)
    print("viz:", viz_id, "|", vis_state["title"])
    return viz_id


def build(dv_id):
    # ---- D1: activity ----
    viz(dv_id, "cw-viz-rev-time",
        hist_vis("Revisions over time by wiki", "labels.wiki"),
        'record_kind: "wiki_revision"')
    viz(dv_id, "cw-viz-event-time",
        hist_vis("Events over time by type", "labels.event_type"),
        'record_kind: "wiki_event"')
    viz(dv_id, "cw-viz-agent-count", metric_vis("Agent names"),
        'record_kind: "wiki_label"')
    viz(dv_id, "cw-viz-top-agents",
        table_vis("Top agent labels by revisions", "authors.raw", 25),
        'record_kind: "wiki_revision"')
    make_dashboard("collusion-wiki-activity", "Collusion Wiki — Activity",
                   "Wiki swarm activity over time; Nightingale collusion.wiki export.",
                   [("cw-viz-rev-time", 32, 12, 0, 0),
                    ("cw-viz-agent-count", 16, 12, 32, 0),
                    ("cw-viz-event-time", 24, 12, 0, 12),
                    ("cw-viz-top-agents", 24, 12, 24, 12)])

    # ---- D2: grammars ----
    viz(dv_id, "cw-viz-grammar-time",
        hist_vis("Grammar-tagged revisions over time", "tags", "grammar:.*"),
        'record_kind: "wiki_revision"')
    viz(dv_id, "cw-viz-grammar-pages",
        bar_vis("Grammar families — pages", "tags", 10, "grammar:.*"),
        'record_kind: "wiki_page"')
    viz(dv_id, "cw-viz-grammar-labels",
        bar_vis("Grammar families — agent labels", "tags", 10, "grammar:.*"),
        'record_kind: "wiki_label"')
    viz(dv_id, "cw-viz-grammar-md",
        markdown_vis("About these grammars",
                     "Name grammars shared with the RubyGems swarm: `zz*` prefixes, "
                     "10-digit epoch suffixes, `oai` infixes, `999` (Christopher's watchlist). "
                     "`try[a-z][0-9]zz` is absent wiki-side — a RubyGems-only grammar."))
    make_dashboard("collusion-wiki-grammars", "Collusion Wiki — Name grammars",
                   "zz / epoch10 / oai / 999 grammar breakdown across pages, revisions, agent labels.",
                   [("cw-viz-grammar-time", 32, 12, 0, 0),
                    ("cw-viz-grammar-md", 16, 12, 32, 0),
                    ("cw-viz-grammar-pages", 24, 12, 0, 12),
                    ("cw-viz-grammar-labels", 24, 12, 24, 12)])

    # ---- D3: laundering ----
    viz(dv_id, "cw-viz-proxy-links",
        bar_vis("Proxy families in extracted links", "labels.proxy_family", 10),
        'record_kind: "wiki_link"')
    viz(dv_id, "cw-viz-top-hosts",
        bar_vis("Top link hosts", "labels.host", 25),
        'record_kind: "wiki_link"')
    viz(dv_id, "cw-viz-proxy-short",
        bar_vis("Shortener target proxy families", "labels.proxy_family", 10),
        'record_kind: "wiki_shortener"')
    viz(dv_id, "cw-viz-top-keywords",
        table_vis("Top shortener keywords", "labels.keyword", 20),
        'record_kind: "wiki_shortener"')
    make_dashboard("collusion-wiki-laundering", "Collusion Wiki — Laundering chains",
                   "Reader-proxy laundering: r.jina.ai, translate.goog chains, HF Space CORS proxy.",
                   [("cw-viz-proxy-links", 24, 12, 0, 0),
                    ("cw-viz-proxy-short", 24, 12, 24, 0),
                    ("cw-viz-top-hosts", 24, 14, 0, 12),
                    ("cw-viz-top-keywords", 24, 14, 24, 12)])

    # ---- D4: gem bridge ----
    viz(dv_id, "cw-viz-bridge-count", metric_vis("Bridge gems"),
        'record_kind: "wiki_bridge"')
    viz(dv_id, "cw-viz-bridge-proxy",
        bar_vis("Bridge homepage laundering chains", "labels.proxy_family", 10),
        'record_kind: "wiki_bridge"')
    viz(dv_id, "cw-viz-bridge-hosts",
        bar_vis("Bridge homepage hosts", "labels.homepage_host", 20),
        'record_kind: "wiki_bridge"')
    viz(dv_id, "cw-viz-bridge-table",
        table_vis("Bridge gems", "package", 100, "version"),
        'record_kind: "wiki_bridge"')
    viz(dv_id, "cw-viz-bridge-md",
        markdown_vis("About this bridge",
                     "79 June-18 campaign gems embedded as `registry_metadata` records in the "
                     "wiki corpus (SEC county.json retrieval experiments). All 79 are in JFrog's "
                     "inventory — zero outside it. Mechanism boundary: go-import, web_hooks, A000, "
                     ".yardopts are all zero wiki-side; the wiki is a sibling operation, not the "
                     "RubyGems coordination channel."))
    make_dashboard("collusion-wiki-gem-bridge", "Collusion Wiki — Gem bridge",
                   "The 79 June-18 gems inside the wiki corpus; laundering chains; JFrog overlap.",
                   [("cw-viz-bridge-count", 12, 10, 0, 0),
                    ("cw-viz-bridge-md", 36, 10, 12, 0),
                    ("cw-viz-bridge-proxy", 24, 12, 0, 10),
                    ("cw-viz-bridge-hosts", 24, 12, 24, 10),
                    ("cw-viz-bridge-table", 48, 14, 0, 22)])


def verify():
    found = req("GET", "/api/saved_objects/_find?type=dashboard&per_page=100&fields=title")
    for d in found.get("saved_objects", []):
        if d["id"].startswith("collusion-wiki-"):
            print("dashboard:", d["id"], "|", d["attributes"].get("title"))


def main():
    dv_id = data_view_id()
    if "--verify" in sys.argv:
        verify()
        return
    build(dv_id)
    verify()


if __name__ == "__main__":
    main()
