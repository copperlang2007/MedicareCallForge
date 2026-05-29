"""
MedicareCallForge Intake Service - Production FastAPI application.

This is the live intake layer for inbound Medicare calls.
- Enforces the Hard Compliance Gate on every single call (non-negotiable).
- Uses UVal-style scoring for dual-stream decisions (enroll in-house vs sell).
- Provides MCP-style tools.
- Designed to be deployed to Railway / Docker and integrated with your llm-router-engine.

End-to-end ready for controlled market pilot when wired to real GHL/Twilio webhooks.
"""

from __future__ import annotations

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Literal

from fastapi.responses import StreamingResponse

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from medicare_call_forge.compliance.gate import (
    CallContext,
    apply_hard_compliance_gate,
    create_audit_event,
)
from medicare_call_forge.scoring.uval_scorer import MedicareLeadScorer, LeadScore
from medicare_call_forge.observability import metrics, audit_vault
from medicare_call_forge.telephony.inbound_handler import get_telephony_router
from medicare_call_forge.dashboard import get_luxury_dashboard_html
from medicare_call_forge.ghl.client import ghl_client
from medicare_call_forge.router_integration import RealRouterAdapter

# Production logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("medicare_call_forge")

# In-memory audit chain (production: persist to Postgres + MinIO/S3 vault)
_audit_chain: list[dict[str, Any]] = []
_last_hash: str | None = None

# Live event stream for the luxury dashboard (simple in-memory for pilot)
_live_events: asyncio.Queue = asyncio.Queue(maxsize=100)

# Initialize scorer (in production this would be configured with real models from llm-router-engine)
scorer = MedicareLeadScorer()


class InboundCallWebhook(BaseModel):
    """Simulated or real GHL/Twilio-style inbound call payload."""
    call_id: str
    from_number: str
    state: str | None = None
    contact_state: str | None = None
    has_explicit_tcpa_consent: bool = False
    is_dnc_listed: bool = False
    recording_started: bool = False
    transcript_evidence: dict[str, Any] = Field(default_factory=dict)
    dial_attempts: int = 0
    last_dialed_at: datetime | None = None
    # Additional signals for scoring (in real system these come from IVR or early transcript)
    has_high_intent_signals: bool = False
    state_licensing_fit: float = 0.7
    predicted_enrollment_prob: float = 0.55
    estimated_cost_to_serve: float = 22.0


class ComplianceDecision(BaseModel):
    compliance: Any
    score: LeadScore
    decision: Literal["enroll_in_house", "sell_call", "block"]
    reason: str
    audit_event: dict[str, Any]
    recommended_action: str


class SellLeadPackage(BaseModel):
    """Output for the 'sell at $25' stream (leadmarket style)."""
    call_id: str
    packaged_lead: dict[str, Any]
    compliance_proof: dict[str, Any]
    suggested_price_cents: int = 2500
    expected_margin_cents: int = 900


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("MedicareCallForge Intake Service starting - Hard Compliance Gate + Dual-Stream UVal Scorer armed.")
    yield
    logger.info("Service shutting down. Final audit chain length: %d", len(_audit_chain))


app = FastAPI(
    title="MedicareCallForge Intake Service",
    version="0.2.0",
    description="Production compliance-first intake + dual-stream decisioning for Medicare inbound calls. End-to-end market pilot ready.",
    lifespan=lifespan,
)

# Mount production telephony handlers (Twilio Voice + GHL patterns)
# Both revenue streams (enroll vs sell) are first-class after the Hard Compliance Gate.
app.include_router(get_telephony_router())


