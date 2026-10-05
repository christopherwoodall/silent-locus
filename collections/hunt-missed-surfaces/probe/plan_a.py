#!/usr/bin/env python3
"""Lane 2 plan A: crt.sh (cert transparency) + urlhaus (abuse.ch host reputation).
crt.sh is keyless and queryable; incident URLs may surface infra footprints."""
import sys
sys.path.insert(0, ".")
from probe import probe

# --- crt.sh: odd subdomains/certs around incident windows ---
for domain, pid in [("civilrightsdata.ed.gov", "crtsh-doe"),
                    ("bea.gov", "crtsh-bea"),
                    ("bac-lac.gc.ca", "crtsh-lac")]:
    probe("crt.sh", pid,
          f"https://crt.sh/?q=%25.{domain}&output=json",
          note=(f"cert transparency for %25.{domain}; agents don't mint certs but "
                f"infra/relay certs in incident windows may show; grepped for fingerprints"),
          timeout=90)

# --- urlhaus: were incident URLs ever reported as malicious? ---
for host, pid in [("civilrightsdata.ed.gov", "urlhaus-doe"),
                  ("bea.gov", "urlhaus-bea"),
                  ("www.sec.gov", "urlhaus-sec")]:
    probe("urlhaus (abuse.ch)", pid,
          "https://urlhaus-api.abuse.ch/v1/host/",
          method="POST", data=f"host={host}",
          note=(f"abuse.ch keyless POST host-lookup: was {host} ever flagged "
                f"as malware-URL host; query_status no_results = honest negative"),
          timeout=60)
