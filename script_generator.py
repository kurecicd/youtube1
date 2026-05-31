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

Write EXACTLY 18 CONNECTED SCENES that form ONE continuous 3-minute story in {location}.
Every scene must be a clear continuation of the previous scene. They must feel like frames of the SAME story.

REQUIRED STORY STRUCTURE (18 scenes):
Scene 1  (INTRO):      Tobias and Samuel get ready to go, excited faces, putting on shoes/coats
Scene 2  (ARRIVAL):    They arrive at {location}, eyes wide, pointing at everything
Scene 3  (FIRST LOOK): Walking in slowly, looking around in amazement
Scene 4  (EXPLORE 1):  They discover something interesting — an animal, object, or place
Scene 5  (EXPLORE 2):  They get closer, Tobias reaches out cautiously
Scene 6  (DISCOVER):   They find something special — a baby animal, hidden spot, or surprise
Scene 7  (EXCITEMENT): Both boys react with pure joy, jumping and laughing
Scene 8  (PLAY 1):     They start playing — running, chasing, climbing, splashing
Scene 9  (PLAY 2):     Samuel shows Tobias how to do something new
Scene 10 (PLAY 3):     Tobias tries it himself, wobbly but brave
Scene 11 (PLAY 4):     They play together in perfect harmony, wide smiles
Scene 12 (PROBLEM):    Something goes wrong — Tobias slips, drops something, or gets scared
Scene 13 (WORSE):      Tobias looks upset, small tears, needs help
Scene 14 (HELP):       Samuel or Mum/Dad rushes over, arms out, coming to rescue
Scene 15 (RESCUE):     Problem is solved, Tobias looks relieved and grateful
Scene 16 (CELEBRATE):  Both boys hug and cheer, jumping with happiness
Scene 17 (WIND DOWN):  They sit together happily, tired but content, sharing a snack or rest
Scene 18 (FAREWELL):   Big waves goodbye, heading home hand in hand, both looking back smiling

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
      "story_beat": "intro",
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
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())
