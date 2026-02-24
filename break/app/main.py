"""
Workshop demo app: four MCP-related attack patterns.

Run: uvicorn app.main:app --reload
Or:  docker compose up --build
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.scenarios import naming_attack, prompt_injection, secret_exposure, tool_chaining

# ---------------------------------------------------------------------------
# Paths and templating
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ---------------------------------------------------------------------------
# Scenario metadata for homepage
# ---------------------------------------------------------------------------
SCENARIOS = [
    {
        "id": 1,
        "title": "Scenario 1",
        "description": "Chat with the assistant. Try the time, search, weather, or math—then try sending a message.",
    },
    {
        "id": 2,
        "title": "Scenario 2",
        "description": "Summarize a document. Paste document text and request a summary.",
    },
    {
        "id": 3,
        "title": "Scenario 3",
        "description": "Investigate a customer (123 or 456). Try a full report; then see what the log allows.",
    },
    {
        "id": 4,
        "title": "Scenario 4",
        "description": "Book flights with the assistant. Search flights, check details, booking status, airport info, and promos.",
    },
]


def get_all_tools() -> list[dict]:
    """Aggregate tools from all scenarios for the /tools endpoint."""
    tools = []
    tools.extend(naming_attack.TOOLS)
    tools.extend(tool_chaining.TOOLS)
    tools.extend(secret_exposure.TOOLS)
    return tools


# ---------------------------------------------------------------------------
# App and routes
# ---------------------------------------------------------------------------
app = FastAPI(title="MCP Workshop Demo", docs_url=None, redoc_url=None)

# Static files (if any)
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "scenarios": SCENARIOS},
    )


@app.get("/scenario/{sid:int}", response_class=HTMLResponse)
async def scenario_page(request: Request, sid: int):
    if sid not in (1, 2, 3, 4):
        return HTMLResponse("<h1>Not found</h1>", status_code=404)
    scenario = next(s for s in SCENARIOS if s["id"] == sid)
    return templates.TemplateResponse(
        request=request,
        name="scenario.html",
        context={"request": request, "scenario": scenario},
    )


@app.post("/api/scenario/1")
async def run_scenario_1(body: dict):
    """Scenario 1: Naming / impersonation — multi-turn chat; tool selection by name."""
    user_input = body.get("input", "").strip()
    history = body.get("history")
    if not isinstance(history, list):
        history = []
    return naming_attack.run_naming_scenario(user_input, history=history)


@app.post("/api/scenario/2")
async def run_scenario_2(body: dict):
    """Scenario 2: Prompt injection — document directives as instructions."""
    document_text = body.get("document", "").strip()
    return prompt_injection.run_prompt_injection_scenario(document_text)


@app.post("/api/scenario/3")
async def run_scenario_3(body: dict):
    """Scenario 3: Tool chaining — exfiltration via composed tools."""
    user_input = body.get("input", "").strip()
    return tool_chaining.run_tool_chaining_scenario(user_input)


@app.post("/api/scenario/4")
async def run_scenario_4(body: dict):
    """Scenario 4: Secret exposure — flight booking; coupon leaked via internal ref."""
    user_input = body.get("input", "").strip()
    return secret_exposure.run_secret_exposure_scenario(user_input)


# Not linked from UI; curious attendees can discover it manually.
@app.get("/tools")
async def list_tools():
    """Returns registered tools in JSON. Exists for discovery, not advertised in UI."""
    return {"tools": get_all_tools()}


@app.get("/attacker-log")
async def attacker_log():
    """Stores and displays webhook payloads sent in scenario 3 (exfiltration demo)."""
    return {"payloads": tool_chaining.get_attacker_log()}
