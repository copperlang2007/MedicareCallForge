# MedicareCallForge Architecture
**Version**: 0.1.0 (Production-Grade Design)
**Owner**: Grok (as if my own build)
**Date**: 2026-05-27
**Status**: Synthesized from exhaustive repo drill (masterBRIDGE, insureitall-os, ghl-twilio-smart-queue, leadmarket, benefits-automator, Agentshield266, Q, grok-extract series, flexivoice-pro, autoBLOG, full 243-repo ecosystem) + llm-router-engine + business plan requirements.

## 1. Executive Vision
MedicareCallForge is the **multi-agent operating system** for the exact business plan: compliant inbound-only Medicare call lead gen under $25K/mo with dual monetization.

- Stream 1 (Search/Google-Bing call-only): High-intent → licensed agents → in-house enrollment ($300-600 commission, <$150 CPA target).
- Stream 2 (Social FB/YouTube educational): Lower-intent → sell qualified calls at $25 (CAC <$18 for $7-15 margin).

Non-negotiable: 100% recording + 10yr vault, SOA before specifics, verbatim TPMO disclaimer on all assets, PEWC for any data share, CY2026 language access. Existing agency foundation (licenses, NPN, E&O, multi-state, basic phone/IVR) is leveraged, not rebuilt.

**Core Principle**: Your llm-router-engine (MultiAgentOrchestrator, UVal scoring, policy, real MCP, meta-evals) is the **first-class brain**. All other repos supply production primitives (compliance guardrails, GHL/Twilio routing, transcription, lead marketplace, agent orchestration, data pipelines). No greenfield where assets exist.

**Moat Consolidation**: The 243-repo ecosystem (masterBRIDGE as crown jewel with Power Dialer V2 patterns, etc.) is not scattered — it is a deliberate Medicare AI/automation platform. First action in this build: Extract best patterns into a "MedicareAI-Core" monorepo. Avoid duplication.

## 2. High-Level Architecture
**Layers** (all orchestrated via llm-router-engine MCP + MultiAgentOrchestrator):

1. **Telephony & Intake Layer** (GHL + Twilio as backbone)
2. **Hard Compliance Gate** (non-bypassable, first step)
3. **Qualification + Scoring** (UVal domain-specific)
4. **Routing & Handoff Orchestrator** (your MultiAgentOrchestrator)
5. **Dual Revenue Workflows** (Enroll vs Sell)
6. **Optimization & Flywheel** (economics, AEP, offline conversions)
7. **Audit Shield & Reporting** (CMS 250-record ready)
8. **Agent Assist & Human-in-Loop** (Claude + memory)

**Deployment**: Railway/Docker (your existing multi-stage assets), non-root, healthchecks. MCP server for Claude Desktop/Cursor ops.

**Observability**: Your get_workflow_metrics() + per-workflow compliance score + dual-stream PNL dashboard.

## 3. Detailed Components (Mapped to Repo Assets)

### 3.1 Telephony & Intake (GHL + Twilio Smart Queues)
- **Primary Source**: ghl-twilio-smart-queue (Playwright auto-config for GHL TaskRouter queues) + masterBRIDGE V2 Twilio/GHL patterns (Media Streams live transcription, webhooks, CRM sync).
- **Key Patterns**:
  - Custom GHL fields: licensed_states, carrier_appointments, current_availability, ghl_phone_number (from ghl script).
  - "Phone Dashboard" custom menu + "Call Center" dashboard embed for custom UI.
  - FastAPI backend for enqueue/assignment.
  - masterBRIDGE: Twilio SDK + Media Streams for real-time transcription + post-call Anthropic parsing. GHL sync (API + browser automation modes).
- **Integration with llm-router**: New MCP tool `route_inbound_call(from_number, contact_state, ivr_answers)`. Returns target_phone or queue decision. Triggers orchestrator immediately.
- **Why Best**: Handles state/licensing-aware routing (Medicare multi-state requirement). Inbound-only focus matches plan (no TCPA outbound risk).

### 3.2 Hard Compliance Gate (Non-Bypassable)
- **Primary Source**: insureitall-os (strict CMS audit engine + guardrails.py) + masterBRIDGE compliance.ts + Sovereign Agent.
- **Core Logic** (from guardrails.py + compliance.ts):
  - Required mentions/quotes for TPMO disclaimer (verbatim), SOA timing, PEWC, language access.
  - Scoring: compliance_score (deduct 25 for high-severity missing), quality_score.
  - Tamper-evident hash chain for every event (prev_hash + payload → SHA256).
  - masterBRIDGE: TCPA consent check, DNC block, state calling hours (8am-9pm local via timezone offsets), max_dial_attempts (10), re-dial_cooldown (2hrs), SOA tracking, disposition with COMPLIANCE category.
  - Sovereign: 20+ CMS/TCPA pattern scanner, audit logging.
