# Project Pixel 🤖

A personalized, open-source AI desk assistant built on real hardware. Pixel sits on your desk, wakes up when you say its name, sees through a camera, listens through a microphone, thinks using Claude AI, and talks back through a speaker — all running on a device the size of a hockey puck.

This is a team build project. The goal is to ship ~10 personalized units as gifts **and** to learn how modern AI systems actually work by building one from scratch.

---

## What We're Building

```
         ┌─────────────────────────────────────────────────────┐
         │                    Your Mac                          │
         │                                                      │
         │   ┌──────────────┐      ┌──────────────────────┐    │
         │   │  Hub Backend │      │   Hub Dashboard      │    │
         │   │  (FastAPI)   │      │   (React browser UI) │    │
         │   │              │      │                      │    │
         │   │ • Wake word  │      │ • Live transcript    │    │
         │   │ • Whisper    │      │ • Settings panel     │    │
         │   │   (STT)      │      │ • Audio monitor      │    │
         │   │ • Claude API │◄────►│                      │    │
         │   │   (brain)    │      └──────────────────────┘    │
         │   │ • MLX TTS    │                                   │
         │   │   (voice)    │                                   │
         │   └──────┬───────┘                                   │
         │          │ WebSocket                                 │
         └──────────┼────────────────────────────────────────  ┘
                    │ Wi-Fi (LAN)
              ┌─────▼──────────────────────┐
              │     Pixel Device            │
              │   (XIAO ESP32-S3 Sense)     │
              │                             │
              │ • 1.28" round display       │
              │ • Built-in camera           │
              │ • Built-in microphone       │
              │ • Speaker (Phase 4)         │
              │ • Animated face             │
              └─────────────────────────────┘
```

**The device is dumb. The Mac is smart.** The ESP32 handles display, camera, mic, and Wi-Fi. All the AI reasoning happens on the Mac and streams back in real time.

---

## What You'll Learn

This project touches a wide range of modern software and AI concepts. By the time we ship, you'll have hands-on experience with:

| Area | What we use | What you'll understand |
|---|---|---|
| AI / LLMs | Claude API | How language models work, system prompts, tool use, memory |
| Speech | Whisper (STT), MLX-Audio (TTS) | How speech recognition and synthesis work locally |
| Embedded | ESP32-S3, PlatformIO, C++ | Microcontroller firmware, Wi-Fi, WebSocket clients |
| Backend | Python, FastAPI, asyncio | Async web servers, WebSocket handlers, real-time streaming |
| Frontend | React, Vite | Dashboard UI, live WebSocket feeds |
| Infra | Docker | Containerized services, environment management |
| Compliance | HIPAA, BAA | Why data residency matters in AI systems |

No prior experience with any of these is required — the docs explain each one as we go.

---

## Project Status

| Phase | What | Status |
|---|---|---|
| **Phase 1** | Claude brain wired in, Gemini replaced | ✅ Done |
| **Phase 2** | Captive portal Wi-Fi setup on ESP32 | 🔲 Next |
| **Phase 3** | Onboarding interview (Pixel learns who you are) | 🔲 Planned |
| **Phase 4** | Enclosure design + speaker hardware | 🔲 Planned |
| **Phase 5** | Per-recipient personalization + batch flash | 🔲 Planned |
| **Phase 6** | Setup guide + welcome cards | 🔲 Planned |

---

## Repo Structure

```
project_pixel/
│
├── omnibot/              ← Upstream OmniBot source (READ ONLY — do not edit)
│                           This is the open-source project we're building on top of.
│                           Keep it intact so we can reference the original at any time.
│
├── hub/
│   ├── backend/          ← Python FastAPI server (the "brain" of the system)
│   │   ├── app.py            Main server — WebSocket handler, API routes
│   │   ├── claude_session.py Our addition — Claude API conversation manager
│   │   ├── gemini_tts_stream.py Placeholder — being replaced by local_audio.py
│   │   ├── persona.py        Persona/memory file management (SOUL, USER, MEMORY)
│   │   ├── wake_listen.py    Wake word detection + audio buffer management
│   │   └── hub_config.py     API key management, data directory config
│   │
│   └── frontend/         ← React dashboard (runs in your browser)
│       └── src/
│           └── App.jsx       Main dashboard UI
│
├── firmware/             ← ESP32-S3 C++ firmware (PlatformIO)
│   └── src/
│       └── main.cpp          Everything the device does — display, mic, Wi-Fi, WebSocket
│
├── personas/             ← Per-recipient persona configs (one folder per person)
│
├── enclosure/            ← 3D print files (STL/STEP from official Pixel build)
│   └── stl/
│
├── docs/                 ← All project documentation
│   ├── PLAN.md               Full phased build plan
│   ├── CONCEPTS.md           Learn: LLMs, APIs, WebSockets, STT/TTS, Docker
│   ├── ONBOARDING.md         How to get your dev environment set up
│   ├── CONTRIBUTING.md       How we work together as a team
│   ├── parts-list.md         Hardware BOM with prices and links
│   └── local-audio-recommendation.md  Why we chose local STT/TTS
│
├── tools/                ← Helper scripts (flash firmware, generate personas)
├── Dockerfile            ← Builds the hub as a Docker container
└── docker-compose.yml    ← Runs the hub with one command
```

---

## Quick Links

| I want to... | Go to |
|---|---|
| Understand the AI concepts | [docs/CONCEPTS.md](docs/CONCEPTS.md) |
| Set up my dev environment | [docs/ONBOARDING.md](docs/ONBOARDING.md) |
| See the full build plan | [docs/PLAN.md](docs/PLAN.md) |
| Know what to work on | [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) |
| Understand why we built it this way | [docs/design-principles.md](docs/design-principles.md) |
| Order hardware | [docs/parts-list.md](docs/parts-list.md) |
| Understand the audio stack | [docs/local-audio-recommendation.md](docs/local-audio-recommendation.md) |

---

## Getting Started

Clone the repo, then add the upstream OmniBot reference locally (it is gitignored — not tracked in our repo):

```bash
git clone https://github.com/pcasa/pixel-project
cd pixel-project
git clone https://github.com/nazirlouis/OmniBot omnibot
```

Then follow [docs/ONBOARDING.md](docs/ONBOARDING.md) to set up your dev environment.

---

## The Base Project

Project Pixel is built on top of [OmniBot](https://github.com/nazirlouis/OmniBot) by Naz Louis — an open-source AI desk companion. The original YouTube build video: [I Made Cute Robots For Your Desk](https://www.youtube.com/watch?v=uG98Q4yfBS8).

We've forked and modified it to:
- Replace Gemini AI with Claude (better reasoning, and we have a BAA for HIPAA compliance)
- Replace cloud STT/TTS with local processing (Whisper + MLX-Audio — no audio leaves the Mac)
- Replace BLE Wi-Fi provisioning with a captive portal (simpler for gift recipients)
- Add a first-run onboarding interview (Pixel learns who you are)
- Pre-personalize each unit before shipping

---

## Hardware

Each unit is built from:
- **Seeed Studio XIAO ESP32-S3 Sense** — the microcontroller, with built-in camera and microphone
- **Seeed Round Display for XIAO** — the 1.28" circular touchscreen
- **MAX98357A I2S Amp** + **Waveshare 8Ω 2W speaker** — audio output
- **USB-C power** — always plugged in, no battery
- **3D printed enclosure** — using official STL files from the original Pixel build (~$15 from Patreon)

Full parts list with prices and links: [docs/parts-list.md](docs/parts-list.md)
