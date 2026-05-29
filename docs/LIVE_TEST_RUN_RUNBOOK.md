# Live Test Run Runbook — MedicareCallForge

**For Client Use Only**  
**Military-Grade Controlled Test Protocol**

## Objective
Safely perform real phone call tests against the production intake system to validate:
- Hard Compliance Gate
- Live MultiAgentOrchestrator brain decisions
- Full audit trail (including brain rationale)
- GHL integration (lc_phone + outcomes)
- Economics recording and alerts
- Dashboard Brain Intelligence panel

## Prerequisites (Must Be Completed First)

1. App deployed with real credentials
2. `COMPLIANCE_TEST_MODE=true` set in environment
3. Dedicated test Twilio number configured (see TWILIO_CONSOLE_CHECKLIST.md)
4. Test GHL contact exists with `lc_phone` custom field populated
5. Military verification harness has been run successfully:
   ```bash
   python scripts/verify_military_e2e.py
   ```

## Test Protocol

### Phase 1 — Simulated Tests (Dashboard)
- Perform 10–15 simulated test calls via the dashboard "TRIGGER TEST CALL" button.
- Verify in real time:
  - Brain Intelligence panel updates
  - Economics data appears
  - Audit vault shows `brain_routing_decision` events
  - GHL contact receives notes + custom fields

### Phase 2 — Live Phone Tests (Recommended Sequence)

**Test Caller**: Use the exact script in `LIVE_TEST_CALLER_SCRIPT.md`

| Call # | Caller Type          | Expected Outcome                          | Verification Points |
|--------|----------------------|-------------------------------------------|---------------------|
| 1–3    | Scripted (full language) | Full gate pass + brain decision + GHL sync | All artifacts present |
| 4–6    | Natural conversation | Gate may block or pass depending on language | Observe blocking behavior |
| 7–10   | High-intent phrasing   | Brain should prefer `enroll_in_house`     | Check divergence vs local UVal |
| 11–15  | Educational phrasing   | Brain should prefer `sell_call`           | Check sell path + provenance |

### After Each Live Call
1. Immediately check the dashboard → Brain Intelligence panel
2. Open the contact in GHL and verify:
   - Note contains brain rationale
   - `lc_phone` field is populated
   - Custom fields updated
3. Check Audit Vault for the new `brain_routing_decision` event
4. Confirm economics record appears with correct stream

## Safety Rules

- Only use the dedicated test Twilio number.
- Never enable `COMPLIANCE_TEST_MODE` on production traffic.
- Document every live test call (time, caller, number used, observed outcome).
- If any critical alert fires (margin kill-switch, etc.), stop testing and investigate.

## Rollback / Cleanup

After testing is complete:
1. Set `COMPLIANCE_TEST_MODE=false`
2. Point any production numbers only after client sign-off
3. Export the full audit pack from the test period for internal records

## Success Criteria (Client Sign-Off)

- [ ] 15+ simulated calls with full data in dashboard
- [ ] 10+ live phone calls with brain decisions visible
- [ ] Brain Intelligence panel shows both enroll and sell decisions with rationales
- [ ] GHL contacts show correct lc_phone + brain rationale in notes
- [ ] Full audit chain (compliance_gate → brain_routing_decision → recording_vaulted) visible and exportable
- [ ] Economics data and at least one AEP scenario projection visible
- [ ] No unexpected critical alerts during testing

---

**Document Version**: 1.0  
**Prepared for**: Client Live Test Phase  
**Next Step**: Production traffic only after client approval of this runbook.