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

from medicare_call_forge.economics.dual_stream_pnl import economics_engine, DualStreamSnapshot


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
    """Extends SimpleMetrics with persistent vault + real dual-stream PNL engine."""

    def __init__(self):
        super().__init__()
        self.vault = PersistentAuditVault()

    def record_call(self, call_id: str, decision: str, compliance_score: float, uval: float, audit_event: dict | None = None):
        super().record_call(call_id, decision, compliance_score, uval)
        if audit_event:
            self.vault.append(audit_event)

    def get_dual_stream_economics(self, brain_metrics: dict[str, Any] | None = None) -> dict:
        """
        Now powered by the real DualStreamPNLAdapter.

        This is the production path. It can be fed by:
        - grok-extract-telesales-pnl batch outputs
        - live MultiAgentOrchestrator cost signals (via brain_metrics)
        - real post-call processing
        """
        snapshot: DualStreamSnapshot = economics_engine.get_snapshot(brain_metrics=brain_metrics)

        return {
            "search_enroll_stream": {
                "calls": snapshot.enroll.calls,
                "enrollments": snapshot.enroll.enrollments,
                "revenue_cents": snapshot.enroll.revenue_cents,
                "cost_cents": snapshot.enroll.cost_cents,
                "cac_cents": snapshot.enroll.cac_cents,
                "margin_cents": snapshot.enroll.margin_cents,
                "avg_uval": round(snapshot.enroll.avg_uval, 3),
                "target_cac_cents": snapshot.enroll.target_cac_cents,
            },
            "social_sell_stream": {
                "calls": snapshot.sell.calls,
                "revenue_cents": snapshot.sell.revenue_cents,
                "cost_cents": snapshot.sell.cost_cents,
                "margin_cents": snapshot.sell.margin_cents,
                "avg_uval": round(snapshot.sell.avg_uval, 3),
                "target_cac_cents": snapshot.sell.target_cac_cents,
                "target_margin_cents": snapshot.sell.target_margin_cents,
            },
            "overall": {
                "total_calls": snapshot.total_calls,
                "overall_margin_cents": snapshot.overall_margin_cents,
                "brain_cost_efficiency": snapshot.brain_cost_efficiency,
                "audit_vault_size": len(self.vault.get_all()),
                "timestamp": snapshot.timestamp,
            },
            "note": "Real dual-stream PNL. Feed via economics_engine.ingest_batch() from grok-extract-telesales-pnl or live brain.",
        }


# Global instances
metrics = EnhancedMetrics()
audit_vault = metrics.vault  # Convenient access for app.py and dashboard
