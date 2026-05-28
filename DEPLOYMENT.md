# Deployment & Pilot Wiring

This document provides the fastest path to production pilot.

## Local Development

See README.md for quick start.

## Connecting Real Traffic (Recommended Next Step)

→ **[PILOT_WIRING_GUIDE.md](PILOT_WIRING_GUIDE.md)** — The authoritative guide for wiring real Twilio numbers and GHL studio workflows.

This includes:
- Environment variables (Twilio + GHL + TaskRouter)
- Webhook configuration
- GHL custom field forwarding (`LicensedStates`, `CarrierAppointments`, etc.)
- TaskRouter enqueue for both streams
- Media Streams for transcription (masterBRIDGE pattern)

## Production Deployment Options

### Railway (Fastest)
- Link this repo
- Set environment variables from `.env.example`
- Deploy

`railway.toml` and multi-stage `Dockerfile` are already configured.

### Docker
```bash
docker build -t medicarecallforge .
docker run -p 8000:8000 --env-file .env medicarecallforge
```

## MCP Tools for Agents

Install the MCP extra:
```bash
pip install -e ".[mcp]"
```

Run the GHL tools server:
```bash
medicarecallforge-ghl-mcp
```

Or via module:
```bash
python -m medicare_call_forge.mcp.server
```

Configure in Claude Desktop / Cursor for full agent access to GHL + MedicareCallForge logic.

## Monitoring & Observability

- `/dashboard` — Luxury operator console with live feed, charts, and audit export
- `/health`
- `/audit/vault`
- `/metrics/economics`
- `/ghl/health`

## Next After Pilot Wiring

See [docs/ROADMAP.md](docs/ROADMAP.md) and [docs/MARKET_PILOT_CHECKLIST.md](docs/MARKET_PILOT_CHECKLIST.md).