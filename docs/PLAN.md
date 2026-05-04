# Project Pixel — Build Plan

A personalized AI desk assistant based on the [OmniBot](https://github.com/nazirlouis/OmniBot)
open-source project. ~10 units, gifted to colleagues and bosses who work from home on Macs.
Plug-and-play, no technical knowledge required from recipients.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Hardware & Parts List](#2-hardware--parts-list)
3. [3D Enclosure](#3-3d-enclosure)
4. [Software Architecture](#4-software-architecture)
5. [Code Modifications](#5-code-modifications)
6. [Onboarding Flow](#6-onboarding-flow)
7. [Pre-Personalization (Per Unit)](#7-pre-personalization-per-unit)
8. [Setup Guide for Recipients](#8-setup-guide-for-recipients)
9. [Welcome Card](#9-welcome-card)
10. [Phased Build Plan](#10-phased-build-plan)

---

## 1. Project Overview

### What it is
A physical AI assistant that sits on a home desk. It wakes on voice, sees through its camera,
talks back via a round display and speaker, and maintains a memory of who its owner is.

### Key design decisions
| Decision | Choice | Reason |
|---|---|---|
| AI brain | Claude API (Anthropic) | Personality, memory, reasoning — superior to Gemini for nuanced conversation |
| Voice output | Gemini Flash TTS (free tier) | Zero cost per unit, good quality, no ElevenLabs dependency |
| Provisioning | Captive portal on ESP32 | No companion app needed; works on any phone/laptop |
| Hub software | Docker on Mac | Self-contained; one command to start |
| API keys | User provides their own | Each person owns their data; no shared backend |
| First run | Guided onboarding interview | Pixel learns the user's name, role, preferences automatically |
| Pre-ship | Name + role seeded per unit | Feels personal from the first interaction |

### Base project
`omnibot/` — upstream OmniBot clone (read-only reference). Do not modify this directory.
Our modified code lives in `firmware/`, `hub/`, and `tools/`.

---

## 2. Hardware & Parts List

### Per unit (×10)

| Component | Part | Est. Price | Notes |
|---|---|---|---|
| MCU + camera | Seeed Studio XIAO ESP32-S3 Sense | ~$15 | Built-in OV2640 camera + PDM mic |
| Display | Seeed Studio 1.28" Round Touch Display Shield | ~$10 | GC9A01 240×240, CHSC6X touch, PCF8563 RTC |
| Audio output | MAX98357A I2S DAC + small 4Ω/3W speaker | ~$5 | Mono, fits inside enclosure |
| Power | USB-C cable + 5V/1A wall adapter | ~$5 | No battery — always plugged in |
| Enclosure | 3D printed (Bambu Lab X1) | ~$2 filament | See section 3 |
| Misc | Short wires, M2 screws, rubber feet | ~$2 | |

**Estimated BOM per unit: ~$39**
**10-unit total: ~$390**

### Tools & consumables (one-time)
- PlatformIO (VS Code extension) — firmware flashing
- USB-C to USB-A cable for initial flash
- Bambu Lab X1 with PLA or PETG filament
- Soldering iron (minimal — I2S DAC wiring)

---

## 3. 3D Enclosure

### Design goals
- Compact cylinder or puck shape (~70–80mm diameter, ~50mm tall)
- Round display flush with top face
- Ventilation slots (ESP32-S3 runs warm under load)
- Cable exit at rear/bottom for USB-C
- Speaker grille on front or side
- Snap-fit lid or M2 screw retention — no glue
- Camera hole aligned with display axis (forward-facing)

### Research starting points
- **OmniBot default enclosure**: check `omnibot/` for any STL files or linked designs
- **Printables / Thingiverse**: search "XIAO ESP32-S3 Sense round display enclosure"
- **GC9A01 round display mounts**: several community designs exist for the 1.28" Seeed round shield
- **Design from scratch if needed**: Fusion 360 or Bambu Studio parametric design

### Print settings (Bambu X1)
- Material: PETG (better heat tolerance than PLA near USB-C port)
- Layer height: 0.2mm standard
- Infill: 15% gyroid
- Supports: required for camera/speaker holes

### Files
Store STL/3MF files in `enclosure/stl/`. Document design decisions in `enclosure/README.md`.

---

## 4. Software Architecture

```
[XIAO ESP32-S3 Sense]
  │  USB-C power
  │  Wi-Fi (captive portal → user's LAN)
  │  WebSocket (ws://hub-mac:8000)
  └──────────────────────────────────────┐
                                         ▼
                              [Mac Hub — Docker]
                              ┌─────────────────────────────┐
                              │  hub/backend/  (FastAPI)    │
                              │  ┌──────────────────────┐   │
                              │  │  Wake word detect    │   │
                              │  │  Audio stream in/out │   │
                              │  │  Claude API client ◄─┼───┼──► api.anthropic.com
                              │  │  Gemini Flash TTS  ◄─┼───┼──► generativelanguage.googleapis.com
                              │  │  Persona/memory mgr  │   │
                              │  │  Onboarding engine   │   │
                              │  └──────────────────────┘   │
                              │  hub/frontend/  (React)      │
                              │  Settings UI, dashboard       │
                              └─────────────────────────────┘
```

### Key files (upstream OmniBot → our copies)

| Upstream | Our Copy | Change |
|---|---|---|
| `omnibot/app/backend/gemini_live_session.py` | `hub/backend/claude_session.py` | Full rewrite for Claude API |
| `omnibot/app/backend/app.py` | `hub/backend/app.py` | Swap Gemini refs → Claude, add onboarding routes |
| `omnibot/app/backend/elevenlabs_tts_stream.py` | `hub/backend/gemini_tts_stream.py` | Rewrite for Gemini Flash TTS |
| `omnibot/app/backend/persona.py` | `hub/backend/persona.py` | Extend for onboarding interview state |
| `omnibot/app/backend/.env.example` | `hub/backend/.env.example` | Add ANTHROPIC_API_KEY, keep GEMINI_API_KEY |
| `omnibot/bots/Pixel/src/main.cpp` | `firmware/src/main.cpp` | Add captive portal, remove BLE provisioning |
| `omnibot/bots/Pixel/platformio.ini` | `firmware/platformio.ini` | Copy as-is initially |

---

## 5. Code Modifications

### 5.1 Captive Portal (ESP32 Firmware)

**Goal**: On first boot (no stored Wi-Fi credentials), ESP32 broadcasts its own Wi-Fi hotspot.
User connects from their phone or Mac, gets redirected to a config page, enters home Wi-Fi
SSID + password + hub Mac's IP address. Device saves to NVS and reboots onto the real network.

**Current state (OmniBot)**: Uses BLE GATT provisioning — requires the hub app running and a
BLE connection. Not user-friendly for gift recipients.

**Implementation plan**:
1. In `firmware/src/main.cpp`, replace `startBLEProvisioning()` with `startCaptivePortal()`
2. `startCaptivePortal()` does:
   - `WiFi.mode(WIFI_AP)` → broadcasts SSID `"Pixel-Setup"` (or `"Pixel-[Name]"` if pre-seeded)
   - Starts `AsyncWebServer` on port 80
   - `DNSServer` redirects all DNS queries to 192.168.4.1 (captive portal trigger)
   - Serves a minimal HTML form: Wi-Fi SSID, password, Hub IP address
   - On POST: saves to NVS under `wifi_creds`, shows "Connecting..." on display, reboots
3. Remove all BLE library deps from `platformio.ini` to free RAM (BLE + Wi-Fi simultaneously
   is a memory hazard on ESP32-S3 with camera active)
4. Fallback: if connection fails after 3 attempts, re-open captive portal automatically

**Dependencies to add** (platformio.ini):
```
me-no-dev/AsyncTCP @ ^1.1.1
me-no-dev/ESP Async WebServer @ ^1.2.3
```

**Display messages**:
- `"PIXEL SETUP"` + QR or IP on screen while portal is active
- `"CONNECTING..."` during Wi-Fi join
- `"CONNECTED"` + IP address on success

### 5.2 Claude API Brain (Hub Backend)

**Goal**: Replace `gemini_live_session.py` with a Claude-based conversation engine.

**Current Gemini flow**:
- Gemini Live SDK: bidirectional audio+video streaming, native TTS, tool calls
- One persistent session per connected bot

**Claude flow (new)**:
- Claude API: `claude-sonnet-4-6` (or `claude-haiku-4-5` for lower latency/cost)
- Audio pipeline: ESP32 → hub captures PCM → STT (Whisper or Google STT via existing code) →
  text → Claude API → text response → Gemini TTS → audio → ESP32
- Tool calls: Claude tool_use API (maps to OmniBot's pixel_tool_declarations.py equivalents)
- Memory: Claude's extended thinking or system prompt injection from persona files

**New file**: `hub/backend/claude_session.py`
```python
# Key responsibilities:
# - Maintain per-bot conversation history (list of messages)
# - Inject persona/memory context into system prompt on each turn
# - Call anthropic.messages.create() with tool definitions
# - Return text + tool calls to app.py dispatcher
# - Handle streaming responses for lower latency
```

**API key handling**: `.env` adds `ANTHROPIC_API_KEY=`. Hub settings UI exposes it alongside
the existing Gemini key field.

**Model selection**: Start with `claude-sonnet-4-6`. Budget units may use `claude-haiku-4-5`.

### 5.3 Gemini Flash TTS (Hub Backend)

**Goal**: Keep Gemini for text-to-speech only (free tier, good quality).

**Current state**: OmniBot already supports Gemini TTS as `pixel_tts_voice = "gemini"` —
this is already implemented in `gemini_live_session.py` when using Gemini Live.

**Action needed**: Extract/adapt the TTS-only code path into `hub/backend/gemini_tts_stream.py`
so it works independently of the Gemini Live session (which we're removing as the brain).

**API**: `google.generativeai` → `genai.generate_content()` with speech synthesis config, or
the newer `google-genai` SDK's `generate_content` with audio response MIME type.
Free tier: Gemini Flash 2.0 / Flash 1.5 → 15 RPM / 1M TPD (more than enough for desk assistant).

### 5.4 Persona System & Memory

**Goal**: Each unit has a pre-seeded persona (name, role). On first launch, Pixel conducts an
onboarding interview to fill in deeper preferences and build memory files.

**Existing OmniBot infrastructure** (`persona.py`, `persona_defaults/`): Already supports
persona YAML/JSON files with name, personality, memory snippets. We extend this.

**Pre-seeded fields** (set before shipping):
```json
{
  "recipient_name": "Sarah",
  "recipient_role": "Product Manager at Acme Corp",
  "gift_from": "Peter",
  "onboarding_complete": false
}
```

**Onboarding interview** (first launch, `onboarding_complete: false`):
Pixel asks ~5 questions to build the memory profile. See section 6.

---

## 6. Onboarding Flow

### Trigger
`onboarding_complete: false` in the unit's persona config. Checked on hub startup after
the WebSocket connection from the ESP32 is established.

### Interview script
Pixel greets the user and explains it wants to get to know them. Questions are asked
conversationally — not as a form.

1. **Work context**: "What kind of work do you spend most of your day on?"
2. **Communication style**: "Do you prefer quick bullet-point answers, or do you like me to
   explain things in more detail?"
3. **Daily rhythm**: "What time do you usually start your day, and are there times you're in
   deep focus and shouldn't be interrupted?"
4. **Interests / hobbies**: "What do you like to do when you're not working?"
5. **A personal touch**: "Is there anything specific you'd love me to help you with regularly —
   like briefings, reminders, brainstorming, or just someone to talk to?"

### Onboarding engine (`hub/backend/onboarding.py`)
- State machine: `greeting → q1 → q2 → q3 → q4 → q5 → summary → complete`
- Each answer fed to Claude to extract structured facts → appended to persona memory file
- On `complete`: sets `onboarding_complete: true`, saves persona, transitions to normal mode
- On interrupt (user leaves mid-interview): saves partial state, resumes on next connection

---

## 7. Pre-Personalization (Per Unit)

Before shipping each unit:

1. Flash firmware with recipient's hotspot SSID baked in (or use generic captive portal — 
   captive portal is simpler and more reliable)
2. Create `personas/<recipient>/persona.json` with name, role, gift_from fields
3. Copy persona into the hub Docker image or mount via `OMNIBOT_DATA_DIR` volume
4. Label the unit's USB-C cable with recipient's name

### Persona directory structure
```
personas/
├── sarah_chen/
│   └── persona.json
├── mike_torres/
│   └── persona.json
└── ... (one per recipient)
```

---

## 8. Setup Guide for Recipients

### What the recipient needs to do (one time)

**Step 1: Get your API keys** (~5 min)
- Claude API key: [console.anthropic.com](https://console.anthropic.com) → create account → API Keys → New Key
  - Add $5 credit (lasts months for a desk assistant use pattern)
- Gemini API key: [aistudio.google.com](https://aistudio.google.com) → Get API Key → Free tier, no card needed

**Step 2: Install Docker Desktop** (~5 min)
- [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) → Mac (Apple Silicon or Intel)
- Open Docker Desktop and let it finish setup

**Step 3: Start the Pixel Hub** (~2 min)
```bash
# Run this one command in Terminal:
curl -fsSL https://[YOUR_SETUP_URL]/install.sh | bash
```
Or manually:
```bash
docker run -d \
  -e ANTHROPIC_API_KEY=your_key_here \
  -e GEMINI_API_KEY=your_key_here \
  -p 8000:8000 \
  --name pixel-hub \
  [image]:latest
```

**Step 4: Connect Pixel to your Wi-Fi** (~3 min)
1. Plug Pixel into USB-C power
2. On your phone or Mac, connect to the Wi-Fi network **"Pixel-Setup"**
3. A setup page opens automatically (or go to http://192.168.4.1)
4. Enter your home Wi-Fi name + password, and your Mac's IP address
5. Pixel reboots and connects — the screen shows your name

**Step 5: Meet Pixel**
Say "Hey Pixel" and Pixel will introduce itself and ask you a few questions to get to know you.

### Finding your Mac's IP address
- Apple menu → System Settings → Wi-Fi → Details → IP Address
- Or in Terminal: `ipconfig getifaddr en0`

### Troubleshooting
- Pixel shows "CONNECTING..." for more than 30 seconds → redo Step 4 (check IP address)
- Hub not responding → make sure Docker Desktop is running, then re-run the start command
- QR code on the welcome card links to the full online guide with screenshots

---

## 9. Welcome Card

### Physical card (postcard size, printed)

**Front**: Clean illustration of Pixel glowing on a desk. Title: **"Meet Pixel"**

**Back**:
```
Hi [Name],

This is Pixel — your personal AI desk assistant.
It knows who you are and is here to help.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GET STARTED IN 15 MINUTES:

  1. Get two free API keys (5 min)
  2. Install Docker Desktop (5 min)
  3. Plug in Pixel — follow the screen

Full step-by-step guide:
  [QR CODE]  →  [SHORT URL]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wake word: "Hey Pixel"

Made with care by Peter  ♥
```

### Digital setup guide (linked by QR code)
A simple web page (or Notion/GitHub Pages) with screenshots for each step.
URL: TBD — set up after hub image is published.

---

## 10. Phased Build Plan

### Phase 1 — Foundation (Weeks 1–2)
**Goal**: One working unit with Claude brain and Gemini TTS.

- [ ] Copy `omnibot/app/backend/` → `hub/backend/` as working base
- [ ] Write `hub/backend/claude_session.py` (Claude API conversation engine)
- [ ] Modify `hub/backend/app.py`: swap Gemini Live → Claude session, keep Gemini TTS path
- [ ] Write `hub/backend/gemini_tts_stream.py` (TTS-only, extracted from Gemini Live)
- [ ] Update `hub/backend/.env.example` with ANTHROPIC_API_KEY
- [ ] Update `hub/backend/requirements.txt`: add `anthropic`, remove unused Gemini Live deps
- [ ] Test full voice loop: wake word → STT → Claude → Gemini TTS → speaker
- [ ] Copy `omnibot/bots/Pixel/` → `firmware/` as working base
- [ ] Verify firmware compiles and connects to modified hub

### Phase 2 — Captive Portal (Week 3)
**Goal**: No BLE, first-boot Wi-Fi setup via phone.

- [ ] Implement `startCaptivePortal()` in `firmware/src/main.cpp`
- [ ] Add AsyncWebServer + DNSServer to `firmware/platformio.ini`
- [ ] Remove BLE library deps
- [ ] Design captive portal HTML/CSS (minimal, mobile-friendly)
- [ ] Test on fresh ESP32-S3 (no stored credentials)
- [ ] Test re-provisioning flow (settings button → clear Wi-Fi → portal reopens)
- [ ] Test firmware with hub running on Mac (not localhost — real LAN IP)

### Phase 3 — Onboarding Interview (Week 4)
**Goal**: First-launch Pixel conducts interview, builds persona memory.

- [ ] Write `hub/backend/onboarding.py` (state machine + Claude-driven extraction)
- [ ] Extend `hub/backend/persona.py` with `onboarding_complete` field + save/load
- [ ] Create per-recipient `personas/` directory with pre-seeded JSON files
- [ ] Wire onboarding trigger into `app.py` (check flag on bot connect)
- [ ] Test full onboarding flow: questions → answers → persona file written → normal mode
- [ ] Test resume from interrupted onboarding

### Phase 4 — Enclosure & Hardware (Weeks 4–5)
**Goal**: Physical unit assembled, looks like a finished product.

- [ ] Research existing enclosure designs (Printables, Thingiverse)
- [ ] Design or adapt enclosure in Fusion 360 / Bambu Studio
- [ ] Print prototype (1 unit), check fit for display, camera, USB-C, speaker
- [ ] Iterate design (expect 1–2 rounds)
- [ ] Wire I2S DAC + speaker inside enclosure
- [ ] Print remaining 9 units
- [ ] Document final print settings in `enclosure/README.md`

### Phase 5 — Pre-Personalization & Batch Flash (Week 5)
**Goal**: 10 units ready to ship, each named for its recipient.

- [ ] Write `tools/flash_unit.sh` — flash firmware to one unit (wraps PlatformIO)
- [ ] Write `tools/personalize.sh` — generate persona JSON for a recipient
- [ ] Create persona configs for all ~10 recipients in `personas/`
- [ ] Flash firmware to all 10 units
- [ ] Load Docker image + persona files, smoke-test each unit
- [ ] Label USB-C cables

### Phase 6 — Setup Guide & Welcome Card (Week 5–6)
**Goal**: Recipients can set up without help.

- [ ] Write full setup guide (Markdown → publish to web/Notion)
- [ ] Get short URL / QR code pointing to guide
- [ ] Design welcome card (Figma or Canva)
- [ ] Print 10 welcome cards
- [ ] Pack units: device + USB-C cable + wall adapter + welcome card

### Phase 7 — Executive Intelligence Package (Post-launch)
**Goal**: Calendar awareness, email drafting, meeting notes, daily briefings — with a hard human-in-the-loop gate on all consequential actions.

**Design constraint (non-negotiable):** See `docs/design-principles.md` — Claude can read and draft anything. Claude cannot send, post, create, modify, or delete anything without explicit human confirmation. This is structural, not a setting.

#### 7a — Obsidian Vault as Persistent Storage
- [ ] Define vault folder structure (`notes/`, `emails/`, `pending/`, `skills/`, `persona/`)
- [ ] Update `docker-compose.yml` — mount `~/pixel-vault/` as Docker volume
- [ ] Move persona files into vault volume (currently stored inside container)
- [ ] Document how recipients open vault in Obsidian desktop app
- [ ] Verify vault survives container rebuild/update

#### 7b — Skills System
- [ ] Write default skill templates as markdown files in `vault/skills/default/`
  - `take_meeting_notes.md`
  - `draft_email.md`
  - `daily_briefing.md`
  - `calendar_summary.md`
  - `draft_response.md`
- [ ] Write `tools/update_skills.sh` — pulls company skills from private git repo into `vault/skills/company/`
- [ ] Wire skills folder into `build_composed_system_instruction()` in `persona.py`
- [ ] Test skill update flow: push to company repo → restart hub → new skill available

#### 7c — Human-in-the-Loop Gate
- [ ] Write `hub/backend/action_queue.py` — staged actions pending human confirmation
  - `stage_action(action_type, payload, description)` → writes to `vault/pending/`
  - `confirm_action(action_id)` → executes the real API call
  - `discard_action(action_id)` → removes from pending
- [ ] Define confirmation tool in Claude's tool list — Claude surfaces staged actions but never executes them
- [ ] Wire confirmation into voice path: "yes send it" / "cancel" / "show me the draft"
- [ ] Wire confirmation into dashboard: pending actions panel with approve/discard buttons
- [ ] Write test: confirm that no staged action executes without explicit confirmation signal

#### 7d — Gmail + Calendar + Drive via MCP (already in use at org)
**No OAuth build needed.** The org already runs MCP servers for Gmail, Google Calendar, and Google Drive and uses them with Claude via Claude Code CLI. Google Workspace admin approval is already granted. BAA coverage is confirmed (Claude API/CLI path only — not Claude.ai desktop or Workspace).

- [ ] Run Gmail, Calendar, Drive MCP servers alongside hub in `docker-compose.yml` (separate services)
- [ ] Wire MCP server connections into `hub/backend/claude_session.py` via Anthropic SDK MCP support
- [ ] OAuth tokens stored in vault volume — persist across container restarts
- [ ] Validate all three tools surface correctly in Claude's tool list at hub startup
- [ ] `send_email`, `create_event`, `modify_event`, `delete_*` tools routed through `action_queue.py` (human gate — see Phase 7c)
- [ ] Read-only tools (`read_emails`, `get_calendar`, `read_drive`) pass through directly, no gate

#### 7f — Daily Briefing Skill
- [ ] On morning wake word (or scheduled): pull calendar + recent emails → compose spoken briefing
- [ ] Format: upcoming meetings, flagged emails, any pending actions from prior session
- [ ] Write briefing summary to `vault/notes/daily/YYYY-MM-DD.md`

---

### Phase 8 — Delivery & Support
- [ ] Hand-deliver or ship units
- [ ] Monitor for setup issues (available for help first week)
- [ ] Document common issues in `docs/troubleshooting.md`
- [ ] Plan OTA firmware update mechanism (nice-to-have post-launch)

---

## Open Questions

| Question | Status |
|---|---|
| STT/TTS: Whisper + MLX-Audio replacing Gemini | Decided — see `docs/local-audio-recommendation.md` |
| Hub Docker image registry: GitHub Container Registry or Docker Hub? | TBD |
| Setup guide URL: GitHub Pages vs Notion vs simple HTML? | TBD |
| Wake word: keep openwakeword "Hey Pixel" or change? | Keep for now |
| Short URL for welcome card QR code | TBD after guide is published |
| OTA firmware updates: feasible for gift units? | Post-launch |
| Google Workspace admin approval needed for Gmail OAuth? | Confirm before Phase 7d |
| Obsidian CLI: worth adding? | No — vault is plain markdown files, Python file I/O is sufficient |

---

*Last updated: 2026-05-04*
