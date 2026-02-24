# 01 – Secret exposure (flight booking)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

## Goal

Obtain the hidden flag by using the flight booking tools: discover the internal ref from flight or airport data, then call get_booking_status with that ref.

## Hint

One tool returns an exclusive promo when given a booking reference; that reference appears in other tools' responses. Use get_flight_details or get_airport_info to explore.

## Flag format

`CTF{...}` (CTF prefix with content inside).

## How to run

From repo root:

```bash
uv --directory break/01-oops-that-was-private run challenge.py
```

Or from this directory:

```bash
cd break/01-oops-that-was-private && uv run challenge.py
```

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see [break/CHALLENGES.md](../CHALLENGES.md).

## Solution

Call `get_flight_details` with flight ID `FLT-101` (or `get_airport_info` with code `STAFF`) to get internal ref `7001`, then call `get_booking_status` with `7001` to receive the flag.
