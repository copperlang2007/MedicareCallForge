# MedicareCallForge — Pilot Launch Readiness Checklist

**Military-Grade Go / No-Go Document for Controlled Market Pilot**

Use this checklist with your client before turning on any real ad spend or production numbers.

## Phase 0 — Infrastructure & Secrets (Must Be Green)
- [ ] App deployed to Railway / equivalent with real secrets (no dev placeholders)
- [ ] `COMPLIANCE_TEST_MODE=false` for any production traffic
- [ ] Real GHL_API_TOKEN + GHL_LOCATION_ID configured and working
- [ ] `GHL_PHONE_CUSTOM_FIELD=lc_phone` (or exact client field) verified in GHL
- [ ] Dedicated production Twilio number(s) with webhooks pointed correctly
- [ ] TWILIO_ENROLL_WORKFLOW_SID and/or SELL_WORKFLOW_SID configured (or intentional graceful fallback documented)

## Phase 1 — Compliance & Audit (Non-Negotiable)
- [ ] Hard Compliance Gate passes 100% of required evidence in simulated + live test calls
- [ ] Full audit chain visible: `compliance_gate` → `brain_routing_decision` → `recording_vaulted`
- [ ] Tamper-evident hashes working and exportable via `/audit/vault`
- [ ] Brain rationale and decision provenance captured in every audit event and GHL note
- [ ] COMPLIANCE_TEST_MODE artifacts (if used) clearly marked in audit records

## Phase 2 — Brain & Decisioning
- [ ] Live `MultiAgentOrchestrator` is wired and returning authoritative decisions
- [ ] Brain Intelligence panel in dashboard shows real decisions, rationales, and divergences
- [ ] Brain vs local UVal divergence is being logged and visible
- [ ] `get_workflow_metrics()` (handoff quality, cost efficiency, etc.) is being captured

## Phase 3 — Dual-Stream Economics & Observability
- [ ] Real dual-stream economics flowing into dashboard (not stubs)
- [ ] Historical series and trends visible in charts
- [ ] `check_thresholds()` and AEP `what_if_aep_scenario()` returning usable data
- [ ] Margin / CAC / compliance alerts wired and tested
- [ ] Economics data appears correctly after both simulated and live test calls

## Phase 4 — GHL Integration (lc_phone & Operational Loop)
- [ ] `lc_phone` (or exact client field) is being read and written correctly on every call
- [ ] `log_medicare_call_outcome` is creating notes with brain rationale + compliance proof
- [ ] Custom fields (licensed_states, carrier_appointments, current_availability) are updating
- [ ] MCP tools (if using Claude/Cursor) are working against real GHL location

## Phase 5 — Testing & Verification (Military Standard)
- [ ] `scripts/verify_military_e2e.py` passes cleanly against current deployment
- [ ] At least 15–20 simulated test calls executed with full data trail
- [ ] At least 5–10 live test calls executed on dedicated test number using the approved caller script
- [ ] All artifacts verified: dashboard, GHL contacts, audit vault, economics, brain panel
- [ ] Client has reviewed and signed off on the Live Test Run Runbook results

## Phase 6 — Documentation & Client Handover
- [ ] Client has received and understands:
  - PILOT_WIRING_GUIDE.md
  - LIVE_TEST_RUN_RUNBOOK.md
  - TWILIO_CONSOLE_CHECKLIST.md
  - LIVE_TEST_CALLER_SCRIPT.md
- [ ] Internal team has the military verification harness and knows how to run it post-deploy
- [ ] Go-Live decision recorded with date, approvers, and any open risks

## Final Go / No-Go Decision

**Status:** [ ] GO for controlled pilot   |   [ ] NO-GO (list blockers below)

**Blockers / Open Items:**

1. 
2. 

**Approved By:** ___________________________   Date: ___________

---

**This checklist is the single source of truth for pilot launch readiness.**

Run the full military verification harness + review this document with the client before flipping any production switches.