# Additional Tools for Local Discovery MCP Server

This document suggests additional tools that would enhance the local discovery experience. This server uses **Google Places**, **Google Directions**, **Ticketmaster Discovery**, and **OpenRouter** only.

---

## Core Discovery Tools (Google Places API)

### 1. `find_attractions` / `find_things_to_do`
**Purpose**: Discover attractions, museums, parks, and activities (not just restaurants)
**API**: Google Places API (New) – Text Search with queries like "museums in San Francisco"
**Parameters**:
- `location` (str): City name or address (or lat/lng for bias)
- `category` (str, optional): Type of attraction (museum, park, zoo, theater, etc.)
- `limit` (int, optional): Number of results (default: 10)

**Example Use Cases**:
- "Find museums in San Francisco"
- "What parks are near me?"
- "Show me theaters in New York"

---

### 2. `find_places_open_now`
**Purpose**: Find restaurants/places that are currently open
**API**: Google Places API (New) – Text Search + Place Details `currentOpeningHours`
**Parameters**:
- `location` (str): City name or address
- `category` (str, optional): Filter by category (restaurants, cafes, etc.)
- `limit` (int, optional): Number of results (default: 10)

**Implementation**: Use Place Details field `currentOpeningHours` to filter or display open now

**Example Use Cases**:
- "What restaurants are open right now?"
- "Find coffee shops open near me"

---

### 3. `find_nearby_places`
**Purpose**: Find places near a specific location or coordinate
**API**: Google Places API (New) – Text Search with `locationBias` circle (lat/lng + radius)
**Parameters**:
- `latitude` (float): Latitude
- `longitude` (float): Longitude
- `radius` (int, optional): Radius in meters (default: 1000)
- `query` (str, optional): e.g. "restaurants", "cafes"
- `limit` (int, optional): Number of results (default: 10)

**Example Use Cases**:
- "What's near the Golden Gate Bridge?"
- "Find restaurants within 500m of my location"

---

### 4. `find_places_by_amenities`
**Purpose**: Find places with specific amenities (outdoor seating, etc.) – filter via Place Details after search
**API**: Google Places API (New) – Place Details returns various attributes; search then filter by details
**Parameters**:
- `location` (str): City name or address
- `amenities` (list, optional): Attributes to filter (e.g. outdoor seating)
- `limit` (int, optional): Number of results (default: 10)

**Example Use Cases**:
- "Find restaurants with outdoor seating"
- "Show me cafes with WiFi"

---

### 5. `get_place_photos`
**Purpose**: Get photos of a place to help users visualize it
**API**: Google Places API (New) – Place Details with `photos` in field mask, or Places Photo endpoint
**Parameters**:
- `place_id` (str): Google Place ID
- `limit` (int, optional): Number of photos (default: 5)

**Example Use Cases**:
- "Show me photos of this restaurant"
- "What does this place look like?"

---

## Event & Activity Tools

### 6. Ticketmaster Discovery API – Implemented tools

