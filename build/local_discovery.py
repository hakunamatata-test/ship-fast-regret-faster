from typing import Any
import api_clients
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("local-discovery")

# In-memory storage for place IDs and event IDs (resources)
_stored_place_ids: dict[str, list[str]] = {}
_stored_event_ids: dict[str, list[str]] = {}


def format_place_result(place: dict[str, Any]) -> str:
    """Format a single place result for display."""
    name = place.get("displayName", {}).get("text", "Unknown")
    address = place.get("formattedAddress", "Address not available")
    place_id = place.get("id", "N/A")
    
    return f"""
Name: {name}
Address: {address}
Place ID: {place_id}
"""


def format_ticketmaster_event(event: dict[str, Any]) -> str:
    """Format a single Ticketmaster event for display."""
    name = event.get("name", "Unknown Event")
    event_id = event.get("id", "N/A")
    url = event.get("url", "URL not available")
    dates = event.get("dates", {}) or {}
    start = dates.get("start", {}) or {}
    local_date = start.get("localDate", "")
    local_time = start.get("localTime", "")
    when = f"{local_date} {local_time}".strip() or "Date not available"
    venues_embed = (event.get("_embedded") or {}).get("venues") or []
    venue_name = venues_embed[0].get("name", "") if venues_embed else ""
    return f"""
Event: {name}
Date: {when}
Venue: {venue_name}
Event ID: {event_id}
URL: {url}
"""


def format_ticketmaster_event_details(event: dict[str, Any]) -> str:
    """Format full Ticketmaster event details (from get event by ID)."""
    name = event.get("name", "Unknown Event")
    event_id = event.get("id", "N/A")
    url = event.get("url", "URL not available")
    info = (event.get("info") or "").strip()
    please_note = (event.get("pleaseNote") or "").strip()
    dates = event.get("dates", {}) or {}
    start = dates.get("start", {}) or {}
    local_date = start.get("localDate", "")
    local_time = start.get("localTime", "")
    when = f"{local_date} {local_time}".strip() or "Date not available"
    venues_embed = (event.get("_embedded") or {}).get("venues") or []
    venue_block = ""
    if venues_embed:
        v = venues_embed[0]
        addr = v.get("address", {}) or {}
        line1 = addr.get("line1", "")
        city = (v.get("city") or {}).get("name", "")
        state = (v.get("state") or {}).get("name", "")
        venue_block = f"Venue: {v.get('name', '')}\nAddress: {', '.join(x for x in [line1, city, state] if x)}"
    price_ranges = event.get("priceRanges") or []
    price_block = ""
    if price_ranges:
        pr = price_ranges[0]
        mn = pr.get("min")
        mx = pr.get("max")
        curr = pr.get("currency", "USD")
        if mn is not None and mx is not None:
            price_block = f"Price range: {curr} {mn:.0f} - {mx:.0f}\n"
        elif mn is not None:
            price_block = f"Price from: {curr} {mn:.0f}\n"
    lines = [
        f"Event: {name}",
        f"Date: {when}",
        venue_block,
        price_block,
        f"Event ID: {event_id}",
        f"URL: {url}",
    ]
    if info:
        lines.append(f"Info: {info[:500]}{'...' if len(info) > 500 else ''}")
    if please_note:
        lines.append(f"Note: {please_note[:300]}{'...' if len(please_note) > 300 else ''}")
    return "\n".join(x for x in lines if x)


def format_ticketmaster_venue(venue: dict[str, Any]) -> str:
    """Format a Ticketmaster venue for display."""
    name = venue.get("name", "Unknown Venue")
    venue_id = venue.get("id", "N/A")
    url = venue.get("url", "")
    addr = venue.get("address", {}) or {}
    line1 = addr.get("line1", "")
    city = (venue.get("city") or {}).get("name", "")
    state = (venue.get("state") or {}).get("name", "")
    address = ", ".join(x for x in [line1, city, state] if x) or "Address not available"
    return f"""
Name: {name}
Address: {address}
Venue ID: {venue_id}
URL: {url}
"""


