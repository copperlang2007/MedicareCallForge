"""
MCP Tools for GoHighLevel (GHL / LeadConnector) integration in MedicareCallForge.

These tools allow agents (Claude, MultiAgentOrchestrator, etc.) to safely
interact with GHL contacts for Medicare-specific workflows.

Phone numbers passed to update / log tools are written to the custom field
configured by the GHL_PHONE_CUSTOM_FIELD environment variable
(defaults to "lc_phone" — perfect for setups using LC Phone in GHL).

Available tools:
- ghl_search_contact_by_phone
- ghl_search_contacts (general search)
- ghl_get_contact
- ghl_get_contact_activities
- ghl_update_medicare_custom_fields
- ghl_add_note
- ghl_create_contact
- ghl_create_opportunity (key for sell stream)
- ghl_log_medicare_call_outcome
"""

from typing import Any

from medicare_call_forge.ghl.client import ghl_client


def ghl_search_contact_by_phone(phone: str) -> dict[str, Any]:
    """
    Search for a contact in GoHighLevel by phone number.

    Args:
        phone: Phone number to search (e.g. "+15551234567")

    Returns:
        Contact object if found, or error information.
    """
    if not ghl_client.enabled:
        return {"error": "GHL client not configured (missing GHL_API_TOKEN and/or GHL_LOCATION_ID)"}

    contact = ghl_client.search_contact_by_phone(phone)
    if contact:
        return {
            "found": True,
            "contact_id": contact.get("id"),
            "name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
            "phone": contact.get("phone"),
            "email": contact.get("email"),
            "custom_fields": contact.get("customFields", {}),
        }
    return {"found": False, "message": "No contact found for that phone number"}


def ghl_update_medicare_custom_fields(
    contact_id: str,
    licensed_states: list[str] | str | None = None,
    carrier_appointments: list[str] | str | None = None,
    current_availability: str | None = None,
    ghl_phone_number: str | None = None,
    **extra_custom_fields: Any,
) -> dict[str, Any]:
    """
    Update Medicare-specific custom fields on a GHL contact.

    This is the recommended way for agents to maintain licensing and availability data.

    The ghl_phone_number (if provided) is written to whatever custom field
    you configured via the GHL_PHONE_CUSTOM_FIELD environment variable.
    Default is "lc_phone" (common for users whose GHL client uses LC Phone).

    Args:
        contact_id: GHL Contact ID
        licensed_states: List of states or comma-separated string
        carrier_appointments: List of carriers or comma-separated string
        current_availability: Availability status string
        ghl_phone_number: Phone number — will be saved to your GHL_PHONE_CUSTOM_FIELD
        **extra_custom_fields: Any other custom fields you want to set

    Returns:
        Success status and details.
    """
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured"}

    success = ghl_client.update_medicare_custom_fields(
        contact_id=contact_id,
        licensed_states=licensed_states,
        carrier_appointments=carrier_appointments,
        current_availability=current_availability,
        ghl_phone_number=ghl_phone_number,
        **extra_custom_fields,
    )

    return {
        "success": success,
        "contact_id": contact_id,
        "updated_fields": {
            k: v for k, v in {
                "licensed_states": licensed_states,
                "carrier_appointments": carrier_appointments,
                "current_availability": current_availability,
                "ghl_phone_number": ghl_phone_number,
                **extra_custom_fields,
            }.items() if v is not None
        },
    }


