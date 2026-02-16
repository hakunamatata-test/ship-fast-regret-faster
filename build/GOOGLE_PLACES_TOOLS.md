# Additional Tools with Google Places API (New)

This document outlines **unique tools and features** that become possible when using Google Places API (New). This server uses only Google Places, Google Directions, Ticketmaster, and OpenRouter.

> **Note**: Google Places API has free usage thresholds but requires a Google Cloud account. See [FREE_API_ALTERNATIVES.md](./FREE_API_ALTERNATIVES.md) for pricing details.

---

## Autocomplete & Search Enhancement Tools

### 1. `autocomplete_places`
**Purpose**: Provide intelligent place autocomplete as user types
**Unique Feature**: Session-based pricing and better predictions
**API**: Google Places API Autocomplete (New)
**Parameters**:
- `input` (str): User's partial input text
- `location` (str, optional): Bias results toward location
- `types` (list, optional): Filter by place types (restaurant, museum, etc.)
- `session_token` (str, optional): Session token for billing grouping

**Benefits**:
- More accurate predictions than basic search
- Session tokens group autocomplete + selection for better pricing
- Supports place and query predictions
- Location biasing for better local results

**Example Use Cases**:
- "As user types 'Starbucks', show autocomplete suggestions"
- "Autocomplete restaurants near user's location"

---

### 2. `validate_address`
**Purpose**: Validate and standardize addresses
**API**: Google Places API Address Validation
**Parameters**:
- `address` (str): Address to validate
- `region_code` (str, optional): Country code (e.g., "US")

**Returns**: Validated address with standardized format, components, and verification status

**Example Use Cases**:
- "Is this address valid?"
- "Standardize this address format"

---

## Reviews & Ratings Tools

### 3. `get_detailed_reviews`
**Purpose**: Get structured reviews with ratings, text, author info, and time
**Unique Feature**: Google's extensive review database
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `limit` (int, optional): Number of reviews (default: 5)
- `sort_by` (str, optional): "most_relevant" or "newest"

**Returns**: 
- Review text, rating (1-5), author name, author photo
- Relative time description ("2 weeks ago")
- Language of review
- More structured than Foursquare tips

**Example Use Cases**:
- "Show me recent reviews for this restaurant"
- "What are people saying about this place?"

---

### 4. `get_review_summary`
**Purpose**: Get aggregated review statistics
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Overall rating (0-5)
- Total review count
- Rating distribution (how many 5-star, 4-star, etc.)
- Review summary if available

**Example Use Cases**:
- "What's the overall rating breakdown?"
- "How many reviews does this place have?"

---

## Accessibility & Special Needs Tools

### 5. `find_wheelchair_accessible_places`
**Purpose**: Find places with detailed wheelchair accessibility information
**Unique Feature**: Detailed accessibility data
**API**: Google Places API Place Details / Search
**Parameters**:
- `location` (str): City name or address
- `category` (str, optional): Filter by category
- `limit` (int, optional): Number of results (default: 10)

**Returns**: Places with:
- Wheelchair accessible entrance
- Accessible parking
- Accessible restrooms
- Accessible seating
- More detailed than basic "accessible" flag

**Example Use Cases**:
- "Find wheelchair accessible restaurants"
- "Show me accessible museums with parking"

---

### 6. `get_accessibility_details`
**Purpose**: Get detailed accessibility information for a specific place
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Entrance accessibility details
- Parking accessibility
- Restroom accessibility
- Seating accessibility
- Other accessibility features

---

## Opening Hours & Schedule Tools

### 7. `get_special_opening_hours`
**Purpose**: Get special/holiday hours that differ from regular schedule
**Unique Feature**: Special days and holiday hours
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `date` (str, optional): Specific date to check (YYYY-MM-DD)

**Returns**:
- Regular hours
- Special days (holidays, events with different hours)
- Next 7 days schedule
- Secondary opening hours (if applicable)

**Example Use Cases**:
- "Is this place open on Christmas?"
- "What are the special hours this week?"

---