@mcp.tool()
async def find_restaurants(
    city: str,
    place_type: str = "restaurant",
    limit: int = 10
) -> str:
    """Find restaurants or coffee shops in a specific city.
    
    Args:
        city: City name (e.g., "Redmond, WA" or "San Francisco")
        place_type: Type of place - "restaurant" or "coffee shop" (default: "restaurant")
        limit: Maximum number of results (default: 10)
    
    Returns:
        Formatted list of places with their IDs, names, and addresses
    """
    query = f"{place_type}s in {city}"
    
    result = await api_clients.search_places_google(
        text_query=query,
        max_result_count=limit
    )
    
    if not result or "places" not in result:
        return f"Unable to find {place_type}s in {city}."
    
    places = result["places"]
    if not places:
        return f"No {place_type}s found in {city}."
    
    formatted_results = [f"Found {len(places)} {place_type}(s) in {city}:\n"]
    
    for i, place in enumerate(places, 1):
        formatted_results.append(f"{i}. {format_place_result(place)}")
    
    # Store place IDs as a resource for follow-up queries
    place_ids = [place.get("id") for place in places if place.get("id")]
    _stored_place_ids["latest"] = place_ids
    
    result_text = "\n---\n".join(formatted_results)
    result_text += f"\n\nPlace IDs stored. Use 'latest' in check_dine_in_delivery_options or check_vegetarian_options to use these IDs."
    
    return result_text


@mcp.tool()
async def check_dine_in_delivery_options(
    place_ids: str | list[str],
    use_stored: bool = False
) -> str:
    """Check which places offer dine-in, delivery, or takeout options.
    
    Args:
        place_ids: Comma-separated string or list of Google Place IDs (from find_restaurants_or_coffee_shops)
                  Can also use "latest" to use the most recent search results
        use_stored: If True, use stored place IDs from latest search (default: False)
    
    Returns:
        Formatted list showing dine-in, delivery, and takeout availability for each place
    """
    # Handle different input formats
    if use_stored and "latest" in _stored_place_ids:
        place_ids_list = _stored_place_ids["latest"]
    elif isinstance(place_ids, str):
        if place_ids.lower() == "latest":
            place_ids_list = _stored_place_ids.get("latest", [])
        else:
            # Split comma-separated string
            place_ids_list = [pid.strip() for pid in place_ids.split(",") if pid.strip()]
    else:
        place_ids_list = place_ids if isinstance(place_ids, list) else []
    
    if not place_ids_list:
        return "No place IDs provided. Use find_restaurants_or_coffee_shops first, or pass place_ids parameter."
    
    results = []
    
    for place_id in place_ids_list:
        place_details = await api_clients.get_place_details_google(place_id)
        
        if not place_details:
            results.append(f"Place ID {place_id}: Unable to fetch details")
            continue
        
        name = place_details.get("displayName", {}).get("text", "Unknown")
        dine_in = place_details.get("dineIn", False)
        delivery = place_details.get("delivery", False)
        takeout = place_details.get("takeout", False)
        
        options = []
        if dine_in:
            options.append("Dine-in ✓")
        else:
            options.append("Dine-in ✗")
        
        if delivery:
            options.append("Delivery ✓")
        else:
            options.append("Delivery ✗")
        
        if takeout:
            options.append("Takeout ✓")
        else:
            options.append("Takeout ✗")
        
        results.append(f"""
{name} (ID: {place_id}):
  {', '.join(options)}
""")
    
    return "\n---\n".join(results) if results else "No results found."


