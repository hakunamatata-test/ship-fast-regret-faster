# BREAK the MCP

Welcome to Phase 2 of the workshop, where you will apply your understanding of common MCP vulnerabilities to break MCP servers in a fun, Capture the Flag style exercise!

This repo contains standalone MCP challenge servers you can run, connect to and play around with through [**MCPJam Inspector**](https://github.com/MCPJam/inspector). Each challenge has a flag in the format `CTF{...}`. Use the checklist at the bottom to track which ones you've completed. Stuck? Ask workshop facilitators for a hint!

Solutions will be shared towards the end of Break Phase.

---

## Prerequisites

- MCPJam account (for model access) — [sign up](https://login.mcpjam.com/sign-up)
- **Node.js** and **npm** (for MCPJam) - [install](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
  <br> Note (macOS): `npx` should be available by default with Node.js. If it is not available, run:
   ```bash
   brew update
   brew install node
   ```
- **uv** (Python package manager) — [install](https://docs.astral.sh/uv/getting-started/installation/)

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
   - Click **Add Server**.
   - **Server name:** e.g. `Challenge 1` (use a different name per challenge if you run several).
   - **Connection type:** `STDIO`.
   - **Command:** (replace `<path>` with the absolute path to your repo, e.g. `/Users/you/ship-fast-regret-faster`): <br>

   | Challenge | Command |
   |-----------|--------|
   | 01 Oops that was private | `uv --directory <path>/break/01-oops-that-was-private run challenge.py` |
   | 02 Deputy in the middle | `uv --directory <path>/break/02-deputy-in-the-middle run challenge.py` |
   | 03 Looks legit to me | `uv --directory <path>/break/03-looks-legit-to-me run challenge.py` |
   | 04 Name your poison | `uv --directory <path>/break/04-name-your-poison run challenge.py` |
   | 05 Behind the curtain | `uv --directory <path>/break/05-behind-the-curtain run challenge.py` |
   | 06 Forward thinking | `uv --directory <path>/break/06-forward-thinking run challenge.py` |

2. Click **Add server**.

3. **Connect** to the server.

4. Open **Chat**, then **Show me connected tools**.

5. Use the tools in chat to find the flag. Each challenge's flag is in the form **`CTF{...}`**.

---

## 3. Challenge checklist

Track your progress by checking off the challenges you've completed:

- [ ] **Challenge 1 — Oops that was private**  
  `01-oops-that-was-private` — Discover an internal coupon from a flight booking server.

- [ ] **Challenge 2 — Deputy in the middle**  
  `02-deputy-in-the-middle` — Explore how the server decides who can do what, then use that to retrieve the flag.

- [ ] **Challenge 3 — Looks legit to me**  
  `03-looks-legit-to-me` — Get the server to reveal the internal report by triggering hidden instructions in a tool's description.

- [ ] **Challenge 4 — Name your poison**  
  `04-name-your-poison` — When you ask to send a message, more than one tool could answer—what you get back depends which one the server chooses.

- [ ] **Challenge 5 — Behind the curtain**  
  `05-behind-the-curtain` — The summarizer reads more than the document. Find the format it obeys and how to ask for the rest.

- [ ] **Challenge 6 — Forward thinking**  
  `06-forward-thinking` — One tool gives you something another tool needs. Piece the steps together to receive the flag.

---
