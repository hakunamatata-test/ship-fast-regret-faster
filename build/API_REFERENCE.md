# API Reference Guide

Quick reference for the APIs used in Local Discovery & Events MCP Server.

This server uses **four APIs only**: Google Places, Google Directions, Ticketmaster Discovery, and OpenRouter.

---

## Google Places API (New)

**Base URL**: `https://places.googleapis.com/v1`

### Authentication
```python
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GOOGLE_API_KEY,
    "X-Goog-FieldMask": "places.id,places.formattedAddress,places.displayName,places.location"
}
```

### Endpoints

#### 1. Text Search
**Endpoint**: `POST /places:searchText`

**Request body**:
- `textQuery`: Search query (e.g., "coffee shops in Redmond")
- `maxResultCount`: Max results (default 10)
- `languageCode`: e.g. "en"
- `locationBias` (optional): Circle with center lat/lng and radius

#### 2. Place Details
**Endpoint**: `GET /places/{place_id}`

**Headers**: `X-Goog-FieldMask` with requested fields (e.g. `id`, `displayName`, `formattedAddress`, `dineIn`, `delivery`, `takeout`, `servesVegetarianFood`, etc.)

---

## Google Directions API

**Endpoint**: `GET https://maps.googleapis.com/maps/api/directions/json`

### Query Parameters
- `origin`: `"{lat},{lng}"`
- `destination`: `"{lat},{lng}"`
- `mode`: `driving` | `walking` | `bicycling` | `transit`
- `key`: Google API key

**Response**: Route legs with `duration` and `distance` text/value.

---

## Ticketmaster Discovery API

**Base URL**: `https://app.ticketmaster.com/discovery/v2/`

### Authentication
API key as query parameter: `apikey={TICKETMASTER_API_KEY}`

### Endpoints

#### 1. Search Events
**Endpoint**: `GET events.json`
- `city`, `countryCode`, `keyword`, `startDateTime`, `endDateTime`, `size`, etc.

#### 2. Get Event by ID
**Endpoint**: `GET events/{event_id}.json` (with `_embedded=venues` for venue details)

#### 3. Search Venues
**Endpoint**: `GET venues.json`
- `city`, `countryCode`, `size`, etc.

#### 4. Get Venue by ID
**Endpoint**: `GET venues/{venue_id}.json`

---

## OpenRouter API (LLM)

**Base URL**: `https://openrouter.ai/api/v1`

### Authentication
```python
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}
```

### Endpoint
**Endpoint**: `POST /chat/completions`

**Request body**:
- `model`: e.g. `meta-llama/llama-3.1-8b-instruct:free`
- `messages`: `[{"role": "user", "content": "..."}]`
- `max_tokens`: e.g. 150

**Response**: `choices[0].message.content` for the summary text.

---

## Error Handling

- **Google APIs**: Check `response.status_code`; 400/401/403/404/429 possible.
- **Ticketmaster**: Same; use `apikey` and handle rate limits.
- **OpenRouter**: Same; respect rate limits (e.g. 50 req/day on free tier).

### Best Practices
- Store API keys in environment variables (e.g. `.env`).
- Validate input before making requests.
- Handle rate limiting (429) with backoff.
- Provide clear error messages to users.