@mcp.tool()
async def check_vegetarian_options(
    place_ids: str | list[str],
    use_stored: bool = False
) -> str:
    """Check which places serve vegetarian or vegan food.
    
    Args:
        place_ids: Comma-separated string or list of Google Place IDs (from find_restaurants_or_coffee_shops)
                  Can also use "latest" to use the most recent search results
        use_stored: If True, use stored place IDs from latest search (default: False)
    
    Returns:
        Formatted list showing vegetarian/vegan availability for each place
    """
    # Handle different input formats
    if use_stored and "latest" in _stored_place_ids:
        place_ids_list = _stored_place_ids["latest"]
    elif isinstance(place_ids, str):
        if place_ids.lower() == "latest":
            place_ids_list = _stored_place_ids.get("latest", [])
        else:
            # Split comma-separated string
            place_ids_list = [pid.strip() for pid in place_ids.split(",") if pid.strip()]
    else:
        place_ids_list = place_ids if isinstance(place_ids, list) else []
    
    if not place_ids_list:
        return "No place IDs provided. Use find_restaurants_or_coffee_shops first, or pass place_ids parameter."
    
    results = []
    vegetarian_places = []
    
    for place_id in place_ids_list:
        place_details = await api_clients.get_place_details_google(place_id)
        
        if not place_details:
            results.append(f"Place ID {place_id}: Unable to fetch details")
            continue
        
        name = place_details.get("displayName", {}).get("text", "Unknown")
        vegetarian = place_details.get("servesVegetarianFood", False)
        
        options = []
        if vegetarian:
            options.append("Vegetarian ✓")
            vegetarian_places.append(name)
        else:
            options.append("Vegetarian ✗")
        
        results.append(f"""
{name} (ID: {place_id}):
  {', '.join(options)}
""")
    
    result_text = "\n---\n".join(results) if results else "No results found."
    
    if vegetarian_places:
        result_text += f"\n\nPlaces serving vegetarian food: {', '.join(vegetarian_places)}"
    
    return result_text


@mcp.tool()
async def find_events_in_city(
    city: str,
    country: str,
    limit: int = 10
) -> str:
    """Find events in a city using the Ticketmaster Discovery API.

    Args:
        city: City name (e.g., "San Francisco", "London")
        country: Country name or ISO 2-letter code (e.g., "United States", "US", "UK")
        limit: Maximum number of results (default: 10)

    Returns:
        Formatted list of events with names, dates, venues, IDs, and URLs
    """
    result = await api_clients.search_events_ticketmaster(
        city=city,
        country=country,
        limit=limit
    )

    if not result:
        return "Unable to search events. Check TICKETMASTER_API_KEY and try again."

    embedded = result.get("_embedded") or {}
    events = embedded.get("events") or []

    if not events:
        return f"No events found in {city}, {country}."

    formatted_results = [f"Found {len(events)} event(s) in {city}, {country}:\n"]

    for i, event in enumerate(events, 1):
        formatted_results.append(f"{i}. {format_ticketmaster_event(event)}")

    event_ids = [e.get("id") for e in events if e.get("id")]
    _stored_event_ids["latest"] = event_ids

    result_text = "\n---\n".join(formatted_results)
    result_text += "\n\nEvent IDs stored. Use these IDs to look up event or ticket details from Ticketmaster."

    return result_text


@mcp.tool()
async def get_event_details_ticketmaster(event_id: str) -> str:
    """Get full details for a single Ticketmaster event (price range, info, venue address).

    Args:
        event_id: Ticketmaster event ID (from find_events_in_city or find_events_by_keyword).

    Returns:
        Event name, date, venue, address, price range, info/notes, and ticket URL.
    """
    if not event_id or not str(event_id).strip():
        return "No event ID provided. Use find_events_in_city first to get event IDs."
    event = await api_clients.get_event_ticketmaster(str(event_id).strip())
    if not event:
        return f"Could not load event {event_id}. Check the ID and TICKETMASTER_API_KEY."
    # Some APIs return event inside _embedded.events
    embedded = event.get("_embedded") or {}
    events_list = embedded.get("events") or []
    if events_list:
        event = events_list[0]
    return format_ticketmaster_event_details(event)


