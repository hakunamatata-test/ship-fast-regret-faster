# MCP Security Challenges

Standalone MCP challenge servers you can run locally and connect to with **MCPJam**. Each challenge has a flag in the format `CTF{...}`. Use the checklist at the bottom to track which ones you've completed.

---

## Prerequisites

- **Node.js** and **npm** (for MCPJam)
- **uv** (Python package manager) — [install uv](https://docs.astral.sh/uv/getting-started/installation/)
- This repo cloned locally

---

## 1. Run MCPJam locally

1. Install and run MCPJam with npm:

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. MCPJam will open in your browser (or give you a URL). Use it to add and connect to the challenge servers below.

---

## 2. Add and run a challenge server

For each challenge you want to play:

1. **Add your server** in MCPJam:
   - Click **Add Server** (or equivalent).
   - **Server name:** e.g. `Challenge 1` (use a different name per challenge if you run several).
   - **Connection type:** **STDIO**.
   - **Command:** (replace `<path>` with the absolute path to your repo, e.g. `/Users/you/ship-fast-regret-faster`):

   | Challenge | Command |
   |-----------|--------|
   | Challenge 1 | `uv run --directory <path>/break 01-oops-that-was-private/challenge.py` |
   | Challenge 2 | `uv run --directory <path>/break 02-deputy-in-the-middle/challenge.py` |
   | Challenge 3 | `uv run --directory <path>/break 03-looks-legit-to-me/challenge.py` |
   | Challenge 4 — Name Your Poison | `uv run --directory <path>/break 04-name-your-poison/challenge.py` |
   | Challenge 5 — Behind the Curtain | `uv run --directory <path>/break 05-behind-the-curtain/challenge.py` |
   | Challenge 6 — Forward Thinking | `uv run --directory <path>/break 06-forward-thinking/challenge.py` |

   Example on macOS/Linux (Challenge 1):

   ```text
   uv run --directory /Users/you/ship-fast-regret-faster/break 01-oops-that-was-private/challenge.py
   ```

2. Click **Add server**.

3. **Connect** to the server (e.g. click **Connect** or open the server you added).

4. Open **Chat**, then **Show me connected tools** (or the equivalent that lists tools).

5. Use the tools in chat to find the flag. Each challenge's flag is in the form **`CTF{...}`**.

---

## 3. Challenge checklist

Track your progress by checking off the challenges you've completed:

- [ ] **Challenge 1 — Secret exposure (flight booking)**  
  `01-oops-that-was-private` — Discover an internal coupon from a flight booking server.

- [ ] **Challenge 2 — Confused Deputy (authorization mismatch)**  
  `02-deputy-in-the-middle` — Explore how the server decides who can do what, then use that to retrieve the flag.

- [ ] **Challenge 3 — Tool poisoning (metadata)**  
  `03-looks-legit-to-me` — Get the server to reveal the internal report by triggering hidden instructions in a tool's description.

- [ ] **Challenge 4 — Name Your Poison (tool naming / impersonation)**  
  `04-name-your-poison` — Attacker adds a tool with a similar name to the legit one (same description); selection by name/order may pick the malicious tool, which leaks the flag in its response.

- [ ] **Challenge 5 — Behind the Curtain (prompt injection via tool parameters)**  
  `05-behind-the-curtain` — The summarize tool parses config from your directives. Find the config block format and the right keys (mode, output_level, unlock_code) to reveal the flag.

- [ ] **Challenge 6 — Forward Thinking (tool chaining / exfiltration)**  
  `06-forward-thinking` — Get a full report (to obtain the export code), then use send_report with that code to deliver the report and receive the flag.

---
