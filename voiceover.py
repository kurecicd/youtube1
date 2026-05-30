import requests
import config

ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{config.ELEVENLABS_VOICE_ID}"


def generate_voiceover(text: str) -> bytes:
    response = requests.post(
        ELEVENLABS_URL,
        headers={
            "xi-api-key": config.ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75,
                "style": 0.3,
                "use_speaker_boost": True,
            },
        },
    )
    response.raise_for_status()
    return response.content
