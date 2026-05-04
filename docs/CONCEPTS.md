# Concepts Guide

This document explains the key technologies in Project Pixel. You don't need to master all of these before contributing — but reading through this once will make the codebase make a lot more sense.

---

## Table of Contents

1. [Large Language Models (LLMs)](#1-large-language-models-llms)
2. [The Claude API](#2-the-claude-api)
3. [System Prompts and Persona](#3-system-prompts-and-persona)
4. [Tool Use (Function Calling)](#4-tool-use-function-calling)
5. [Speech-to-Text (STT) and Whisper](#5-speech-to-text-stt-and-whisper)
6. [Text-to-Speech (TTS) and MLX-Audio](#6-text-to-speech-tts-and-mlx-audio)
7. [WebSockets](#7-websockets)
8. [FastAPI and Async Python](#8-fastapi-and-async-python)
9. [Docker](#9-docker)
10. [ESP32 Firmware and PlatformIO](#10-esp32-firmware-and-platformio)
11. [HIPAA, BAA, and Why It Matters Here](#11-hipaa-baa-and-why-it-matters-here)

---

## 1. Large Language Models (LLMs)

An LLM is a neural network trained on a massive amount of text. Through that training it learns patterns in language — well enough that it can predict what a useful, coherent response to any input would look like.

**The key insight:** LLMs don't "know" things the way a database does. They generate probable next tokens (words/word-pieces) given everything that came before. The reason Claude gives thoughtful answers is because thoughtful answers appear frequently in the context of thoughtful questions in its training data.

**What this means in practice:**
- The same question asked twice can get different answers (probabilistic)
- The model is sensitive to how you phrase things (hence "prompt engineering")
- Context matters enormously — everything in the conversation window influences the output
- There's a context window limit — a maximum amount of text the model can "see" at once

**Where this shows up in our code:**
`hub/backend/claude_session.py` — we maintain a rolling history of the last 20 conversation turns per device and send them all with every request, so Claude remembers the conversation.

---

## 2. The Claude API

The Claude API is how we talk to Claude programmatically. Instead of using the chat.claude.ai website, we send HTTP requests to Anthropic's servers and get responses back as JSON.

**The basic request:**
```python
import anthropic

client = anthropic.AsyncAnthropic(api_key="your-key")

response = await client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are Pixel, a friendly desk assistant.",  # personality
    messages=[
        {"role": "user", "content": "What's the weather like?"},
    ]
)

print(response.content[0].text)  # Claude's reply
```

**Key concepts:**
- **`model`** — which version of Claude to use. `claude-sonnet-4-6` is the main one we use; it's fast and capable.
- **`system`** — the system prompt (see section 3). This is where we inject personality and memory.
- **`messages`** — the conversation history. A list of alternating user/assistant turns.
- **`max_tokens`** — maximum length of the response. Tokens are roughly ¾ of a word on average.

**API keys and billing:**
Each request costs a small amount based on how many tokens are sent and received. For a desk assistant with typical conversational use, $5 of credit lasts months. Each user has their own key — their conversations never touch anyone else's account.

**Where this shows up in our code:**
`hub/backend/claude_session.py` → `ClaudeSession.send_message()`

---

## 3. System Prompts and Persona

The **system prompt** is a special message that sets the stage for every conversation. It's not part of the conversation history — it's more like standing instructions that Claude reads before every reply.

This is how we give Pixel its personality, inject the user's memory, and describe what tools are available.

**Our system prompt is built from several files (in `hub/backend/persona_defaults/`):**

| File | Purpose |
|---|---|
| `SOUL.md` | Core personality — tone, communication style, values |
| `IDENTITY.md` | Who Pixel is — name, role, what it's for |
| `USER.md` | Who the *human* is — filled in during onboarding |
| `MEMORY.md` | Durable facts Claude should always remember |
| `AGENTS.md` | Behavioral guidelines for how to act |
| `HEARTBEAT.md` | Periodic self-reflection and memory consolidation checklist |

**Why files instead of hardcoded strings?**
Because they can be edited at runtime. If a user says "be more concise," Claude can update `SOUL.md` directly. If the user shares something important, it goes into `MEMORY.md`. The persona evolves over time without any code changes.

**Where this shows up in our code:**
`hub/backend/persona.py` → `build_composed_system_instruction()` assembles all these files into one big system prompt before each Claude call.

---

## 4. Tool Use (Function Calling)

LLMs are great at text, but what if you want Claude to actually *do* something — like change the face animation on the display, or save a fact to memory?

**Tool use** solves this. You define a set of functions Claude is allowed to call, describe what they do in plain English, and Claude decides when to call them as part of its response.

**Example — face animation:**
```python
# We tell Claude a tool exists:
{
    "name": "face_animation",
    "description": "Animates Pixel's face. Use for emotional or conversational states.",
    "input_schema": {
        "type": "object",
        "properties": {
            "animation": {
                "type": "string",
                "enum": ["happy", "sad", "thinking", "excited", ...]
            }
        }
    }
}

# Claude decides to call it:
# User: "That's great news!"
# Claude calls: face_animation(animation="excited")
# Our code receives that, sends a WebSocket message to the ESP32
# The ESP32 displays the excited face animation
# Then Claude continues with its text response
```

**The flow for a tool call:**
1. Claude responds with `stop_reason: "tool_use"` instead of `"end_turn"`
2. Our code extracts the tool name and arguments
3. We run the actual function (update a file, send a WebSocket message, etc.)
4. We send the result back to Claude as a `tool_result` message
5. Claude finishes its response

**Where this shows up in our code:**
`hub/backend/claude_session.py` → the tool use loop in `send_message()`
`hub/backend/app.py` → `_execute_claude_tool()` — runs the actual tool functions
`hub/backend/pixel_tool_declarations.py` — tool definitions

---

## 5. Speech-to-Text (STT) and Whisper

**The problem:** The ESP32 captures raw PCM audio (just a stream of numbers representing air pressure over time). Claude can only read text. Something needs to convert between them.

**Speech-to-Text (STT)** is the process of turning audio into a text transcript.

**Whisper** is an open-source STT model from OpenAI, released under the MIT license. It runs entirely locally — no internet required, no API key, no cost per use. On Apple Silicon Macs it runs efficiently using the Neural Engine.

```python
import whisper

model = whisper.load_model("base")  # ~74MB model file
result = model.transcribe("audio.wav")
print(result["text"])  # "Hey Pixel, what's on my calendar today?"
```

**Why local matters:**
If we used a cloud STT service (Google, AWS, etc.), every word the user speaks would be uploaded to that company's servers. For our use case with sensitive work conversations, that's not acceptable. Whisper runs on your Mac, processes audio locally, and nothing leaves the machine.

**MLX-Audio alternative:**
On Apple Silicon Macs, `mlx-audio` provides an even faster STT option using Apple's Metal GPU acceleration. We auto-detect which is available at startup.

**Where this shows up in our code:**
`hub/backend/gemini_tts_stream.py` → `transcribe_audio()` (currently Gemini, being replaced)
Future: `hub/backend/local_audio.py` → `transcribe_audio()` using Whisper/MLX

---

## 6. Text-to-Speech (TTS) and MLX-Audio

**The problem:** Claude responds with text. Pixel needs to speak out loud.

**Text-to-Speech (TTS)** converts text into audio waveforms. The challenge is making it sound natural — not like a 1990s GPS.

**Modern neural TTS** (what we're using) works by running a neural network that was trained on thousands of hours of human speech. The output is indistinguishable from a real person's voice.

**Our stack:**
- **MLX-Audio** (primary, Apple Silicon): Uses Apple's MLX framework with Metal GPU acceleration. Under 500ms latency for conversational-length responses. Multiple voice options.
- **Kokoro-ONNX** (fallback, any Mac): 82M parameter model, 54 voice presets, runs on CPU.

```python
# Example with mlx-audio
from mlx_audio.tts import TTS

tts = TTS(model="kokoro")
audio = tts.generate("Hello, I'm Pixel. How can I help you today?", voice="casual_female")
# audio is a numpy array of PCM samples, ready to play or stream
```

**The audio pipeline:**
1. TTS generates raw PCM audio (just numbers — 24,000 samples per second)
2. We base64-encode it and broadcast it as a WebSocket message
3. The browser dashboard receives it and plays it through your Mac's speakers
4. (Phase 4) We'll also stream it to the ESP32's speaker via the MAX98357A amp

**Where this shows up in our code:**
`hub/backend/gemini_tts_stream.py` → `text_to_pcm()` (currently Gemini, being replaced)
Future: `hub/backend/local_audio.py` → `text_to_pcm()`

---

## 7. WebSockets

Most web communication is **request/response**: your browser asks for something, the server replies, connection closes. This works for loading web pages but is terrible for real-time communication — like streaming audio from a microphone.

**WebSockets** keep a connection open permanently. Either side can send a message at any time without the other side having to ask first. Think of it like a phone call instead of sending letters.

**In Project Pixel, WebSockets do everything real-time:**

```
ESP32                          Hub Mac                      Browser Dashboard
  │                               │                               │
  │── connect to /ws/stream ─────►│                               │
  │                               │◄──── connect to /ws ─────────│
  │                               │                               │
  │── [binary] PCM audio ────────►│                               │
  │                               │── [JSON] audio_captured ─────►│
  │                               │                               │
  │                               │── [JSON] live_transcription ──►│
  │                               │                               │
  │◄── [JSON] wake_processing ────│                               │
  │                               │                               │
  │◄── [JSON] gemini_first_token ─│                               │
  │   (triggers thinking face)    │                               │
  │                               │── [JSON] ai_response_delta ──►│
  │                               │                               │
  │◄── [JSON] status: success ────│                               │
  │   (displays reply text)       │── [JSON] live_audio_chunk ───►│
  │                               │   (browser plays audio)       │
```

**Binary vs JSON messages:**
- The ESP32 sends **binary** packets (raw PCM bytes with a 1-byte type prefix)
- The hub communicates with the browser dashboard using **JSON text** messages

**Where this shows up in our code:**
`hub/backend/app.py` → `esp32_stream_endpoint()` (handles ESP32 connection)
`hub/backend/app.py` → `websocket_endpoint()` (handles browser dashboard connection)
`firmware/src/main.cpp` → `webSocketEvent()` (ESP32 side)

---

## 8. FastAPI and Async Python

**FastAPI** is the Python web framework powering the hub. It handles:
- HTTP API routes (settings, persona management, etc.)
- WebSocket connections (ESP32 and browser)
- Background tasks (heartbeat, presence detection)

**Why async?**
Traditional Python code runs one thing at a time. `async/await` lets Python switch between tasks while one is waiting — like waiting for the Claude API to respond. Without async, the whole server would freeze every time we made an API call.

```python
# Sync (bad for a server — blocks everything while waiting)
response = claude_client.messages.create(...)  # server frozen for 1-2 seconds

# Async (good — server handles other connections while waiting)
response = await claude_client.messages.create(...)  # yields control, resumes when ready
```

**Key patterns you'll see in `app.py`:**
- `async def` — an async function
- `await` — pause here until this finishes, but let other things run
- `asyncio.create_task()` — start something in the background without waiting
- `asyncio.Lock()` — prevent two requests from running the same code simultaneously

**Where this shows up in our code:**
`hub/backend/app.py` — the entire server
`hub/backend/claude_session.py` — `async def send_message()`

---

## 9. Docker

**The problem:** "Works on my machine" — software that runs fine on your Mac but fails on someone else's because they have a different Python version, missing libraries, or wrong environment variables.

**Docker** packages your application and everything it needs (Python version, libraries, config) into a single **container** — a self-contained unit that runs identically on any machine that has Docker installed.

**Key concepts:**
- **Dockerfile** — the recipe for building the container (what to install, what to copy in)
- **docker-compose.yml** — how to *run* the container (ports, environment variables, volumes)
- **Volume** — a folder shared between the container and your Mac, so data persists when the container restarts

```bash
# This one command starts the entire hub:
docker compose up

# Equivalent to: install Python 3.11, install 20+ packages, configure everything, start server
```

**Why this matters for gift recipients:**
We can give them one command to paste into Terminal. Docker handles everything else — they don't need to know what Python or pip are.

**Where this shows up:**
`Dockerfile` — builds the hub image
`docker-compose.yml` — runs it with the right settings

---

## 10. ESP32 Firmware and PlatformIO

**The ESP32** is a tiny, cheap microcontroller chip. The XIAO ESP32-S3 Sense we're using is roughly the size of a thumb drive and contains:
- A dual-core processor running at 240MHz
- 8MB of RAM
- Wi-Fi and Bluetooth radios
- A camera interface
- A PDM microphone

**Firmware** is the program that runs directly on the hardware — there's no operating system in between. It's written in C++ and compiled for the specific chip.

**PlatformIO** is the tool we use to write, compile, and flash firmware. It's a VS Code extension that handles all the toolchain complexity.

```
Write C++ → PlatformIO compiles → Binary file → USB flash → Runs on ESP32
```

**Key things the firmware does:**
- Connects to Wi-Fi (using stored credentials, or captive portal on first boot)
- Opens a WebSocket connection to the hub Mac
- Reads microphone audio via I2S and sends it to the hub
- Receives messages from the hub and updates the display
- Renders face animations on the round screen

**Why C++ instead of Python/JavaScript?**
Microcontrollers have no OS, very limited RAM (8MB total), and need deterministic timing. C++ gives direct control over memory and hardware registers. Python would be too slow and memory-hungry.

**Where this shows up:**
`firmware/src/main.cpp` — the entire ESP32 program (3,600+ lines)
`firmware/platformio.ini` — build configuration (target chip, libraries)

---

## 11. HIPAA, BAA, and Why It Matters Here

**HIPAA** (Health Insurance Portability and Accountability Act) is a US law that sets rules for handling Protected Health Information (PHI) — health records, diagnoses, treatment details, and anything that could identify a patient.

**Why this matters for Pixel:**
Our org has teams that handle PHI. If someone uses Pixel for work and a health-related topic comes up in conversation, that conversation could contain PHI. Any AI service processing that data needs to be HIPAA compliant.

**Business Associate Agreement (BAA):**
A BAA is a legal contract between your org and an AI/cloud provider. It says the provider will handle your data in a HIPAA-compliant way, and they're legally liable if they don't. Our org has a BAA with Anthropic (Claude).

**What this means for our architecture:**

| Component | Data it sees | Compliant? | Why |
|---|---|---|---|
| Claude API | Text transcripts | ✅ Yes | Covered by org BAA |
| Whisper (local) | Raw audio | ✅ Yes | Never leaves the Mac |
| MLX-Audio TTS (local) | Claude's text response | ✅ Yes | Never leaves the Mac |
| Gemini API | ❌ Would see audio + text | ❌ No | No BAA on free tier |

**The rule of thumb:** If it's local, it's safe. If it's a cloud API, there must be a BAA.

This is why we replaced Gemini STT/TTS with local processing — not just a technology preference, but a compliance requirement.
