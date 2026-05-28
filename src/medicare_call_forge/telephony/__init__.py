"""
Telephony intake layer for MedicareCallForge.

Production Twilio Voice + GHL inbound webhooks with non-bypassable Hard Compliance Gate + dual-stream UVal decisioning.
Wires to llm-router-engine MultiAgentOrchestrator for the full brain (Compliance Gate as first WorkflowStep).
"""

from .inbound_handler import get_telephony_router, twilio_voice_inbound

__all__ = ["get_telephony_router", "twilio_voice_inbound"]