### 8. `get_secondary_opening_hours`
**Purpose**: Get different schedules for different services (drive-through, dining room, etc.)
**Unique Feature**: Multiple schedules per place
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Primary hours (main service)
- Secondary hours (drive-through, delivery, etc.)
- Service type labels

**Example Use Cases**:
- "What are the drive-through hours vs dining room hours?"
- "When is delivery available?"

---

### 9. `check_if_open_at_time`
**Purpose**: Check if a place is open at a specific date/time
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `datetime` (str): Date and time to check (ISO 8601 format)

**Returns**: Boolean indicating if place is open at that time

**Example Use Cases**:
- "Is this restaurant open at 8 PM tomorrow?"
- "Will this place be open on New Year's Day?"

---

## Photo & Visual Tools

### 10. `get_place_photos_with_attribution`
**Purpose**: Get photos with proper attribution and metadata
**Unique Feature**: Millions of photos with attribution requirements
**API**: Google Places API Place Photos (New)
**Parameters**:
- `place_id` (str): Google Place ID
- `max_width` (int, optional): Max photo width in pixels
- `max_height` (int, optional): Max photo height in pixels
- `limit` (int, optional): Number of photos (default: 5)

**Returns**:
- Photo URLs (with proper sizing)
- Photo references
- Author attributions (required for display)
- Photo metadata

**Example Use Cases**:
- "Show me photos of this restaurant"
- "Get high-quality photos for display"

---

### 11. `get_photo_by_reference`
**Purpose**: Get a specific photo by its reference ID
**API**: Google Places API Place Photos (New)
**Parameters**:
- `photo_reference` (str): Photo reference ID
- `max_width` (int, optional): Max width
- `max_height` (int, optional): Max height

**Use Case**: When you have a photo reference from place details and want to fetch the actual image

---

## Location & Navigation Tools

### 12. `get_google_maps_link`
**Purpose**: Generate Google Maps links for places
**Unique Feature**: Direct Google Maps integration
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `link_type` (str, optional): "directions", "place", or "search"

**Returns**: Google Maps URL for:
- Viewing place on Google Maps
- Getting directions
- Sharing location

**Example Use Cases**:
- "Get directions link for this restaurant"
- "Share this place on Google Maps"

---

### 13. `find_places_along_route`
**Purpose**: Find places along a route between two points
**API**: Google Places API + Directions API
**Parameters**:
- `origin` (str): Starting location
- `destination` (str): Ending location
- `category` (str, optional): Type of place to find
- `radius` (int, optional): Search radius from route (meters)

**Returns**: Places near the route with distance from route

**Example Use Cases**:
- "Find restaurants along my route"
- "Show me gas stations on the way"

---

## Business Information Tools

### 14. `check_business_status`
**Purpose**: Check if a business is operational, closed, or moved
**Unique Feature**: Business status tracking
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Business status (OPERATIONAL, CLOSED_PERMANENTLY, CLOSED_TEMPORARILY)
- If moved: new location information (`movedPlace`, `movedPlaceId`)
- Last updated timestamp

**Example Use Cases**:
- "Is this business still open?"
- "Did this restaurant move?"

---

### 15. `get_business_attributes`
**Purpose**: Get detailed business attributes and amenities
**Unique Feature**: Extensive attribute database
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Payment options (cash, credit cards, etc.)
- Dining options (dine-in, takeout, delivery)
- Amenities (WiFi, parking, outdoor seating, etc.)
- Atmosphere (casual, formal, etc.)
- Crowd (family-friendly, LGBTQ+ friendly, etc.)

**Example Use Cases**:
- "What payment methods are accepted?"
- "Is this place family-friendly?"

---

## Advanced Search Tools

### 16. `search_by_place_type`
**Purpose**: Search using Google's extensive place type taxonomy
**Unique Feature**: 100+ place types
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `location` (str): City name or address
- `type` (str): Place type (restaurant, cafe, museum, park, etc.)
- `keyword` (str, optional): Additional search term
- `radius` (int, optional): Search radius (meters)

