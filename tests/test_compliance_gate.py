"""
Production-grade tests for the Hard Compliance Gate.

These tests are part of the permanent verification harness for market readiness.
All high-severity compliance failures must be caught.
"""

import pytest
from datetime import datetime, timezone

from medicare_call_forge.compliance.gate import (
    CallContext,
    apply_hard_compliance_gate,
    ComplianceFlagCode,
)


def test_perfect_compliant_call_passes():
    """Ideal inbound call that meets every business plan requirement."""
    context = CallContext(
        call_id="call_ideal_001",
        from_number="+15551234567",
        state="CA",
        has_explicit_tcpa_consent=True,
        recording_started=True,
        transcript_or_evidence={
            "mentions": {
                "tp_mo_disclaimer_verbatim": True,
                "soa_before_specifics": True,
                "recording_started": True,
                "pewc_captured": True,
                "language_access_notice": True,
            },
            "quotes": {
                "tp_mo_disclaimer_verbatim": "We do not offer every plan...",
                "soa_before_specifics": "Signed at 14:02:15 before any plan discussion",
                "recording_started": "Recording started at call answer per 42 CFR",
                "pewc_captured": "PEWC consent captured at 14:01:45",
                "language_access_notice": "Language access notice provided in English/Spanish",
            },
        },
        dial_attempts=1,
    )

    result = apply_hard_compliance_gate(context)
    assert result.ready_for_next_step is True
    assert result.compliance_score >= 95.0
    assert len([f for f in result.flags if f.severity == "high"]) == 0


def test_compliance_test_mode_allows_proceeding_with_weak_evidence():
    """COMPLIANCE_TEST_MODE must allow calls through for safe live testing while still logging the bypass."""
    context = CallContext(
        call_id="call_test_mode_003",
        from_number="+15551112222",
        state="FL",
        has_explicit_tcpa_consent=True,
        recording_started=True,
        transcript_or_evidence={
            "mentions": {
                "soa_before_specifics": True,
            }
            # Deliberately missing several core mentions
        },
    )

    # Normal mode should block or heavily penalize
    normal_result = apply_hard_compliance_gate(context)
    assert normal_result.ready_for_next_step is False or normal_result.compliance_score < 70

    # Test mode should allow proceeding
    test_result = apply_hard_compliance_gate(context, test_mode=True)
    assert test_result.ready_for_next_step is True

    # Must still record that test mode was active
    test_mode_flags = [f for f in test_result.flags if "TEST" in str(f.evidence or "")]
    assert len(test_mode_flags) > 0


def test_missing_recording_and_tp_mo_blocks():
    """Realistic failure mode that would trigger CMS fines."""
    context = CallContext(
        call_id="call_fail_002",
        from_number="+15559876543",
        state="TX",
        has_explicit_tcpa_consent=True,
        recording_started=False,  # Critical failure
        transcript_or_evidence={
            "mentions": {
                "soa_before_specifics": True,
            }
            # TPMO disclaimer completely missing
        },
    )

    result = apply_hard_compliance_gate(context)
    assert result.ready_for_next_step is False
    # Policy-driven verbatim key + explicit recording check both fire
    assert any(f.code == ComplianceFlagCode.MISSING_TP_MO_DISCLAIMER_VERBATIM for f in result.flags)
    assert any(f.code == ComplianceFlagCode.MISSING_RECORDING for f in result.flags)
    assert result.compliance_score < 70


def test_audit_hash_chain_is_tamper_evident():
    """The 10-year vault requirement."""
    context1 = CallContext(call_id="c1", from_number="+1", recording_started=True, has_explicit_tcpa_consent=True)
    r1 = apply_hard_compliance_gate(context1)

    context2 = CallContext(call_id="c2", from_number="+1", recording_started=True, has_explicit_tcpa_consent=True)
    r2 = apply_hard_compliance_gate(context2, prev_hash=r1.audit_hash)

    assert r2.prev_audit_hash == r1.audit_hash
    assert r2.audit_hash != r1.audit_hash  # Different content → different hash


def test_tpa_no_consent_blocks():
    context = CallContext(
        call_id="no_consent",
        from_number="+1",
        has_explicit_tcpa_consent=False,
        recording_started=True,
    )
    result = apply_hard_compliance_gate(context)
    assert result.ready_for_next_step is False
    assert any(f.code == ComplianceFlagCode.TCPA_NO_CONSENT for f in result.flags)
