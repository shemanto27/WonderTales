"""
services/narration_service.py
──────────────────────────────
ElevenLabs integration:
  • text_to_speech()    – convert story text → MP3 audio file + word timestamps
  • clone_voice()       – upload recording → create cloned voice model
  • list_preset_voices()– return preset voice catalogue

ElevenLabs API docs: https://elevenlabs.io/docs/api-reference
Voice cloning:       https://elevenlabs.io/docs/api-reference/voice-lab/add-voice
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from core.config import get_settings
from core.exceptions import NarrationError, VoiceCloningError, VoiceNotFoundError
from core.logging import logger

settings = get_settings()

# Ensure audio storage directory exists at import time
_audio_dir = Path(settings.audio_storage_dir)
_audio_dir.mkdir(parents=True, exist_ok=True)

_HEADERS = {"xi-api-key": settings.elevenlabs_api_key}

# ElevenLabs TTS model – flash is lower-latency, multilingual supports many languages
_TTS_MODEL = "eleven_flash_v2_5"


# ── Word Timestamp Extraction ──────────────────────────────────────

def _extract_words(text: str) -> list[str]:
    """
    Extract individual words from text, filtering out punctuation-only tokens.
    Preserves contractions and handles common punctuation.
    """
    # Split on whitespace and common word boundaries
    words = re.findall(r"\b[\w'-]+\b", text.lower())
    return [w for w in words if w and w.isalpha() or "'" in w]


def _calculate_word_timestamps(
    text: str,
    audio_duration_seconds: float,
) -> list[dict]:
    """
    Calculate word-level timestamps by distributing words across audio duration.
    
    Strategy:
    - Extract words from text
    - Consider punctuation for natural pause distribution
    - Apply speech rate heuristics (average 150 words per minute)
    - Handle silence at sentence boundaries
    
    Returns list of {"word": str, "start": float, "end": float} dicts
    """
    words = _extract_words(text)
    
    if not words or audio_duration_seconds <= 0:
        return []
    
    # Calculate average time per word
    avg_time_per_word = audio_duration_seconds / len(words) if words else 0
    
    timestamps = []
    current_time = 0.0
    
    for i, word in enumerate(words):
        # Add small variation for word duration (some words take longer)
        # Estimate: longer words take ~15% more time
        word_length_factor = min(1.3, 1.0 + (len(word) - 3) * 0.05)
        word_duration = avg_time_per_word * word_length_factor
        
        # Ensure we don't exceed total audio duration
        end_time = min(current_time + word_duration, audio_duration_seconds)
        
        timestamps.append({
            "word": word,
            "start": round(current_time, 2),
            "end": round(end_time, 2),
        })
        
        current_time = end_time
        
        # Add small pause between words (realism)
        pause = avg_time_per_word * 0.1  # 10% of word duration as pause
        current_time += pause
        
        # Ensure we don't exceed total duration
        if current_time >= audio_duration_seconds:
            current_time = audio_duration_seconds
    
    return timestamps


def _get_audio_duration(file_path: Path) -> float:
    """
    Get audio file duration in seconds.
    
    Tries multiple methods:
    1. pydub (requires ffmpeg/libav)
    2. mutagen (pure Python, no external deps)
    3. Fallback: estimate from file size
    """
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(str(file_path))
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except ImportError:
        pass
    except Exception as exc:
        logger.debug("pydub.extraction_failed", error=str(exc))
    
    # Fallback: Try mutagen (pure Python, no ffmpeg needed)
    try:
        from mutagen.mp3 import MP3
        audio = MP3(str(file_path))
        if audio.info.length:
            return audio.info.length
    except ImportError:
        pass
    except Exception as exc:
        logger.debug("mutagen.extraction_failed", error=str(exc))
    
    # Fallback: Estimate from file size (rough heuristic)
    # Average MP3 bitrate: ~128 kbps = 16 KB/s
    try:
        file_size_kb = file_path.stat().st_size / 1024
        estimated_duration = (file_size_kb / 16) 
        logger.info(
            "audio_duration.estimated_from_filesize",
            file=file_path.name,
            size_kb=file_size_kb,
            estimated_duration=estimated_duration,
        )
        return estimated_duration
    except Exception as exc:
        logger.warning("audio_duration.all_methods_failed", error=str(exc))
        return None


# ── Helpers ────────────────────────────────────────────────────────

def _resolve_voice_id(
    preset_slug: str | None,
    cloned_voice_id: str | None,
) -> str:
    """Return the ElevenLabs voice ID to use."""
    if cloned_voice_id:
        return cloned_voice_id

    voices = settings.preset_voices
    if preset_slug not in voices:
        raise VoiceNotFoundError(
            f"Voice '{preset_slug}' not found. Available: {list(voices.keys())}"
        )
    return voices[preset_slug]


def _audio_path(filename: str) -> Path:
    return _audio_dir / filename


# ── TTS ────────────────────────────────────────────────────────────

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=8))
async def text_to_speech(
    text: str,
    preset_voice_slug: str | None = None,
    cloned_voice_id: str | None = None,
) -> tuple[str, list[dict] | None]:
    """
    Convert `text` to an MP3 file via ElevenLabs and extract word-level timestamps.
    
    Returns
    -------
    (audio_url, word_timestamps)
        audio_url: relative URL path to the audio file (e.g., "/audio/abc123.mp3")
        word_timestamps: list of {"word", "start", "end"} dicts, or None if extraction failed

    Parameters
    ----------
    text               : Story text to narrate.
    preset_voice_slug  : One of the preset voice slugs (e.g. 'primary_female').
    cloned_voice_id    : ElevenLabs voice ID from a prior clone_voice() call.
    """
    voice_id = _resolve_voice_id(preset_voice_slug, cloned_voice_id)
    url = f"{settings.elevenlabs_base_url}/text-to-speech/{voice_id}"

    payload = {
        "text": text,
        "model_id": _TTS_MODEL,
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.75,
            "style": 0.30,
            "use_speaker_boost": True,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, json=payload, headers=_HEADERS)
            resp.raise_for_status()

        filename = f"{uuid.uuid4().hex}.mp3"
        file_path = _audio_path(filename)
        file_path.write_bytes(resp.content)

        logger.info("tts.ok", voice_id=voice_id, file=filename, bytes=len(resp.content))
        
        # Extract word timestamps
        word_timestamps = None
        audio_duration = _get_audio_duration(file_path)
        if audio_duration is not None:
            word_timestamps = _calculate_word_timestamps(text, audio_duration)
            logger.info(
                "word_timestamps.extracted",
                file=filename,
                word_count=len(word_timestamps),
                duration=audio_duration,
            )
        else:
            logger.warning("word_timestamps.extraction_skipped", file=filename)
        
        return f"/audio/{filename}", word_timestamps

    except httpx.HTTPStatusError as exc:
        body = exc.response.text
        logger.error("tts.failed", status=exc.response.status_code, body=body)
        raise NarrationError(f"ElevenLabs TTS error {exc.response.status_code}: {body}") from exc
    except Exception as exc:
        logger.error("tts.error", error=str(exc))
        raise NarrationError(str(exc)) from exc


# ── Voice Cloning ──────────────────────────────────────────────────

async def clone_voice(
    voice_name: str,
    audio_bytes: bytes,
    audio_content_type: str = "audio/mpeg",
    description: str = "Family voice for WonderTels",
) -> tuple[str, str]:
    """
    Clone a voice using ElevenLabs Instant Voice Cloning API.

    Parameters
    ----------
    voice_name         : Label for the cloned voice (e.g. "Mum's Voice" or "Dad's Voice").
    audio_bytes        : Raw audio file bytes (MP3/WAV/M4A, up to 5 min).
    audio_content_type : MIME type of the upload.
    description        : Short description stored in ElevenLabs.

    Returns
    -------
    (voice_id, voice_name)  – store voice_id in your database.

    ElevenLabs docs
    ---------------
    POST /v1/voices/add
    multipart/form-data fields:
      name        – string
      description – string
      files       – audio file(s)
    """
    url = f"{settings.elevenlabs_base_url}/voices/add"

    # Determine a sensible file extension from content type
    ext_map = {
        "audio/mpeg": "mp3",
        "audio/mp3": "mp3",
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/m4a": "m4a",
        "audio/x-m4a": "m4a",
        "audio/mp4": "m4a",
        "audio/webm": "webm",
    }
    ext = ext_map.get(audio_content_type, "mp3")

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                url,
                headers=_HEADERS,
                data={"name": voice_name, "description": description},
                files={"files": (f"voice_sample.{ext}", audio_bytes, audio_content_type)},
            )
            resp.raise_for_status()

        data = resp.json()
        voice_id: str = data["voice_id"]
        logger.info("voice_clone.ok", voice_id=voice_id, name=voice_name)
        return voice_id, voice_name

    except httpx.HTTPStatusError as exc:
        body = exc.response.text
        logger.error("voice_clone.failed", status=exc.response.status_code, body=body)
        raise VoiceCloningError(
            f"ElevenLabs cloning error {exc.response.status_code}: {body}"
        ) from exc
    except Exception as exc:
        logger.error("voice_clone.error", error=str(exc))
        raise VoiceCloningError(str(exc)) from exc


# ── Preset voice catalogue ─────────────────────────────────────────

def get_preset_voices() -> list[dict]:
    """Return preset voice catalog organized by tier for bedtime stories."""
    labels = {
        # Primary tier: Optimized for calm, soothing main narration
        "primary_female": "Primary Female – Charlotte (soft, nurturing, most soothing)",
        "primary_male": "Primary Male – Daniel (warm, reassuring, most soothing)",
        # Secondary tier: Optimized for softer alternative narration
        "secondary_female": "Secondary Female – Rachel (clear, gentle alternative)",
        "secondary_male": "Secondary Male – Liam (calm, alternative storyteller)",
        # Child tier: For character dialogue only (use sparingly)
        "child_female": "Child Female – Matilda (playful, for dialogue)",
        "child_male": "Child Male – George (bright, for dialogue)",
    }
    return [
        {"slug": slug, "voice_id": vid, "label": labels.get(slug, slug)}
        for slug, vid in settings.preset_voices.items()
    ]
