# Twilio Console Configuration Checklist — Live Test Run

**Use this only with a dedicated test Twilio number. Never point production numbers until after successful military verification.**

## 1. Number Selection
- Buy or use a **test-only** Twilio number (different from any production Medicare numbers).
- Note the number and the Account SID.

## 2. Voice Configuration (Critical)

Go to: Twilio Console → Phone Numbers → Manage → Active numbers → [Your Test Number]

### Voice Webhook Settings
- **A Call comes in**:
  - Webhook URL: `https://YOUR_APP_URL/webhooks/twilio/voice`
  - HTTP Method: **POST**

- **Status Callback** (highly recommended):
  - Status Callback URL: `https://YOUR_APP_URL/webhooks/twilio/status`
  - Status Callback Method: **POST**
  - Status Callback Events: Select at minimum **Completed**, **Recording** (if using recordings)

### Advanced (Optional but Recommended for Full Test)
- Enable "Recording" under "Call Recording" if you want to test the full vault path.
- Set "Recording Status Callback" to the same `/webhooks/twilio/status` URL if desired.

## 3. Secrets You Must Have Configured in the App

```env
TWILIO_AUTH_TOKEN=your_real_auth_token_here          # NOT the dev-placeholder
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1the_test_number

GHL_API_TOKEN=your_real_ghl_token
GHL_LOCATION_ID=your_location_id
GHL_PHONE_CUSTOM_FIELD=lc_phone

COMPLIANCE_TEST_MODE=true                            # Safe live testing mode
```

## 4. Verification Before First Call

Run this command against your deployed app:

```bash
python scripts/verify_military_e2e.py
```

All assertions should pass before making the first real phone call.

## 5. After Testing

- Set `COMPLIANCE_TEST_MODE=false` (or remove the line) before using any production traffic.
- Point production numbers only after the client has signed off on the full audit trail and economics data from the test runs.

**Document the exact test number used and the date/time of each live test call.** This becomes part of your internal compliance record.