All use **Ticketmaster Discovery API v2**. Env: `TICKETMASTER_API_KEY` (https://developer.ticketmaster.com/).

| Tool | Purpose |
|------|--------|
| **`find_events_in_city`** | Events in a city (city, country, limit). Returns event IDs for follow-up. |
| **`get_event_details_ticketmaster`** | Full event details by ID: price range, info, venue address, URL. |
| **`find_events_by_keyword`** | Events in a city matching a keyword (artist, team, show name). |
| **`find_events_by_date_range`** | Events in a city between start_date and end_date (YYYY-MM-DD or ISO 8601). |
| **`find_venues_in_city`** | Venues (arenas, theaters, clubs) in a city. |
| **`get_venue_details_ticketmaster`** | Full venue details by ID (name, address, URL). |
| **`find_events_at_venue`** | Upcoming events at a specific venue (by venue ID). |

**Example flows**: "Events in SF" → `find_events_in_city`; "Comedy in London" → `find_events_by_keyword`; "What’s at Chase Center?" → `find_venues_in_city` (get venue ID) → `find_events_at_venue`; "Events June 1–7 in NYC" → `find_events_by_date_range`.

---

### 7. Ticketmaster – Optional tools you can add

| Tool | API / params | Purpose |
|------|--------------|--------|
| **`find_events_by_classification`** | `classificationName` (Music, Sports, Arts, Film, Miscellaneous) | Filter by type. |
| **`find_attractions_ticketmaster`** | `keyword`, `country` → `GET .../attractions.json` | Search artists/teams/attractions; then use `attractionId` in event search. |
| **`get_attraction_details_ticketmaster`** | `attraction_id` → `GET .../attractions/{id}.json` | Details for an artist/attraction. |
| **`find_events_near_location`** | `latlong`, `radius` (miles) → events.json | Events near lat/long (e.g. "near me"). |
| **`list_classifications_ticketmaster`** | `GET .../classifications.json` (segment/category tree) | Expose genre/category list to users. |

---

### 8. `find_events_by_date` (covered by Ticketmaster)
**Purpose**: Find events on a specific date or date range.  
**Implemented as**: `find_events_by_date_range(city, country, start_date, end_date, limit)` (Ticketmaster).  
**Example**: "What events are happening this weekend?" → use start/end of weekend in YYYY-MM-DD.

---

### 9. `find_free_events`
**Purpose**: Find free events (no ticket cost)
**API**: Ticketmaster Discovery API – filter or post-filter events by price (e.g. free or minimal cost) when returned in event details
**Parameters**:
- `city` (str): City name
- `country` (str): Country name or code
- `limit` (int, optional): Number of results (default: 10)

**Implementation**: Use Ticketmaster event search; filter results where price indicates free when available

---

## Location & Navigation Tools

### 11. `calculate_distance`
**Purpose**: Calculate distance between two locations
**API**: Simple calculation (Haversine formula) or geocoding API
**Parameters**:
- `lat1` (float): Latitude of first location
- `lon1` (float): Longitude of first location
- `lat2` (float): Latitude of second location
- `lon2` (float): Longitude of second location
- `unit` (str, optional): "km" or "miles" (default: "km")

**Implementation**: Can be done locally using Haversine formula (no API needed!)

**Example Use Cases**:
- "How far is this restaurant from me?"
- "Which event is closest to my location?"

---

### 12. `geocode_location`
**Purpose**: Convert address to coordinates (or vice versa)
**API**: OpenStreetMap Nominatim API (FREE, no auth)
**Parameters**:
- `address` (str): Address or place name
- `reverse` (bool, optional): If true, convert coordinates to address

**Endpoint**: `GET https://nominatim.openstreetmap.org/search`

**Example Use Cases**:
- "Get coordinates for '123 Main St, San Francisco'"
- "What's the address at 37.7749, -122.4194?"

---

## Recommendation & Filtering Tools

### 13. `find_places_by_price`
**Purpose**: Find places filtered by price range
**API**: Google Places API (New) – Text Search with price-level intent; Place Details may expose price level where available
**Parameters**:
- `location` (str): City name or address
- `price_min` (int, optional): Minimum price level (1-4)
- `price_max` (int, optional): Maximum price level (1-4)
- `category` (str, optional): Filter by category
- `limit` (int, optional): Number of results (default: 10)

**Example Use Cases**:
- "Find budget restaurants ($)"
- "Show me mid-range places ($$)"

---

### 14. `find_places_by_rating`
**Purpose**: Find places filtered by minimum rating
**API**: Google Places API (New) – Place Details or search; use rating data where exposed
**Parameters**:
- `location` (str): City name or address
- `min_rating` (float): Minimum rating (0.0-10.0)
- `category` (str, optional): Filter by category
- `limit` (int, optional): Number of results (default: 10)

**Example Use Cases**:
- "Show me highly rated restaurants (4+ stars)"
- "Find top-rated museums"

---

### 15. `find_similar_places`
**Purpose**: Find places similar to a given place
**API**: Google Places API (New) – use Place Details for category/type then Text Search nearby with same type
**Parameters**:
- `place_id` (str): Google Place ID
- `limit` (int, optional): Number of results (default: 5)

**Implementation**: Use same category and nearby location

**Example Use Cases**:
- "Find restaurants similar to this one"
- "Show me other places like this"

---

## Integration Tools

### 16. `get_weather_for_event`
**Purpose**: Get weather forecast for an event date/location
**API**: NWS API (FREE - same as weather MCP server!)
**Parameters**:
- `latitude` (float): Latitude of event location
- `longitude` (float): Longitude of event location
- `date` (str, optional): Date to check (YYYY-MM-DD), defaults to event date

**Note**: Can reuse weather MCP server logic or call NWS API directly

**Example Use Cases**:
- "What's the weather for this outdoor event?"
- "Will it rain during the concert?"

---

### 17. `get_trending_places`
**Purpose**: Find currently popular or trending places
**API**: Google Places API (New) – Text Search; sort or filter by prominence/user_ratings_total where available
**Parameters**:
- `location` (str): City name or address
- `category` (str, optional): Filter by category
- `limit` (int, optional): Number of results (default: 10)

**Implementation**: Use relevance/prominence and rating count where exposed

**Example Use Cases**:
- "What's trending in San Francisco?"
- "Show me popular places right now"

---

## Dietary & Accessibility Tools

### 18. `find_places_by_dietary`
**Purpose**: Find places that accommodate dietary restrictions
**API**: Google Places API (New) – Place Details `servesVegetarianFood` etc.; search then filter or use check_vegetarian_options pattern
**Parameters**:
- `location` (str): City name or address
- `dietary` (str): Dietary restriction (vegetarian, vegan, etc.)
- `limit` (int, optional): Number of results (default: 10)

**Implementation**: Use Place Details dietary fields (e.g. servesVegetarianFood) after search

**Example Use Cases**:
- "Find vegan restaurants"
- "Show me gluten-free options"

---

### 19. `find_accessible_places`
**Purpose**: Find wheelchair-accessible places
**API**: Google Places API (New) – Place Details accessibility attributes where available
**Parameters**:
- `location` (str): City name or address
- `category` (str, optional): Filter by category
- `limit` (int, optional): Number of results (default: 10)

**Example Use Cases**:
- "Find wheelchair-accessible restaurants"
- "Show me accessible museums"

---

## Information Tools

### 20. `get_neighborhood_info`
**Purpose**: Get information about a neighborhood/area
**API**: OpenStreetMap Nominatim API (free) or Google Places Text Search for area overview
**Parameters**:
- `location` (str): Neighborhood name or address
- `info_type` (str, optional): Type of info (demographics, nearby_places, etc.)

**Example Use Cases**:
- "Tell me about the Mission District"
- "What's in this neighborhood?"

---

### 21. `get_place_tips` / reviews
**Purpose**: Get reviews or editorial summary for a place
**API**: Google Places API (New) – Place Details with reviews/summary in field mask where available
**Parameters**:
- `place_id` (str): Google Place ID
- `limit` (int, optional): Number of reviews (default: 5)

---

### 22. `compare_places`
**Purpose**: Compare multiple places side-by-side
**API**: Google Places API (New) – fetch Place Details for each ID and format comparison
**Parameters**:
- `place_ids` (list): List of Google Place IDs (2-5 places)

**Returns**: Side-by-side comparison of ratings, prices, hours, etc.

**Example Use Cases**:
- "Compare these three restaurants"
- "Which place is better?"

---

## Recommended Priority Order for Implementation

### Phase 1 (Essential - Extend Core Functionality):
1. ✅ `find_attractions` / `find_things_to_do` - Core discovery beyond restaurants
2. ✅ `find_places_open_now` - Very practical for users
3. ✅ `find_nearby_places` - Location-based discovery
4. ✅ `get_place_photos` - Visual information

### Phase 2 (Event Enhancements):
5. ✅ `get_event_details_ticketmaster` - Complete event information
6. ✅ `find_events_by_date_range` - Date-based event search
7. ✅ `get_weather_for_event` - Practical integration

### Phase 3 (Filtering & Recommendations):
8. ✅ `find_places_by_amenities` - Specific needs
9. ✅ `find_places_by_price` - Budget filtering
10. ✅ `find_places_by_rating` - Quality filtering
11. ✅ `calculate_distance` - Location utility

### Phase 4 (Advanced Features):
12. ✅ `find_places_by_dietary` - Dietary restrictions
13. ✅ `find_similar_places` - Recommendations
14. ✅ `get_trending_places` - Popularity
15. ✅ `compare_places` - Decision support

---

## Implementation Notes

### Google Places API:
- Use Text Search for discovery; use Place Details with field masks for attributes (dineIn, delivery, servesVegetarianFood, etc.)
- Request only needed fields via `X-Goog-FieldMask` to reduce cost and latency

### Rate Limits:
- **Google Places/Directions**: Check Google Cloud quota for your project
- **Ticketmaster**: Check developer portal for limits
- **OpenRouter**: 50 requests/day, 20/minute (free tier)
- **Nominatim**: Be respectful - add delays between requests

### Error Handling:
- Handle missing data gracefully (not all places have photos, hours, etc.)
- Provide fallbacks when data is unavailable
- Cache frequently accessed data to reduce API calls

### Code Organization:
- Group related tools together
- Reuse API client functions
- Create formatters for each data type
- Follow the same patterns as existing tools

---

## Example Tool Implementation Structure

```python
@mcp.tool()
async def find_attractions(
    location: str,
    category: str | None = None,
    limit: int = 10
) -> str:
    """Find attractions, museums, parks, and things to do in a location.
    
    Args:
        location: City name or address
        category: Type of attraction (museum, park, zoo, theater, etc.)
        limit: Number of results (default: 10)
    """
    # Implementation using Google Places API (Text Search)
    # Use textQuery e.g. "museums in {location}"
    # Format and return results
```

---

## Summarization & LLM-based Tools

### Implemented

- **`summarize_recommendations`** – Summarizes the raw output from any discovery tool (restaurants, events, dine-in/vegetarian/ticket info) into a short paragraph. Uses OpenRouter (free Llama model). Requires `OPENROUTER_API_KEY`. Parameters: `text` (output from another tool), `max_words` (default 100).

### Ideas you can add

1. **`recommend_from_results`** – Input: result text + optional user criteria (e.g. "vegetarian", "with outdoor seating", "family-friendly"). LLM picks the best 1–2 options and returns a short recommendation with reasoning.
2. **`itinerary_summary`** – Input: city, date, and optional constraints. Chain: find events + find restaurants (+ travel time). Pass combined text to LLM to produce a "plan for the day" or "top 3 options" narrative.
3. **`compare_places_narrative`** – Input: 2–3 place names/IDs (or "latest"). Fetch details, format as text, then LLM returns a short comparison ("Best for X…", "Best for Y…").
4. **`answer_question_about_place`** – Input: place_id + free-form question (e.g. "Is this good for kids?", "Is it quiet?"). Fetch place details (and reviews/tips if available), send to LLM, return a direct answer (with "I don’t have that information" when appropriate).
5. **Template-based summary (no LLM)** – A `summarize_places_bullets` that takes stored place IDs and returns a fixed-format summary (e.g. "N places: A (delivery ✓), B (vegan ✓), C (takeout ✓)") without calling an LLM; useful when no API key or when you want deterministic output.

### Implementation notes

- **OpenRouter**: Free tier (e.g. `meta-llama/llama-3.1-8b-instruct:free`), 50 req/day, 20/min. Key via `OPENROUTER_API_KEY`.
- **Security**: Do not send PII or secrets in prompts; keep prompts and responses logged only if safe (no credentials). Validate and limit `max_words` / `max_tokens` to avoid abuse.
- **Fallback**: If no key or API error, return a clear message and optionally a short template summary (e.g. first 3 lines of the input).

---

## Resources for Implementation

- **Google Places API (New)**: https://developers.google.com/maps/documentation/places/web-service/overview
- **Google Directions API**: https://developers.google.com/maps/documentation/directions
- **Ticketmaster Discovery API**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
- **OpenRouter**: https://openrouter.ai/docs
- **Nominatim API**: https://nominatim.org/release-docs/latest/api/Search/
- **Haversine Formula**: https://en.wikipedia.org/wiki/Haversine_formula