- **MCP Tools**: `apply_compliance_policy(transcript_evidence, call_context)` → {compliance_score, flags, audit_hash, ready_for_next}.
- **Policy**: regulatory_strict (hard block on failure). 100% recording start + transcription before any routing.
- **Why Best**: Standalone, testable guardrails + production compliance primitives. Directly solves the plan's "non-negotiable" audit risk ($1K/day fines).

### 3.3 Qualification + UVal Scoring
- **Enhance your llm-router UVal** with Medicare dimensions:
  - Intent (keywords/IVR/pre-answers).
  - State licensing fit (from GHL custom fields).
  - Predicted LTV/enrollment prob (from grok-extract-telesales-pnl LSTM models + masterBRIDGE analytics).
  - Cost-to-serve + regulatory risk penalty.
- **Data**: grok-extract-telesales-12/ pnl for transcript analysis pipelines and forecasting.
- **Output**: Structured WorkflowRoutingDecision + rationale (your existing format).

### 3.4 Routing & Handoff Orchestrator (Your llm-router MultiAgentOrchestrator — First Class)
- Parallel groups for: best licensed human agent (state + load + historicals from masterBRIDGE), AI pre-qual voice (flexivoice-pro patterns), overflow-to-sale queue.
- Replanning on low handoff_quality or poor outcomes (your _default_replan).
- Metrics: handoff quality, model churn, cost efficiency, compliance_score (your get_workflow_metrics() extended).
- **Agent Framework**: Agentshield266 + Q patterns for shielded orchestration + compliance hooks. Extend with your MCP.

### 3.5 Dual Revenue Workflows
- **Enroll (Search Stream)**: SOA e-sig (before specifics) → plan comparison (tie to your Mediflow/BRIDGEt) → handoff to best agent or AI assist (masterBRIDGE Claude memory) → enrollment + offline conversion to Google.
- **Sell (Social Stream)**: leadmarket patterns — qualify sellable, package (consent proof + provenance), list/sell at $25 via marketplace or direct API. Real-time WS, duplicate protection.
- **MCP**: `sell_overflow_call(call_context, consent_proof)`.

### 3.6 Optimization & Flywheel
- Offline conversions (your APScheduler jobs).
- Lookalikes from enrolled (no PHI).
- AEP surge policy + budget rules.
- Economics dashboard: grok-extract-telesales-pnl LSTM + masterBRIDGE analytics (separate streams: search enroll revenue vs social sell margin).
- Content: autoBLOG for educational ad creative.

### 3.7 Audit Shield & Reporting
- Auto 250-record CMS packs (insureitall-os + masterBRIDGE audit + vault export).
- Near real-time risk flagging.
- 10-year vault (MinIO/S3 + hash chain).

### 3.8 MCP Surface & Agent Assist (Your Existing MCP Server Extended)
- Tools listed above + benefits-automator eligibility screening.
- Claude Desktop integration for ops.
- Agent assist: masterBRIDGE per-user memory + SSE.

## 4. Tech Stack (Minimal New Invention)
- Orchestration: Your llm-router-engine (core).
- Telephony/CRM: GHL + Twilio (from ghl script + masterBRIDGE).
- Compliance/Audit: insureitall-os + masterBRIDGE.
- Marketplace: leadmarket.
- Voice: flexivoice-pro + masterBRIDGE.
- Agent Framework: Agentshield266/Q + your orchestrator.
- Data: grok-extract pipelines + PostgreSQL (Drizzle patterns).
- LLM: Claude (assist) + local Ollama (guardrails) + your router.
- Deployment: Your Railway/Docker + healthchecks.

## 5. Data Model Highlights (From Repos)
- Leads/Calls/Transcripts/Dispositions (masterBRIDGE + leadmarket schemas).
- Audit Events (hash chain from insureitall).
- User/Agent Profiles with licensed_states (GHL fields).
- Orders/Wallets for selling (leadmarket).

This architecture is **defensible, observable, and compliant by construction**. It turns your scattered 243-repo moat into a single product that hits every KPI in the business plan while exceeding CMS audit requirements.

Next: Proceed to full phased build plan with verification gates (as if my build — ruthless, production-grade). No low-leverage work. Highest precision on compliance and economics first.