**Place Types Include**:
- `restaurant`, `cafe`, `bar`, `bakery`
- `museum`, `art_gallery`, `zoo`, `aquarium`
- `park`, `tourist_attraction`, `amusement_park`
- `shopping_mall`, `store`, `supermarket`
- And 90+ more types

**Example Use Cases**:
- "Find all art galleries in the city"
- "Search for bakeries near me"

---

### 17. `search_with_price_level`
**Purpose**: Search filtered by price level with Google's price data
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `location` (str): City name or address
- `min_price` (int, optional): Minimum price level (0-4)
- `max_price` (int, optional): Maximum price level (0-4)
- `type` (str, optional): Place type

**Returns**: Places with price level indicators ($ to $$$$)

---

### 18. `search_by_rating_range`
**Purpose**: Search places within a rating range
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `location` (str): City name or address
- `min_rating` (float): Minimum rating (0.0-5.0)
- `max_rating` (float, optional): Maximum rating (0.0-5.0)
- `type` (str, optional): Place type

**Returns**: Places filtered by rating

---

## Integration & Utility Tools

### 19. `get_place_id_from_coordinates`
**Purpose**: Convert coordinates to Google Place ID
**API**: Google Places API Place Details (reverse geocoding)
**Parameters**:
- `latitude` (float): Latitude
- `longitude` (float): Longitude

**Returns**: Google Place ID for the location

**Use Case**: When you have coordinates and need Place ID for other API calls

---

### 20. `batch_get_place_details`
**Purpose**: Get details for multiple places efficiently
**API**: Google Places API Place Details (multiple calls)
**Parameters**:
- `place_ids` (list): List of Google Place IDs (up to 20)

**Returns**: Details for all requested places

**Note**: Implement as wrapper that makes multiple API calls efficiently

---

### 21. `get_place_website_and_contact`
**Purpose**: Get website, phone, and contact information
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Website URL
- Phone number (international format)
- Formatted phone number
- Business status

**Example Use Cases**:
- "What's the phone number for this restaurant?"
- "Get the website for this place"

---

## Comparison & Analysis Tools

### 22. `compare_places_detailed`
**Purpose**: Compare multiple places with detailed metrics
**API**: Google Places API Place Details (multiple)
**Parameters**:
- `place_ids` (list): List of Google Place IDs (2-5 places)
- `compare_fields` (list, optional): Fields to compare (rating, price, reviews, etc.)

**Returns**: Side-by-side comparison with:
- Ratings and review counts
- Price levels
- Opening hours
- Distance from reference point
- Key attributes

---

### 23. `find_places_similar_to`
**Purpose**: Find places similar to a given place using Google's data
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `place_id` (str): Reference Google Place ID
- `radius` (int, optional): Search radius (meters, default: 2000)
- `limit` (int, optional): Number of results (default: 10)

**Implementation**: 
1. Get place details for reference place
2. Extract place type, price level, rating range
3. Search nearby with similar criteria

**Returns**: Places with similar characteristics

---

## Unique Google-Specific Features

### 24. `get_place_editorial_summary`
**Purpose**: Get Google's editorial summary/description of a place
**Unique Feature**: Google-generated place descriptions
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**: Editorial summary text (if available)

**Example Use Cases**:
- "Tell me about this place"
- "Get a description of this restaurant"

---

### 25. `check_place_verification_status`
**Purpose**: Check if a place is verified by Google
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**: Verification status and business ownership info

---

## Implementation Notes

### Field Masks (Important!)
Google Places API (New) requires **field masks** - you must specify exactly which fields you want:

```python
fields = [
    "displayName",
    "formattedAddress",
    "rating",
    "userRatingCount",
    "currentOpeningHours",
    "photos",
    "reviews",
    "accessibilityOptions",
    "priceLevel"
]
```

**Benefits**:
- Lower costs (only pay for fields you use)
- Faster responses
- Better control over data

### Session Tokens for Autocomplete
- Generate UUID v4 for each autocomplete session
- Use same token for autocomplete requests and place selection
- Groups billing for better pricing

