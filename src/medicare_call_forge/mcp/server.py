"""
MCP Server for MedicareCallForge GHL Tools.

Run this as a stdio MCP server so Claude Desktop, Cursor, or agents can use the GHL tools.

✅ The server automatically loads your .env file from the project root.
   → You only need to maintain one .env file. No need to copy variables
     into claude_desktop_config.json.

Usage (for Claude Desktop config):
{
  "mcpServers": {
    "medicarecallforge-ghl": {
      "command": "python",
      "args": ["-m", "medicare_call_forge.mcp.server"]
    }
  }
}
"""

from pathlib import Path
from dotenv import load_dotenv

# Robust .env loading for both local runs and Claude Desktop
# 1. Try the project root relative to this file
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# 2. Also try loading from current working directory (fallback)
load_dotenv()  # looks for .env in cwd

# This ensures your GHL_API_TOKEN, GHL_LOCATION_ID, Twilio vars etc.
# are available even when Claude Desktop launches the MCP server.

# === Startup Debug Logging (visible in Claude Desktop MCP logs) ===
import sys

print("=== MedicareCallForge GHL MCP Server Starting ===", file=sys.stderr)
print(f"Attempted .env path: {env_path}", file=sys.stderr)
print(f".env file exists at that path: {env_path.exists()}", file=sys.stderr)

# Import ghl_client AFTER env is loaded so we can report its status
from medicare_call_forge.ghl.client import ghl_client

print(f"GHL client enabled: {ghl_client.enabled}", file=sys.stderr)
if ghl_client.enabled:
    print(f"GHL Location ID configured: {bool(ghl_client.location_id)}", file=sys.stderr)
else:
    print("WARNING: GHL is NOT enabled. Check GHL_API_TOKEN and GHL_LOCATION_ID in your .env", file=sys.stderr)
print("=== End Startup Debug ===", file=sys.stderr)
# === End Debug Logging ===

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .ghl_tools import (
    ghl_search_contact_by_phone,
    ghl_search_contacts,
    ghl_get_contact,
    ghl_get_contact_activities,
    ghl_update_medicare_custom_fields,
    ghl_add_note,
    ghl_create_contact,
    ghl_create_opportunity,
    ghl_log_medicare_call_outcome,
)

server = Server("medicarecallforge-ghl")


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="ghl_search_contact_by_phone",
            description="Search for a contact in GoHighLevel by phone number. Returns contact details and current custom fields.",
            inputSchema={
                "type": "object",
                "properties": {
                    "phone": {"type": "string", "description": "Phone number, e.g. +15551234567"}
                },
                "required": ["phone"],
            },
        ),
        Tool(
            name="ghl_search_contacts",
            description="General contact search with query and filters. More powerful than phone-only search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
            },
        ),
        Tool(
            name="ghl_get_contact",
            description="Fetch full details for a GoHighLevel contact by ID, including all custom fields.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "GHL Contact ID"}
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="ghl_get_contact_activities",
            description="Get recent activities, notes, and call logs for a contact (excellent context for agents).",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string"},
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="ghl_update_medicare_custom_fields",
            description="Update key Medicare custom fields on a GHL contact (licensed_states, carrier_appointments, current_availability, etc.). The ghl_phone_number is saved to the field defined by GHL_PHONE_CUSTOM_FIELD (default: lc_phone for most LC Phone users). Recommended for maintaining licensing data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string"},
                    "licensed_states": {"type": ["array", "string"], "items": {"type": "string"}},
                    "carrier_appointments": {"type": ["array", "string"], "items": {"type": "string"}},
                    "current_availability": {"type": "string"},
                    "ghl_phone_number": {"type": "string", "description": "Phone number. Written to GHL_PHONE_CUSTOM_FIELD (usually lc_phone or lc phone)"},
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="ghl_add_note",
            description="Add a free-form note/activity to a GoHighLevel contact. Use this for general notes; prefer ghl_log_medicare_call_outcome for structured call results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["contact_id", "title", "body"],
            },
        ),
        Tool(
            name="ghl_create_contact",
            description="Create a new contact in GoHighLevel. Useful for new inbound leads.",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
        ),
        Tool(
            name="ghl_create_opportunity",
            description="Create an opportunity (especially powerful for the 'sell' stream to push leads to buyers or the lead marketplace).",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string"},
                    "title": {"type": "string"},
                    "pipeline_id": {"type": "string"},
                    "stage_id": {"type": "string"},
                    "monetary_value": {"type": "integer"},
                },
                "required": ["contact_id", "title"],
            },
        ),
        Tool(
            name="ghl_log_medicare_call_outcome",
            description="Log a completed Medicare inbound call outcome to GoHighLevel. Creates a compliance-grade note and updates tracking fields (including phone in your GHL_PHONE_CUSTOM_FIELD). Use after every call.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string"},
                    "decision": {"type": "string", "enum": ["enroll_in_house", "sell_call"]},
                    "compliance_hash": {"type": "string"},
                    "uval": {"type": "number"},
                    "compliance_score": {"type": "number"},
                    "recording_url": {"type": "string"},
                    "state": {"type": "string"},
                    "from_number": {"type": "string"},
                },
                "required": ["contact_id", "decision", "compliance_hash", "uval", "compliance_score"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "ghl_search_contact_by_phone":
        result = ghl_search_contact_by_phone(**arguments)
    elif name == "ghl_search_contacts":
        result = ghl_search_contacts(**arguments)
    elif name == "ghl_get_contact":
        result = ghl_get_contact(**arguments)
    elif name == "ghl_get_contact_activities":
        result = ghl_get_contact_activities(**arguments)
    elif name == "ghl_update_medicare_custom_fields":
        result = ghl_update_medicare_custom_fields(**arguments)
    elif name == "ghl_add_note":
        result = ghl_add_note(**arguments)
    elif name == "ghl_create_contact":
        result = ghl_create_contact(**arguments)
    elif name == "ghl_create_opportunity":
        result = ghl_create_opportunity(**arguments)
    elif name == "ghl_log_medicare_call_outcome":
        result = ghl_log_medicare_call_outcome(**arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [TextContent(type="text", text=str(result))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
