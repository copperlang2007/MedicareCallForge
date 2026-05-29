# Recommended Live Test Caller Script

**Purpose**: Exact language a test caller should read when making live phone calls to a test Twilio number.

This script is written to satisfy the **Hard Compliance Gate** requirements (TPMO verbatim, SOA before specifics, recording notice, PEWC, language access).

Use this script for initial live test runs when `COMPLIANCE_TEST_MODE=true`.

---

**Test Caller Script (Read Verbatim)**

"Hi, this is a test call for MedicareCallForge system verification.

This call is being recorded for compliance and quality assurance.

We do not offer every plan in your area. We represent multiple carriers.

Before we discuss any specific Medicare plans, I need to confirm a Scope of Appointment. Do you authorize me to discuss Medicare Advantage plans with you today?

[Wait for verbal yes]

Thank you. This call is being recorded.

We also need your permission to share your information with MedicareCallForge for the purpose of this test. Is that okay?

[Wait for verbal yes]

We offer language assistance services in English and Spanish at no cost. Do you need an interpreter or any other language help today?

Thank you. This completes the required disclosures for this test call."

---

### Notes for the Test Caller

- Speak clearly and at normal pace.
- Pause after each required disclosure and wait for acknowledgment where indicated.
- The system will detect the key phrases via early speech or Media Stream.
- After the script, you may say anything (or hang up) — the gate should have already passed.

### When to Use the Script vs Free Conversation

- Use the full script for the **first 3–5 live test calls** while validating the full chain.
- Once you confirm the gate + brain + GHL + vault are all working, you can do more natural conversation tests (the system will still enforce the gate on every call).

### Pro Tip

Record your test calls on your end as well. This creates a secondary audit trail for the client during the test phase.