import os
from typing import Any
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

# API Base URLs
GOOGLE_PLACES_BASE_URL = "https://places.googleapis.com/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
TICKETMASTER_BASE_URL = "https://app.ticketmaster.com/discovery/v2/"

async def make_google_places_request(
    endpoint: str,
    data: dict[str, Any],
    method: str = "POST",
    field_mask: str | None = None
) -> dict[str, Any] | None:
    """Make a request to Google Places API (New).
    
    Args:
        endpoint: API endpoint path (e.g., "places:searchText")
        data: Request body data as dictionary
        method: HTTP method (default: "POST")
        field_mask: Optional field mask (default: basic fields for search)
    
    Returns:
        Parsed JSON response or None if error
    """
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return None
    
    url = f"{GOOGLE_PLACES_BASE_URL}/{endpoint}"
    
    # Default field mask for search endpoints
    if field_mask is None:
        field_mask = "places.id,places.formattedAddress,places.displayName,places.location"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": field_mask
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "POST":
                response = await client.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
            else:
                response = await client.get(
                    url,
                    headers=headers,
                    params=data,
                    timeout=30.0
                )
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error making Google Places API request: {e}")
            return None


async def search_places_google(
    text_query: str,
    location: dict[str, float] | None = None,
    max_result_count: int = 10,
    language_code: str = "en"
) -> dict[str, Any] | None:
    """Search places using Google Places API Text Search.
    
    Args:
        text_query: Search query (e.g., "coffee shops in Redmond")
        location: Optional location bias with lat/lng (e.g., {"latitude": 47.6740, "longitude": -122.1215})
        max_result_count: Maximum number of results (default: 10)
        language_code: Language code for results (default: "en")
    
    Returns:
        JSON response with places array or None if error
    
    Example:
        result = await search_places_google(
            "coffee shops in Redmond",
            location={"latitude": 47.6740, "longitude": -122.1215}
        )
    """
    request_data = {
        "textQuery": text_query,
        "maxResultCount": max_result_count,
        "languageCode": language_code
    }
    
    # Add location bias if provided
    if location:
        request_data["locationBias"] = {
            "circle": {
                "center": {
                    "latitude": location["latitude"],
                    "longitude": location["longitude"]
                },
                "radius": 5000.0  # 5km radius
            }
        }
    
    return await make_google_places_request("places:searchText", request_data)


# ISO 2-letter country codes for Ticketmaster (country param -> countryCode)
_COUNTRY_TO_CODE: dict[str, str] = {
    "us": "US", "usa": "US", "united states": "US", "united states of america": "US",
    "uk": "GB", "gb": "GB", "united kingdom": "GB", "great britain": "GB",
    "ca": "CA", "canada": "CA", "au": "AU", "australia": "AU",
    "de": "DE", "germany": "DE", "fr": "FR", "france": "FR",
    "es": "ES", "spain": "ES", "it": "IT", "italy": "IT",
    "nl": "NL", "netherlands": "NL", "ie": "IE", "ireland": "IE",
    "mx": "MX", "mexico": "MX", "br": "BR", "brazil": "BR",
    "jp": "JP", "japan": "JP", "in": "IN", "india": "IN",
}


def _normalize_country_code(country: str) -> str:
    """Return ISO 2-letter country code for Ticketmaster API."""
    if not country:
        return "US"
    key = country.strip().lower()
    if len(key) == 2:
        return key.upper()
    return _COUNTRY_TO_CODE.get(key, key.upper()[:2] if len(key) >= 2 else "US")


async def search_events_ticketmaster(
    city: str,
    country: str,
    limit: int = 10
) -> dict[str, Any] | None:
    """Search events using Ticketmaster Discovery API v2.

    Args:
        city: City name (e.g., "San Francisco")
        country: Country name or ISO 2-letter code (e.g., "United States" or "US")
        limit: Maximum number of results (default: 10, API max 200)

    Returns:
        Parsed JSON with _embedded.events or None if error
    """
    if not TICKETMASTER_API_KEY:
        print("Error: TICKETMASTER_API_KEY not found in environment variables")
        return None

    country_code = _normalize_country_code(country)
    url = f"{TICKETMASTER_BASE_URL}events.json"

    params: dict[str, Any] = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city.strip(),
        "countryCode": country_code,
        "size": min(max(1, limit), 200),
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error making Ticketmaster API request: {e}")
            return None


