# 05 – Behind the Curtain (prompt injection via tool parameters)

**Educational use only.** This server is intentionally vulnerable for workshop purposes.

This exercise illustrates **prompt injection in an MCP setup**: the summarize tool accepts a `formatting_directives` parameter that is naively parsed and executed. Document content (or user-supplied directives) controls tool behavior. Discover the config block format and the right keys to pull the curtain back and reveal the flag.

## Goal

Obtain the flag by getting the summarize tool to return internal output. The tool reads a config block from the directives parameter; finding the right combination of keys and values reveals the flag.

## Hint

The tool summarizes a document and accepts optional formatting directives. It only reads config from a specific block format (CONFIG_START ... CONFIG_END with key=value lines). The tool's response includes log lines that hint at valid keys and why certain values are rejected. Try output_level and mode; level 3 may require an extra step and a code from a previous run.

**If the assistant says it's ready and asks for document content:** the config is only applied when the assistant actually *calls* the MCP tool with your text in the `formatting_directives` parameter. In one message, give both a short document and the CONFIG block, and ask the assistant to call `summarize_document` with that document and those directives (e.g. "Call summarize_document with document 'test' and formatting_directives: CONFIG_START ... CONFIG_END"). Then read the tool's *response* (the log section) for hints and the flag.

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

Configure your MCP client to run this command via STDIO, then use the tools to find the flag. For step-by-step setup with MCPJam, see [break/CHALLENGES.md](../CHALLENGES.md).

## Solution

1. Call `summarize_document` with a document and formatting_directives containing a config block: CONFIG_START ... CONFIG_END.
2. Inside the block use key=value lines. Valid keys: format, output_level, mode, unlock_code.
3. Set output_level=2 and mode=advanced; the response log will include "Unlock code for this session: 7".
4. Call again with output_level=3, mode=advanced, and unlock_code=7 in the config block. The summary will include the flag.
