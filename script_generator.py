import json
import random
import anthropic
import config

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def generate_script() -> dict:
    theme = random.choice(config.THEMES)

    prompt = f"""Generate a 2-3 minute kids nursery rhyme YouTube video script about: {theme}

The main characters are a real family, drawn in Pixar cartoon style:
- TOBIAS — the younger brother (toddler), tiny and round-faced, bright blonde hair, big blue eyes, chubby cheeks, always curious and giggly
- SAMUEL — the older brother (around 7 years old), taller and energetic, blonde hair, brave and playful, loves to lead adventures
- DAD — tall, dark hair, friendly beard, warm and funny
- MUM — dark hair, glasses, kind and loving smile

Tobias and Samuel are always in every scene. Dad and Mum appear occasionally to join the fun or cheer the boys on.

Return ONLY valid JSON with this exact structure:
{{
  "title": "Short catchy YouTube title max 60 chars featuring Tobias",
  "description": "YouTube description 2-3 sentences include hashtags #kidsshorts #nurseryhymes #toddlerlearning #tobias",
  "tags": ["nursery rhyme", "kids", "toddler", "Tobias", "Samuel", "brothers", "educational", "cartoon"],
  "theme": "{theme}",
  "voiceover": "Complete voiceover text, rhythmic and fun, 300-350 words, simple language for ages 2-6. Both Tobias and Samuel are heroes. Use their names often.",
  "scenes": [
    {{
      "id": 1,
      "image_prompt": "Scene-specific description only (characters are auto-included). Describe: setting, action, mood, background, lighting. Example: 'Sunny farm yard with red barn, Tobias pointing excitedly at a cow, Samuel laughing beside him, warm golden light'",
      "caption": "Short screen caption max 6 words"
    }}
  ]
}}

Requirements:
- Exactly 10 scenes
- Both Tobias and Samuel must appear in every scene image prompt
- Happy positive content only, no scary elements
- Simple repetitive language toddlers love
- Each image_prompt must specify Tobias and bright Pixar cartoon style, vivid colors, no text
- Return ONLY the JSON, no other text"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())
