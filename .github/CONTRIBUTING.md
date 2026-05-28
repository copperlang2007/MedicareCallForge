# Contributing to MedicareCallForge

Thank you for your interest in contributing to MedicareCallForge! This is a production-grade system for Medicare inbound call lead generation with strict compliance requirements.

## Code of Conduct

By participating, you agree to maintain the highest standards of professionalism and compliance awareness.

## How to Contribute

1. **Fork the repository** and create your branch from `main`.
2. **Make your changes** following our style guidelines.
3. **Test thoroughly** – especially anything touching the compliance gate or GHL integration.
4. **Submit a pull request** with a clear description.

## Development Setup

```bash
cd MedicareCallForge
py -3 -m pip install -e ".[dev]"
```

## Key Principles

- **Compliance First**: The Hard Compliance Gate (`apply_hard_compliance_gate`) must never be bypassed. All changes must preserve this invariant.
- **Dual-Stream Integrity**: Changes must correctly handle both "enroll_in_house" and "sell_call" paths with proper UVal scoring.
- **GHL Integration**: When modifying telephony or GHL code, ensure custom fields (`licensed_states`, `carrier_appointments`, etc.) and LC Phone handling remain correct.
- **MCP Tools**: Tools exposed for agents must have excellent descriptions and safe error handling.

## Commit Messages

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation only
- `refactor:` code change that neither fixes a bug nor adds a feature
- `test:` adding missing tests
- `chore:` changes to build process or tools

## Pull Requests

See `.github/PULL_REQUEST_TEMPLATE.md` for the required format.

## Questions?

Open an issue or contact the maintainer.

---

**Remember**: This system handles regulated Medicare calls. Accuracy and auditability are non-negotiable.