### Rate Limits
- Varies by API method and pricing tier
- Check current limits in Google Cloud Console
- Implement exponential backoff for rate limit errors

### Cost Optimization
- Use field masks to request only needed fields
- Cache place details (Place IDs are stable)
- Use session tokens for autocomplete
- Batch requests when possible

---

## Google Places API Capabilities

| Feature | Google Places API (New) |
|---------|-------------------------|
| **Reviews** | Structured reviews with ratings |
| **Photos** | Millions with attribution |
| **Autocomplete** | Advanced with session tokens |
| **Accessibility** | Detailed wheelchair data |
| **Special Hours** | Holiday/special days |
| **Secondary Hours** | Multiple schedules |
| **Price Level** | Detailed ($ to $$$$) |
| **Business Status** | Moved/closed tracking |
| **Place Types** | 100+ types |

---

## Recommended Tools to Implement First

### High Priority (Unique Value):
1. ✅ `autocomplete_places` - Better UX than basic search
2. ✅ `get_detailed_reviews` - More structured than tips
3. ✅ `get_special_opening_hours` - Holiday hours
4. ✅ `find_wheelchair_accessible_places` - Detailed accessibility
5. ✅ `get_google_maps_link` - Direct Maps integration

### Medium Priority (Useful Features):
6. ✅ `get_place_photos_with_attribution` - High-quality photos
7. ✅ `check_business_status` - Moved/closed tracking
8. ✅ `get_business_attributes` - Detailed amenities
9. ✅ `validate_address` - Address validation
10. ✅ `get_secondary_opening_hours` - Multiple schedules

### Lower Priority (Nice to Have):
11. ✅ `get_review_summary` - Aggregated stats
12. ✅ `compare_places_detailed` - Enhanced comparison
13. ✅ `find_places_along_route` - Route-based search
14. ✅ `get_place_editorial_summary` - Google descriptions

---

## Code Example Structure

```python
@mcp.tool()
async def autocomplete_places(
    input_text: str,
    location: str | None = None,
    types: list[str] | None = None,
    session_token: str | None = None
) -> str:
    """Provide intelligent place autocomplete as user types.
    
    Args:
        input_text: User's partial input text
        location: Bias results toward this location
        types: Filter by place types (restaurant, museum, etc.)
        session_token: Session token for billing grouping (UUID v4)
    """
    url = "https://places.googleapis.com/v1/places:autocomplete"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "suggestions.placePrediction.placeId,suggestions.placePrediction.text"
    }
    
    data = {
        "input": input_text,
    }
    
    if location:
        data["locationBias"] = {"location": {"lat": lat, "lng": lng}}
    
    if types:
        data["includedPrimaryTypes"] = types
    
    if session_token:
        data["sessionToken"] = session_token
    
    # Make request and format results
    # ...
```

---

## Resources

- **Google Places API Documentation**: https://developers.google.com/maps/documentation/places/web-service
- **Place Data Fields**: https://developers.google.com/maps/documentation/places/web-service/data-fields
- **Autocomplete (New)**: https://developers.google.com/maps/documentation/places/web-service/place-autocomplete
- **Place Photos (New)**: https://developers.google.com/maps/documentation/places/web-service/place-photos
- **Session Tokens**: https://developers.google.com/maps/documentation/places/web-service/session-tokens
- **Field Masks Guide**: https://developers.google.com/maps/documentation/places/web-service/choose-fields

---

## Summary

Google Places API (New) offers **25+ unique tools** that leverage:
- ✅ Advanced autocomplete with session pricing
- ✅ Structured reviews and ratings
- ✅ Detailed accessibility information
- ✅ Special and secondary opening hours
- ✅ Business status tracking
- ✅ Extensive place type taxonomy
- ✅ High-quality photos with attribution
- ✅ Google Maps integration
- ✅ Address validation
- ✅ Route-based search

Google Places API provides comprehensive data and unique features that enhance the local discovery experience when combined with Ticketmaster (events) and OpenRouter (summarization).
