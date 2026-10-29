#!/usr/bin/env python3
"""Lane 2 plan B: leakix (keyless tier?) + hackertarget host intel.
leakix: GET https://api.leakix.net/search?q=... — if it demands a key, grade D.
hackertarget: free-tier hostsearch; note limits."""
import sys
sys.path.insert(0, ".")
from probe import probe

for q, pid in [("oai", "leakix-oai"),
               ("civilrightsdata", "leakix-civilrightsdata"),
               ("county.json", "leakix-countyjson")]:
    probe("leakix.net", pid,
          f"https://api.leakix.net/search?q={q}",
          note=("keyless-tier search for fingerprint '" + q +
                "'; 401/402/429 -> auth-or-denied -> grade D surface"),
          timeout=60)

probe("hackertarget.com", "hackertarget-doe",
      "https://api.hackertarget.com/hostsearch/?q=civilrightsdata.ed.gov",
      note="free-tier hostsearch for CRDC host; note rate-limit headers/blocks",
      timeout=60)
