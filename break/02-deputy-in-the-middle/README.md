# 02 – Confused Deputy (authorization mismatch)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

This exercise illustrates the [Confused Deputy problem](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices#confused-deputy-problem) in an MCP context: the server (the deputy) has privileged capability but decides *which principal* is authorized using client-supplied request context instead of the caller's session. In production MCP OAuth proxies, the same confusion appears when the proxy uses a static client ID and does not enforce per-client consent and `redirect_uri`, allowing an attacker's client to receive authorization codes intended for another.

## Goal

Obtain the flag by exploiting the confused deputy: the server performs privileged actions based on the wrong principal (client-supplied options instead of your session).

## Hint

The server should authorize based on your session. What other request data does it use to decide access? Explore the support dashboard (try different tasks) and notice which dashboard tools take optional parameters.

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

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see [break/CHALLENGES.md](../CHALLENGES.md).

## Solution

1. Call `get_session` to get your session_id (e.g. sess_abc123).
2. Call `support_dashboard` with task `clients` to learn that actions are gated by a "principal" and your session is principal `user`; elevated actions require a different principal.
3. Call `admin_dashboard` with `action="get_flag"`, your `session_id`, and `options` set to a JSON object that specifies a privileged principal (e.g. `{"principal": "admin"}` or `{"client_id": "admin"}`). The server trusts the principal in `options` instead of deriving it from the session (confused deputy), so it returns the flag.
