# MedicareCallForge — Market Pilot Checklist

**Status**: Core E2E dual-stream system with Hard Compliance Gate is **DELIVERED** and runnable.

Use this checklist to go from current state to a real controlled pilot with both revenue streams active.

## Pre-Pilot (Do These Before Turning on Real Ad Spend)

- [ ] Real GHL + Twilio webhook integration (use ghl-twilio-smart-queue + masterBRIDGE patterns)
- [ ] Live agent handoff implemented (GHL TaskRouter + masterBRIDGE routing)
- [ ] Production economics dashboard live (replace stub with grok-extract-pnl + masterBRIDGE analytics)
- [ ] Sell stream connected to real buyers or leadmarket instance
- [ ] Full red-team mitigations executed (see RED_TEAM_REPORT.md)
- [ ] AEP capacity + compliance war game passed
- [ ] Operator training complete using the simulator + runbooks
- [ ] Monitoring/alerting in place for compliance score drops and margin thresholds
- [ ] Legal / FMO review of sell-stream buyer contracts and data sharing

## Current State (What You Can Run Today)

- Hard Compliance Gate (production version)
- UVal Scorer for dual-stream decisions
- Both revenue streams fully wired in the FastAPI service
- Audit trail + tamper-evident hashing
- Simulator that demonstrates both paths
- Docker + Railway deployment ready
- Router integration adapter for your llm-router-engine

## Verification (Run This Locally)

```powershell
cd C:\Users\lang2\MedicareCallForge
pip install -e ".[dev]"
uvicorn src.medicare_call_forge.app:app --reload

# In another terminal:
python examples/full_flow_simulator.py
# or
.\verify_both_streams.ps1
```

You should see:
- One high-intent path routed to `enroll_in_house`
- One social/overflow path routed to `sell_call` with a packaged lead

## Next Autonomous High-Leverage Work (If Continuing the Build)

1. Production GHL webhook adapter + signature verification
2. Live handoff to agents (GHL + Twilio TaskRouter)
3. Real economics dashboard (grok-extract-pnl + masterBRIDGE analytics)
4. Full llm-router-engine wiring as the brain
5. AEP surge policy + dry-run tooling

**This foundation is the highest-precision starting point possible from your moat.**

Run it. Extend it. Ship the pilot.

No low-leverage work. Highest skill and precision maintained.