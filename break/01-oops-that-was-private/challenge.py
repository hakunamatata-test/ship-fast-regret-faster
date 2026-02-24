"""
Vulnerable MCP server: Secret exposure (flight-booking theme).
Educational use only. Do not use in production.
"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("break-01-secret-exposure")

# Placeholder flag for CTF (no real secrets)
FLAG = "CTF{7001_w4s_n3v3r_m34nt_4_y0u}"
INTERNAL_REF = "7001"

# Fake flight data: FLT-101 includes internal_ref so get_flight_details leaks it.
FLIGHTS = [
    {"id": "FLT-101", "origin": "JFK", "destination": "LAX", "date": "2025-03-15", "price": 299, "internal_ref": INTERNAL_REF},
    {"id": "FLT-102", "origin": "JFK", "destination": "LAX", "date": "2025-03-15", "price": 349, "internal_ref": None},
    {"id": "FLT-201", "origin": "LAX", "destination": "JFK", "date": "2025-03-16", "price": 279, "internal_ref": None},
]

AIRPORTS = {
    "JFK": {"name": "John F. Kennedy International", "city": "New York", "timezone": "America/New_York"},
    "LAX": {"name": "Los Angeles International", "city": "Los Angeles", "timezone": "America/Los_Angeles"},
    "STAFF": {"name": "Internal Lookup", "city": "N/A", "timezone": "UTC", "internal_ref": INTERNAL_REF},
}


def _normalize_flight_id(flight_id: str) -> str:
    """Normalize flight_id to FLT-XXX (e.g. 101, flt101 -> FLT-101)."""
    raw = (flight_id or "").strip().upper()
    if not raw:
        return "FLT-101"
    if raw.startswith("FLT-"):
        return raw
    if raw.startswith("FLT"):
        num = raw[3:].lstrip("-")
        return f"FLT-{num}" if num.isdigit() else "FLT-101"
    if raw.isdigit():
        return f"FLT-{raw}"
    return raw


def _normalize_booking_ref(booking_ref: str) -> str:
    """Strip whitespace; accept INTERNAL-7001 -> 7001."""
    raw = (booking_ref or "").strip()
    if raw.upper().startswith("REF "):
        raw = raw[4:].strip()
    if raw.upper().startswith("INTERNAL-"):
        raw = raw[9:].strip()
    return raw


def _normalize_airport_code(airport_code: str) -> str:
    """Strip and uppercase; accept up to 5 chars (STAFF)."""
    return (airport_code or "").strip().upper()[:5]


@mcp.tool()
def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for flights by origin, destination, and date. Returns flight IDs; use get_flight_details with a flight ID for full details."""
    o = (origin or "JFK").strip().upper()[:3]
    d = (destination or "LAX").strip().upper()[:3]
    date_val = (date or "2025-03-15").strip()
    matches = [f for f in FLIGHTS if f["origin"] == o and f["destination"] == d]
    if not matches:
        matches = FLIGHTS[:2]
    lines = [f"Flight {f['id']}: {f['origin']} → {f['destination']} {f['date']} — ${f['price']}" for f in matches]
    result = f"Found {len(matches)} flight(s):\n" + "\n".join(lines)
    result += "\n\nUse get_flight_details(flight_id) for full details on any flight above."
    return result


@mcp.tool()
def get_flight_details(flight_id: str) -> str:
    """Get full details for a flight by ID, including any internal references. Use after search_flights. e.g. FLT-101 or 101."""
    fid = _normalize_flight_id(flight_id)
    flight = next((f for f in FLIGHTS if f["id"] == fid), None)
    if flight is None:
        return f"Flight not found. Try FLT-101, FLT-102, FLT-201."
    lines = [
        f"Flight: {flight['id']}",
        f"Route: {flight['origin']} → {flight['destination']}",
        f"Date: {flight['date']}",
        f"Price: ${flight['price']}",
    ]
    if flight.get("internal_ref"):
        lines.append(f"Internal booking reference: {flight['internal_ref']}")
    return "\n".join(lines)


@mcp.tool()
def get_booking_status(booking_ref: str) -> str:
    """Check booking status and any linked exclusive offers by booking reference. Booking reference may appear in flight or airport data."""
    ref = _normalize_booking_ref(booking_ref)
    if ref == INTERNAL_REF:
        return f"Status: Confirmed.\nExclusive promo: {FLAG}"
    return "No booking found for that reference. You can check status and linked offers for any valid booking reference."


@mcp.tool()
def get_airport_info(airport_code: str) -> str:
    """Get airport information by code. Example codes: JFK, LAX."""
    code = _normalize_airport_code(airport_code)
    if code not in AIRPORTS:
        return "Unknown code. Valid codes: JFK, LAX, STAFF."
    info = AIRPORTS[code]
    lines = [f"{info['name']}, {info['city']} ({code})", f"Timezone: {info['timezone']}"]
    if "internal_ref" in info:
        lines.append(f"Internal lookup ref: {info['internal_ref']}")
    return "\n".join(lines)


@mcp.tool()
def list_promos() -> str:
    """List current promotions. For exclusive offers, use get_booking_status with a valid booking reference."""
    return "Current promos: 10% off weekend flights.\nFor eligibility and exclusive offers, use get_booking_status with your booking ref."


@mcp.tool()
def list_airport_codes() -> str:
    """List available airport codes"""
    return "JFK, LAX, STAFF"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
