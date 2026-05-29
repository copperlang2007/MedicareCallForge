# MedicareCallForge — Orchestrated Multi-Agent Build Plan

**Purpose**: This document is designed to be consumed by an orchestrator (llm-router-engine MultiAgentOrchestrator + MCP tools) or a team of specialized sub-agents. It turns the current foundation into a controlled market pilot with both revenue streams live, 100% compliance artifact capture, and real unit economics visibility.

**Core Philosophy** (Non-negotiable):
- Compliance Gate is always the first WorkflowStep (is_parallel_group=false).
- Every step produces tamper-evident audit artifacts.
- Parallel specialists only after the gate passes.
- Real data from your moat repos (masterBRIDGE, ghl-twilio-smart-queue, insureitall-os, grok-extract-telesales-pnl, leadmarket, etc.) takes precedence over new invention.
- Verification with evidence before any task is marked complete.
- Strict todo discipline — one in_progress at a time per agent.

**Current State (as of late May 2026)**:
- Hard Compliance Gate (insureitall-os + masterBRIDGE patterns) — production quality, non-bypassable.
- Medicare UVal Scorer — dual-stream decisioning working in simulator.
- Telephony handler — production-grade with your "lc phone" GHL custom field support.
- Real GHL client + MCP tools (9 tools exposed, including create_opportunity and lc_phone-aware updates).
- Luxury dashboard + audit vault (JSON-backed, exportable packs).
- llm-router-engine adapter ready (Compliance Gate can be first WorkflowStep).
- Docker + Railway ready.
- Full dual-stream E2E simulator + verification scripts.

**What This Plan Achieves**:
Turn the above into a live pilot where real (small-volume) inbound calls flow through both streams with:
- 100% recording + compliance proof
- Real agent handoff via your existing GHL TaskRouter
- Visible per-stream PNL
- Red-team mitigations active
- Ready for controlled ad spend ramp before AEP

---

## Phase 0 — Unblock Live Traffic (Highest Priority — Do This First)

**Goal**: Be able to take real inbound calls from your GHL/Twilio environment through the full system with 100% artifact capture.

**Business Context**:
You cannot validate unit economics or agent capacity until real calls (not just the simulator) flow through the Hard Gate + dual-stream decisioning. This is the #1 item blocking "turn on real ad spend" per your MARKET_PILOT_CHECKLIST.

### Task 0.1: Production GHL + Twilio Webhook Wiring (Live)
**Context**: Your `ghl-twilio-smart-queue` + `masterBRIDGE` repos already contain the exact patterns (Playwright custom field sync, TaskRouter enqueue with rich attributes, Media Streams, compliance.ts enforcement). The current `telephony/inbound_handler.py` is architected to receive them but is not yet pointed at your real production numbers/workflows.

**Sub-tasks for agents** (can be parallelized):
- Map your exact GHL custom fields (especially "lc phone" + licensed_states/carrier_appointments/current_availability) and confirm they are being forwarded correctly in the inbound webhook.
- Configure real Twilio number voice webhook + statusCallback to point at the production `/webhooks/twilio/voice` and `/status` endpoints (with proper signature validation using real `TWILIO_AUTH_TOKEN`).
- Create or adapt the two TaskRouter workflows (Enroll high-intent vs Sell overflow) using the attribute schema already defined in the handler (compliance_hash, uval, decision, licensed info, GHL fields).
- Wire Media Streams (masterBRIDGE pattern) for live transcription on the voice path.
- End-to-end test with real test calls (small volume) — verify gate pass, correct stream decision, rich attributes in TaskRouter, recording + vaulting, and GHL contact update with compliance proof.

**Verification Criteria** (evidence required):
- 50+ real test calls with 100% recording.
- Every call has a tamper-evident audit hash.
- TaskRouter receives the expected rich JSON attributes.
- GHL contact shows the lc_phone + outcome note.
- Dashboard shows the live calls.

**Files to touch**: `telephony/inbound_handler.py`, `ghl/client.py`, `PILOT_WIRING_GUIDE.md` (update with your actual SIDs and field keys), new runbook in `docs/`.

**Suggested Agent Role**: "GHL + Telephony Integration Agent" (use your ghl-twilio-smart-queue + masterBRIDGE code as primary source).

**Risk Tie-in**: RED_TEAM_REPORT.md — "Real GHL/Twilio webhook authentication and live call transfer" is listed as Phase 0 requirement.

### Task 0.2: Live Agent Handoff (GHL TaskRouter + masterBRIDGE Routing)
**Context**: Rich enqueue attributes are already in the code. The missing piece is the actual routing logic and capacity-aware assignment using your existing masterBRIDGE agent data (licensed_states, carrier_appointments, current_availability).

