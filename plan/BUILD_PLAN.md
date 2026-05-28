# MedicareCallForge — Production-Grade Build Plan
**Treated as my own build. Strict engineering-execution discipline enforced throughout.**
**Base**: llm-router-engine (your existing MultiAgentOrchestrator, UVal, policy, MCP, meta-evals, deployment assets) + consolidated assets from 243-repo ecosystem.
**Goal**: Ship a fully tested, CMS-audit-ready, economically precise system that hits the exact business plan numbers with zero shortcuts.
**Verification Bar**: Nothing marked complete without evidence (tests passing + real artifacts + metrics + docs updated).

## Phase 0: Compliance & Licensing Baseline + Moat Consolidation (Highest Leverage — 4-6 Weeks)
**Why First**: The plan's non-negotiables (100% recording, SOA timing, verbatim TPMO, PEWC) are the #1 failure mode. Your existing agency foundation is the advantage — compress 4-6 months of setup into weeks. Consolidate the moat before writing new code.

**Tasks (with Verification)**:
1. Execute business plan Phase 1 exactly:
   - TPMO registration with all target carriers + FMO.
   - AHIP + carrier certifications for every agent who will touch calls.
   - Multi-state non-resident licenses via NIPR.
   - 10-year call recording vault (auto-start, AI transcription linked to CRM, CMS-accessible export, MinIO/S3 storage).
   - CRM + SOA e-signature workflow (test 100% timing on samples).
   - All landing pages, ad copy, scripts audited for verbatim TPMO + CY2026 language access notice + per-channel tracking numbers.
2. Moat Consolidation (do this in parallel — highest ROI):
   - Create MedicareAI-Core monorepo (structure already created in C:\Users\lang2\MedicareCallForge).
   - Extract:
     - Compliance primitives: insureitall-os/quality/cms_audit_guardrails.py + masterBRIDGE artifacts/.../compliance.ts + Sovereign scanner.
     - Telephony: ghl-twilio-smart-queue/setup_ghl_twilio_refined.py + masterBRIDGE Twilio/GHL patterns (Media Streams, webhooks, CRM sync).
     - Marketplace: leadmarket core (schema, API, Stripe wallet, WS).
     - Agent framework: Agentshield266 + Q (skills, orchestration, shielding).
     - Data pipelines: grok-extract-telesales-* (transcript analysis, lstm_forecaster.py for PNL).
     - Voice: flexivoice-pro voice_director + masterBRIDGE transcription.
     - Content: autoBLOG.
   - Create shared types (from masterBRIDGE/leadmarket Drizzle schemas adapted).
   - Remove duplication. Version the core.
3. Verification Gates (evidence required before moving on):
   - 100% of 50+ sample calls have: recording started + correct verbatim disclaimer + language notice + SOA signed *before* any plan specifics.
   - FMO sign-off on full compliance pack.
   - Run insureitall-os guardrails tests + masterBRIDGE compliance checks (all pass).
   - Moat monorepo has clean extraction of top 5 primitives with tests/docs.
   - No ad spend approved until all gates Green. Document: Compliance Matrix + Moat Inventory.

**Tools/Repos Used**: insureitall-os, masterBRIDGE, ghl-twilio-smart-queue, leadmarket, Agentshield266, grok-extract series, flexivoice-pro, autoBLOG, your existing deployment scripts.

## Phase 1: Telephony + Intake Router + Hard Compliance Gate (3-4 Weeks)
**Why Next**: Get real calls flowing through the brain with zero compliance leakage. This unblocks everything else.

**Tasks**:
1. Extend ghl-twilio-smart-queue + masterBRIDGE patterns into llm-router MCP:
   - New tool: `route_inbound_call(from_number, contact_state, ivr_answers)`.
   - GHL custom fields + TaskRouter smart queues (state/licensing aware).
   - "Phone Dashboard" + Call Center embeds.
   - Twilio Media Streams live transcription + post-call parsing (masterBRIDGE).
2. Embed Hard Compliance Gate as first orchestrator step (non-bypassable):
   - Port guardrails.py + compliance.ts logic.
   - Tamper-evident hash chain on every event.
   - Policy: regulatory_strict (hard block + audit log).
   - 100% recording + transcription start before routing decision.
3. Integrate benefits-automator as MCP tools for eligibility screening during calls.
4. Verification:
   - End-to-end test call from ad click → recording in vault with correct scoring/disclaimer/SOA timing + audit_hash + compliance_score > 95.
   - Metrics logged via your get_workflow_metrics().
   - Guardrails tests + masterBRIDGE compliance unit tests all pass.
   - MCP tool callable from Claude Desktop.

**Repos Integrated**: ghl-twilio-smart-queue, masterBRIDGE, insureitall-os, benefits-automator, your llm-router-engine.

## Phase 2: Multi-Agent Orchestration Core + Qualification/Scoring (3-4 Weeks)
**Core Brain Activation**.

**Tasks**:
1. Extend your MultiAgentOrchestrator:
   - WorkflowSteps for full lifecycle (parallel routing groups for best licensed agent vs AI pre-qual vs overflow queue).
   - Dependencies + automatic replanning on low handoff_quality or poor compliance/outcomes (your existing _default_replan + rich WorkflowOutcome).
