import json
import random
import anthropic
import config

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def generate_script() -> dict:
    theme = random.choice(config.THEMES)

    prompt = f"""Generate a 1-minute kids nursery rhyme YouTube Short script about: {theme}

Return ONLY valid JSON with this exact structure:
{{
  "title": "Short catchy YouTube title max 60 chars",
  "description": "YouTube description 2-3 sentences include hashtags #kidsshorts #nurseryhymes #toddlerlearning",
  "tags": ["nursery rhyme", "kids", "toddler", "shorts", "educational"],
  "theme": "{theme}",
  "voiceover": "Complete voiceover text, rhythmic and fun, 130-160 words, simple language for ages 2-6",
  "scenes": [
    {{
      "id": 1,
      "image_prompt": "Detailed DALL-E prompt: bright Pixar-style cartoon, specific scene description, vibrant colors, NO text in image, kids friendly, vertical composition",
      "caption": "Short screen caption max 6 words"
    }}
  ]
}}

Requirements:
- Exactly 7 scenes
- Happy positive content only, no scary elements
- Simple repetitive language toddlers love
- Each image_prompt must specify bright Pixar cartoon style, vivid colors, no text
- Return ONLY the JSON, no other text"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    return json.loads(message.content[0].text)
