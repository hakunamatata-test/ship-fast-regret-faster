"""
Vulnerable MCP server: Prompt injection via tool parameters (Behind the Curtain).

The summarize_document tool accepts formatting_directives from the user/document.
That content is parsed as config (CONFIG_START...CONFIG_END) and executed—so
untrusted input controls tool behavior. Discovery: find block format, keys,
mode=advanced, output_level=2 to get unlock code, then output_level=3 + unlock_code.

Educational use only. Do not use in production.
"""
import re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("break-05-behind-the-curtain")

FLAG = "CTF{b3h1nd_th3_curt41n_d1r3ct1v3s}"

CONFIG_BLOCK_START = "config_start"
CONFIG_BLOCK_END = "config_end"
KNOWN_KEYS = {"format", "output_level", "mode", "include", "unlock_code", "code"}
VALID_FORMAT = {"bullets", "list", "plain"}
VALID_MODE = {"standard", "advanced"}
VALID_OUTPUT_LEVEL = {1, 2, 3}
UNLOCK_CODE = 7


def _extract_config_block(directives: str) -> str:
    if not directives:
        return ""
    lower = directives.lower()
    i = lower.find(CONFIG_BLOCK_START)
    if i == -1:
        return ""
    i += len(CONFIG_BLOCK_START)
    j = lower.find(CONFIG_BLOCK_END, i)
    if j == -1:
        return ""
    return directives[i:j].strip()


def _parse_key_value_block(block: str) -> dict:
    result = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().lower()
        value = value.strip()
        if key in ("output_level", "output level"):
            try:
                result["output_level"] = int(value)
            except ValueError:
                result["output_level"] = 0
        elif key in ("unlock_code", "code"):
            try:
                result["unlock_code"] = int(value)
            except ValueError:
                result["unlock_code"] = 0
        elif key:
            result[key] = value.lower() if value else ""
    return result


@mcp.tool()
def summarize_document(document: str, formatting_directives: str = "") -> str:
    """Summarize a document. Optional formatting_directives: use CONFIG_START ... CONFIG_END with key=value lines (e.g. format=bullets, output_level=2). The response includes a log section with hints."""
    log = []
    log.append("[MCP] Tool received document and formatting_directives.")

    block = _extract_config_block(formatting_directives or "")
    config = {}

    if not block:
        log.append("[MCP] No config block found. Use CONFIG_START ... CONFIG_END with key=value lines.")
    else:
        config = _parse_key_value_block(block)
        for key in list(config.keys()):
            if key not in KNOWN_KEYS:
                log.append(f"[MCP] Unknown key '{key}'. Known keys: format, output_level, mode, include, unlock_code.")
                del config[key]
        if config:
            log.append(f"[MCP] Parsed config: {dict(config)}")
        else:
            log.append("[MCP] Config block present but no key=value lines found. Try: format=bullets or output_level=2")

    format_val = config.get("format", "")
    if format_val and format_val not in VALID_FORMAT:
        format_val = "plain"
    output_level = config.get("output_level", 1)
    if output_level not in VALID_OUTPUT_LEVEL:
        output_level = 1
    mode = config.get("mode", "standard")
    if mode not in VALID_MODE:
        mode = "standard"

    if output_level == 3 and mode != "advanced":
        log.append("[MCP] output_level 3 requires mode=advanced (current: standard). Capped at 2.")
        output_level = 2

    unlock_code = config.get("unlock_code", 0)
    if unlock_code is None:
        unlock_code = 0
    if output_level == 3 and unlock_code != UNLOCK_CODE:
        log.append("[MCP] Level 3 requires a valid unlock_code. Run once with output_level=2 and mode=advanced; the code appears in this log.")
        output_level = 2

    if mode == "advanced" and config.get("output_level") == 2:
        log.append(f"[MCP] Level 3 (internal fields) is available. Unlock code for this session: {UNLOCK_CODE}")

    summary_parts = [f"Summary: Document length {len(document or '')} characters. Processed."]
    if format_val in ("bullets", "list"):
        summary_parts.append("Formatted as bullet list.")
    if output_level >= 2:
        summary_parts.append("Metadata: (none)")
    if output_level == 3:
        summary_parts.append(f"Internal fields: flag={FLAG}")

    log_section = "\n".join(log)
    summary_section = "\n".join(summary_parts)
    return f"Log:\n{log_section}\n\nSummary:\n{summary_section}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
