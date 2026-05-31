import os
import math
import requests
import fal_client
import config

os.environ["FAL_KEY"] = config.FAL_API_KEY

STABLE_AUDIO_MODEL = "fal-ai/stable-audio"
CLIP_DURATION = 44  # seconds per generation (stable-audio max ~47s)


def generate_music(prompt: str, target_duration: float) -> bytes:
    """Generate looping nursery rhyme music to match target video duration."""
    result = fal_client.subscribe(
        STABLE_AUDIO_MODEL,
        arguments={
            "prompt": prompt,
            "seconds_total": CLIP_DURATION,
            "steps": 100,
        },
    )

    audio_url = result["audio_file"]["url"]
    audio_bytes = requests.get(audio_url).content

    if target_duration <= CLIP_DURATION:
        return audio_bytes

    return _loop_to_duration(audio_bytes, target_duration)


def _loop_to_duration(audio_bytes: bytes, target_seconds: float) -> bytes:
    """Use pydub to loop the audio clip to target_seconds with a fade-out."""
    from pydub import AudioSegment
    import io

    segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
    target_ms = int(target_seconds * 1000)

    n = math.ceil(target_ms / len(segment))
    looped = segment * n
    looped = looped[:target_ms].fade_out(min(3000, target_ms // 6))

    buf = io.BytesIO()
    looped.export(buf, format="mp3")
    return buf.getvalue()
