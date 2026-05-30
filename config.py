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
