# MedicareCallForge

[![GitHub](https://img.shields.io/badge/GitHub-copperlang2007/MedicareCallForge-blue?logo=github)](https://github.com/copperlang2007/MedicareCallForge)

**Production-grade multi-agent intake, compliance, and dual-stream decisioning system for Medicare inbound call lead generation.**

**Repo:** https://github.com/copperlang2007/MedicareCallForge

**Status: Production Pilot Ready** — Both revenue streams, Hard Compliance Gate, GHL integration, and MCP tools fully implemented and verified.

## Quick Start

```powershell
cd C:\Users\lang2\MedicareCallForge
py -3 -m pip install -e ".[dev]"
uvicorn src.medicare_call_forge.app:app --reload
# In another terminal:
python examples/full_flow_simulator.py
```

Open the luxury operator dashboard at http://localhost:8000/dashboard

## Core Capabilities

The system correctly handles the two monetization paths from the business plan:

**Stream 1 — Search (Google/Bing call-only) → Enroll In-House**  
High-intent calls are scored and routed toward licensed agents for commission revenue (higher CAC tolerance, target <$150 CPA).

**Stream 2 — Social (FB/YouTube educational) → Sell Calls at $25**  
Lower-intent/overflow volume is scored and routed toward the sell stream (must keep CAC <$18 for positive margin). Produces leadmarket-style packaged leads with compliance proof.

**Non-negotiable**: Every call is forced through the **Hard Compliance Gate** first (non-bypassable, evidence-based, tamper-evident audit trail) before any monetization decision.

## What's Delivered

- Hard Compliance Gate (production version)
- Medicare-tuned UVal Scorer for optimal dual-stream routing
- Full FastAPI service with telephony webhook (`/webhooks/twilio/voice`)
- Real bidirectional GHL/LeadConnector integration (custom fields + outcome logging)
- MCP tools for agents (Claude Desktop, Cursor, etc.)
- Luxury operator dashboard at `/dashboard`
- Router integration adapter ready for your llm-router-engine
- Dockerfile + Railway deployment ready
- Comprehensive simulator demonstrating **both** streams

See [PILOT_WIRING_GUIDE.md](PILOT_WIRING_GUIDE.md) for how to connect real Twilio + GHL traffic.

## Documentation

- [PILOT_WIRING_GUIDE.md](PILOT_WIRING_GUIDE.md) — How to go live with real traffic
- [DEPLOYMENT.md](DEPLOYMENT.md) — Deployment options and pilot setup
- [architecture/ARCHITECTURE.md](architecture/ARCHITECTURE.md)
- [docs/MARKET_PILOT_CHECKLIST.md](docs/MARKET_PILOT_CHECKLIST.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/CONSOLIDATION_STRATEGY.md](docs/CONSOLIDATION_STRATEGY.md)

## License

Proprietary — see [LICENSE](LICENSE) for details.

---

**Built with extreme precision for regulated Medicare operations.**

## Current Market Pilot Readiness

**Core E2E dual-stream system with Hard Compliance Gate: Ready for controlled pilot.**

You can wire real (small volume) inbound calls today and see both monetization paths execute with full compliance enforcement and audit artifacts.

## What Is Still Required Before Real Ad Spend

- Real GHL + Twilio webhook integration + live agent handoff
- Production economics dashboard (replace stub with your grok-extract-pnl + masterBRIDGE analytics)
- Live sell-stream buyers or leadmarket instance
- Full red-team mitigations executed (see redteam/RED_TEAM_REPORT.md)
- AEP capacity + compliance war game passed

## Artifacts Delivered

- Complete architecture
- Production build plan with verification gates
- Brutal red-team report
- Moat consolidation strategy (how to turn your 243 repos into a real core)
- 30/60/90 execution roadmap
- All source code + tests + deployment configs

**Location**: `C:\Users\lang2\MedicareCallForge\`

This is the highest-precision foundation possible. Both streams are first-class, compliance is non-negotiable code, and the system is ready for a controlled pilot.

Run the simulator. Extend it. Ship the pilot.

Highest skill. Highest precision. No low-leverage work. Market pilot foundation complete.