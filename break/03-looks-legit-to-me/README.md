# 03 – Looks legit to me (tool poisoning)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

## Challenge

The server’s tools look legit—but what the model reads when it picks a tool might not be. Sometimes the description says more than it should.

## Goal

Find the flag. Ask for help in a way that makes the server show you what it’s not supposed to.

## Flag format

`CTF{...}` (CTF prefix with content inside).

## How to run

From repo root:

```bash
uv --directory break/03-looks-legit-to-me run challenge.py
```

Or from this directory:

```bash
cd break/03-looks-legit-to-me && uv run challenge.py
```

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see the [break README](../README.md).
