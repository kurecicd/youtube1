import json
import random
import anthropic
import config

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

STORIES = [
    ("the sunny farm", "Tobias and Samuel visit Grandpa's farm for the first time"),
    ("the beach", "Tobias and Samuel's big beach adventure with Dad"),
    ("the forest trail", "Tobias and Samuel go on a magical forest walk"),
    ("the playground", "Tobias and Samuel discover the best playground ever"),
    ("the bakery kitchen", "Tobias and Samuel help Mum bake cookies"),
    ("the zoo", "Tobias and Samuel's amazing day at the zoo"),
    ("the garden", "Tobias and Samuel plant their first vegetable garden"),
    ("the snowy park", "Tobias and Samuel's very first snowy day"),
    ("the rainy day indoors", "Tobias and Samuel build the biggest blanket fort"),
    ("the market", "Tobias and Samuel go shopping at the colourful market"),
    ("the library", "Tobias and Samuel discover a magical book"),
    ("the swimming pool", "Tobias learns to splash with Samuel's help"),
]


def generate_script() -> dict:
    location, story_summary = random.choice(STORIES)

    prompt = f"""You are writing a children's nursery rhyme video script for YouTube (TinyTunes channel).

STORY: "{story_summary}"
SETTING: {location}

CHARACTERS (Pixar 3D cartoon style, same look in every scene):
- TOBIAS — tiny chubby toddler ~2yrs, platinum-blonde hair, huge blue eyes, blue hoodie, grey pants. Curious, giggly.
- SAMUEL — boy ~7yrs, taller, golden-blonde hair, red t-shirt, dark shorts. Brave, energetic, loves to lead.
- DAD — tall, brown hair, friendly beard, orange t-shirt. Appears in 1-2 scenes max.
- MUM — dark hair, round glasses, green cardigan. Appears in 1-2 scenes max.

Write EXACTLY 8 CONNECTED SCENES that form ONE continuous story in {location}.
Every scene must be a clear continuation of the previous scene. They must feel like frames of the SAME story.

REQUIRED STORY STRUCTURE:
Scene 1 (ARRIVAL): Tobias and Samuel arrive at {location}, pointing and laughing with excitement
Scene 2 (EXPLORE): They explore and point at something amazing they discover
Scene 3 (DISCOVER): They find something special — an animal, a treasure, a friend
Scene 4 (PLAY): They have great fun together with what they found
Scene 5 (PROBLEM): Something small goes wrong — Tobias trips, drops something, gets stuck, or is scared
Scene 6 (HELP): Samuel or Mum/Dad rush in and help solve the problem, Tobias is safe
Scene 7 (CELEBRATE): Everything is wonderful, both boys jump and cheer together
Scene 8 (FAREWELL): Happy goodbye wave, heading home, both boys look back smiling

Return ONLY valid JSON with this exact structure:
{{
  "title": "Catchy YouTube Shorts title, max 60 chars, include Tobias and Samuel",
  "description": "2-3 sentence YouTube description. Include #TinyTunes #KidsCartoon #NurseryRhyme #Toddler #KidsShorts",
  "tags": ["TinyTunes", "nursery rhyme", "kids cartoon", "toddler", "Tobias", "Samuel", "brothers", "kids songs"],
  "theme": "{location}",
  "music_prompt": "cheerful upbeat children's nursery rhyme instrumental, glockenspiel xylophone ukulele, {location} adventure theme, bright and playful, toddler-friendly, no lyrics, loop-friendly",
  "scenes": [
    {{
      "id": 1,
      "story_beat": "arrival",
      "image_prompt": "Bright Pixar 3D cartoon. {location}. Tobias (tiny chubby toddler, platinum-blonde hair, blue hoodie) and Samuel (taller boy, golden hair, red t-shirt) [describe EXACTLY what both boys are doing in this specific scene, continuing the story naturally from the previous scene]. Vivid saturated colours, warm soft lighting, joyful mood. No text in image.",
      "caption": "short caption, max 5 words"
    }}
  ]
}}

CRITICAL RULES:
- Each image_prompt must clearly describe how this scene follows from the previous one
- Both Tobias and Samuel must appear in EVERY scene
- image_prompt must mention their outfits (blue hoodie for Tobias, red t-shirt for Samuel) for character consistency
- Happy content only, nothing scary, nothing sad that isn't quickly resolved
- Return ONLY the JSON, absolutely no other text"""

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
