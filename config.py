import os
import json
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
YOUTUBE_CHANNEL_ID = os.environ["YOUTUBE_CHANNEL_ID"]
YOUTUBE_CLIENT_SECRET = json.loads(os.environ["YOUTUBE_CLIENT_SECRET_JSON"])
YOUTUBE_TOKEN = os.environ.get("YOUTUBE_TOKEN_JSON", "")

ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel — warm, clear narration

# Locked character descriptions — derived from reference images in assets/
CHARACTER_DESC = """Characters (always draw in Pixar/Disney 3D cartoon style, consistent look every scene):
- TOBIAS: tiny chubby toddler ~2yrs, short platinum-blonde hair, huge bright blue eyes, very round chubby cheeks, small button nose, blue hoodie, grey pants. Always looks happy and curious.
- SAMUEL: boy ~7yrs, much taller than Tobias, golden-blonde hair, confident smile, red t-shirt, dark shorts. Arms often crossed or gesturing. Brave and energetic.
- DAD (occasional): tall man, short brown hair, friendly beard, rust/orange t-shirt, jeans. Warm smile.
- MUM (occasional): woman, short dark hair, round glasses, green cardigan, jeans. Kind loving expression.
All characters share the same bright Pixar 3D animation style. No text or labels in image."""

THEMES = [
    "farm animals making sounds on a sunny day",
    "the alphabet with colorful cartoon characters",
    "counting from 1 to 10 with cute objects",
    "colors of the rainbow with happy characters",
    "ocean animals swimming in the sea",
    "jungle animals in a tropical forest",
    "fruits and vegetables in a garden",
    "vehicles like cars trains and planes",
    "bedtime routine for sleepy animals",
    "weather sunshine rain and rainbows",
    "seasons spring summer autumn winter",
    "body parts head shoulders knees and toes",
]
