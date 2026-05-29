# Live Test Phase — Ops & Dashboard Training Guide
**One-pager for client's ops, sales, and leadership team**

**Goal**: Safely run real phone test calls, understand what the brain is doing, and know exactly what "good" looks like in the dashboard before scaling.

## 1. Before the First Live Test Call (Ops Checklist)
- Confirm with tech lead: `COMPLIANCE_TEST_MODE=true` is set on the deployed app.
- Use only the dedicated **test Twilio number** (never production numbers).
- Have the approved caller script ready (see LIVE_TEST_CALLER_SCRIPT.md).
- Run the smoke test first: `python scripts/post_deploy_smoke_test.py`
- Run the full military harness: `python scripts/verify_military_e2e.py` (must be all green).

## 2. During a Live Test Call — What to Watch in the Dashboard
Open the dashboard (`/dashboard`) in a separate tab before dialing.

**Key Tabs to Monitor:**
- **Overview**: Watch total calls, compliance score, and the two stream KPI cards update in near real-time.
- **Live Operations**: New row appears within seconds of call end with decision, compliance, UVal.
- **Brain & Routing (most important)**:
  - "Brain Intelligence" panel shows the new decision.
  - Look for:
    - **Brain Decision** vs **Local UVal** columns
    - **DIVERGENCE** flag (yellow = brain and local UVal disagreed — this is valuable signal)
    - Brain Rationale (click row for full text + raw brain metrics like handoff quality)
  - Agreement rate and recent divergences update automatically.

- **Audit Vault**: New events appear (especially `brain_routing_decision` with full provenance).

## 3. What "Good" Looks Like on a Test Call
- Gate passes (or correctly blocks if caller didn't deliver required language — this is working as designed).
- Brain makes a clear recommendation (enroll or sell) with rationale.
- GHL contact is updated with lc_phone + note containing brain rationale and compliance hash.
- Economics data lands in the dashboard (you'll see the call contribute to the correct stream).
- If COMPLIANCE_TEST_MODE is on, you will see a clear warning in logs and a low-severity flag in the audit event — this is expected and safe.

## 4. Red Flags to Stop and Escalate Immediately
- Gate passes when it shouldn't (missing disclosures but still routes) → test mode may be misconfigured.
- Brain rationale is empty or nonsense.
- No GHL contact update or missing lc_phone.
- Critical alerts firing in economics (CAC breach, margin kill-switch) on test volume.
- Divergence rate > 30% with no clear pattern (discuss with tech lead).

## 5. After the Test Call Session
1. Export the full audit pack for the session (`/audit/vault` → Export button).
2. Review in GHL: every test contact should have proper notes and custom fields.
3. Debrief: What did the brain get right/wrong? Any patterns in divergences?
4. When ready to stop testing: Ask tech lead to set `COMPLIANCE_TEST_MODE=false`.

## 6. Quick Commands (for whoever is running the tests)
```bash
# After any deploy
python scripts/post_deploy_smoke_test.py

# Before/after a batch of live test calls
python scripts/verify_military_e2e.py
```

**This guide + the Live Test Run Runbook is everything the ops/sales team needs for the controlled live test phase.**

Keep this card open during test days. Questions → escalate to the technical owner running the brain and compliance systems.