# MCP Attack Patterns — Workshop

Workshop materials for **MCP-related attack patterns**. Attack demos run as **MCPJam** STDIO challenges (see [CHALLENGES.md](CHALLENGES.md)); the **web app** in `app/` is a landing page that lists the challenges and how to run them.

**These challenges are intentionally vulnerable for educational purposes.** Do not deploy in production or expose to untrusted users.

---

## What This Repo Is

- **MCPJam challenges** (folders `01-*` … `06-*`): STDIO MCP servers; run with `uv run --directory <path>/break <challenge>/challenge.py` and connect via MCPJam. Each has a `CTF{...}` flag.
- **Web app** (`app/`): FastAPI + Jinja2 landing page; no in-browser scenarios. Run with Docker or uvicorn to show the challenge list and setup instructions.

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

## What Each Challenge Covers

See [CHALLENGES.md](CHALLENGES.md) for run commands and hints. Summary:

| Challenge | Theme |
|-----------|--------|
| **01** — Oops, That Was Private | Secret exposure (flight booking; internal ref leaked). |
| **02** — Deputy in the Middle | Man-in-the-middle / proxy. |
| **03** — Looks Legit to Me | Tool poisoning via metadata/description. |
| **04** — Name Your Poison | Tool naming / impersonation (similar names; wrong tool can be selected). |
| **05** — Behind the Curtain | Prompt injection via tool parameters (CONFIG block in directives). |
| **06** — Forward Thinking | Tool chaining / exfiltration (full report + export code → send_report). |

---

## STRIDE Mapping

| Challenge / theme        | STRIDE category        |
|--------------------------|-------------------------|
| Naming / Impersonation   | Spoofing                |
| Prompt injection (params)| Tampering               |
| Tool chaining            | Information disclosure  |
| Secret exposure          | Information disclosure  |
| Tool poisoning (metadata)| Spoofing / Tampering    |

---

## Repo Structure

```
break/
  app/
    main.py              # FastAPI landing page (lists challenges)
    templates/
      index.html
    static/
  01-oops-that-was-private/   … 06-forward-thinking/   # MCPJam STDIO challenges
  CHALLENGES.md           # Setup and checklist
  requirements.txt
  Dockerfile
  docker-compose.yml
  README.md
```

---

## Intentionally Vulnerable

This application is **intentionally vulnerable** for educational purposes. Use only in controlled workshop or lab environments. Do not use in production or expose to untrusted networks or users.
