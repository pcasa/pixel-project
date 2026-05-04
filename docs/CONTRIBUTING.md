# Contributing Guide

---

## How We Work

**Everyone works on everything together.**

No one owns a phase. No one is the "firmware person" or the "Python person." All three of us go through every phase, touch every file, and build the same understanding. The goal is that when we're done, any one of us could explain how the whole system works — not just our corner of it.

In practice this means:
- We tackle one phase at a time as a group
- Everyone reads the same docs before we write any code
- Everyone writes their own version or contributes to a shared implementation
- We talk through decisions together before making them
- When someone's stuck, we work through it together rather than one person just fixing it

This is slower than dividing work. It's also how you actually learn.

---

## Git Workflow

```bash
# One branch per phase — everyone works off the same branch
git checkout -b phase-2/captive-portal

# Pull before you start to get everyone's latest
git pull origin phase-2/captive-portal

# Commit often with clear messages
git add firmware/src/main.cpp
git commit -m "replace startBLEProvisioning with startCaptivePortal skeleton"

# Push so everyone can see progress
git push origin phase-2/captive-portal
```

**Rules:**
- Never commit directly to `main`
- One branch per phase — shared by all three
- Merge to `main` only when the whole group agrees it's done
- `omnibot/` is read-only — never edit files there

---

## Phase by Phase

We go through these in order. Don't start a phase until the previous one is merged and everyone understands it.

---

### Phase 2 — Captive Portal
**Branch:** `phase-2/captive-portal`
**Files:** `firmware/src/main.cpp`, `firmware/platformio.ini`
**Language:** C++

**What we're building:**
The ESP32 currently uses Bluetooth to receive Wi-Fi credentials — which requires the hub app and a BLE pairing step. Too complex for recipients who aren't technical. We're replacing it with a **captive portal**: on first boot the ESP32 broadcasts its own hotspot called `Pixel-Setup`. Connect to it from any phone or laptop, a config page opens automatically (like a hotel Wi-Fi page), enter home Wi-Fi credentials and the Mac's IP, the device saves it and reboots connected.

**Before writing any code, everyone reads:**
- `docs/CONCEPTS.md` → section 10 (ESP32 Firmware and PlatformIO)
- `firmware/src/main.cpp` → find `startBLEProvisioning()` — that's what we're replacing
- `firmware/platformio.ini` — understand how libraries are declared

**Libraries to add to `platformio.ini`:**
```
me-no-dev/AsyncTCP @ ^1.1.1
me-no-dev/ESP Async WebServer @ ^1.2.3
```

**What done looks like:**
- [ ] Fresh ESP32 (no stored credentials) boots to a `Pixel-Setup` Wi-Fi hotspot
- [ ] Any URL on that hotspot redirects to the config page (DNS redirect)
- [ ] Config page collects: Wi-Fi SSID, password, Hub IP address
- [ ] On submit: saves to NVS flash, shows `CONNECTING...`, reboots connected
- [ ] Success shows `CONNECTED` + the device's IP on the display
- [ ] 3 failed attempts → portal reopens automatically
- [ ] All BLE library deps removed from `platformio.ini`

**What we'll all understand after this:**
Embedded C++, how microcontrollers handle Wi-Fi and networking, DNS redirection, NVS flash storage, async HTTP servers on constrained hardware

---

### Phase 3 — Onboarding Interview
**Branch:** `phase-3/onboarding`
**Files:** `hub/backend/onboarding.py` (new), `hub/backend/app.py` (small hook)
**Language:** Python

**What we're building:**
When a Pixel connects for the first time, instead of going straight into conversation, Pixel introduces itself and asks ~5 questions to learn about the user. The answers get written into their persona files (`USER.md`, `MEMORY.md`) so Claude carries that context in every future conversation. This is what makes each unit feel personal.

**Before writing any code, everyone reads:**
- `docs/CONCEPTS.md` → sections 2, 3, and 4 (Claude API, System Prompts, Tool Use)
- `hub/backend/persona.py` in full — especially `write_persona_markdown()` and `build_composed_system_instruction()`
- `hub/backend/claude_session.py` — understand `send_message()`
- `hub/backend/app.py` → `esp32_stream_endpoint()` — the connection lifecycle

**The 5 questions:**
1. What kind of work do you spend most of your day on?
2. Do you prefer quick answers or detailed explanations?
3. What time do you start your day, and when are you in deep focus?
4. What do you like to do when you're not working?
5. Is there anything you'd love regular help with?

