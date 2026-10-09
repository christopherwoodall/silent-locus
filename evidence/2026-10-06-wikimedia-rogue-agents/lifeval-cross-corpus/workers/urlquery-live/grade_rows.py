#!/usr/bin/env python3
"""Extract per-report rows from urlquery htmx search HTML into JSONL.
Usage: grade_rows.py <htmlfile> > out.jsonl
Columns: date, detections(UQ,IDS,TDS), domain, report_uuid, ip, country
"""
import re, sys, json, html

def rows_of(path):
    body = open(path, encoding="utf-8", errors="replace").read()
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S)
    out = []
    for tr in trs:
        if "<th" in tr:
            continue
        uuid_m = re.search(r"/report/([0-9a-f-]{36})", tr)
        dom_m = re.search(r'href="/report/[0-9a-f-]{36}"[^>]*>([^<]+)</a>', tr)
        date_m = re.search(r'<td class="whitespace-nowrap px-3 py-2[^>]*>([^<]+)</td>', tr)
        ip_m = re.search(r'q=ip\.addr:([0-9a-fA-F.:]+)"', tr)
        cc_m = re.search(r'/static/images/flags/([A-Z]{2})\.png', tr)
        uq_m = re.search(r'title="urlquery detections".*?<span[^>]*>(\d+)</span>', tr, re.S)
        ids_m = re.search(r'title="Network IDS detections".*?<span[^>]*>(\d+)</span>', tr, re.S)
        tds_m = re.search(r'title="Threat Detection System detections".*?<span[^>]*>(\d+)</span>', tr, re.S)
        out.append({
            "date": date_m.group(1).strip() if date_m else None,
            "domain": html.unescape(dom_m.group(1)).strip() if dom_m else None,
            "report_uuid": uuid_m.group(1) if uuid_m else None,
            "ip": ip_m.group(1) if ip_m else None,
            "country": cc_m.group(1) if cc_m else None,
            "uq": int(uq_m.group(1)) if uq_m else 0,
            "ids": int(ids_m.group(1)) if ids_m else 0,
            "tds": int(tds_m.group(1)) if tds_m else 0,
        })
    return out

if __name__ == "__main__":
    for r in rows_of(sys.argv[1]):
        print(json.dumps(r))