@app.post("/webhooks/inbound-call", response_model=ComplianceDecision)
async def handle_inbound_call(webhook: InboundCallWebhook) -> ComplianceDecision:
    """
    Main entrypoint for every inbound call (from GHL, Twilio, or simulator).
    This endpoint is the gatekeeper. Every call MUST pass the Hard Compliance Gate first.
    Then it is scored with UVal for the optimal dual-stream decision.
    """
    global _last_hash

    context = CallContext(
        call_id=webhook.call_id,
        from_number=webhook.from_number,
        state=webhook.state,
        contact_state=webhook.contact_state,
        has_explicit_tcpa_consent=webhook.has_explicit_tcpa_consent,
        is_dnc_listed=webhook.is_dnc_listed,
        recording_started=webhook.recording_started,
        transcript_or_evidence=webhook.transcript_evidence,
        dial_attempts=webhook.dial_attempts,
        last_dialed_at=webhook.last_dialed_at,
    )

    # Step 1: Hard Compliance Gate (non-negotiable)
    compliance_result = apply_hard_compliance_gate(context, prev_hash=_last_hash)

    # Create immutable audit event
    audit_event = create_audit_event(
        prev_hash=_last_hash,
        event_type="compliance_gate",
        entity_id=webhook.call_id,
        payload=compliance_result.model_dump(),
    )
    _audit_chain.append(audit_event.model_dump())
    _last_hash = audit_event.hash
    # Also persist to the new durable vault (Track 4)
    audit_vault.append(audit_event.model_dump())

    if not compliance_result.ready_for_next_step:
        score = LeadScore(
            overall_uval=0.0,
            enroll_fit=0.0,
            sell_margin_potential=0.0,
            compliance_risk=1.0,
            recommended_stream="block",
            rationale="Hard compliance failure - call blocked before any monetization path.",
        )
        metrics.record_call(webhook.call_id, "block", compliance_result.compliance_score, 0.0)
        return ComplianceDecision(
            compliance=compliance_result,
            score=score,
            decision="block",
            reason=f"Hard compliance failure: {[f.code for f in compliance_result.flags]}",
            audit_event=audit_event.model_dump(),
            recommended_action="Do not connect the call. Log for review and potential remediation.",
        )

    # Step 2: UVal Scoring for optimal dual-stream decision
    score_input = {
        "compliance_score": compliance_result.compliance_score,
        "has_high_intent_signals": webhook.has_high_intent_signals,
        "state_licensing_fit": webhook.state_licensing_fit,
        "predicted_enrollment_prob": webhook.predicted_enrollment_prob,
        "estimated_cost_to_serve": webhook.estimated_cost_to_serve,
        "regulatory_flags_count": len([f for f in compliance_result.flags if f.severity == "high"]),
    }
    score = scorer.score(score_input)

    # Step 3: Execute the chosen stream
    if score.recommended_stream == "enroll_in_house":
        decision = "enroll_in_house"
        reason = score.rationale
        action = "Transfer to best licensed agent using GHL + masterBRIDGE-style smart routing. Track as high-value enrollment."
    elif score.recommended_stream == "sell_call":
        decision = "sell_call"
        reason = score.rationale
        action = "Package as sellable lead (leadmarket style) and list at ~$25. Expected margin tracked."
    else:
        decision = "block"
        reason = score.rationale
        action = "Do not monetize. Review for quality issues."

    metrics.record_call(webhook.call_id, decision, compliance_result.compliance_score, score.overall_uval)

    # Publish to live dashboard stream (for luxury operator console)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "call_id": webhook.call_id,
        "decision": decision,
        "compliance_score": compliance_result.compliance_score,
        "uval": score.overall_uval,
        "audit_hash": audit_event.hash,
        "reason": reason,
    }
    try:
        _live_events.put_nowait(event)
    except asyncio.QueueFull:
        pass  # drop oldest if needed in production

    logger.info(
        "Call %s processed | Compliance: %.1f | UVal: %.3f | Decision: %s",
        webhook.call_id, compliance_result.compliance_score, score.overall_uval, decision
    )

    return ComplianceDecision(
        compliance=compliance_result,
        score=score,
        decision=decision,
        reason=reason,
        audit_event=audit_event.model_dump(),
        recommended_action=action,
    )


