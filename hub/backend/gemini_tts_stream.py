"""
Gemini Flash TTS: convert text to raw PCM audio.

Uses the Gemini generate_content API with AUDIO response modality —
the same underlying TTS engine used by Gemini Live, but as a standalone call
so it works independently of the Live streaming session.

Output format: 24 kHz, 16-bit signed little-endian PCM, mono (same as Live path).
"""

from __future__ import annotations

import asyncio
import base64
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# 24 kHz PCM is what Gemini Live produces; keeping the same rate avoids resampling on playback.
OUTPUT_SAMPLE_RATE = 24_000

# Override with OMNIBOT_TTS_VOICE env var (e.g. Puck, Kore, Charon, Fenrir, Aoede).
_TTS_VOICE_ENV = (os.environ.get("OMNIBOT_TTS_VOICE") or "").strip()
DEFAULT_VOICE_NAME = _TTS_VOICE_ENV if _TTS_VOICE_ENV else "Umbriel"

# TTS model — supports AUDIO response_modalities.
# Falls back to gemini-2.0-flash-exp if the preview name changes.
TTS_MODEL = os.environ.get("OMNIBOT_TTS_MODEL", "gemini-2.0-flash-exp")


def _extract_pcm_from_response(response: object) -> bytes:
    """Pull raw bytes out of a Gemini generate_content response with AUDIO modality."""
    try:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                inline = getattr(part, "inline_data", None)
                if inline is None:
                    continue
                data = getattr(inline, "data", None)
                if not data:
                    continue
                if isinstance(data, bytes):
                    return data
                if isinstance(data, str):
                    return base64.b64decode(data)
    except Exception as e:
        logger.warning("[tts] failed to extract PCM from response: %s", e)
    return b""


async def text_to_pcm(
    genai_client: object,
    text: str,
    *,
    voice_name: str = DEFAULT_VOICE_NAME,
    model: str = TTS_MODEL,
) -> bytes:
    """
    Convert text to raw PCM via Gemini TTS. Returns bytes (may be empty on failure).
    Runs the blocking generate_content call in a thread executor.
    """
    if not text or not text.strip():
        return b""

    from google.genai import types

    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name,
                )
            )
        ),
    )

    try:
        response = await asyncio.to_thread(
            genai_client.models.generate_content,
            model=model,
            contents=text.strip(),
            config=config,
        )
    except Exception as e:
        logger.error("[tts] generate_content failed model=%s: %s", model, e)
        return b""

    pcm = _extract_pcm_from_response(response)
    if not pcm:
        logger.warning("[tts] no audio in response (model=%s, text_len=%d)", model, len(text))
    return pcm


async def transcribe_audio(
    genai_client: object,
    wav_bytes: bytes,
    *,
    model: str = "gemini-2.0-flash",
) -> str:
    """
    Transcribe WAV audio using Gemini. Returns plain text transcript (may be empty on failure).
    """
    if not wav_bytes:
        return ""

    from google.genai import types

    contents = [
        types.Part.from_bytes(data=wav_bytes, mime_type="audio/wav"),
        "Transcribe only what is spoken in this audio. Output just the transcript with no extra commentary.",
    ]

    try:
        response = await asyncio.to_thread(
            genai_client.models.generate_content,
            model=model,
            contents=contents,
        )
        return (response.text or "").strip()
    except Exception as e:
        logger.error("[stt] transcription failed model=%s: %s", model, e)
        return ""