async def get_event_ticketmaster(event_id: str) -> dict[str, Any] | None:
    """Get a single event by ID using Ticketmaster Discovery API v2.

    Args:
        event_id: Ticketmaster event ID (from find_events_in_city or search).

    Returns:
        Event object or None if not found or error.
    """
    if not TICKETMASTER_API_KEY:
        print("Error: TICKETMASTER_API_KEY not found in environment variables")
        return None
    if not event_id or not str(event_id).strip():
        return None

    url = f"{TICKETMASTER_BASE_URL}events/{str(event_id).strip()}.json"
    params: dict[str, Any] = {"apikey": TICKETMASTER_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error fetching Ticketmaster event: {e}")
            return None


async def search_events_ticketmaster_ext(
    city: str | None = None,
    country: str = "US",
    keyword: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    classification_name: str | None = None,
    venue_id: str | None = None,
    limit: int = 10,
) -> dict[str, Any] | None:
    """Search events with optional keyword, date range, classification, or venue.

    Date format: YYYY-MM-DD or ISO 8601 (e.g. 2024-06-01T00:00:00Z).
    classification_name examples: Music, Sports, Arts, Film, Miscellaneous.

    Returns:
        Parsed JSON with _embedded.events or None.
    """
    if not TICKETMASTER_API_KEY:
        print("Error: TICKETMASTER_API_KEY not found in environment variables")
        return None

    country_code = _normalize_country_code(country)
    url = f"{TICKETMASTER_BASE_URL}events.json"
    params: dict[str, Any] = {
        "apikey": TICKETMASTER_API_KEY,
        "countryCode": country_code,
        "size": min(max(1, limit), 200),
    }
    if city:
        params["city"] = city.strip()
    if keyword:
        params["keyword"] = keyword.strip()
    if start_date:
        params["startDateTime"] = start_date.strip()
    if end_date:
        params["endDateTime"] = end_date.strip()
    if classification_name:
        params["classificationName"] = classification_name.strip()
    if venue_id:
        params["venueId"] = str(venue_id).strip()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error making Ticketmaster API request: {e}")
            return None


async def search_venues_ticketmaster(
    city: str,
    country: str = "US",
    limit: int = 10,
) -> dict[str, Any] | None:
    """Search venues by city using Ticketmaster Discovery API v2.

    Returns:
        Parsed JSON with _embedded.venues or None.
    """
    if not TICKETMASTER_API_KEY:
        print("Error: TICKETMASTER_API_KEY not found in environment variables")
        return None

    country_code = _normalize_country_code(country)
    url = f"{TICKETMASTER_BASE_URL}venues.json"
    params: dict[str, Any] = {
        "apikey": TICKETMASTER_API_KEY,
        "city": city.strip(),
        "countryCode": country_code,
        "size": min(max(1, limit), 200),
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error making Ticketmaster venues request: {e}")
            return None


async def get_venue_ticketmaster(venue_id: str) -> dict[str, Any] | None:
    """Get a single venue by ID using Ticketmaster Discovery API v2."""
    if not TICKETMASTER_API_KEY:
        print("Error: TICKETMASTER_API_KEY not found in environment variables")
        return None
    if not venue_id or not str(venue_id).strip():
        return None

    url = f"{TICKETMASTER_BASE_URL}venues/{str(venue_id).strip()}.json"
    params: dict[str, Any] = {"apikey": TICKETMASTER_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error fetching Ticketmaster venue: {e}")
            return None


async def get_place_details_google(
    place_id: str,
    fields: list[str] | None = None
) -> dict[str, Any] | None:
    """Get detailed information about a place using Google Places API.
    
    Args:
        place_id: Google Place ID
        fields: List of fields to request (e.g., ["dineIn", "delivery", "servesVegetarianFood"])
                If None, requests common fields including dining options
    
    Returns:
        JSON response with place details or None if error
    """
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return None
    
    # Default fields if not specified
    if fields is None:
        fields = [
            "id", "displayName", "formattedAddress", "location",
            "currentOpeningHours", "dineIn", "delivery", "takeout", 
            "servesVegetarianFood","servesBreakfast", "servesCoffee", 
            "servesDessert", "servesLunch", "servesDinner"
        ]
    
    url = f"{GOOGLE_PLACES_BASE_URL}/places/{place_id}"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": ",".join(fields)
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error getting place details: {e}")
            return None


async def get_travel_time_google(
    origin_lat: float,
    origin_lng: float,
    destination_lat: float,
    destination_lng: float,
    mode: str = "driving"
) -> dict[str, Any] | None:
    """Get travel time between two locations using Google Directions API.
    
    Args:
        origin_lat: Origin latitude
        origin_lng: Origin longitude
        destination_lat: Destination latitude
        destination_lng: Destination longitude
        mode: Travel mode - "driving", "walking", "bicycling", or "transit" (default: "driving")
    
    Returns:
        JSON response with route information including duration, or None if error
    """
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in environment variables")
        return None
    
    url = "https://maps.googleapis.com/maps/api/directions/json"
    
    params = {
        "origin": f"{origin_lat},{origin_lng}",
        "destination": f"{destination_lat},{destination_lng}",
        "mode": mode,
        "key": GOOGLE_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error getting travel time: {e}")
            return None


async def make_openrouter_request(
    prompt: str,
    model: str = "meta-llama/llama-3.1-8b-instruct:free",
    max_tokens: int = 150
) -> dict[str, Any] | None:
    """Make a request to OpenRouter LLM API.
    
    Args:
        prompt: The prompt text to send to the LLM
        model: Model to use (default: free Llama model)
        max_tokens: Maximum tokens in response (default: 150)
    
    Returns:
        Parsed JSON response or None if error
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found in environment variables")
        return None
    
    url = f"{OPENROUTER_BASE_URL}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"Error making OpenRouter API request: {e}")
            return None
