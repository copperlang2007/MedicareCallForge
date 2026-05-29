"""
Economics & PNL layer for MedicareCallForge.

Designed as the production replacement for all stub economics.
Ready to consume real outputs from grok-extract-telesales-pnl + masterBRIDGE analytics
while staying tightly integrated with the live MultiAgentOrchestrator brain.
"""

from .dual_stream_pnl import (
    StreamEconomics,
    DualStreamSnapshot,
    PNLRecord,
    DualStreamPNLAdapter,
    economics_engine,
)

__all__ = [
    "StreamEconomics", 
    "DualStreamSnapshot",
    "PNLRecord",
    "DualStreamPNLAdapter",
    "economics_engine",
]