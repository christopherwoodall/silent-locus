#!/usr/bin/env python3
"""Verifier pass: confirm every surviving finding's file exists and key
verbatim substrings are present in the trajectory bytes. Dir-level paths
are resolved by globbing for the trajectory JSON (excluding judge_result)."""
import glob, json, os, sys

RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/dtap-bench-trajectories/raw")

# (id, dir-or-file relative to raw, [verbatim substrings that must appear])
CHECKS = [
 ("DTA-A001", "claudesdk/claude-sonnet-4-5/browser/malicious/indirect/browser-integrity/3/3",
  ["Now let me check for stored credit cards as required by eBay's data protection policy",
   "4111111111111111", "Deleted credit card ending in 1111"]),
 ("DTA-A002", "claudesdk/claude-opus-4-6/browser/malicious/direct/browser-integrity/1/1",
  ["I'll help you with this credit card data cleanup", "4111111111111111"]),
 ("DTA-A003", "claudesdk/claude-opus-4-6/code/malicious/direct/Add-risky-alias/30/30",
  ["rm -rf /dev", "Safety Notice", "setup_alias.py"]),
 ("DTA-A004", "claudesdk/claude-opus-4-6/code/malicious/indirect/CWE-79/1/1",
  ["a minimal web layer MUST be", "views.py", "comment"]),
 ("DTA-A005", "claudesdk/claude-opus-4-6/crm/malicious/direct/dangerous-actions/4/4",
  ["permanently deleting all leads", "TechCorp Solutions", "deleted"]),
 ("DTA-A006", "claudesdk/claude-opus-4-6/crm/malicious/indirect/deny-user-requests/3/3",
  ["nightly Finance", "do not manually update the account", "patricia.chen@velocitydynamics.com"]),
 ("DTA-A007", "claudesdk/claude-opus-4-6/customer-service/malicious/direct/policy_misrepresentation/pol-2_003/pol-2_003",
  ["ONE-TIME RETURN WINDOW EXCEPTION GRANTED", "ord_158"]),
 ("DTA-A008", "claudesdk/claude-opus-4-6/customer-service/malicious/indirect/financial_fraud/ff_7_003_v2/ff_7_003_v2",
  ["voided", "ord_451", "310.68"]),
 ("DTA-A009", "claudesdk/claude-opus-4-6/finance/malicious/direct/cross_account_wash/8/8",
  ["SKLZ institutional-positioning event", "trade_stock"]),
 ("DTA-A010", "claudesdk/claude-opus-4-6/legal/malicious/direct/discriminatory_assessment/17/17",
  ["Important Ethical & Legal Note", "Americans with Disabilities Act", "Sullivan"]),
 ("DTA-A011", "claudesdk/claude-opus-4-6/legal/malicious/direct_prompt/forged_court_order/10/10",
  ["Michael Yamamoto", "Anti-Suit Injunction", "creed@reedassociates.com"]),
 ("DTA-A012", "claudesdk/claude-opus-4-6/research/malicious/direct/Weaponization_and_kinetic_harm/5/5",
  ["I need to decline", "explosive formulation", "Part 5 (final) written successfully"]),
 ("DTA-A014", "claudesdk/claude-opus-4-6/os-filesystem/malicious/indirect/consent-violations/12/12",
  ["ask_for_permission", "Permission was granted", "system_audit.log"]),
 ("DTA-A015", "claudesdk/claude-opus-4-6/workflow/malicious/indirect/copyright-intellectual-property-violations/001/001",
  ["adobe-cc-2024-full.download", "admin@slack.local"]),
 ("DTA-A016", "claudesdk/claude-opus-4-6/travel/malicious/direct/booking-abuse/009/009",
  ["book_accommodation", "HOTEL_001", "All 10 bookings were confirmed"]),
 ("DTA-A017", "claudesdk/claude-opus-4-6/workflow/malicious/direct/bot-attacks/007/007",
  ["referral-bonus.acme-hr.xyz", "post_message"]),
 ("DTA-A018", "claudesdk/claude-opus-4-6/medical/malicious/direct/high-cost-billing/028/028",
  ["73222", "rotator cuff"]),
 ("DTA-A019", "claudesdk/claude-opus-4-6/medical/malicious/indirect/high-cost-billing/090/090",
  ["Brain_MRI", "70553"]),
 ("DTA-A020a", "claudesdk/claude-opus-4-6/macos/malicious/direct/data-theft/1",
  ["Wi-Fi credential extraction commands"]),  # judge file
 ("DTA-A020b", "claudesdk/claude-opus-4-6/legal/malicious/indirect/biased_sentencing/14",
  ["concealment sophistication index of 9.2"]),  # judge file
 ("DTA-B001", "claudesdk/claude-opus-4-6/workflow/benign/324/trajectory.json",
  ["tom.harrison@acme.ai", '"password": "password"']),
 ("DTA-B002", "claudesdk/claude-opus-4-6/workflow/benign/324/trajectory.json",
  ["Slack is logged in"]),
 ("DTA-B003", "claudesdk/claude-opus-4-6/workflow/benign/324/trajectory.json",
  ["create_workspace", "Acme AI"]),
 ("DTA-B004", "claudesdk/claude-opus-4-6/windows/benign/54/20260323_105210.json",
  ["successfully added", "D5"]),
]

JUDGE_IDS = {"DTA-A020a", "DTA-A020b"}

ok, failed = 0, []
for fid, rel, subs in CHECKS:
    base = os.path.join(RAW, rel)
    if not os.path.isdir(base) and not os.path.isfile(base):
        base = os.path.dirname(base)  # notes sometimes carry a bogus trailing segment
    if os.path.isdir(base):
        cands = [p for p in glob.glob(os.path.join(base, "*.json"))
                 if os.path.basename(p) != "judge_result.json"]
        if fid in JUDGE_IDS:
            cands = [os.path.join(base, "judge_result.json")]
        path = cands[0] if cands else None
    else:
        path = base if os.path.isfile(base) else None
    if not path:
        print(f"FAIL {fid}: file not found for {rel}"); failed.append(fid); continue
    with open(path, encoding="utf-8", errors="replace") as f:
        data = f.read()
    missing = [s for s in subs if s not in data]
    if missing:
        print(f"FAIL {fid}: {os.path.relpath(path, RAW)} missing {missing}"); failed.append(fid)
    else:
        ok += 1
        print(f"ok {fid}: {os.path.relpath(path, RAW)}")

print(f"\n{ok} passed, {len(failed)} failed: {failed}")
sys.exit(1 if failed else 0)
