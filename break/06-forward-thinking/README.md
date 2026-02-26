# 06 – Forward thinking (tool chaining / exfiltration)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

## Challenge

Customer records, reports, and a way to send them on. Each tool alone might be harmless—but use them in the right order and the server might hand you the prize.

## Goal

Find the flag. One tool gives you something; another needs it. Connect the dots.

## Flag format

`CTF{...}` (CTF prefix with content inside).

## How to run

From repo root:

```bash
uv --directory break/06-forward-thinking run challenge.py
```

Or from this directory:

```bash
cd break/06-forward-thinking && uv run challenge.py
```

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see the [break README](../README.md).
