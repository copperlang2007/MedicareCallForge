#!/usr/bin/env python3
"""
Post-Deploy Smoke Test — MedicareCallForge

Run this after every deployment (or before any client demo / live test phase).

It exercises the critical production paths without requiring real phone calls:
- Health
- Compliance Gate (via simulated high-quality call)
- Live Brain decision path
- Economics endpoint (including alerts and historical)
- GHL connectivity (if configured)
"""

import os
import sys
from datetime import datetime, timezone

import httpx

BASE_URL = os.getenv("SMOKE_BASE_URL", "http://localhost:8000")

def check(name: str, condition: bool, details: str = ""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")
    if details:
        print(f"      {details}")
    if not condition:
        sys.exit(1)

def main():
    print(f"MedicareCallForge Post-Deploy Smoke Test")
    print(f"Target: {BASE_URL}")
    print(f"Time:   {datetime.now(timezone.utc).isoformat()}\n")

    client = httpx.Client(base_url=BASE_URL, timeout=15.0)

    # 1. Health
    r = client.get("/health")
    check("Health endpoint", r.status_code == 200, r.json())

    # 2. Simulated high-quality call through full gate + brain
    payload = {
        "call_id": f"smoke-{int(datetime.now().timestamp())}",
        "from_number": "+15551234567",
        "state": "CA",
        "has_explicit_tcpa_consent": True,
        "recording_started": True,
        "has_high_intent_signals": True,
        "state_licensing_fit": 0.95,
        "transcript_evidence": {
            "mentions": {
                "tp_mo_disclaimer_verbatim": True,
                "soa_before_specifics": True,
                "recording_started": True,
                "pewc_captured": True,
                "language_access_notice": True,
            },
            "quotes": {
                "tp_mo_disclaimer_verbatim": "We do not offer every plan in your area...",
            },
        },
    }
    r = client.post("/webhooks/inbound-call", json=payload)
    check("Inbound call (gate + brain)", r.status_code == 200)
    data = r.json()
    check("Brain decision present", "decision" in data)
    check("Compliance gate passed", data.get("compliance", {}).get("ready_for_next_step") is True)

    # 3. Economics + alerts
    r = client.get("/metrics/economics")
    econ = r.json()
    check("Economics endpoint", r.status_code == 200)
    check("Historical data present", "historical" in econ)
    check("Alerts field present", "alerts" in econ)

    # 4. Brain decisions (if any have been made)
    r = client.get("/brain/recent-decisions")
    check("Brain decisions endpoint", r.status_code == 200)

    # 5. GHL connectivity (best effort)
    r = client.get("/ghl/health")
    ghl = r.json()
    if ghl.get("connected"):
        print("[PASS] GHL connectivity healthy")
    else:
        print("[INFO] GHL not connected (expected in some environments)")

    print("\nAll critical smoke checks passed. System is deploy-healthy.")
    print("Next: Run full military verification harness before client live tests.")

if __name__ == "__main__":
    main()
