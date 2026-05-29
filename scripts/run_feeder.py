"""
Feeder script: Feeds the AGENT_ORCHESTRATED_BUILD_PLAN into the RealRouterAdapter / MultiAgentOrchestrator.

This is the entry point for orchestrated multi-agent execution of the build plan.
"""

from medicare_call_forge.orchestration.build_plan import get_phase0_workflow_steps
from medicare_call_forge.router_integration import RealRouterAdapter


def main():
    print("=== FEEDING PHASE 0 BUILD PLAN TO THE LIVE MULTIAGENT ORCHESTRATOR ===\n")

    adapter = RealRouterAdapter()
    steps = get_phase0_workflow_steps()

    print(f"Total WorkflowSteps in Phase 0: {len(steps)}")
    print("Compliance Gate is first (is_parallel_group=False). Then 3 parallel specialists.\n")

    # Wire real live: one orchestrated run through the real llm-router-engine brain
    result = adapter.execute_build_workflow(steps)

    print("=== LIVE ORCHESTRATOR RESULT ===\n")
    print(f"Source: {result.get('source')}")
    print(f"Workflow ID: {result.get('orchestrator_workflow_id')}")
    print(f"Steps routed through real brain: {result.get('steps_routed', 0)}")
    print()

    decisions = result.get("decisions", [])
    for i, d in enumerate(decisions, 1):
        print(f"  Decision {i}: model={d.get('chosen_model')}  step={str(d.get('step_id') or 'N/A')[:8]}...")
        rationale = (d.get("rationale") or "")[:110]
        if rationale:
            # Strip any non-ascii to survive Windows cp1252 consoles (same pattern as llm-router safe_output)
            safe = rationale.encode("ascii", "ignore").decode("ascii", "ignore")
            print(f"    Rationale: {safe}...")

    print("\n=== REAL WORKFLOW METRICS (from live MultiAgentOrchestrator) ===")
    metrics = result.get("metrics", {})
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    print("\n=== PHASE 0 BUILD PLAN EXECUTED BY LIVE BRAIN ===")
    print("Real MultiAgentOrchestrator (with OrchestrationContext, parallel groups, handoff tracking, get_workflow_metrics) drove the AGENT_ORCHESTRATED_BUILD_PLAN Phase 0 steps.")


if __name__ == "__main__":
    main()