2. Domain UVal Scorer (enhance your existing):
   - Medicare dimensions: intent, state licensing fit (GHL fields), LTV from grok-extract-pnl LSTM, cost-to-serve, regulatory risk.
   - Lightweight LLM judge (use your meta-evals harness, seed with extracted telesales data).
3. Wire Agentshield266/Q patterns for shielded multi-agent orchestration + compliance hooks.
4. Verification:
   - 100+ simulated + real calls through full orchestrator.
   - 100% gate pass rate.
   - get_workflow_metrics() shows meaningful handoff quality, cost efficiency, compliance score.
   - New integration tests (modeled on your prior test_mcp_integration.py).

**Repos**: Your llm-router-engine (first-class), Agentshield266, Q, grok-extract series, masterBRIDGE analytics.

## Phase 3: Dual Revenue Workflows + Selling Layer (3-4 Weeks)
**Hit the Business Plan Economics**.

**Tasks**:
1. Enrollment Workflow (Search Stream):
   - SOA e-sig before specifics.
   - Plan comparison (tie to your existing Mediflow/BRIDGEt data).
   - Handoff to best agent or AI assist (masterBRIDGE Claude memory + SSE).
   - Enrollment + offline conversion push to Google.
2. Overflow Sale Workflow (Social Stream):
   - Qualification for sellable.
   - Packaging with consent proof + provenance (masterBRIDGE + leadmarket).
   - Listing/sale at $25 via leadmarket marketplace or direct API.
   - Real-time WS, duplicate protection.
3. Separate stream metrics (exactly as business plan requires).
4. Verification:
   - Full end-to-end for both streams on 100+ calls.
   - Margin math holds in simulation (social CAC <$18 at $25 sell price).
   - All compliance artifacts attached to every record.
   - leadmarket-style flows tested with real (anonymized) data.

**Repos**: leadmarket, masterBRIDGE, your orchestrator, grok-extract for qualification signals.

## Phase 4: Flywheel, AEP Readiness, Dashboards, Self-Improvement (4-6 Weeks)
**Make the System Learn and Scale**.

**Tasks**:
1. Offline conversion jobs (your APScheduler) + lookalikes (no PHI).
2. AEP-specific policy + budget surge rules + full dry-run simulation.
3. Real dashboard (your FastAPI service):
   - Live workflows, per-workflow compliance score, stream-specific KPIs (search cost/enrollment, social sell margin, etc.).
   - Recommendations from metrics.
4. Meta-evals regression (your harness) on Medicare cases (seed with grok-extract data + few-shot).
5. Economics dashboard: grok-extract-telesales-pnl LSTM + masterBRIDGE analytics.
6. Verification:
   - Successful AEP dry-run (volume + cost spike handled).
   - Dashboard objectively matches business plan targets.
   - Evals show measurable improvement over baseline.
   - All prior checklists Green.

**Repos**: grok-extract series, masterBRIDGE, your llm-router-engine jobs + dashboard.

## Phase 5: Production Hardening, Deployment, Audit Shield (Parallel + Ongoing)
**Ship Like You Mean It**.

**Tasks**:
1. Full deployment using your existing Railway/Docker assets (multi-stage, non-root, healthchecks, COPY for llm_router + plugins + pyproject).
2. AI compliance monitoring (near real-time flagging via guardrails + masterBRIDGE scanner).
3. 10-year vault export + quarterly self-audit pack generator (250-record CMS style, using insureitall-os + masterBRIDGE audit logging).
4. Human-in-loop escalation for edge cases.
5. Full red-team of entire system (see separate report).
6. Verification:
   - 100% recording rate in production for 2+ consecutive weeks.
   - Successful mock CMS audit pack.
   - All your prior production checklists (from llm-router-engine work) Green.
   - No secrets in source, full audit trail.

## Testing Strategy (Your Standards + Domain)
- Unit: Your pytest + guardrails tests + compliance.ts tests.
- Integration: Transcript + compliance + routing + selling flows (modeled on your test_mcp_integration.py).
- Meta-evals: Your existing harness + new Medicare workflow cases (ORCH-03/04 style) + LLM judge strengthened with repo data.
- Load/AEP: Dry-runs with volume + cost spikes.
- Compliance: 100% recording + artifact checks on every test run.
- Security: Your existing hooks + secret scanning on all extracted code.

## Documentation (Part of the Work)
- All phases produce updated docs in the structure (already created).
- Runbooks for GHL/Twilio setup, audit pack generation, AEP surge.
- Compliance Matrix (living doc).

**Exit Criteria for Entire Build**: System handles real production volume with 100% compliance on every call, separate stream profitability visible and matching plan, ready for controlled ad spend ramp, all todos closed with evidence, red-team mitigations implemented or accepted with plan.

This is the plan I would execute if it was my company and my money on the line. Highest precision on compliance and economics first. No low-leverage work.

Next decision (executing immediately as my build): Advance to red-team synthesis and begin writing the first production code skeleton (Compliance Gate MCP tool) in the src/ structure. No waiting.