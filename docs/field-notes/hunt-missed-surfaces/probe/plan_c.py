#!/usr/bin/env python3
"""Lane 2 plan C: dead-drop/paste surfaces (indexability audit) + microlink liveness.

These surfaces are almost certainly unscourable-by-design (no search/index
interface); the probe is to CONFIRM that with evidence, not to find hits."""
import sys
sys.path.insert(0, ".")
from probe import probe

probe("0x0.st", "paste-0x0st-index",
      "https://0x0.st/",
      note="indexability audit: does any search/list/index endpoint exist? "
           "0x0.st is a write-once pastebin; expected none",
      timeout=45)

probe("ix.io", "paste-ixio-index",
      "https://ix.io/",
      note="indexability audit: ix.io addresses pastes as ix.io/user:NN (user-scoped); "
           "check for any global index/search interface",
      timeout=45)

probe("paste.rs", "paste-pasters-index",
      "https://paste.rs/",
      note="indexability audit: paste.rs homepage documents API; check for search/index",
      timeout=45)

probe("termbin.com", "paste-termbin-index",
      "https://termbin.com/",
      note="indexability audit: termbin is netcat-only FIFO paste; check site for any index",
      timeout=45)

probe("telegra.ph", "telegraph-index",
      "https://telegra.ph/",
      note="indexability audit: telegraph pages are addressable but unlisted; "
           "verify no search/index API exists (api.telegra.ph only: accounts/pages)",
      timeout=45)

probe("microlink.io", "microlink-live",
      "https://api.microlink.io?url=https://example.com",
      note="free-tier liveness: metadata/screenshot API; verify response and "
           "confirm there is no log/history interface of queried URLs",
      timeout=45)
