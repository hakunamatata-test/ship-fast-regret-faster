# Google Places API (New) — Setup

This guide walks you through creating a Google Cloud project, enabling the Places API (New), and creating an API key for the Local Discovery MCP server.

---

## 1. Create a Google Cloud project

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one):
   - **Create project**: [console.cloud.google.com/projectcreate](https://console.cloud.google.com/projectcreate)
   - Enter a **Project name** and **Project ID**.
3. **Billing** must be enabled on the project to use the Places API (Google offers free monthly usage; see [pricing](https://developers.google.com/maps/billing-and-pricing)).

---

## 2. Enable the Places API (New)

1. Open the [API Library](https://console.cloud.google.com/apis/library).
2. Search for **Places API (New)** (or go to [places.googleapis.com](https://console.cloud.google.com/apis/library/places.googleapis.com)).
3. Select **Places API (New)** and click **Enable**.

**Note:** This is the *new* Places API (`places.googleapis.com`), not the legacy “Places API”. The server uses the new endpoints (e.g. `places:searchText`, `GET /places/{place_id}`).

---

## 3. Create an API key

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials).
2. Click **Create credentials** → **API key**.
3. Copy the generated key. You will use it as `GOOGLE_API_KEY` in the build `.env` file.

---

## 4. (Recommended) Restrict the API key

To reduce risk of misuse:

1. On the Credentials page, click the API key you created.
2. Under **API restrictions**, choose **Restrict key** and select **Places API (New)** (and any other APIs you use, e.g. Directions if you add travel-time tools later).
3. Under **Application restrictions**, you can restrict by IP or HTTP referrer if your usage is from a known environment.
4. Save.

---

## 5. Add the key to the build server

In the `build/` directory, create or edit `.env`:

```env
GOOGLE_API_KEY=your_api_key_here
```

Make sure to add .env to .gitignore

---

## 6. API Debugging

Try running this curl request to ensure your API key is set up correctly

```
curl -X GET -H 'Content-Type: application/json' \
-H "X-Goog-Api-Key: <api-key>" \
-H "X-Goog-FieldMask: id,displayName,formattedAddress,dineIn" \
https://places.googleapis.com/v1/places/ChIJt4S8_XuBhYARzDbXXYAiuno
```

You should get the following response:

```
{
  "id": "ChIJt4S8_XuBhYARzDbXXYAiuno",
  "formattedAddress": "138 Cyril Magnin St, San Francisco, CA 94102, USA",
  "displayName": {
    "text": "Magnin Street Cafe & Bistro",
    "languageCode": "en"
  },
  "dineIn": true
}
```

---

## References

- [Places API (New) — Cloud setup](https://developers.google.com/maps/documentation/places/web-service/cloud-setup)
- [Get an API key for Places API](https://developers.google.com/maps/documentation/places/web-service/get-api-key)
- [Places API (New) — Overview](https://developers.google.com/maps/documentation/places/web-service/op-overview)
- [Usage and billing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)