def ghl_log_medicare_call_outcome(
    contact_id: str,
    decision: str,
    compliance_hash: str,
    uval: float,
    compliance_score: float,
    recording_url: str | None = None,
    state: str | None = None,
    from_number: str | None = None,
) -> dict[str, Any]:
    """
    Log a completed Medicare call outcome back to GoHighLevel.

    This creates a note on the contact (excellent for compliance/audit) and
    updates useful custom fields for filtering and reporting.

    The phone number context (from_number) is associated via your configured
    GHL_PHONE_CUSTOM_FIELD (default lc_phone for LC Phone users).

    Use this after every inbound call (both enroll and sell streams).

    Args:
        contact_id: GHL Contact ID
        decision: "enroll_in_house" or "sell_call"
        compliance_hash: The tamper-evident audit hash from MedicareCallForge
        uval: UVal score from the dual-stream decision
        compliance_score: Compliance gate score (0-100)
        recording_url: URL to the call recording (if available)
        state: State the call originated from
        from_number: Caller's phone number

    Returns:
        Success status.
    """
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured"}

    success = ghl_client.log_medicare_call_outcome(
        contact_id=contact_id,
        decision=decision,
        compliance_hash=compliance_hash,
        uval=uval,
        compliance_score=compliance_score,
        recording_url=recording_url,
        state=state,
        from_number=from_number,
    )

    return {
        "success": success,
        "contact_id": contact_id,
        "decision": decision,
        "compliance_hash": compliance_hash,
        "message": "Call outcome logged to GHL (note + custom fields)",
    }


def ghl_get_contact(contact_id: str) -> dict[str, Any]:
    """
    Fetch full details for a specific GoHighLevel contact.

    Useful when you have a contact_id (e.g. from a previous search or call log)
    and need the complete record including all custom fields.

    Args:
        contact_id: The GHL Contact ID (usually starts with "c_" or similar)

    Returns:
        Full contact object or error.
    """
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured (missing GHL_API_TOKEN and/or GHL_LOCATION_ID)"}

    if not contact_id or not isinstance(contact_id, str):
        return {"success": False, "error": "contact_id is required and must be a string"}

    contact = ghl_client.get_contact(contact_id)
    if contact:
        return {
            "success": True,
            "contact": contact,
        }
    return {"success": False, "error": f"Contact not found or API error for id: {contact_id}"}


def ghl_add_note(contact_id: str, title: str, body: str) -> dict[str, Any]:
    """
    Add a general note/activity to a GoHighLevel contact.

    Use this for free-form notes. For structured Medicare call outcomes,
    prefer `ghl_log_medicare_call_outcome` instead.

    Args:
        contact_id: GHL Contact ID
        title: Short title for the note
        body: Full content of the note

    Returns:
        Success status.
    """
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured (missing GHL_API_TOKEN and/or GHL_LOCATION_ID)"}

    if not contact_id or not isinstance(contact_id, str):
        return {"success": False, "error": "contact_id is required"}

    if not title or not body:
        return {"success": False, "error": "title and body are both required"}

    success = ghl_client.add_note(contact_id, title, body)

    return {
        "success": success,
        "contact_id": contact_id,
        "title": title,
        "message": "Note added to GHL contact" if success else "Failed to add note",
    }


def ghl_search_contacts(query: str | None = None, limit: int = 10, **filters: Any) -> dict[str, Any]:
    """General contact search with optional query and filters."""
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured"}

    contacts = ghl_client.search_contacts(query=query, limit=limit, **filters)
    return {"success": True, "contacts": contacts, "count": len(contacts)}


def ghl_get_contact_activities(contact_id: str, limit: int = 20) -> dict[str, Any]:
    """Get recent activities/notes for a contact (great context for agents)."""
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured"}

    activities = ghl_client.get_contact_activities(contact_id, limit=limit)
    return {"success": True, "contact_id": contact_id, "activities": activities}


def ghl_create_contact(
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    custom_fields: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """Create a new contact in GHL."""
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured"}

    result = ghl_client.create_contact(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        custom_fields=custom_fields,
        **extra,
    )
    if result:
        return {"success": True, "contact": result}
    return {"success": False, "error": "Failed to create contact"}


def ghl_create_opportunity(
    contact_id: str,
    title: str,
    pipeline_id: str | None = None,
    stage_id: str | None = None,
    monetary_value: int | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """
    Create an opportunity (especially powerful for the 'sell' stream to push leads to buyers).
    """
    if not ghl_client.enabled:
        return {"success": False, "error": "GHL client not configured"}

    result = ghl_client.create_opportunity(
        contact_id=contact_id,
        title=title,
        pipeline_id=pipeline_id,
        stage_id=stage_id,
        monetary_value=monetary_value,
        **extra,
    )
    if result:
        return {"success": True, "opportunity": result}
    return {"success": False, "error": "Failed to create opportunity"}
