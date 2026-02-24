# MCP Attack Patterns — Workshop Demo

A simple interactive demo app used in workshops to demonstrate **four MCP-related attack patterns**. This is **not** a CTF: there are no flags, scoring, or authentication. Attendees explore each scenario briefly before speakers walk through the vulnerability and mitigations.

**This application is intentionally vulnerable for educational purposes.** Do not deploy in production or expose to untrusted users.

---

## What This Repo Is

- A single **FastAPI** app with **Jinja2** templates.
- No external APIs; no real LLM calls. Agent behavior is simulated deterministically in Python.
- Four scenarios, each illustrating a different structural design flaw that leads to abuse.

---

## How to Run

**Option 1 — Docker (recommended)**

```bash
docker compose up --build
```

**Option 2 — Local**

```bash
cd break
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open **http://localhost:8080**. The app runs on port 8080.

---

## What Each Scenario Demonstrates

### Scenario 1: Naming / Impersonation

- **Goal:** Unsafe tool selection based on **name matching** (e.g. first tool whose name contains `"email"`, or alphabetical order).
- **Setup:** Two tools are registered: `email_sender` and `email_sender_service`. Both look legitimate; neither is labeled malicious. They are registered so that the flawed selection logic picks `email_sender_service` first.
- **Exploration:** The assistant offers several actions (tell the time, search, weather, simple math, and send messages). Users can try these; only when they ask to **send an email or message** does the agent invoke tools—and that’s when the vulnerability triggers.
- **Behavior:** When the user sends a message, the “agent” selects a tool by a naive rule (e.g. first substring match). The chosen tool sends the message but **also returns internal metadata** (e.g. an API key) in the response or in the debug log. The message still succeeds; the vulnerability is subtle.
- **In the UI:** When a message is sent, the **Log** panel shows which tools were available (`email_sender_service`, `email_sender`) and which was selected—but not the selection rule. Attendees can think about why that tool was chosen instead of the other; the facilitator reveals the name-based selection logic during the walkthrough.
- **Teaching point:** Tool **names** are not trust boundaries. Substring or name-based selection is unsafe; tool identity must be explicit and validated (e.g. by stable ID), not inferred from names.

**Learning point for attendees:** You discovered that the assistant used a tool whose *name* sounded right (“email” in the name) but that tool was not the safe one—it leaked an internal API key. The lesson: **do not trust tool selection by name or substring.** In real systems, agents must resolve tools by a stable, explicit identity (e.g. ID or registry policy), not by matching user intent to tool names. Otherwise a malicious or misconfigured tool with a similar name can be chosen and expose secrets or change behavior.

### Scenario 2: Prompt Injection in an MCP Setup (Instruction vs Data)

- **Goal:** Show how **document content is passed as an MCP tool parameter** (e.g. “formatting directives”), so untrusted data is executed as tool input. This is prompt injection in an **MCP** context: the agent calls an MCP tool and naively uses the document as the tool’s directive parameter.
- **Setup:** The agent calls an MCP tool `summarize_document(document, formatting_directives)`. The document is user-controlled and is naively passed in full as `formatting_directives`. The tool obeys those directives; when they ask for internal/sensitive output, it returns the admin key.
- **Behavior:** The tool only reads config from a **config block** in the document (`CONFIG_START` … `CONFIG_END`) with `key=value` lines. The log gives feedback (e.g. “No config block found”, “Unknown key … Known keys: format, output_level, mode, include, unlock_code”, “output_level 3 requires mode=advanced”, “Level 3 requires a valid unlock_code”). Discovery path: (1) block format and valid keys, (2) `output_level=3` requires `mode=advanced`, (3) run with `output_level=2` and `mode=advanced` to see an **unlock code** in the log, (4) run again with `output_level=3`, `mode=advanced`, and `unlock_code=<code>` to trigger the leak. Extra step (unlock code) adds exploratory work before the admin key is revealed.
- **Teaching point:** In MCP, **tool parameters must not be sourced from untrusted input**. Strict separation: document content is data to summarize, not the directive string for the tool. Never pass user/document text as a parameter that controls tool behavior.

**Learning point for attendees:** You got the tool to return the “admin key” by discovering the config block format, valid keys, and the gated option (`mode=advanced` + `output_level=3`). That document content was passed as the MCP tool’s config and executed. The lesson: **in MCP, keep untrusted data out of tool parameters.** Document/user content should not become the directive or control input to a tool; otherwise prompt injection happens in the tool layer.

### Scenario 3: Tool Chaining / Data Exfiltration (more challenging)

- **Goal:** **Composition risk**: individually safe tools become dangerous when chained automatically. Harder than scenario 2: multi-step discovery and an export code gate.
- **Setup:** Tools include `get_customer_record(customer_id)` and `send_webhook(url, data)`. Default “investigate” returns a **summary only**; the log hints at “full report”. A **full report** run returns more detail and an **export code** in the log. **Forwarding** the report to a URL requires that export code (inline or in a `FORWARD_START` … `FORWARD_END` block).
- **Behavior:** Discovery path: (1) Investigate customer → summary only, log says “Request ‘full report’ for detailed output”. (2) “Full report for customer 123” → full details + “Export code for forwarding: 7” in log. (3) Forward to a URL without code → “Forwarding requires a valid export_code. Run a full report first.” (4) Forward with `export_code=7` (or in a FORWARD block with `url=` and `export_code=7`) → full record sent to webhook; view at **`/attacker-log`**.
- **Teaching point:** **Policy-gating** and **payload restrictions** are needed when composing tools. Individual tools can be “safe”; automatic chaining can enable exfiltration.

**Learning point for attendees:** You had to discover “full report”, get the export code from the log, then use that code when requesting forwarding—and the full record was sent to your URL. Each tool alone might be safe; **chaining them on user instruction** created exfiltration. The lesson: **tool composition must be policy-gated.** Restrict which tools can be combined, which URLs are allowed, and what data can be included in outbound payloads.


### Scenario 4: Secret Exposure (flight-booking theme)

- **Goal:** Obtain the hidden 70% discount coupon from the flight-booking assistant.
- **Setup:** The server offers search_flights, get_flight_details, get_booking_status, get_airport_info, and list_promos. The coupon is returned only by **get_booking_status** when called with a specific internal booking ref. That ref is **leaked** in responses from **get_flight_details** (for flight FLT-101: field `internal_ref`) and **get_airport_info** (for airport code STAFF: line "Internal lookup ref: 7001"). There is no access control on get_booking_status—anyone who obtains the ref can receive the coupon.
- **Behavior:** Discovery path: (1) Explore tools (search flights, flight details, airport info, list promos). (2) Notice the internal ref (e.g. 7001) in get_flight_details for FLT-101 or in get_airport_info for STAFF. (3) Call get_booking_status with that ref (e.g. "booking status 7001") to receive the coupon. The log notes when a privileged ref was used.
- **Teaching point:** Internal identifiers must not be exposed in user-facing tool responses. Tools that return sensitive data (e.g. promos, coupons) must validate the caller or ref and must not accept internal refs from untrusted input.

**Learning point for attendees:** You found an internal ref in flight or airport data and used it in get_booking_status to obtain the coupon. The lesson: **do not leak internal refs in API responses**, and **sensitive tools must enforce access control** instead of trusting refs that could be discovered elsewhere.

---

## STRIDE Mapping

| Scenario              | STRIDE Category       | How it maps |
|-----------------------|------------------------|-------------|
| **Naming / Impersonation** | **Spoofing**           | A tool is chosen by name similarity; a less-trusted or malicious tool can be selected and impersonate the intended one. |
| **Prompt Injection**       | **Tampering**          | Untrusted document content is treated as instructions and alters behavior (e.g. revealing secrets). |
| **Tool Chaining**          | **Information Disclosure** | Composing “get record” and “send webhook” allows sensitive data to be sent to an attacker-controlled endpoint. |
| **Secret Exposure**        | **Information Disclosure** | Internal ref leaked by flight/airport tools; get_booking_status returns coupon when given that ref (no access control). |

---

## Discovery Notes (for facilitators)

**How do attendees learn what tools exist and how chaining works?**

- **Tools:** The app does **not** link to or list tools in the UI. Curious attendees can discover **`/tools`** by exploring (e.g. trying `/tools` in the browser or common API paths). That endpoint returns the registered tools in JSON. So they can find out what tools exist without being told.
- **How chaining is triggered:** The Scenario 3 log guides discovery: “Request ‘full report’” and “Export code for forwarding” imply that a “forwarding” action exists. Attendees experiment with phrasing (e.g. “forward report to …” with the export code). There are no direct pointers in the UI. After they successfully trigger a forward, the log explicitly mentions **“Chaining: get_customer_record → send_webhook”** and **“Invoked send_webhook”**, so they see which tools were involved only after the fact.
- **How might someone find `/attacker-log`?** We don’t put the URL in the task placeholder or description. After a **successful** forward in Scenario 3, the log adds one line: **“Receiving endpoint: /attacker-log”**. So they discover where to view the exfiltrated payload only after they’ve already triggered the chaining. Alternatively they might guess common paths (e.g. `/log`, `/webhook-log`, `/attacker-log`) while exploring the app. Facilitators can mention that “if you get a forward to work, the log will tell you where the data went” without naming the path upfront.

- **Scenario 4 (secret exposure):** The internal ref (7001) appears in **get_flight_details** for flight FLT-101 (field `internal_ref`) and in **get_airport_info** for airport code **STAFF** ("Internal lookup ref: 7001"). search_flights also logs "ref 7001 used for FLT-101" when FLT-101 is in the results. Participants must use that ref in get_booking_status to receive the coupon.


---

## Repo Structure

```
break/
  app/
    main.py              # FastAPI app, routes, /tools, /attacker-log
    scenarios/
      naming_attack.py   # Scenario 1
      prompt_injection.py# Scenario 2
      tool_chaining.py   # Scenario 3
      secret_exposure.py # Scenario 4
    templates/
      index.html
      scenario.html
    static/
  requirements.txt
  Dockerfile
  docker-compose.yml
  README.md
```

---

## Intentionally Vulnerable

This application is **intentionally vulnerable** for educational purposes. Use only in controlled workshop or lab environments. Do not use in production or expose to untrusted networks or users.
