"""
Production-grade GoHighLevel (LeadConnector) API client for MedicareCallForge.

Designed to work with the patterns from ghl-twilio-smart-queue and masterBRIDGE.

Key easy-to-use helpers:
- update_medicare_custom_fields(...)   → for licensed_states, carrier_appointments, etc.
- log_medicare_call_outcome(...)       → pushes decision + full compliance proof as a note + custom fields

All calls are best-effort with graceful degradation so the voice path never breaks.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger("medicare_call_forge.ghl")


class GHLClient:
    """Production GHL (LeadConnector) client with proper Location-Id support."""

    def __init__(self):
        # Support preferred names + common aliases
        token = (
            os.getenv("GHL_API_TOKEN")
            or os.getenv("GHL_API_KEY")
        )
        location_id = os.getenv("GHL_LOCATION_ID")
        base_url = os.getenv("GHL_BASE_URL", "https://services.leadconnectorhq.com")

        self.token = token
        self.location_id = location_id
        self.base_url = base_url.rstrip("/")

        headers = {
            "Content-Type": "application/json",
            "Version": "2021-07-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if location_id:
            headers["Location-Id"] = location_id

        self.client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=12.0,
        )
        self.enabled = bool(token)

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any] | None:
        if not self.enabled:
            return None
        try:
            resp = self.client.request(method, path, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.warning("GHL API call failed (%s %s): %s", method, path, exc)
            return None

    def search_contact_by_phone(self, phone: str) -> dict[str, Any] | None:
        """Search for a contact by phone number. Returns first match or None."""
        if not phone:
            return None
        # GHL search supports phone query
        data = self._request("GET", "/contacts/search", params={"query": phone, "limit": 1})
        contacts = data.get("contacts", []) if data else []
        return contacts[0] if contacts else None

    def get_contact(self, contact_id: str) -> dict[str, Any] | None:
        return self._request("GET", f"/contacts/{contact_id}")

    def update_contact_custom_fields(self, contact_id: str, fields: dict[str, Any]) -> bool:
        """
        Update custom fields on a contact.
        Pass the exact internal GHL custom field IDs or names as keys.
        """
        payload = {"customFields": fields}
        result = self._request("PUT", f"/contacts/{contact_id}", json=payload)
        return result is not None

    def add_note(self, contact_id: str, title: str, body: str) -> bool:
        """Add a note/activity to a contact (excellent for compliance proof)."""
        payload = {
            "title": title,
            "body": body,
            "type": "note",
        }
        result = self._request("POST", f"/contacts/{contact_id}/notes", json=payload)
        return result is not None

    # =====================================================================
    # Convenient Medicare-specific helpers (what you asked for)
    # =====================================================================

    def update_medicare_custom_fields(
        self,
        contact_id: str,
        *,
        licensed_states: list[str] | str | None = None,
        carrier_appointments: list[str] | str | None = None,
        current_availability: str | None = None,
        ghl_phone_number: str | None = None,
        **extra_custom_fields: Any,
    ) -> bool:
        """
        Easy helper to update the key Medicare custom fields on a GHL contact.

        The phone number is written to whatever field you set in GHL_PHONE_CUSTOM_FIELD
        (your setup uses "lc phone" / lc_phone).

        Usage example:
            ghl_client.update_medicare_custom_fields(
                contact_id,
                licensed_states=["CA", "TX"],
                carrier_appointments=["UHC", "Aetna"],
                current_availability="Available",
                ghl_phone_number="+15551234567",
            )
        """
        fields: dict[str, Any] = {}

        if licensed_states is not None:
            fields["licensed_states"] = licensed_states if isinstance(licensed_states, str) else ", ".join(licensed_states)
        if carrier_appointments is not None:
            fields["carrier_appointments"] = carrier_appointments if isinstance(carrier_appointments, str) else ", ".join(carrier_appointments)
        if current_availability is not None:
            fields["current_availability"] = current_availability
        if ghl_phone_number is not None:
            # Write to whatever custom field the user configured in their GHL ("lc phone" / lc_phone)
            phone_field = os.getenv("GHL_PHONE_CUSTOM_FIELD", "lc_phone")
            fields[phone_field] = ghl_phone_number

        # Allow passing any additional custom fields the user has in GHL
        fields.update(extra_custom_fields)

        if not fields:
            return True

        return self.update_contact_custom_fields(contact_id, fields)

    def log_medicare_call_outcome(
        self,
        contact_id: str,
        *,
        decision: str,                    # "enroll_in_house" or "sell_call"
        compliance_hash: str,
        uval: float,
        compliance_score: float,
        recording_url: str | None = None,
        state: str | None = None,
        from_number: str | None = None,
        brain_rationale: str | None = None,
    ) -> bool:
        """
        High-level helper specifically for MedicareCallForge call outcomes.

        Pushes a clean note + updates useful custom fields (decision, hash, uval, etc.)
        in one call. This is the recommended way to log calls back to GHL.
        Brain rationale included for full military audit trail (in note).
        """
        # 1. Log as a note (best for audit/compliance proof)
        note_body = (
            f"Decision: {decision}\n"
            f"Compliance Score: {compliance_score:.1f}%\n"
            f"UVal: {uval:.3f}\n"
            f"Audit Hash: {compliance_hash}\n"
        )
        if recording_url:
            note_body += f"Recording: {recording_url}\n"
        if state:
            note_body += f"State: {state}\n"
        if from_number:
            note_body += f"Phone: {from_number}\n"
        if brain_rationale:
            note_body += f"Brain Rationale: {brain_rationale[:200]}\n"

        note_success = self.add_note(contact_id, f"MedicareCallForge - {decision}", note_body)

        # 2. Also update convenient custom fields for filtering/reporting in GHL
        field_success = self.update_medicare_custom_fields(
            contact_id,
            last_medicare_decision=decision,
            last_medicare_compliance_hash=compliance_hash,
            last_medicare_uval=round(uval, 3),
            last_medicare_compliance_score=round(compliance_score, 1),
            last_medicare_recording_url=recording_url or "",
        )

        return note_success or field_success   # at least one should succeed

    # ------------------------------------------------------------------
    # Additional methods for full GHL MCP exposure (read + write)
    # ------------------------------------------------------------------

    def search_contacts(self, query: str | None = None, limit: int = 10, **filters: Any) -> list[dict[str, Any]]:
        """General contact search with optional query and filters."""
        params: dict[str, Any] = {"limit": limit}
        if query:
            params["query"] = query
        params.update(filters)
        data = self._request("GET", "/contacts/search", params=params)
        return data.get("contacts", []) if data else []

    def create_contact(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        custom_fields: dict[str, Any] | None = None,
        **extra: Any,
    ) -> dict[str, Any] | None:
        """Create a new contact in GHL."""
        payload: dict[str, Any] = {}
        if first_name: payload["firstName"] = first_name
        if last_name: payload["lastName"] = last_name
        if phone: payload["phone"] = phone
        if email: payload["email"] = email
        if custom_fields: payload["customFields"] = custom_fields
        payload.update(extra)
        return self._request("POST", "/contacts", json=payload)

    def create_opportunity(
        self,
        contact_id: str,
        title: str,
        pipeline_id: str | None = None,
        stage_id: str | None = None,
        monetary_value: int | None = None,
        **extra: Any,
    ) -> dict[str, Any] | None:
        """
        Create an opportunity (especially useful for the 'sell' stream to push leads to buyers).
        """
        payload: dict[str, Any] = {"contactId": contact_id, "title": title}
        if pipeline_id: payload["pipelineId"] = pipeline_id
        if stage_id: payload["stageId"] = stage_id
        if monetary_value is not None: payload["monetaryValue"] = monetary_value
        payload.update(extra)
        return self._request("POST", "/opportunities", json=payload)

    def get_contact_activities(self, contact_id: str, limit: int = 20) -> list[dict[str, Any]]:
        """Get recent activities/notes for a contact (useful context for agents)."""
        data = self._request("GET", f"/contacts/{contact_id}/activities", params={"limit": limit})
        return data.get("activities", []) if data else []

    def close(self):
        self.client.close()


# Singleton for easy import (initialized with TelephonySettings)
ghl_client = GHLClient()
