#!/usr/bin/env python3
"""Lane 2 plan F: relay-class grade-C extras (on-demand capture + text-extraction).
Ghost Archive (on-demand archive, no account) and Megalodon are the strongest
arquivo.pt analogs; urltoany is a markdown.new analog."""
import sys
sys.path.insert(0, ".")
from probe import probe

probe("Ghost Archive (ghostarchive.org)", "ghostarchive-home",
      "https://ghostarchive.org/",
      note=("on-demand capture surface, no account: check for any capture "
            "search/index/enumeration shape (archive/<id> URLs are permanent "
            "public; is there a /search or listing?)"),
      timeout=60)

probe("Megalodon (megalodon.jp)", "megalodon-live",
      "https://megalodon.jp/",
      note="verify live status (unverified 2026-10-03): Japanese on-demand "
           "web archive; check current URL/archive shape",
      timeout=60)

probe("urltoany.com", "urltoany-home",
      "https://urltoany.com/",
      note="markdown.new analog: check for keyless API shape (SourceForge "
           "lists 'Has API'); no-log fetch-relay class expected",
      timeout=60)
