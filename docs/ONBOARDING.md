# Onboarding Guide

Welcome to Project Pixel. This doc gets you from zero to a running dev environment. You don't need the physical hardware to start — the hub runs fine on its own for backend development.

---

## Prerequisites

Install these before anything else:

| Tool | Why | Install |
|---|---|---|
| **Git** | Version control | `brew install git` |
| **Python 3.11** | Hub backend | `brew install python@3.11` |
| **Node.js 20+** | Dashboard frontend | `brew install node` |
| **Docker Desktop** | Run the hub in a container | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| **VS Code** | Editor | [code.visualstudio.com](https://code.visualstudio.com) |
| **PlatformIO** (VS Code extension) | ESP32 firmware | Install via VS Code Extensions panel |

**Check your versions:**
```bash
python3.11 --version   # Should be 3.11.x
node --version         # Should be 20.x or higher
docker --version       # Any recent version
git --version          # Any recent version
```

---

## Clone the Repo

```bash
git clone <repo-url> project_pixel
cd project_pixel
```

> Note: `omnibot/` is the upstream OmniBot source, included as a reference. **Do not edit files in `omnibot/`.** All our work lives in `hub/`, `firmware/`, `docs/`, and `tools/`.

---

## Get Your API Key

Pixel uses the Claude API as its AI brain. You need a personal API key.

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an account (or sign in)
3. Navigate to **API Keys** → **Create Key**
4. Copy the key — you'll only see it once
5. Add $5 credit under **Billing** (lasts months for typical use)

---

## Set Up the Hub Backend

### Option A — Run directly with Python (fastest for development)

```bash
cd hub/backend

# Create a virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Start the server
python app.py
```

The hub runs at `http://localhost:8000`. Open it in your browser to see the dashboard.

### Option B — Run with Docker (closest to what recipients use)

```bash
# From the repo root:
cp hub/backend/.env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

docker compose up --build
```

Hub runs at `http://localhost:8000`.

---

## Explore the Dashboard

With the hub running, open `http://localhost:8000` in Chrome or Firefox.

The dashboard shows:
- **Connected devices** (none yet without hardware)
- **Intelligence Feed** — live transcript of conversations
- **Settings** — per-device configuration, API key management
- **Persona editor** — SOUL, USER, MEMORY files

You can send text commands to Pixel from the dashboard even without hardware — good for testing Claude responses.

---

## Set Up the Frontend for Development

If you're working on the dashboard UI:

```bash
cd hub/frontend
npm install
npm run dev    # Runs at http://localhost:5173 with hot reload
```

The frontend proxies API calls to the backend at port 8000, so you need the backend running too.

---

## Set Up Firmware Development (ESP32)

You only need this if you're working on the device firmware.

1. Install the **PlatformIO** extension in VS Code
2. Open `firmware/` as a PlatformIO project
3. PlatformIO will auto-install the ESP32 toolchain and libraries on first open

**To flash the firmware to a device:**
1. Connect the XIAO ESP32-S3 Sense via USB-C
2. In VS Code: click the PlatformIO icon → **Upload**
3. Or from terminal: `cd firmware && pio run --target upload`

**To monitor serial output:**
```bash
cd firmware && pio device monitor
```

This shows debug logs from the ESP32 — useful for troubleshooting Wi-Fi and WebSocket connections.

---

## Project Structure Walkthrough

Here's what to read first, in order:

### 1. `hub/backend/hub_config.py`
Short file (~250 lines). Handles API key loading, data directory config, and secrets storage. Good starting point — no domain knowledge required.

### 2. `hub/backend/claude_session.py`
Our main addition. ~150 lines. Shows how we talk to the Claude API, manage conversation history, and handle tool calls. Read this alongside [docs/CONCEPTS.md](CONCEPTS.md) sections 2 and 4.

### 3. `hub/backend/persona.py`
How Pixel's personality/memory system works. Reads and writes markdown files (SOUL.md, USER.md, MEMORY.md etc.) that form the system prompt. ~535 lines but very readable.

### 4. `hub/backend/app.py`
The main server — 3,000+ lines. Don't try to read it all at once. Jump to specific functions:
- `esp32_stream_endpoint()` — how the device connects
- `_run_claude_audio_turn()` — the full voice interaction pipeline
- `stream_chat_turn_response()` — text command from dashboard

### 5. `firmware/src/main.cpp`
The ESP32 program. ~3,600 lines of C++. Key sections are clearly commented:
- `USER CONFIGURATION` at the top — Wi-Fi and hub IP settings
- `webSocketEvent()` — how it handles messages from the hub
- `wakeStreamTask()` — how it streams mic audio

---

## Making Your First Change

A good first exercise: **change Pixel's default greeting in SOUL.md**.

1. Open `hub/backend/persona_defaults/SOUL.md`
2. Find the personality description and change something small
3. Restart the hub (`python app.py`)
4. Send a text command from the dashboard: "Introduce yourself"
5. Notice how Claude's response reflects your change

This demonstrates the whole system: persona files → system prompt → Claude API → response.

---

## Useful Commands

```bash
# Run hub backend
cd hub/backend && python app.py

# Run hub in Docker
docker compose up

# Run frontend dev server
cd hub/frontend && npm run dev

# Flash firmware
cd firmware && pio run --target upload

# Watch ESP32 serial output
cd firmware && pio device monitor

# Run Python syntax check on a file
python3 -m py_compile hub/backend/claude_session.py

# Install a new Python package and add to requirements
pip install package-name && pip freeze | grep package-name >> hub/backend/requirements.txt
```

---

## Troubleshooting

**Hub fails to start — `ModuleNotFoundError`**
Make sure your virtual environment is active: `source hub/backend/.venv/bin/activate`

**`ANTHROPIC_API_KEY not configured` warning on startup**
You haven't added your key to `.env`. Edit `hub/backend/.env` and add `ANTHROPIC_API_KEY=sk-ant-...`

**ESP32 not connecting to hub**
The hub IP in the firmware must match your Mac's actual LAN IP. Find it: `ipconfig getifaddr en0`. Then update `backend_ip` at the top of `firmware/src/main.cpp` and re-flash.

**Docker build fails**
Make sure Docker Desktop is running (check the menu bar icon). Then: `docker compose build --no-cache`

**PlatformIO can't find the device**
Try a different USB-C cable (some cables are charge-only, not data). On Mac you may need to allow the USB driver in System Settings → Privacy & Security.
