#!/usr/bin/env python3
"""Lantern Phase 2 profiler: read fetched panels, classify access state.

Reads raw/panels/*.html + *.headers.txt + fetch-log.jsonl.
Writes working/panel-profiles.jsonl.
No multi-line regex. Substring checks + html.parser only.
"""
import json, os, re
from html.parser import HTMLParser

BASE = os.path.expanduser("~/workspace/silent-locus/data/lanes/cairn-panels")
RAW = os.path.join(BASE, "raw/panels")
WORK = os.path.join(BASE, "working")

class TitleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.h1 = ""
        self.in_h1 = False
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.in_h1 = True
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h1 and not self.h1:
            self.h1 += data.strip()

def has_cjk(s):
    for ch in s:
        o = ord(ch)
        if 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF:
            return True
    return False

def has_cyrillic(s):
    for ch in s:
        if 0x0400 <= ord(ch) <= 0x04FF:
            return True
    return False

def extract_api_paths(html):
    """Collect /api/... and other endpoint-ish quoted strings (observed only)."""
    found = set()
    for q in ('"', "'", "`"):
        i = 0
        while True:
            j = html.find(q, i)
            if j < 0:
                break
            k = html.find(q, j + 1)
            if k < 0 or k - j > 200:
                i = j + 1
                continue
            s = html[j + 1:k]
            i = k + 1
            if s.startswith("/") and len(s) > 2 and ("api" in s.lower() or
                    s.startswith("/projects") or s.startswith("/static") is False and
                    any(w in s.lower() for w in ("project", "task", "session", "agent", "run", "event", "chat", "ws", "socket"))):
                if " " not in s and "<" not in s and ">" not in s:
                    found.add(s)
    return sorted(found)

def version_strings(html):
    out = []
    low = html.lower()
    for brand in ("cairn", "hermes", "openclaw", "strix"):
        i = low.find(brand)
        while i >= 0 and len(out) < 10:
            seg = html[i:i + 60]
            # look for vX.Y in the segment
            for tok in seg.split():
                t = tok.strip(" ,;:'\"()[]")
                if t[:1].lower() == "v" and len(t) > 1 and t[1].isdigit() and "." in t:
                    if t not in out:
                        out.append(f"{brand} {t}")
            i = low.find(brand, i + 1)
    return out

def classify(ip, port, harness, rec, html, headers):
    p = {"ip": ip, "port": port, "harness": harness,
         "url": rec.get("url"), "reachable": rec.get("reachable"),
         "http_status": rec.get("http_status"), "final_url": rec.get("final_url"),
         "title": "", "access_state": "unknown", "projects_visible_count": 0,
         "project_names": [], "languages": [], "version_strings": [],
         "api_paths_seen": [], "notes": ""}
    if rec.get("skipped"):
        p["access_state"] = "skipped"
        p["notes"] = rec.get("skip_reason", "")
        return p
    if not rec.get("reachable"):
        p["access_state"] = "dead"
        p["notes"] = (rec.get("fetch_error") or "unreachable")[:200]
        return p
    size = rec.get("size", 0)
    ctype = rec.get("content_type", "")
    low = html.lower()
    tp = TitleParser()
    try:
        tp.feed(html[:200000])
    except Exception:
        pass
    p["title"] = tp.title.strip()[:200]
    # headers: server
    for line in headers.splitlines():
        if line.lower().startswith("server:"):
            p["server_header"] = line.split(":", 1)[1].strip()
            break
    # languages
    if has_cjk(html[:100000]):
        p["languages"].append("chinese")
    if has_cyrillic(html[:100000]):
        p["languages"].append("russian")
    p["languages"].append("english")
    # login markers
    login_markers = ('type="password"', 'type=\\\'password\\\'', "loginapp()", "signin",
                     "sign in to continue", "sign in —", "sign in -", "username",
                     "mot de passe", "contraseña")
    dash_markers = ("cytoscape", "project list view", "dashboard", "x-data=",
                    "timeline", "projects")
    is_login = any(m in low for m in login_markers)
    title_low = p["title"].lower()
    title_login = any(w in title_low for w in ("login", "sign in", "sign-in", "вход", "登录"))
    if size < 500:
        p["access_state"] = "empty"
        p["notes"] = f"body too small ({size} bytes)"
    elif ctype and "text/html" not in ctype.lower():
        p["access_state"] = "non_html"
        p["notes"] = f"content-type {ctype}, {size} bytes; not a panel page"
    elif is_login or title_login:
        p["access_state"] = "login_gated"
        p["notes"] = "auth wall (login form/password field present)"
    elif any(m in low for m in dash_markers):
        p["access_state"] = "open_dashboard"
        p["notes"] = "SPA dashboard shell; project data loads client-side via API"
    else:
        p["access_state"] = "requires_interaction"
        p["notes"] = "page fetched but state unclear from static HTML"
    p["version_strings"] = version_strings(html)
    p["api_paths_seen"] = extract_api_paths(html)
    # server-side project names are not in SPA shell; keep empty with note
    return p

def main():
    fetchlog = {}
    fl = os.path.join(WORK, "fetch-log.jsonl")
    if os.path.exists(fl):
        for line in open(fl, encoding="utf-8"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            fetchlog[(d["ip"], d["port"])] = d  # last entry wins (re-fetch pass)
    out = open(os.path.join(WORK, "panel-profiles.jsonl"), "w", encoding="utf-8")
    n = 0
    for (ip, port), rec in sorted(fetchlog.items()):
        stem = f"{ip}_{port}"
        html_p = os.path.join(RAW, stem + ".html")
        head_p = os.path.join(RAW, stem + ".headers.txt")
        html = open(html_p, encoding="utf-8", errors="replace").read() if os.path.exists(html_p) else ""
        headers = open(head_p, encoding="utf-8", errors="replace").read() if os.path.exists(head_p) else ""
        p = classify(ip, port, rec.get("harness"), rec, html, headers)
        out.write(json.dumps(p, ensure_ascii=False) + "\n")
        n += 1
    out.close()
    print(f"profiles written: {n}")

if __name__ == "__main__":
    main()
