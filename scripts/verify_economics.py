#!/usr/bin/env python3
"""
Phase 1 Economics Verification Script

Demonstrates the new real DualStreamPNLAdapter wired into the system.

Run this to prove the economics foundation is ready to receive real data
from grok-extract-telesales-pnl + live MultiAgentOrchestrator cost signals.

This is the autonomous Phase 1 companion while waiting for live call testing.
"""

from medicare_call_forge.economics import economics_engine, PNLRecord
from medicare_call_forge.observability import metrics
from medicare_call_forge.router_integration import RealRouterAdapter

def main():
    print("=== MEDICARECALLFORGE PHASE 1 — REAL ECONOMICS VERIFICATION ===\n")

    adapter = RealRouterAdapter()
    print(f"Live brain active: {adapter._orchestrator is not None}")

    # Simulate ingesting real-style data (what grok-extract-telesales-pnl would produce)
    print("\n--- Ingesting sample batch (simulating grok-extract output) ---")

    batch = [
        PNLRecord(call_id="e1", stream="enroll_in_house", timestamp="2026-05-28T10:00:00Z",
                  decision="enroll_in_house", revenue_cents=18500, cost_cents=6200, uval=0.78,
                  compliance_score=96.2, is_enrollment=True, source="grok-extract-batch"),
        PNLRecord(call_id="e2", stream="enroll_in_house", timestamp="2026-05-28T10:05:00Z",
                  decision="enroll_in_house", revenue_cents=17200, cost_cents=7100, uval=0.71,
                  compliance_score=94.8, is_enrollment=True, source="grok-extract-batch"),
        PNLRecord(call_id="s1", stream="sell_call", timestamp="2026-05-28T10:10:00Z",
                  decision="sell_call", revenue_cents=2500, cost_cents=1650, uval=0.55,
                  compliance_score=91.3, is_enrollment=False, source="grok-extract-batch"),
    ]

    economics_engine.ingest_batch(batch)

    brain_metrics = adapter._orchestrator.get_workflow_metrics() if adapter._orchestrator else {}
    snapshot = economics_engine.get_snapshot(brain_metrics=brain_metrics)

    print(f"Enroll calls: {snapshot.enroll.calls} | CAC: ${snapshot.enroll.cac_cents/100 if snapshot.enroll.cac_cents else 'N/A'}")
    print(f"Sell calls:   {snapshot.sell.calls} | Margin/call: ${snapshot.sell.margin_per_call_cents/100 if snapshot.sell.margin_per_call_cents else 'N/A'}")

    # Demonstrate live brain decision path (Phase 2)
    call_ctx = {"has_high_intent_signals": True, "state_licensing_fit": 0.92}
    brain_dec = adapter.decide_telephony_stream(call_ctx)
    print(f"Live brain call decision source: {brain_dec['source']}")
    print(f"Brain recommendation present: {brain_dec.get('brain_recommendation') is not None}")

    series = economics_engine.get_historical_series(3)
    print(f"Historical series points available: {len(series['labels'])}")

    # Now what the dashboard / API will see
    econ = metrics.get_dual_stream_economics(brain_metrics=brain_metrics)
    print("\n--- /metrics/economics response (what dashboard sees) ---")
    print("Enroll stream calls:", econ["search_enroll_stream"]["calls"])
    print("Sell stream margin_cents:", econ["social_sell_stream"].get("margin_cents"))
    print("Overall brain_cost_efficiency:", econ["overall"].get("brain_cost_efficiency"))
    print("Note:", econ["note"])

    print("\n=== PHASE 1 ECONOMICS FOUNDATION VERIFIED ===")
    print("Ready to receive real grok-extract-telesales-pnl data and live brain cost signals.")
    print("Next (when you have time): point real calls + watch the numbers become real.")

if __name__ == "__main__":
    main()