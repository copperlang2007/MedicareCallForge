"""
Orchestrated Build Plan for MedicareCallForge.

This module turns the AGENT_ORCHESTRATED_BUILD_PLAN.md into executable
WorkflowSteps for the llm-router-engine MultiAgentOrchestrator.

It enables true multi-agent execution of the remaining work to reach
a controlled market pilot.

The Compliance Gate is always the first non-bypassable step.
"""

from __future__ import annotations

from typing import List, Any

try:
    from llm_router.orchestration.models import WorkflowStep
except ImportError:
    # Fallback for environments where the router is not installed yet
    class WorkflowStep:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


def get_phase0_workflow_steps() -> List[WorkflowStep]:
    """
    Phase 0: Unblock Live Traffic

    Highest priority tasks that must be completed before any real ad spend.
    These directly address the gaps in MARKET_PILOT_CHECKLIST.md.
    """
    steps: List[WorkflowStep] = []

    # Step 0: Non-bypassable Compliance Gate for the entire build plan
    # This ensures every subsequent build step is executed under regulatory_strict policy.
    steps.append(
        WorkflowStep(
            description=(
                "Execute Hard Compliance Gate as the first step for all Phase 0 build activities. "
                "Verify that all GHL/Twilio wiring, live handoff, and operator runbooks maintain "
                "100% recording, verbatim TPMO, SOA-before-specifics, PEWC for data sharing, and "
                "tamper-evident audit trail. Fail the build step on any compliance violation."
            ),
            # task_class omitted so live engine's classify_task (factual_medical_regulated for Medicare compliance text) is used
            required_capabilities=["regulatory_strict", "audit_trail", "soa_enforcement", "tp_mo_verbatim"],
            is_parallel_group=False,
        )
    )

    # Parallel specialists after gate passes
    steps.append(
        WorkflowStep(
            description=(
                "Production GHL + Twilio webhook integration (live). "
                "Use patterns from ghl-twilio-smart-queue + masterBRIDGE. "
                "Configure real webhooks, TaskRouter workflows for both streams (Enroll high-intent vs Sell overflow), "
                "forward 'lc_phone' + licensed_states/carrier_appointments/current_availability custom fields, "
                "enable Media Streams transcription, and perform end-to-end verification with real test calls "
                "producing 100% artifact capture (recording + compliance_hash + GHL contact update)."
            ),
            # task_class omitted → live engine classify_task will return factual_medical_regulated
            required_capabilities=["ghl_api", "twilio_webhook", "taskrouter", "media_streams", "custom_field_sync"],
            is_parallel_group=True,
        )
    )

    steps.append(
        WorkflowStep(
            description=(
                "Implement and verify live agent handoff via GHL TaskRouter + masterBRIDGE routing. "
                "Use the rich attributes already defined in the telephony handler (compliance_hash, uval, decision, "
                "licensed info, GHL fields). Add capacity-aware routing, SLA fallbacks, and full provenance logging "
                "back into the audit trail and dashboard."
            ),
            # task_class omitted → live engine classify_task
            required_capabilities=["taskrouter_routing", "agent_capacity", "licensed_state_matching", "provenance"],
            is_parallel_group=True,
        )
    )

    steps.append(
        WorkflowStep(
            description=(
                "Operator runbooks + training using the simulator. "
                "Create repeatable drills for compliance score drops, margin collapse kill-switch, "
                "and both-stream incident handling. At least two operators must be able to independently "
                "handle simulated incidents using only the runbooks and /dashboard."
            ),
            # task_class omitted → live engine classify_task
            required_capabilities=["runbook_creation", "simulator_drills", "dashboard_training"],
            is_parallel_group=True,
        )
    )

    return steps


def get_phase1_workflow_steps() -> List[WorkflowStep]:
    """Phase 1: Real Economics & Visibility (can run in parallel with late Phase 0)."""
    steps: List[WorkflowStep] = []

    steps.append(
        WorkflowStep(
            description=(
                "Replace all economics stubs with real dual-stream PNL. "
                "Integrate grok-extract-telesales-pnl (LSTM forecasting) + masterBRIDGE analytics. "
                "Build production dashboard views for per-stream revenue, CAC, margin, LTV, and AEP projections. "
                "Wire threshold alerts for compliance and margin."
            ),
            # task_class omitted → live engine classify_task
            required_capabilities=["pnl_integration", "forecasting", "real_time_dashboard", "alerting"],
            is_parallel_group=True,
        )
    )

    steps.append(
        WorkflowStep(
            description=(
                "Connect sell stream to real buyers or leadmarket instance. "
                "Use leadmarket patterns for provenance and API key auth. "
                "Enforce buyer onboarding (license verification, PEWC contracts, audit rights). "
                "Implement kill-switch if margin or buyer quality collapses."
            ),
            # task_class omitted → live engine classify_task
            required_capabilities=["leadmarket_api", "buyer_onboarding", "pewc_enforcement", "kill_switch"],
            is_parallel_group=True,
        )
    )

    return steps


def get_full_build_plan_workflow() -> List[WorkflowStep]:
    """
    Returns the complete ordered workflow for the orchestrated build.
    Compliance Gate is always first.
    """
    steps = get_phase0_workflow_steps()
    steps.extend(get_phase1_workflow_steps())
    # Future phases (2 & 3) can be appended here once Phase 0/1 are green
    return steps


# Example usage with the RealRouterAdapter / MultiAgentOrchestrator:
#
# from medicare_call_forge.router_integration import RealRouterAdapter
#
# adapter = RealRouterAdapter()
# plan_steps = get_phase0_workflow_steps()
#
# for step in plan_steps:
#     context = {"build_task": step.description, ...}
#     result = adapter.score_and_decide(context)
#     print(result)
#
# When the real llm-router-engine is installed and running, the adapter will
# execute the full workflow with replanning, metrics, and audit logging.