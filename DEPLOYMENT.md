# Deployment & Going Live

## Local Development (Fastest for Testing)

```powershell
cd C:\Users\lang2\MedicareCallForge
py -3 -m pip install -e ".[dev]"
uvicorn src.medicare_call_forge.app:app --reload
```

Then run the simulator in another terminal:
```powershell
python examples/full_flow_simulator.py
```

Open the luxury dashboard: http://localhost:8000/dashboard

## Production Pilot Wiring (Recommended Next Step)

→ See **[PILOT_WIRING_GUIDE.md](PILOT_WIRING_GUIDE.md)** for the complete, step-by-step instructions.

This covers:
- Real Twilio number webhook configuration
- GHL studio / workflow integration
- Required environment variables (`TWILIO_*`, `GHL_*`, TaskRouter SIDs)
- LC Phone custom field handling ("lc phone")
- Media Streams for transcription
- TaskRouter enqueue for both streams

## Deployment Options

### Railway (Recommended for Pilot)
- Connect this repo
- Set environment variables from `.env.example`
- Deploy (multi-stage Dockerfile + `railway.toml` already configured)

### Docker
```bash
docker build -t medicarecallforge .
docker run -p 8000:8000 --env-file .env medicarecallforge
```

## MCP Tools for Agents

```bash
pip install -e ".[mcp]"
medicarecallforge-ghl-mcp
```

Configure in Claude Desktop / Cursor for direct agent access to GHL + MedicareCallForge tools.

## Monitoring

- `/dashboard` — Full operator console with live calls, charts, and one-click audit export
- `/health`
- `/audit/vault`
- `/metrics/economics`
- `/ghl/health`

## Next Steps After Wiring

See [docs/MARKET_PILOT_CHECKLIST.md](docs/MARKET_PILOT_CHECKLIST.md) and [docs/ROADMAP.md](docs/ROADMAP.md).