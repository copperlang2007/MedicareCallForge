# MedicareCallForge Pilot Wiring Guide — Live GHL + Twilio + lc_phone

**Purpose**: Exact steps to point your real GHL/Twilio production numbers at MedicareCallForge so real inbound calls flow through the Hard Compliance Gate + live MultiAgentOrchestrator brain + dual-stream routing (enroll_in_house vs sell_call), with 100% recording, tamper-evident audit, rich TaskRouter attributes, and GHL lc_phone + outcome sync.

This is Phase 0.1 of AGENT_ORCHESTRATED_BUILD_PLAN.md. Do this before any ad spend.

## 1. Confirm Your GHL Custom Fields (lc_phone is non-negotiable)

Your client uses **"lc phone"** (internal key often `lc_phone` or `lc phone`).

In MedicareCallForge this is driven by one env var:

```env
GHL_PHONE_CUSTOM_FIELD=lc_phone
```

**Verification**:
- In GHL → Settings → Custom Fields (or via contact), confirm the field that holds the agent's LC / phone number for routing.
- The system already handles both `lc_phone` and `lc phone` (with space) in `_get_ghl_phone_number` and update paths.
- MCP tools (`ghl_update_medicare_custom_fields`, etc.) and `update_medicare_custom_fields` write the phone value to whatever you set in `GHL_PHONE_CUSTOM_FIELD`.

Run this to test from your machine (after setting real GHL_* env):

```bash
python -c "
from medicare_call_forge.ghl.client import ghl_client
print('GHL enabled:', ghl_client.enabled)
print('Location:', ghl_client.location_id)
# Find a test contact and write lc_phone
c = ghl_client.search_contact_by_phone('+15551234567')
if c:
    ok = ghl_client.update_medicare_custom_fields(c['id'], ghl_phone_number='+15551234567')
    print('lc_phone write success:', ok)
"
```

## 2. Twilio Number + Webhook Configuration (Production)

In Twilio Console → Phone Numbers → Manage → Active numbers:

- Select the number that receives Medicare inbound calls.
- Voice Configuration:
  - **Webhook URL**: `https://<your-railway-or-domain>/webhooks/twilio/voice`
  - **HTTP Method**: POST
  - **Status Callback URL**: `https://<your-railway-or-domain>/webhooks/twilio/status` (or append `?compliance_hash=...` if you want to pass it)
  - **Status Callback Method**: POST

**Critical env vars on the deployed service** (Railway / Docker / .env):

```env
TWILIO_AUTH_TOKEN=your_real_auth_token_from_twilio_console   # REQUIRED for signature validation in prod
TWILIO_ACCOUNT_SID=AC...
TWILIO_PHONE_NUMBER=+1the-real-number
TWILIO_ENROLL_WORKFLOW_SID=WW...   # Create in TaskRouter (see below)
TWILIO_SELL_WORKFLOW_SID=WW...     # Create in TaskRouter (see below)
MEDIA_STREAM_WS_URL=wss://your-transcription-service/stream   # optional but recommended (masterBRIDGE pattern)

GHL_API_TOKEN=...
GHL_LOCATION_ID=...
GHL_PHONE_CUSTOM_FIELD=lc_phone
```

**Signature validation**: The handler calls `_validate_twilio_signature`. In prod the placeholder must be replaced — otherwise it logs a warning and accepts everything (dev only).

## 3. TaskRouter Workflows (Two Streams — Enroll vs Sell)

From your ghl-twilio-smart-queue + masterBRIDGE patterns, create two Workflows in Twilio TaskRouter:

### Enroll Workflow (high-intent search calls → licensed agents)
- Name: `MedicareCallForge-Enroll`
- Use the rich attributes already sent by the handler:
  ```json
  {
    "compliance_hash": "...",
    "uval": 0.78,
    "intent": "enroll",
    "state": "CA",
    "licensed_states": ["CA","TX"],
    "carrier_appointments": ["UHC","Aetna"],
    "current_availability": "Available",
    "ghl_phone_number": "+1555...",
    "compliance_score": 94.2
  }
  ```
- Routing: Skills-based on `licensed_states` + `carrier_appointments` + availability (use your existing masterBRIDGE agent data as Workers).

### Sell Workflow (social/educational overflow → $25 sell path)
- Name: `MedicareCallForge-Sell`
- Same attribute schema.
- Routing: Lower priority queue or direct to sell-buyer integration / follow-up sequence (leadmarket provenance already attached).

Set the two SIDs in the env vars above.

When both SIDs are present, the handler will do real `<Enqueue><Task attributes="...">` for both streams (no Dial fallback).

## 4. Media Streams (Live Transcription — masterBRIDGE V2)

If you have a transcription WebSocket (Deepgram, AssemblyAI, or your own):

```env
MEDIA_STREAM_WS_URL=wss://your-service.com/twilio-stream
```

The handler will start the Stream **before** Enqueue on enroll calls (compliance_hash and callSid are passed as parameters).

## 5. End-to-End Test Checklist (Real Calls — Evidence Required)

Before declaring Phase 0 Green:

1. Point a test Twilio number at the webhook URLs (or use GHL Studio function forward).
2. Make 10–20 real test calls (mix of high-intent "medicare advantage" phrasing and low-intent educational).
3. Verify for **every** call:
   - 100% recording URL appears in Twilio + vault audit event.
   - Tamper-evident `compliance.audit_hash` chain entry.
   - TaskRouter (or fallback) receives the full attribute payload (check logs or Task Inspector).
   - GHL contact for the caller shows:
     - The lc_phone (or whatever `GHL_PHONE_CUSTOM_FIELD` points to) updated.
     - A note with Decision / UVal / Compliance Score / Audit Hash / Recording URL.
   - Dashboard (if wired) shows the live event.
4. Confirm live brain is active: in logs you should see `Real MultiAgentOrchestrator wired` and the voice path preferring the adapter when `_orchestrator` is present.
5. No crashes on `/status` (the previous undefined-variable bug is fixed).

## 6. Production Hardening Quick List

- Never deploy with `TWILIO_AUTH_TOKEN=dev-placeholder...`
- Set `MEDIA_STREAM_WS_URL` only after the WS is hardened (PHI considerations).
- Add rate limiting / bot detection on the public webhook if exposing directly (Twilio itself provides some protection via signature).
- For sell stream: wire the `SellLeadPackage` + provenance into your real buyer/leadmarket endpoint (PEWC immutable proof required).
- Monitor `/health` + dashboard + audit vault export before scaling calls.

## 7. Rollback / Kill Switches

- Set `TWILIO_ENROLL_WORKFLOW_SID` and `TWILIO_SELL_WORKFLOW_SID` to empty → automatic graceful Dial fallback (still records + vaults + logs to GHL).
- The Hard Compliance Gate can never be bypassed (even on fallback).

---

**When this guide is executed with real numbers and 50+ calls pass the verification criteria above, Phase 0 is unblocked.**

Update this file with your actual SIDs, exact custom field keys, and test call dates as you go. Feed the results back into the live MultiAgentOrchestrator via the feeder for metrics.

References:
- AGENT_ORCHESTRATED_BUILD_PLAN.md (Phase 0.1)
- masterBRIDGE compliance.ts + Media Streams patterns
- ghl-twilio-smart-queue Playwright + TaskRouter attribute schema
- Current `telephony/inbound_handler.py` + `ghl/client.py` (lc_phone aware everywhere)

Last updated: after "wire real live" + production path fixes (status scope + live brain preference in voice handler).