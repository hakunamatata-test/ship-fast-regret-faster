# 04 – Name your poison (tool naming / impersonation)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

## Challenge

Ask to send a message and the server will pick a tool to do it. Two tools could do the job—and they’re not the same under the hood.

## Goal

Find the flag. Get the server to “send” something and see what you get back.

## Flag format

`CTF{...}` (CTF prefix with content inside).

## How to run

From repo root:

```bash
uv --directory break/04-name-your-poison run challenge.py
```

Or from this directory:

```bash
cd break/04-name-your-poison && uv run challenge.py
```

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see the [break README](../README.md).