**What done looks like:**
- [ ] Device with `onboarding_complete: false` triggers interview on first wake word
- [ ] Questions are asked naturally in character — not as a numbered list
- [ ] Answers extracted by Claude and written to `USER.md` and `MEMORY.md`
- [ ] After all 5, transitions to normal conversation mode
- [ ] Interrupted interviews resume from the right question on reconnect
- [ ] Device with `onboarding_complete: true` skips interview entirely

**What we'll all understand after this:**
State machines in async Python, Claude API prompt engineering, how persona/memory files shape Claude's behavior, async file I/O

---

### Phase 4 — Local Audio
**Branch:** `phase-4/local-audio`
**Files:** `hub/backend/local_audio.py` (new), `hub/backend/app.py` (swap import), `hub/backend/requirements.txt`, `hub/backend/.env.example`, `docker-compose.yml`
**Language:** Python

**What we're building:**
The hub currently uses Gemini's cloud API for both STT (voice → text) and TTS (text → voice). This is a HIPAA compliance problem — we have a BAA with Anthropic but not Google. We're replacing both with fully local processing: Whisper or MLX-Audio for STT, MLX-Audio or Kokoro-ONNX for TTS. Audio never leaves the Mac.

**Before writing any code, everyone reads:**
- `docs/CONCEPTS.md` → sections 5 and 6 (Whisper, TTS/MLX-Audio)
- `docs/local-audio-recommendation.md` — the full decision with library comparison
- `hub/backend/gemini_tts_stream.py` — the file we're replacing; understand what each function returns
- `hub/backend/app.py` → `_run_claude_audio_turn()` — how those functions are called

**The interface `app.py` expects:**
```python
async def transcribe_audio(wav_bytes: bytes) -> str:
    """WAV bytes → transcript text. Empty string on failure."""

async def text_to_pcm(text: str, voice: str = None) -> bytes:
    """Text → raw 24kHz PCM bytes. Empty bytes on failure."""

def list_voices() -> list[str]:
    """Available voice names for the settings UI."""
```

**What done looks like:**
- [ ] `transcribe_audio()` correctly transcribes spoken English from 16kHz WAV
- [ ] `text_to_pcm()` returns valid 24kHz PCM that plays in the browser dashboard
- [ ] Auto-detects Apple Silicon vs Intel at startup, uses the right path
- [ ] Zero network calls — verify by testing with Wi-Fi off
- [ ] At least 3 voice options via `list_voices()`
- [ ] `GEMINI_API_KEY` removed from `.env.example`, `docker-compose.yml`, and `app.py` warnings
- [ ] `gemini_tts_stream.py` deleted entirely
- [ ] Recipients only need one API key: Claude

**What we'll all understand after this:**
Local ML model inference, audio fundamentals (sample rates, PCM), Apple Silicon optimization via MLX, the full voice pipeline from mic to speaker

---

### Phase 5 — Personalization & Flash Tools
**Branch:** `phase-5/tools`
**Files:** `tools/flash_unit.sh`, `tools/personalize.sh`
**Language:** Bash / Python

Build the scripts that let us quickly set up all 10 units before shipping — generate a persona JSON for each recipient, flash firmware, verify connection.

---

### Phase 6 — Setup Guide & Welcome Card
**Branch:** `phase-6/docs`
**Files:** `docs/setup-guide.md`, `docs/welcome-card.md`

Write the materials that ship with each unit. The setup guide walks a non-technical person through getting their API key, installing Docker, and connecting to Pixel. The welcome card is a printed postcard with a QR code.

---

## Code Style

**Python:**
- Type hints on all function signatures
- `async def` for anything that does I/O
- Names that read like English — minimize the need for comments
- Functions over ~50 lines should be split

**C++ (firmware):**
- Follow the existing style in `main.cpp`
- `Serial.printf()` for debug with `[Section]` prefixes
- Keep `loop()` non-blocking — use FreeRTOS tasks for slow operations

**Both:**
- Named constants — no bare numbers
- Delete code you replace — no commented-out dead blocks

---

## Learning Resources

| Topic | Resource |
|---|---|
| Claude API | [docs.anthropic.com](https://docs.anthropic.com) — Messages, Tool Use, Models |
| Python async | `asyncio` docs → "Coroutines and Tasks" |
| FastAPI + WebSockets | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| ESP32 firmware | Search "ESP32 Arduino AsyncWebServer captive portal" |
| Local audio | [MLX-Audio](https://github.com/Blaizzy/mlx-audio), [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) |

---

## When Someone's Stuck

Work through it together. Not by jumping to the answer — by talking through what you know, what you've tried, and what you'd look at next. Everyone in the conversation learns something, even the person who wasn't stuck.
