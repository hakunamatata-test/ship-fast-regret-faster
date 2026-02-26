# 02 – Deputy in the middle (confused deputy)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

## Challenge

Support dashboard, admin dashboard — the server is supposed to decide *who* can do what based on your session. But who does it really trust when you make a request?

## Goal

Find the flag. Get the server to give you something only a higher-privileged caller should see.

## Flag format

`CTF{...}` (CTF prefix with content inside).

## How to run

From repo root:

```bash
uv --directory break/02-deputy-in-the-middle run challenge.py
```

Or from this directory:

```bash
cd break/02-deputy-in-the-middle && uv run challenge.py
```

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see the [break README](../README.md).
