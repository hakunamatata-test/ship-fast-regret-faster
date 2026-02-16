# Local Discovery & Events MCP Server

An MCP (Model Context Protocol) server that helps you discover local restaurants, events, and activities, check dine-in/delivery/vegetarian options, get event and venue details, and summarize recommendations.

**Story**: *"Help me discover local restaurants, events, and activities in my area, get reviews, and summarize recommendations."*

---

## Overview

This server uses **four APIs**:

- **Google Places API (New)** – place search and place details (dine-in, delivery, takeout, vegetarian, etc.)
- **Google Directions API** – travel time between two locations (driving, walking, bicycling, transit)
- **Ticketmaster Discovery API** – events and venues (search by city, keyword, date range; event/venue details)
- **OpenRouter API** – LLM summarization of discovery results (free tier with models like Llama)

---

## Tools

| Tool | Description |
|------|-------------|
| `find_restaurants_or_coffee_shops` | Search restaurants or coffee shops in a city (Google Places). Results are stored for follow-up tools. |
| `check_dine_in_delivery_options` | Check which places offer dine-in, delivery, or takeout (by place IDs or `"latest"`). |
| `check_vegetarian_options` | Check which places serve vegetarian/vegan (by place IDs or `"latest"`). |
| `find_events_in_city` | Find events in a city (Ticketmaster). |
| `find_events_by_keyword` | Find events in a city matching a keyword (artist, team, show name). |
| `find_events_by_date_range` | Find events in a city between two dates. |
| `get_event_details_ticketmaster` | Full event details by ID (price range, venue address, URL). |
| `find_venues_in_city` | Find venues (arenas, theaters, clubs) in a city. |
| `get_venue_details_ticketmaster` | Full venue details by ID. |
| `find_events_at_venue` | Upcoming events at a specific venue. |
| `get_travel_time` | Travel time and distance between two coordinates (driving, walking, bicycling, transit). |
| `summarize_recommendations` | Summarize discovery results (e.g. from the tools above) into a short paragraph via OpenRouter. |

## Resources

- **`place://{key}`** – Stored place IDs (e.g. `place://latest` after a place search).
- **`event://{key}`** – Stored event IDs (e.g. `event://latest` after an event search).

---

## Setup

### 1. Install dependencies

From the `local-discovery` directory:

```bash
uv sync
# or: pip install -e .
```

### 2. API keys

Create a `.env` file in `local-discovery` (and add it to `.gitignore`). Required variables:

| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` | Google Cloud API key with **Places API (New)** and **Directions API** enabled. |
| `TICKETMASTER_API_KEY` | [Ticketmaster Discovery API](https://developer.ticketmaster.com/) key. |
| `OPENROUTER_API_KEY` | [OpenRouter](https://openrouter.ai/) key for summarization (free tier: 50 req/day, 20/min). |

Example `.env`:

```env
GOOGLE_API_KEY=your_google_api_key
TICKETMASTER_API_KEY=your_ticketmaster_key
OPENROUTER_API_KEY=your_openrouter_key
```

---

## Running the server

Start the MCP server (stdio transport):

```bash
uv run python local_discovery.py
```

Or with Python directly:

```bash
python local_discovery.py
```

Use this server from any MCP client (e.g. Claude Desktop, Cursor) by configuring it to run the above command.

---

## Project structure

```
local-discovery/
├── README.md           # This file
├── PLAN.md             # Implementation plan and tool details
├── API_REFERENCE.md    # API endpoints and auth
├── ADDITIONAL_TOOLS.md  # More tool ideas (Google Places / Ticketmaster)
├── GOOGLE_PLACES_TOOLS.md
├── pyproject.toml      # Dependencies
├── local_discovery.py  # MCP server (tools, resources, entrypoint)
├── api_clients.py      # Google, Ticketmaster, OpenRouter API clients
└── .env                # API keys (create locally, do not commit)
```

---

## Documentation

- **[API_REFERENCE.md](./API_REFERENCE.md)** – APIs used (Google Places, Directions, Ticketmaster, OpenRouter).
- **[PLAN.md](./PLAN.md)** – Implementation plan, tool specs, and extension ideas.
- **[ADDITIONAL_TOOLS.md](./ADDITIONAL_TOOLS.md)** – Extra tools you can add (attractions, open now, photos, etc.).
- **[GOOGLE_PLACES_TOOLS.md](./GOOGLE_PLACES_TOOLS.md)** – Google Places–specific tool ideas.

---

## Architecture

- **FastMCP** for tool and resource registration.
- **Async HTTP** via `httpx` in `api_clients.py`.
- **In-memory storage** for the latest place and event IDs (exposed as resources).
- **Error handling** and safe handling of missing API keys or failed requests.

Rate limits: respect Google Cloud and Ticketmaster quotas; OpenRouter free tier is 50 requests/day and 20/minute.
