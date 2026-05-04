# Local Audio Stack — Recommendation

## Why Local (No Cloud TTS/STT)

The project involves organization-specific skills, sensitive documentation, Gmail integration, and potential PHI. A BAA exists with Anthropic (Claude API) but **not** with Google (Gemini). Running STT and TTS locally means:

- Audio never leaves the Mac
- Only text touches the network (via Claude API, covered by BAA)
- Recipients need one API key only (Claude)
- No per-request cost for audio processing

---

## Recommended Architecture

```
[ESP32 mic] ──PCM──► [Hub Mac]
                         │
                    STT (local)
                         │
                      text ──► Claude API (BAA) ──► text
                         │
                    TTS (local)
                         │
                    PCM audio ──► browser dashboard speaker
                              ──► (Phase 4) ESP32 speaker
```

---

## Two-Tier Implementation

### Tier 1 — Apple Silicon (Primary)
**Library**: `mlx-audio`
Uses Apple's MLX framework with Metal acceleration. Handles both STT and TTS in a single library — no separate Whisper install needed.

| Capability | Model | Notes |
|---|---|---|
| STT | Mistral streaming via MLX | <5% CPU, real-time |
| TTS | Kokoro or Qwen3-TTS via MLX | <500ms latency for conversational phrases |
| Voices | casual_male, casual_female, cheerful_female, neutral_male, neutral_female + multilingual | |
| Install | `pip install mlx-audio` | |
| Requires | Apple Silicon (M1/M2/M3/M4) | |

### Tier 2 — Fallback (Intel Mac or MLX unavailable)
**Libraries**: `openai-whisper` (STT) + `kokoro-onnx` (TTS)
CPU-based via ONNX Runtime. Works on any Mac.

| Capability | Library | Notes |
|---|---|---|
| STT | openai-whisper | Runs on CPU, good accuracy |
| TTS | kokoro-onnx | 54 voice presets, 8 languages |
| Install | `pip install openai-whisper kokoro-onnx soundfile` + `brew install espeak` | |
| Requires | Python 3.11 or 3.12 (not 3.13) | |

### Auto-detection at hub startup
```python
try:
    import mlx.core
    # Apple Silicon path
    USE_MLX_AUDIO = True
except ImportError:
    # Fallback path
    USE_MLX_AUDIO = False
```

---

## Voice Options

| Engine | Voice Count | Standout Feature |
|---|---|---|
| Kokoro (ONNX) | 54 presets | Best quality-to-speed on CPU |
| Qwen3-TTS (via MLX) | 9 presets + voice design | Describe a voice in plain English |
| Piper TTS | Hundreds | Fastest latency, most accent variety |
| macOS `say` | ~20 (varies by OS version) | Zero install, always available as last resort |

**Voice design** (Qwen3-TTS via MLX) is worth noting: instead of picking a preset you can describe characteristics — e.g. "calm, warm, conversational" — giving effectively unlimited voice options.

---

## What This Replaces

| Previous | Replacement | Reason |
|---|---|---|
| `gemini_tts_stream.transcribe_audio()` | MLX-Audio STT or Whisper | No BAA on Gemini API |
| `gemini_tts_stream.text_to_pcm()` | MLX-Audio TTS or Kokoro-ONNX | No BAA on Gemini API |
| `GEMINI_API_KEY` env var | Removed entirely | Not needed |

---

## Implementation File

**`hub/backend/local_audio.py`** — replaces `gemini_tts_stream.py`

Functions to implement:
- `transcribe_audio(wav_bytes) -> str` — STT, returns transcript text
- `text_to_pcm(text, voice=None) -> bytes` — TTS, returns raw 24kHz PCM
- `list_voices() -> list[str]` — enumerate available voices for settings UI

---

## Other Options Evaluated

| Option | Verdict |
|---|---|
| **Ollama** | LLM inference only — no TTS capability. Can be paired with external TTS but adds complexity for no gain. |
| **Chatterbox-Turbo** | Strong quality, 350M params, very fast (one-step decoder). Good alternative to Kokoro if voice expressiveness is a priority. |
| **Piper TTS** | Best raw latency and most voice variety. Less expressive than Kokoro. Good option if latency is the top priority. |
| **Bark** | Best audio quality of any local model. Too slow for real-time conversation (not suitable). |
| **macOS `say`** | Zero-install fallback. Quality is adequate but noticeably robotic vs neural models. |
| **ElevenLabs** | Has BAA on Business plan but adds cost and cloud dependency. Not needed given local options. |

---

## References

- [MLX-Audio — GitHub](https://github.com/Blaizzy/mlx-audio)
- [Kokoro-82M — Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M)
- [kokoro-onnx — GitHub](https://github.com/thewh1teagle/kokoro-onnx)
- [Piper TTS — GitHub](https://github.com/rhasspy/piper)
- [Qwen3-TTS with MLX-Audio — myByways](https://mybyways.com/blog/qwen3-tts-with-mlx-audio-on-macos)
- [Best Local TTS Models 2026 — Murmur](https://www.murmurtts.com/blog/best-local-tts-models-2026)
- [6 Best On-Device TTS Models — Medium](https://medium.com/@amosgyamfi/the-6-best-on-device-tts-models-for-voice-ai-d9ae478d3878)
