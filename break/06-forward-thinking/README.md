# 06 – Forward Thinking (tool chaining / data exfiltration)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

This exercise illustrates **tool chaining risk**: individually safe tools (get customer record, get full report, send report) become dangerous when the model chains them on user request. Obtain an export code from a full report, then use it to "forward" a report and retrieve the flag.

## Goal

Obtain the flag by chaining tools: first get a full report (which reveals an export code), then use that code when asking to forward or send the report. The send tool returns the flag when given a valid export code.

## Hint

Explore customer records and report options. One tool returns a "full report" that includes an export code in its response. Another tool can forward or send a report to a URL but requires that export code. Chain the tools in the right order.

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

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see [break/CHALLENGES.md](../CHALLENGES.md).

## Solution

1. Call `get_customer_record` with customer_id 123 or 456 to see that customers exist.
2. Call `get_full_report` with customer_id 123 (or 456). The response includes "Export code for forwarding: 7".
3. Call `send_report` with url (any URL, e.g. https://example.com), export_code=7, and customer_id=123. The tool returns success and the flag (e.g. "Report delivered. Flag: CTF{...}").