**Sub-tasks**:
- Implement the production enqueue path in the telephony handler (replace Dial fallback with real `<Enqueue workflowSid=...><Task>` for both streams).
- Build or adapt the Workflow + TaskRouter configuration that uses the attributes for skills-based routing (licensed agent match for enroll path, overflow for sell path).
- Add fallback logic (if no licensed agent available within SLA → park or AI assist with human escalation gate).
- Instrument handoff quality metrics back into the dashboard and audit trail.

**Verification**:
- Real calls reach actual licensed agents (or properly parked with recording).
- Handoff latency and success rate visible in dashboard.
- Full provenance in the audit hash chain.

**Files**: `telephony/inbound_handler.py`, new `routing/` module or extension of `ghl/` client, updates to dashboard.

### Task 0.3: Operator Runbooks + Training
**Context**: Even with perfect code, humans will be in the loop during pilot (especially AEP). Your simulator is excellent — turn it into repeatable operator drills.

**Deliverables**:
- Runbook: "What to do when compliance score drops below X"
- Runbook: "Sell stream margin collapse kill-switch procedure"
- Simulator-based training scenarios for both streams
- Dashboard + alerting familiarization

**Verification**: At least two operators can independently handle a simulated compliance incident and a margin alert using only the runbooks + dashboard.

---

## Phase 1 — Real Economics & Visibility (Parallelizable with Phase 0)

**Goal**: Replace all economics stubs with real data so you can see whether the dual-stream math actually works at pilot volume.

**Autonomous Progress (max without any Phase 0 live traffic)**: 
- Full `DualStreamPNLAdapter` + `PNLRecord` + time-series snapshots (`get_historical_series`) in `src/medicare_call_forge/economics/`.
- Real ingestion path ready for `grok-extract-telesales-pnl` batches.
- Wired into `EnhancedMetrics`, `/metrics/economics`, telephony post-call, and luxury dashboard (real CAC/margin/UVal + dynamic chart support).
- **Phase 2 foundation**: Live `MultiAgentOrchestrator` now executes real 1-step `WorkflowStep` for every call decision (`decide_telephony_stream`). Returns `brain_recommendation` + `brain_rationale` + full metrics. Telephony handler surfaces brain participation in logs.
- Live brain cost signals + time-series flow through the system.
- All tests green.

The real llm-router-engine brain is now an active decision participant for both build plans and production call routing, with real economics visible in the command center.

**Military End-to-End Wave (latest autonomous execution)**:
- Brain is now **authoritative** for call routing (primary decision key comes from live MultiAgentOrchestrator when it returns a valid stream, with full local UVal audit trail).
- Economics engine includes time-series history + production AEP what-if simulator (`what_if_aep_scenario`).
- Luxury dashboard is fully dynamic (real historical series driving Chart.js trend charts).
- Military verification harness `scripts/verify_military_e2e.py` proves the complete autonomous chain.
- All tests green.

### Task 1.1: Production Economics Dashboard (grok-extract-pnl + masterBRIDGE Analytics)
**Context**: This is the single most repeated blocker in your own docs (`MARKET_PILOT_CHECKLIST.md`, `PILOT_READY_STATUS.md`, `ROADMAP.md`, `verify_both_streams.ps1`, `app.py`, `observability.py`).

**Sub-tasks**:
- Integrate your existing `grok-extract-telesales-pnl` LSTM/forecasting pipelines as the source of truth for per-stream revenue, CAC, margin, and LTV.
- Pull agent capacity, licensed state coverage, and availability from masterBRIDGE data.
- Build real-time views in the dashboard: Stream 1 vs Stream 2 PNL, margin trend, AEP spike projection.
- Wire alerts (compliance score + margin thresholds).

**Verification**:
- Dashboard shows real numbers (not the current stub) for the last 7–30 days of simulator or live calls.
- "What-if" AEP volume scenario produces believable margin numbers.

**Suggested Agent Role**: "Economics Agent" — primary sources are your grok-extract-telesales-pnl and masterBRIDGE analytics repos.

### Task 1.2: Sell Stream Buyer / Leadmarket Connection
**Context**: The sell path already produces clean `SellLeadPackage` with provenance and compliance proof. It has nowhere to go.

**Sub-tasks**:
- Connect to your real leadmarket instance or direct buyers (using the patterns from your `leadmarket` repo).
- Enforce buyer onboarding (license verification, PEWC contract, audit rights).
- Implement per-transfer PEWC proof + immutable logging (extend the existing hash chain).
- Add kill-switch + fallback if buyer quality or pricing collapses.

**Verification**:
- At least one real (or tightly controlled test) sell package successfully delivered to a buyer with full provenance.
- All data sharing is PEWC-documented and auditable.

---

## Phase 2 — Full Multi-Agent Orchestration as the Brain

