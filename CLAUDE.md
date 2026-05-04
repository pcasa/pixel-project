# Project Pixel — Claude Code Instructions

## What this project is
A personalized AI desk assistant built on OmniBot. ~10 units gifted to colleagues. Hardware: XIAO ESP32-S3 Sense + 1.28" round display. Hub runs on Mac via Docker.

## Critical rules
- **`omnibot/` is READ ONLY** — never edit files there. It is the upstream reference.
- All working code lives in `hub/`, `firmware/`, `docs/`, `tools/`, `personas/`
- `hub/backend/` is a fork of `omnibot/app/backend/` — our additions are `claude_session.py`, `gemini_tts_stream.py` (being replaced), and modifications to `app.py` and `hub_config.py`
- `firmware/` is a fork of `omnibot/bots/Pixel/`

## AI stack
- **Brain:** Claude API (`claude-sonnet-4-6`) — `hub/backend/claude_session.py`
- **STT:** Local Whisper or MLX-Audio — `hub/backend/local_audio.py` (not yet written, replacing `gemini_tts_stream.py`)
- **TTS:** Local MLX-Audio or Kokoro-ONNX — same file
- **Gemini is intentionally removed** — HIPAA/BAA compliance. Do not re-add Gemini as a data processor.

## Current state (as of 2026-05-04)
- Phase 1 complete: Claude wired in via `claude_session.py`, `USE_GEMINI_LIVE = False`
- `gemini_tts_stream.py` still used for STT/TTS — **pending replacement with `local_audio.py`**
- Phase 2–6 not yet started (see `docs/PLAN.md` and `docs/CONTRIBUTING.md`)

## Key files to understand first
1. `hub/backend/claude_session.py` — how we talk to Claude
2. `hub/backend/persona.py` — persona/memory file system
3. `hub/backend/app.py` — main FastAPI server (large; navigate by function)
4. `firmware/src/main.cpp` — entire ESP32 program

## Compliance
The org has a BAA with Anthropic. PHI may pass through conversations. Only Claude (text) may touch the network. All audio processing must be local. Never suggest adding cloud STT/TTS without explicit BAA confirmation.

## Docs
- Architecture and decisions: `docs/PLAN.md`
- Concept explanations: `docs/CONCEPTS.md`
- Getting started: `docs/ONBOARDING.md`
- What to work on: `docs/CONTRIBUTING.md`
- Hardware BOM: `docs/parts-list.md`
- Audio stack decision: `docs/local-audio-recommendation.md`
