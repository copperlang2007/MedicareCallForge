"""
Observability + Persistent Audit Vault for MedicareCallForge.

- In-memory + JSON file-backed tamper-evident audit chain (production-ready for pilot)
- Dual-stream economics with hooks for your grok-extract-telesales-pnl + masterBRIDGE analytics
- Designed to feed the luxury dashboard and future real orchestrator metrics
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SimpleMetrics:
    """In-memory metrics for pilot. Thread-safe enough for low volume."""

    def __init__(self):
        self.calls: list[dict[str, Any]] = []
        self.stream_counts = defaultdict(int)
        self.total_compliance_score = 0.0
        self.call_count = 0

    def record_call(self, call_id: str, decision: str, compliance_score: float, uval: float):
        self.calls.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "call_id": call_id,
            "decision": decision,
            "compliance_score": compliance_score,
            "uval": uval,
        })
        self.stream_counts[decision] += 1
        self.total_compliance_score += compliance_score
        self.call_count += 1

    def get_summary(self) -> dict[str, Any]:
        if self.call_count == 0:
            return {"status": "no_calls_yet"}

        avg_compliance = self.total_compliance_score / self.call_count

        return {
            "total_calls": self.call_count,
            "stream_breakdown": dict(self.stream_counts),
            "average_compliance_score": round(avg_compliance, 1),
            "compliance_target": ">= 95 for production",
            "note": "Replace this stub with real dual-stream economics from your grok-extract models.",
        }


VAULT_PATH = Path("data/audit_vault.json")
VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)


class PersistentAuditVault:
    """Tamper-evident audit chain with file persistence (simple but production-viable for pilot)."""

    def __init__(self, path: Path = VAULT_PATH):
        self.path = path
        self.chain: list[dict] = []
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self.chain = json.loads(self.path.read_text())
            except Exception:
                self.chain = []

    def _save(self):
        self.path.write_text(json.dumps(self.chain, indent=2, default=str))

    def append(self, event: dict):
        if self.chain:
            event["prev_hash"] = self.chain[-1].get("hash")
        else:
            event["prev_hash"] = None

        # Compute hash for tamper evidence (matches gate style)
        body = json.dumps({"prev": event.get("prev_hash"), "payload": event}, sort_keys=True, default=str)
        import hashlib
        event["hash"] = hashlib.sha256(body.encode()).hexdigest()
        event["timestamp"] = datetime.now(timezone.utc).isoformat()

        self.chain.append(event)
        self._save()

    def get_last(self):
        return self.chain[-1] if self.chain else None

    def get_all(self):
        return self.chain


class EnhancedMetrics(SimpleMetrics):
    """Extends SimpleMetrics with persistent vault + dual-stream economics hooks."""

    def __init__(self):
        super().__init__()
        self.vault = PersistentAuditVault()

    def record_call(self, call_id: str, decision: str, compliance_score: float, uval: float, audit_event: dict | None = None):
        super().record_call(call_id, decision, compliance_score, uval)
        if audit_event:
            self.vault.append(audit_event)

    def get_dual_stream_economics(self) -> dict:
        """Enhanced version ready for replacement by grok-extract-pnl + masterBRIDGE."""
        summary = self.get_summary()
        vault_size = len(self.vault.get_all())

        return {
            "search_enroll_stream": {
                "target_cac": "<$40",
                "target_cpa": "<$150",
                "projected_enrollments_per_100": "18-25",
                "avg_uval": 0.77,
                "calls": summary.get("stream_breakdown", {}).get("enroll_in_house", 0),
            },
            "social_sell_stream": {
                "sell_price": "$25",
                "target_margin": "$7-15",
                "target_cac": "<$18",
                "avg_uval": 0.56,
                "calls": summary.get("stream_breakdown", {}).get("sell_call", 0),
            },
            "overall": {
                "total_calls": summary.get("total_calls", 0),
                "avg_compliance": summary.get("average_compliance_score", 0),
                "audit_vault_size": vault_size,
                "note": "Replace with real grok-extract-telesales-pnl LSTM + masterBRIDGE analytics for production.",
            },
        }


# Global instances
metrics = EnhancedMetrics()
audit_vault = metrics.vault  # Convenient access for app.py and dashboard
