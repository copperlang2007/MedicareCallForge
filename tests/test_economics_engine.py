"""
Tests for the DualStreamPNLAdapter and production alerting/forecasting.
These are critical for pilot economics visibility and kill-switch behavior.
"""

import pytest

from medicare_call_forge.economics.dual_stream_pnl import (
    DualStreamPNLAdapter,
    PNLRecord,
)


def test_economics_thresholds_and_aep_scenario():
    engine = DualStreamPNLAdapter()

    # Simulate some real call data
    engine.record_live_call(
        call_id="test_econ_001",
        decision="enroll_in_house",
        cost_cents=6200,
        revenue_cents=18500,
        uval=0.78,
        compliance_score=96.0,
        is_enrollment=True,
    )
    engine.record_live_call(
        call_id="test_econ_002",
        decision="sell_call",
        cost_cents=1650,
        revenue_cents=2500,
        uval=0.54,
        compliance_score=91.0,
        is_enrollment=False,
    )

    snapshot = engine.get_snapshot()
    assert snapshot.enroll.calls >= 1
    assert snapshot.sell.calls >= 1

    # Thresholds should return a list (may be empty with good data)
    alerts = engine.check_thresholds(snapshot)
    assert isinstance(alerts, list)

    # AEP what-if must produce usable numbers
    scenario = engine.what_if_aep_scenario(8500, 4200)
    assert scenario["totals"]["total_margin_dollars"] > 0
    assert scenario["totals"]["blended_cac_dollars"] > 0


def test_economics_thresholds_fire_on_breach():
    """Production alerting must detect and report kill-switch conditions (e.g. high CAC or low margin)."""
    engine = DualStreamPNLAdapter()

    # Force a bad enroll scenario: high cost, low revenue → high CAC breach
    engine.record_live_call(
        call_id="breach_enroll_001",
        decision="enroll_in_house",
        cost_cents=12000,   # very high cost
        revenue_cents=8000,
        uval=0.65,
        compliance_score=88.0,
        is_enrollment=True,
    )

    snapshot = engine.get_snapshot()
    alerts = engine.check_thresholds(snapshot)

    # Should fire at least one critical alert (CAC breach)
    assert any("CAC" in a.get("code", "") or "BREACH" in a.get("code", "") for a in alerts)
    assert any(a.get("severity") == "CRITICAL" for a in alerts)
