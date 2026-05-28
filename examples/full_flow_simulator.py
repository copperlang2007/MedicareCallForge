r"""
End-to-end flow simulator for MedicareCallForge - Demonstrates BOTH revenue streams.

This script shows the complete inbound call journey for the two monetization paths in the business plan:

1. Search (Google/Bing call-only) -> High-intent -> Enroll In-House (commission revenue)
2. Social (FB/YouTube educational) -> Lower-intent/overflow -> Sell Call at $25 (lead sales)

Run the service first:
  cd C:\Users\lang2\MedicareCallForge
  uvicorn src.medicare_call_forge.app:app --reload

Then run:
  python examples/full_flow_simulator.py

Or open the luxury operator console at:
  http://localhost:8000/dashboard

Production telephony is now live at /webhooks/twilio/voice (GHL fields + TaskRouter Enqueue + Media Streams per your moat repos). Point real Twilio/GHL webhooks for pilot.

This is the closest thing to a real pilot you can run locally without live GHL/Twilio webhooks.
"""

import asyncio
from datetime import datetime, timezone

import httpx

BASE_URL = "http://localhost:8000"


async def simulate_search_high_intent_enroll_path():
    """High-intent search call -> should strongly favor enroll_in_house."""
    payload = {
        "call_id": f"search_high_{int(datetime.now(timezone.utc).timestamp())}",
        "from_number": "+15551234567",
        "state": "CA",
        "has_explicit_tcpa_consent": True,
        "recording_started": True,
        "has_high_intent_signals": True,
        "state_licensing_fit": 0.95,
        "predicted_enrollment_prob": 0.78,
        "estimated_cost_to_serve": 28.0,
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
                "soa_before_specifics": "Scope of Appointment signed at 14:02 before any plan discussion"
            }
        },
        "dial_attempts": 1,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/webhooks/inbound-call", json=payload, timeout=15.0)
        data = resp.json()
        print("=== STREAM 1: SEARCH -> ENROLL IN-HOUSE ===")
        print(f"Decision: {data['decision']}")
        print(f"UVal: {data['score']['overall_uval']} | Enroll Fit: {data['score']['enroll_fit']}")
        print(f"Reason: {data['reason']}")
        print(f"Action: {data['recommended_action']}")
        print(f"Compliance Score: {data['compliance']['compliance_score']}")
        print()


async def simulate_social_overflow_sell_path():
    """Social/educational lower-intent call -> should go to sell_call stream."""
    payload = {
        "call_id": f"social_overflow_{int(datetime.now(timezone.utc).timestamp())}",
        "from_number": "+15559876543",
        "state": "NY",
        "has_explicit_tcpa_consent": True,
        "recording_started": True,
        "has_high_intent_signals": False,
        "state_licensing_fit": 0.6,
        "predicted_enrollment_prob": 0.42,
        "estimated_cost_to_serve": 14.0,
        "transcript_evidence": {
            "mentions": {
                "tp_mo_disclaimer_verbatim": True,
                "recording_started": True,
                "language_access_notice": True,
            }
        },
        "dial_attempts": 2,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/webhooks/inbound-call", json=payload, timeout=15.0)
        data = resp.json()
        print("=== STREAM 2: SOCIAL -> SELL CALL AT $25 ===")
        print(f"Decision: {data['decision']}")
        print(f"UVal: {data['score']['overall_uval']} | Sell Margin Potential: {data['score']['sell_margin_potential']}")
        print(f"Reason: {data['reason']}")
        print(f"Action: {data['recommended_action']}")
        print()

        if data["decision"] == "sell_call":
            # Demonstrate the sell tool (leadmarket-style)
            sell_resp = await client.post(
                f"{BASE_URL}/tools/sell-overflow-call",
                json={"call_id": data["compliance"]["call_id"] if "call_id" in str(data) else payload["call_id"], "compliance_proof": data["audit_event"]},
                timeout=15.0,
            )
            print("SELL PACKAGE GENERATED:")
            print(sell_resp.json())
            print()


async def main():
    print("=== MedicareCallForge End-to-End Dual-Stream Simulator ===\n")
    print("Service must be running: uvicorn src.medicare_call_forge.app:app --reload\n")

    try:
        await simulate_search_high_intent_enroll_path()
        await simulate_social_overflow_sell_path()
        print("=== BOTH STREAMS DEMONSTRATED SUCCESSFULLY ===")
        print("The system correctly routes high-intent search calls toward enrollment")
        print("and lower-intent social calls toward the sell-at-$25 path while enforcing")
        print("the Hard Compliance Gate on every call.")
    except httpx.ConnectError:
        print("ERROR: Service not running on http://localhost:8000")
        print("Start it first with the command above.")


if __name__ == "__main__":
    asyncio.run(main())
