# MedicareCallForge — Client Live Test Quick Reference Card

**One-page cheat sheet for safe live test runs (print or keep open during testing)**

## 1. Before Any Live Call
- Run `python scripts/verify_military_e2e.py` against the deployed app → must be all green.
- Confirm `COMPLIANCE_TEST_MODE=true` is set (and will be turned off after testing).
- Use only a dedicated **test Twilio number** (never production).

## 2. For the First 5–10 Real Phone Calls
Use the exact script in `LIVE_TEST_CALLER_SCRIPT.md`.

Key lines the caller must deliver clearly:
- "This call is being recorded for compliance..."
- "We do not offer every plan... multiple carriers."
- Scope of Appointment confirmation before any plan talk.
- PEWC consent.
- Language access notice.

## 3. What Success Looks Like (Dashboard & GHL)
- Brain Intelligence panel shows the new decision with rationale and any divergence from local UVal.
- GHL contact has:
  - Note containing "Brain Rationale"
  - lc_phone (or your exact field) populated
  - last_medicare_* custom fields updated
- Audit Vault has the `brain_routing_decision` event chained after the compliance gate.
- Economics data updated (stream, uval, etc.).

## 4. If the Gate Blocks the Call
This is **correct behavior**. The caller did not deliver the required disclosures. Re-run with the full script.

## 5. After Testing Session
1. Set `COMPLIANCE_TEST_MODE=false` in the environment.
2. Export the audit pack for the test period.
3. Review results with the team using `PILOT_LAUNCH_READINESS_CHECKLIST.md`.
4. Only then point production numbers.

**Golden Rule**: Every real call must still produce a complete, tamper-evident audit trail — even in test mode.

Keep this card + the full Live Test Run Runbook open during the first live test day.