import json
import random
import anthropic
import config

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def generate_script() -> dict:
    theme = random.choice(config.THEMES)

    prompt = f"""Generate a 2-3 minute kids nursery rhyme YouTube video script about: {theme}

The two main characters are brothers:
- TOBIAS — the younger brother, cute and curious, big blue eyes, red t-shirt
- SAMUEL — the older brother, taller, protective and brave, leads the way

The brothers go on a fun adventure together related to the theme. They discover things, meet animals or friends, and learn something simple. Samuel sometimes teaches Tobias, Tobias sometimes surprises Samuel.

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
      "image_prompt": "Detailed DALL-E prompt: bright Pixar-style cartoon, Tobias (younger boy, big blue eyes, red t-shirt) and Samuel (older taller boy, brave) together in specific scene, vibrant colors, NO text in image, kids friendly, vertical composition",
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
