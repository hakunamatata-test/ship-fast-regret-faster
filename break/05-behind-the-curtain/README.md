# 05 – Behind the curtain (prompt injection via tool parameters)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

## Challenge

A summarizer that takes your document—and maybe more. What you put in can steer what the tool does. Pull the right strings and something hidden might show up.

## Goal

Find the flag. Get the summarizer to show you what it keeps behind the curtain.

## Flag format

`CTF{...}` (CTF prefix with content inside).

## How to run

From repo root:

```bash
uv --directory break/05-behind-the-curtain run challenge.py
```

Or from this directory:

```bash
cd break/05-behind-the-curtain && uv run challenge.py
```

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see the [break README](../README.md).