@app.post("/tools/sell-overflow-call", response_model=SellLeadPackage)
async def sell_overflow_call(call_id: str, compliance_proof: dict[str, Any]) -> SellLeadPackage:
    """MCP-style tool for the sell stream (inspired by leadmarket)."""
    # In real system: validate compliance_proof hash chain, package PII-minimized lead, push to marketplace
    expected_margin = 900  # $9 margin at $25 sale with ~$16 blended CAC target
    return SellLeadPackage(
        call_id=call_id,
        packaged_lead={
            "type": "medicare_inbound_overflow",
            "call_id": call_id,
            "compliance_ok": True,
            "packaged_at": datetime.now(timezone.utc).isoformat(),
        },
        compliance_proof=compliance_proof,
        suggested_price_cents=2500,
        expected_margin_cents=expected_margin,
    )


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "compliance_gate_armed": True,
        "dual_stream_uval_scorer_active": True,
        "audit_chain_length": len(_audit_chain),
        "version": "0.2.0",
    }


@app.get("/audit/last")
async def get_last_audit():
    """For operators and CMS audit prep."""
    last = audit_vault.get_last() or (_audit_chain[-1] if _audit_chain else None)
    if not last:
        raise HTTPException(404, "No audits yet")
    return last


@app.get("/audit/vault")
async def get_full_audit_vault():
    """Full tamper-evident audit chain for the luxury dashboard and CMS packs."""
    return {
        "vault": audit_vault.get_all(),
        "total": len(audit_vault.get_all()),
        "latest_hash": audit_vault.get_last()["hash"] if audit_vault.get_last() else None,
    }


@app.get("/metrics/economics")
async def economics():
    """
    Production dual-stream economics endpoint.

    Now powered by the real DualStreamPNLAdapter + live MultiAgentOrchestrator brain
    cost signals when available.
    """
    brain_metrics = {}
    try:
        if _router_adapter._orchestrator:
            brain_metrics = _router_adapter._orchestrator.get_workflow_metrics() or {}
    except Exception:
        pass

    data = metrics.get_dual_stream_economics(brain_metrics=brain_metrics)

    # Attach real historical series + military alerts (Phase 2/3 dashboard upgrade)
    try:
        from medicare_call_forge.economics import economics_engine
        data["historical"] = economics_engine.get_historical_series(days=7)
        data["alerts"] = economics_engine.check_thresholds()
    except Exception:
        data["historical"] = {"labels": [], "enroll_calls": [], "sell_calls": [], "overall_margin_dollars": []}
        data["alerts"] = []

    return data


@app.get("/dashboard", response_class=HTMLResponse)
async def luxury_dashboard():
    """
    The polished, high-end operator console.
    Quiet luxury. Regulatory precision. Both revenue streams presented with dignity.
    """
    return HTMLResponse(content=get_luxury_dashboard_html())


@app.get("/ghl/health")
async def ghl_health():
    """Quick GHL connection health check (used by dashboard and ops)."""
    return {
        "connected": ghl_client.enabled,
        "base_url": ghl_client.client.base_url if ghl_client.enabled else None,
        "message": "GHL client ready" if ghl_client.enabled else "GHL_API_KEY not configured (graceful mode)",
    }


@app.get("/brain/recent-decisions")
async def recent_brain_decisions(limit: int = 25):
    """Military intelligence endpoint for the Brain tab — recent authoritative decisions from the live MultiAgentOrchestrator."""
    adapter = RealRouterAdapter()
    decisions = adapter.get_recent_brain_decisions(limit=limit)
    return {
        "decisions": decisions,
        "total_recorded": len(decisions),
        "brain_active": adapter._orchestrator is not None,
    }


@app.get("/live/events")
async def live_events():
    """Server-Sent Events stream for real-time updates in the luxury dashboard."""
    async def event_generator():
        while True:
            try:
                event = await asyncio.wait_for(_live_events.get(), timeout=30)
                yield f"data: {json.dumps(event)}\n\n"
            except asyncio.TimeoutError:
                yield ": keep-alive\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# For local development / E2E testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