@mcp.tool()
async def find_events_by_keyword(
    city: str,
    country: str,
    keyword: str,
    limit: int = 10
) -> str:
    """Find events in a city matching a keyword (artist, team, show name, etc.).

    Args:
        city: City name (e.g., "San Francisco")
        country: Country name or ISO 2-letter code (e.g., "US", "United States")
        keyword: Search term (e.g., "Taylor Swift", "Warriors", "comedy")
        limit: Maximum number of results (default: 10)

    Returns:
        Formatted list of matching events with names, dates, venues, IDs, and URLs.
    """
    result = await api_clients.search_events_ticketmaster_ext(
        city=city,
        country=country,
        keyword=keyword.strip(),
        limit=limit,
    )
    if not result:
        return "Unable to search events. Check TICKETMASTER_API_KEY and try again."
    embedded = result.get("_embedded") or {}
    events = embedded.get("events") or []
    if not events:
        return f"No events found in {city} matching '{keyword}'."
    formatted = [f"Found {len(events)} event(s) in {city} matching '{keyword}':\n"]
    for i, event in enumerate(events, 1):
        formatted.append(f"{i}. {format_ticketmaster_event(event)}")
    event_ids = [e.get("id") for e in events if e.get("id")]
    _stored_event_ids["latest"] = event_ids
    result_text = "\n---\n".join(formatted)
    result_text += "\n\nEvent IDs stored for follow-up (e.g. get_event_details_ticketmaster)."
    return result_text


@mcp.tool()
async def find_events_by_date_range(
    city: str,
    country: str,
    start_date: str,
    end_date: str,
    limit: int = 10
) -> str:
    """Find events in a city within a date range.

    Args:
        city: City name (e.g., "San Francisco")
        country: Country name or ISO 2-letter code (e.g., "US")
        start_date: Start date in ISO 8601, e.g. 2024-06-01T00:00:00Z
        end_date: End date in ISO 8601, e.g. 2024-06-01T00:00:00Z
        limit: Maximum number of results (default: 10)

    Returns:
        Formatted list of events in the date range.
    """
    result = await api_clients.search_events_ticketmaster_ext(
        city=city,
        country=country,
        start_date=start_date.strip(),
        end_date=end_date.strip(),
        limit=limit,
    )
    if not result:
        return "Unable to search events. Check TICKETMASTER_API_KEY and try again."
    embedded = result.get("_embedded") or {}
    events = embedded.get("events") or []
    if not events:
        return f"No events found in {city} between {start_date} and {end_date}."
    formatted = [f"Found {len(events)} event(s) in {city} ({start_date} to {end_date}):\n"]
    for i, event in enumerate(events, 1):
        formatted.append(f"{i}. {format_ticketmaster_event(event)}")
    event_ids = [e.get("id") for e in events if e.get("id")]
    _stored_event_ids["latest"] = event_ids
    result_text = "\n---\n".join(formatted)
    result_text += "\n\nEvent IDs stored for follow-up."
    return result_text


@mcp.tool()
async def find_venues_in_city(
    city: str,
    country: str = "US",
    limit: int = 10
) -> str:
    """Find venues (arenas, theaters, clubs) in a city using Ticketmaster.

    Args:
        city: City name (e.g., "San Francisco", "London")
        country: Country name or ISO 2-letter code (default: "US")
        limit: Maximum number of results (default: 10)

    Returns:
        Formatted list of venues with names, addresses, IDs, and URLs.
    """
    result = await api_clients.search_venues_ticketmaster(
        city=city,
        country=country,
        limit=limit,
    )
    if not result:
        return "Unable to search venues. Check TICKETMASTER_API_KEY and try again."
    embedded = result.get("_embedded") or {}
    venues = embedded.get("venues") or []
    if not venues:
        return f"No venues found in {city}, {country}."
    formatted = [f"Found {len(venues)} venue(s) in {city}, {country}:\n"]
    for i, venue in enumerate(venues, 1):
        formatted.append(f"{i}. {format_ticketmaster_venue(venue)}")
    result_text = "\n---\n".join(formatted)
    result_text += "\n\nUse venue IDs with find_events_at_venue to see upcoming events."
    return result_text


