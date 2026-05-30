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
      "image_prompt": "Detailed DALL-E prompt: bright Pixar-style cartoon, Tobias (tiny toddler, bright blonde hair, big blue eyes, chubby cheeks) and Samuel (older boy ~7yrs, taller, blonde hair, energetic) together in specific scene. Dad (tall, dark hair, beard) or Mum (dark hair, glasses, kind smile) may appear. Vibrant colors, NO text in image, kids friendly, vertical 9:16 composition",
      "caption": "Short screen caption max 6 words"
    }}
  ]
}}

Requirements:
- Exactly 14 scenes
- Both Tobias and Samuel must appear in every scene image prompt
- Happy positive content only, no scary elements
- Simple repetitive language toddlers love
- Each image_prompt must specify Tobias and bright Pixar cartoon style, vivid colors, no text
- Return ONLY the JSON, no other text"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    return json.loads(message.content[0].text)
