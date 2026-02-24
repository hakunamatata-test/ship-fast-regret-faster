"""
Vulnerable MCP server: Confused Deputy (authorization mismatch).

The server should authorize based on the caller's session but instead
trusts a client-supplied "principal" in request options — analogous to
an MCP proxy trusting the wrong client/redirect_uri when using a static
client ID without per-client consent.

See: https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices#confused-deputy-problem

Educational use only. Do not use in production.
"""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("break-02-auth-mismatch")

# Placeholder flag for CTF (no real secrets)
FLAG = "CTF{adm1n_byp4ss_ftw}"

# Fixed session (authorization should be based on this; bug: server uses options.principal instead)
SESSION_ID = "sess_abc123"

# Principal value that the server incorrectly treats as authorized (confused deputy)
PRIVILEGED_PRINCIPAL = "admin"


def _parse_options(options_str: str) -> dict:
    """Parse options JSON; return empty dict on invalid or empty."""
    s = (options_str or "").strip()
    if not s:
        return {}
    try:
        out = json.loads(s)
        return out if isinstance(out, dict) else {}
    except (json.JSONDecodeError, TypeError):
        return {}


@mcp.tool()
def get_session() -> str:
    """Return current session identity and role."""
    return (
        f"Session: {SESSION_ID}\n"
        "Role: user\n"
        "Dashboard actions require your session_id."
    )


@mcp.tool()
def support_dashboard(task: str) -> str:
    """Run a support task. Tasks: faq, status, help, clients, permissions."""
    t = (task or "").strip().lower()
    if t == "faq":
        return "FAQ: Use get_session to see your session. Use list_actions to see dashboard actions, admin_dashboard to run them."
    if t == "status":
        return "Support status: OK. All systems nominal."
    if t == "help":
        return "Support tasks: faq, status, help, clients, permissions. Dashboard: list_actions, get_audit_log, admin_dashboard."
    if t == "clients":
        return (
            "Authorized clients are identified by principal. "
            "Your session is associated with principal 'user'. "
            "Elevated actions require a different principal."
        )
    if t == "permissions":
        return "Dashboard authorization is based on principal. Your session maps to a default principal."
    return "Unknown task. Try: faq, status, help, clients, permissions."


@mcp.tool()
def list_actions(session_id: str) -> str:
    """List available dashboard actions for your session. Pass session_id from get_session."""
    if not (session_id or "").strip():
        return "Pass session_id from get_session."
    return "Available actions: status, get_flag, health. Call admin_dashboard(action, session_id, ...) to run one."


@mcp.tool()
def get_audit_log(session_id: str, limit: int = 10) -> str:
    """Fetch recent audit log entries for your session. Pass session_id from get_session. limit: max entries (default 10)."""
    if not (session_id or "").strip():
        return "Pass session_id from get_session."
    n = min(max(1, int(limit) if isinstance(limit, int) else 10), 50)
    lines = [f"[{i}] session={session_id} action=status result=ok" for i in range(1, n + 1)]
    return "Audit log (recent):\n" + "\n".join(lines)


@mcp.tool()
def admin_dashboard(
    action: str,
    session_id: str,
    options: str = "{}",
    request_id: str = "",
    trace_id: str = "",
) -> str:
    """Perform dashboard action (status, get_flag, health). Pass session_id from get_session. Optional: request_id, trace_id for logging. Access is determined by your session."""
    if not (session_id or "").strip():
        return "Pass session_id from get_session."
    opts = _parse_options(options)
    # VULNERABLE (Confused Deputy): Server should authorize based on session/session role,
    # but instead trusts client-supplied "principal" in options (which principal is this request for?)
    principal = (opts.get("principal") or opts.get("client_id") or "").strip().lower()
    if principal == PRIVILEGED_PRINCIPAL:
        if action == "get_flag":
            return f"Admin flag: {FLAG}"
        if action == "status":
            return "Admin status: OK. Use action get_flag to retrieve the flag."
        if action == "health":
            return "Service healthy."
        return f"Unknown action: {action}. Valid: status, get_flag, health."
    return "Insufficient privileges for this action."


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