@mcp.tool()
async def get_venue_details_ticketmaster(venue_id: str) -> str:
    """Get full details for a single Ticketmaster venue.

    Args:
        venue_id: Ticketmaster venue ID (from find_venues_in_city).

    Returns:
        Venue name, address, and URL.
    """
    if not venue_id or not str(venue_id).strip():
        return "No venue ID provided. Use find_venues_in_city first."
    venue = await api_clients.get_venue_ticketmaster(str(venue_id).strip())
    if not venue:
        return f"Could not load venue {venue_id}. Check the ID and TICKETMASTER_API_KEY."
    embedded = venue.get("_embedded") or {}
    venues_list = embedded.get("venues") or []
    if venues_list:
        venue = venues_list[0]
    return format_ticketmaster_venue(venue)


@mcp.tool()
async def find_events_at_venue(
    venue_id: str,
    limit: int = 10
) -> str:
    """Find upcoming events at a specific venue.

    Args:
        venue_id: Ticketmaster venue ID (from find_venues_in_city)
        limit: Maximum number of results (default: 10)

    Returns:
        Formatted list of events at that venue.
    """
    if not venue_id or not str(venue_id).strip():
        return "No venue ID provided. Use find_venues_in_city first."
    result = await api_clients.search_events_ticketmaster_ext(
        venue_id=str(venue_id).strip(),
        country="US",
        limit=limit,
    )
    if not result:
        return "Unable to search events. Check TICKETMASTER_API_KEY and try again."
    embedded = result.get("_embedded") or {}
    events = embedded.get("events") or []
    if not events:
        return f"No events found at venue {venue_id}."
    formatted = [f"Found {len(events)} event(s) at this venue:\n"]
    for i, event in enumerate(events, 1):
        formatted.append(f"{i}. {format_ticketmaster_event(event)}")
    event_ids = [e.get("id") for e in events if e.get("id")]
    _stored_event_ids["latest"] = event_ids
    result_text = "\n---\n".join(formatted)
    result_text += "\n\nEvent IDs stored for follow-up."
    return result_text


# TODO Add your own tools here
# Find tool ideas in TOOL_IDEAS.md

# TODO Tool 1
# @mcp.tool()
# Tool 1 definition

# TODO Tool 2
# @mcp.tool()
# Tool 2 definition

# ...more tools...


@mcp.resource("place://{key}")
def get_place_ids(key: str) -> str:
    """Get stored place IDs by key.
    
    Args:
        key: Key to retrieve (e.g., "latest")
    
    Returns:
        Comma-separated list of place IDs
    """
    if key in _stored_place_ids:
        return ",".join(_stored_place_ids[key])
    return "No place IDs found for this key."


@mcp.resource("event://{key}")
def get_event_ids(key: str) -> str:
    """Get stored event IDs by key.
    
    Args:
        key: Key to retrieve (e.g., "latest")
    
    Returns:
        Comma-separated list of event IDs
    """
    if key in _stored_event_ids:
        return ",".join(_stored_event_ids[key])
    return "No event IDs found for this key."


# TODO Add your own resources here
# @mcp.resource("resource://{key}")
# Resource definition

# TODO Resource 1
# @mcp.resource("resource://{key}")
# Resource 1 definition

# TODO Resource 2
# @mcp.resource("resource://{key}")
# Resource 2 definition
# ...more resources...

@mcp.prompt()
def plan_concert_and_dinner(city: str) -> str:
    """Generates a user message to plan a concert and dinner in a given city.
    
    Args:
        city: City name (e.g., "San Francisco")
    
    Returns:
        Prompt message to plan a concert and dinner in a given city
    """
    return f"Plan a veg-friendly dinner and a concert in {city}"

@mcp.prompt()
def full_day_plan(city: str, date: str) -> str:
    """Generates a user message to plan a full day in a given city on a given date. Includes coffee, event and dinner.
    
    Args:
        city: City name (e.g., "San Francisco")
        date: Date (e.g., "2026-03-01")
    
    Returns:
        Prompt message to plan a full day in a given city on a given date
    """
    return f"Plan a full day in {city} on {date} - include coffee places, events and dinner"


# TODO Add your own prompt here
# @mcp.prompt()

# TODO Prompt 1
# @mcp.prompt()

# TODO Prompt 2
# @mcp.prompt()
# Prompt 2 definition
# ...more prompts...

def main():
    """Initialize and run the MCP server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