**Goal**: Make your real `llm-router-engine` (MultiAgentOrchestrator) the active decision engine instead of the current high-fidelity simulation.

### Task 2.1: Compliance Gate as First Non-Bypassable WorkflowStep
**Context**: The adapter in `router_integration.py` already has the skeleton (`build_medicare_compliance_first_workflow`). The gate code is ready. This is the natural first use of the orchestrator.

**Sub-tasks**:
- Instantiate real `MultiAgentOrchestrator` with `regulatory_strict: true` and Medicare objectives.
- Make the Hard Compliance Gate the literal first `WorkflowStep` (is_parallel_group=false, required_capabilities=["regulatory_strict", "audit_trail"]).
- Wire real execution (not simulation) of the gate using the existing `apply_hard_compliance_gate`.
- Implement default replanning on low compliance score or handoff quality.
- Expose rich `get_workflow_metrics()` (including compliance-specific signals) back to the dashboard.

**Verification**:
- Simulator + any live calls now route through the real orchestrator for the gate step.
- Metrics show handoff quality, model churn, and compliance score per workflow.
- Zero bypasses possible (enforced in the workflow definition).

**Suggested Agent Role**: "Orchestrator Wiring Agent" — primary source is your `llm-router-engine` examples + the existing adapter.

### Task 2.2: Parallel Specialists + Real Agent Handoff
- After gate passes, run parallel specialists (licensed agent matcher, sell-buyer fit evaluator, AI pre-qual benefits screener using your `benefits-automator` patterns).
- Final synthesis step produces the dual-stream decision using the UVal scorer + orchestrator context.
- Handoff to real GHL TaskRouter (from Phase 0) with full provenance.

---

## Phase 3 — AEP Hardening & Scale Prep

**Goal**: Survive the highest-volume, highest-scrutiny period without compliance or margin collapse.

**Key Workstreams** (many can run in parallel):
- AEP surge policy + capacity modeling (agent + multi-agent system as force multiplier) — use masterBRIDGE capacity data.
- Full volume + compliance + margin war game using the simulator + real economics.
- Quarterly mock CMS 250-record audit pack generator (automated, using the existing hash chain + vault).
- Production observability + alerting (compliance score, margin, GHL latency, transcription quality).
- Multi-provider LLM abstraction + deterministic fallbacks for every voice/decision step.
- Meta-evals regression harness on real Medicare cases (using your llm-router-engine evals patterns).

**Verification Gates** (from your own roadmap):
- Successful AEP dry-run with all scenarios (volume spike, CAC spike, compliance failure, agent capacity shortfall).
- Dashboard matches business plan targets under stress.
- Automated 250-record audit pack generated cleanly in <48 hours with zero gaps.
- 100% recording rate sustained for 2+ weeks in a realistic load test.

---

## Cross-Cutting / Ongoing Requirements (Apply to Every Phase)

- **Strict Todo Discipline**: Every agent maintains its own live todo list with exactly one `in_progress` item. No batching of completions.
- **Verification Before Done**: No task is closed without runnable evidence (tests, simulator runs, or real call artifacts).
- **Moat Consolidation**: Prefer patterns from your 243-repo ecosystem over new invention. Document every extraction.
- **Red-Team Integration**: Every significant change must be reviewed against `RED_TEAM_REPORT.md`. Update the report with new findings.
- **Audit Artifact Completeness**: Every call, decision, and GHL interaction must produce a tamper-evident record.
- **MCP Tool Quality**: Any new MCP tool must have production-grade descriptions, input validation, and graceful degradation when GHL is unavailable.

---

## Suggested Orchestration Pattern (for llm-router-engine)

Use the existing `RealRouterAdapter` + `build_medicare_compliance_first_workflow` pattern:

1. Compliance Gate (first, non-parallel, regulatory_strict)
2. Parallel group (after gate passes):
   - Licensed agent matcher (masterBRIDGE data)
   - Sell-buyer fit evaluator (leadmarket + economics)
   - AI pre-qual / benefits screener (benefits-automator patterns)
3. Final synthesis + dual-stream decision (UVal + orchestrator metrics)
4. Handoff (GHL TaskRouter enqueue with full provenance)

Default replan on low compliance score or poor handoff quality.

Expose `get_workflow_metrics()` (including compliance-specific signals) to the dashboard.

---

**This plan is now the locked execution blueprint for the orchestrated multi-agent build.**

It is deliberately scoped to the items your own checklists and red-team identified as blocking a real pilot. Everything else is secondary until these are green with evidence.

Feed this document to your MultiAgentOrchestrator or spawn specialized sub-agents against the individual tasks.

Highest skill. Highest precision. Both streams. Market pilot.

Run it. Extend it. Ship the pilot.